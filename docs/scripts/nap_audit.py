#!/usr/bin/env python3
"""NAP (Name / Address / Phone) consistency audit. Run from website/.

A Team Contracting is a service-area business, so the rules are stricter than
a normal NAP check:
  * the NAME is "A Team Contracting" with NO hyphen everywhere except the logo
    wordmark, which is a stylized mark and stays "A-TEAM"
  * there must be NO street address anywhere — not visible, not in schema
  * the PHONE is one number in one display format, and every tel: link uses
    the same E.164 form
Anything inconsistent here splits the business's identity across citations,
which is the single most common cause of a local pack ranking stalling.
"""
import re, json, pathlib, html as H, sys, collections

NAME   = "A Team Contracting"
PHONE  = "(937) 777-9093"
TEL    = "tel:+19377779093"
EMAIL  = "Owner@ateamcontractings.com"
CITY, REGION, ZIP = "Tipp City", "OH", "45371"

errors, warns = [], []
def err(p, m):  errors.append((str(p), m))
def warn(p, m): warns.append((str(p), m))

pages = sorted(p for p in pathlib.Path('.').rglob('index.html') if 'node_modules' not in str(p))

phone_formats = collections.Counter()
name_variants = collections.Counter()
biz_nodes     = []

for p in pages:
    h = p.read_text()

    # ---- NAME -------------------------------------------------------
    # quoted customer reviews are off limits: three customers wrote "A-Team"
    # Customers wrote "A-Team" with a hyphen and Anthony's replies are quoted
    # verbatim from Google. None of that may be rewritten, so it is scrubbed
    # before the name check rather than reported.
    scrub = h
    for pat in [r'<blockquote>.*?</blockquote>',
                r'<p class="review-text">.*?</p>',
                r'<div class="lp-review">.*?</div>\s*</div>',
                r'<article class="rv-card">.*?</article>',
                r'"reviewBody":".*?"\}',
                r'<!--.*?-->']:
        scrub = re.sub(pat, ' ', scrub, flags=re.S)
    # the logo wordmark is a stylized mark and legitimately keeps its hyphen
    scrub = re.sub(r'<(span|div) class="logo-text">.*?</\1>', ' ', scrub, flags=re.S)

    for m in re.finditer(r'A-Team\b|A-TEAM\b', scrub):
        err(p, f"hyphenated brand name outside the logo: ...{scrub[max(0,m.start()-50):m.start()+30]}...")
    for m in re.finditer(r'\bA\s+Team\s+Contracting\b|\bA-Team\s+Contracting\b', scrub):
        name_variants[m.group(0)] += 1

    # ---- PHONE ------------------------------------------------------
    display = re.sub(r'(href|src)="(tel|sms|mailto):[^"]*"', ' ', h)
    for m in re.finditer(r'\(?937\)?[\s.\-]?\s?939[\s.\-]?2936', display):
        phone_formats[m.group(0)] += 1
    for m in re.finditer(r'href="tel:([^"]*)"', h):
        if m.group(1) != TEL.split(':', 1)[1]:
            err(p, f"tel: link is {m.group(1)!r}, expected {TEL.split(':',1)[1]!r}")
    # a phone number that is displayed but not tappable on mobile
    if PHONE in h and 'tel:' not in h:
        warn(p, "displays the phone number but has no tel: link")

    # ---- ADDRESS ----------------------------------------------------
    if 'streetAddress' in h:
        err(p, "streetAddress present — this is a service-area business")
    prose = re.sub(r'placeholder="[^"]*"|value="[^"]*"', ' ', h)
    for m in re.finditer(r'\b\d{2,5}\s+[A-Z][a-z]+\s+(Street|St|Road|Rd|Avenue|Ave|Drive|Dr|Lane|Ln|Way|Court|Ct|Boulevard|Blvd)\b', prose):
        err(p, f"looks like a street address in visible copy: {m.group(0)!r}")

    # ---- schema NAP -------------------------------------------------
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        d = json.loads(blk)
        if not (isinstance(d, dict) and str(d.get('@id', '')).endswith('#business')):
            continue
        biz_nodes.append((str(p), d))
        if d.get('name') != NAME:            err(p, f"schema name {d.get('name')!r} != {NAME!r}")
        if d.get('telephone') != PHONE:      err(p, f"schema telephone {d.get('telephone')!r} != {PHONE!r}")
        if d.get('email') != EMAIL:          err(p, f"schema email {d.get('email')!r} != {EMAIL!r}")
        a = d.get('address', {})
        if a.get('streetAddress'):           err(p, "schema address has a streetAddress")
        if a.get('addressLocality') != CITY: err(p, f"schema locality {a.get('addressLocality')!r} != {CITY!r}")
        if a.get('addressRegion') != REGION: err(p, f"schema region {a.get('addressRegion')!r} != {REGION!r}")
        if a.get('postalCode') != ZIP:       err(p, f"schema postalCode {a.get('postalCode')!r} != {ZIP!r}")

    # ---- visible NAP block -------------------------------------------
    nap = re.search(r'<div class="footer-nap".*?</div>', h, re.S)
    if nap:
        txt = H.unescape(re.sub(r'<[^>]+>', ' ', nap.group(0)))
        if NAME not in txt:  err(p, "footer NAP block missing the business name")
        if PHONE not in txt: err(p, "footer NAP block missing the phone number")
        if CITY not in txt:  err(p, "footer NAP block missing the city")

# ---- every business node must be byte-identical ----------------------
if biz_nodes:
    ref_file, ref = biz_nodes[0]
    for f, d in biz_nodes[1:]:
        diff = [k for k in set(d) | set(ref) if d.get(k) != ref.get(k)]
        # /reviews/ legitimately adds review + aggregateRating: the reviews it
        # describes are rendered on that page. Nowhere else may.
        allowed = {'review', 'aggregateRating'} if f.startswith('reviews/') else set()
        unexpected = [k for k in diff if k not in allowed]
        if unexpected:
            errors.append((f, f"business node differs from {ref_file} in: {unexpected}"))
        for k in ('review', 'aggregateRating'):
            if k in d and not f.startswith('reviews/'):
                errors.append((f, f"{k} on a page where the reviews are not visible"))

print(f"{len(pages)} pages | {len(biz_nodes)} business nodes\n")
print("phone formats found:", dict(phone_formats) or "none")
print("name variants found:", dict(name_variants) or "none")
if len(phone_formats) > 1:
    errors.append(("(sitewide)", f"phone rendered in {len(phone_formats)} different formats: {dict(phone_formats)}"))
if len(name_variants) > 1:
    errors.append(("(sitewide)", f"business name written {len(name_variants)} different ways: {dict(name_variants)}"))

print()
print(f"ERRORS ({len(errors)})")
for f, m in errors: print(f"  {f}: {m}")
print()
print(f"WARNINGS ({len(warns)})")
for f, m in warns: print(f"  {f}: {m}")
sys.exit(1 if errors else 0)
