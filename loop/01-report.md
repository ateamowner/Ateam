# Loop 1 — Report
**Date:** 2026-09-02

## Score: 68 → 76

| Dimension | Before | After | Δ | Why |
|---|---:|---:|---:|---|
| Conversion | 19 | 25 | +6 | `/clean-club/` gives the recurring rung a real destination, linked from 59 pages. Homepage now leads with the entry offer instead of a mid-ladder service. |
| Local SEO | 15 | 17 | +2 | Homepage no longer cannibalizes `/soft-washing-tipp-city-ohio/`'s title. Orphan fixed. New indexable, schema-complete page in the sitemap. 2 real over-length meta descriptions trimmed. |
| Speed & technical | 13 | 14 | +1 | Removed a duplicated Netlify RUM script that was loading twice on every one of 58 live pages. |
| Trust | 11 | 11 | — | Untouched this loop — still gated on a real photo of Anthony, which can't be invented. |
| Copy & voice | 8 | 9 | +1 | Homepage hero now matches Anthony's voice guidance and the real offer, not a leftover pre-ladder framing. |
| Mobile | 8 | 8 | — | Not touched; no regressions (mobile drawer / dock verified intact on the new page and all edited pages). |

**Predicted 68 → 74. Actual 68 → 76.** Predicted low on Conversion (guessed +4, actual +6) —
the 59-page footer/drawer link sweep landed on more pages than planned, and correcting the
audit's own false-positive title-length flags (see `/memory/lessons.md`) meant less time
lost to non-fixes and more to real work.

## Shipped

1. **Built `/clean-club/`** — full page: hero, two plan cards, a 4-step how-it-works, an
   honest "why bother" section, FAQ with matching schema, breadcrumb, footer, mobile dock.
   Built on the site's *existing* offer terms only (10% off, two schedules, price confirmed
   on site) — no pricing or structure invented, per the guardrail.
2. **Linked Clean Club sitewide** — added to the footer Resources column and mobile nav
   drawer on 59 of 63 pages (the 3 thank-you pages and the noindexed `/free-quote/` were
   deliberately skipped). Left the tight 8-item desktop nav bar untouched to avoid a
   layout regression with no way to visually verify it in this environment.
3. **Re-pointed the homepage** at brand + entry offer: title, meta/OG/Twitter, hero badge,
   H1 and hero sub rewritten. Kept the existing driveway hero photo (real, not fabricated)
   and led the headline with window cleaning per the offer ladder, without contradicting it.
4. **Fixed the `/seal-coating-piqua-ohio/` orphan** by swapping one card in
   `/pressure-washing-piqua-ohio/`'s related-services grid — that page still keeps its
   pricing-guide link via the sitewide footer, so nothing lost coverage.
5. **Trimmed 2 real over-length meta descriptions** (163, 164 chars → both under 150).
6. **Removed a duplicated Netlify RUM script** from 58 pages — Netlify injects its own
   live regardless of what's committed; the checked-in copy (stale, empty `deploy-branch`
   attribute) was pure duplication, doubling the RUM/CWV script on every live page.
7. **Corrected 3 false-positive audit findings** rather than "fixing" things that weren't
   broken: an entity-decoding bug had over-counted 3 title lengths as violations, and 3
   flagged image alt/dimension gaps turned out to be intentional JS-driven elements
   (lightbox image, upload preview, decorative background). Documented in `/memory/lessons.md`
   so future loops don't repeat the audit mistake.

## Verified
- All 64 pages: exactly one `<title>`, one `<h1>` (utility pages excepted), balanced `<div>` tags.
- Zero duplicate titles, zero duplicate meta descriptions sitewide (checked post-edit).
- Zero real broken internal links — the only flagged href (`/painting-services/`) is a
  pre-existing, intentional 301 in `_redirects`, not a missing page.
- Zero remaining orphan pages (was 1).
- `sitemap.xml` parses as valid XML, 60 entries.
- Clean Club has 59 inbound internal links (was 0).

## Not shipped, and why
- Brand palette/font revert — guardrail, needs Anthony's call.
- Clean Club deposit + monthly restructure — guardrail, pricing change needs Anthony.
- `/dayton-ohio/` and `/piqua-ohio/` hubs — real, sized for Loop 2+, not near-zero-effort.
- GA4/GSC — blocked on account access.
- Competitor teardown ran to completion despite an interruption partway through — see below.

## Competitor teardown — `/intel/competitors.md` (15 competitors, all fetched and sourced)
The recon agent hit a session rate limit mid-task but had already written the full file
before stopping; it did finish. Top findings, ranked by expected revenue impact:
- **G1. No indexable prices on service/city pages.** Closest local rival (Stoltz, Troy)
  prints real price ranges in body copy on every page; A Team's prices live only inside
  the estimator tool.
- **G2. No real online booking.** The estimator dead-ends at "call to confirm" — Stoltz has
  a live booking calendar at the same point in the funnel.
- **G3. Review count is A Team's biggest trust gap.** 32 reviews vs. Superior Window &
  Gutter's 445+ and Window Genie's 268.
- **G4. Missing Dayton and Piqua hubs, confirmed independently** by both the site-model
  crawl and this teardown — both cities are claimed on the homepage but have no hub page,
  while direct competitors run 27–173 city pages.
- Full ranked list (G1–G15) plus what A Team is already ahead on (the photo estimator CTA,
  Clean Club, and guarantee terms all outrank anything observed) is in `/intel/competitors.md`.

## What's next (Loop 2 candidates)
1. `/dayton-ohio/` and `/piqua-ohio/` city hubs — confirmed missing by two independent passes.
2. Add indexable price ranges to city × service pages (G1) — highest-ranked competitor gap.
3. Name and brand the existing guarantees (G7) — A Team's terms already beat every
   competitor observed; they're just not sold as hard as Sonrise's "Rainy Day Guarantee."

## Blocking
Nothing blocks the loop from continuing. Six items are parked in `/needs-anthony.md`
(production branch confirmation, phone number conflict, brand palette decision, Clean
Club pricing structure, GA4/GSC access, a real photo) — the loop keeps running without them.
