# Backlog

Ranked ideas not yet shipped. Loop 1 shipped items 1-4 below (moved to done).
Pull the next 3 for Loop 2 by (impact × confidence) ÷ effort — recompute against
the current baseline, not these Loop-0 numbers, since Loop 1 changed the board.

## Done — Loop 1
- [x] Build `/clean-club/`
- [x] Link Clean Club from footer + mobile drawer on 59 pages
- [x] Re-point homepage title/H1/meta/hero at brand + window-cleaning entry offer
- [x] Fix `/seal-coating-piqua-ohio/` orphan (linked from `/pressure-washing-piqua-ohio/`)
- [x] Trim 2 over-160-char meta descriptions
- [x] Remove duplicate committed Netlify RUM script (58 pages) — Netlify injects its own at serve time; the committed copy was dead weight causing 2x RUM script loads on every live page

## Open — ranked

| # | Opportunity | Dim | Effort | Notes |
|---|---|---|---:|---|
| 1 | `/dayton-ohio/` city hub | SEO | 3 | Largest metro served, no hub page. Model on `/troy-ohio/`. |
| 2 | Window + soft washing pages for Piqua | SEO | 3 | Piqua only has pressure-washing + seal-coating today. |
| 3 | Gutter cleaning expansion beyond Tipp City | SEO | 4 | Currently Tipp-only; keyword agent flagged Troy/Beavercreek/Huber Heights/Dayton as the highest-opportunity gaps, largely on seasonal (Sep–Oct) demand. UNVERIFIED volume — Ahrefs/Semrush were both blocked this pass, retry next loop. |
| 4 | `/piqua-ohio/` hub | SEO | 2 | Two service pages exist for Piqua with no hub tying them together. |
| 5 | `/window-cleaning-cost-ohio/` | SEO | 3 | Mirrors the proven `pressure-washing-cost-ohio` page; no equivalent for windows exists. |
| 6 | Real photo of Anthony on homepage | Trust | — | Blocked on Anthony — asset, not code. See `needs-anthony.md`. |
| 7 | GA4 + GSC install | Measurement | — | Blocked on Anthony's account access. Every future ranking decision is guessing without this. |
| 8 | Add indexable price ranges to city × service pages | Conv + SEO | 5 | Competitor gap G1 — Stoltz (closest local rival) prints real price ranges in body copy on every page; A Team's prices live only inside the estimator. |
| 9 | Name and brand the existing guarantees | Trust | 2 | Competitor gap G7 — A Team's 12-month algae / 24-month roof-streak terms already beat every competitor observed, but they're unbranded homepage text. Give them a name and a URL. |
| 10 | Add an `/faq/` page + FAQ block on every city × service page | SEO | 3 | Competitor gap G9 — two competitors run FAQ in primary nav; A Team's FAQ content exists per-page but has no dedicated URL. |
| 11 | Re-run keyword volume research | Recon | — | Ahrefs plan-blocked, Semrush out of API units this pass. `/intel/keywords.md` has real page-gap analysis but no verified volume. Retry when units are available. |
| 12 | Dead `Anton`/`Montserrat` `@font-face` declarations | Tech | 1 | Declared in CSS, never applied by any rule. Zero download cost (unused `@font-face` isn't fetched) but confusing — low priority cleanup. |
