# A Team Contracting — Local Keyword Map

**Prepared:** 2026-09-02
**Scope:** window cleaning, pressure washing, power washing, soft washing, house washing, roof cleaning, gutter cleaning, concrete cleaning, driveway sealing / seal coating
**Markets:** Tipp City, Troy, Vandalia, Huber Heights, Piqua, Dayton, Englewood, Fairborn, Beavercreek OH

---

## 0. DATA SOURCE STATUS — READ THIS FIRST

| Source | Status | Result |
|---|---|---|
| Ahrefs MCP (`keywords-explorer-overview`) | **FAILED** | `{"error": "Insufficient plan"}` |
| Ahrefs MCP (`keywords-explorer-search-suggestions`) | **FAILED** | `{"error": "Insufficient plan"}` |
| Ahrefs MCP (`subscription-info-limits-and-usage`, a free endpoint) | **FAILED** | `{"error": "Insufficient plan"}` — the whole Ahrefs connection is plan-blocked, not just paid endpoints |
| Semrush MCP (`keyword_research`) | **FAILED** | Active subscription, but **zero API units remaining**. Semrush directs the account owner to https://www.semrush.com/mcp-access to add units. |
| WebSearch (fallback) | **WORKED** | Used for SERP/autocomplete/"people also ask" style discovery and competitor page-pattern reading |

### Consequence

**No verified search volume or keyword difficulty figures exist in this document.**
Every priority signal below is an **UNVERIFIED ESTIMATE**, derived from:
- Relative city population / household count in the Miami Valley
- SERP composition observed via WebSearch (how many directory aggregators vs. real local businesses rank)
- Which query phrasings actually surfaced content in live search results
- Standard home-services search behavior patterns

To avoid fabricating numbers, this map uses **demand tiers (A / B / C)** rather than invented monthly volumes. Re-run this map once Ahrefs plan access or Semrush API units are restored, and replace every tier with a real number.

**Demand tier legend (UNVERIFIED ESTIMATE throughout):**
- **Tier A** — highest relative local demand in this service area
- **Tier B** — solid, worth a dedicated page
- **Tier C** — thin; fold into a parent page rather than building a standalone page

---

## 1. Head terms per service

No verified volume/difficulty available (see §0). Ranked by estimated relative national/regional demand and by commercial intent.

| Head term | Est. relative demand | Commercial intent | Notes |
|---|---|---|---|
| pressure washing | Tier A | High | The umbrella term most homeowners actually type; broadest of the set |
| power washing | Tier A | High | Near-synonym of "pressure washing." Treat as an alias, **not** a separate page — same intent, same SERP |
| window cleaning | Tier A | High | Second-strongest service term; also the natural anchor for a recurring/membership offer |
| house washing | Tier B | High | Rising term, more specific than "pressure washing"; strongly residential |
| gutter cleaning | Tier B | High | Highly seasonal (fall spike), high repeat rate, very underbuilt on this site |
| roof cleaning | Tier B | High | Usually searched as a problem ("black streaks on roof") rather than the service name |
| soft washing | Tier B | Medium | Industry vocabulary; homeowners search the problem more than the method. Valuable as a differentiator/explainer, weaker as a raw acquisition term |
| driveway sealing | Tier B | High | Homeowner-facing phrasing |
| seal coating / sealcoating | Tier B | High | Contractor-facing phrasing; the two are used interchangeably in the industry (confirmed via search). Site currently uses `seal-coating-*` — keep, but target "driveway sealing" language **on** those pages |
| concrete cleaning | Tier C | Medium | Most people search "driveway cleaning" or "driveway pressure washing," not "concrete cleaning" |
| window washing | Tier C | High | Alias of window cleaning — target as an on-page variant, never a separate page |
| driveway cleaning | Tier B | High | **Recommended primary phrasing over "concrete cleaning"** for consumer pages |

> **Alias groups — do not build separate pages for these, they are one intent each:**
> `pressure washing` = `power washing` · `window cleaning` = `window washing` · `seal coating` = `sealcoating` = `driveway sealing` · `concrete cleaning` ≈ `driveway cleaning`

---

## 2. City × service matrix

### 2.1 City demand ranking (UNVERIFIED ESTIMATE — based on population/household count)

| City | Est. market size | Notes |
|---|---|---|
| Dayton | Tier A (largest) | Far and away the biggest population base; also the most competitive SERP |
| Beavercreek | Tier A | Affluent, high-value homes — strong fit for premium/recurring |
| Huber Heights | Tier A | Large suburban housing stock |
| Fairborn | Tier B | |
| Troy | Tier B | Strong secondary hub for northern Miami Valley |
| Piqua | Tier B | Underserved by national competitors — genuine local opening |
| Vandalia | Tier C | |
| Englewood | Tier C | |
| Tipp City | Tier C (by size) | But it is the home base — brand/proximity signal beats raw size |

### 2.2 Existing coverage vs. gaps

Legend: ✅ page exists · **GAP** = build candidate · — = not recommended

| Service | Tipp City | Troy | Vandalia | Huber Hts | Piqua | Dayton | Englewood | Fairborn | Beavercreek |
|---|---|---|---|---|---|---|---|---|---|
| Window cleaning | ✅ | ✅ | ✅ | ✅ | **GAP (B)** | **GAP (A)** | ✅ | ✅ | ✅ |
| Pressure washing | ✅ | ✅ | ✅ | ✅ | ✅ | **GAP (A)*** | ✅ | ✅ | ✅ |
| Soft washing | ✅ | ✅ | ✅ | ✅ | **GAP (C)** | **GAP (C)** | ✅ | ✅ | ✅ |
| Roof cleaning | ✅ | **GAP (B)** | ✅ | ✅ | **GAP (C)** | **GAP (B)** | **GAP (C)** | ✅ | ✅ |
| Gutter cleaning | ✅ | **GAP (A)** | **GAP (B)** | **GAP (A)** | **GAP (C)** | **GAP (A)** | **GAP (C)** | **GAP (B)** | **GAP (A)** |
| Concrete / driveway cleaning | ✅ | **GAP (B)** | — | **GAP (B)** | — | **GAP (B)** | — | — | **GAP (B)** |
| House washing | — | — | — | — | — | ✅ | — | — | — |
| Seal coating | ✅ | ✅ | ✅ | ✅ | ✅ | **GAP (C)** | **GAP (C)** | ✅ | ✅ |
| Commercial pressure washing | — | **GAP (C)** | — | — | — | ✅ | — | — | **GAP (C)** |
| Commercial window cleaning | — | — | — | — | — | **GAP (B)** | — | — | **GAP (C)** |
| **City hub page** | ✅ | ✅ | ✅ | ✅ | **GAP (B)** | **GAP (A)** | ✅ | ✅ | ✅ |

`*` Dayton has `house-washing-dayton-ohio` and `commercial-pressure-washing-dayton-ohio` but **no general residential `pressure-washing-dayton-ohio`** — this is the single largest head-term gap on the site.

### 2.3 Which gaps deserve a dedicated page

**Build these (clear standalone intent + real demand):**
- `gutter-cleaning-{troy, huber-heights, beavercreek, dayton}-ohio` — gutter cleaning is a genuinely separate buying decision from washing, and the site currently has it in Tipp City only
- `pressure-washing-dayton-ohio` — biggest market, biggest head term, currently missing
- `dayton-ohio` and `piqua-ohio` city hubs — every other city has one; these two are orphaned even though services pages point into them
- `window-cleaning-dayton-ohio` and `window-cleaning-piqua-ohio`
- `roof-cleaning-troy-ohio` and `roof-cleaning-dayton-ohio`
- `driveway-cleaning-{troy, huber-heights, beavercreek, dayton}-ohio` (or `concrete-cleaning-*` to match existing URL pattern)
- `commercial-window-cleaning-dayton-ohio`

**Do NOT build (fold into an existing page instead):**
- `house-washing-{city}` outside Dayton — it will cannibalize the existing `pressure-washing-{city}` and `soft-washing-{city}` pages. Add a "house washing" H2 section to each existing pressure-washing city page instead
- `power-washing-{city}` — pure alias of pressure washing; add as an on-page variant and an internal alias, not a URL
- `soft-washing-{piqua, dayton}` — soft washing is a method, not a search-first term; low standalone upside. Cover it inside the Dayton/Piqua pressure-washing pages
- `seal-coating-{englewood, dayton}` — Tier C; the seven existing seal-coating pages already blanket the corridor
- `concrete-cleaning-{vandalia, englewood, piqua, fairborn}` — too thin to sustain a unique page

---

## 3. "Near me" and question keywords

### 3.1 "Near me" patterns

"Near me" queries resolve by the searcher's device location, so they are won by **Google Business Profile + proximity + a matching city page**, not by putting "near me" in a title tag. Practical guidance:

| Query pattern | How to win it |
|---|---|
| window cleaning near me | GBP categories + the city page that matches the searcher's location |
| pressure washing near me / power washing near me | Same; ensure every city page has NAP + service-area schema |
| gutter cleaning near me | **Currently unwinnable outside Tipp City** — no city pages exist. This is the strongest argument for the gutter build-out |
| house washing near me | Route to `house-washing-dayton-ohio` + city pressure-washing pages |
| roof cleaning near me / roof washing near me | Route to roof-cleaning city pages |
| driveway cleaning near me / concrete cleaning near me | Needs the driveway/concrete city pages built |
| driveway sealing near me / sealcoating near me | Existing seal-coating pages cover it |
| window washers near me | Alias — on-page variant only |
| pressure washing companies near me / pressure washing services near me | Add these exact phrasings as on-page copy on city pages |

**Do not create a `/near-me/` page.** It is a proximity signal, not a keyword to own.

### 3.2 Cost / pricing questions (highest commercial intent of all question terms)

Site already has `pressure-washing-cost-ohio` — that template works and should be replicated.

- how much does window cleaning cost — **no page exists**
- window cleaning prices per window / per pane
- how much does gutter cleaning cost — **no page exists** (national reference range found in search: roughly $75–$400, avg ~$170 — third-party figure, not a keyword volume)
- how much does it cost to pressure wash a house — partially covered
- house washing cost per square foot — third-party sources put Ohio pressure washing broadly in the $0.08–$0.40/sq ft range, with Dayton house washing quoted ~$400–$600 for a 1,500–2,000 sq ft house
- roof cleaning cost / cost to remove black streaks from roof
- driveway sealing cost Ohio — Ohio-specific third-party figure found: ~$0.18–$0.32/sq ft residential
- seal coating cost per square foot
- concrete / driveway cleaning cost
- commercial pressure washing cost per square foot
- how much to pressure wash a driveway

### 3.3 Frequency questions ("how often")

These are the natural on-ramp to a subscription offer — they end with an answer that *is* a recurring schedule.

- how often should you get your windows professionally cleaned *(answer found in search: twice a year, spring + fall — perfect Clean Club hook)*
- how often should you pressure wash your house *(answer: annually for most; every 6–8 months in wetter/humid regions — Ohio qualifies)*
- how often should you clean your gutters *(twice a year, spring + fall)*
- how often should a roof be cleaned
- how often should you seal your driveway
- how often should commercial storefront windows be cleaned

### 3.4 Comparison / "vs" questions

Site already has `soft-washing-vs-pressure-washing` — good. Missing:

- pressure washing vs power washing (difference)
- soft washing vs pressure washing for roof *(strong consensus in search results: soft washing is safer for roofs; high-pressure can void shingle warranties — usable trust content)*
- roof cleaning vs roof replacement
- professional window cleaning vs DIY
- sealcoating vs resurfacing a driveway
- house washing vs power washing

### 3.5 Problem-first / symptom queries (often outrank service terms)

Homeowners search symptoms before they search services. Site's blog already covers two of these well.

- black streaks on roof / how to remove black streaks from roof ✅ (blog exists)
- green algae on driveway ✅ (blog exists)
- green/black mildew on vinyl siding
- moss on roof shingles Ohio
- hard water spots on windows — how to remove
- clogged gutters overflowing
- salt stains on concrete driveway *(Ohio-specific winter angle — no page exists)*
- oil stains on driveway removal
- pollen on siding spring

---

## 4. Seasonal demand — Ohio exterior cleaning

Directional pattern, drawn from Ohio contractor sources found via WebSearch. **No verified search-trend data** — this is an UNVERIFIED ESTIMATE of demand timing, not measured volume.

| Window | What spikes | Content/campaign hook |
|---|---|---|
| **Late Feb – Mar** | Early planning searches, "best time to pressure wash," quote requests | Publish/refresh seasonal content ~4–6 weeks *before* the spike. Early-bird Clean Club signups |
| **Apr – May (peak ramp)** | House washing, window cleaning, driveway cleaning. Removing a winter's worth of road-salt film, grime, and north-facing green haze | Spring reset messaging; "winter salt removal" angle is distinctly Ohio |
| **Late May – Jun** | Pollen removal, pre-summer siding wash, deck cleaning before staining ✅ (blog exists) | Get ahead of humidity before light growth becomes heavy growth |
| **Jul – Aug (peak volume)** | Algae/mildew are most visible, so this is when most people call. Sources describe **late August as the single busiest stretch** for Ohio wash companies | Capacity is the constraint, not demand. Push Clean Club to smooth the curve |
| **Sep – Oct** | **Gutter cleaning surges** (leaf fall), fall window cleaning, pre-winter protective washing | The gutter-cleaning page gap is most expensive right now — this is the annual peak and the site has one gutter page |
| **Apr–Jun + Sep–Oct** | Seal coating / driveway sealing — needs dry, moderate temps; effectively a two-window season in Ohio | |
| **Nov – Feb (trough)** | Residential exterior demand collapses | **Commercial is the winter hedge**: storefronts, dumpster pads, drive-thru lanes, salt-stain removal, and interior commercial window cleaning run year-round |

**Strategic read:** the residential business has a hard Nov–Feb floor. The two structural fixes are (1) the recurring Clean Club and (2) commercial contracts — both of which are also the least-built parts of the current site.

---

## 5. Commercial & recurring-intent terms (for the "Clean Club" offer)

### 5.1 Recurring / membership / subscription terms

The subscription model is confirmed as a real and growing category in this industry — Shine, Spotless ("Home Protection Plan"), Evergreen Clean, and Squeegee Bros all run named residential recurring programs, and bundles that wrap windows with gutter + exterior wash grow fastest. **A Team currently has no page for this at all.**

- window cleaning maintenance plan
- window cleaning membership / window cleaning subscription
- exterior cleaning maintenance plan
- recurring window cleaning service
- home exterior maintenance plan
- annual home washing plan
- house washing maintenance program
- semi-annual window cleaning
- quarterly exterior cleaning service
- home maintenance subscription
- gutter cleaning maintenance plan / twice a year gutter cleaning
- exterior cleaning packages / bundle
- window cleaning + gutter cleaning package

**Note on realistic expectations:** these are almost certainly low-volume terms. Their value is **conversion and retention, not traffic** — the Clean Club page should exist to be linked from every service page and every "how often should I…" article, where the intent is already primed. Do not judge it on search volume.

### 5.2 Commercial terms

Existing: `commercial-pressure-washing-dayton-ohio` only.

- commercial pressure washing Dayton Ohio ✅
- commercial window cleaning Dayton Ohio — **GAP, Tier B**
- storefront window cleaning
- office window cleaning
- restaurant dumpster pad cleaning
- drive thru lane cleaning
- parking lot pressure washing / parking garage cleaning
- sidewalk cleaning commercial
- building exterior cleaning
- HOA pressure washing / HOA exterior cleaning *(competitors in Dayton actively target this)*
- apartment complex pressure washing
- property management exterior cleaning
- retail center pressure washing
- commercial cleaning contract Dayton
- fleet washing (only if the service is actually offered — do not publish for a service you don't run)

---

## 6. Ranked shortlist — 15 highest-opportunity targets

Ranked by (gap severity × estimated demand × commercial intent × ease of execution). **All demand signals are UNVERIFIED ESTIMATES.** Every item below is confirmed absent from `sitemap.xml`.

| # | Target keyword | Page to build | Why |
|---|---|---|---|
| 1 | pressure washing Dayton Ohio | `/pressure-washing-dayton-ohio/` | Largest market + strongest head term, and the only city where the primary service page is missing. Dayton has house-washing and commercial pages but no residential pressure-washing page |
| 2 | gutter cleaning Troy Ohio | `/gutter-cleaning-troy-ohio/` | Gutter cleaning exists in Tipp City only. Sep–Oct is the annual peak — this is the most time-sensitive gap on the site |
| 3 | gutter cleaning Beavercreek Ohio | `/gutter-cleaning-beavercreek-ohio/` | Largest affluent suburb with zero gutter coverage; high recurring-revenue fit |
| 4 | gutter cleaning Huber Heights Ohio | `/gutter-cleaning-huber-heights-ohio/` | Large suburban housing stock, no coverage |
| 5 | gutter cleaning Dayton Ohio | `/gutter-cleaning-dayton-ohio/` | Biggest population base for the second-most-underbuilt service |
| 6 | Dayton Ohio (city hub) | `/dayton-ohio/` | Every other city has a hub; Dayton — the largest — does not. Needed to consolidate authority across the three existing Dayton service pages plus the new ones |
| 7 | window cleaning Dayton Ohio | `/window-cleaning-dayton-ohio/` | Tier-A head term × Tier-A city, completely absent |
| 8 | how much does window cleaning cost | `/window-cleaning-cost-ohio/` | Mirrors the proven `pressure-washing-cost-ohio` template; top-of-funnel with real buying intent, and no page exists |
| 9 | exterior cleaning maintenance plan / window cleaning membership | `/clean-club/` | The Clean Club has no landing page. Converts existing traffic, smooths the Nov–Feb trough, raises LTV. Judge on conversion, not volume |
| 10 | Piqua Ohio (city hub) | `/piqua-ohio/` | Piqua has two service pages but no hub — orphaned. Competitors are thin here, so it is the cheapest Tier-B city to actually rank in |
| 11 | window cleaning Piqua Ohio | `/window-cleaning-piqua-ohio/` | Only city with pressure-washing + seal-coating but no window-cleaning page |
| 12 | roof cleaning Troy Ohio | `/roof-cleaning-troy-ohio/` | Troy is the largest city missing roof cleaning; can lean on the existing black-streaks blog post for internal links |
| 13 | how much does gutter cleaning cost | `/gutter-cleaning-cost-ohio/` | Second cost page; feeds every new gutter city page and the Clean Club |
| 14 | commercial window cleaning Dayton Ohio | `/commercial-window-cleaning-dayton-ohio/` | Commercial is the winter revenue hedge; the commercial pressure-washing page proves the pattern works, and window cleaning is the natural companion |
| 15 | driveway cleaning Beavercreek / Huber Heights Ohio | `/concrete-cleaning-beavercreek-ohio/`, `/concrete-cleaning-huber-heights-ohio/` | Concrete/driveway cleaning exists in Tipp City only. Use "driveway cleaning" as the on-page phrasing even if the URL keeps the `concrete-cleaning-` pattern |

### Supporting content (build alongside, not as standalone bets)

- Blog: "How often should you clean your gutters in Ohio?" → links to all new gutter pages + Clean Club
- Blog: "How often should you have your windows professionally cleaned?" → the twice-a-year answer *is* the Clean Club pitch
- Blog: "Salt stains on concrete — removing winter road salt in Ohio" → fills the Feb–Mar content gap
- Add a "House washing" H2 section to each existing `pressure-washing-{city}` page (no new URLs)
- Add "power washing" and "window washing" as on-page alias copy across existing city pages

---

## 7. Next action to make this map quantitative

This document has **no real volume or difficulty numbers** because both data providers were unavailable. To upgrade it:

1. Restore Ahrefs plan access (every endpoint, including free ones, currently returns `Insufficient plan`), **or**
2. Add Semrush API units at https://www.semrush.com/mcp-access

Then re-run `keywords-explorer-overview` / `keyword_research` against the term list in §1, §3 and §5 and replace every Tier A/B/C with a measured volume and KD. Until then, treat §2 (page-gap analysis) as the reliable part of this document — it is derived from the actual sitemap, not from estimated demand — and treat §1, §4, §5 and §6 rankings as informed judgment.
