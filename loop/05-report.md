# Loop 5 — Report
**Date:** 2026-09-05 · **Score before:** 88/100 · **Score after (predicted):** 91/100

## Shipped
- `/gutter-cleaning-piqua-ohio/`, `/gutter-cleaning-englewood-ohio/`,
  `/gutter-cleaning-fairborn-ohio/` — all 9 served cities now have their own gutter-cleaning
  page (the pattern started in Loop 3 and completed here). Same $99+ pricing, FAQ set and page
  structure as every other gutter-cleaning city page; local-knowledge sections reuse facts each
  city's hub page already published (Piqua: Great Miami/canopy/Echo Hills/Covington Avenue;
  Englewood: US-40/I-70/MetroPark/Stillwater; Fairborn: Fairfield–Osborn merger, base-boom
  growth, Bath Township).
- `/soft-washing-piqua-ohio/` and `/window-cleaning-piqua-ohio/` — closes the Piqua hub's last
  two service gaps. Reused Piqua's own published facts (river-valley algae angle, downtown
  brick/wood near Fort Piqua Plaza and High Street, aluminum ranch belt near Covington Avenue,
  the Great Miami aquifer hard-water fact) rather than researching anything fresh.
- Retargeted every dead cross-link found in Sense: 3 service link-cards on `piqua-ohio`
  (gutter, soft washing, window cleaning), 1 gutter link-card each on `englewood-ohio` and
  `fairborn-ohio`.
- Also found and fixed drift on the *canonical* gutter-cleaning hub page
  (`/gutter-cleaning-tipp-city-ohio/`) itself: its area-grid still pointed Troy, Vandalia and
  Huber Heights at pressure-washing pages instead of their own (already-live) gutter pages, and
  carried Englewood/Beavercreek/Fairborn as unlinked placeholder spans. Fixed all of it while
  in the file, plus added a handful of missing mutual links between sibling gutter pages
  (Troy→Piqua, Beavercreek→Fairborn, Vandalia→Englewood) so the 3 new pages ship with real
  inbound links (4, 3, 3) rather than a single hub link each.
- Added all 5 new pages to `sitemap.xml`; bumped `lastmod` on every hub/sibling page touched.

## Verification
- Full-site audit re-run: zero duplicate titles/metas, exactly one `<h1>` per page, all 4
  JSON-LD schema blocks on each new page parse as valid JSON, sitemap matches the file tree
  (only the 2 pre-existing intentional omissions — `/free-quote/` and its thanks page — absent,
  unrelated to this loop).
- Inbound-link count for all 5 new pages checked at build time, not after: 4/3/3/3/2 — no
  orphans.
- One bug caught and fixed before shipping: a stray `</br>` typo landed inside two FAQ
  question strings in `window-cleaning-piqua-ohio`'s JSON-LD block; found by grepping for it
  and confirmed the schema re-parses clean after the fix.

## Learn
- Local SEO capped out at 20/20 after Loop 4, so this loop's score gain (88 → 91) had to land
  under Conversion (+2, more indexed landing pages) and Trust (+1, sitewide cross-link
  consistency) instead of the dimension the work is most obviously "about." Logged in
  `memory/lessons.md`.
- New pattern found and logged: the canonical hub page for a service drifts *more* than the
  city pages linking to it, because it's edited less often. Worth a specific check next time a
  dead cross-link points at one.

## Next up (per `memory/backlog.md`)
Everything content-side that doesn't require Anthony's input is now shipped. Remaining backlog
is either blocked (GA4/GSC, a real photo, phone-number conflict, brand palette, Clean Club
structure, review-count/certification gaps — all in `needs-anthony.md`) or deferred pending
real data (`/window-cleaning-cost-ohio/`, the title-trim item). Next loop should re-run the
full Sense pass fresh rather than pull from a backlog that's now mostly cleared.
