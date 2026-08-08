"""Quality gate, perceptual hashing, and composite detection.

Three jobs that all reduce to reading pixels, kept together so they share one
grayscale conversion rather than three.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from PIL import Image

# --- perceptual hash -------------------------------------------------------

_HASH_SIZE = 8


def phash(img: Image.Image) -> int:
    """Difference hash. Robust to rescaling and mild recompression.

    Used to catch re-uploads. The Drive folder contains eleven near-identical
    copies of one graphic and a confirmed byte-identical duplicate pair, so
    this is load-bearing, not defensive.
    """
    small = img.convert("L").resize((_HASH_SIZE + 1, _HASH_SIZE), Image.LANCZOS)
    pixels = np.asarray(small, dtype=np.int16)
    diff = pixels[:, 1:] > pixels[:, :-1]
    bits = 0
    for bit in diff.flatten():
        bits = (bits << 1) | int(bit)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def looks_duplicate(a: int, b: int, threshold: int = 5) -> bool:
    """Near-duplicate, not just byte-identical. Threshold in bits out of 64."""
    return hamming(a, b) <= threshold


# --- quality ---------------------------------------------------------------


@dataclass
class Quality:
    blur: float
    mean_luma: float
    clipped_shadows: float
    clipped_highlights: float
    problems: list[str] = field(default_factory=list)

    @property
    def usable(self) -> bool:
        return not self.problems


def _luma(img: Image.Image) -> np.ndarray:
    return np.asarray(img.convert("L"), dtype=np.float64)


def _laplacian_variance(gray: np.ndarray) -> float:
    """Variance of the Laplacian. Low variance means few edges means blur."""
    k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float64)
    h, w = gray.shape
    if h < 3 or w < 3:
        return 0.0
    # Explicit 3x3 correlation. Avoids a scipy dependency for one kernel.
    out = np.zeros((h - 2, w - 2), dtype=np.float64)
    for dy in range(3):
        for dx in range(3):
            coeff = k[dy, dx]
            if coeff:
                out += coeff * gray[dy : dy + h - 2, dx : dx + w - 2]
    return float(out.var())


def assess(img: Image.Image, blur_min: float = 100.0) -> Quality:
    gray = _luma(img)
    # Work at a consistent scale so the blur threshold means the same thing for
    # a 1080px graphic and a 4032px phone photo.
    if max(gray.shape) > 1024:
        scale = 1024 / max(gray.shape)
        small = img.convert("L").resize(
            (max(1, int(img.width * scale)), max(1, int(img.height * scale))),
            Image.LANCZOS,
        )
        gray = np.asarray(small, dtype=np.float64)

    blur = _laplacian_variance(gray)
    mean_luma = float(gray.mean())
    total = gray.size
    shadows = float((gray < 8).sum()) / total
    highlights = float((gray > 247).sum()) / total

    problems: list[str] = []
    if blur < blur_min:
        problems.append(f"blurry (laplacian variance {blur:.0f} < {blur_min:.0f})")
    if mean_luma < 45:
        problems.append(f"underexposed (mean luma {mean_luma:.0f})")
    if mean_luma > 225:
        problems.append(f"blown out (mean luma {mean_luma:.0f})")
    if shadows > 0.55:
        problems.append(f"crushed shadows ({shadows:.0%} of frame)")
    if highlights > 0.45:
        problems.append(f"clipped highlights ({highlights:.0%} of frame)")

    return Quality(blur, mean_luma, shadows, highlights, problems)


# --- before / after delta --------------------------------------------------


def transformation_delta(before: Image.Image, after: Image.Image) -> float:
    """How different the two frames are, 0.0 to 1.0.

    A proof post whose transformation is invisible at thumbnail size is a
    failed proof post. Two of the five composites Ant uploaded on Aug 6 fall
    into that category, which is why this is a gate and not a metric.

    Compared at thumbnail scale on purpose: that is how the audience sees it.
    """
    size = (64, 64)
    a = np.asarray(before.convert("L").resize(size, Image.LANCZOS), dtype=np.float64)
    b = np.asarray(after.convert("L").resize(size, Image.LANCZOS), dtype=np.float64)
    return float(np.abs(a - b).mean() / 255.0)


# --- composite detection ---------------------------------------------------


@dataclass
class Composite:
    is_composite: bool
    reason: str = ""
    seam: str = ""          # "horizontal", "vertical", or ""


def detect_composite(img: Image.Image) -> Composite:
    """True when the file is already a finished before/after graphic.

    Ant's folder receives both raw job photos and finished branded composites.
    Branding a composite produces a second logo, so the pipeline has to tell
    them apart before the branding stage.

    Detected by the divider: a finished composite has a strong, straight,
    full-width or full-height edge near the middle, plus panels that differ
    from each other. A raw photo almost never does.
    """
    gray = _luma(img)
    h, w = gray.shape
    if h < 32 or w < 32:
        return Composite(False)

    def seam_strength(axis: int) -> tuple[float, int]:
        """Largest mean gradient across a line near the middle third."""
        length = gray.shape[axis]
        lo, hi = int(length * 0.35), int(length * 0.65)
        best, best_at = 0.0, 0
        for i in range(max(1, lo), min(length - 1, hi)):
            if axis == 0:
                grad = np.abs(gray[i + 1, :] - gray[i - 1, :]).mean()
            else:
                grad = np.abs(gray[:, i + 1] - gray[:, i - 1]).mean()
            if grad > best:
                best, best_at = float(grad), i
        return best, best_at

    h_strength, h_at = seam_strength(0)
    v_strength, v_at = seam_strength(1)

    # A divider bar or hard join reads far stronger than ordinary image detail.
    threshold = 28.0
    if h_strength >= v_strength and h_strength > threshold:
        top, bottom = gray[:h_at], gray[h_at:]
        if abs(top.mean() - bottom.mean()) > 3 or h_strength > 45:
            return Composite(
                True, f"horizontal seam at y={h_at} (gradient {h_strength:.0f})", "horizontal"
            )
    if v_strength > threshold:
        left, right = gray[:, :v_at], gray[:, v_at:]
        if abs(left.mean() - right.mean()) > 3 or v_strength > 45:
            return Composite(
                True, f"vertical seam at x={v_at} (gradient {v_strength:.0f})", "vertical"
            )

    return Composite(False)
