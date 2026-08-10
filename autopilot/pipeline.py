"""The photo pipeline: watch, sniff, normalize, dedupe, gate, classify, archive.

Runs over a local directory today. The Drive source drops in behind the same
`iter_files` interface once the service account exists, which is why nothing
below imports a Google client.

    python -m autopilot.pipeline <directory>
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from . import config as cfg
from .images import compose, quality
from .images.load import UnreadableImage, is_video, load, sniff
from .state import Manifest, PhotoRecord

# --- filename classification ----------------------------------------------

# Ant's own naming, when he uses it, is better ground truth than anything a
# model would infer: "PW driveway Centerville" carries service, subject and
# city for free. It is a seed, never a dependency: half the folder is
# IMG_0228.PNG.
_SERVICE_PATTERNS: list[tuple[str, str]] = [
    (r"\bsoft ?wash|\bsw\b", "softwash"),
    (r"\bpressure ?wash|\bpower ?wash|\bpw\b", "pressure_wash"),
    (r"\bwindow", "window"),
    (r"\bgutter", "gutter"),
    (r"\broof|\bfacia|\bfascia", "roof"),
    (r"\bfence", "fence"),
    (r"\bdeck", "deck"),
    (r"\bmold|\bmoss|\balgae", "softwash"),
]

_SUBJECT_PATTERNS: list[tuple[str, str]] = [
    (r"\bdriveway", "driveway"),
    (r"\bwalkway|\bsidewalk|\bpath", "walkway"),
    (r"\bpatio|\bpaver", "patio"),
    (r"\bsiding|\bgable|\bhouse", "siding"),
    (r"\broof", "roof"),
    (r"\bgutter", "gutter"),
    (r"\bwindow", "windows"),
    (r"\bfence", "fence"),
    (r"\bconcrete", "concrete"),
]

_BEFORE = re.compile(r"\bbefore\b|\bb4\b", re.IGNORECASE)
_AFTER = re.compile(r"\bafter\b", re.IGNORECASE)
_BEFORE_AFTER = re.compile(r"before ?and ?after|beforeafter|b ?& ?a", re.IGNORECASE)


@dataclass
class Tags:
    service: str = ""
    subject: str = ""
    city: str = ""
    phase: str = ""      # before | after | both | ""
    source: str = "filename"

    @property
    def is_bare(self) -> bool:
        """True when the filename told us nothing, so vision has to carry it."""
        return not (self.service or self.subject or self.city or self.phase)


def classify_from_name(name: str, neighborhoods: list[str]) -> Tags:
    low = name.lower().replace("_", " ").replace("-", " ")
    tags = Tags()

    for pattern, value in _SERVICE_PATTERNS:
        if re.search(pattern, low):
            tags.service = value
            break
    for pattern, value in _SUBJECT_PATTERNS:
        if re.search(pattern, low):
            tags.subject = value
            break
    for hood in neighborhoods:
        # "Carraige trails Tipp city" is spelled as Ant types it, not as the
        # city list spells it, so match loosely on the city token.
        if hood.lower() in low:
            tags.city = hood
            break

    if _BEFORE_AFTER.search(low):
        tags.phase = "both"
    elif _AFTER.search(low):
        tags.phase = "after"
    elif _BEFORE.search(low):
        tags.phase = "before"

    return tags


# --- ingest ----------------------------------------------------------------


@dataclass
class Outcome:
    path: Path
    status: str                       # accepted | composite | duplicate | rejected | video | unreadable | blocked
    detail: str = ""
    tags: Tags = field(default_factory=Tags)
    record: PhotoRecord | None = None


def iter_files(root: Path) -> list[Path]:
    """Every file under root, recursively.

    Recursive on purpose. The Job Photos folder is empty at the top level and
    the photos live in a `Before and after` subfolder, so a flat listing would
    find nothing and report success forever.
    """
    return sorted(p for p in root.rglob("*") if p.is_file())


def ingest(
    root: Path,
    settings: cfg.Settings,
    manifest: Manifest | None = None,
) -> list[Outcome]:
    manifest = manifest if manifest is not None else Manifest.load()
    photo_cfg = settings.data["photos"]
    video_cfg = settings.data.get("video", {})
    blocked_ids = {b["drive_file_id"] for b in settings.data.get("blocklist", [])}
    # Matched on the stem, not the full name. Extensions lie all over this
    # folder, and a blocked asset re-saved as .PNG instead of .JPG is still the
    # same blocked asset.
    blocked_stems = {
        Path(b["name"]).stem.lower() for b in settings.data.get("blocklist", [])
    }

    outcomes: list[Outcome] = []
    seen_this_batch: dict[int, Path] = {}

    for path in iter_files(root):
        file_id = path.name  # local runs key on name; Drive runs key on file ID

        if file_id in blocked_ids or path.stem.lower() in blocked_stems:
            outcomes.append(Outcome(path, "blocked", "on the publish blocklist"))
            continue

        if sniff(path) is None:
            outcomes.append(Outcome(path, "unreadable", "unrecognised format"))
            continue

        if is_video(path):
            detail = "catalogued, video is parked for v1"
            if video_cfg.get("catalogue_when_disabled", True):
                if manifest.get(file_id) is None:
                    manifest.add(
                        PhotoRecord(
                            file_id=file_id, name=path.name, phash="0",
                            real_format=sniff(path) or "", kind="video",
                            note="video parked, decisions.video_in_v1",
                        )
                    )
            outcomes.append(Outcome(path, "video", detail))
            continue

        try:
            loaded = load(path)
        except UnreadableImage as exc:
            outcomes.append(Outcome(path, "unreadable", str(exc)))
            continue

        img = loaded.image
        digest = quality.phash(img)

        prior = manifest.near_duplicate(digest)
        if prior is not None and prior.file_id != file_id:
            outcomes.append(
                Outcome(path, "duplicate", f"near-identical to {prior.name}")
            )
            continue
        if digest in seen_this_batch:
            outcomes.append(
                Outcome(
                    path, "duplicate",
                    f"near-identical to {seen_this_batch[digest].name} in this batch",
                )
            )
            continue
        seen_this_batch[digest] = path

        tags = classify_from_name(path.name, settings.neighborhoods)

        comp = quality.detect_composite(img)
        if comp.is_composite:
            tags.phase = tags.phase or "both"
            record = manifest.get(file_id) or manifest.add(
                PhotoRecord(
                    file_id=file_id, name=path.name, phash=f"{digest:016x}",
                    real_format=loaded.real_format, width=img.width, height=img.height,
                    kind="composite", note=comp.reason,
                )
            )
            outcomes.append(
                Outcome(path, "composite", comp.reason, tags, record)
            )
            continue

        assessment = quality.assess(img, blur_min=photo_cfg["blur_laplacian_min"])
        if not assessment.usable:
            outcomes.append(
                Outcome(path, "rejected", "; ".join(assessment.problems), tags)
            )
            continue

        record = manifest.get(file_id) or manifest.add(
            PhotoRecord(
                file_id=file_id, name=path.name, phash=f"{digest:016x}",
                real_format=loaded.real_format, width=img.width, height=img.height,
                kind="photo",
                note="extension mislabeled" if loaded.mislabeled else "",
            )
        )
        outcomes.append(Outcome(path, "accepted", "", tags, record))

    return outcomes


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2

    root = Path(argv[1])
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 2

    settings = cfg.load()
    manifest = Manifest()
    outcomes = ingest(root, settings, manifest)

    order = ["accepted", "composite", "duplicate", "rejected", "video", "blocked", "unreadable"]
    by_status: dict[str, list[Outcome]] = {k: [] for k in order}
    for o in outcomes:
        by_status.setdefault(o.status, []).append(o)

    for status in order:
        items = by_status.get(status) or []
        if not items:
            continue
        print(f"\n{status.upper()}  ({len(items)})")
        for o in items:
            bits = []
            if o.tags.service:
                bits.append(o.tags.service)
            if o.tags.subject:
                bits.append(o.tags.subject)
            if o.tags.city:
                bits.append(o.tags.city)
            tag_str = f"  [{', '.join(bits)}]" if bits else ""
            detail = f"  {o.detail}" if o.detail else ""
            print(f"  {o.path.name}{tag_str}{detail}")

    bare = [o for o in outcomes if o.status in {"accepted", "composite"} and o.tags.is_bare]
    if bare:
        print(
            f"\n{len(bare)} file(s) had no usable filename signal and will need "
            "vision classification"
        )

    print(f"\n{len(outcomes)} file(s) examined, {len(by_status.get('accepted') or [])} accepted")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
