# Lessons — read before every loop

## What predicted well
- Loop 1: the offer-ladder reframe (Clean Club had zero links, homepage sold the wrong rung)
  was scored as the top opportunity by pure (impact×confidence)/effort math, and it was —
  actual score change matched the prediction.
- Loop 2: predicted 76 → 80 for Dayton coverage, landed exactly on 80.

## What didn't
- Nothing has missed its prediction yet (2 loops in). Watch for over-confidence — recompute
  honestly next time a prediction misses, don't just declare victory by pattern-matching.

## Patterns worth reusing
- **Sitewide single-string bugs compound.** Two loops in a row found a feature (Clean Club,
  then the Dayton footer link) that was correctly built once but never propagated to every
  page's shared chrome (footer/nav). Before hunting new content gaps, grep every shared-chrome
  link target against its correct destination, sitewide, every loop.
- **Reuse committed facts, never invent new ones.** New pages should pull pricing from
  `/pressure-washing-cost-ohio/` (already published) and city facts from a quick WebSearch
  verification pass before writing — not from pattern-matching the tone of existing pages.
  Two loops of new-page content, zero fabricated numbers or unverifiable local claims so far.
- **Cross-check subagent findings against a second source before trusting them fully.**
  The keyword-hunter (no working paid API) and this repo's own audit independently converged
  on the Dayton gap — that agreement is what made it trustworthy. The competitor-scout's
  self-assessment of A Team's *own* site was wrong (undercounted pages) because it worked from
  live fetches instead of the repo — subagents researching this business from the outside will
  always be a weaker source on this site's own inventory than a direct repo crawl.

## What to stop trying
- Nothing pruned yet.
