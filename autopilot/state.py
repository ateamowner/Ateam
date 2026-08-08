"""Durable record of what the pipeline has seen and used.

Written by the pipeline, read by the scheduler. Plain JSON on purpose: it lives
in the repo, diffs readably, and survives without a database.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

from .images.quality import hamming

STATE_DIR = Path(__file__).parent / "state"
USED_PHOTOS = STATE_DIR / "used_photos.json"


@dataclass
class PhotoRecord:
    file_id: str
    name: str
    phash: str                      # hex, so JSON stays readable
    real_format: str
    width: int = 0
    height: int = 0
    kind: str = "photo"             # photo | composite | video
    first_seen: str = ""
    # Per platform, not global. One job serves Facebook, Instagram and Google
    # in the same week under different copy.
    used_on: dict[str, str] = field(default_factory=dict)
    blocked: bool = False
    note: str = ""


class Manifest:
    def __init__(self, records: list[PhotoRecord] | None = None):
        self.records: list[PhotoRecord] = records or []
        self._by_id = {r.file_id: r for r in self.records}

    # --- persistence ---

    @classmethod
    def load(cls, path: Path = USED_PHOTOS) -> "Manifest":
        if not path.exists():
            return cls()
        raw = json.loads(path.read_text(encoding="utf-8"))
        return cls([PhotoRecord(**r) for r in raw.get("photos", [])])

    def save(self, path: Path = USED_PHOTOS) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "photos": [asdict(r) for r in self.records],
        }
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    # --- queries ---

    def get(self, file_id: str) -> PhotoRecord | None:
        return self._by_id.get(file_id)

    def add(self, record: PhotoRecord) -> PhotoRecord:
        if not record.first_seen:
            record.first_seen = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self.records.append(record)
        self._by_id[record.file_id] = record
        return record

    def near_duplicate(self, digest: int, threshold: int = 5) -> PhotoRecord | None:
        """First record within `threshold` bits, or None.

        Catches re-uploads under a different name. The Drive folder has a
        confirmed byte-identical pair and eleven near-copies of one graphic,
        so this fires on real data, not hypotheticals.
        """
        for r in self.records:
            if hamming(int(r.phash, 16), digest) <= threshold:
                return r
        return None

    def available_for(self, platform: str, cooldown_days: int, today: date | None = None) -> list[PhotoRecord]:
        """Records that may be published to this platform right now."""
        today = today or datetime.now(timezone.utc).date()
        out = []
        for r in self.records:
            if r.blocked or r.kind == "video":
                continue
            last = r.used_on.get(platform)
            if last:
                age = (today - date.fromisoformat(last[:10])).days
                if age < cooldown_days:
                    continue
            out.append(r)
        return out

    def mark_used(self, file_id: str, platform: str, when: date | None = None) -> None:
        record = self._by_id.get(file_id)
        if record is None:
            raise KeyError(f"unknown photo {file_id}")
        record.used_on[platform] = (when or datetime.now(timezone.utc).date()).isoformat()
