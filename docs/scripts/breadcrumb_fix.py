#!/usr/bin/env python3
"""Bring every BreadcrumbList into agreement with the visible trail. Run from website/.

Three things go wrong and this fixes all of them:
  1. A stray "Reviews" <li> that a previous pass injected into blog-post trails.
     Reviews is not an ancestor of a post, so it does not belong in the crumb.
  2. Blog-post schema naming the full <title> while the visible crumb shows a
     short label. Google wants the schema to describe the visible trail.
  3. Pages with a visible trail and no BreadcrumbList at all — the trail is
     there for readers but invisible to search.
"""
import re, json, pathlib, html as H

SITE = "https://ateamcontractings.com"
BOGUS = '    <li><a href="/reviews/">Reviews</a></li>\n'
changed = []

def visible_trail(h):
    nav = re.search(r'<nav class="breadcrumb".*?</nav>', h, re.S)
    if not nav: return None
    out = []
    for li in re.findall(r'<li>(.*?)</li>', nav.group(0), re.S):
        a = re.search(r'href="([^"]*)"', li)
        out.append((H.unescape(re.sub(r'<[^>]+>', '', li)).strip(), a.group(1) if a else None))
    return out

def ld_for(trail, page_url):
    items = []
    for i, (name, href) in enumerate(trail, 1):
        items.append({"@type": "ListItem", "position": i, "name": name,
                      "item": (SITE + href) if href else page_url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

for p in sorted(pathlib.Path('.').rglob('index.html')):
    if 'node_modules' in str(p): continue
    h = orig = p.read_text()
    d = str(p.parent).replace('.', '', 1).strip('/')
    page_url = f"{SITE}/{d}/" if d else f"{SITE}/"

    # 1. drop the stray Reviews crumb, but only where it sits inside the trail
    nav = re.search(r'<nav class="breadcrumb".*?</nav>', h, re.S)
    if nav and BOGUS in nav.group(0):
        h = h.replace(nav.group(0), nav.group(0).replace(BOGUS, ''), 1)

    trail = visible_trail(h)
    if not trail:
        if h != orig: p.write_text(h); changed.append((str(p), "removed stray Reviews crumb"))
        continue

    want = ld_for(trail, page_url)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    existing = next((b for b in blocks if json.loads(b).get('@type') == 'BreadcrumbList'), None)

    if existing is None:
        # 3. no schema at all — inject one just before </head>
        tag = '<script type="application/ld+json">' + json.dumps(want, separators=(',', ':')) + '</script>\n'
        h = h.replace('</head>', tag + '</head>', 1)
        p.write_text(h); changed.append((str(p), "added missing BreadcrumbList"))
    elif json.loads(existing) != want:
        # 2. schema disagrees with the visible trail — rewrite it
        h = h.replace(existing, json.dumps(want, separators=(',', ':')), 1)
        p.write_text(h); changed.append((str(p), "realigned BreadcrumbList to visible trail"))
    elif h != orig:
        p.write_text(h); changed.append((str(p), "removed stray Reviews crumb"))

for f, what in changed: print(f"  {f:52} {what}")
print(f"\n{len(changed)} pages changed")
