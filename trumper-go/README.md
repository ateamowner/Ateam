# trumper.go — site

A static, no-backend site for the `trumper.go` Web3 domain: what the project
is, the latest takes and curated headlines, the domain's wallet records, and a
plain-language statement of where the project stands.

Built to be pinned to IPFS and served from the domain itself, so there is no
server to keep running.

## Structure

- `index.html` — page layout/sections.
- `content.js` — all site content as a single `SITE` object. Edit this file to
  update the site; the page re-renders from it automatically.
- `app.js` — renders `content.js` into `index.html`. No framework, no build
  step, no network calls.
- `styles.css` — brand system (Orange `#FF6A13`, Blue `#3D8BD4`, dark
  `#0B1119`). System fonts only, so nothing has to download from a CDN that an
  IPFS gateway may not reach.
- `icon.svg` — favicon.

Everything is referenced with relative paths, which is what makes the folder
work unchanged from a local disk, a normal web host, or an IPFS CID.

## Updating the site

Edit the relevant array/object in `content.js`. No other file needs to change
for content edits.

- **New post** — add an object to the top of `SITE.posts`. Use
  `kind: 'take'` for your own writing and `kind: 'link'` plus a
  `source: { label, url }` when you are pointing at someone else's piece.
- **Wallet records** — fill in the real addresses in `SITE.wallets.addresses`,
  then set `SITE.wallets.live = true`. The section stays hidden while that flag
  is `false`, so placeholder addresses can never render as if they were real.
- **Social links** — set the `url` on a row in `SITE.links`. A row with
  `url: null` renders as "not live yet" instead of a dead link.
- **Where we stand** — keep `SITE.standing` current. It is the most useful
  thing on the page for anyone deciding whether to trust the site, and it is
  only worth anything if it is true.

## Running locally

No build step. Serve the folder with any static file server:

```
cd trumper-go
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` directly with `file://`
also works.

## Deploying to IPFS

1. Pin the folder. Any pinning service works — the goal is a CID that stays
   pinned, not one that gets garbage-collected in a week:

   ```
   ipfs add -r trumper-go
   ```

   The CID of the top-level folder is the one you want.

2. In the Unstoppable Domains dashboard for `trumper.go`, set the IPFS website
   record to that CID.

3. Re-pin and update the record every time you publish. The CID changes with
   the content — that is the point, but it does mean the domain record is a
   manual step in the publish loop.

Note that `.go` resolution needs a Web3-aware browser (Brave, Opera) or an
extension; other visitors reach it through a public gateway. Worth keeping in
mind before pointing a general audience at the bare domain.

## Deploying to a normal web host

The same folder works as-is on any static host. Publish `trumper-go` as the
root directory with no build command.
