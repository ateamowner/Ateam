# Lessons

Read this first, every loop. Prune anything that's failed twice.

## Loop 1

- **A mature site was already here.** The brief reads like the site doesn't exist yet
  ("reverse-engineer... before you change anything"). It's a 63-page, technically strong
  site with real conversion infrastructure. Phase 0 found this by actually crawling —
  don't assume a brief's framing matches the repo's actual state. Always crawl before planning.
- **Grep-based audits over-count HTML-entity length.** My first title/meta length pass
  flagged 5 titles and 3 descriptions as over-length; after decoding `&amp;` → `&` properly,
  only 2 descriptions were real. Always decode entities before measuring rendered length —
  otherwise you "fix" things that aren't broken and waste a loop's effort budget.
- **Not every audit hit is a bug.** 3 flagged "missing alt / missing dimensions" images
  were all JS-driven elements by design (a lightbox `<img>` with empty `src`/`alt` until
  clicked, a hidden upload preview, a decorative `aria-hidden` background image with
  intentional `alt=""`). Read the surrounding markup before touching an audit finding —
  a regex hit is a lead, not a verdict.
- **A "10 opportunities" list can hide one real theme.** Nearly every real finding this
  loop traced back to one thing: the offer ladder was defined after the site was mostly
  built, so the site doesn't point at it yet (homepage sells the wrong rung, Clean Club
  has no page). Ship the theme, not just the ranked list — a `/clean-club/` page and a
  homepage rewrite do more for the score than five independent one-off fixes would.
- **Paid SEO tools can be unavailable mid-loop.** Ahrefs returned "Insufficient plan" on
  every endpoint including its own free usage-check; Semrush was out of API units. The
  keyword-hunter agent correctly fell back to WebSearch and labeled everything an
  UNVERIFIED ESTIMATE rather than inventing volume numbers — that's the right failure
  mode. Don't retry the same blocked tool mid-loop; note it in the backlog and move on.
- **A subagent can be cut off by its own session limit mid-task.** The competitor-scout
  agent hit "session limit" before writing `/intel/competitors.md`. Don't block the loop
  on a stalled recon agent — ship what's ready, log the gap, retry next loop.
- **Netlify auto-injects its RUM/analytics script at serve time regardless of what's
  committed.** A stale committed copy (found with an empty `deploy-branch` attribute,
  a tell that it was snapshotted once and never updated) silently doubles the script on
  every page. Diff live HTML against the repo source early — it catches deploy-pipeline
  bugs that no local audit will ever see.
- **Confirm the production branch before trusting any "ship" language.** Netlify's live
  RUM tag named the actual deploy branch (`claude/business-plans-daily-reminders-vw8oz1`),
  not `main`. This has to be verified once, in writing, in `needs-anthony.md` — pushing to
  the wrong branch would make every future loop's "shipped" claim false.
