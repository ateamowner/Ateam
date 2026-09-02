# Competitor Intel — Window Cleaning / Pressure Washing / Soft Washing / Roof Cleaning
### Tipp City · Troy · Dayton, Ohio market
**Prepared for:** A Team Contracting (ateamcontractings.com)
**Research date:** 2026-09-02
**Method:** Live web search + direct page fetches of each competitor's site. Sitemaps pulled via `curl` where available.

> **Verification standard used in this document**
> - **Observed** = I fetched the page (or read it in a search result) and this text/element was actually present.
> - **Not verified** = I could not confirm it. It is *not* a claim that the thing is absent — only that I did not see it.
> - No review counts, prices, rankings, or revenue figures are estimated or inferred anywhere in this file. Every number below was printed on the competitor's own page.

---

## A Team Contracting — current baseline (observed, for comparison)

Fetched `ateamcontractings.com/`, `/estimate/`, and `/sitemap.xml`.

| Attribute | Observed on A Team's site |
|---|---|
| H1 | "Soft Washing in Tipp City, OH \| Windows & Pressure Washing" |
| Primary CTA | "SNAP A PIC. GET A PRICE →" |
| Services | Pressure washing, soft washing, window cleaning, roof cleaning, gutter cleaning, concrete cleaning, seal coating, exterior painting, commercial |
| Cities | Tipp City, Troy, Vandalia, Huber Heights, Fairborn, Beavercreek, Englewood, Piqua, Dayton (9) |
| Public prices | Seal coating "$2 per square foot flat" on homepage; estimator shows "windows / homes start at $99 · gutters start at $99 · roof washes start at $499" plus size-based figures (small windows $143, medium $186) |
| Instant estimator | Yes — `/estimate/`, photo-optional, returns an itemized ballpark instantly |
| Online booking | **No calendar/booking.** Estimator ends with "contact us by phone or text to confirm" |
| Membership | "Clean Club" — windows 2×/yr (10% off) or house + driveway annually (10% off) |
| Reviews shown | "Google 5.0 · 32 reviews", "BBB A+" |
| Guarantees | 12-month algae re-clean on house washes; 24-month organic-streak guarantee on roofs |
| Gallery / crew photos | Before/after pairs present; owner Anthony Leonard and crew pictured |
| Badges | BBB A+; "fully insured" text |
| Sitemap size | **59 URLs**, incl. city × service pages for 7 cities |

---

## Summary table

Legend: ✅ observed present · ❌ observed absent · — not verified · **F** = national franchise

| # | Domain | Business | Type | Services | Cities claimed | Public $ | Instant estimator | Online booking | Membership | Reviews shown on site | Guarantee | City×service pages |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | stoltzpressurewash.com | Stoltz Pressure Washing | Local (Troy) | 9 | 15 + "all areas" | ✅ ranges | ✅ | ✅ "Book Now" | ❌ | ❌ none shown | ✅ 100% satisfaction + warranty | ✅ `/service-areas/{city}/{service}/` |
| 2 | redheadpressurecleaning.com | Redhead Pressure Cleaning | Local (Springboro) | 25 | **173 city pages** | ❌ | ❌ | ❌ | ❌ | ✅ "5.0 · 55 Google Reviews" | ❌ none stated | ❌ city-only (1 page/city) |
| 3 | superiorwindowcleaning.net | Superior Window & Gutter Cleaning | Local (Dayton, since 1990) | 2 (windows, gutters) | 27 | ❌ | ❌ | — (has "Pay Online") | ❌ | ✅ **"Over 445 + 5 Star Reviews"** | ✅ 100% satisfaction | — service pages only |
| 4 | windowgenie.com/locations/ohio/dayton/ | Window Genie of Dayton | **F** (Neighborly) | 7 | 30+ | ❌ | ❌ | — | ✅ "Annual Maintenance Plans" | ✅ **268 reviews, 4.8/5** | ✅ "Neighborly Done Right Promise®" | ✅ service pages under location |
| 5 | prestigepressurewashing.com | Prestige Pressure Washing & Roof Cleaning | Local (Dayton) | 15 | 45+ | ❌ | ✅ "price estimator" link | ❌ | ❌ | ❌ testimonials only, no count | ✅ 100% Satisfaction badge | ✅ city + service pages |
| 6 | salospressurewashing.com | Salo's Pressure Washing LLC | Local (Dayton area) | 14 | 17 + "and more" | ❌ | ❌ | ❌ | ❌ | ❌ reviews page, no count on home | ❌ none stated | ✅ city + service pages |
| 7 | stealthprowash.com | Stealth Pro Wash | Local (Springboro) | 18 | 23 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ "Satisfaction Guaranteed" | ✅ city + service pages |
| 8 | cleantecsoftwash.com | Cleantec Softwash | Local (OH/IN border) | 7 | 17 (OH + IN) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ money-back satisfaction | ✅ `/dayton-oh` style city pages |
| 9 | soakcitysoftwash.com | Soak City Softwash | Local (Troy) | 8 | 16 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ none stated | ❌ service pages only (19 URLs) |
| 10 | kevsseethruwindowcleaning.com | Kev's See-Thru Window Cleaning | Local (Tipp City) | 8 | 33 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Additional verified players (lighter profiles below):** Mattox Power Washing, Paul's Power Wash, Sonrise Services LLC, Fish Window Cleaning (**F**).

---

# Per-competitor detail

## 1. Stoltz Pressure Washing — `stoltzpressurewash.com` ⚠️ closest threat
**Type:** Genuinely local — Troy, OH. Phone 937-872-3030. Not a franchise (observed: single-location site, local phone).

- **H1 (homepage):** "We make the grime disappear."
- **Primary CTA:** "Book Now"
- **H1 on a city×service page:** "House Washing in Tipp City, OH" — CTA "Get a Fast Free Quote"
- **Services observed:** soft house wash, pressure washing, roof & soft wash, concrete cleaning, gutter cleaning, deck restoration, fence cleaning, window washing, fleet washing.
- **Cities observed:** Troy, Tipp City, Dayton, Piqua, Vandalia, Sidney, Huber Heights, Englewood, Clayton, Brookville, Covington, West Milton, Pleasant Hill, Casstown, Bradford (+ "All areas" link).
- **City × service landing pages: YES.** URL pattern `/service-areas/{city}/{service}/` — e.g. `/service-areas/tipp-city/house-washing/`. Six services cross-linked from each city page (soft house wash, pressure washing, roof & soft wash, concrete cleaning, gutter cleaning, deck restoration).
- **Public pricing: YES, in page copy** (this is the notable part — it is indexable text, not hidden behind a tool):
  - Soft house wash $400–$800; large homes up to ~$1,250
  - Driveway / concrete cleaning $100–$350
  - Roof & soft wash $500–$800
- **Offer structure:** free on-site or photo quotes; online booking; instant estimate tool; photo upload. No membership, no bundle discount observed.
- **Trust:** "100% Satisfaction" guarantee, warrantied service, "100% removal of moss, mold, mildew & algae" on soft washing; "EPA-safe detergents"; gallery with before/after pairs.
- **Not verified / observed absent:** no review count or star rating anywhere on the pages fetched; no crew or owner photos; no insurance badge images; no financing.
- **Note on a second domain:** `stoltzpressurewashing.com` also resolves and carries the Stoltz name (H1 "PRESSURE WASHING SERVICES", CTA "GET A FAST QUOTE", only 3 reviews shown, service areas "Miami Valley / Tipp City / Troy / Dayton"). Whether these are the same legal entity, a rebuild, or unrelated is **not verified**. The `.../pressurewash.com` build is clearly the more advanced one.
- **Page structure note:** neither Stoltz domain serves an XML sitemap at `/sitemap.xml` (returned zero `<loc>` entries).

**Why this matters:** Stoltz is the only competitor found that beats A Team on *two* fronts at once — city × service coverage AND public prices sitting in crawlable body copy — and it is based in Troy, 6 miles from Tipp City.

---

## 2. Redhead Pressure Cleaning — `redheadpressurecleaning.com` ⚠️ SEO footprint threat
**Type:** Genuinely local — based Springboro, OH (Township of Franklin, Warren County). Not a franchise (observed).

- **H1 (Troy city page):** "Pressure Washing in Troy, OH"
- **Primary CTA:** "Get My Free Quote"
- **Sitemap: 221 URLs. 173 of them are `/service-areas/{city}-oh` pages** — a very large flat city footprint including troy-oh, tipp-city-oh, piqua-oh, sidney-oh, vandalia-oh, dayton-oh, beavercreek-oh, plus Cincinnati-metro towns.
- **25 dedicated service pages** at `/services/{service}`: pressure washing, house washing, soft washing, roof washing, driveway, concrete, patio, deck, fence, sidewalk, walkway, gutter cleaning, **gutter brightening**, paver cleaning, **paver sealing**, commercial pressure washing, storefront, parking lot, **dumpster pad**, graffiti removal, rust stain removal, oil stain removal, brick & stone, vinyl siding, pool deck, exterior building washing.
- **Offer structure:** free estimates by form or phone. No prices, no instant estimator, no online booking, no membership, no bundle discount observed.
- **Trust:** "5.0 · 55 Google Reviews" displayed on page; "Licensed & insured" as text; gallery + reviews page in nav.
- **Not verified:** owner/crew photos; guarantee language (none stated on the page fetched); badge images.
- **Structure note:** each city gets exactly *one* page — it is city-only, not city × service. Wide but shallow. A Team's city × service structure is architecturally better; Redhead simply has ~19× more city pages.

---

## 3. Superior Window & Gutter Cleaning — `superiorwindowcleaning.net` ⚠️ review-count threat
**Type:** Genuinely local — Dayton, "serving Dayton Ohio since 1990" (per search result). Not a franchise (observed).

- **H1:** "PROFESSIONAL WINDOW AND GUTTER CLEANING SERVICES IN DAYTON, OH"
- **Primary CTA:** "GET A QUOTE"
- **Services:** window cleaning (interior + exterior) and gutter cleaning only — deliberately narrow.
- **Cities observed (27):** Beavercreek, Bellbrook, Brookville, Centerville, Clayton, Dayton, Englewood, Fairborn, Huber Heights, Kettering, Lewisburg, Miamisburg, Moraine, Oakwood, Riverside, Springboro, Sugarcreek, **Troy, Tipp City**, Union, Vandalia, Washington Twp, Waynesville, West Carrollton, West Milton, Yellow Springs, Xenia.
- **Trust — the standout:** **"Over 445 + 5 Star Reviews"** aggregated across Google, Facebook and BBB, stated on the homepage. Also: "100% satisfaction guarantee", "GUARANTEED RESULTS", **bonded and insured**, **Ohio Bureau of Workers' Compensation badge**, BBB seal.
- **Notable nav item: "Pay Online"** — customer self-serve payment, plus a **"Careers"** page.
- **Offer structure:** no public prices, no estimator, no membership, no bundle discount observed.
- **Not verified:** owner/crew photos (none visible); whether individual city landing pages exist (nav shows service dropdowns, not city pages).

**Why this matters:** they are the review-volume leader in Dayton-area window cleaning by an order of magnitude over A Team's 32, and they cover Troy and Tipp City.

---

## 4. Window Genie of Dayton — `windowgenie.com/locations/ohio/dayton/` 🏢 NATIONAL FRANCHISE
**Type:** **National franchise** — Window Genie is a Neighborly brand (observed: "Neighborly Done Right Promise®" on page, corporate `/locations/{state}/{city}/` URL structure).

- **H1:** "Window Cleaning Services in Dayton, Ohio"
- **Primary CTA:** "Request a Quote"
- **Services:** interior & exterior window cleaning, **solar panel cleaning**, pressure washing (house/deck/fence/concrete), **concrete sealing**, **holiday lighting (seasonal & permanent)**, gutter cleaning, **window tinting (solar control, security, decorative, film removal)**.
- **Cities:** Dayton primary + 30+ surrounding, skewing south/southwest (Cincinnati, Hamilton, Fairfield, Lebanon, Middletown, Oxford, Springboro, Miamisburg, Waynesville, Monroe, Trenton…). **Notably does not list Tipp City, Troy or Piqua** in the observed list — the north Miami Valley is comparatively open.
- **Trust:** **268 customer reviews, 4.8/5 star rating displayed**; "Neighborly Done Right Promise®"; background checks + insurance noted; professional team photos and before/after images.
- **Offer structure:** free estimates, no public prices, **Annual Maintenance Plans** mentioned, online quote request form (no instant price, no self-serve calendar observed).
- **Structure:** multiple service-specific landing pages nested under the location; national domain authority behind every one.

---

## 5. Prestige Pressure Washing & Roof Cleaning — `prestigepressurewashing.com`
**Type:** Genuinely local — Dayton. Not a franchise (observed).

- **H1:** "Dayton's Longest Established & Most Experienced Pressure Washing & Roof Cleaning Company"
- **Primary CTA:** "CALL US NOW"
- **Services (15):** roof cleaning, **dome/bubble cleaning**, house washing, fence, concrete, gutter, deck, commercial roof cleaning, **paver cleaning & sealing**, **stone cleaning & restoration**, **holiday lighting**, **cooling tower cleaning**, commercial pressure washing, **parking garage cleaning**, misc.
- **Cities: 45+ named**, incl. Tipp City, Troy, Vandalia, Huber Heights, Englewood, Covington, West Milton, Union, Sidney — and out to Cincinnati, Columbus, Springfield, Richmond IN.
- **Offer structure:** "Save 10% or more" promoted (mechanism not specified on the page); a price estimator is linked; no public prices; no membership observed.
- **Trust — the deepest badge stack found:** **Veteran Owned Business**, Fully Insured, **Ohio Bureau of Workers Compensation**, **Power Washers of North America (PWNA) membership**, BBB A+, Angi A rating, 100% Satisfaction Guarantee badge. Extensive categorized before/after gallery.
- **Not verified:** aggregate star rating or review count (individual testimonials only, no count); crew photos (owner "Shawn" named in testimonials only).
- **Structure note:** has a **"Store"** nav item — some form of e-commerce/product page (contents not verified).

---

## 6. Salo's Pressure Washing LLC — `salospressurewashing.com`
**Type:** Genuinely local — south Dayton metro. Not a franchise (observed).

- **H1:** "YOUR TOP-RATED DAYTON PRESSURE WASHING COMPANY"
- **Primary CTA:** "Get A Free Estimate" (repeated throughout)
- **Services (14):** house washing, driveway washing, roof cleaning, concrete, **paver cleaning & sealing**, **rust stain removal**, deck & fence, fence washing, gutter, window cleaning, commercial pressure washing, exterior building washing, commercial concrete, **dumpster pad cleaning & sanitation**.
- **Cities (17):** Centerville, Oakwood, Bellbrook, Springboro, Beavercreek, Miamisburg, West Chester, Kettering, Mason, Lebanon, Xenia, Waynesville, Spring Valley, Huber Heights, Vandalia, Englewood, **Tipp City** + "and more". Skews south — Troy and Piqua not listed.
- **Offer structure:** free estimate form only. No prices, no estimator, no booking, no membership, no bundles observed.
- **Trust:** BBB Business Review badge; project gallery; a dedicated **"Reviews"** nav page and a **"Tips"** (blog) section.
- **Not verified / observed absent:** no star rating or review count on the homepage; no guarantee language; no crew photos.
- **Structure:** individual city and service landing pages confirmed.

---

## 7. Stealth Pro Wash — `stealthprowash.com` (also `stealthsoftwash.com`)
**Type:** Genuinely local — Springboro / Dayton. Not a franchise (observed).

- **H1:** "Welcome To Stealth Pro Wash"  *(weak, non-keyword H1 — a genuine on-page mistake)*
- **Primary CTA:** "Request A Quote"
- **Services (18):** soft washing, pressure washing, roof cleaning, exterior house, deck, **solar panel cleaning**, **brick cleaning**, window cleaning, siding, driveway, walkway, fence, gutter, commercial roof, **HOA cleaning**, commercial solar panel, **apartment complex cleaning**, building cleaning.
- **Cities (23):** Dayton, Springboro, Beavercreek, Bellbrook, Centerville, Kettering, Lebanon, Miamisburg, Waynesville, West Carrollton, West Chester, Franklin, Middletown, Washington Twp, Mason, Spring Valley, Moraine, Germantown, Farmersville, Xenia, Wilmington, **Fairborn**, Yellow Springs. Entirely south of Dayton — **Tipp City, Troy and Piqua are absent**.
- **Trust:** **SoftWash Systems Certified** badge (a recognized industry certification), "Good Stewards" and business seals, "Satisfaction Guaranteed".
- **Not verified / observed absent:** no prices, no estimator, no booking, no membership, no bundle discount, no review count or rating, **no before/after gallery**, no crew photos.
- **Structure notes:** nav includes **"Why Softwash"** (an educational/category-defining page), **"FAQs"**, **"Specials"**, separate **Residential** and **Commercial** trees, and a blog.

---

## 8. Cleantec Softwash — `cleantecsoftwash.com`
**Type:** Genuinely local — operates the Ohio/Indiana border corridor. Not a franchise (observed).

- **H1 (Dayton city page):** "Softwashing & Pressure Washing Services in Dayton, OH"
- **Primary CTA:** "Request an Estimate"
- **Services (7):** house softwashing, concrete cleaning, pressure washing, roof softwashing, window cleaning, gutter cleaning, commercial exterior cleaning.
- **Cities (17, OH + IN):** Dayton, Eaton, Greenville, Arcanum, Brookville, Vandalia, Clayton/Englewood, **Piqua, Troy**, Middletown, Oxford, Hamilton, Kettering OH; Union City, Centerville, Connersville, Richmond IN.
- **City landing pages:** yes — flat `/{city}-oh` pattern (e.g. `/dayton-oh`).
- **Trust:** **money-back satisfaction guarantee**; BBB logo; "Christian Blue Certified Business" badge; a city-scoped gallery titled "Our Recent Dayton Softwashing Gallery" (nice touch — gallery localized to the city page).
- **Not verified / observed absent:** no prices, no estimator/booking, no membership, no bundles, no review count or rating, no crew photos.

---

## 9. Soak City Softwash — `soakcitysoftwash.com`
**Type:** Genuinely local, family-run — **1453 Michael Dr, Troy, OH**, 937-552-5577. Not a franchise (observed).

- **H1:** "Pressure Washing Experts in Troy, Ohio"
- **Primary CTA:** "Get a Quote"
- **Services (8):** house soft wash, roof cleaning, driveway & sidewalk pressure washing, fence, **gutter cleaning & brightening**, deck & patio, window cleaning, concrete.
- **Cities (16):** Troy, Conover, Covington, Dayton, Englewood, Fletcher, **Tipp City**, Vandalia, Huber Heights, Laura, Ludlow Falls, **Piqua**, Pleasant Hill, Sidney, Union, West Milton — i.e. exactly A Team's northern territory.
- **Trust:** **licensed and insured badge**, a "Pressure Washers - Near Me" badge, physical street address published, before/after gallery with 5+ project examples.
- **Not verified / observed absent:** no prices, no estimator, no booking, no membership, no bundles, no review count/rating on homepage, no guarantee stated, no crew photos.
- **Structure:** only **19 URLs in sitemap** — service pages only, no city × service matrix. Smallest footprint of the group; direct geographic overlap but weak site.

---

## 10. Kev's See-Thru Window Cleaning — `kevsseethruwindowcleaning.com`
**Type:** Genuinely local — **based in Tipp City, OH**. Owner Kevin Foley Jr. Not a franchise (observed).

- **H1:** "Commercial & Residential Window Cleaning Services"  *(no city in the H1)*
- **Primary CTA:** "Submit Question" (quote form button)
- **Services (8):** window cleaning, gutter cleaning, power washing, light fixture detailing, ceiling fan detailing, post-construction cleaning, **lawn service & maintenance**, **snow removal**.
- **Cities (33):** Huber Heights, Englewood, Greenville, Dayton, **Troy, Tipp City**, Riverside, Fairborn, Beavercreek, Xenia, Wilmington, Cincinnati, Lima, St. Mary's, Celina, Bellefontaine, London, Miamisburg, Springboro, Middletown, Springfield, Bellbrook, Sugarcreek, Trotwood, Brookville, Oxford, Eaton, **Piqua**, Sidney, Wapakoneta, New Carlisle, Vandalia, Urbana.
- **Trust:** one photo of the owner (Kevin Foley Jr.); references external reviews.
- **Not verified / observed absent:** no prices, no estimator, no booking, no membership, no bundles, no review count/rating, no guarantee, minimal gallery (one image), no insurance badge, **no city or service landing pages**.
- **Assessment:** in A Team's home town, but the weakest web presence in this set. Low SEO threat, real word-of-mouth threat.

---

## Additional verified players (lighter profiles)

### Mattox Power Washing — `mattoxpowerwashing.com` (local)
- **H1:** "Leading Power Washing Service Center" · **CTA:** "Get A Free Estimate" · Joe@mattoxpowerwashing.com, 937-247-6112
- 26+ cities incl. **Tipp City, Troy**, Huber Heights, Vandalia, Englewood, Dayton, out to Cincinnati.
- 10 services including **Permanent Outdoor Lighting** and **Christmas Light Hanging** — the clearest example of an off-season revenue line.
- Before/after gallery ✅, **team member photos ✅**. No prices, no estimator, no booking, no membership, no review count, no guarantee, no insurance badges observed.

### Paul's Power Wash — `paulspower-wash.com` (local; area code 614 = Columbus-based, serving Dayton)
- **H1 (city page):** "Pressure Washing in Huber Heights, OH" · **CTA:** "Request Free Quote"
- **URL pattern `/{city-name}/` with 45 city pages listed in the footer** — including Huber Heights and Beavercreek.
- 6 services incl. **equipment washing**. Before/after gallery (3 pairs), 3 testimonials, "Fully insured / Licensed and insured" as text. **FAQ page in nav.**
- No prices, no estimator, no booking, no membership, no star rating/review count, no crew photos observed.

### Sonrise Services LLC — `soncleaned.com` (local, south Dayton metro)
- **H1:** "Professional Window Cleaning, Gutter Cleaning & Power Washing" · **CTA:** "Call for a free estimate: 937.436.4499" (phone-only CTA)
- Cities: Bellbrook, Beavercreek, Centerville, Kettering, Oakwood, Springboro, greater Dayton, N. Cincinnati.
- Distinctive: a named **"Rainy Day Guarantee"** with its own nav item and dedicated page — a memorable, ownable guarantee. Also **"Sonrise Team" crew photo**, a **Reviews** page, a **Jobs** page, and a **Carpet Cleaning** cross-sell.
- No prices, no estimator, no booking, no membership, no review count/rating observed.

### Fish Window Cleaning — Dayton East 🏢 NATIONAL FRANCHISE
- **Franchise status observed** in search results: described as the world's largest window cleaning franchise; corporate URL `fishwindowcleaning.com/Dayton-OH-3092/`; national number (855) 601-3474.
- Territory observed in the page title: **Dayton, Beavercreek, Fairborn, Kettering, Xenia** — again, no Tipp City / Troy / Piqua.
- Positioning observed in snippet: uniformed, extensively trained technicians; free on-site estimate.
- **Everything else is "not verified"** — the site returned HTTP 404 to my fetches (likely bot blocking), so I did not confirm H1, CTA, pricing, reviews or guarantees firsthand.
- A Yelp listing for a Fish Window Cleaning at 74 N Orange St, Xenia OH is marked **CLOSED** (updated Dec 2025). Whether the Dayton East territory is still operating is **not verified**.

### Excluded after checking
- **Whiteline Window Washing (`whitelinewindowwashing.com`)** appeared in Dayton search results, but the live site's service areas are **Encinitas, Carlsbad, La Jolla, Rancho Santa Fe, Del Mar, Chula Vista, San Diego** — it is a San Diego company, not a Dayton competitor. Excluded. *(Worth noting only because its offer design is strong: monthly / quarterly / bi-annual recurring tiers with up to 25% savings, a 90-day guarantee, and a **$100 cash referral reward + $50 discount** program.)*
- **Castle Power Wash** (`castlepowerwash.com`) and **Advanced Window Cleaning Services** (`advancedwindowcleaningservices.com`) both returned HTTP 503 on fetch. Their existence in the market is observed via search results; **no site details verified**.
- **Colin's Crystal Clean** (`colinscrystalclean.com`, Troy, 937-524-4320) returned empty content on fetch. **Not verified.**

---

## Market observations (inferred, flagged as such)

1. **Inferred:** the market splits geographically. Stealth Pro Wash, Salo's, Window Genie, Fish and Sonrise are all concentrated **south of Dayton** (Centerville / Springboro / Kettering / Cincinnati corridor) and do not list Tipp City, Troy or Piqua. The companies that *do* directly overlap A Team's home turf are **Stoltz, Soak City, Kev's See-Thru, Superior, Cleantec, Redhead, Prestige and Mattox**.
2. **Observed:** only **two** of the twelve sites checked put actual prices in body copy — Stoltz (ranges) and A Team (starting-at figures inside the estimator). Public pricing is still a genuine differentiator in this market.
3. **Observed:** only Stoltz offers self-serve online **booking**. Everyone else is form-or-phone.
4. **Observed:** only Window Genie (franchise) and A Team offer a **recurring/maintenance plan**. This is A Team's strongest structural advantage over local rivals.
5. **Observed:** review counts displayed on-site range from 3 (Stoltz's second domain) to **445+** (Superior). A Team's 32 is on the low end of those who publish a number at all.

---

# GAP LIST
### Things competitors have that ateamcontractings.com does not

Ordered by expected revenue impact. Every gap cites the competitor(s) where I actually observed the thing.

### Tier 1 — highest impact

**G1. Indexable price ranges in body copy on every service and city page.**
*Who has it:* Stoltz prints "$400–$800", "up to ~$1,250", "$100–$350", "$500–$800" directly in the text of `/service-areas/tipp-city/house-washing/`.
*A Team's state:* prices exist only as "starting at $99 / $499" and inside the `/estimate/` tool. The 40+ city × service pages carry no numbers.
*Action:* add a "What house washing costs in {City}" price-range block to all 40+ city × service pages, wired to the same numbers the estimator returns, plus `Product`/`Offer` schema. This captures "how much does X cost" queries that currently route to Stoltz.

**G2. Real online booking — a calendar, not a callback.**
*Who has it:* Stoltz ("Book Now" + online booking + instant estimate + photo upload).
*A Team's state:* the estimator produces a price, then dead-ends at "call or text us to confirm." That is a conversion leak at the exact moment intent is highest.
*Action:* attach a self-serve date/time picker to the end of the `/estimate/` flow with a deposit or card-on-file hold. A Team already has the harder half built.

**G3. Review volume, and review counts repeated on every page.**
*Who has it:* Superior Window & Gutter Cleaning — "Over 445 + 5 Star Reviews" on the homepage. Window Genie — 268 reviews, 4.8/5. Redhead — "5.0 · 55 Google Reviews" printed on its city pages.
*A Team's state:* "Google 5.0 · 32 reviews" on the homepage only.
*Action:* (a) a systematic post-job review-request routine — closing the 32 → 100+ gap is the single biggest trust lever available; (b) stamp the live count/rating into the header or hero of every city × service page, not just the homepage, the way Redhead does.

**G4. City coverage depth — and specifically the missing Dayton and Piqua hubs.**
*Who has it:* Redhead 173 city pages; Paul's Power Wash 45; Prestige 45+; Kev's 33; Mattox 26; Superior 27.
*A Team's state:* 59 total URLs, 7 city hubs (`/tipp-city-ohio/`, `/troy-ohio/`, `/vandalia-ohio/`, `/huber-heights-ohio/`, `/fairborn-ohio/`, `/beavercreek-ohio/`, `/englewood-ohio/`). **There is no `/dayton-ohio/` and no `/piqua-ohio/` hub page**, even though both cities are claimed on the homepage.
*Action:* build the two missing hubs first, then extend to the towns competitors are already farming and A Team is not: Piqua, Sidney, Covington, West Milton, Pleasant Hill, Union, Clayton, New Carlisle, Brookville, Springfield, Xenia, Kettering, Centerville, Miamisburg.

**G5. Holes in the existing city × service matrix.**
*A Team's state (from sitemap):* roof cleaning pages exist for only 4 cities (Huber Heights, Fairborn, Beavercreek, Vandalia) — **no roof-cleaning page for Troy, Piqua, Englewood or Dayton**. Gutter cleaning and concrete cleaning exist for **Tipp City only**. Window cleaning is missing for Piqua and Dayton.
*Who has it:* Stoltz runs a full 6-service × 15-city grid; Redhead runs 25 service pages.
*Action:* complete the grid. Roof cleaning is the highest-ticket service ($499+ per the estimator) and is missing from the two largest markets in the service area.

### Tier 2 — meaningful, low effort

**G6. Third-party industry certifications and authority badges.**
*Who has it:* Prestige — Veteran Owned, **Ohio Bureau of Workers Compensation**, **PWNA (Power Washers of North America) membership**, BBB A+, Angi A. Stealth — **SoftWash Systems Certified**. Superior — **bonded**, Ohio BWC badge, BBB. Soak City — licensed & insured badge.
*A Team's state:* BBB A+ and "fully insured" text only.
*Action:* join and display PWNA and/or SoftWash Systems certification; add an Ohio BWC badge; state "bonded" if applicable. These are cheap credibility that three separate competitors are using.

**G7. A named, memorable guarantee — and guarantees repeated per page.**
*Who has it:* Sonrise's **"Rainy Day Guarantee"** has its own nav item and page. Window Genie has the trademarked "Neighborly Done Right Promise®". Cleantec offers a **money-back** guarantee. Stoltz promises "100% removal of moss, mold, mildew & algae".
*A Team's state:* the 12-month algae and 24-month roof guarantees are genuinely stronger than most of these — but they are unnamed, unbranded, and live only in homepage body text.
*Action:* name them (e.g. "The 12-Month Clean Wall Promise"), give them a dedicated URL, and repeat the badge on every service and city page. A Team is currently under-selling its best differentiator.

**G8. "Pay Online" / self-serve customer payment.**
*Who has it:* Superior Window & Gutter Cleaning, as a top-level nav item.
*A Team's state:* not present in the 59-URL sitemap.
*Action:* add a `/pay/` page. Removes friction on collections and reads as an established operation.

**G9. An FAQ page.**
*Who has it:* Stealth Pro Wash and Paul's Power Wash both carry FAQ in primary nav; Superior has `/FAQs`.
*A Team's state:* no FAQ URL in the sitemap.
*Action:* one `/faq/` page with `FAQPage` schema, plus a 4–6 question FAQ block appended to each city × service page — the cheapest available win for AI-answer and featured-snippet visibility.

**G10. Commercial depth beyond a single page.**
*Who has it:* Redhead — storefront, parking lot, dumpster pad, graffiti removal, exterior building washing as separate pages. Salo's — commercial concrete, dumpster pad cleaning & sanitation, exterior building. Stealth — **HOA cleaning, apartment complex cleaning**, commercial roof, commercial solar. Prestige — cooling tower, parking garage, commercial roof.
*A Team's state:* one page, `/commercial-pressure-washing-dayton-ohio/`.
*Action:* split into HOA / property management, apartment complex, storefront, restaurant & dumpster pad. Commercial contracts are recurring by nature and directly feed the Clean Club model A Team already runs.

**G11. An educational "Why soft washing" category page.**
*Who has it:* Stealth Pro Wash carries "Why Softwash" in primary nav.
*A Team's state:* has `/soft-washing-vs-pressure-washing/`, which is close — but it is not in the primary nav and is not framed as the category-defining page.
*Action:* promote it into main nav. Owning the category explanation is how you win the AI-answer citation for "what is soft washing".

### Tier 3 — revenue-line and program gaps

**G12. Off-season revenue services A Team does not offer.**
Observed on competitors' sites, absent from A Team's:
- **Holiday / Christmas lighting** — Mattox, Prestige, Window Genie
- **Permanent outdoor lighting** — Mattox
- **Window tinting** (solar control, security, decorative, film removal) — Window Genie
- **Solar panel cleaning** — Stealth, Window Genie
- **Deck restoration / staining** — Stoltz
- **Paver cleaning & sealing** — Salo's, Redhead, Prestige
- **Gutter brightening** (sold separately from gutter cleaning) — Redhead, Soak City
- **Rust / oil stain removal** as a named service — Salo's, Redhead, Mattox
- **Fleet & equipment washing** — Stoltz, Redhead, Paul's
- **Snow removal / lawn** — Kev's See-Thru
*Action:* holiday lighting and gutter brightening are the two lowest-lift additions — one fills the Nov–Jan hole in a business whose season ends in October, the other is a pure add-on upsell on a job the crew is already on site for.

**G13. A dollar-denominated referral program.**
*Who has it:* observed only outside this market (Whiteline, San Diego: $100 cash to the referrer, $50 off to the referred, plus a waived travel fee for neighbors). **No Dayton-area competitor in this set was observed running one.**
*Action:* this is an open lane, not a catch-up item. A "$50 to you, $50 to your neighbor" offer, pitched on the day of service in a neighborhood A Team is already working, compounds with route density.

**G14. A careers / hiring page.**
*Who has it:* Superior ("Careers"), Sonrise ("Jobs").
*A Team's state:* not in the sitemap.
*Action:* a `/careers/` page. Signals scale to customers and is the cheapest recruiting channel when crew capacity becomes the constraint on growth.

**G15. Blog depth.**
*Who has it:* Redhead (221-URL site with a blog), Salo's ("Tips"), Stealth, Prestige, Soak City, Cleantec, Paul's — all run blogs.
*A Team's state:* 4 posts.
*Action:* the existing posts are well-chosen (black roof streaks, driveway algae, best time to wash, deck prep). Keep cadence and localize: "{City} hard water spots", "Why Miami Valley roofs streak", tying each post back to the matching city × service page.

### Where A Team is already ahead — do not trade these away

- **Instant photo-based estimator with real numbers.** Only Stoltz and Prestige have anything comparable, and A Team's "SNAP A PIC. GET A PRICE →" CTA is the sharpest, most differentiated CTA observed in the entire set. Every competitor's CTA is a generic "Get a Quote" / "Request an Estimate" / "Call Us Now".
- **Clean Club recurring membership.** Only Window Genie (a national franchise) offers anything similar locally.
- **Guarantee terms.** 12-month algae and 24-month roof-streak guarantees are longer and more specific than any competitor guarantee observed — most are just "100% satisfaction."
- **Owner and crew visibility.** A Team names and shows Anthony Leonard and the crew. Only Mattox, Sonrise and Kev's do anything comparable; the majority show no faces at all.
- **City × service URL architecture.** Structurally better than Redhead's 173 flat city pages. A Team's problem is coverage, not design.

---

## Sources

- [A-Team Contracting](https://ateamcontractings.com/) · [estimator](https://ateamcontractings.com/estimate/)
- [Stoltz Pressure Washing](https://www.stoltzpressurewash.com/) · [Tipp City house washing page](https://www.stoltzpressurewash.com/service-areas/tipp-city/house-washing/) · [stoltzpressurewashing.com](https://stoltzpressurewashing.com/)
- [Redhead Pressure Cleaning — Troy](https://redheadpressurecleaning.com/service-areas/troy-oh)
- [Superior Window And Gutter Cleaning](https://www.superiorwindowcleaning.net/)
- [Window Genie — Dayton, OH](https://www.windowgenie.com/locations/ohio/dayton/)
- [Prestige Pressure Washing](https://prestigepressurewashing.com/)
- [Salo's Pressure Washing LLC](https://www.salospressurewashing.com/)
- [Stealth Pro Wash](https://stealthprowash.com/)
- [Cleantec Softwash — Dayton](https://www.cleantecsoftwash.com/dayton-oh)
- [Soak City Softwash](https://www.soakcitysoftwash.com/)
- [Kev's See-Thru Window Cleaning](https://kevsseethruwindowcleaning.com/)
- [Mattox Power Washing](https://mattoxpowerwashing.com/)
- [Paul's Power Wash — Huber Heights](https://www.paulspower-wash.com/huber-heights/)
- [Sonrise Services LLC](https://www.soncleaned.com/)
- [Fish Window Cleaning — Dayton East](https://www.fishwindowcleaning.com/Dayton-OH-3092/) *(fetch blocked; search-result data only)*
- [Whiteline Window Washing](https://www.whitelinewindowwashing.com/) *(San Diego — excluded from market set)*
