/*
 * Canary URLs — look like a normal hop to the homepage, not a tripwire page.
 *
 * /c/:token  (32+ hex or base32)
 *
 * Known token: log time, token, user-agent, x-forwarded-for, referer,
 * then 302 to https://ateamcontractings.com/ with no canary UTM.
 * Unknown token: 404.
 *
 * Tokens live in netlify/canary-tokens.json (labels CANARY-01 .. CANARY-10,
 * no recipient names). If CANARY_WEBHOOK_URL is set in the Netlify dashboard,
 * a hit also POSTs {token, label, time, ua, ip, referer}. That env var is
 * unset on purpose — do not invent a live webhook secret.
 */

import tokens from "../canary-tokens.json" with { type: "json" };
import {
  CANARY_DESTINATION,
  findCanary,
  pathAfter,
  requestMeta,
  redirect,
  notFound,
  normalizeToken,
} from "./_lib/qr-routes.mjs";
import { appendScanLog, pingCanaryWebhook } from "./_lib/log.mjs";

export const config = {
  path: ["/c/:token", "/c/:token/"],
};

function tokenFrom(req, context) {
  const fromPath = normalizeToken(context?.params?.token);
  if (fromPath) return fromPath;
  const url = new URL(req.url);
  return normalizeToken(
    url.searchParams.get("token") ||
      pathAfter(url.pathname, "c") ||
      pathAfter(url.pathname, "canary"),
  );
}

export default async (req, context) => {
  const token = tokenFrom(req, context);
  const row = findCanary(tokens, token);
  if (!row) return notFound();

  const meta = requestMeta(req);
  const payload = {
    kind: "canary",
    time: meta.time,
    token,
    label: row.label,
    ua: meta.ua,
    ip: meta.ip,
    referer: meta.referer,
  };

  await appendScanLog(payload);
  await pingCanaryWebhook({
    token,
    label: row.label,
    time: meta.time,
    ua: meta.ua,
    ip: meta.ip,
    referer: meta.referer,
  });

  return redirect(CANARY_DESTINATION);
};
