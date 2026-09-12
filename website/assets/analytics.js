/*
 * Sitewide GA4 for ateamcontractings.com.
 *
 * Measurement ID G-YRWQKM1HKN — A Team Contracting property 550782419.
 * Do not invent or swap this ID. No GTM, Clarity, or other pixels live here.
 *
 * This file is the only analytics include. Every public HTML page loads it
 * from <head> as <script src="/assets/analytics.js"></script>. It:
 *   1. Loads gtag.js and configs GA4 (automatic page_view on every page).
 *   2. Fires the recommended generate_lead event when a Netlify form named
 *      quick-quote or estimate-request is submitted (HTML5 validation has
 *      already passed). Beacon transport so the hit survives the redirect.
 *   3. Re-fires generate_lead on the matching thank-you page if the submit
 *      hit was lost — sessionStorage dedupes so one lead = one event.
 *
 * Event: generate_lead
 * Param: form_name = "quick-quote" | "estimate-request"
 *
 * The ads landing form (ad-quote on /free-quote/) is intentionally not
 * converted here. Pageviews on that URL still count.
 */
(function () {
  "use strict";

  var MEASUREMENT_ID = "G-YRWQKM1HKN";

  var LEAD_FORMS = {
    "quick-quote": true,
    "estimate-request": true,
  };

  // Thank-you URLs are the Netlify success redirect for each form.
  var THANKS_PATHS = {
    "/thanks/": "quick-quote",
    "/estimate/thanks/": "estimate-request",
  };

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = window.gtag || gtag;

  gtag("js", new Date());
  gtag("config", MEASUREMENT_ID);

  var loader = document.createElement("script");
  loader.async = true;
  loader.src = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;
  document.head.appendChild(loader);

  function storageKey(formName) {
    return "ateam_ga4_lead_" + formName;
  }

  function alreadySent(formName) {
    try {
      return sessionStorage.getItem(storageKey(formName)) === "1";
    } catch (e) {
      return false;
    }
  }

  function markSent(formName) {
    try {
      sessionStorage.setItem(storageKey(formName), "1");
    } catch (e) {
      /* Private mode — still send; a refresh may double-fire. */
    }
  }

  function fireLead(formName) {
    if (!formName || !LEAD_FORMS[formName] || alreadySent(formName)) return;
    markSent(formName);
    gtag("event", "generate_lead", {
      form_name: formName,
      transport_type: "beacon",
    });
  }

  function formNameOf(form) {
    var hidden = form.querySelector('input[name="form-name"]');
    return ((hidden && hidden.value) || form.getAttribute("name") || "").trim();
  }

  function bindForms() {
    var forms = document.querySelectorAll(
      'form[name="quick-quote"], form[name="estimate-request"]'
    );
    Array.prototype.forEach.call(forms, function (form) {
      form.addEventListener("submit", function () {
        fireLead(formNameOf(form));
      });
    });
  }

  function fireThanksIfNeeded() {
    var path = window.location.pathname;
    if (path.charAt(path.length - 1) !== "/") path += "/";
    var formName = THANKS_PATHS[path];
    if (formName) fireLead(formName);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindForms);
  } else {
    bindForms();
  }
  fireThanksIfNeeded();
})();
