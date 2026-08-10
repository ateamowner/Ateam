# Recovered: the original instant estimator

`estimate-original-2026-07-07.html` is the real multi-step instant quote tool
that used to live at `/estimate/`, recovered byte-for-byte from Netlify deploy
history. It was never in git — it only ever existed as a drag-and-drop upload.

**This file is kept outside `website/` on purpose.** It is a reference copy, not
a deployable page — see "Why it can't just be re-uploaded" below.

## What happened to it

| When | Deploy | What changed |
|---|---|---|
| 2026-07-07 15:59 | `6a4d224bd4a0abd1a7e8b9a7` | **Last deploy containing the tool.** 19KB, multi-step quiz, photo capture, pricing engine. |
| 2026-07-12 18:40 | `6a53df83ddc5f6228aed79ad` | `/estimate/` returns **404** — the file was dropped from the upload. |
| 2026-07-12 18:40 (37s later) | `6a53dfa5ac08572f7737be65` | Replaced with the current text/call/email page ("Get Your Instant Price"). |

Every deploy since has carried the replacement. All of these were manual
drag-and-drop uploads (`deploy_source: "drop"`), which is exactly how a file
gets dropped without anyone noticing — there was no diff to review.

Recover other lost files the same way: the deploy list is at
`https://api.netlify.com/api/v1/sites/bd6d0e0f-f62f-4f5a-9734-0d555c735381/deploys`,
and any deploy's files are browsable at
`https://<deploy-id>--ateamcontractingscom.netlify.app/<path>`.

## What's worth keeping: the pricing engine

These are real numbers and the most valuable part of the file.

```
WINDOW_BASE      small $143   medium $186   large $244   xl $330
TWO_STORY_MULT   1.45

driveway/walkway small $143   medium $215   large $287   xl $388
house siding     small $287   medium $402   large $532   xl $719
roof softwash    small $431   medium $575   large $791   xl $1079

bundle discount  12% off retail when any wash add-on is selected
quoted range     ballpark x 0.90  to  ballpark x 1.12
```

## Why it can't just be re-uploaded

Three defects, two of them serious. Restoring this file as-is would put a
broken tool back on the site.

### 1. Leads went nowhere

```js
const ZAPIER_WEBHOOK_URL = "";     // never filled in
async function submitLead(){
  go(7);                            // shows "YOU'RE ON THE BOARD!"
  if(ZAPIER_WEBHOOK_URL){ ... }     // ...and this never ran
}
```

The customer typed their name, phone and address, saw a success screen, and
**nothing was sent anywhere.** Every lead through this tool was silently
discarded. This is the most expensive bug in the file.

### 2. The AI photo reading never worked in production

`runAI()` calls `https://api.anthropic.com/v1/messages` directly from the
browser with **no API key and no `anthropic-version` header**. In a deployed
web page that request cannot authenticate — it always threw, always landed in
the `catch`, and always showed the fallback line:

> "Got your photo and saved it for Anthony. He'll confirm the exact number fast."

Which was itself untrue — the photo was only ever held in browser memory and
sent to that failing request. Nothing reached Anthony.

The code pattern suggests it was authored in an environment that proxies
Anthropic calls for you; that proxy doesn't exist on a real website.

**Do not "fix" this by pasting an API key into the page.** Client-side
JavaScript is public — the key would be readable by anyone who views source,
and usable by anyone who finds it. Doing this properly needs a server-side
proxy (a Netlify Function) that holds the key as an environment variable.

### 3. Smaller problems

- `src="logo.webp"` is relative, so it resolved to `/estimate/logo.webp` and
  404'd. (It has an `onerror` handler that hides the broken image, which is
  why nobody noticed.)
- The customer's name is interpolated straight into `innerHTML` on the success
  screen without escaping.
- Pulls fonts from Google Fonts and uses the older brand palette
  (`#F58220`/`#1B5B98`), so it doesn't match the current site.
- Standalone page with its own chrome — no site nav, no schema, not responsive
  beyond a fixed narrow column.
