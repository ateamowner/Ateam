"""Pairing before/after frames and branding the result.

Two rules here exist because breaking them has cost this project real work:
never crop to force an aspect ratio, and never key the logo background by
color.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np
from PIL import Image

BRAND_ORANGE = (245, 130, 32)
BRAND_BLUE = (27, 91, 152)
BRAND_CHARCOAL = (51, 51, 51)
WHITE = (255, 255, 255)


# --- logo transparency -----------------------------------------------------


def already_transparent(img: Image.Image, min_cut: float = 0.02) -> bool:
    """True when a meaningful share of the image is already transparent.

    `ATeam Logo Web 1200.png` ships cut. The gray-background master does not.
    Both can reach this code, so the distinction is made by looking rather than
    by trusting the filename.
    """
    if img.mode not in ("RGBA", "LA"):
        return False
    alpha = np.asarray(img.getchannel("A"))
    return float((alpha == 0).mean()) >= min_cut


def cut_background(logo: Image.Image, tolerance: int = 32) -> Image.Image:
    """Make the logo's outer background transparent by flood fill from the corners.

    Deliberately not a color key. The A-Team shield has white detail inside it,
    and keying every white pixel eats that detail. A flood fill only removes
    background that is actually connected to the edge of the canvas, so
    enclosed white survives.

    The fill is seeded from all four corners so an off-center subject or a
    background split by the artwork still clears completely.
    """
    rgba = logo.convert("RGBA")
    arr = np.asarray(rgba, dtype=np.int16)
    h, w = arr.shape[:2]
    rgb = arr[:, :, :3]

    # Already cut. Running the fill anyway nibbles anti-aliased edge pixels that
    # happen to sit near the seed color and touch the border: measured at 2,296
    # lost pixels on the real ATeam Logo Web 1200, which is already 62.8%
    # transparent. Only the opaque master needs this.
    if already_transparent(rgba):
        return rgba

    # Seed color is the median of the four corners, so one odd corner pixel
    # cannot throw the whole cut off.
    corners = np.array(
        [rgb[0, 0], rgb[0, w - 1], rgb[h - 1, 0], rgb[h - 1, w - 1]], dtype=np.int16
    )
    seed = np.median(corners, axis=0)

    similar = (np.abs(rgb - seed).max(axis=2) <= tolerance)

    visited = np.zeros((h, w), dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    def push(y: int, x: int) -> None:
        if not visited[y, x] and similar[y, x]:
            visited[y, x] = True
            queue.append((y, x))

    for x in range(w):
        push(0, x)
        push(h - 1, x)
    for y in range(h):
        push(y, 0)
        push(y, w - 1)

    while queue:
        y, x = queue.popleft()
        if y > 0:
            push(y - 1, x)
        if y < h - 1:
            push(y + 1, x)
        if x > 0:
            push(y, x - 1)
        if x < w - 1:
            push(y, x + 1)

    out = arr.copy()
    out[:, :, 3] = np.where(visited, 0, arr[:, :, 3])
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def stamp_logo(
    canvas: Image.Image,
    logo: Image.Image,
    width_fraction: float = 0.12,
    opacity: float = 0.85,
    margin_fraction: float = 0.025,
) -> Image.Image:
    """Composite the logo bottom right at a fraction of the canvas width."""
    base = canvas.convert("RGBA")
    target_w = max(1, int(base.width * width_fraction))
    scale = target_w / logo.width
    mark = logo.resize((target_w, max(1, int(logo.height * scale))), Image.LANCZOS)

    if opacity < 1.0:
        alpha = mark.getchannel("A").point(lambda a: int(a * opacity))
        mark.putalpha(alpha)

    margin = int(base.width * margin_fraction)
    pos = (base.width - mark.width - margin, base.height - mark.height - margin)

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.paste(mark, pos, mark)
    return Image.alpha_composite(base, layer)


# --- pairing ---------------------------------------------------------------


@dataclass
class Pair:
    before: Image.Image
    after: Image.Image
    layout: str  # "side_by_side" or "stacked"


def _match_height(images: list[Image.Image]) -> list[Image.Image]:
    """Scale every frame to a common height, keeping its natural width.

    This is the rule that matters. Forcing a shared aspect ratio by cropping
    has destroyed good pairs before, so mismatched orientations are reconciled
    on one axis only and the other is allowed to differ.
    """
    target = min(im.height for im in images)
    out = []
    for im in images:
        if im.height == target:
            out.append(im)
            continue
        scale = target / im.height
        out.append(im.resize((max(1, round(im.width * scale)), target), Image.LANCZOS))
    return out


def _match_width(images: list[Image.Image]) -> list[Image.Image]:
    target = min(im.width for im in images)
    out = []
    for im in images:
        if im.width == target:
            out.append(im)
            continue
        scale = target / im.width
        out.append(im.resize((target, max(1, round(im.height * scale))), Image.LANCZOS))
    return out


def compose_pair(
    pair: Pair,
    divider: int = 8,
    divider_color: tuple[int, int, int] = BRAND_ORANGE,
    background: tuple[int, int, int] = WHITE,
) -> Image.Image:
    """Join a before and after into one frame with a brand divider.

    Side by side matches heights and lets widths differ. Stacked matches widths
    and lets heights differ. Neither crops.
    """
    if pair.layout == "side_by_side":
        left, right = _match_height([pair.before, pair.after])
        w = left.width + divider + right.width
        h = left.height
        canvas = Image.new("RGB", (w, h), background)
        canvas.paste(left.convert("RGB"), (0, 0))
        canvas.paste(
            Image.new("RGB", (divider, h), divider_color), (left.width, 0)
        )
        canvas.paste(right.convert("RGB"), (left.width + divider, 0))
        return canvas

    top, bottom = _match_width([pair.before, pair.after])
    w = top.width
    h = top.height + divider + bottom.height
    canvas = Image.new("RGB", (w, h), background)
    canvas.paste(top.convert("RGB"), (0, 0))
    canvas.paste(Image.new("RGB", (w, divider), divider_color), (0, top.height))
    canvas.paste(bottom.convert("RGB"), (0, top.height + divider))
    return canvas


def fit_to_canvas(
    img: Image.Image,
    size: tuple[int, int],
    background: tuple[int, int, int] = WHITE,
) -> Image.Image:
    """Letterbox onto a platform canvas. Scales down to fit, never crops."""
    target_w, target_h = size
    scale = min(target_w / img.width, target_h / img.height)
    w, h = max(1, round(img.width * scale)), max(1, round(img.height * scale))
    resized = img.convert("RGB").resize((w, h), Image.LANCZOS)
    canvas = Image.new("RGB", size, background)
    canvas.paste(resized, ((target_w - w) // 2, (target_h - h) // 2))
    return canvas
