"""Tests for the week planner."""

from __future__ import annotations

import copy
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from autopilot import config as cfg
from autopilot.schedule import (
    BUCKET_EXCLUSIONS,
    bucket_counts,
    plan_week,
    week_slots,
    week_start,
)

SETTINGS = cfg.load()
MONDAY = date(2026, 8, 24)
results: list[tuple[bool, str]] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    results.append((ok, f"{label}{'  ' + detail if detail and not ok else ''}"))


def test_the_week_matches_the_documented_cadence() -> None:
    planned = plan_week(MONDAY, SETTINGS)
    originals = [p for p in planned if not p.slot.is_derived]

    check(len(planned) == 34, "34 pieces a week", f"got {len(planned)}")
    check(len(originals) == 27, "27 of them original", f"got {len(originals)}")

    per_platform: dict[str, int] = {}
    for p in planned:
        per_platform[p.slot.platform] = per_platform.get(p.slot.platform, 0) + 1
    expected = {
        "facebook": 14, "instagram_feed": 7, "instagram_story": 7,
        "google_business": 3, "nextdoor": 3,
    }
    check(per_platform == expected, "per-platform counts match the cadence",
          f"got {per_platform}")


def test_mix_sums_exactly() -> None:
    """Rounding each share independently does not always total the slot count."""
    for n in range(1, 60):
        counts = bucket_counts(n, SETTINGS)
        if sum(counts.values()) != n:
            check(False, f"mix sums to the slot count for n={n}",
                  f"got {sum(counts.values())}")
            return
    check(True, "mix sums exactly for every slot count from 1 to 59")

    counts = bucket_counts(27, SETTINGS)
    check(counts == {"proof": 11, "education": 5, "offer": 5, "local": 3, "family": 3},
          "27 originals split as documented", f"got {counts}")


def test_exclusions_are_honoured() -> None:
    planned = plan_week(MONDAY, SETTINGS)
    for p in planned:
        banned = BUCKET_EXCLUSIONS.get(p.slot.platform, set())
        if p.bucket in banned and not p.slot.is_derived:
            check(False, f"{p.slot.platform} must never run {p.bucket}")
            return
    check(True, "no platform runs a bucket it excludes")

    nextdoor = [p.bucket for p in planned if p.slot.platform == "nextdoor"]
    check("offer" not in nextdoor, "Nextdoor never gets an offer post",
          f"got {nextdoor}")


def test_nextdoor_cap_is_enforced() -> None:
    data = copy.deepcopy(SETTINGS.data)
    data["cadence"]["nextdoor"]["days"] = ["mon", "tue", "wed", "thu"]
    loose = cfg.Settings(data=data, voice=SETTINGS.voice, brand=SETTINGS.brand,
                         banned_phrases=SETTINGS.banned_phrases)
    try:
        week_slots(MONDAY, loose)
    except cfg.ConfigError as exc:
        check("cap is 3" in str(exc), "a fourth Nextdoor slot raises", str(exc))
    else:
        check(False, "exceeding the Nextdoor cap must raise")


def test_stories_mirror_that_days_feed_post() -> None:
    planned = plan_week(MONDAY, SETTINGS)
    feed = {p.slot.when.date(): p.bucket
            for p in planned if p.slot.platform == "instagram_feed"}
    stories = [p for p in planned if p.slot.platform == "instagram_story"]

    check(len(stories) == 7, "a story every day", f"got {len(stories)}")
    mismatched = [s for s in stories if feed.get(s.slot.when.date()) != s.bucket]
    check(not mismatched, "each story carries its feed post's bucket",
          f"{len(mismatched)} mismatched")


def test_wall_clock_survives_the_daylight_saving_change() -> None:
    """US DST ends 1 Nov 2026. A 9am slot must stay 9am on both sides of it."""
    slots = week_slots(date(2026, 10, 26), SETTINGS)
    morning = [s for s in slots if s.platform == "facebook" and s.when.hour == 9]
    check(len(morning) == 7, "seven 9am Facebook slots across the DST week",
          f"got {len(morning)}")

    offsets = {s.when.utcoffset() for s in morning}
    check(len(offsets) == 2, "the UTC offset does shift mid-week",
          f"offsets {offsets}")
    check(all(s.when.minute == 0 for s in morning),
          "and the wall-clock time never drifts")


def test_planning_is_deterministic() -> None:
    a = [(str(p.slot), p.bucket) for p in plan_week(MONDAY, SETTINGS)]
    b = [(str(p.slot), p.bucket) for p in plan_week(MONDAY, SETTINGS)]
    check(a == b, "the same week plans identically twice")


def test_approval_texts_stay_out_of_family_time() -> None:
    """The brief contradicted itself: a 6pm text inside a 5-7pm quiet window."""
    import shutil
    import tempfile

    import yaml

    approvals = SETTINGS.data["approvals"]
    quiet_start, quiet_end = approvals["quiet_hours"]
    offenders = [t for t in approvals["batch_times"] if quiet_start <= t < quiet_end]
    check(not offenders, "no approval batch lands in quiet hours", f"{offenders}")

    src = Path(cfg.CONFIG_DIR)
    with tempfile.TemporaryDirectory() as td:
        dst = Path(td)
        for f in src.iterdir():
            shutil.copy(f, dst / f.name)
        data = yaml.safe_load((dst / "config.yaml").read_text())
        data["approvals"]["batch_times"] = ["07:00", "18:00"]
        (dst / "config.yaml").write_text(yaml.safe_dump(data))
        try:
            cfg.load(dst)
        except cfg.ConfigError as exc:
            check("family time" in str(exc),
                  "restoring the 6pm text is rejected at load", str(exc))
        else:
            check(False, "a batch inside quiet hours must raise")


def test_publish_times_may_sit_inside_quiet_hours() -> None:
    """An automated post interrupts nobody. Only texts to Ant are restricted."""
    planned = plan_week(MONDAY, SETTINGS)
    quiet_start, quiet_end = SETTINGS.data["approvals"]["quiet_hours"]
    inside = [p for p in planned
              if quiet_start <= f"{p.slot.when:%H:%M}" < quiet_end]
    check(bool(inside), "posts still publish during family time",
          "expected Facebook 17:30 and Nextdoor 18:00 to remain")


def test_week_start_snaps_to_monday() -> None:
    check(week_start(date(2026, 8, 27)) == date(2026, 8, 24),
          "a Thursday resolves to its Monday")
    check(week_start(date(2026, 8, 24)) == date(2026, 8, 24),
          "a Monday resolves to itself")


def run() -> int:
    test_the_week_matches_the_documented_cadence()
    test_mix_sums_exactly()
    test_exclusions_are_honoured()
    test_nextdoor_cap_is_enforced()
    test_stories_mirror_that_days_feed_post()
    test_wall_clock_survives_the_daylight_saving_change()
    test_planning_is_deterministic()
    test_approval_texts_stay_out_of_family_time()
    test_publish_times_may_sit_inside_quiet_hours()
    test_week_start_snaps_to_monday()

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
