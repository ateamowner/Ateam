"""Opening a file safely, whatever the name on it claims.

The Drive folder is full of iPhone HEIF images called .png, JPEGs called .PNG,
and files with no extension at all. Extensions are treated as decoration here.
The magic bytes decide.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

try:  # HEIF is the common case in this folder, not an edge case.
    import pillow_heif

    pillow_heif.register_heif_opener()
    HEIF_AVAILABLE = True
except ImportError:  # pragma: no cover - environment without the codec
    HEIF_AVAILABLE = False


class UnreadableImage(Exception):
    """Raised when a file is not an image we can open."""


# (offset, signature, format name)
_SIGNATURES: list[tuple[int, bytes, str]] = [
    (0, b"\x89PNG\r\n\x1a\n", "PNG"),
    (0, b"\xff\xd8\xff", "JPEG"),
    (0, b"GIF87a", "GIF"),
    (0, b"GIF89a", "GIF"),
    (0, b"BM", "BMP"),
    (0, b"II*\x00", "TIFF"),
    (0, b"MM\x00*", "TIFF"),
    (8, b"WEBP", "WEBP"),
    # HEIF/HEIC brands live in the ftyp box at offset 4.
    (4, b"ftypheic", "HEIF"),
    (4, b"ftypheix", "HEIF"),
    (4, b"ftyphevc", "HEIF"),
    (4, b"ftypmif1", "HEIF"),
    (4, b"ftypmsf1", "HEIF"),
    (4, b"ftypavif", "AVIF"),
]

_VIDEO_SIGNATURES: list[tuple[int, bytes, str]] = [
    (4, b"ftypisom", "MP4"),
    (4, b"ftypmp4", "MP4"),
    (4, b"ftypM4V", "MP4"),
    (4, b"ftypqt", "MOV"),
]


def sniff(path: Path) -> str | None:
    """Return the real format from the file's leading bytes, or None."""
    with open(path, "rb") as fh:
        head = fh.read(32)

    for offset, sig, name in _SIGNATURES + _VIDEO_SIGNATURES:
        if head[offset : offset + len(sig)] == sig:
            return name
    return None


def is_video(path: Path) -> bool:
    fmt = sniff(path)
    return fmt in {"MP4", "MOV"}


@dataclass
class Loaded:
    image: Image.Image
    real_format: str
    claimed_extension: str
    # True when the extension lied about what the file actually is.
    mislabeled: bool


def load(path: Path) -> Loaded:
    """Open an image with rotation already applied.

    exif_transpose runs here, before this function returns, so no caller can
    ever receive a pre-transpose image. Every crop, resize, hash and paste
    downstream sees upright pixels. This is the failure that has bitten this
    project before, and the fix belongs at the boundary rather than in each
    call site.
    """
    real = sniff(path)
    if real is None:
        raise UnreadableImage(f"{path.name}: not a recognised image format")
    if real in {"MP4", "MOV"}:
        raise UnreadableImage(f"{path.name}: video, not an image")
    if real in {"HEIF", "AVIF"} and not HEIF_AVAILABLE:
        raise UnreadableImage(
            f"{path.name}: HEIF file but pillow-heif is not installed"
        )

    try:
        img = Image.open(path)
        img.load()
    except Exception as exc:  # noqa: BLE001 - Pillow raises many types
        raise UnreadableImage(f"{path.name}: {exc}") from exc

    img = ImageOps.exif_transpose(img)

    ext = path.suffix.lower().lstrip(".")
    claimed = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "heic": "HEIF"}.get(ext)

    return Loaded(
        image=img,
        real_format=real,
        claimed_extension=ext,
        mislabeled=bool(ext) and claimed is not None and claimed != real,
    )
