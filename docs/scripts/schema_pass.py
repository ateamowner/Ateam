#!/usr/bin/env python3
"""
Phase A — complete the business schema across every page.

Three edits per page, all done by parsing the JSON-LD rather than regexing HTML:

 1. Inject ONE canonical HomeAndConstructionBusiness node carrying @id
    "https://ateamcontractings.com/#business" — the single description of the
    business, with sameAs, foundingDate, founder, postalCode, geo and hours.
 2. Collapse every nested `provider` LocalBusiness (a partial duplicate of the
    business on 14 pages) down to a bare {"@id": ...} reference to that node.
    That is what @id is for, and it stops 14 slightly-different copies of the
    business drifting apart.
 3. Add hasOfferCatalog to the Service node, but ONLY on pages that visibly
    publish the price it describes. Marking up a price the visitor cannot see
    is the same manual-action risk as marking up invisible reviews.

Service-area business: there is no streetAddress property anywhere, by design.
"""
import json
import os
import re
import sys

ROOT = "/home/user/Ateam/website"
BUSINESS_ID = "https://ateamcontractings.com/#business"

CITIES = ["Tipp City", "Troy", "Vandalia", "Huber Heights", "Piqua",
          "Dayton", "Englewood", "Fairborn", "Beavercreek", "Covington"]

BUSINESS = {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "@id": BUSINESS_ID,
    "name": "A-Team Contracting",
    "url": "https://ateamcontractings.com/",
    "telephone": "(937) 939-2936",
    "email": "Owner@ateamcontractings.com",
    "image": "https://ateamcontractings.com/images/gallery/gallery-pressure-wash-1.webp",
    "logo": "https://ateamcontractings.com/logo.webp",
    "priceRange": "$",
    "foundingDate": "2023-01-01",
    "founder": {"@type": "Person", "name": "Anthony Leonard"},
    "employee": {"@type": "Person", "name": "Anthony Leonard"},
    # Service-area business. Locality/region/postal only — never streetAddress.
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Tipp City",
        "addressRegion": "OH",
        "postalCode": "45371",
        "addressCountry": "US",
    },
    # Tipp City centroid — the town we work out of, not a street address.
    "geo": {"@type": "GeoCoordinates", "latitude": 39.9581, "longitude": -84.1733},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "opens": "07:00",
        "closes": "19:00",
    }],
    "areaServed": [
        {"@type": "City", "name": c, "addressRegion": "OH", "addressCountry": "US"}
        for c in CITIES
    ],
    "sameAs": [
        "https://g.page/r/CdoEOEshw5VUEAE/",
        "https://www.bbb.org/us/oh/tipp-city/profile/window-cleaning/a-team-contracting-0322-1440107933",
        "https://www.facebook.com/Ateamcontractings/",
        "https://nextdoor.com/page/a-team-contracting-services",
        "https://www.yelp.com/biz/a-team-contracting-tipp-city",
    ],
}

# Real published prices. A page only gets the offer it actually shows.
DRIVEWAY = ("Driveway, sidewalk & concrete pressure washing", "150", "300")
HOUSE = ("Full house exterior wash", "300", "600")


def offer(name, low, high):
    return {
        "@type": "Offer",
        "itemOffered": {"@type": "Service", "name": name},
        "priceSpecification": {
            "@type": "PriceSpecification",
            "minPrice": low,
            "maxPrice": high,
            "priceCurrency": "USD",
        },
    }


def visible_offers(html):
    """Only the ranges the visitor can actually read on this page."""
    out = []
    if "150–$300" in html or "150-$300" in html:
        out.append(offer(*DRIVEWAY))
    if "300–$600" in html or "300-$600" in html:
        out.append(offer(*HOUSE))
    return out


BLOCK_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def process(path):
    rel = os.path.relpath(os.path.dirname(path), ROOT)
    rel = "/" if rel == "." else "/" + rel + "/"
    html = open(path, encoding="utf-8").read()
    original = html
    notes = []

    blocks = BLOCK_RE.findall(html)
    parsed = [json.loads(b) for b in blocks]

    # --- 2. collapse nested provider objects into an @id reference ----------
    def collapse(node):
        changed = False
        if isinstance(node, dict):
            p = node.get("provider")
            if isinstance(p, dict) and p.get("@type") in ("LocalBusiness", "HomeAndConstructionBusiness"):
                node["provider"] = {"@id": BUSINESS_ID}
                changed = True
            pub = node.get("publisher")
            if isinstance(pub, dict) and pub.get("@type") in ("Organization", "LocalBusiness"):
                node["publisher"] = {"@id": BUSINESS_ID}
                changed = True
            for v in node.values():
                changed |= collapse(v)
        elif isinstance(node, list):
            for v in node:
                changed |= collapse(v)
        return changed

    # --- 3. hasOfferCatalog on Service, only where prices are visible -------
    offers = visible_offers(html)

    new_blocks = []
    dropped_old_business = False
    for raw, obj in zip(blocks, parsed):
        # Drop any pre-existing standalone business node; the canonical one replaces it.
        if isinstance(obj, dict) and obj.get("@type") == "HomeAndConstructionBusiness" and "@id" not in obj:
            dropped_old_business = True
            continue
        if collapse(obj):
            notes.append("provider→@id")
        if isinstance(obj, dict) and obj.get("@type") == "Service" and offers and "hasOfferCatalog" not in obj:
            obj["hasOfferCatalog"] = {
                "@type": "OfferCatalog",
                "name": "Published price ranges",
                "itemListElement": offers,
            }
            notes.append("hasOfferCatalog(%d)" % len(offers))
        new = dumps(obj)
        new_blocks.append((raw, new))

    for raw, new in new_blocks:
        if raw != new:
            html = html.replace(
                '<script type="application/ld+json">%s</script>' % raw,
                '<script type="application/ld+json">%s</script>' % new,
                1,
            )
    if dropped_old_business:
        for raw, obj in zip(blocks, parsed):
            if isinstance(obj, dict) and obj.get("@type") == "HomeAndConstructionBusiness" and "@id" not in obj:
                html = html.replace(
                    '<script type="application/ld+json">%s</script>\n' % raw, "", 1)
                html = html.replace(
                    '<script type="application/ld+json">%s</script>' % raw, "", 1)
        notes.append("replaced legacy business node")

    # --- 1. inject the canonical business node -----------------------------
    # Test for the DEFINITION, not the id string: after step 2 most pages carry
    # a bare {"@id": ...} reference, and a substring check on the id would read
    # that reference as "already defined" and leave the node dangling.
    current = [json.loads(b) for b in BLOCK_RE.findall(html)]
    defined = any(
        isinstance(b, dict) and b.get("@id") == BUSINESS_ID
        and b.get("@type") == "HomeAndConstructionBusiness"
        for b in current
    )
    if not defined:
        html = html.replace(
            "</head>",
            '<script type="application/ld+json">%s</script>\n</head>' % dumps(BUSINESS),
            1,
        )
        notes.append("+business")

    if html != original:
        open(path, "w", encoding="utf-8").write(html)
    return rel, notes


def main():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != "node_modules"]
        if "index.html" in filenames:
            files.append(os.path.join(dirpath, "index.html"))
    for path in sorted(files):
        rel, notes = process(path)
        print("  %-46s %s" % (rel, ", ".join(notes) or "-"))
    print("\n  %d pages processed" % len(files))


if __name__ == "__main__":
    sys.exit(main())
