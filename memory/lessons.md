# Lessons — read before every loop

## What predicted well
- Loop 1: the offer-ladder reframe (Clean Club had zero links, homepage sold the wrong rung)
  was scored as the top opportunity by pure (impact×confidence)/effort math, and it was —
  actual score change matched the prediction.
- Loop 2: predicted 76 → 80 for Dayton coverage, landed exactly on 80.
- Loop 3: predicted 80 → 84 for gutter cleaning expansion, landed exactly on 84.

## What didn't
- Nothing has missed its prediction yet (2 loops in). Watch for over-confidence — recompute
  honestly next time a prediction misses, don't just declare victory by pattern-matching.

## Patterns worth reusing
- **Sitewide single-string bugs compound.** Three loops in a row found a feature (Clean Club,
  the Dayton footer link, gutter-cleaning link-cards on 6 pages) that was correctly built once
  but never propagated to every page's shared chrome or cross-links. Before hunting new content
  gaps, grep every shared-chrome and in-page link target against its correct destination,
  sitewide, every loop. This has paid off 3/3 times so far — keep it as a permanent Sense step.
- **Reuse committed facts, never invent new ones — and check on-site first.** New pages should
  pull pricing from `/pressure-washing-cost-ohio/` or `/gutter-cleaning-tipp-city-ohio/`
  (already published), and city facts from that city's own existing hub/service page if one
  exists before reaching for WebSearch. Loop 3 built 3 new pages with zero new search calls by
  reusing facts Troy, Beavercreek and Huber Heights already had published elsewhere on the
  site. Three loops of new-page content, zero fabricated numbers or unverifiable local claims.
- **Check for orphans at build time, not after.** Ship new pages with real inbound links from
  day one (retarget the dead cross-link that motivated the page) rather than adding the page
  and coming back later — Loop 1's `seal-coating-piqua-ohio` shipped with zero inbound links
  and had to be fixed after the fact; Loop 3's three new pages shipped with 5/2/3 inbound links
  each because the cross-link retargeting was part of the same build step.
- **Cross-check subagent findings against a second source before trusting them fully.**
  The keyword-hunter (no working paid API) and this repo's own audit independently converged
  on the Dayton gap — that agreement is what made it trustworthy. The competitor-scout's
  self-assessment of A Team's *own* site was wrong (undercounted pages) because it worked from
  live fetches instead of the repo — subagents researching this business from the outside will
  always be a weaker source on this site's own inventory than a direct repo crawl.

## What to stop trying
- Nothing pruned yet.
