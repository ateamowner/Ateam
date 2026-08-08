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

    # Ant's own constructions must survive. These are the false-positive cases
    # that matter most, because breaking them means the system stops sounding
    # like him.
    ant_voice = [
        (
            "?!? is his, not a violation",
            "Since when do gas stations charge $3 for air to fill tires?!? "
            "Just wasted $7.50 in Centerville on machines that were broken.",
            "nextdoor",
        ),
        (
            "facepalm counts as one emoji, not two",
            "A pressure washer alone doesn't kill mold \U0001F926‍♂️ "
            "and it's back in a season \U0001F9FC",
            "facebook",
        ),
        (
            "ellipses are his pause, not a rule break",
            "Is that just dirt on your siding?… or is mold eating away at it?",
            "facebook",
        ),
    ]
    for label, text, platform in ant_voice:
        noise = lint(text, platform, SETTINGS)
        if noise:
            failures += 1
            print(f"  FAIL  {label}: {[str(v) for v in noise]}")
        else:
            print(f"  ok    {label}")

    # Specificity: the advisory scorer that keeps drafts concrete.
    from autopilot.lint import specificity

    for ex in SETTINGS.voice.examples:
        sp = specificity(ex.body, SETTINGS)
        if sp.grounded:
            print(f"  ok    example {ex.index} is grounded ({sp.score} anchors)")
        else:
            failures += 1
            print(f"  FAIL  example {ex.index} scored {sp.score}, needs 2")

    filler = [
        "Your siding deserves the best care possible. Contact us today for a "
        "free estimate on all your exterior cleaning needs.",
        "Spring is here and that means it is time to think about your home's "
        "exterior. We are ready to help.",
    ]
    for text in filler:
        sp = specificity(text, SETTINGS)
        if sp.grounded:
            failures += 1
            print(f"  FAIL  generic filler scored {sp.score} and passed")
        else:
            print(f"  ok    generic filler rejected ({sp.score} anchors)")

    # An apostrophe is not a quotation. This scored every contraction as
    # reported speech until the pattern was narrowed to double quotes.
    contractions = "You don't have to call and we won't forget, that's the point."
    if "quote" in specificity(contractions, SETTINGS).anchors:
        failures += 1
        print("  FAIL  contractions counted as a quotation")
    else:
        print("  ok    contractions are not counted as a quotation")

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

    checks = (
        len(CASES)
        + len(ant_voice)
        + len(SETTINGS.voice.examples)
        + len(filler)
        + 2  # contractions, clean copy
    )
    print(f"\n{'FAIL' if failures else 'OK'}  {checks} cases, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
