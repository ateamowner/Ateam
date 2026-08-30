/**
 * Public QR lead-source destinations.
 * Print https://ateamcontractings.com/qr/<slug> on the matching piece.
 * The function logs the scan, then 302s here with UTM.
 *
 * truck / card → homepage (who we are)
 * flyer / invoice / yard → estimator (ready to quote)
 */
export const QR_ROUTES = {
  truck: "/",
  flyer: "/estimate/",
  invoice: "/estimate/",
  yard: "/estimate/",
  card: "/",
};

export const QR_UTM = {
  utm_source: "qr",
  utm_medium: "offline",
};

export const CANARY_DESTINATION = "https://ateamcontractings.com/";

export const TOKEN_RE = /^[0-9a-z]{32,}$/i;

export function normalizeSlug(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\/+$/, "");
}

export function normalizeToken(value) {
  return String(value || "").trim().toLowerCase();
}

export function qrDestination(slug, origin = "https://ateamcontractings.com") {
  const key = normalizeSlug(slug);
  const path = QR_ROUTES[key];
  if (!path) return null;
  const url = new URL(path, origin);
  url.searchParams.set("utm_source", QR_UTM.utm_source);
  url.searchParams.set("utm_medium", QR_UTM.utm_medium);
  url.searchParams.set("utm_campaign", key);
  return url.toString();
}

export function findCanary(tokens, rawToken) {
  const token = normalizeToken(rawToken);
  if (!TOKEN_RE.test(token)) return null;
  return (tokens || []).find((row) => normalizeToken(row?.token) === token) || null;
}

export function pathAfter(pathname, marker) {
  const parts = String(pathname || "").split("/").filter(Boolean);
  const idx = parts.indexOf(marker);
  if (idx === -1 || !parts[idx + 1]) return "";
  return parts[idx + 1];
}

export function headerValue(req, name) {
  return req?.headers?.get?.(name) || "";
}

export function requestMeta(req) {
  return {
    time: new Date().toISOString(),
    ua: headerValue(req, "user-agent"),
    referer: headerValue(req, "referer") || headerValue(req, "referrer"),
    ip:
      headerValue(req, "x-forwarded-for").split(",")[0].trim() ||
      headerValue(req, "x-nf-client-connection-ip") ||
      headerValue(req, "client-ip"),
  };
}

export function redirect(location) {
  return new Response(null, {
    status: 302,
    headers: {
      Location: location,
      "Cache-Control": "no-store, no-cache, must-revalidate",
      "X-Robots-Tag": "noindex, nofollow",
    },
  });
}

export function notFound() {
  return new Response("Not Found", {
    status: 404,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Robots-Tag": "noindex, nofollow",
    },
  });
}
