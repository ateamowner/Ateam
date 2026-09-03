# Loop 3 — Plan
**Date:** 2026-09-03 · **Score after Loop 2:** 80/100 (confirmed live)

## Sense
Re-synced with the merged deploy branch — no drift since Loop 2's merge. The keyword-hunter
subagent's Loop 1 finding carries real urgency now: gutter cleaning is built for Tipp City
only, and Sep–Oct is the annual peak for it in Ohio. Today is September 3 — this gap is live
right now, not theoretical. Three city hub pages (Troy, Beavercreek, Huber Heights) already
have a "Gutter Cleaning" link-card that falls back to the Tipp City page because no dedicated
page exists — the same dead-link pattern Loop 1 found with Clean Club and Loop 2 found with
the Dayton footer link.

## Rank
| Opportunity | Dim | Impact | Conf | Effort | Score |
|---|---|---:|---:|---:|---:|
| Gutter cleaning: Troy, Beavercreek, Huber Heights (seasonal, Sep–Oct peak now) | SEO + Conv | 7 | 0.8 | 3 | **1.87** |
| Retarget the 4 hub/service-page "here" links currently falling back to Tipp City | SEO + Conv | 4 | 0.9 | 1 | **3.60** |
| `/window-cleaning-cost-ohio/` | SEO + Copy | 5 | 0.8 | 2.5 | 1.60 |
| `/piqua-ohio/` hub | SEO | 5 | 0.7 | 3 | 1.17 |

## Decide
Shipping gutter cleaning for Troy, Beavercreek and Huber Heights, plus retargeting every
in-page link that currently falls back to the Tipp City page for those three cities. Same
theme as Loops 1–2: a real gap, seasonally urgent this time, built on verified facts already
published elsewhere on the site (Troy's neighborhoods and mileage from its own hub, Beavercreek's
1980 incorporation and area tags from its own hub, Huber Heights' brick-city facts from its own
pressure-washing page) — nothing new invented.

Not shipping: `/window-cleaning-cost-ohio/` and `/piqua-ohio/` — real opportunities, backlogged
for the next loop so this one stays focused and verifiable.

## Build notes
- Pricing stays identical to the live Tipp City page: gutter cleaning starts at $99, same FAQ,
  same policy language (blower vs. hand-clearing, debris hauled away, flow test). Only the hero,
  local-knowledge section and area tags are city-specific — and every fact in them is reused
  from that city's own existing hub/service page, not invented fresh.
- Cross-links: retarget the "Gutter Cleaning" link-card on `troy-ohio`, `beavercreek-ohio`,
  `huber-heights-ohio`, and `pressure-washing-huber-heights-ohio` to the new city-specific pages.
  Nav and footer boilerplate (which points every category to its Tipp City page, the same
  convention on all 66 existing pages) is untouched — that's the established pattern, not a bug.

## Predicted score: 80 → 84
