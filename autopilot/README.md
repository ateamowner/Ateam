# A-Team Social Autopilot

Plan and per-platform automation status: [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md).

**Step 2 of 9.** Configuration, voice and brand rules, and the rule engine that
enforces them. Nothing publishes yet.

## What is here

    config/config.yaml   every ID, cadence, threshold and rule, verified against the live account
    config/voice.md      how Ant sounds, plus 10 example posts awaiting his approval
    config/brand.md      color, type, logo, pricing display, template inventory
    config/banned.txt    phrases that block a draft and trigger a rewrite
    config.py            loads and validates all of the above
    lint.py              the voice and platform rules, as blocking checks
    check.py             Step 2 verification
    tests/test_lint.py   negative tests, so the linter is known to actually fire

## Running it

    pip install -r autopilot/requirements.txt
    python -m autopilot.check          # validate config, lint the 10 examples
    python autopilot/tests/test_lint.py # prove the rules catch violations

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
