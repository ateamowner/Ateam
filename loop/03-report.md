# Loop 3 — Report
**Date:** 2026-09-03 · **Score: 80 → 84** (predicted 80 → 84, hit exactly)

## Shipped
1. **`/gutter-cleaning-troy-ohio/`**, **`/gutter-cleaning-beavercreek-ohio/`**,
   **`/gutter-cleaning-huber-heights-ohio/`** — gutter cleaning was Tipp-City-only going into
   this loop, and Sep–Oct is the annual peak in Ohio. Today is September 3 — this was a live
   gap, not a theoretical one. Each page: full hero, local-knowledge section built from facts
   already published on that city's own hub/service page (Troy: 6 mi via US-25A, 1807 boundary,
   real neighborhoods; Beavercreek: 1980 incorporation, I-675 corridor, patchwork subdivisions;
   Huber Heights: 20 min out, largest brick-home community in America, mortar-safe ladder
   standoffs), gallery, cost breakdown, 8-9 question FAQ, lead form, full schema.
2. **Retargeted 6 dead-end cross-links** that fell back to the Tipp City gutter page — the
   in-page "Gutter Cleaning →" cards on `troy-ohio`, `beavercreek-ohio`, `huber-heights-ohio`,
   `pressure-washing-troy-ohio`, `window-cleaning-troy-ohio`, and
   `pressure-washing-huber-heights-ohio` now point at each city's own new page. Same class of
   bug as Loop 1's Clean Club links and Loop 2's Dayton footer link — a feature that existed
   but never got wired to a real destination once one existed.
3. Added all 3 new pages to `sitemap.xml`.

## Verify
- Full-site audit across all 69 pages: **zero duplicate titles, zero duplicate metas, exactly
  one H1 per page**, valid Service + FAQPage + BreadcrumbList schema on each new page.
- Sitemap cross-checked against the file tree: only the 4 intentionally-omitted pages absent —
  unchanged from baseline, correct.
- Internal-link check: **zero broken links** (excluding the pre-existing, documented
  `/painting-services/` redirect).
- **No orphans**: each new page has real inbound links (5, 2, and 3 respectively) from the
  retargeted cross-links — unlike Loop 1's `seal-coating-piqua-ohio` bug, none of these three
  shipped with zero inbound links.
- Every local fact used (distances, incorporation dates, neighborhood names, brick-community
  claim) was pulled from that same city's own already-published, already-live page — nothing
  new researched or invented this loop. Pricing ($99+ starting, same cost-driver list) is
  identical to the live Tipp City gutter page.

## Learn
- **The "dead cross-link" pattern is now 3-for-3 across 3 loops** (Clean Club → 50 pages,
  Dayton footer → 62 pages, gutter link-cards → 6 pages). It's cheap to check and worth making
  a standing step in every loop's Sense phase: grep every city hub's link-card `href`s against
  what pages actually exist, not just what the site's authors intended.
- **Reusing a city's own already-published facts is both safer and faster than researching
  fresh ones.** Three pages built this loop with zero new WebSearch calls, because Troy,
  Beavercreek and Huber Heights all already had verified local detail on their own hub/service
  pages from earlier work. Worth checking "does this city already have a hub with real facts
  on it?" before reaching for search on the next city-expansion loop.

## Not shipped, backlogged
- `/window-cleaning-cost-ohio/` — reuses the already-published $125–$300 figure, safe to build,
  still queued for a future loop.
- `/piqua-ohio/` hub — Piqua now has zero dedicated city-cluster attention (Dayton's hub shipped
  in Loop 2); still on the backlog.
- Gutter cleaning for Vandalia, Dayton, Piqua, Englewood, Fairborn — the remaining cities without
  a dedicated gutter page. Real gap, next gutter loop.
