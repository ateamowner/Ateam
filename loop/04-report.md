# Loop 4 — Report
**Date:** 2026-09-03 · **Score: 84 → 88** (predicted 84 → 88, hit exactly)

## Shipped
1. **`/piqua-ohio/`** — the last served city without a hub page. Piqua had two service pages
   (`pressure-washing-piqua-ohio`, `seal-coating-piqua-ohio`) but no page linking them together,
   unlike every other city A Team serves. Built on the same pattern as the Troy/Beavercreek/
   Dayton hubs, with local facts reused from `pressure-washing-piqua-ohio` (Fort Piqua Plaza,
   High Street, Echo Hills, Covington Avenue, 15 min via I-75) — nothing new researched.
2. **`/gutter-cleaning-dayton-ohio/`** and **`/gutter-cleaning-vandalia-ohio/`** — two more
   cities whose hubs had a "Gutter Cleaning" link falling back to Tipp City. Local facts reused
   from Loop 2's Dayton pages and the existing `vandalia-ohio` hub (Butler Township, South Brown
   School Road, airport area) — zero new WebSearch calls.
3. **Retargeted 5 dead-end cross-links**: `dayton-ohio`, `vandalia-ohio`,
   `pressure-washing-dayton-ohio`, `pressure-washing-vandalia-ohio`, and
   `window-cleaning-vandalia-ohio` all now point at their own city's gutter page.
4. Added all 3 new pages to `sitemap.xml`.

## Not shipped, and why
- **`/window-cleaning-cost-ohio/`** — reconsidered mid-loop. The only real published number for
  window cleaning is one line ("$125–$300 per home") on `/pressure-washing-cost-ohio/`. A page
  structured like that pricing guide — with per-size tables, per-window math — would mean
  inventing pricing structure that doesn't exist, which is close enough to the "never change
  pricing without asking" guardrail that I backed off rather than build something thin or risky.
  Staying in the backlog until there's a real number to build around.
- **Title trims** — reconsidered and downgraded. The 6 flagged titles are 61–63 characters,
  barely over my own audit script's 60-char flag and still well inside Google's actual
  pixel-width truncation point. Trimming them risked cutting brand consistency (the "| A Team"
  suffix) for a cosmetic gain. Not worth the edit.

## Verify
- Full-site audit across all 72 pages: **zero duplicate titles, zero duplicate metas, exactly
  one H1 per page**, valid Service/WebPage + FAQPage + BreadcrumbList schema on each new page.
- Sitemap cross-checked against the file tree: only the 4 intentionally-omitted pages absent.
- **Zero broken internal links** (excluding the documented `/painting-services/` redirect).
- **No orphans**: the 3 new pages have 3, 3, and 4 real inbound links from the retargeted
  cross-links.
- Every local fact (Piqua's landmarks, Dayton's neighborhoods, Vandalia's streets) was reused
  from that city's own already-published page — fourth loop running with zero fabricated
  local claims or invented pricing.

## Learn
- **Knowing when *not* to build is as valuable as knowing what to build.** This loop's most
  important decision was declining `/window-cleaning-cost-ohio/` mid-plan once the actual data
  behind it turned out to be one number, not a table. The backlog had scored it "safe" based on
  reusing that one figure — the plan should have checked *how much* content that one figure
  actually supports before scoring it ready. Future backlog entries for pricing pages should
  note how many real data points exist, not just whether one is available.
- **The dead-cross-link check is now 4-for-4.** Every loop that started with a grep of
  city-hub link-cards against real page targets has found at least one dead link. It's cheap
  (a few grep calls) and has never once come back empty — keep it as the first Sense step,
  every loop, indefinitely.

## Score after this loop: 88/100
Remaining backlog: gutter cleaning for Piqua/Englewood/Fairborn, a real `/window-cleaning-cost-ohio/`
once there's more than one number to build it on, and everything blocked on Anthony in
`needs-anthony.md` (GA4/GSC, a real photo, the phone-number conflict, brand palette decision).
