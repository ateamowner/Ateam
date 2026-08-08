"""Negative tests. A linter that never fires is worse than no linter."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from autopilot import config as cfg
from autopilot.lint import lint

SETTINGS = cfg.load()

# Each case is (label, text, platform, bucket, rule expected to fire).
CASES = [
    (
        "banned phrase",
        "Let's circle back on getting your driveway washed.",
        "facebook", "", "banned-phrase",
    ),
    (
        "leverage as a verb",
        "We leverage hot water to lift the stain right out.",
        "facebook", "", "banned-phrase",
    ),
    (
        "one-man operation",
        "We are a one-man operation and proud of it.",
        "facebook", "", "banned-phrase",
    ),
    (
        "em dash",
        "Softwash is the answer — low pressure, every time.",
        "facebook", "", "em-dash",
    ),
    (
        "stacked exclamation",
        "That driveway came back white!!",
        "facebook", "", "stacked-exclamation",
    ),
    (
        "too many emoji",
        "Driveway done \U0001F9FC\U0001F9FC\U0001F9FC and it looks great.",
        "facebook", "", "emoji",
    ),
    (
        "hashtags outside instagram",
        "Driveway done in Tipp City. #PressureWashing",
        "facebook", "", "hashtags",
    ),
    (
        "too many hashtags on instagram",
        "Clean. #a #b #c #d #e #f",
        "instagram feed", "", "hashtags",
    ),
    (
        "phone in google business body",
        "Window cleaning in Tipp City, call us at (937) 939-2936 to book today.",
        "google business profile", "", "phone-in-body",
    ),
    (
        "phone in nextdoor body",
        "Neighbors in Centerville, reach me on 937-939-2936 any time.",
        "nextdoor", "", "phone-in-body",
    ),
    (
        "google business hook missing city",
        "We had a great day out there doing some work on a house that needed it badly.",
        "google business profile", "", "gbp-hook",
    ),
    (
        "nextdoor with no neighborhood",
        "Washed a driveway today and it came out great. Let me know if you want one.",
        "nextdoor", "", "nextdoor-local",
    ),
    (
        "clean club called a contract",
        "Clean Club is a simple contract that runs all year.",
        "facebook", "", "clean-club",
    ),
    (
        "undated scarcity on an offer",
        "Roof softwash special, limited time only. Send us a message.",
        "facebook", "Offer", "undated-scarcity",
    ),
]


def run() -> int:
    failures = 0
    for label, text, platform, bucket, expected in CASES:
        rules = {v.rule for v in lint(text, platform, SETTINGS, bucket=bucket)}
        if expected in rules:
            print(f"  ok    {label}")
        else:
            failures += 1
            print(f"  FAIL  {label}: expected {expected!r}, got {sorted(rules) or 'nothing'}")

    # A clean post must stay clean, or the rules are too eager to fire.
    clean = (
        "Washed a driveway over in Centerville today. Twelve years of tire marks "
        "and it came back almost white. Comment your street and I will take a look."
    )
    noise = lint(clean, "nextdoor", SETTINGS)
    if noise:
        failures += 1
        print(f"  FAIL  false positive on clean copy: {[str(v) for v in noise]}")
    else:
        print("  ok    clean copy passes untouched")

    print(f"\n{'FAIL' if failures else 'OK'}  {len(CASES) + 1} cases, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
