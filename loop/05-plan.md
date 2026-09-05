# Loop 5 — Plan
**Date:** 2026-09-05 · **Score after Loop 4:** 88/100 (confirmed live)

## Sense
Standing dead-cross-link check (routine every loop since Loop 3): grepped every hub's service
link-cards against the pages that actually exist.

- `piqua-ohio` — Gutter Cleaning, Soft Washing and Window Cleaning link-cards (plus header,
  mobile drawer, and footer instances) all still fall back to the Tipp City pages. Piqua has
  `pressure-washing-piqua-ohio` and `seal-coating-piqua-ohio` but nothing for the other three
  core services.
- `englewood-ohio` — Gutter Cleaning link-card falls back to Tipp City. Englewood already has
  its own pressure-washing, soft-washing and window-cleaning pages; gutter is the one gap.
- `fairborn-ohio` — same gap: Gutter Cleaning falls back to Tipp City while pressure-washing,
  soft-washing, window-cleaning and seal-coating all have dedicated Fairborn pages.

This matches the backlog exactly: "Gutter cleaning: Piqua, Englewood, Fairborn" (0.70) and
"Window/soft washing in Piqua" (0.80) are both marked Ready with real local facts already on
site — no new WebSearch needed for either.

## Rank
| Opportunity | Dim | Impact | Conf | Effort | Score |
|---|---|---:|---:|---:|---:|
| Soft washing + window cleaning in Piqua (2 pages, closes the hub's last 2 gaps) | SEO + Conv | 4 | 0.6 | 3 | **0.80** |
| Gutter cleaning: Piqua, Englewood, Fairborn (3 pages, closes the pattern sitewide) | SEO + Trust | 4 | 0.7 | 4 | **0.70** |

Both items were already scored and marked "Ready" in `memory/backlog.md` from prior loops.
No item this loop required fresh ranking — the Sense pass simply reconfirmed both gaps are
still open and still buildable from on-site facts.

## Decide
Shipping all 5 pages — both backlog items are ready, low-fabrication-risk, and together close
out every remaining dead-cross-link instance found in Sense:

- `/soft-washing-piqua-ohio/` — river-valley algae angle (Great Miami, shade canopy, Echo
  Hills), aluminum ranch belt (Covington Avenue), downtown brick/wood (Fort Piqua Plaza, High
  Street) — all reused from `pressure-washing-piqua-ohio` and `piqua-ohio`.
- `/window-cleaning-piqua-ohio/` — same hard-water/aquifer fact already published for Piqua,
  plus the same downtown-divided-light / storm-window angle used on the Troy window page,
  reframed with Piqua's own local knowledge instead of Troy's Strawberry Festival hook.
- `/gutter-cleaning-piqua-ohio/`, `/gutter-cleaning-englewood-ohio/`,
  `/gutter-cleaning-fairborn-ohio/` — identical structure, pricing ($99+) and FAQ set as every
  other gutter-cleaning city page; local-knowledge section reuses each city's own hub-page
  facts (Piqua: river/canopy; Englewood: US-40/I-70/MetroPark/Stillwater; Fairborn: the
  Fairfield–Osborn merger, base-boom growth, Bath Township).

Nothing invented: every fact below traces to a page already live on this site.

## Build notes
- All 5 pages follow the established template pattern (head/schema block, header/nav, hero,
  local-knowledge prose, svc-grid or link-grid, FAQ accordion, cta-band with quick-quote form,
  standard footer) — copied from the closest existing service-city page and re-keyed.
- Retargeting cross-links: `piqua-ohio` (3 services × ~3 link instances each), `englewood-ohio`
  (1 gutter link-card), `fairborn-ohio` (1 gutter link-card).
- Each new page gets real inbound links at build time (from its own hub + the sitewide
  service-nav pattern), not added after — per the Loop 1 orphan lesson.
- Pricing, FAQ answers and schema markup for all 5 pages match the equivalent Tipp City/Troy
  pages verbatim on numbers — no new prices invented anywhere.

## Predicted score: 88 → 91
