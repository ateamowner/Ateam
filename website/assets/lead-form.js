/*
 * Lead form support for any form marked with [data-lead-form]:
 * /free-quote/ (ads landing page) and /estimate/ (instant estimator).
 *
 * Two jobs:
 *   1. Capture ad attribution (utm_*, gclid, fbclid, ...) into the form's
 *      hidden fields, so every Netlify submission says which ad paid for it.
 *   2. Best-effort POST a copy of the lead to a Zapier Catch Hook, so Anthony
 *      gets a text within seconds instead of checking email.
 *
 * Netlify Forms is the system of record. Everything in this file is additive:
 * if the script fails to load, is blocked, or the webhook is never configured,
 * the form still submits normally and the lead is still captured. A lead must
 * never be lost to a notification failure.
 *
 * SETUP — text alerts (optional):
 *   1. In Zapier create a Zap with the "Webhooks by Zapier → Catch Hook"
 *      trigger and copy the URL it gives you.
 *   2. Paste it into ZAPIER_WEBHOOK_URL below and redeploy.
 *   3. Add an SMS action (Twilio, ClickSend, or Zapier's own SMS) sending to
 *      (937) 939-2936. Useful fields: name, phone, city, services, timeline,
 *      source.
 * Leaving it blank is fine and fully supported — see README.
 */
(function () {
  "use strict";

  var ZAPIER_WEBHOOK_URL = "";

  var STORAGE_KEY = "ateam_attribution";

  // Ad-platform click IDs, most specific first — the first one present wins.
  var CLICK_IDS = ["gclid", "gbraid", "wbraid", "fbclid", "msclkid", "ttclid", "li_fat_id"];
  var UTM_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];

  function readAttribution() {
    var params = new URLSearchParams(window.location.search);
    var found = {};
    var sawSomething = false;

    UTM_KEYS.forEach(function (k) {
      var v = params.get(k);
      if (v) { found[k] = v; sawSomething = true; }
    });

    for (var i = 0; i < CLICK_IDS.length; i++) {
      var v = params.get(CLICK_IDS[i]);
      if (v) {
        found.click_id = CLICK_IDS[i] + "=" + v;
        // A bare gclid with no utm_source still tells us the platform.
        if (!found.utm_source) {
          found.utm_source =
            CLICK_IDS[i] === "gclid" || CLICK_IDS[i] === "gbraid" || CLICK_IDS[i] === "wbraid" ? "google" :
            CLICK_IDS[i] === "fbclid" ? "facebook" :
            CLICK_IDS[i] === "msclkid" ? "bing" :
            CLICK_IDS[i] === "ttclid" ? "tiktok" : "paid";
        }
        sawSomething = true;
        break;
      }
    }

    // Params only exist on the ad click itself. Persist them so attribution
    // survives a wander over to the gallery and back.
    try {
      if (sawSomething) {
        sessionStorage.setItem(STORAGE_KEY, JSON.stringify(found));
      } else {
        var saved = sessionStorage.getItem(STORAGE_KEY);
        if (saved) found = JSON.parse(saved);
      }
    } catch (e) {
      /* Private mode or storage disabled — carry on with what's in the URL. */
    }

    return found;
  }

  // A single human-readable string, so the text message and any spreadsheet
  // column are legible without decoding UTM tags.
  function describeSource(attr) {
    if (attr.utm_source) {
      var s = attr.utm_source;
      if (attr.utm_campaign) s += " / " + attr.utm_campaign;
      if (attr.utm_medium && !attr.utm_campaign) s += " / " + attr.utm_medium;
      return "Ad — " + s;
    }
    var ref = document.referrer;
    if (ref) {
      try {
        var host = new URL(ref).hostname.replace(/^www\./, "");
        if (host && host !== window.location.hostname) return "Referral — " + host;
      } catch (e) { /* malformed referrer, fall through */ }
    }
    return "Website — " + document.title.split("|")[0].trim();
  }

  function setField(form, name, value) {
    var el = form.querySelector('input[name="' + name + '"]');
    if (el && value) el.value = value;
  }

  var forms = document.querySelectorAll("[data-lead-form]");
  if (!forms.length) return;

  var attr = readAttribution();

  Array.prototype.forEach.call(forms, function (form) {
  UTM_KEYS.forEach(function (k) { setField(form, k, attr[k]); });
  setField(form, "click_id", attr.click_id);
  setField(form, "source", describeSource(attr));
  setField(form, "landing_page", window.location.href);
  setField(form, "referrer", document.referrer || "direct");

  form.addEventListener("submit", function () {
    // Guard against a double-tap producing two leads and two texts.
    var btn = form.querySelector("[data-submit]") || form.querySelector(".lp-submit");
    if (btn) {
      if (btn.dataset.sent === "1") return;
      btn.dataset.sent = "1";
      btn.textContent = "Sending…";
    }

    if (!ZAPIER_WEBHOOK_URL) return;

    var data = new FormData(form);
    var payload = new URLSearchParams();

    data.forEach(function (value, key) {
      if (key === "form-name" || key === "bot-field") return;
      // Files can't ride along in a form-encoded body; note it and move on.
      // The actual image is on the Netlify submission.
      if (value instanceof File) {
        if (value.size > 0) payload.append("photo_attached", "yes");
        return;
      }
      // Checkbox groups arrive as repeated keys — collapse to one field.
      var existing = payload.get(key);
      payload.set(key, existing ? existing + ", " + value : value);
    });

    if (!payload.get("services")) payload.set("services", "Not specified");
    if (!payload.get("photo_attached")) payload.set("photo_attached", "no");
    payload.set("submitted_at", new Date().toISOString());

    // Form-encoded + no-cors keeps this a "simple" request: no preflight and
    // no CORS failure. keepalive lets it complete after Netlify navigates away
    // to the thank-you page.
    try {
      fetch(ZAPIER_WEBHOOK_URL, {
        method: "POST",
        mode: "no-cors",
        keepalive: true,
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: payload.toString(),
      })["catch"](function () {
        /* Never block or delay the submission on a notification failure. */
      });
    } catch (e) {
      /* Same — the Netlify submission proceeds regardless. */
    }
  });
  });
})();
