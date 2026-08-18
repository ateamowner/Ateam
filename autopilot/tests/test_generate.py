"""Tests for the generation loop, using a fake client so no API key is needed.

The loop is the part that matters: a draft that breaks a rule must come back
rewritten, and a draft that never clears must fail loudly rather than publish.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from autopilot import config as cfg
from autopilot.generate import (
    Job,
    GenerationError,
    build_request,
    build_system,
    generate,
)

SETTINGS = cfg.load()
results: list[tuple[bool, str]] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    results.append((ok, f"{label}{'  ' + detail if detail and not ok else ''}"))


class FakeBlock:
    type = "text"

    def __init__(self, text: str):
        self.text = text


class FakeResponse:
    stop_reason = "end_turn"
    stop_details = None

    def __init__(self, text: str):
        self.content = [FakeBlock(text)]


class FakeMessages:
    def __init__(self, outbox: list[str], log: list[dict]):
        self.outbox = outbox
        self.log = log

    def create(self, **kwargs):
        self.log.append(kwargs)
        return FakeResponse(self.outbox[min(len(self.log) - 1, len(self.outbox) - 1)])


class FakeClient:
    """Returns each scripted draft in turn. Records every request it received."""

    def __init__(self, drafts: list[str]):
        self.log: list[dict] = []
        self.messages = FakeMessages(drafts, self.log)
        # The engine prefers the beta path; make it unavailable so these tests
        # exercise the plain path deterministically.
        self.beta = None


GOOD = (
    "Spent Thursday on a driveway off Far Hills in Centerville. Twelve years of "
    "tire marks and it came back almost white. Night and day.\n\n"
    "Anybody on that stretch got one you've given up on? Say the word below."
)


def test_system_prompt_carries_voice_and_brand() -> None:
    system = build_system(SETTINGS)
    text = system[0]["text"]
    check("Jobs like this are why people call us back" in text,
          "system prompt carries the voice guide")
    check("YOUR PRICE" in text, "system prompt carries the brand guide")
    check(system[0].get("cache_control") == {"type": "ephemeral"},
          "system prompt is marked for caching")


def test_request_carries_platform_constraints() -> None:
    job = Job(service="gutter", city="Huber Heights", when="Thursday")
    gbp = build_request(job, "Proof", "Google Business Profile", SETTINGS)
    check("No phone number" in gbp, "Google Business request forbids the phone number")
    check("100 characters" in gbp, "Google Business request states the visible window")
    check("Huber Heights" in gbp, "the job details reach the request")

    ig = build_request(job, "Proof", "Instagram feed", SETTINGS)
    check("Exactly 5 hashtags" in ig, "Instagram request asks for exactly 5 hashtags")

    nd = build_request(job, "Local", "Nextdoor", SETTINGS)
    check("No hashtags" in nd, "Nextdoor request forbids hashtags")
    check("No phone number" in nd, "Nextdoor request forbids the phone number")


def test_clean_draft_passes_first_time() -> None:
    client = FakeClient([GOOD])
    draft = generate(Job(city="Centerville"), "Local", "Nextdoor", SETTINGS, client=client)
    check(draft.attempts == 1, "a clean draft is accepted on the first attempt")
    check(len(client.log) == 1, "only one API call was made", f"{len(client.log)}")


def test_violation_triggers_a_rewrite_with_the_reason() -> None:
    """The banned phrase must come back to the model, not just a retry."""
    bad = (
        "Let's circle back on that driveway in Centerville on Thursday. "
        "Twelve years of marks, gone."
    )
    client = FakeClient([bad, GOOD])
    draft = generate(Job(city="Centerville"), "Local", "Nextdoor", SETTINGS, client=client)

    check(draft.attempts == 2, "a violating draft is rewritten", f"{draft.attempts}")
    second = client.log[1]["messages"]
    feedback = second[-1]["content"]
    check(second[-2]["role"] == "assistant", "the rejected draft is echoed back")
    check("circle back" in feedback, "the feedback names the offending phrase")
    check("cannot publish" in feedback, "the feedback is explicit about the outcome")


def test_thin_draft_is_rewritten_too() -> None:
    """Passing the hard rules is not enough. Abstract copy gets sent back."""
    thin = "Your siding deserves the best care. Reach out for a free estimate."
    client = FakeClient([thin, GOOD])
    draft = generate(Job(city="Centerville"), "Local", "Nextdoor", SETTINGS, client=client)
    check(draft.attempts == 2, "an abstract draft is rewritten")
    check("too abstract" in client.log[1]["messages"][-1]["content"],
          "the feedback explains it needs concrete anchors")


def test_it_gives_up_rather_than_publishing_a_violation() -> None:
    client = FakeClient(["We should circle back on this at the end of the day."])
    try:
        generate(Job(city="Centerville"), "Local", "Nextdoor", SETTINGS,
                 client=client, max_attempts=3)
    except GenerationError as exc:
        check("circle back" in str(exc), "gives up loudly and names the blocker")
        check(len(client.log) == 3, "it used the full attempt budget",
              f"{len(client.log)}")
    else:
        check(False, "a permanently violating draft must raise, not return")


def test_offer_posts_require_explicit_approval() -> None:
    offer = (
        "Window cleaning in Tipp City, booked Thursday. Homeowner had us out for "
        "glass and we bundled the driveway into one trip. One crew, one day."
    )
    client = FakeClient([offer])
    draft = generate(Job(city="Tipp City"), "Offer", "Facebook", SETTINGS, client=client)
    check(draft.needs_explicit_approval,
          "an offer post is flagged for Ant's explicit yes")

    client2 = FakeClient([GOOD])
    local = generate(Job(city="Centerville"), "Local", "Nextdoor", SETTINGS, client=client2)
    check(not local.needs_explicit_approval,
          "a local post can ride the auto-approve path")


def test_refusal_is_surfaced_not_swallowed() -> None:
    class Refusing(FakeClient):
        def __init__(self):
            super().__init__(["unused"])
            outer = self

            class M:
                def create(self, **kwargs):
                    outer.log.append(kwargs)
                    r = FakeResponse("")
                    r.stop_reason = "refusal"

                    class D:
                        category = "test-category"

                    r.stop_details = D()
                    return r

            self.messages = M()

    try:
        generate(Job(), "Proof", "Facebook", SETTINGS, client=Refusing())
    except GenerationError as exc:
        check("declined" in str(exc), "a refusal raises rather than returning empty")
    else:
        check(False, "a refusal must not be treated as a caption")


def run() -> int:
    test_system_prompt_carries_voice_and_brand()
    test_request_carries_platform_constraints()
    test_clean_draft_passes_first_time()
    test_violation_triggers_a_rewrite_with_the_reason()
    test_thin_draft_is_rewritten_too()
    test_it_gives_up_rather_than_publishing_a_violation()
    test_offer_posts_require_explicit_approval()
    test_refusal_is_surfaced_not_swallowed()

    failures = 0
    for ok, label in results:
        if ok:
            print(f"  ok    {label}")
        else:
            failures += 1
            print(f"  FAIL  {label}")
    print(f"\n{'FAIL' if failures else 'OK'}  {len(results)} checks, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
