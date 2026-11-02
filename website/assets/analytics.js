/*
 * Sitewide GA4 for ateamcontractings.com.
 *
 * Measurement ID G-YRWQKM1HKN — A Team Contracting property 550782419.
 * Do not invent or swap this ID. No GTM, Clarity, or other pixels live here.
 *
 * This file is the only analytics include. Every public HTML page loads it
 * from <head> as <script src="/assets/analytics.js"></script> (perf-tuned
 * pages use the same tag with `defer`; both work). It:
 *   1. Configs GA4 (automatic page_view on every page) and loads gtag.js
 *      on first interaction or 3.5 s after window load (whichever first) so
 *      it never competes with first paint / LCP.
 *   2. Fires the recommended generate_lead event when a Netlify form named
 *      quick-quote or estimate-request is submitted (HTML5 validation has
 *      already passed). Beacon transport so the hit survives the redirect.
 *   3. Re-fires generate_lead on the matching thank-you page if the submit
 *      hit was lost — sessionStorage dedupes so one lead = one event.
 *
 * Event: generate_lead
 * Param: form_name = "quick-quote" | "estimate-request"
 *
 * Click events (2026-11-01): phone_tap (tel:), email_tap (mailto:),
 * cta_click (links to /estimate/, /free-quote/, /contact/). See below.
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

  // Perf (Oct 8 LCP fix, round 2): inject gtag.js only after the page has
  // painted and settled — on the visitor's first interaction (scroll, tap,
  // click, key) or 3.5 s after window load, whichever comes first. Round 1
  // loaded it right at `load`, which still landed before first paint on slow
  // devices and dragged mobile LCP to ~4.8 s in Lighthouse. Hits queued in
  // dataLayer above (js + config → page_view) are sent once it arrives, so
  // every visitor who stays ~4 s or touches the page is still counted.
  var gtagLoaded = false;
  var INTERACTION_EVENTS = ["scroll", "pointerdown", "touchstart", "keydown", "click"];
  function loadGtag() {
    if (gtagLoaded) return;
    gtagLoaded = true;
    INTERACTION_EVENTS.forEach(function (ev) {
      window.removeEventListener(ev, loadGtag, { passive: true, capture: true });
    });
    var loader = document.createElement("script");
    loader.async = true;
    loader.src = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;
    document.head.appendChild(loader);
  }
  INTERACTION_EVENTS.forEach(function (ev) {
    window.addEventListener(ev, loadGtag, { passive: true, capture: true });
  });
  function scheduleAfterLoad() {
    setTimeout(loadGtag, 3500);
  }
  if (document.readyState === "complete") {
    scheduleAfterLoad();
  } else {
    window.addEventListener("load", scheduleAfterLoad);
  }
  // A visitor who submits a form first still needs gtag for the lead hit.
  document.addEventListener("submit", loadGtag, true);
  // Leaving early (tab hidden) — flush the queued page_view if we can.
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") loadGtag();
  });

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
  // Click tracking (added 2026-11-01). One delegated listener, so every
  // page that loads this file is covered with no per-page markup.
  //   phone_tap  - any tel: link       (params: link_location, page_path)
  //   email_tap  - any mailto: link    (params: link_location, page_path)
  //   cta_click  - links to /estimate/, /free-quote/ or /contact/
  //                (params: cta_target, link_text, link_location, page_path)
  // Beacon transport so the hit survives the dialer / navigation. The
  // capture-phase click listener above has already started loading gtag.js;
  // queued events are sent when it arrives.
  var CTA_PATHS = ["/estimate/", "/free-quote/", "/contact/"];

  function linkLocation(el) {
    if (el.closest("header, nav")) return "header";
    if (el.closest("footer")) return "footer";
    if (el.closest(".lp-sticky, .sticky-cta, [data-cta-bar]")) return "sticky_bar";
    return "body";
  }

  function normPath(href) {
    try {
      var u = new URL(href, window.location.href);
      if (u.origin !== window.location.origin) return "";
      var p = u.pathname;
      if (p.charAt(p.length - 1) !== "/") p += "/";
      return p;
    } catch (e) {
      return "";
    }
  }

  document.addEventListener(
    "click",
    function (ev) {
      var a = ev.target && ev.target.closest ? ev.target.closest("a[href]") : null;
      if (!a) return;
      var href = (a.getAttribute("href") || "").trim();
      var lower = href.toLowerCase();
      var base = {
        link_location: linkLocation(a),
        page_path: window.location.pathname,
        transport_type: "beacon",
      };
      if (lower.indexOf("tel:") === 0) {
        gtag("event", "phone_tap", base);
        return;
      }
      if (lower.indexOf("mailto:") === 0) {
        gtag("event", "email_tap", base);
        return;
      }
      var path = normPath(href);
      for (var i = 0; i < CTA_PATHS.length; i++) {
        if (path === CTA_PATHS[i]) {
          base.cta_target = CTA_PATHS[i];
          base.link_text = (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 100);
          gtag("event", "cta_click", base);
          return;
        }
      }
    },
    true
  );

  fireThanksIfNeeded();
  // Thank-you pages carry the conversion — load gtag right away there.
  (function () {
    var path = window.location.pathname;
    if (path.charAt(path.length - 1) !== "/") path += "/";
    if (THANKS_PATHS[path]) loadGtag();
  })();
})();
