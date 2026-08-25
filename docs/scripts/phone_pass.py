#!/usr/bin/env python3
"""Replace the company phone number sitewide: (937) 939-2936 -> (937) 777-9093.

Two textual forms cover every occurrence: the display format used in visible
text and JSON-LD `telephone` fields, and the bare digit string that appears
inside every tel:/sms: href and E.164 JSON-LD value (tel:+19379392936 etc).
Idempotent: re-running after the number is already updated is a no-op.

Run from anywhere; paths are relative to the repo root.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]

OLD_DISPLAY, NEW_DISPLAY = "(937) 939-2936", "(937) 777-9093"
OLD_DIGITS, NEW_DIGITS = "9379392936", "9377779093"

WEBSITE_GLOBS = ["website/**/index.html", "website/assets/*.js", "website/README.md"]
EXTRA_FILES = [
    "docs/review-request-templates.md",
    "docs/scripts/footer_pass.py",
    "docs/scripts/nap_audit.py",
    "docs/scripts/schema_pass.py",
    "plan-data.js",
]

def files():
    seen = set()
    for pat in WEBSITE_GLOBS:
        for p in ROOT.glob(pat):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p
    for rel in EXTRA_FILES:
        p = ROOT / rel
        if p.is_file() and p not in seen:
            seen.add(p)
            yield p

changed = 0
for p in files():
    text = p.read_text(encoding="utf-8")
    new_text = text.replace(OLD_DISPLAY, NEW_DISPLAY).replace(OLD_DIGITS, NEW_DIGITS)
    if new_text != text:
        p.write_text(new_text, encoding="utf-8")
        changed += 1
        print(f"  updated {p.relative_to(ROOT)}")

print(f"\n{changed} file(s) updated.")
