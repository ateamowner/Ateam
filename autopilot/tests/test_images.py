"""Tests for the photo pipeline.

Each of these covers a failure that is either documented in the architecture
notes or was observed in Ant's real Drive folder.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from PIL import Image

from autopilot import config as cfg
from autopilot.images import compose, quality
from autopilot.images.load import load, sniff
from autopilot.pipeline import classify_from_name
from autopilot.state import Manifest, PhotoRecord

SETTINGS = cfg.load()
results: list[tuple[bool, str]] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    results.append((ok, f"{label}{'  ' + detail if detail and not ok else ''}"))


def noisy(w: int, h: int, seed: int = 0) -> Image.Image:
    """An image with real edge detail, so it is not read as blurry."""
    import random

    rng = random.Random(seed)
    img = Image.new("RGB", (w, h))
    img.putdata([
        (rng.randrange(256), rng.randrange(256), rng.randrange(256))
        for _ in range(w * h)
    ])
    return img


def test_sniff_ignores_the_extension(tmp: Path) -> None:
    """Half the Drive folder is HEIF or JPEG wearing a .png name."""
    p = tmp / "definitely_a_photo.png"
    noisy(40, 40).save(p, format="JPEG")
    check(sniff(p) == "JPEG", "sniff reads bytes, not the .png extension",
          f"got {sniff(p)}")
    check(load(p).mislabeled is True, "mislabeled extension is flagged")


def test_exif_transpose_runs_at_the_boundary(tmp: Path) -> None:
    """Rotation must be applied before anything downstream sees the pixels."""
    p = tmp / "rotated.jpg"
    img = noisy(60, 30)
    exif = img.getexif()
    exif[274] = 6  # orientation: rotate 90 CW
    img.save(p, format="JPEG", exif=exif)

    out = load(p).image
    check(
        (out.width, out.height) == (30, 60),
        "exif_transpose applied on load",
        f"got {out.width}x{out.height}, expected 30x60",
    )


def test_phash_catches_a_rescaled_reupload() -> None:
    original = noisy(300, 300, seed=7)
    resaved = original.resize((150, 150)).resize((300, 300))
    buf = io.BytesIO()
    resaved.save(buf, format="JPEG", quality=70)
    recompressed = Image.open(buf)

    a, b = quality.phash(original), quality.phash(recompressed)
    check(quality.looks_duplicate(a, b), "phash survives rescale and recompression",
          f"hamming {quality.hamming(a, b)}")

    different = noisy(300, 300, seed=99)
    check(
        not quality.looks_duplicate(a, quality.phash(different)),
        "phash separates genuinely different photos",
    )


def test_flood_fill_keeps_interior_white() -> None:
    """The reason this is a flood fill and not a color key.

    A white ring on a white background: the outer white must go transparent,
    the white at the centre must survive. A color key removes both and eats the
    detail inside the A-Team shield.
    """
    size = 80
    logo = Image.new("RGB", (size, size), (255, 255, 255))
    px = logo.load()
    cx = cy = size // 2
    for y in range(size):
        for x in range(size):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if 12 < d < 28:
                px[x, y] = (27, 91, 152)   # blue ring
    cut = compose.cut_background(logo)
    alpha = cut.getchannel("A")

    check(alpha.getpixel((0, 0)) == 0, "outer background is cut")
    check(alpha.getpixel((cx, cy)) == 255, "white inside the shape survives")
    check(alpha.getpixel((cx, cy - 20)) == 255, "the mark itself survives")


def test_already_cut_logo_is_left_alone() -> None:
    """Found by running against the real logo, not the synthetic one.

    ATeam Logo Web 1200 ships already transparent. Flood filling it anyway
    nibbled 2,296 anti-aliased edge pixels that sat near the seed color and
    touched the border. The gray-background master still needs the fill, so the
    difference is decided by looking at the alpha channel.
    """
    size = 60
    cut = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = cut.load()
    for y in range(20, 40):
        for x in range(20, 40):
            px[x, y] = (27, 91, 152, 255)

    check(compose.already_transparent(cut), "an already-cut logo is recognised")
    before = sum(1 for v in cut.getchannel("A").get_flattened_data() if v > 0)
    after_img = compose.cut_background(cut)
    after = sum(1 for v in after_img.getchannel("A").get_flattened_data() if v > 0)
    check(after == before, "no pixels lost on an already-cut logo",
          f"{before} -> {after}")

    # The opaque master still gets cut.
    flat = Image.new("RGB", (size, size), (222, 222, 222))
    flat.paste(cut, (0, 0), cut)
    check(
        not compose.already_transparent(flat.convert("RGBA")),
        "an opaque master is not mistaken for a cut one",
    )
    recut = compose.cut_background(flat)
    check(recut.getchannel("A").getpixel((0, 0)) == 0, "master background is cut")
    check(recut.getchannel("A").getpixel((30, 30)) == 255, "master mark survives")


def test_pairing_never_crops() -> None:
    """Mismatched orientations reconcile on one axis and keep natural widths."""
    portrait = noisy(600, 900, seed=1)
    landscape = noisy(1200, 800, seed=2)

    joined = compose.compose_pair(
        compose.Pair(portrait, landscape, "side_by_side"), divider=8
    )
    # Heights match at 800; widths scale naturally and stay different.
    scaled_portrait_w = round(600 * (800 / 900))
    expected_w = scaled_portrait_w + 8 + 1200
    check(joined.height == 800, "side by side matches heights", f"got {joined.height}")
    check(
        joined.width == expected_w,
        "widths stay natural, nothing is cropped",
        f"got {joined.width}, expected {expected_w}",
    )

    stacked = compose.compose_pair(
        compose.Pair(portrait, landscape, "stacked"), divider=8
    )
    check(stacked.width == 600, "stacked matches widths", f"got {stacked.width}")


def test_fit_to_canvas_letterboxes() -> None:
    wide = noisy(2000, 500, seed=3)
    out = compose.fit_to_canvas(wide, (1080, 1350))
    check(out.size == (1080, 1350), "canvas is the exact platform size")
    # A crop would have filled the frame; a letterbox leaves background.
    check(out.getpixel((5, 5)) == (255, 255, 255), "letterboxed rather than cropped")


def test_transformation_delta_flags_a_weak_pair() -> None:
    """Two of Ant's Aug 6 composites show almost no visible change."""
    before = noisy(200, 200, seed=5)
    same = before.copy()
    check(
        quality.transformation_delta(before, same) < 0.02,
        "identical frames score near zero",
    )
    dark = Image.new("RGB", (200, 200), (10, 10, 10))
    light = Image.new("RGB", (200, 200), (240, 240, 240))
    check(
        quality.transformation_delta(dark, light) > 0.8,
        "a real transformation scores high",
    )


def test_blur_is_rejected() -> None:
    from PIL import ImageFilter

    sharp = noisy(300, 300, seed=11)
    blurred = sharp.filter(ImageFilter.GaussianBlur(radius=6))
    check(quality.assess(sharp).usable, "a sharp photo passes the gate")
    check(not quality.assess(blurred).usable, "a blurred photo is rejected")
    check(
        not quality.assess(Image.new("RGB", (300, 300), (4, 4, 4))).usable,
        "an underexposed frame is rejected",
    )


def test_filename_classification() -> None:
    hoods = SETTINGS.neighborhoods
    t = classify_from_name("PW driveway Centerville.png", hoods)
    check(t.service == "pressure_wash", "PW reads as pressure wash", t.service)
    check(t.subject == "driveway", "driveway subject", t.subject)
    check(t.city == "Centerville", "city from filename", t.city)

    t2 = classify_from_name("SW siding tipp city.png", hoods)
    check(t2.service == "softwash", "SW reads as softwash", t2.service)
    check(t2.city == "Tipp City", "lowercase city still matches", t2.city)

    t3 = classify_from_name("IMG_0228.PNG", hoods)
    check(t3.is_bare, "a camera-roll name yields nothing and says so")


def test_manifest_cooldown_is_per_platform() -> None:
    from datetime import date

    m = Manifest([
        PhotoRecord(file_id="a", name="a.jpg", phash="0", real_format="JPEG")
    ])
    m.mark_used("a", "facebook", when=date(2026, 8, 1))

    today = date(2026, 8, 20)
    fb = [r.file_id for r in m.available_for("facebook", 90, today)]
    ig = [r.file_id for r in m.available_for("instagram", 90, today)]
    check("a" not in fb, "used on Facebook, so unavailable there")
    check("a" in ig, "still available on Instagram, cooldown is per platform")

    later = date(2026, 12, 1)
    check(
        "a" in [r.file_id for r in m.available_for("facebook", 90, later)],
        "available again once the cooldown expires",
    )


def run() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        test_sniff_ignores_the_extension(tmp)
        test_exif_transpose_runs_at_the_boundary(tmp)

    test_phash_catches_a_rescaled_reupload()
    test_flood_fill_keeps_interior_white()
    test_already_cut_logo_is_left_alone()
    test_pairing_never_crops()
    test_fit_to_canvas_letterboxes()
    test_transformation_delta_flags_a_weak_pair()
    test_blur_is_rejected()
    test_filename_classification()
    test_manifest_cooldown_is_per_platform()

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
