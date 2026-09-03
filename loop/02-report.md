# Loop 2 — Report
**Date:** 2026-09-02 · **Score: 76 → 80** (predicted 76 → 80, hit exactly)

## Shipped
1. **`/pressure-washing-dayton-ohio/`** — the biggest service × the biggest city, previously missing.
   Full page: hero, local-knowledge prose (verified facts only — 16 mi / ~21 min via I-75,
   real Dayton neighborhoods), gallery, service cross-links, 6-question FAQ, lead form, schema
   (Service + FAQPage + BreadcrumbList + HomeAndConstructionBusiness).
2. **`/dayton-ohio/`** city hub — every other service city already has one; Dayton's pages had
   no hub linking them together. Built on the same pattern as `troy-ohio`, cross-linking all
   3 Dayton pages plus neighboring cities. Reused a real, already-published Google review
   (Mona Motekallem) rather than inventing one.
3. **Cross-linked the 3 Dayton pages** — `house-washing-dayton-ohio` and
   `commercial-pressure-washing-dayton-ohio` now link to the new hub and to each other.
4. **Fixed the footer "Dayton, OH" link on 62 pages** — it pointed at `house-washing-dayton-ohio`
   sitewide; now points at the new `/dayton-ohio/` hub, matching every other city's footer link.
5. Added both new pages to `sitemap.xml`.
6. Re-ran the competitor-scout recon that hit a rate limit in Loop 1 — `intel/competitors.md`
   is now complete (10 competitors, 9 directly verified). Top finding: A Team's review *count*
   (32) reads small next to competitors showing hundreds — a real trust gap, logged below.

## Verify
- Full-site audit re-run across all 66 pages: **zero duplicate titles, zero duplicate metas,
  every page exactly one H1**, schema present and valid on both new pages.
- Sitemap cross-checked against the file tree: only the 4 intentionally-omitted pages (3
  thank-you pages, noindexed `/free-quote/`) are absent — correct, unchanged from baseline.
- Internal-link check: only flagged link is `/painting-services/`, which is a documented,
  intentional 301 redirect predating this loop — not a regression.
- All images referenced on the new pages verified to exist before writing (`gallery-driveway-sidewalk-2.webp`, etc.).
- City facts fact-checked via WebSearch before writing, not invented: Tipp City–Dayton distance
  (16 mi / ~21 min, travelmath.com) and the named Dayton neighborhoods (Oregon District, South
  Park, Wright-Dunbar, Belmont) are real, verified historic districts — not suburbs mislabeled
  as neighborhoods.
- Pricing on the new page reuses the numbers already live on `/pressure-washing-cost-ohio/` —
  nothing new invented, no guardrail risk.

## Learn
- **The keyword-hunter subagent (no working paid data) and this manual audit independently
  converged on the same #1 gap** (Dayton residential pressure washing). When two different
  methods agree without shared data, that's a stronger signal than either alone — worth
  weighting subagent-sourced opportunities higher next time they corroborate a manual finding.
- **The sitewide footer-link bug pattern repeats.** Loop 1 found Clean Club unlinked on 50
  pages; Loop 2 found the Dayton footer link pointing at the wrong page on 62 pages. Both were
  single-string sitewide typos/oversights, not per-page mistakes. Worth a standing check next
  loop: grep every footer link target against what it should be, across all pages, before
  looking for new content gaps.
- **The competitor-scout agent's own site read was incomplete** — its retry still reported "no
  standalone service page found" for window cleaning and only "confirmed Troy" as a full city
  page, despite `/window-cleaning-tipp-city-ohio/` and 62 other pages existing. It was
  searching/fetching the live site fresh rather than reading this repo, and undercounted. Its
  competitor-side findings (review count gap, certification badges) are still solid — just
  discount its A-Team-side self-assessment.

## Not shipped, backlogged
- Gutter cleaning expansion (Troy/Beavercreek/Huber Heights) — real gap, bigger effort, next loop.
- `/window-cleaning-cost-ohio/` — mirrors the proven pricing-guide template, safe to build
  (reuses the already-published $125–$300 window-cleaning figure), backlogged for effort reasons.
- Review-count trust gap (32 vs. competitors' hundreds) — not fixable in code; flagged for Anthony.
