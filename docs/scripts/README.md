# Sitewide edit scripts

The website is 27 standalone HTML files with no templating layer, so a change
to something shared — the business schema, the footer — has to touch every
file. These are the scripts that did that, kept so the next such change is a
diff to a script rather than 27 hand edits.

Both are **idempotent**: re-running them on an already-updated site is a no-op.
Run from anywhere; they use the absolute path to `website/`.

```
python3 docs/scripts/schema_pass.py
python3 docs/scripts/footer_pass.py
```

## `schema_pass.py`

Defines the business exactly once per page as a `HomeAndConstructionBusiness`
with `@id` `https://ateamcontractings.com/#business`, and rewrites every
`provider`/`publisher` to a bare `{"@id": ...}` reference to it.

Edit the `BUSINESS` dict to change the business facts, then re-run. It parses
the JSON-LD rather than regexing the HTML, so it will not silently mangle a
block it does not understand.

Adds `hasOfferCatalog` to `Service` nodes **only** on pages whose HTML visibly
contains the matching price range. That check is the point, not an
optimisation — see the AggregateRating note in `website/README.md`.

One trap it already fell into once, now guarded: after the provider rewrite,
the business `@id` string appears on pages that only *reference* it. Testing
for the id as a substring reads those as "already defined" and leaves 21 pages
with a dangling reference. The check has to look for a node whose `@id` **and**
`@type` both match.

## `footer_pass.py`

Replaces the old BBB `<iframe>` seal with a linked static `<img>`, and adds the
NAP line plus the five profile links, wrapped in `.container` so the block
lines up with the footer content above it.

Writes CSS to `css/site.css` for the 25 pages that link it, and separately into
the homepage's inline `<style>` — the homepage does not use the shared
stylesheet.
