"""Step 2 verification: load every config input and lint the voice examples.

    python -m autopilot.check

Exits non-zero if configuration is invalid or any example post breaks a rule.
This is what proves the Step 2 files are consistent with each other rather than
just present.
"""

from __future__ import annotations

import sys

from . import config as cfg
from .lint import lint


def main() -> int:
    try:
        settings = cfg.load()
    except cfg.ConfigError as exc:
        print(f"FAIL  config: {exc}")
        return 1

    print("config.yaml    loaded and validated")

    counts = settings.weekly_post_counts()
    total = sum(counts.values())
    detail = ", ".join(f"{k} {v}" for k, v in counts.items())
    print(f"cadence        {total} pieces per week ({detail})")

    mix = settings.data["content_mix"]
    originals = total - counts["instagram_story"]
    mix_detail = ", ".join(f"{k} {round(v * originals)}" for k, v in mix.items())
    print(f"content mix    {originals} originals ({mix_detail})")

    print(f"brand.md       {len(settings.brand.splitlines())} lines")
    print(f"banned.txt     {len(settings.banned_phrases)} phrases")

    examples = settings.voice.examples
    print(f"voice.md       {len(examples)} example posts")

    if len(examples) != 10:
        print(f"FAIL  voice: expected 10 examples, parsed {len(examples)}")
        return 1

    failures = 0
    for ex in examples:
        problems = lint(ex.body, ex.platform, settings, bucket=ex.bucket)
        label = f"  {ex.index:>2}. {ex.bucket} / {ex.platform}"
        if problems:
            failures += 1
            print(f"{label}  FAIL")
            for p in problems:
                print(f"        {p}")
        else:
            print(f"{label}  ok")

    missing = cfg.missing_credentials(settings)
    if missing:
        print(f"\ncredentials    {len(missing)} not yet set: {', '.join(missing)}")
        print("               expected at this stage, publishing is not wired up yet")

    blocked = settings.data.get("blocklist", [])
    if blocked:
        print(f"\nblocklist      {len(blocked)} asset(s) barred from publishing:")
        for b in blocked:
            print(f"  - {b['name']}  ({b['reason'].strip().splitlines()[0]}...)")

    decisions = settings.data.get("decisions", [])
    if decisions:
        print("\ndecisions on record:")
        for d in decisions:
            print(f"  {d['id']:<20} {d['choice']}   ({d['decided']})")

    open_qs = settings.data.get("open_questions", [])
    if open_qs:
        print("\nopen questions awaiting Ant:")
        for q in open_qs:
            print(f"  - {q['question']}")
            print(f"    default until answered: {q['default_until_answered']}")
    else:
        print("\nno open questions")

    if failures:
        print(f"\nFAIL  {failures} example post(s) break a rule")
        return 1

    print("\nOK  every example passes the linter")
    return 0


if __name__ == "__main__":
    sys.exit(main())
