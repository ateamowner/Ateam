# A Team Contracting — Site Model
**Built:** 2026-09-02 · **Method:** full local crawl of `website/` (63 pages) + live fetch verification
**Verified live == repo:** yes. `https://ateamcontractings.com/` byte-matches `website/index.html` apart from Netlify's form rewrite and injected RUM script.

---

## 1. Stack fingerprint

| Thing | Finding |
|---|---|
| Hosting | Netlify. Site ID `bd6d0e0f-f62f-4f5a-9734-0d555c735381` |
| **Production deploy branch** | **`claude/business-plans-daily-reminders-vw8oz1`** — NOT `main`. Read from the live RUM tag `data-netlify-deploy-branch`. **Merging to `main` will not ship anything.** |
| CMS / builder | None. Hand-authored static HTML, one `index.html` per directory |
| Build step | None. `website/netlify.toml` → `publish = "."` |
| CSS | Single stylesheet `/css/site.css` (37.9 KB), no framework |
| JS | 3 vanilla files: `estimator.js` (14.9 KB), `lead-form.js` (6 KB), `sealcoat-calc.js` (1.8 KB). No framework, no jQuery |
| Serverless | `netlify/functions/`: `photo-note.mjs` (needs `ANTHROPIC_API_KEY`), `qr.mjs` (`/qr/*`), `canary.mjs` (`/c/*`) |
| Forms handler | Netlify Forms (`data-netlify="true"` + `bot-field` honeypot), plus a parallel POST to a Zapier Catch Hook from `lead-form.js` |
| Analytics | Netlify RUM only. **No GA4, no Meta Pixel, no Google Ads tag, no GSC verification meta found** |
| Chat widget | None |
| Canonical host | apex `ateamcontractings.com`. `_redirects` 301s all `www` and `http` to apex |

### How a change ships
Edit HTML/CSS in `website/` → commit → push to the branch Netlify has set as production
(`claude/business-plans-daily-reminders-vw8oz1`) → Netlify auto-deploys, no build.
**This is the single biggest process risk in the repo** — see `/needs-anthony.md`.

---

## 2. Page inventory (63 pages)

**Service × city coverage**

| Service | Tipp City | Troy | Vandalia | Huber Hts | Piqua | Dayton | Englewood | Fairborn | Beavercreek |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Window cleaning | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | ✅ |
| Pressure washing | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| Soft washing | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | ✅ |
| Roof cleaning | ✅ | — | ✅ | ✅ | — | — | — | ✅ | ✅ |
| Seal coating | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ |
| Gutter cleaning | ✅ | — | — | — | — | — | — | — | — |
| Concrete cleaning | ✅ | — | — | — | — | — | — | — | — |
| Exterior painting | ✅ | — | — | — | — | — | — | — | — |
| House washing | — | — | — | — | — | ✅ | — | — | — |

**City hub pages:** Tipp City, Troy, Vandalia, Huber Heights, Englewood, Fairborn, Beavercreek.
**No hub for Piqua or Dayton** — despite Dayton being the largest metro in the service area.

**Other pages:** `/`, `/about/`, `/contact/`, `/gallery/`, `/reviews/`, `/blog/` + 6 posts,
`/estimate/`, `/free-quote/` (noindex), `/pressure-washing-cost-ohio/`,
`/soft-washing-vs-pressure-washing/`, `/commercial-pressure-washing-dayton-ohio/`, 3 thank-you pages.

---

## 3. Technical health — strong

- **Zero duplicate titles. Zero duplicate meta descriptions.** All 63 pages unique.
- **Every page has exactly one `<h1>`.** No missing, no doubles.
- Schema on all 63: `HomeAndConstructionBusiness` sitewide, plus `Service` (39), `FAQPage` (47), `BreadcrumbList` (58), `Article` on posts. All parse clean.
- Sitemap has 59 entries and **zero broken/phantom URLs**; the 4 omissions are 3 thank-you pages + the noindexed `/free-quote/` — correct.
- `_headers` sets HSTS, X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy; immutable caching on `/images/`, `/fonts/`.
- Render path: 1 stylesheet, **0 render-blocking scripts**, `fetchpriority="high"` on the LCP image, `loading="lazy"` on 13 of 17 homepage images, all imagery WebP.
- Assets: images 5.4 MB total (lazy-loaded, largest single file 223 KB), fonts 148 KB, CSS 38 KB.

### Minor technical nits
- `/gallery/` — 1 image missing `alt`, 1 missing width/height. `/` — 1 image missing `alt`. `/estimate/` — 1 missing dimensions.
- 3 meta descriptions run 163–164 chars (`/`, `/pressure-washing-tipp-city-ohio/`, `/tipp-city-ohio/`) — will truncate in SERPs.
- 5 titles exceed 60 chars.
- `@font-face` declares `Anton` and `Montserrat` but **no CSS rule uses either** — dead declarations (no download cost, but misleading).

---

## 4. Conversion path — short, and already entry-offer aware

Homepage → submitted quote is **1 click, 3 fields**:
1. Land on `/`
2. Scroll to `#qq` (or tap "Or talk it through")
3. Fill **name, phone, service** (only 3 required) → submit → `/thanks/`

The photo estimator at `/estimate/` is 3 questions + optional photo, and its hidden
`services` field **already defaults to `"Window cleaning"`** — the entry rung. Good.
Both forms carry full UTM/click-id/referrer capture into Netlify Forms and Zapier.

**This path is not the bottleneck.** Friction is low. The problem is *what the path is selling* — see §5.

---

## 5. Offer-ladder alignment — the real gap

| Rung | Offer | Where it lives on the site |
|---|---|---|
| 1. Entry | **Window cleaning** | Nav link + 7 city pages. **Absent from the homepage H1, title and hero.** |
| 2. Bundle | Windows + wash | Handled well — estimator computes a bundle discount; FAQ explains it |
| 3. Recurring | **Clean Club** | Mentioned on **50 pages** — and has **no page, no URL, and zero links anywhere on the site** |

Two concrete failures:

**A. The homepage sells rung 2, not rung 1.**
`<title>Soft Washing in Tipp City, OH | Windows & Pressure Washing</title>`
`<h1>Soft Washing in Tipp City. Dirty Siding? Black Streaks? Gone By Friday.</h1>`

The most-linked page on the site (62 inbound) reads as a soft-washing city landing page.
It does not carry the brand, does not lead with the entry offer, and competes with the
real `/soft-washing-tipp-city-ohio/` page. Commit `b639bd0` shows this was a deliberate
prior choice ("leave homepage soft-wash lead intact") — made before the offer ladder was set.

**B. Clean Club is a dead end.**
It appears as a homepage section and as two `<select>` options in the quote forms. There is
**no `/clean-club/` page**, so it cannot be linked from a post, texted to a past customer,
put in an email signature, printed on a QR card, or ranked for membership/recurring searches.
The highest-value rung of the ladder has nowhere to send anyone.

---

## 6. Internal linking

Healthy hub-and-spoke: `/` (62 inbound), `/blog/`, `/gallery/`, `/pressure-washing-cost-ohio/`,
`/soft-washing-vs-pressure-washing/` all at ~61.

**Weak spots:**
- `/seal-coating-piqua-ohio/` — **true orphan, 0 inbound internal links**, yet indexable and in the sitemap.
- Every other seal-coating city page sits at **1 inbound link**.
- Englewood pages (window/soft/pressure) at 2–3 inbound.

---

## 7. Trust signals — present and real

Shown sitewide: Google **5.0 · 32 reviews**, BBB A+ badge and accreditation link, "family-owned",
"fully insured", 24-hour response, named warranties (12-month house wash re-clean, 24-month roof
on organic streaks), 3 named Google reviews with real customer names, 46-image before/after gallery,
`sameAs` links to Google, BBB, Facebook, Instagram, Nextdoor, Yelp.

`aggregateRating` in schema claims 5.0/32. **Not independently re-verified in this pass** — it must
match the live Google Business Profile or it is a structured-data risk. Listed for Anthony to confirm.

---

## 8. Voice — clean

Scanned all 63 pages against `autopilot/config/banned.txt` plus Anthony's stated dislikes.
**One hit:** "highest-leverage" in `/blog/how-to-remove-black-streaks-from-roof/`. That is the
adjectival form, which the repo's own rule explicitly permits ("leverage as a verb is banned,
the noun is not"). Still reads like consultant-speak in a homeowner post — logged as a nit.

"family-owned" appears on 23 of 63 pages. **No "one-man operation" language anywhere.** Correct.

---

## 9. Brand system — DRIFTED FROM SPEC ⚠️

The brief specifies Orange `#F58220`, Blue `#1B5B98`, Charcoal `#333333`;
Anton (display) / Montserrat (body) / Caveat (accent).

The live site uses **none of those three colors**:

| Role | Brief spec | Live site |
|---|---|---|
| Orange | `#F58220` | `#E86A12` |
| Blue | `#1B5B98` | `#002050` (navy) |
| Charcoal | `#333333` | `#111827` (ink) |
| Accent | — | `#2BB8D0` (cyan) — **not in the brief at all** |
| Display font | Anton | Archivo Black |
| Body font | Montserrat | Inter |
| Accent font | Caveat | Caveat ✅ |

This came from a deliberate multi-commit restyle (`481d4dc`, `0378786`, `9f6ea30`, `fbe0725` —
"Claystone" cream-and-navy look, "Reserve Hammer Orange for CTAs and remap accents to A-Cyan").

**Not changed in this pass.** Reverting the palette and typography is a full visual redesign,
not a fix, and the brief's "keep brand exact" guardrail cuts both ways here. Anthony has to say
which is canonical. See `/needs-anthony.md`.
