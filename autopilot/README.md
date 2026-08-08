# A-Team Social Autopilot

Plan and per-platform automation status: [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md).

**Steps 2 and 3 of 9.** Configuration, voice and brand rules, the rule engine
that enforces them, and the photo pipeline. Nothing publishes yet.

## What is here

    config/config.yaml   every ID, cadence, threshold and rule, verified against the live account
    config/voice.md      how Ant sounds, plus 10 example posts awaiting his approval
    config/brand.md      color, type, logo, pricing display, template inventory
    config/banned.txt    phrases that block a draft and trigger a rewrite
    config.py            loads and validates all of the above
    lint.py              the voice and platform rules, as blocking checks
    state.py             used_photos.json, perceptual hashes, per-platform cooldown
    pipeline.py          watch, sniff, normalize, dedupe, gate, classify
    images/load.py       magic-byte sniffing, HEIF, exif_transpose at the boundary
    images/quality.py    perceptual hash, blur and exposure gate, composite detection
    images/compose.py    logo transparency, pairing, letterboxing
    check.py             Step 2 verification
    tests/                negative tests for the linter, pixel tests for the pipeline

## Running it

    pip install -r autopilot/requirements.txt
    python -m autopilot.check              # validate config, lint the 10 examples
    python -m autopilot.pipeline <dir>     # run the photo pipeline over a folder
    python autopilot/tests/test_lint.py    # prove the rules catch violations
    python autopilot/tests/test_images.py  # prove the pipeline handles the real failures

## The photo pipeline

    sniff      magic bytes decide, never the extension
    normalize  exif_transpose runs inside load(), so no caller sees a sideways pixel
    dedupe     difference hash, catches re-uploads under a new name
    composite  finished branded graphics route around the branding stage
    gate       blur, exposure, and before/after delta at thumbnail scale
    classify   filename seeds it when Ant names the file, vision covers the rest

Verified against Ant's real folder: 8 of 10 files correctly identified as
already-branded composites, one confirmed duplicate caught, one blocklisted
asset stopped even though its extension had changed.

`check.py` exits non-zero if the content mix does not sum to 1.0, the Nextdoor
cadence exceeds its hard cap, a platform is configured to allow a phone number
where it must not, the logo points at the gray-background master, or any example
post breaks a rule.

## The Step 2 gate

The 10 example posts in `voice.md` need Ant's eye. Approved examples become the
few-shot reference every generated post is written against, so a bad example
compounds. Shred anything that does not sound like him.

## Rules worth knowing before editing

- **Cadence is derived, never hardcoded.** `weekly_post_counts()` computes it
  from the cadence block, so the 34-a-week arithmetic cannot drift from what the
  scheduler does.
- **Nothing reads a config file directly except `config.py`.** A missing or
  malformed value raises at load, not at publish time.
- **Credentials are declared, never stored.** `env:NAME` markers resolve from the
  environment. `check.py` reports which are still unset.
- **Open questions live in config.** Anything Ant has not answered carries an
  explicit `default_until_answered` rather than a silent assumption.
