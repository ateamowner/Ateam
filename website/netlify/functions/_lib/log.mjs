/**
 * Append one scan line to the private Netlify Blobs store `scan-logs`.
 * Always writes to the function log so a hit is visible even if Blobs is down.
 * A failed write must never block the 302.
 */
export async function appendScanLog(entry) {
  const line = JSON.stringify(entry);
  console.log("scan-log", line);

  try {
    const { getStore } = await import("@netlify/blobs");
    const store = getStore("scan-logs");
    const kind = entry.kind || "scan";
    const id = `${kind}/${entry.time || new Date().toISOString()}-${crypto.randomUUID()}`;
    await store.set(id, line);

    const listKey = `${kind}/log.jsonl`;
    const prev = (await store.get(listKey)) || "";
    await store.set(listKey, `${prev}${line}\n`);
  } catch (err) {
    console.error("scan-log blob write failed:", err?.message || err);
  }
}

/**
 * Optional canary ping. Set CANARY_WEBHOOK_URL in the Netlify dashboard.
 * There is no default URL and no secret is shipped in this repo.
 */
export async function pingCanaryWebhook(payload) {
  const url = process.env.CANARY_WEBHOOK_URL;
  if (!url) return;

  try {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch (err) {
    console.error("canary webhook failed:", err?.message || err);
  }
}
