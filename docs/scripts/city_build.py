#!/usr/bin/env python3
"""
Phase D, Troy — build /soft-washing-troy-ohio/, /window-cleaning-troy-ohio/
and the /troy-ohio/ hub.

Chrome (head boilerplate, header, breadcrumb, footer, trust block) is lifted
from the existing Troy page so the three new pages cannot drift from the rest
of the site. Everything between <main> and </main> is written fresh.

ANTI-DUPLICATE: the existing pressure-washing-troy page already uses the
historic core (West Main, Public Square, Franklin St), the post-war ring
(Nottingham, Westbrook, Meadow Lakes), the newer subdivisions (Peters,
Barnhart, Stonebridge) and the hard-water/aquifer angle. None of that is
reused here. These pages lead on:

  soft washing    - the Great Miami river valley, the 1807 historic district
                    boundary (river / Clay / Canal / Oxford), Foursquares,
                    Dutch Colonials and bungalows, canopy shade and north walls
  window cleaning - divided-light sash and storm windows downtown, two-storey
                    colonials out east, and the first-weekend-of-June
                    Strawberry Festival as the real local booking deadline
  the hub         - coverage and routing, deliberately short

Local facts verified against troyohio.gov and the Strawberry Festival site
rather than written from memory.
"""
import json
import os
import re

ROOT = "/home/user/Ateam/website"
CITY = os.environ.get("CITY", "Troy")
SRC = os.path.join(ROOT, os.environ.get("CHROME_SRC", "pressure-washing-troy-ohio"), "index.html")
BID = "https://ateamcontractings.com/#business"

src = open(SRC, encoding="utf-8").read()
HEAD_OPEN = src[: src.index("<title>")]
AFTER_HEAD = src[src.index("</head>") : src.index("<nav class=\"breadcrumb\"")]
FOOTER = src[src.index("</main>") :]


def head(title, desc, url, image, extra_ld):
    ld = "\n".join(
        '<script type="application/ld+json">%s</script>'
        % json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        for b in extra_ld
    )
    return (
        HEAD_OPEN
        + "<title>%s</title>\n" % title
        + '<meta name="description" content="%s">\n' % desc
        + '<meta name="author" content="Anthony Leonard, A Team Contracting">\n'
        + '<meta name="geo.placename" content="%s, Ohio">\n' % CITY
        + '<meta name="geo.region" content="US-OH">\n'
        + '<meta name="robots" content="index, follow, max-image-preview:large">\n'
        + '<meta property="og:title" content="%s">\n' % title
        + '<meta property="og:description" content="%s">\n' % desc
        + '<meta property="og:type" content="website">\n'
        + '<meta property="og:url" content="%s">\n' % url
        + '<meta property="og:image" content="%s">\n' % image
        + '<meta name="twitter:card" content="summary_large_image">\n'
        + '<meta name="twitter:title" content="%s">\n' % title
        + '<meta name="twitter:description" content="%s">\n' % desc
        + '<meta name="twitter:image" content="%s">\n' % image
        + '<link rel="canonical" href="%s">\n' % url
        + '<meta name="theme-color" content="#08243f">\n'
        '<link rel="preload" href="/fonts/montserrat-var.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="preload" href="/fonts/anton-400.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="preload" href="/fonts/caveat-700-v2.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="stylesheet" href="/css/site.css">\n'
        + ld
        + "\n"
    )


def crumb(mid_label, mid_href, leaf):
    m = ('<li><a href="%s">%s</a></li>\n    ' % (mid_href, mid_label)) if mid_href else ""
    return (
        '<nav class="breadcrumb" aria-label="Breadcrumb">\n  <ol>\n'
        '    <li><a href="/">Home</a></li>\n    '
        + m
        + '<li><span aria-current="page">%s</span></li>\n  </ol>\n</nav>\n' % leaf
    )


def faq_ld(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


def breadcrumb_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(items)
        ],
    }


def service_ld(stype, name, desc, url):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": stype,
        "name": name,
        "description": desc,
        "url": url,
        "areaServed": {"@type": "City", "name": CITY, "addressRegion": "OH",
                       "addressCountry": "US"},
        "provider": {"@id": BID},
    }


def faq_html(heading, sub, pairs):
    items = "\n".join(
        '      <div class="faq-item">\n'
        '        <button class="faq-q" onclick="toggleFaq(this)">%s</button>\n'
        '        <div class="faq-a">%s</div>\n'
        "      </div>" % (q, a)
        for q, a in pairs
    )
    return (
        '<section class="bg-off">\n  <div class="container">\n'
        + '    <div class="section-label">' + CITY + ' Questions</div>\n'
        + "    <h2>%s</h2>\n"
        '    <p class="section-sub">%s</p>\n'
        '    <div class="faq-grid">\n%s\n    </div>\n  </div>\n</section>\n'
        % (heading, sub, items)
    )


def write(path, title, desc, url, image, extra_ld, crumbs, body):
    out = head(title, desc, url, image, extra_ld) + AFTER_HEAD + crumbs + \
        "\n<main>\n" + body + FOOTER
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
    words = len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).split())
    print("  %-30s %4d words in <main>" % ("/" + path + "/", words))
