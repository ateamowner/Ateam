#!/usr/bin/env python3
"""Sitewide SEO / indexability audit. Run from website/.

Checks the things that actually keep a page out of the index or get it filtered:
canonical correctness, robots directives, title/description presence and
uniqueness, heading structure, social tags, structured data, sitemap agreement,
image alt and intrinsic sizing. Exits non-zero if any ERROR is found.
"""
import re, json, html as H, pathlib, collections, sys

SITE = "https://ateamcontractings.com"
errors, warns, notes = [], [], []

def err(p, m):  errors.append((str(p), m))
def warn(p, m): warns.append((str(p), m))

root = pathlib.Path('.')
pages = sorted(p for p in root.rglob('index.html') if 'node_modules' not in str(p))

def url_of(p):
    d = str(p.parent).replace('.', '', 1).strip('/')
    return f"{SITE}/{d}/" if d else f"{SITE}/"

def text_of(h):
    b = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', b)))

titles, descs, canons = collections.defaultdict(list), collections.defaultdict(list), {}
indexable = []

for p in pages:
    h = p.read_text()
    u = url_of(p)
    low = h.lower()

    # --- indexability -------------------------------------------------
    rob = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', h, re.I)
    robots = rob.group(1).lower() if rob else ""
    noindex = 'noindex' in robots
    if not noindex:
        indexable.append(u)

    # --- canonical ----------------------------------------------------
    cans = re.findall(r'<link\s+rel="canonical"\s+href="([^"]*)"', h, re.I)
    if len(cans) == 0:
        # A noindex page does not need one, and Google advises against pairing
        # noindex with a canonical anyway. Only indexable pages must have it.
        if not noindex: err(p, "no canonical")
    elif len(cans) > 1:
        err(p, f"{len(cans)} canonicals: {cans}")
    else:
        c = cans[0]
        canons[u] = c
        if not c.startswith('https://'):
            err(p, f"canonical not absolute https: {c}")
        elif c != u:
            err(p, f"canonical points elsewhere: {c} (page is {u})")

    # --- title --------------------------------------------------------
    t = re.search(r'<title>(.*?)</title>', h, re.S)
    if not t:
        err(p, "no <title>")
    else:
        tt = H.unescape(t.group(1)).strip()
        if not noindex:
            titles[tt].append(u)
            if len(tt) > 60: warn(p, f"title {len(tt)} chars (>60): {tt}")
            if len(tt) < 15: warn(p, f"title only {len(tt)} chars: {tt}")

    # --- description --------------------------------------------------
    ds = re.findall(r'<meta\s+name="description"\s+content="([^"]*)"', h, re.I)
    if not ds:
        err(p, "no meta description")
    elif len(ds) > 1:
        err(p, f"{len(ds)} meta descriptions")
    else:
        d = H.unescape(ds[0]).strip()
        if not noindex:
            descs[d].append(u)
            n = len(d)
            if n > 165: warn(p, f"description {n} chars (>165)")
            if n < 70:  warn(p, f"description {n} chars (<70)")

    # --- headings -----------------------------------------------------
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    if len(h1) != 1:
        err(p, f"{len(h1)} h1 tags")
    levels = [int(m) for m in re.findall(r'<h([1-6])[^>]*>', h)]
    prev = 0
    for lv in levels:
        if prev and lv > prev + 1:
            warn(p, f"heading jumps h{prev} -> h{lv}")
            break
        prev = lv

    # --- basics -------------------------------------------------------
    if not re.search(r'<html[^>]+lang=', h):       err(p, "no lang attribute")
    if 'name="viewport"' not in low:               err(p, "no viewport meta")
    if '<meta charset' not in low:                 err(p, "no charset")

    # --- social -------------------------------------------------------
    for tag in ['og:title', 'og:description', 'og:url', 'og:image']:
        if f'property="{tag}"' not in h: warn(p, f"missing {tag}")
    ogu = re.search(r'<meta\s+property="og:url"\s+content="([^"]*)"', h)
    if ogu and ogu.group(1) != u:
        err(p, f"og:url {ogu.group(1)} != page url {u}")

    # --- structured data ----------------------------------------------
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(blk)
        except Exception as e:
            err(p, f"invalid JSON-LD: {e}")

    # --- images -------------------------------------------------------
    for tag in re.findall(r'<img[^>]*>', h):
        if 'alt=' not in tag:
            err(p, f"img without alt: {tag[:70]}")
        elif re.search(r'alt=""', tag) and 'aria-hidden' not in tag:
            warn(p, f"empty alt (ok if decorative): {tag[:70]}")
        if not ('width=' in tag and 'height=' in tag) and 'logo' not in tag:
            warn(p, f"img without width/height (CLS risk): {tag[:70]}")

    # --- thin content --------------------------------------------------
    words = len(text_of(h).split())
    if not noindex and words < 300:
        warn(p, f"thin page: {words} words total")

# --- cross-page ---------------------------------------------------------
for t, us in titles.items():
    if len(us) > 1: errors.append(("(sitewide)", f"duplicate title on {len(us)} pages: {t!r} -> {us}"))
for d, us in descs.items():
    if len(us) > 1: errors.append(("(sitewide)", f"duplicate description on {len(us)} pages -> {us}"))

# --- sitemap ------------------------------------------------------------
sm = pathlib.Path('sitemap.xml').read_text()
locs = re.findall(r'<loc>(.*?)</loc>', sm)
if len(locs) != len(set(locs)):
    errors.append(("sitemap.xml", "duplicate <loc> entries"))
for l in locs:
    if not l.startswith(SITE): errors.append(("sitemap.xml", f"foreign host: {l}"))
    if not l.endswith('/'):    errors.append(("sitemap.xml", f"no trailing slash: {l}"))
missing = sorted(set(indexable) - set(locs))
extra   = sorted(set(locs) - set(indexable))
for m in missing: errors.append(("sitemap.xml", f"indexable page missing from sitemap: {m}"))
for e in extra:   errors.append(("sitemap.xml", f"sitemap lists a noindex/nonexistent page: {e}"))

# --- robots.txt ---------------------------------------------------------
rt = pathlib.Path('robots.txt').read_text()
if 'Sitemap:' not in rt: errors.append(("robots.txt", "no Sitemap: directive"))
elif f"{SITE}/sitemap.xml" not in rt: errors.append(("robots.txt", "Sitemap: URL does not match site"))
for line in rt.splitlines():
    if line.strip().lower().startswith('disallow:'):
        path = line.split(':', 1)[1].strip()
        if path and path != '/netlify/':
            for l in locs:
                if l.replace(SITE, '').startswith(path):
                    errors.append(("robots.txt", f"Disallow {path} blocks sitemap URL {l}"))

# --- orphans ------------------------------------------------------------
linked = set()
for p in pages:
    for href in re.findall(r'href="(/[^"#?]*)"', p.read_text()):
        linked.add(SITE + (href if href.endswith('/') or '.' in href.rsplit('/', 1)[-1] else href + '/'))
orphans = [u for u in indexable if u not in linked and u != f"{SITE}/"]
for o in orphans: warns.append(("(internal links)", f"orphan — no internal link points here: {o}"))

# --- report -------------------------------------------------------------
print(f"{len(pages)} pages | {len(indexable)} indexable | {len(locs)} in sitemap\n")
if errors:
    print(f"ERRORS ({len(errors)})")
    for f, m in errors: print(f"  {f}: {m}")
else:
    print("ERRORS (0)  — none")
print()
if warns:
    print(f"WARNINGS ({len(warns)})")
    for f, m in warns: print(f"  {f}: {m}")
else:
    print("WARNINGS (0) — none")
sys.exit(1 if errors else 0)
