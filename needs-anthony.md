# Needs Anthony

One line each. Everything here is blocked on you — the loop keeps running without it.

## Blocking / high priority

- **Which branch does Netlify actually deploy?** Production is currently building from
  `claude/business-plans-daily-reminders-vw8oz1`, not `main`. Until that's confirmed or changed,
  merging this work to `main` ships nothing. (Netlify → Site configuration → Build & deploy → Branches)
- **Phone number conflict — three different numbers are in play.** The site uses
  **(937) 777-9093** on all 63 pages (685 mentions, 433 `tel:` links). The swarm brief says
  (937) 270-2452. Your profile says (937) 939-2936. I changed nothing. Which is the number that rings?
- **Brand palette + fonts have drifted from the written spec.** The brief says Orange `#F58220`,
  Blue `#1B5B98`, Charcoal `#333333`, Anton + Montserrat. The live site uses `#E86A12`, `#002050`,
  `#111827`, plus a cyan `#2BB8D0` that isn't in the spec, with Archivo Black + Inter. That came from
  the "Claystone" restyle you approved. Is the restyle canonical, or should the site go back to spec?
  I did not touch it — reverting is a full redesign, not a fix.

## Clean Club

- **Deposit + monthly commitment?** The brief describes Clean Club as deposit + monthly. The site
  currently sells it as "10% off, two schedules, no dollar amount." I built `/clean-club/` on the
  **existing** terms only — I won't change pricing or offer structure without you saying so.
- **Do you want a Clean Club price on the page,** or keep "10% off the regular price, confirmed on site"?

## Verification

- **Confirm Google reviews are still 5.0 with 32 reviews.** That number is hard-coded into
  `aggregateRating` schema on every page. If the live count has moved, the structured data is stale.
- **Warranty wording** (12-month house wash re-clean, 24-month roof on organic streaks) — still accurate?

## Measurement — the loop is guessing without these

- **Google Analytics 4** — not installed. No behavior data at all right now.
- **Google Search Console** — no verification tag found. Without it there is no query or impression data,
  so keyword work is inference instead of evidence.
- **Google Business Profile access** — needed to align GBP categories/services with the site.

## Content

- **A real photo of you** (and family/crew if you want) for the homepage. Right now trust rests on
  reviews and job photos — there's no face. This is the single biggest trust gap and I can't invent it.
- **Piqua** — worth a full city hub? Dayton's is built now (Loop 2); Piqua still has 2 service
  pages and no hub.

## From the Loop 2 competitor teardown (`intel/competitors.md`)

- **Review count reads small.** The site shows 5.0★/32 reviews — a strong rating, but some
  competitors show hundreds (one shows 3,000+). The rating isn't the problem, the count is.
  If you want this pushed, it's a review-request cadence fix, not a code fix — I can help
  build the ask once you tell me how you want to request them.
- **Certification badges.** A couple of competitors show SoftWash Systems or PWNA certification
  badges and state their exact liability coverage (e.g. "$1M insured") instead of just "insured."
  If you hold any certifications beyond BBB, or want the coverage amount stated, tell me and
  I'll add it — I won't display a cert or a dollar figure I can't confirm you actually have.
