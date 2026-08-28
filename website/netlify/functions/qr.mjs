/*
 * QR lead-source redirects.
 *
 * /qr/truck  /qr/flyer  /qr/invoice  /qr/yard  /qr/card
 *
 * Logs the scan (time, slug, user-agent, referer) to Netlify Blobs + function
 * logs, then 302s to the homepage or estimator with
 * utm_source=qr&utm_medium=offline&utm_campaign=<slug>.
 *
 * Unknown slugs 404. A log failure still redirects — the visitor should never
 * see a function error on a printed URL.
 */

import {
  qrDestination,
  pathAfter,
  requestMeta,
  redirect,
  notFound,
  normalizeSlug,
} from "./_lib/qr-routes.mjs";
import { appendScanLog } from "./_lib/log.mjs";

export const config = {
  path: ["/qr/:slug", "/qr/:slug/"],
};

function slugFrom(req, context) {
  const fromPath = normalizeSlug(context?.params?.slug);
  if (fromPath) return fromPath;
  const url = new URL(req.url);
  return normalizeSlug(url.searchParams.get("slug") || pathAfter(url.pathname, "qr"));
}

export default async (req, context) => {
  const slug = slugFrom(req, context);
  const dest = qrDestination(slug, new URL(req.url).origin);
  if (!dest) return notFound();

  const meta = requestMeta(req);
  await appendScanLog({
    kind: "qr",
    time: meta.time,
    slug,
    ua: meta.ua,
    referer: meta.referer,
  });

  return redirect(dest);
};
