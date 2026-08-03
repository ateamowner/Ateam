// Sends each quote request to a Zapier "Catch Hook" so Zapier can text the
// owner. This runs *in addition to* the normal Netlify Forms submission —
// Netlify stays the system of record, so a webhook failure can never cost a
// lead.
//
// SETUP: paste your Zapier Catch Hook URL below. See README.md ("Text
// notifications via Zapier") for the Zap steps.
(function () {
  var ZAPIER_WEBHOOK_URL = "";

  var form = document.querySelector('form[name="quote-request"]');
  if (!form) return;

  form.addEventListener("submit", function () {
    if (!ZAPIER_WEBHOOK_URL) {
      console.warn(
        "[A-Team] ZAPIER_WEBHOOK_URL is not set in lead-form.js — " +
          "the lead was saved to Netlify Forms but no text was sent."
      );
      return;
    }

    var data = new FormData(form);
    data.delete("form-name");
    data.delete("bot-field");
    data.append("submitted_at", new Date().toISOString());
    data.append("page", window.location.href);

    // Form-encoded + no-cors keeps this a "simple" request: no preflight, no
    // CORS error, and Zapier parses the body straight into Zap fields.
    // keepalive lets it finish after Netlify navigates to the thank-you page.
    try {
      fetch(ZAPIER_WEBHOOK_URL, {
        method: "POST",
        mode: "no-cors",
        keepalive: true,
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(data).toString(),
      }).catch(function () {
        /* Never block or delay the submission on a notification failure. */
      });
    } catch (e) {
      /* Same — the Netlify submission proceeds regardless. */
    }
  });
})();
