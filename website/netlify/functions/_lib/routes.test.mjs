import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import {
  QR_ROUTES,
  CANARY_DESTINATION,
  qrDestination,
  findCanary,
  pathAfter,
} from "./qr-routes.mjs";
import qr from "../qr.mjs";
import canary from "../canary.mjs";

const tokens = JSON.parse(
  readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../../canary-tokens.json"), "utf8"),
);

function request(path, headers = {}) {
  return new Request(`https://ateamcontractings.com${path}`, { headers });
}

test("five public QR slugs are defined", () => {
  assert.deepEqual(Object.keys(QR_ROUTES).sort(), ["card", "flyer", "invoice", "truck", "yard"]);
});

test("QR destinations carry offline UTM and the slug campaign", () => {
  const truck = qrDestination("truck");
  assert.equal(truck, "https://ateamcontractings.com/?utm_source=qr&utm_medium=offline&utm_campaign=truck");
  const flyer = qrDestination("flyer");
  assert.equal(
    flyer,
    "https://ateamcontractings.com/estimate/?utm_source=qr&utm_medium=offline&utm_campaign=flyer",
  );
  assert.equal(qrDestination("unknown"), null);
});

test("QR handler 302s known slugs and 404s the rest", async () => {
  for (const slug of Object.keys(QR_ROUTES)) {
    const res = await qr(request(`/qr/${slug}`), { params: { slug } });
    assert.equal(res.status, 302, slug);
    const loc = res.headers.get("Location");
    assert.match(loc, /utm_source=qr/);
    assert.match(loc, /utm_medium=offline/);
    assert.match(loc, new RegExp(`utm_campaign=${slug}`));
    assert.ok(!/canary/i.test(loc));
  }

  const missing = await qr(request("/qr/nope"), { params: { slug: "nope" } });
  assert.equal(missing.status, 404);
});

test("seeded canary file has 10 unnamed tokens", () => {
  assert.equal(tokens.length, 10);
  const labels = tokens.map((row) => row.label);
  assert.deepEqual(
    labels,
    Array.from({ length: 10 }, (_, i) => `CANARY-${String(i + 1).padStart(2, "0")}`),
  );
  for (const row of tokens) {
    assert.match(row.token, /^[0-9a-f]{32,}$/i);
    assert.ok(row.token.length >= 32);
    assert.ok(!/name|recipient/i.test(JSON.stringify(row)));
  }
});

test("canary handler 302s known tokens to the homepage with no UTM", async () => {
  const row = tokens[0];
  const res = await canary(request(`/c/${row.token}`), { params: { token: row.token } });
  assert.equal(res.status, 302);
  assert.equal(res.headers.get("Location"), CANARY_DESTINATION);
  assert.ok(!/utm_/i.test(res.headers.get("Location")));
});

test("canary handler 404s unknown or short tokens", async () => {
  const unknown = await canary(request("/c/" + "ab".repeat(20)), {
    params: { token: "ab".repeat(20) },
  });
  assert.equal(unknown.status, 404);

  const short = await canary(request("/c/short"), { params: { token: "short" } });
  assert.equal(short.status, 404);

  assert.equal(findCanary(tokens, "nope"), null);
});

test("rewrite URLs still 302 when path params are missing", async () => {
  const qrRes = await qr(request("/.netlify/functions/qr/truck"));
  assert.equal(qrRes.status, 302);
  assert.match(qrRes.headers.get("Location"), /utm_campaign=truck/);

  const row = tokens[0];
  const canaryRes = await canary(request(`/.netlify/functions/canary/${row.token}`));
  assert.equal(canaryRes.status, 302);
  assert.equal(canaryRes.headers.get("Location"), CANARY_DESTINATION);
});

test("pathAfter reads pretty and function URLs", () => {
  assert.equal(pathAfter("/qr/truck", "qr"), "truck");
  assert.equal(pathAfter("/qr/truck/", "qr"), "truck");
  assert.equal(pathAfter("/.netlify/functions/qr/flyer", "qr"), "flyer");
  assert.equal(pathAfter("/c/abc123", "c"), "abc123");
});
