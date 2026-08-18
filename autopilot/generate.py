"""The copywriter: turns a real job into a post that sounds like Ant.

Every draft goes through the same rules the linter enforces, and a violation
triggers a rewrite with the specific problem fed back. Ant never sees a draft
that breaks a rule, which is the whole point of the loop.

    python -m autopilot.generate --preview        # generate one of each bucket
    python -m autopilot.generate --preview --dry  # no API call, show the prompts
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field

from . import config as cfg
from .lint import Violation, carries_price, lint, specificity

MODEL = "claude-opus-5"
# A caption is deliberately short. This is a ceiling, not a target.
MAX_TOKENS = 2000
MAX_ATTEMPTS = 4


class GenerationError(Exception):
    """Raised when no draft cleared the rules within the attempt budget."""


@dataclass
class Job:
    """The real job a post is anchored to.

    The pattern behind the examples Ant approved is that every post reports
    something specific. This is where that specificity comes from, so a field
    left empty is a post that will read thin.
    """

    service: str = ""            # softwash, pressure_wash, window, gutter, roof
    subject: str = ""            # siding, driveway, walkway, gutters, windows
    city: str = ""               # must be one of the configured neighborhoods
    street: str = ""             # optional, sharpens Nextdoor posts considerably
    when: str = ""               # "Tuesday", "last week", "this morning"
    duration: str = ""           # "two hours", "ninety minutes"
    detail: str = ""             # what made this job worth telling someone about
    quote: str = ""              # anything the homeowner actually said
    image_kind: str = ""         # composite | pair | single | none

    def brief(self) -> str:
        rows = [
            ("service", self.service),
            ("subject", self.subject),
            ("city", self.city),
            ("street", self.street),
            ("when", self.when),
            ("how long", self.duration),
            ("what happened", self.detail),
            ("homeowner said", self.quote),
        ]
        lines = [f"- {label}: {value}" for label, value in rows if value]
        return "\n".join(lines) if lines else "- no job details supplied"


@dataclass
class Draft:
    text: str
    bucket: str
    platform: str
    attempts: int
    anchors: list[str] = field(default_factory=list)
    needs_explicit_approval: bool = False


def build_system(settings: cfg.Settings) -> list[dict]:
    """The stable instruction prefix, cached across every post in a run.

    Ordering matters: voice and brand never change between calls, so they sit
    at the front behind a cache breakpoint. Anything that varies per post goes
    in the user turn, after the breakpoint, or the cache never hits.
    """
    rules = f"""You write social posts for A-Team Contracting, a family-owned exterior \
cleaning company in Tipp City, Ohio, serving greater Dayton. You are writing as the \
owner, Anthony "Ant" Leonard.

Two documents follow. The voice guide is the specification, not a suggestion. The \
examples in it were approved by Ant himself, and matching how they sound matters more \
than any instruction you might infer on your own.

=== VOICE GUIDE ===
{settings.voice.raw}

=== BRAND GUIDE ===
{settings.brand}

=== OUTPUT ===
Return only the post text. No preamble, no explanation, no surrounding quotes, no \
subject line. What you return is published verbatim."""

    return [{"type": "text", "text": rules, "cache_control": {"type": "ephemeral"}}]


def build_request(job: Job, bucket: str, platform: str, settings: cfg.Settings) -> str:
    ladder = settings.data["offer_ladder"]
    rung_hint = {
        "proof": "Move the reader from noticing to asking. Rung 1 or 2.",
        "education": "Seed the problem so the reader recognises it on their own house.",
        "offer": f"Name the offer plainly. {ladder['rung_2']['role']}",
        "local": "Neighbor first. The service is secondary to the story.",
        "family": "Family owned is the moat. No selling.",
        "clean club": f"Rung 3. {ladder['rung_3']['role']}",
    }.get(bucket.lower(), "")

    rules = settings.platform_rules(
        {"instagram feed": "instagram", "instagram story": "instagram",
         "google business profile": "google_business"}.get(platform.lower(), platform.lower())
    )

    constraints = []
    if rules.get("allow_phone_in_body") is False:
        constraints.append("No phone number anywhere in the text.")
    if rules.get("require_service_and_city_in_first_sentence"):
        constraints.append(
            f"Name the service and the city inside the first "
            f"{rules.get('visible_chars', 100)} characters. Only that much shows "
            "before Google truncates it."
        )
    if rules.get("require_neighborhood_mention"):
        constraints.append("Name the neighborhood or the road.")
    if rules.get("max_hashtags"):
        constraints.append(f"Exactly {rules['max_hashtags']} hashtags at the end.")
    else:
        constraints.append("No hashtags.")

    return f"""Write one {bucket} post for {platform}.

{rung_hint}

The job:
{job.brief()}

Platform constraints:
{chr(10).join('- ' + c for c in constraints)}

Anchor the post in the job above. Do not invent details that are not listed. If a \
detail you want is missing, write around it rather than making it up."""


def _feedback(problems: list[Violation], anchors_needed: bool) -> str:
    lines = ["That draft cannot publish. Fix these and return the full post again:"]
    lines += [f"- {p}" for p in problems]
    if anchors_needed:
        lines.append(
            "- too abstract: it needs at least two concrete anchors from the job "
            "above, or a specific mechanic of how the service works"
        )
    return "\n".join(lines)


def generate(
    job: Job,
    bucket: str,
    platform: str,
    settings: cfg.Settings,
    client=None,
    max_attempts: int = MAX_ATTEMPTS,
) -> Draft:
    """Write one post, rewriting until it clears every rule."""
    if client is None:
        import anthropic

        client = anthropic.Anthropic()

    system = build_system(settings)
    messages = [{"role": "user", "content": build_request(job, bucket, platform, settings)}]

    last_problems: list[Violation] = []
    for attempt in range(1, max_attempts + 1):
        text = _call(client, system, messages, settings)

        problems = lint(text, platform, settings, bucket=bucket)
        spec = specificity(text, settings)

        if not problems and spec.grounded:
            return Draft(
                text=text,
                bucket=bucket,
                platform=platform,
                attempts=attempt,
                anchors=spec.anchors,
                # One rule, owned by the config, so the generator and the
                # scheduler can never disagree about what may publish itself.
                needs_explicit_approval=settings.needs_explicit_approval(
                    bucket, has_price=carries_price(text)
                ),
            )

        last_problems = problems
        messages += [
            {"role": "assistant", "content": text},
            {"role": "user", "content": _feedback(problems, not spec.grounded)},
        ]

    raise GenerationError(
        f"{max_attempts} attempts, still failing: "
        + "; ".join(str(p) for p in last_problems)
    )


def _bad_request_type():
    """anthropic.BadRequestError, or a type that never matches if unavailable."""
    try:
        import anthropic

        return anthropic.BadRequestError
    except ImportError:
        class _Never(Exception):
            pass

        return _Never


def _call(client, system, messages, settings) -> str:
    """One API call, with the refusal fallback enabled where supported."""
    kwargs = dict(model=MODEL, max_tokens=MAX_TOKENS, system=system, messages=messages)

    want_fallback = settings.data.get("generation", {}).get("refusal_fallback", True)
    if want_fallback and getattr(client, "beta", None) is not None:
        try:
            return _text_of(
                client.beta.messages.create(
                    betas=["server-side-fallback-2026-07-01"],
                    fallbacks="default",
                    **kwargs,
                )
            )
        except _bad_request_type() as exc:
            # Cannot be exercised without a live key, so it degrades to the
            # plain call instead of taking the whole run down.
            print(f"  note: refusal fallback rejected ({exc}), retrying without it")

    return _text_of(client.messages.create(**kwargs))


def _text_of(response) -> str:
    if getattr(response, "stop_reason", None) == "refusal":
        detail = getattr(response, "stop_details", None)
        raise GenerationError(
            f"model declined to write this post "
            f"({getattr(detail, 'category', 'no category given')})"
        )
    parts = [b.text for b in response.content if b.type == "text"]
    return "\n".join(parts).strip()


# --- preview ---------------------------------------------------------------

# Drawn from files actually in the Drive folder, so the preview shows what the
# system will really produce rather than a demo.
SAMPLE_JOBS: list[tuple[Job, str, str]] = [
    (
        Job(service="softwash", subject="siding", city="Tipp City",
            street="Carriage Trails", when="Tuesday", duration="two hours",
            detail="green algae up the whole north side, homeowner thought the siding "
                   "was stained for good and was pricing replacement",
            quote="that's the same house?", image_kind="composite"),
        "Proof", "Facebook",
    ),
    (
        Job(service="gutter", subject="gutters", city="Huber Heights",
            when="Thursday", detail="packed with shingle grit and maple seeds, "
            "flushed the downspouts and checked the seams while up there",
            image_kind="composite"),
        "Proof", "Google Business Profile",
    ),
    (
        Job(service="pressure_wash", subject="driveway", city="Centerville",
            street="Far Hills", when="Thursday",
            detail="twelve years of tire marks and a little oil, came back almost "
                   "white, three neighbors wandered over to ask what we were using"),
        "Local", "Nextdoor",
    ),
    (
        Job(service="roof", subject="roof", city="Fairborn", when="last week",
            detail="homeowner asked why the north face was black and the south was "
                   "clean, it is Gloeocapsa magma and it sits where the moisture does"),
        "Education", "Facebook",
    ),
    (
        Job(service="window", subject="windows", city="Tipp City",
            detail="booked for glass, homeowner walked us round back and pointed at "
                   "the siding, so we bundled it into one trip"),
        "Offer", "Facebook",
    ),
]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="generate sample posts")
    parser.add_argument("--dry", action="store_true", help="print prompts, call nothing")
    args = parser.parse_args(argv[1:])

    settings = cfg.load()

    if args.dry:
        system = build_system(settings)
        print(f"system prompt: {len(system[0]['text']):,} characters, cached\n")
        job, bucket, platform = SAMPLE_JOBS[0]
        print(build_request(job, bucket, platform, settings))
        return 0

    if not args.preview:
        parser.print_help()
        return 2

    failures = 0
    for job, bucket, platform in SAMPLE_JOBS:
        print(f"\n{'=' * 68}\n{bucket} / {platform}\n{'=' * 68}")
        try:
            draft = generate(job, bucket, platform, settings)
        except GenerationError as exc:
            failures += 1
            print(f"FAILED: {exc}")
            continue
        print(draft.text)
        note = f"\n[{draft.attempts} attempt(s), anchors: {', '.join(draft.anchors)}"
        if draft.needs_explicit_approval:
            note += ", needs Ant's explicit yes"
        print(note + "]")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
