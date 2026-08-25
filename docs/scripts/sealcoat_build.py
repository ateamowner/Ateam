#!/usr/bin/env python3
"""Build the 7 seal-coating pages (Tipp City + the 6 satellite cities that
already have a multi-city service footprint via pressure washing).

Chrome (head boilerplate, header/nav, mobile drawer, breadcrumb shell,
footer, scripts) is lifted from pressure-washing-troy-ohio/index.html,
which already uses the shared /css/site.css stylesheet rather than an
inline <style> block -- the newer, current convention for any page that's
part of a multi-city set. Content between <main> and </main> is written
fresh per city below; nothing is templated boilerplate.

Run from anywhere; paths are relative to the repo root.
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "website")
CHROME_SRC = os.path.join(ROOT, "pressure-washing-troy-ohio", "index.html")
BID = "https://ateamcontractings.com/#business"
RATE = 2
PHONE_DISPLAY = "(937) 777-9093"
PHONE_TEL = "tel:+19377779093"

src = open(CHROME_SRC, encoding="utf-8").read()
HEAD_OPEN = src[: src.index("<title>")]
# Everything from </head> through the opening <main> tag, i.e. topbar/header/breadcrumb-shell.
AFTER_HEAD = src[src.index("</head>") : src.index('<nav class="breadcrumb"')]
FOOTER = src[src.index("</main>") :]

BUSINESS_LD = json.loads(
    re.search(
        r'<script type="application/ld\+json">(\{"@context":"https://schema\.org","@type":"HomeAndConstructionBusiness".*?\})</script>',
        src,
    ).group(1)
)


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def head(cfg):
    title = cfg["title"]
    desc = cfg["desc"]
    url = cfg["url"]
    image = cfg["image"]
    h = HEAD_OPEN
    h += f"<title>{esc(title)}</title>\n"
    h += f'<meta name="description" content="{esc(desc)}">\n'
    h += '<meta name="author" content="Anthony Leonard, A Team Contracting">\n'
    h += f'<meta name="geo.placename" content="{cfg["city"]}, Ohio">\n'
    h += '<meta name="geo.region" content="US-OH">\n'
    h += '<meta name="robots" content="index, follow, max-image-preview:large">\n'
    h += f'<meta property="og:title" content="{esc(title)}">\n'
    h += f'<meta property="og:description" content="{esc(desc)}">\n'
    h += '<meta property="og:type" content="website">\n'
    h += f'<meta property="og:url" content="{url}">\n'
    h += f'<meta property="og:image" content="{image}">\n'
    h += '<meta name="twitter:card" content="summary_large_image">\n'
    h += f'<meta name="twitter:title" content="{esc(title)}">\n'
    h += f'<meta name="twitter:description" content="{esc(desc)}">\n'
    h += f'<meta name="twitter:image" content="{image}">\n'
    h += f'<link rel="canonical" href="{url}">\n'
    h += '<meta name="theme-color" content="#08243f">\n'
    h += '<link rel="preload" href="/fonts/montserrat-var.woff2" as="font" type="font/woff2" crossorigin>\n'
    h += '<link rel="preload" href="/fonts/anton-400.woff2" as="font" type="font/woff2" crossorigin>\n'
    h += '<link rel="preload" href="/fonts/caveat-700-v2.woff2" as="font" type="font/woff2" crossorigin>\n'
    h += '<link rel="stylesheet" href="/css/site.css">\n'

    service_ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Seal Coating",
        "name": f"Seal Coating in {cfg['city']}, Ohio",
        "description": cfg["service_desc"],
        "url": url,
        "areaServed": {"@type": "City", "name": cfg["city"], "addressRegion": "OH", "addressCountry": "US"},
        "provider": {"@id": BID},
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Published rate",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {"@type": "Service", "name": "Clear acrylic seal coating, concrete or roof"},
                    "priceSpecification": {
                        "@type": "UnitPriceSpecification",
                        "price": str(RATE),
                        "priceCurrency": "USD",
                        "unitCode": "FTK",
                        "unitText": "square foot",
                    },
                }
            ],
        },
    }
    h += '<script type="application/ld+json">' + json.dumps(service_ld, separators=(",", ":")) + "</script>\n"

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in cfg["faqs"]
        ],
    }
    h += '<script type="application/ld+json">' + json.dumps(faq_ld, separators=(",", ":")) + "</script>\n"

    h += '<script type="application/ld+json">' + json.dumps(BUSINESS_LD, separators=(",", ":")) + "</script>\n"

    crumb_items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://ateamcontractings.com/"}]
    if cfg["is_base"]:
        crumb_items.append({"@type": "ListItem", "position": 2, "name": "Seal Coating", "item": url})
    else:
        crumb_items.append(
            {"@type": "ListItem", "position": 2, "name": "Seal Coating", "item": "https://ateamcontractings.com/seal-coating-tipp-city-ohio/"}
        )
        crumb_items.append({"@type": "ListItem", "position": 3, "name": f"{cfg['city']}, OH", "item": url})
    breadcrumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumb_items}
    h += '<script type="application/ld+json">' + json.dumps(breadcrumb_ld, separators=(",", ":")) + "</script>\n"

    return h


def breadcrumb_nav(cfg):
    if cfg["is_base"]:
        items = '<li><a href="/">Home</a></li>\n    <li><span aria-current="page">Seal Coating</span></li>'
    else:
        items = (
            '<li><a href="/">Home</a></li>\n    '
            '<li><a href="/seal-coating-tipp-city-ohio/">Seal Coating</a></li>\n    '
            f'<li><span aria-current="page">{cfg["city"]}, OH</span></li>'
        )
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">\n  <ol>\n    {items}\n  </ol>\n</nav>\n'


def calculator_section(cfg):
    return f"""<section class="bg-off">
  <div class="container">
    <div class="section-label">See Your Price</div>
    <h2>What Would It Cost <em>You</em>?</h2>
    <p class="section-sub">{cfg['calc_intro']}</p>
    <form class="calc-card" id="calc">
      <div class="calc-field">
        <label for="calc-sqft">Approximate square footage</label>
        <input type="number" id="calc-sqft" min="0" max="20000" step="10" placeholder="e.g. 600" inputmode="numeric">
        <input type="range" id="calc-sqft-range" min="0" max="4000" step="10" value="0" aria-label="Square footage slider">
      </div>
      <div class="calc-result">
        <span class="calc-result-label">Your price</span>
        <span class="calc-result-price" id="calc-price">&mdash;</span>
      </div>
      <p class="calc-note">A ballpark, not a quote &mdash; very small areas can carry a minimum service charge, and the final number is always confirmed on site before we start. Not sure of the square footage? Pace it off or just estimate; we'll measure for real when we come out.</p>
      <a href="sms:+19377779093" id="calc-cta" class="calc-cta">Text This Number to Get Booked &rarr;</a>
    </form>
  </div>
</section>
"""


def build_body(cfg):
    o = []
    a = o.append

    a('<section class="page-hero">\n  <div class="container">')
    a(f'    <div class="section-label">{cfg["hero_label"]}</div>')
    a(f'    <h1>{cfg["h1"]}</h1>')
    a(f'    <p>{cfg["hero_p"]}</p>')
    a('    <div class="hero-btns">')
    a(f'      <a href="#calc" class="btn btn-orange">See Your Price ↓</a>')
    a(f'      <a href="{PHONE_TEL}" class="btn btn-outline">Call {PHONE_DISPLAY}</a>')
    a("    </div>")
    a('    <div class="hero-stats">')
    for num, label in cfg["stats"]:
        a(f'      <div><div class="stat-num">{num}</div><div class="stat-label">{label}</div></div>')
    a("    </div>\n  </div>\n</section>\n")

    a(calculator_section(cfg))

    a("<section>\n  <div class=\"container prose\">")
    a(f'    <div class="section-label">Local Knowledge</div>')
    a(f'    <h2>{cfg["local_h2"]}</h2>')
    a(f'    <p class="lede">{cfg["local_lede"]}</p>')
    for h3, p in cfg["local_sections"]:
        a(f"    <h3>{h3}</h3>")
        a(f"    <p>{p}</p>")
    a('    <div class="callout">')
    a(f'      <h3>{cfg["callout_h3"]}</h3>')
    a(f'      <p>{cfg["callout_p"]}</p>')
    a("    </div>\n  </div>\n</section>\n")

    a('<section class="bg-off">\n  <div class="container">')
    a('    <div class="section-label">What We Seal</div>')
    a("    <h2>Concrete and Roofs, One Product</h2>")
    a('    <div class="link-grid">')
    a(
        f'      <a class="link-card" href="/concrete-cleaning-tipp-city-ohio/"><h3>Concrete Driveways &amp; Patios</h3>'
        f"<p>{cfg['seal_note_concrete']}</p>"
        '<span class="go">Concrete cleaning details →</span></a>'
    )
    a(
        f'      <a class="link-card" href="/roof-cleaning-tipp-city-ohio/"><h3>Roofs</h3>'
        f"<p>{cfg['seal_note_roof']}</p>"
        '<span class="go">Roof cleaning details →</span></a>'
    )
    a(
        f'      <a class="link-card" href="/pressure-washing-{cfg["slug"]}-ohio/"><h3>Pressure Washing First</h3>'
        f"<p>{cfg['seal_note_pw']}</p>"
        '<span class="go">Pressure washing details →</span></a>'
    )
    a("    </div>\n  </div>\n</section>\n")

    a('<section class="bg-off">\n  <div class="container">')
    a(f'    <div class="section-label">{cfg["city"]} Questions</div>')
    a(f"    <h2>Seal Coating in {cfg['city']} — FAQ</h2>")
    a(f'    <p class="section-sub">Straight answers. If yours isn\'t here, call or text {PHONE_DISPLAY}.</p>')
    a('    <div class="faq-grid">')
    for q, ans in cfg["faqs"]:
        a('      <div class="faq-item">')
        a(f'        <button class="faq-q" onclick="toggleFaq(this)">{q}</button>')
        a(f'        <div class="faq-a">{ans}</div>')
        a("      </div>")
    a("    </div>\n  </div>\n</section>\n")

    a('<div class="cta-band">\n  <div class="container">')
    a(f"    <h2>Get a {cfg['city']} Seal Coating Price</h2>")
    a("    <p>Use the calculator above for a ballpark, or send us your square footage directly. Takes about a minute.</p>")
    a(f'    <a href="#calc" class="btn btn-orange" style="margin-right:.75rem">See Your Price →</a>')
    a(f'    <a href="{PHONE_TEL}" style="color:rgba(255,255,255,.9);font-weight:700;font-size:.9rem">or call {PHONE_DISPLAY}</a>')
    a("  </div>\n</div>\n")

    return "\n".join(o)


def footer_for(cfg):
    f = FOOTER
    services_old = '<li><a href="/concrete-cleaning-tipp-city-ohio/">Concrete Cleaning</a></li>'
    services_new = services_old + '\n          <li><a href="/seal-coating-tipp-city-ohio/">Seal Coating</a></li>'
    f = f.replace(services_old, services_new, 1)
    f = f.replace(
        '<script src="/assets/lead-form.js" defer></script>',
        '<script src="/assets/lead-form.js" defer></script>\n<script src="/assets/sealcoat-calc.js" defer></script>',
    )
    if "/assets/lead-form.js" not in f:
        f = f.replace(
            "</script>\n\n<script async id=\"netlify-rum-container\"",
            "</script>\n<script src=\"/assets/sealcoat-calc.js\" defer></script>\n\n<script async id=\"netlify-rum-container\"",
            1,
        )
    return f


def mobile_drawer_and_after_head(cfg):
    h = AFTER_HEAD
    old = '<a href="/concrete-cleaning-tipp-city-ohio/">Concrete Cleaning</a>'
    new = old + '\n    <a href="/seal-coating-tipp-city-ohio/">Seal Coating</a>'
    h = h.replace(old, new, 1)
    return h


def general_faqs(city):
    return [
        (
            "Do I need the surface cleaned before sealing?",
            "Yes, always. Sealer applied over dirt, algae or old coating traps it underneath and fails early &mdash; sometimes within a season. Every seal coating job we do includes a wash first, or we confirm the surface is already clean enough before we start.",
        ),
        (
            f"What does a typical driveway cost to seal in {city}?",
            "At $2 per square foot, a standard 500 sq ft driveway runs about $1,000. Use the calculator above with your own square footage for an exact ballpark.",
        ),
    ]


CITIES = [
    dict(
        slug="tipp-city", city="Tipp City", is_base=True,
        title="Seal Coating in Tipp City, Ohio | A Team Contracting",
        desc="Clear, water-based acrylic seal coating for concrete driveways, patios and roofs in Tipp City, OH. $2 per square foot, flat rate. Call (937) 777-9093.",
        image="https://ateamcontractings.com/images/gallery/gallery-pressure-wash-2.webp",
        service_desc="Clear water-based acrylic seal coating for concrete and roofs in Tipp City, OH. $2 per square foot flat rate, applied after a full wash.",
        hero_label="Tipp City, Ohio &middot; Family-Owned",
        h1="Seal It Before <em>Ohio Winter Does</em>",
        hero_p="A clear, water-based acrylic sealer for concrete driveways, patios, walkways and roofs &mdash; applied after a full wash, priced at a flat $2 per square foot. No size tiers, no guessing.",
        stats=[("$2/sq ft", "Flat rate, every surface"), ("2 Surfaces", "Concrete or roof"), ("24&ndash;48 hrs", "Before it's ready for traffic")],
        local_h2="Why Sealing Matters Here",
        local_lede="Tipp City sits square in Ohio's freeze-thaw belt. Water that soaks into unsealed concrete freezes, expands, and pops the surface loose one winter at a time &mdash; the pitting and flaking you see on driveways poured in the 1990s that were never sealed.",
        local_sections=[
            ("What a sealer actually stops", "A clear acrylic sealer sheds water instead of letting it soak in. Less water in the concrete means less freeze-thaw damage, less deicing-salt scaling in the pores, and less staining from oil, leaves and tire marks. It doesn't change the color or look of the surface &mdash; it just keeps it from breaking down."),
            ("Best paired with a wash, not a substitute for one", 'Sealer bonds to concrete or shingles, not to dirt, algae or old grime sitting on top of them. Every seal coating job we do starts with a proper wash and a full dry-out &mdash; see <a href="/concrete-cleaning-tipp-city-ohio/">concrete cleaning</a> and <a href="/roof-cleaning-tipp-city-ohio/">roof cleaning</a> for what that looks like on its own.'),
        ],
        callout_h3="One flat rate, no tiers",
        callout_p='Most of our other services price off your home\'s size because the job scales with the house. Sealing scales with square footage directly, so that\'s exactly how we price it: $2 per square foot, concrete or roof, no guessing which "tier" your driveway falls into.',
        seal_note_concrete="Freeze-thaw is the real enemy here &mdash; a clear acrylic topcoat keeps water from soaking into the slab and expanding when it freezes, the single biggest cause of Ohio driveway pitting.",
        seal_note_roof="Applied after a roof soft wash, the same sealer adds a water-resistant layer that helps shingles shed rain instead of holding it.",
        seal_note_pw="Sealer only bonds to a clean surface, so a pressure wash or surface-cleaner pass on the concrete comes first, with full dry time before we seal.",
        calc_intro="One flat rate across Tipp City, no size tiers to guess between: $2 per square foot, concrete or roof. Enter your approximate square footage below.",
        faqs=[
            ("Can you seal my roof and driveway in the same visit?", "Yes &mdash; we regularly do both while we're already on site. Ask for a combined price when you reach out."),
            *general_faqs("Tipp City"),
            ("How long does a seal coat last in Tipp City?", "One to three years is typical here, depending on how many freeze-thaw cycles the surface goes through each winter and how much traffic it sees. We'll tell you honestly when a recoat is worth it."),
            ("How soon can I drive on a freshly sealed driveway?", "Plan on 24 to 48 hours before regular vehicle traffic. Foot traffic is usually fine within a few hours."),
            ("Will it make my driveway or roof slippery?", "We use sealers formulated for outdoor foot and vehicle traffic, not a high-gloss indoor product, so it shouldn't leave a slick film. If a spot ever feels slicker than expected after rain, tell us and we'll look at it."),
        ],
    ),
    dict(
        slug="troy", city="Troy", is_base=False,
        title="Seal Coating in Troy, Ohio | A Team Contracting",
        desc="Clear acrylic seal coating for concrete driveways and roofs in Troy, OH. $2/sq ft flat rate. Family-owned, 6 miles from our Tipp City shop. Call (937) 777-9093.",
        image="https://ateamcontractings.com/images/gallery/gallery-tt-18.webp",
        service_desc="Clear water-based acrylic seal coating for concrete and roofs in Troy, OH. $2 per square foot flat rate.",
        hero_label="Troy, Ohio &middot; Six Miles From Our Shop",
        h1="Troy Concrete, <em>Protected Not Just Cleaned</em>",
        hero_p="The newer Troy subdivisions off Peters Road and Barnhart Road are old enough now that their driveway concrete is starting to show its age. A clear acrylic sealer, applied after a wash, is the difference between a driveway that keeps degrading and one that stops.",
        stats=[("6 mi", "From Tipp City to Troy"), ("$2/sq ft", "Flat rate, every surface"), ("1&ndash;3 yrs", "Typical life of a sealed coat")],
        local_h2="Why Troy's Newer Concrete Needs This Now",
        local_lede="Troy's building boom off Peters Road, Barnhart Road and Stonebridge in the 1990s and 2000s means a lot of this city's driveway concrete just crossed the twenty-to-thirty-year mark &mdash; old enough for surface wear to start showing, young enough that sealing now actually saves it.",
        local_sections=[
            ("Concrete has a lifecycle, and sealing extends it", "Unsealed concrete absorbs water every time it rains or snows. Over enough winters, that water freezing and expanding inside the pores is what causes the pitting, flaking and hairline cracking you start to notice on a twenty-year-old driveway. A sealer doesn't undo existing damage, but it stops feeding it."),
            ("The historic core is a different job", "We treat Troy's older brick homes near West Main and the Public Square differently for cleaning &mdash; soft wash, masonry-safe detergent &mdash; and the same logic carries over to sealing: brick and older mortar aren't candidates for the same acrylic concrete sealer, so we scope that separately if it comes up."),
        ],
        callout_h3="Sealing doesn't fix a driveway that's already cracked",
        callout_p="If your concrete already has active cracking or heaving, sealing slows further water damage but won't repair what's already broken. We'll tell you straight if a driveway is past the point where sealing alone is the right call.",
        seal_note_concrete="Troy's newer subdivision concrete is entering the age range where sealing meaningfully slows further pitting and cracking from decades of freeze-thaw exposure.",
        seal_note_roof="The same clear acrylic sealer goes on Troy roofs after a soft wash, adding a water-resistant layer once the black streaks and moss are gone.",
        seal_note_pw="A Troy driveway gets a pressure wash or surface-cleaner pass first &mdash; sealer trapped over dirt or algae fails early, so this step never gets skipped.",
        calc_intro="Same $2 per square foot rate whether it's a Peters Road driveway or a downtown walkway &mdash; no travel fee, no size tier, just square footage times the rate.",
        faqs=[
            ("Do you charge extra to seal a driveway in Troy?", "No. Troy is about six miles up US-25A from our shop &mdash; we're there most weeks anyway. There's no travel surcharge; the $2 per square foot rate is the same as a Tipp City address."),
            *general_faqs("Troy"),
            ("How long will a seal coat last on a Troy driveway?", "Usually one to three years, depending on traffic and how many hard freezes it goes through &mdash; the newer subdivisions off Peters and Barnhart tend to need it sooner than a driveway that's already held up for decades."),
            ("How soon can I park in the driveway after sealing?", "Give it 24 to 48 hours before regular vehicle traffic; foot traffic is fine after a few hours."),
            ("Can you seal the older brick homes near the Public Square?", "Not with the same product. Brick and historic lime mortar need a masonry-specific sealer, not the acrylic concrete/roof sealer we use for driveways and asphalt shingles. Ask us and we'll scope it separately if that's what you need."),
        ],
    ),
    dict(
        slug="vandalia", city="Vandalia", is_base=False,
        title="Seal Coating in Vandalia, Ohio | A Team Contracting",
        desc="Clear acrylic seal coating for concrete and roofs in Vandalia, OH. $2/sq ft flat rate, no travel charge. Call (937) 777-9093.",
        image="https://ateamcontractings.com/images/gallery/gallery-tt-20.webp",
        service_desc="Clear water-based acrylic seal coating for concrete and roofs in Vandalia, OH. $2 per square foot flat rate.",
        hero_label="Vandalia, Ohio &middot; Fifteen Minutes From Our Shop",
        h1="Vandalia Concrete Sees <em>More Salt Than Most</em>",
        hero_p="Vandalia sits at the interchange of two interstates, which means more winter road salt tracked onto driveways than almost anywhere else we work. A sealer is the one thing that actually stops salt from scaling the surface.",
        stats=[("15 min", "From Tipp City to Vandalia"), ("$2/sq ft", "Flat rate, every surface"), ("1&ndash;3 yrs", "Typical life of a sealed coat")],
        local_h2="Salt Is the Real Threat to Vandalia Driveways",
        local_lede="Living at the intersection of I-70 and I-75 and next to Dayton International Airport means Vandalia roads and driveways see heavier winter salting than most of Miami County &mdash; and salt is harder on unsealed concrete than plain water is.",
        local_sections=[
            ("How salt damages concrete", "Deicing salt lowers the freezing point of water sitting in concrete's pores, which sounds helpful until that saltwater still eventually freezes and expands &mdash; with more force than plain water. The result is surface scaling: the flaky, crumbling top layer you see on older, unsealed driveways near well-salted roads."),
            ("A sealer blocks the pores salt gets into", "A clear acrylic sealer closes off the surface so salt brine can't soak in and sit through a freeze cycle. It won't stop salt from reaching your car, but it meaningfully slows the damage to the concrete itself."),
        ],
        callout_h3="Rinse before winter if you can't reseal yet",
        callout_p="If your driveway isn't sealed yet this season, hosing off salt residue after a storm &mdash; instead of letting it sit &mdash; buys you real time. It's not a substitute for sealing, just a stopgap.",
        seal_note_concrete="With more winter road salt in the area than most of Miami County, a sealer here is doing real work &mdash; it closes the pores salt brine would otherwise soak into.",
        seal_note_roof="The same clear acrylic sealer also protects Vandalia roofs after a soft wash, adding a water-resistant layer against the area's exposure.",
        seal_note_pw="Given how much winter salt residue builds up on Vandalia driveways, a thorough pressure wash before sealing matters even more than usual.",
        calc_intro="Whatever your Vandalia driveway or roof measures out to, the math is the same: $2 per square foot, no separate rate for how much salt it's seen.",
        faqs=[
            ("Does the airport or interstate traffic make sealing more important here?", "Yes, genuinely. Vandalia's driveways see more winter deicing salt than most of the area because of how much salted road traffic runs through here. Salt accelerates concrete surface scaling, and a sealer is the direct countermeasure."),
            ("Does the extra salt exposure mean I need to reseal more often here?", "Possibly a bit sooner than a low-salt area &mdash; figure one to three years, toward the shorter end if your driveway backs up to a heavily salted road. We'll check the surface and tell you honestly when it's due."),
            ("How soon can I drive on it after sealing?", "24 to 48 hours for regular vehicle traffic; foot traffic is fine within a few hours."),
            *general_faqs("Vandalia"),
            ("Do you charge extra to come to Vandalia?", "No. Vandalia is about fifteen minutes down 25A from our shop &mdash; the $2 per square foot rate is the same as anywhere else we serve."),
        ],
    ),
    dict(
        slug="huber-heights", city="Huber Heights", is_base=False,
        title="Seal Coating in Huber Heights, Ohio | A Team Contracting",
        desc="Clear acrylic seal coating for concrete driveways and roofs in Huber Heights, OH. $2/sq ft flat rate. Call (937) 777-9093.",
        image="https://ateamcontractings.com/images/gallery/gallery-tt-3.webp",
        service_desc="Clear water-based acrylic seal coating for concrete and roofs in Huber Heights, OH. $2 per square foot flat rate.",
        hero_label="Huber Heights, Ohio &middot; Twenty Minutes From Our Shop",
        h1="Some of the <em>Oldest Concrete</em> We Seal",
        hero_p="Huber Heights was built out fast starting in 1956 &mdash; thousands of brick ranches on original concrete driveways that are now pushing seventy years old. If yours has never been sealed, it's had a long time to soak up water it didn't need to.",
        stats=[("20 min", "From Tipp City to Huber Heights"), ("$2/sq ft", "Flat rate, every surface"), ("1950s+", "When most of this concrete was poured")],
        local_h2="Brick City's Driveways Are Older Than They Look",
        local_lede="Charles Huber built this town out of brick starting in 1956, and a lot of the original concrete driveways and walkways from that first wave are still down &mdash; meaning some of the oldest concrete stock anywhere in our service area.",
        local_sections=[
            ("Older concrete, more freeze-thaw cycles absorbed", "A driveway poured in the late 1950s has been through nearly seventy Ohio winters. If it was never sealed, it's absorbed and released water through every one of them. Sealing now doesn't undo seven decades, but it stops the clock on further water damage."),
            ("Roofs on original ranch homes benefit too", "Many of Huber Heights' original ranch homes have low-slope roof sections where standing water is more of an issue than on a steep pitch. A clear acrylic sealer adds a water-resistant layer on top of a cleaned roof, the same product used on concrete."),
        ],
        callout_h3="We check condition before we quote",
        callout_p="On concrete this old, we look for active cracking or heaving before recommending sealing. If a section is already failing structurally, sealing slows further water intrusion but isn't a repair &mdash; we'll always tell you which situation you're in.",
        seal_note_concrete="On concrete this old &mdash; some of it pushing seventy years &mdash; sealing doesn't reverse decades of wear, but it stops feeding the water damage that's still actively happening.",
        seal_note_roof="The same sealer also goes on the low-slope roof sections common on Huber Heights' original ranch homes, adding a water-resistant layer where standing water is more of a concern.",
        seal_note_pw="Decades-old Huber Heights concrete usually needs a more thorough pressure-washing pass to lift embedded grime before sealer will bond properly.",
        calc_intro="Original 1950s slab or a newer addition, the rate doesn't change in Huber Heights: $2 per square foot, concrete or roof.",
        faqs=[
            ("Is my driveway too old to bother sealing?", "Almost never, as long as it's not actively cracking or heaving. Sealing a decades-old driveway still slows further water damage &mdash; it just won't undo damage that's already there. We'll look at yours and give you a straight answer."),
            *general_faqs("Huber Heights"),
            ("Will an older driveway hold a seal coat as well as a newer one?", "Yes, as long as it's not actively cracking or heaving. Expect roughly one to three years before a recoat is worth considering, same as newer concrete."),
            ("How soon can I drive on it?", "Plan on 24 to 48 hours; foot traffic is fine after a few hours."),
            ("Do you charge extra to come to Huber Heights?", "No &mdash; Huber Heights is about twenty minutes from our Tipp City shop, and the $2 per square foot rate doesn't change based on distance."),
        ],
    ),
    dict(
        slug="fairborn", city="Fairborn", is_base=False,
        title="Seal Coating in Fairborn, Ohio | A Team Contracting",
        desc="Clear acrylic seal coating for concrete and roofs in Fairborn, OH. $2/sq ft flat rate. Call (937) 777-9093.",
        image="https://ateamcontractings.com/images/gallery/gallery-pressure-wash-1.webp",
        service_desc="Clear water-based acrylic seal coating for concrete and roofs in Fairborn, OH. $2 per square foot flat rate.",
        hero_label="Fairborn, Ohio &middot; Thirty Minutes From Our Shop",
        h1="One City, <em>One Generation of Concrete</em>",
        hero_p="Fairborn grew to roughly six times its size between 1950 and 1970 &mdash; meaning most of this city's driveway concrete was poured inside one twenty-year window, and a lot of it is hitting the same stage of life at the same time.",
        stats=[("30 min", "From Tipp City to Fairborn"), ("$2/sq ft", "Flat rate, every surface"), ("1950&ndash;70", "When most local concrete was poured")],
        local_h2="Why So Many Fairborn Driveways Need This at Once",
        local_lede="Fairborn's population boom between 1950 and 1970 poured an enormous amount of concrete in a short window. Fifty-plus years later, a lot of that concrete is reaching the point where surface scaling and pitting start showing up &mdash; and it's showing up on a lot of driveways around the same time.",
        local_sections=[
            ("Why one era of concrete ages predictably", "Concrete from the same building boom tends to fail the same way at the same time, because it's the same mix, the same era's finishing techniques, and the same fifty-plus winters of freeze-thaw exposure. If your neighbor's driveway is starting to flake, yours from the same subdivision probably isn't far behind."),
            ("Sealing now is cheaper than replacing later", 'A full driveway replacement costs many times what sealing does. Catching concrete in the "starting to show wear" stage &mdash; rather than the "actively crumbling" stage &mdash; is exactly when a sealer does the most good.'),
        ],
        callout_h3="Not every 1950s&ndash;70s driveway is a fit",
        callout_p="If your driveway already has open cracks or sections heaving from tree roots, sealing slows future water damage but isn't a fix for what's already moved. We'll be straight with you about which category yours falls into before we quote it.",
        seal_note_concrete="Concrete from Fairborn's 1950&ndash;70 building boom is aging on a predictable timeline &mdash; sealing now, before visible scaling shows up, is the cheap move compared to a driveway that's already flaking.",
        seal_note_roof="The same clear acrylic sealer protects Fairborn roofs after a soft wash, adding a water-resistant layer regardless of which decade the roof itself dates to.",
        seal_note_pw="Fairborn's older concrete often carries decades of embedded staining, so we lean on a thorough pressure wash before sealing rather than a quick rinse.",
        calc_intro="Whether your driveway dates to the 1950s boom or was poured last decade, Fairborn pricing is the same flat $2 per square foot.",
        faqs=[
            ("My neighbor's driveway from the same era is already flaking &mdash; is mine next?", "Possibly, if it's never been sealed. Concrete poured in the same building boom tends to age on a similar timeline, since it's the same era's mix and finishing methods absorbing the same fifty-plus years of Ohio winters. Sealing now, while yours still looks fine, is the cheaper move than waiting for visible damage."),
            *general_faqs("Fairborn"),
            ("If my driveway is from that 1950s-70s building boom, how often will it need resealing?", "Plan on one to three years between coats, similar to newer concrete &mdash; the age of the slab affects whether sealing helps at all, not really how long a given coat lasts once it's down."),
            ("How soon can I drive on a freshly sealed driveway?", "24 to 48 hours for regular traffic; foot traffic is fine within a few hours."),
            ("Do you charge extra to come to Fairborn?", "No &mdash; Fairborn is about thirty minutes from our Tipp City shop, and the $2 per square foot rate is the same everywhere we serve."),
        ],
    ),
    dict(
        slug="beavercreek", city="Beavercreek", is_base=False,
        title="Seal Coating in Beavercreek, Ohio | A Team Contracting",
        desc="Clear acrylic seal coating for concrete, including stamped and decorative concrete, in Beavercreek, OH. $2/sq ft flat rate. Call (937) 777-9093.",
        image="https://ateamcontractings.com/images/gallery/gallery-pressure-wash-2.webp",
        service_desc="Clear water-based acrylic seal coating for concrete, including stamped and decorative finishes, and roofs in Beavercreek, OH. $2 per square foot flat rate.",
        hero_label="Beavercreek, Ohio &middot; Thirty Minutes From Our Shop",
        h1="Stamped Concrete <em>Needs This More</em>",
        hero_p="Beavercreek grew subdivision by subdivision, and its newer developments lean heavily on stamped and colored concrete &mdash; finishes that fade and stain faster than plain gray concrete if they're never sealed.",
        stats=[("30 min", "From Tipp City to Beavercreek"), ("$2/sq ft", "Flat rate, every surface"), ("Clear finish", "No color change on stamped work")],
        local_h2="Beavercreek's Decorative Concrete Is a Different Case",
        local_lede="Because Beavercreek grew subdivision by subdivision rather than outward from one center, its driveways and patios span several distinct concrete generations &mdash; and its newer developments favor stamped, colored and exposed-aggregate finishes far more than the plain broom finish common elsewhere in our service area.",
        local_sections=[
            ("Why decorative concrete fades without a sealer", "Stamped and colored concrete gets its look from integral color or a surface stain, and both fade under UV exposure and wear faster than plain concrete without a protective topcoat. An unsealed stamped patio can visibly dull within a few seasons; a sealed one holds its color much longer."),
            ("Clear means clear &mdash; no color change", "The acrylic sealer we use is clear, not tinted, so it won't alter the color of stamped or colored concrete. It adds a protective, slightly enhanced sheen on top of the existing finish rather than changing it."),
        ],
        callout_h3="Older subdivisions still benefit, just for different reasons",
        callout_p="If your section of Beavercreek has plain gray concrete from an earlier build phase, the driveway-protection case for sealing (water, freeze-thaw, salt) applies the same way it does everywhere else &mdash; the color-preservation angle is specific to the newer stamped and decorative work.",
        seal_note_concrete="On stamped or colored concrete especially, an unsealed surface fades and stains faster &mdash; the clear topcoat protects the color investment as much as the slab itself.",
        seal_note_roof="The same clear, non-tinted sealer also goes on Beavercreek roofs after a soft wash, adding a protective layer without changing the shingle color.",
        seal_note_pw="Stamped and decorative concrete needs a gentler pressure-washing approach than plain broom finish, which is exactly what we adjust for before sealing in Beavercreek.",
        calc_intro="Stamped, exposed-aggregate or plain broom finish &mdash; the rate in Beavercreek is the same $2 per square foot either way.",
        faqs=[
            ("Will sealing change the color of my stamped patio?", "No. We use a clear acrylic sealer, not a tinted one, so it won't alter the existing color or stamp pattern &mdash; it just protects the finish you already have from fading and wear."),
            *general_faqs("Beavercreek"),
            ("Does stamped concrete need resealing more often than plain concrete?", "Generally yes &mdash; stamped and colored finishes are more exposed to UV fading, so we often recommend the shorter end of the one-to-three-year range to keep the color looking sharp."),
            ("How soon can I walk or drive on a sealed patio or driveway?", "Foot traffic is usually fine within a few hours; give it 24 to 48 hours before regular vehicle traffic."),
            ("Do you charge extra to come to Beavercreek?", "No &mdash; Beavercreek is about thirty minutes from our Tipp City shop, and the $2 per square foot rate doesn't change with distance."),
        ],
    ),
    dict(
        slug="piqua", city="Piqua", is_base=False,
        title="Seal Coating in Piqua, Ohio | A Team Contracting",
        desc="Clear acrylic seal coating for concrete and roofs in Piqua, OH. $2/sq ft flat rate. Call (937) 777-9093.",
        image="https://ateamcontractings.com/images/gallery/gallery-pressure-wash-2.webp",
        service_desc="Clear water-based acrylic seal coating for concrete and roofs in Piqua, OH. $2 per square foot flat rate.",
        hero_label="Piqua, Ohio &middot; Fifteen Minutes From Our Shop",
        h1="Slow Down How Fast <em>the Green Comes Back</em>",
        hero_p="Piqua's river-valley humidity and mature tree canopy mean algae and moss come back faster here than in drier parts of our service area. Sealing after a wash is the single best way to buy yourself more time before it returns.",
        stats=[("15 min", "From Tipp City to Piqua"), ("$2/sq ft", "Flat rate, every surface"), ("Slower regrowth", "The real payoff of sealing here")],
        local_h2="Why Piqua's Climate Makes Sealing Worth It",
        local_lede="Piqua grew up on the river and the canal, and the river is still setting the terms &mdash; humidity, shade and a mature tree canopy that keeps a lot of this town damp well into the afternoon. That's exactly the environment algae and moss like best.",
        local_sections=[
            ("Damp, shaded surfaces regrow algae fastest", "Algae and moss need moisture to establish, and Piqua's tree cover and river humidity keep concrete and roofing damp longer than sunnier parts of Miami County. A wash removes what's there today; sealing closes off the porous surface algae spores would otherwise latch onto next."),
            ("It won't stop regrowth forever, but it slows it a lot", "No sealer makes a shaded, humid surface immune to algae permanently. What it does is meaningfully extend the time between washes &mdash; often the difference between reappearing in one season versus two or three."),
        ],
        callout_h3="Pair it with your next wash, not a separate visit",
        callout_p="Since sealer has to go on a clean, dry surface anyway, the cheapest way to add it is right after a scheduled wash rather than as its own trip. Ask about combined pricing when you book.",
        seal_note_concrete="In a shaded, humid town like Piqua, sealing closes off the porous surface algae spores would otherwise latch onto &mdash; it won't stop regrowth, but it slows it down a lot.",
        seal_note_roof="The same sealer goes on Piqua roofs after a soft wash, adding a water-resistant layer that also helps slow how fast moss and algae reestablish in the shade.",
        seal_note_pw="Piqua's shaded, humid conditions mean more algae to strip in the pressure-washing pass before sealer goes down &mdash; we budget the extra time for it.",
        calc_intro="River-valley shade or open yard, Piqua pricing doesn't change: $2 per square foot, concrete or roof.",
        faqs=[
            ("Will sealing actually stop the green from coming back?", "It won't stop it completely &mdash; nothing does in a shaded, humid spot like a lot of Piqua &mdash; but it slows regrowth substantially by closing off the porous surface algae spores latch onto. Expect meaningfully longer gaps between washes, not zero regrowth."),
            *general_faqs("Piqua"),
            ("Does Piqua's humidity mean the sealer wears out faster?", "Not the sealer itself &mdash; one to three years is still typical. What changes is how much benefit you get in between: the algae-slowing effect matters more here than in a sunnier, drier part of the service area."),
            ("How soon can I drive on it?", "24 to 48 hours for regular vehicle traffic; foot traffic is fine after a few hours."),
            ("Do you charge extra to come to Piqua?", "No &mdash; Piqua is about fifteen minutes up I-75 from our shop, and the $2 per square foot rate is the same as a Tipp City address."),
        ],
    ),
]

for cfg in CITIES:
    cfg["url"] = f"https://ateamcontractings.com/seal-coating-{cfg['slug']}-ohio/"
    page = head(cfg) + mobile_drawer_and_after_head(cfg) + breadcrumb_nav(cfg) + "\n<main>\n" + build_body(cfg) + footer_for(cfg)
    out_dir = os.path.join(ROOT, f"seal-coating-{cfg['slug']}-ohio")
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)
    n_faq = page.count('class="faq-q"')
    print(f"  seal-coating-{cfg['slug']:14} {len(page)/1024:5.1f} KB  {n_faq} FAQs")

