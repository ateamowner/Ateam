#!/usr/bin/env python3
"""Differentiate the four roof-cleaning city pages.

roof-cleaning-{beavercreek,fairborn,huber-heights,vandalia} were generated
from one template: the "What We Clean" cards, the before/after blurb and
three of the five FAQs were byte-identical across all four, which put every
pair at 45-48% shingle overlap -- well over the 30% bar dup_check.py
enforces, and exactly the pattern Google filters a city set for.

Each page's hero and "Local Knowledge" section were already genuinely local
and are left alone. This rewrites only the shared scaffolding, grounding each
city's version in the angle that page already establishes:

  beavercreek   - incorporated 1980, farmland to subdivisions in patches;
                  roof age is not guessable from the address
  fairborn      - the base boom put street after street on one shingle clock;
                  plus the moved pre-1920 Osborn houses
  huber-heights - 10,000+ Huber houses on a few plans, so one street shares
                  one elevation, pitch and sun orientation
  vandalia      - valley floor between the Great Miami and the Stillwater;
                  low ground holds damp, north slopes go first

The service facts are unchanged and must stay that way -- no pressure washer
on shingles, $499 start, beds covered and rinsed, Gloeocapsa magma. Only the
framing varies. The FAQPage JSON-LD is regenerated from the visible accordion
afterwards so the two cannot drift.

Run from anywhere; paths resolve against the repo root. Idempotent.
"""
import json
import pathlib
import re
import html as H

ROOT = pathlib.Path(__file__).resolve().parents[2] / "website"

# --- per-city scaffolding copy -------------------------------------------
CITY = {
    "beavercreek": dict(
        sub="Every street here is a different vintage, so the roof gets read before it gets treated.",
        cards=[
            ("Asphalt Shingle Soft Wash", "Solution, dwell time, gentle rinse. On a 1960s ranch and on a two-story from the I-675 years alike &mdash; the pressure never goes up."),
            ("Black Streaks", "Gloeocapsa magma, feeding on the limestone filler in the shingle. Older Beavercreek roofs have simply given it longer to set in."),
            ("Moss &amp; Lichen", "Rooted into the shingle, not sitting on it. Common on the shaded older lots. We treat and let weather finish it."),
            ("Landscaping Protection", "The newer subdivisions came with real planting beds. They get soaked and covered first, rinsed after."),
        ],
        proof="Shot on the job. Greene County and the Miami Valley.",
        faqs=[
            ("Can you pressure wash a roof?", "You can, and it is the fastest way to ruin one. Pressure takes the granules with the streaks. Beavercreek has a lot of roof out on those bigger newer builds, and none of it sees a wand."),
            ("How much does roof cleaning cost?", "Roof washes start at $499. On this side of the county the spread is wide &mdash; a low 1960s ranch and a two-story off I-675 are different jobs. You get the exact number before we start."),
            ("Will it kill my plants?", "No. Beds get saturated and covered before anything goes up, and rinsed once we are down."),
        ],
    ),
    "fairborn": dict(
        sub="One shingle era, one weather pattern, one method that does not vary.",
        cards=[
            ("Asphalt Shingle Soft Wash", "Low pressure, dwell time, gentle rinse &mdash; the same pass on every roof in a cohort that all went up inside the same twenty years."),
            ("Black Streaks", "Gloeocapsa magma. When a whole street streaks at once it is not neglect, it is one shingle era hitting the same age together."),
            ("Moss &amp; Lichen", "It roots in. Force takes granules with it. We treat it and let the weather clear it off."),
            ("Landscaping Protection", "Beds wet down and covered first, rinsed after. Around the older Osborn houses we take the extra pass at the eaves."),
        ],
        proof="Shot on the job. Greene County and the Miami Valley.",
        faqs=[
            ("Can you pressure wash a roof?", "You can, and you should not. High pressure strips the granules off asphalt shingle. On the older moved Osborn houses it will also drive water where you do not want it."),
            ("How much does roof cleaning cost?", "Roof washes start at $499. Fairborn's post-war stock is fairly consistent in size, so quotes here cluster tighter than most towns. Exact price before we start."),
            ("Will it kill my plants?", "No. Everything below gets saturated and covered before we start, and a full rinse after."),
        ],
    ),
    "huber-heights": dict(
        sub="Ten thousand houses, a handful of plans &mdash; and one method for the shingle on all of them.",
        cards=[
            ("Asphalt Shingle Soft Wash", "Low-pressure solution and a gentle rinse. When a street shares one pitch and one orientation, it also shares one correct approach."),
            ("Black Streaks", "Gloeocapsa magma, feeding on the limestone filler. It is why ten identical elevations streak in the same decade, on the same slope."),
            ("Moss &amp; Lichen", "Rooted into the shingle. We kill it and let the weather take it off &mdash; pulling it costs you granules."),
            ("Landscaping Protection", "Beds covered and soaked before the roof gets touched, rinsed after. The brick below is a separate job, not a pressure job."),
        ],
        proof="Shot on the job. Brick City and the Miami Valley.",
        faqs=[
            ("Can you pressure wash a roof?", "No, and we will not. Granules are the shingle's sunscreen. Strip them and a Huber roof that had years left starts aging in fast-forward."),
            ("How much does roof cleaning cost?", "Roof washes start at $499. Because so many houses here run to the same plan, we can usually tell you a number off one look at the street. Exact price before we start."),
            ("Will it kill my plants?", "No. Beds get saturated and covered first and rinsed thoroughly after."),
        ],
    ),
    "vandalia": dict(
        sub="Low ground, damp air, north slopes first &mdash; the method does not change for any of it.",
        cards=[
            ("Asphalt Shingle Soft Wash", "Low-pressure solution, dwell time, gentle rinse. The long low roofs on the ranch belt take the same care as the newer estates."),
            ("Black Streaks", "Gloeocapsa magma. Down on the valley floor it holds damp against the shingle longer, which is why it takes hold sooner here."),
            ("Moss &amp; Lichen", "It roots into the shingle on the slopes that stay wet. We treat it; the weather clears it. Pulling it takes granules."),
            ("Landscaping Protection", "Beds soaked and covered before anything goes on the roof, rinsed once we are down."),
        ],
        proof="Shot on the job. Miami Valley, north of Dayton.",
        faqs=[
            ("Can you pressure wash a roof?", "You can, and you shouldn't. High pressure strips the granules off asphalt shingle. In a damp spot like this the roof needs every bit of that surface intact."),
            ("How much does roof cleaning cost?", "Roof washes start at $499. Size, pitch, growth, material and access set the rest &mdash; and the ranch belt's long roofs measure bigger than they look. Exact price first."),
            ("Will it kill my plants?", "No. Beds get saturated and covered before we start and rinsed thoroughly after."),
        ],
    ),
}

CARD_RE = re.compile(
    r'(<div class="svc-card"><div class="svc-icon">[^<]*</div><h3>)(.*?)(</h3><p>)(.*?)(</p></div>)'
)


def strip_tags(s):
    return H.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def rewrite(city, cfg):
    p = ROOT / f"roof-cleaning-{city}-ohio" / "index.html"
    t = p.read_text(encoding="utf-8")

    # 1. "What We Clean" section-sub
    t, n = re.subn(
        r'(<div class="section-label">What We Clean</div>\s*\n\s*<h2>[^<]*</h2>\s*\n\s*<p class="section-sub">)[^<]*(</p>)',
        lambda m: m.group(1) + cfg["sub"] + m.group(2),
        t,
    )
    assert n == 1, f"{city}: What We Clean sub matched {n}x"

    # 2. the four service cards (headings/icons kept, body copy varied)
    want = {h: b for h, b in cfg["cards"]}
    def card_sub(m):
        head = m.group(2)
        return m.group(1) + head + m.group(3) + want.get(head, m.group(4)) + m.group(5)
    t, n = CARD_RE.subn(card_sub, t)
    assert n == 4, f"{city}: matched {n} svc-cards, expected 4"

    # 3. before/after blurb
    t, n = re.subn(
        r'(<div class="section-label">Real Work</div>\s*\n\s*<h2>[^<]*</h2>\s*\n\s*<p class="section-sub">)[^<]*(</p>)',
        lambda m: m.group(1) + cfg["proof"] + m.group(2),
        t,
    )
    assert n == 1, f"{city}: Real Work sub matched {n}x"

    # 4. the three shared FAQs (the two city-specific ones are left alone)
    for q, a in cfg["faqs"]:
        pat = re.compile(
            r'(<button class="faq-q" onclick="toggleFaq\(this\)">'
            + re.escape(q)
            + r'</button>\s*\n\s*<div class="faq-a">)(.*?)(</div>)',
            re.S,
        )
        t, n = pat.subn(lambda m: m.group(1) + a + m.group(3), t)
        assert n == 1, f"{city}: FAQ {q!r} matched {n}x"

    # 5. regenerate FAQPage JSON-LD from the visible accordion so they cannot drift
    pairs = re.findall(
        r'<button class="faq-q"[^>]*>(.*?)</button>\s*\n\s*<div class="faq-a">(.*?)</div>',
        t,
        re.S,
    )
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": strip_tags(q),
                "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)},
            }
            for q, a in pairs
        ],
    }
    new_ld = '<script type="application/ld+json">' + json.dumps(faq_ld, separators=(",", ":")) + "</script>"
    t, n = re.subn(
        r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"FAQPage".*?</script>',
        lambda _m: new_ld,
        t,
        flags=re.S,
    )
    assert n == 1, f"{city}: FAQPage schema matched {n}x"

    p.write_text(t, encoding="utf-8")
    print(f"  {city:14} {len(pairs)} FAQs, schema regenerated from visible copy")


for city, cfg in CITY.items():
    rewrite(city, cfg)
