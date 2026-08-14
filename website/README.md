# A Team Contracting website (ateamcontractings.com)

This folder is the full source for the live marketing site, reconstructed from
a crawl of the production site (which was previously deployed via drag-and-drop
with no git history) plus a set of image/performance/SEO fixes.

## Linking this to the live Netlify site

The production site (Netlify project `ateamcontractingscom`, site id
`bd6d0e0f-f62f-4f5a-9734-0d555c735381`) is not yet linked to a Git repo. To
switch it to deploy from this repo:

1. Netlify dashboard → the `ateamcontractingscom` site → **Site configuration
   → Build & deploy → Continuous deployment → Link repository**.
2. Pick this repo (`ateamowner/Ateam`) and the `claude/website-performance-images-yehsjh`
   branch (or `main`, once merged).
3. Set **Base directory** to `website`.
4. Build command: leave blank (no build step — this is a static site).
5. Publish directory: `website` (or `.` if Netlify resolves it relative to the
   base directory — check whichever your dashboard version expects).

After linking, every push to the connected branch redeploys automatically.

## What's fixed here vs. the previous live deploy

- Every homepage image that was 404ing (logo, hero photo, 3 service cards, 4
  of 6 "before/after" photos, About photo) now points to real, optimized
  images instead of missing files.
- The logo no longer hotlinks a temporary Netlify deploy-preview subdomain.
- The soft-washing page no longer hotlinks Google Drive thumbnails.
- The homepage's raw HTML, which was truncated mid-script in production
  (missing `</body></html>` and the analytics snippet), is repaired.
- All 41 `/gallery` photos converted to WebP with `width`/`height` attributes
  (8.7MB → 4.4MB total).
- `width`/`height` + `aspect-ratio`/`object-fit` added across the homepage to
  reduce layout shift; hero image no longer lazy-loaded (it's above the fold).
- `_headers` reconstructed from the security headers observed identically on
  every live page/asset (X-Frame-Options, HSTS, etc.).

## Site structure

```
/                                          homepage
/pressure-washing-tipp-city-ohio/          service pages (6)
/soft-washing-tipp-city-ohio/
/window-cleaning-tipp-city-ohio/
/gutter-cleaning-tipp-city-ohio/
/roof-cleaning-tipp-city-ohio/
/concrete-cleaning-tipp-city-ohio/
/exterior-painting-tipp-city-ohio/         adjacent service
/commercial-pressure-washing-dayton-ohio/  commercial

/pressure-washing-troy-ohio/               city landing pages (5)
/pressure-washing-vandalia-ohio/
/pressure-washing-huber-heights-ohio/
/house-washing-dayton-ohio/
/pressure-washing-piqua-ohio/

/pressure-washing-cost-ohio/               price guide
/soft-washing-vs-pressure-washing/         comparison / snippet target
/blog/                                     blog index + 4 posts

/estimate/                                 instant estimator
/estimate/thanks/                          ↳ its thank-you page
/free-quote/                               ads landing page (noindex)
/free-quote/thanks/                        ↳ its thank-you page
/thanks/                                   homepage quick-quote thank-you
/gallery/                                  before & after photos

netlify/functions/photo-note.mjs           the only server-side code
```

The three thank-you pages are all `noindex, nofollow` and none of them are in
`sitemap.xml`. They stay separate URLs because that is how ad platforms count
a conversion.

The six original service pages, `/gallery/` and `/estimate/` keep their inline
`<style>` blocks. Pages added in the August 2026 SEO pass link the shared
`/css/site.css` instead — same design tokens, one cached request.

### The instant estimator (`/estimate/`)

The multi-step quote tool: home size → stories → wash add-ons → optional photo
→ itemised ballpark → contact details. Restored from the original that was
lost when a drag-and-drop deploy dropped the file on 2026-07-12; see
`docs/recovered/` for the recovered source and the full post-mortem.

**The pricing engine lives at the top of `assets/estimator.js`** and nowhere
else. Edit those constants to reprice; nothing else needs touching.

```
WINDOW_BASE      small $143   medium $186   large $244   xl $330
TWO_STORY_MULT   1.45
driveway         $143 / $215 / $287 / $388
siding           $287 / $402 / $532 / $719
roof             $431 / $575 / $791 / $1079
BUNDLE_DISCOUNT  0.12          RANGE  x0.90 – x1.12
```

#### How it submits

The page is **one real `<form>` wrapping every step.** The script only toggles
which step is visible and writes the answers into hidden fields; the final
button is an ordinary submit, so the POST is plain multipart that Netlify
Forms captures with the photo attached.

This matters. The original tool did its only send inside
`if (ZAPIER_WEBHOOK_URL) { ... }` with that constant left as `""`, so every
customer saw a success screen and **no lead was ever sent anywhere**. There is
deliberately no code path here that can do that: if `estimator.js` fails to
load entirely, the form degrades to a working contact form rather than a
silent hole.

Leads arrive as the `estimate-request` form in Netlify, alongside `ad-quote`
from `/free-quote/` and `quick-quote` from the homepage. **All three need the
same one-time notification setup** — see "Where the leads go" below.

### The homepage quick-quote form

Three fields — name, phone, what needs doing — in the closing CTA band on the
homepage, sharing the row with the estimator button. The estimator is still
the main event; this is for the people who won't tap through a quiz but will
give you three boxes. Submits to `/thanks/` as the `quick-quote` form.

Same construction as everything else here: plain Netlify Forms, no fetch, no
JSON, nothing that can silently swallow a lead if a script fails to load.

#### The photo AI ("What we noticed")

Rebuilt properly, behind `netlify/functions/photo-note.mjs`.

The original called the Anthropic API directly from the browser **with no API
key attached**, so it never worked in production — it fell into its catch
block every time and printed a fallback line claiming Anthony had already
looked at the photo, which he had not. The fix is not "put the key in the
page": page source is public, so a key there is a key anyone can read and
spend. It lives in the function, in `process.env`.

How it runs: pick a photo at step 4 → the page shrinks a *copy* to 768px and
POSTs it to `/.netlify/functions/photo-note` → the function asks Claude what
it can see → a short note renders under the ballpark at step 5 and is saved to
a `photo_note` hidden field, so it arrives with the lead.

**To switch it on:** Netlify dashboard → Site configuration → Environment
variables → add `ANTHROPIC_API_KEY` (get one at console.anthropic.com). Until
then the card simply never appears — which is correct behaviour, not a bug.

Everything about it is designed to fail invisibly. No API key, oversized
photo, model refusal, timeout, upstream outage, function not deployed at all —
every one of those returns HTTP 200 `{ unavailable: true }` and the card stays
hidden. It cannot delay the estimate, block a submission, or show a customer
an error, and the photo itself always rides along on the Netlify Forms POST
regardless. All four failure paths are exercised in the browser, not assumed.

The prompt is deliberately fenced: describe only what is visible, never quote
a price or a duration, never claim a human has reviewed the photo, and say so
plainly when the photo is too dark or isn't a building.

Model: `claude-opus-5`.

**Watch the clock if you change anything here.** Netlify caps synchronous
functions at 10 seconds and this whole feature lives inside that wall.
Measured against a deploy preview with a real job photo, 1024px images and
`max_tokens: 300` came back in **7.0s and 8.5s** — working, but close enough
to the ceiling to be unreliable. That is why the page sends 768px, the
function asks for 200 tokens, and extended thinking is off. Three knobs, all
pointed at the same constraint:

| Knob | Where | Now |
|---|---|---|
| Image longest edge | `PHOTO_MAX_EDGE` in `assets/estimator.js` | 768px |
| `max_tokens` | `photo-note.mjs` | 200 |
| Extended thinking | `photo-note.mjs` | off — `thinking: { type: "disabled" }` |

**Thinking has to be turned off explicitly.** On Opus 5 it is on by default,
and `max_tokens` caps thinking and visible text *together*. Leaving it
implicit spent the budget on reasoning and truncated notes mid-sentence, so
the function also treats `stop_reason: "max_tokens"` as unavailable — half a
sentence in front of a customer is worse than no card.

Turning any of them up costs latency directly, and past ~10s the platform
kills the request and the card just stops appearing. If you want a bigger
image or a longer note, move to a Netlify **background function** with a
polling endpoint first — don't just raise the numbers.

With all three set as above, five consecutive warm calls against a deploy
preview measured 5.4s, 5.6s, 5.7s and 6.6s, all returning complete sentences.
Expect the **first call after a deploy** (or after a long idle) to be slower
or to fail outright on a cold start — that customer simply sees no card,
which is the designed behaviour, and the next call is warm.

The dependency (`@anthropic-ai/sdk`) is why `package.json` exists. There is
still no build step; Netlify installs it so the function can be bundled.

### The ads lead form (`/free-quote/`)

A standalone landing page for paid traffic — Google Ads, Meta, Nextdoor,
anything that needs a click to land somewhere that converts. Point the ad's
destination URL straight at:

```
https://ateamcontractings.com/free-quote/
```

It is deliberately different from the rest of the site:

- **No nav.** Every extra link is a way to leak a click you paid for. Logo,
  form, tap-to-call, nothing else.
- **`noindex, follow`** and **not in `sitemap.xml`**, so it never competes
  with the organic service pages. It is *not* blocked in `robots.txt` — Google
  Ads has to crawl the page to score it.
- **Self-contained CSS.** Ad visitors always arrive with a cold cache, so the
  page is one request instead of two. The trade-off: brand colours live both
  here and in `/css/site.css`, so a palette change means editing both.
- **Form above the fold on mobile**, where most ad clicks come from.

Submissions land on `/free-quote/thanks/` — a separate URL, which is what ad
platforms need to count a conversion.

#### Where the leads go

`Netlify Forms` is the system of record. The form is plain HTML with
`data-netlify="true"`, so Netlify captures every submission on deploy with no
server and no third-party dependency.

**One-time setup in the Netlify dashboard:**

1. Deploy this branch, then go to the site → **Forms**. Three forms appear
   after the first deploy that includes the pages: `quick-quote` (homepage),
   `estimate-request` (`/estimate/`) and `ad-quote` (`/free-quote/`).
2. **Forms → Settings → Form notifications → Add notification → Email
   notification.** Send to `Owner@ateamcontractings.com`. Do this **for each
   of the three forms.** Without it submissions are still saved, but nothing
   tells you they arrived.
3. Submit a test through each live form and confirm it shows up.

Netlify strips `data-netlify` and `netlify-honeypot` from the served HTML once
it has registered a form — their *absence* on the live page is the success
signal, not a problem.

**Environment variables** live next door under Site configuration →
Environment variables. Only one is used: `ANTHROPIC_API_KEY`, for the photo
note. Nothing else on the site needs one.

Netlify's free tier covers 100 submissions/month including the photo uploads.
Past that it needs a paid forms plan — worth watching if the ads scale.

#### Text alerts (optional)

Email is slow when someone is comparing three contractors. To get a text
instead, open `assets/lead-form.js` and paste a Zapier **Catch Hook** URL into
`ZAPIER_WEBHOOK_URL` at the top, then add an SMS action in Zapier pointing at
(937) 939-2936. Useful fields: `name`, `phone`, `city`, `services`,
`timeline`, `source`.

This is strictly additive. If the webhook is never configured, fails, or is
blocked, the lead is still captured by Netlify — a notification failure must
never cost a lead.

#### Conversion tracking

`/free-quote/thanks/` has commented-out blocks for Google Ads and Meta Pixel
near the end of `<head>`. Paste in whichever applies and delete the other;
both are inert until real IDs are filled in.

#### Attribution

`assets/lead-form.js` reads `utm_*`, `gclid`, `gbraid`, `wbraid`, `fbclid`,
`msclkid` and `ttclid` off the landing URL into hidden fields, and stashes
them in `sessionStorage` so they survive a wander to the gallery and back.
Every submission carries a readable `source` (e.g. `Ad — google /
tippcity-pressure-washing`) so you can tell which campaign paid for it.

Tag ad URLs like this and the campaign name flows through to the lead:

```
https://ateamcontractings.com/free-quote/?utm_source=google&utm_medium=cpc&utm_campaign=tippcity-pressure-washing
```

### Structured data

Every page defines the business **once**, as a `HomeAndConstructionBusiness`
node with `@id` `https://ateamcontractings.com/#business`. Everything else on
the page — a `Service`'s `provider`, a `BlogPosting`'s `publisher` — points at
that id with a bare `{"@id": "..."}` reference instead of repeating the
business inline. Before this, 14 pages each carried their own slightly
different copy of the business, which is exactly how a phone number or a name
ends up disagreeing with itself across the site.

**A Team is a service-area business. There is no `streetAddress` property
anywhere, and there must never be one.** The address in schema is locality,
region, postal code and country only; `geo` is the Tipp City centroid, not a
premises. The visible footer NAP matches: name, city, phone.

If you edit the business node, edit it everywhere — `docs/` has the script
that generated it. The invariant worth keeping: exactly one definition per
page, zero dangling references.

**No `AggregateRating` or `Review` markup, deliberately.** Google only allows
it where the reviews being described are visible on that same page. The real
numbers are 32 reviews at 5.0, but until those reviews are rendered on a
Reviews page, marking them up is a manual-action risk. Build the page first,
then add the markup — in that order.

`hasOfferCatalog` appears only on pages that visibly publish the price range
it describes (`$150–$300` driveways, `$300–$600` full house exterior). Same
rule, same reason: don't mark up a price the visitor can't read.

### Conventions to keep

- **The business name is "A Team Contracting" — no hyphen.** This is
  deliberate and was changed sitewide on 2026-08-14; earlier drafts of the SEO
  brief specified a hyphen, so don't "fix" it back. It matches the BBB and Yelp
  listings. The name appears in `<title>`, `og:title`, `twitter:title`, the
  `name` in the business schema, image alt text, the footer NAP, the copyright
  line and the header logo lockup — all of them have to agree.
  **The profile URL slugs still contain `a-team-contracting`** (BBB, Yelp,
  Nextdoor). Those are their URLs, not our name; never rewrite them.
  If Google Business Profile still shows the hyphen, that is the one
  remaining NAP mismatch and it needs changing there, not here.
- **One phone number sitewide: (937) 939-2936.** NAP consistency is a local
  ranking signal; a second number anywhere (site, GBP, Nextdoor, Facebook,
  BBB, Yelp, invoices) actively suppresses Map Pack position.
- **Profile URLs live in two places that must agree**: the `sameAs` array in
  the business node, and the footer trust block. Both currently point at
  Google (`g.page/r/CdoEOEshw5VUEAE/`), the BBB profile under the
  `window-cleaning` slug, Facebook, Nextdoor and Yelp.
- **The BBB seal is a static PNG in a real link**, not the dynamic JS seal and
  not an iframe. It carries `width`/`height` so it reserves space instead of
  shifting the footer on load, and `rel="noopener nofollow"`.
- **Trailing slashes on every internal link** (`/estimate/`, not `/estimate`).
- **`<title>` and `og:title` must match**, and meta descriptions stay under
  160 characters or they truncate in search results.
- **Every page carries JSON-LD**: a `Service`/`Article` block, `FAQPage`
  where there's an FAQ, and `BreadcrumbList` on everything below the
  homepage.
- **Add new URLs to `sitemap.xml`** and to the footer columns, which are
  duplicated across pages.
- **City pages must stay genuinely different from each other.** Five
  templated pages with the city name swapped is doorway-page territory and
  Google filters them. Each one leads with real local specifics (housing
  stock, neighborhoods, local conditions) and uses photos actually shot in
  that city where we have them.

## Known gap

The live site's deploy log shows exactly one custom **redirect** rule that
isn't visible over HTTP and isn't reproduced here (not in this folder's
`netlify.toml`, which only sets `publish`). If something depended on it
(an old bookmarked URL, an ad link, etc.), check the previous deploy's
`_redirects`/`netlify.toml` in the Netlify dashboard's deploy file browser
before fully cutting over, and add the equivalent rule to `netlify.toml` or
a `_redirects` file in this folder.
