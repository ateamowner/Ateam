#!/usr/bin/env python3
"""Add a 'Seal Coating' nav/footer link everywhere the site already lists
'Concrete Cleaning' (mobile drawer + footer services list), except the 7
seal-coating pages themselves, which already carry it from sealcoat_build.py.

Idempotent: a second run is a no-op because it checks for the seal-coating
link before inserting.

Run from anywhere; paths are relative to the repo root.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2] / "website"

TARGET = '<a href="/concrete-cleaning-tipp-city-ohio/">Concrete Cleaning</a>'
NEW_HREF = '<a href="/seal-coating-tipp-city-ohio/">Seal Coating</a>'

changed = 0
for p in sorted(ROOT.glob("**/index.html")):
    if p.parent.name.startswith("seal-coating-"):
        continue
    text = p.read_text(encoding="utf-8")
    if TARGET not in text:
        continue
    if NEW_HREF in text:
        continue  # already wired

    def repl(m):
        line_start = text.rfind("\n", 0, m.start()) + 1
        indent = text[line_start : m.start()]
        return m.group(0) + "\n" + indent + NEW_HREF

    new_text = re.sub(re.escape(TARGET), repl, text)
    if new_text != text:
        p.write_text(new_text, encoding="utf-8")
        changed += 1
        print(f"  wired {p.relative_to(ROOT.parent)}")

print(f"\n{changed} file(s) updated.")
