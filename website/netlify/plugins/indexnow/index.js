/**
 * After a successful publish, ping IndexNow with sitemap URLs.
 * Soft-fail: a down IndexNow endpoint must never fail the Netlify build.
 */
const { spawnSync } = require("node:child_process");
const path = require("node:path");

module.exports = {
  async onSuccess({ constants }) {
    const publishDir = constants.PUBLISH_DIR || ".";
    const script = path.join(publishDir, "scripts", "indexnow-ping.mjs");
    const sitemap = path.join(publishDir, "sitemap.xml");
    console.log("[indexnow] onSuccess", script);

    const result = spawnSync(process.execPath, [script], {
      encoding: "utf8",
      env: { ...process.env, INDEXNOW_SITEMAP: sitemap },
    });

    if (result.stdout) console.log(result.stdout);
    if (result.stderr) console.log(result.stderr);
    if (result.error) {
      console.warn("[indexnow] ping failed softly:", result.error.message);
    }
  },
};
