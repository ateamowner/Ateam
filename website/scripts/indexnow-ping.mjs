/**
 * Ping IndexNow / Bing with every URL in sitemap.xml.
 *
 * $0, no secrets. The IndexNow key is public by design (it is also served
 * at /{key}.txt). This script must never fail a Netlify build: every error
 * is logged and the process exits 0.
 *
 * Usage:
 *   node scripts/indexnow-ping.mjs            # POST sitemap URLs
 *   node scripts/indexnow-ping.mjs --dry-run  # parse only, no network
 *
 * Sitemap path (first hit wins):
 *   INDEXNOW_SITEMAP env, ./sitemap.xml, then the live sitemap.
 */
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const HOST = "ateamcontractings.com";
const KEY = "f598e3c2a8096aef342edeccf566e3989e6b23b7607bf201b788335a98713b1b";
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;
const ENDPOINT = "https://api.indexnow.org/indexnow";
const LIVE_SITEMAP = `https://${HOST}/sitemap.xml`;
const BATCH = 10000;
const MAX_BODY = 10 * 1024 * 1024;
const dryRun = process.argv.includes("--dry-run");

function log(...args) {
  console.log("[indexnow]", ...args);
}

function warn(...args) {
  console.warn("[indexnow]", ...args);
}

function urlsFromSitemap(xml) {
  const found = [];
  const re = /<loc>\s*([^<\s]+)\s*<\/loc>/gi;
  let m;
  while ((m = re.exec(xml))) {
    const url = m[1].trim();
    if (url.startsWith(`https://${HOST}/`) || url.startsWith(`http://${HOST}/`)) {
      found.push(url);
    }
  }
  return [...new Set(found)];
}

async function loadSitemapXml() {
  const candidates = [];
  if (process.env.INDEXNOW_SITEMAP) candidates.push(process.env.INDEXNOW_SITEMAP);
  candidates.push(resolve(process.cwd(), "sitemap.xml"));

  for (const path of candidates) {
    try {
      const xml = await readFile(path, "utf8");
      log("read sitemap", path);
      return xml;
    } catch {
      /* try next */
    }
  }

  log("fetching live sitemap", LIVE_SITEMAP);
  const res = await fetch(LIVE_SITEMAP);
  if (!res.ok) throw new Error(`live sitemap HTTP ${res.status}`);
  return await res.text();
}

function payload(urlList) {
  return { host: HOST, key: KEY, keyLocation: KEY_LOCATION, urlList };
}

function splitBySize(urls) {
  const out = [];
  let chunk = [];
  for (const url of urls) {
    const next = chunk.concat(url);
    const size = Buffer.byteLength(JSON.stringify(payload(next)), "utf8");
    if (chunk.length && (next.length > BATCH || size > MAX_BODY)) {
      out.push(chunk);
      chunk = [url];
    } else {
      chunk = next;
    }
  }
  if (chunk.length) out.push(chunk);
  return out;
}

async function postBatch(urlList, i, total) {
  const body = JSON.stringify(payload(urlList));
  log(`POST batch ${i + 1}/${total} (${urlList.length} URLs, ${Buffer.byteLength(body)} bytes)`);
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body,
  });
  const text = await res.text().catch(() => "");
  log(`IndexNow ${res.status}${text ? ` ${text.slice(0, 200)}` : ""}`);
  if (!res.ok && res.status !== 202) {
    warn(`batch ${i + 1} not accepted (HTTP ${res.status}); continuing`);
  }
}

async function main() {
  log("host", HOST);
  log("keyLocation", KEY_LOCATION);
  const xml = await loadSitemapXml();
  const urls = urlsFromSitemap(xml);
  log(`parsed ${urls.length} sitemap URLs`);
  if (!urls.length) {
    warn("no URLs in sitemap; skip ping");
    return;
  }
  const parts = splitBySize(urls);
  if (dryRun) {
    log(`dry-run: would POST ${parts.length} batch(es), no network`);
    return;
  }
  for (let i = 0; i < parts.length; i++) {
    await postBatch(parts[i], i, parts.length);
  }
}

main().catch((err) => {
  warn("ping failed softly:", err?.message || err);
}).finally(() => {
  process.exit(0);
});
