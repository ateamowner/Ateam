# A-Team Contracting website (ateamcontractings.com)

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

## Known gap

The live site's deploy log shows exactly one custom **redirect** rule that
isn't visible over HTTP and isn't reproduced here (not in this folder's
`netlify.toml`, which only sets `publish`). If something depended on it
(an old bookmarked URL, an ad link, etc.), check the previous deploy's
`_redirects`/`netlify.toml` in the Netlify dashboard's deploy file browser
before fully cutting over, and add the equivalent rule to `netlify.toml` or
a `_redirects` file in this folder.
