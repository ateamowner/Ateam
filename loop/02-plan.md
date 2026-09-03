# Loop 2 — Plan
**Date:** 2026-09-02 · **Score after Loop 1:** 76/100 (confirmed live)

## Sense
Re-fetched the live site after Loop 1's merge. Homepage title, Clean Club page, and the
duplicate-RUM fix are all confirmed live. Synced this branch to the production deploy
branch (it had moved 4 commits ahead with new gallery images and an IndexNow integration
committed directly — pulled those in cleanly, no conflicts).

The keyword-hunter subagent (Loop 1) independently converged on the same top gap this
audit flagged: **Dayton has no residential pressure-washing page and no city hub**, despite
being the largest metro in the service area. It has `house-washing-dayton-ohio` and
`commercial-pressure-washing-dayton-ohio` only — the single biggest head term (pressure
washing) × the single biggest city is missing.

## Rank
| Opportunity | Dim | Impact | Conf | Effort | Score |
|---|---|---:|---:|---:|---:|
| `/pressure-washing-dayton-ohio/` — biggest service × biggest city, missing | SEO + Conv | 8 | 0.85 | 2 | **3.40** |
| `/dayton-ohio/` city hub — every other city has one, Dayton's 2 pages are unlinked to each other via a hub | SEO | 6 | 0.85 | 2 | **2.55** |
| Gutter cleaning expansion (Troy/Beavercreek/Huber Heights) | SEO | 6 | 0.7 | 4 | 1.05 |
| `/window-cleaning-cost-ohio/` | SEO + Copy | 5 | 0.8 | 2.5 | 1.60 |
| Re-verify aggregateRating against live GBP | Trust | 5 | 0.5 | 1 | blocked — needs Anthony |

## Decide
Shipping **#1 and #2** this loop — they're the same theme (Dayton coverage) and compound:
the hub gives the two existing Dayton pages, plus the new one, a place to interlink from,
exactly like every other city already has.

Not shipping this loop: gutter expansion (bigger effort, better as its own loop),
window-cleaning-cost-ohio (real opportunity, backlogged), GA4/GSC and photo (blocked on Anthony).

## Build notes
- New pressure-washing page cloned from the `pressure-washing-huber-heights-ohio` template
  (closest match in structure/length) — service schema, FAQ schema, breadcrumb, full nav/footer.
- City facts verified before writing, not invented: Tipp City→Dayton is ~16 miles / ~21 min
  via I-75 (travelmath.com), and the named Dayton neighborhoods (Oregon District, South Park,
  Wright-Dunbar, Belmont) are real, verified historic districts/neighborhoods, not suburbs
  conflated with the city.
- Pricing on both new pages reuses the numbers already published and live on
  `/pressure-washing-cost-ohio/` — nothing new invented.
- Hub cloned from the `troy-ohio` pattern, interlinking all 3 Dayton pages plus cross-links
  to neighboring cities, matching the existing hub convention exactly.

## Predicted score: 76 → 80
