# Offline scan routes (QR + canary)

Server-side log-then-redirect. No ads, no new brand, no client beacon
(adblock would kill a pixel). Hits are written to the Netlify function log
and to the private Blobs store `scan-logs`.

## QR lead sources (print these)

| Printed URL | Lands on | UTM campaign |
| --- | --- | --- |
| `https://ateamcontractings.com/qr/truck` | homepage | `truck` |
| `https://ateamcontractings.com/qr/flyer` | estimator | `flyer` |
| `https://ateamcontractings.com/qr/invoice` | estimator | `invoice` |
| `https://ateamcontractings.com/qr/yard` | estimator | `yard` |
| `https://ateamcontractings.com/qr/card` | homepage | `card` |

Every hop adds `utm_source=qr&utm_medium=offline`. Existing lead forms already
copy those into the submission.

Change a destination in `functions/_lib/qr-routes.mjs` (`QR_ROUTES`).

## Canary tokens

`/c/:token` looks like a normal visit: known tokens 302 to
`https://ateamcontractings.com/` with **no** canary UTM. Unknown tokens 404.
Tokens are not in the sitemap, nav, or `robots.txt`.

Seed file: `canary-tokens.json` — `{id, token, label}` with labels
`CANARY-01` … `CANARY-10`. **Do not put recipient names in the repo.**

### Add a new canary token

1. Generate 32+ hex characters (64 is what the seed file uses):

   ```
   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
   ```

2. Append one object to `canary-tokens.json`:

   ```
   { "id": 11, "token": "<paste hex>", "label": "CANARY-11" }
   ```

3. Deploy. Give the person `https://ateamcontractings.com/c/<token>` only —
   not a page that lists tokens.

## Reading logs

- **Function log:** Netlify → Functions → `qr` / `canary` → lines starting
  `scan-log`.
- **Private store:** Netlify → Blobs → store `scan-logs`.
  Keys look like `qr/<time>-<uuid>` and `canary/<time>-<uuid>`.
  Rolling files: `qr/log.jsonl`, `canary/log.jsonl`.

## Optional webhook

Uncomment and set in the Netlify dashboard (Site configuration → Environment
variables), not in git:

```
# CANARY_WEBHOOK_URL
```

A canary hit then POSTs JSON `{token, label, time, ua, ip, referer}`.
Leave it unset until you have a real hook. There is no default URL.
