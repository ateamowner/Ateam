"""The week: which slot, which bucket, which platform, at what Ohio time.

Slots come from the cadence block, never from a hardcoded list, so the 34-a-week
arithmetic in the architecture notes cannot drift from what actually runs.

    python -m autopilot.schedule            # next week's plan
    python -m autopilot.schedule 2026-08-24 # a specific week
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from . import config as cfg

DAY_INDEX = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}

# Nextdoor punishes anything that reads like an ad, so the offer bucket never
# lands there. Google Business is a local-SEO surface and family posts do
# nothing for it. These are exclusions, not preferences: the mix is rebalanced
# around them rather than quietly violated.
BUCKET_EXCLUSIONS: dict[str, set[str]] = {
    "nextdoor": {"offer"},
    "google_business": {"family"},
}


@dataclass(frozen=True)
class Slot:
    when: datetime               # timezone-aware, America/New_York
    platform: str
    derived_from: str = ""       # set on stories, which reuse the feed post

    @property
    def is_derived(self) -> bool:
        return bool(self.derived_from)

    def __str__(self) -> str:
        return f"{self.when:%a %d %b %H:%M} {self.platform}"


@dataclass(frozen=True)
class PlannedPost:
    slot: Slot
    bucket: str

    def __str__(self) -> str:
        return f"{self.slot}  {self.bucket}"


def week_start(day: date) -> date:
    """The Monday of the week containing `day`."""
    return day - timedelta(days=day.weekday())


def week_slots(monday: date, settings: cfg.Settings) -> list[Slot]:
    """Every publish slot for the week beginning on `monday`.

    Times are built in Ohio local time, so a slot keeps its wall-clock hour
    across a daylight-saving boundary rather than drifting by an hour.
    """
    tz = ZoneInfo(settings.timezone)
    slots: list[Slot] = []

    for platform, spec in settings.data["cadence"].items():
        days = spec.get("days")
        day_offsets = (
            [DAY_INDEX[d] for d in days] if days else list(range(7))
        )
        for offset in day_offsets:
            for hhmm in spec["times"]:
                hour, minute = (int(p) for p in hhmm.split(":"))
                when = datetime.combine(
                    monday + timedelta(days=offset), time(hour, minute), tzinfo=tz
                )
                slots.append(
                    Slot(
                        when=when,
                        platform=platform,
                        derived_from=spec.get("derived_from", ""),
                    )
                )

    _enforce_caps(slots, settings)
    return sorted(slots, key=lambda s: (s.when, s.platform))


def _enforce_caps(slots: list[Slot], settings: cfg.Settings) -> None:
    for platform, spec in settings.data["cadence"].items():
        cap = spec.get("hard_cap_per_week")
        if cap is None:
            continue
        count = sum(1 for s in slots if s.platform == platform)
        if count > cap:
            raise cfg.ConfigError(
                f"{platform} would post {count} times this week, cap is {cap}"
            )


def bucket_counts(originals: int, settings: cfg.Settings) -> dict[str, int]:
    """Split `originals` posts across the mix, summing exactly.

    Largest remainder, so the shares land deterministically and always total
    the number of slots. Rounding each share independently does not.
    """
    mix = settings.data["content_mix"]
    exact = {k: originals * v for k, v in mix.items()}
    counts = {k: int(v) for k, v in exact.items()}

    short = originals - sum(counts.values())
    by_remainder = sorted(
        exact, key=lambda k: (exact[k] - counts[k], mix[k]), reverse=True
    )
    for k in by_remainder[:short]:
        counts[k] += 1
    return counts


def assign_buckets(slots: list[Slot], settings: cfg.Settings) -> list[PlannedPost]:
    """Give every original slot a bucket, honouring the mix and the exclusions.

    Derived slots (Instagram stories) inherit their feed post rather than
    consuming a bucket of their own, which is why the mix is computed against
    originals only.
    """
    originals = [s for s in slots if not s.is_derived]
    derived = [s for s in slots if s.is_derived]

    remaining = bucket_counts(len(originals), settings)
    planned: list[PlannedPost] = []

    # Hardest slots first. A slot that excludes two buckets has to be served
    # before the buckets it can accept are spent elsewhere.
    order = sorted(
        originals,
        key=lambda s: (-len(BUCKET_EXCLUSIONS.get(s.platform, set())), s.when),
    )

    last_by_platform: dict[str, str] = {}
    for slot in order:
        banned = BUCKET_EXCLUSIONS.get(slot.platform, set())
        options = [b for b, n in remaining.items() if n > 0 and b not in banned]
        if not options:
            raise cfg.ConfigError(
                f"no bucket left for {slot}; the mix cannot satisfy the exclusions"
            )
        # Prefer the most-remaining bucket, and avoid repeating what this
        # platform ran last so a feed does not read as three offers in a row.
        options.sort(
            key=lambda b: (b == last_by_platform.get(slot.platform), -remaining[b], b)
        )
        chosen = options[0]
        remaining[chosen] -= 1
        last_by_platform[slot.platform] = chosen
        planned.append(PlannedPost(slot=slot, bucket=chosen))

    by_day_platform = {
        (p.slot.when.date(), p.slot.platform): p.bucket for p in planned
    }
    for slot in derived:
        # A story mirrors that day's feed post, falling back to proof if the
        # feed slot is missing for some reason.
        bucket = by_day_platform.get((slot.when.date(), slot.derived_from), "proof")
        planned.append(PlannedPost(slot=slot, bucket=bucket))

    return sorted(planned, key=lambda p: (p.slot.when, p.slot.platform))


def plan_week(monday: date, settings: cfg.Settings) -> list[PlannedPost]:
    return assign_buckets(week_slots(monday, settings), settings)


def summarise(planned: list[PlannedPost]) -> str:
    originals = [p for p in planned if not p.slot.is_derived]
    counts: dict[str, int] = {}
    for p in originals:
        counts[p.bucket] = counts.get(p.bucket, 0) + 1
    per_platform: dict[str, int] = {}
    for p in planned:
        per_platform[p.slot.platform] = per_platform.get(p.slot.platform, 0) + 1

    lines = [
        f"{len(planned)} pieces, {len(originals)} originals, "
        f"{len(planned) - len(originals)} derived",
        "  platforms: " + ", ".join(f"{k} {v}" for k, v in sorted(per_platform.items())),
        "  mix:       " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())),
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    settings = cfg.load()
    if len(argv) > 1:
        monday = week_start(date.fromisoformat(argv[1]))
    else:
        monday = week_start(date.today()) + timedelta(days=7)

    planned = plan_week(monday, settings)

    print(f"Week of {monday:%A %d %B %Y}\n")
    for p in planned:
        derived = "  (from the feed post)" if p.slot.is_derived else ""
        print(f"  {p}{derived}")
    print()
    print(summarise(planned))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
