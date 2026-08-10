/*
 * Instant estimator for /estimate/.
 *
 * Drives the multi-step quiz and writes its answers into the hidden fields of
 * the real <form> in the page. It does NOT submit anything itself — the final
 * button is an ordinary submit and Netlify Forms captures the POST with the
 * photo attached. If this file fails to load, the form is still a working
 * (if unstepped) contact form. That is deliberate: the previous version of
 * this page performed its only send inside `if (ZAPIER_WEBHOOK_URL)` with the
 * constant left empty, so every lead was silently discarded after the customer
 * was shown a success screen.
 *
 * PRICING ENGINE — recovered verbatim from the original tool (Netlify deploy
 * 6a4d224bd4a0abd1a7e8b9a7, 2026-07-07). Confirmed current 2026-08-10.
 * Edit these numbers and nothing else to reprice.
 */
(function () {
  "use strict";

  var WINDOW_BASE = { small: 143, medium: 186, large: 244, xl: 330 };
  var TWO_STORY_MULT = 1.45;
  var WASH = {
    driveway: { label: "Driveway / walkway pressure wash", small: 143, medium: 215, large: 287, xl: 388 },
    siding:   { label: "House siding softwash",            small: 287, medium: 402, large: 532, xl: 719 },
    roof:     { label: "Roof softwash",                    small: 431, medium: 575, large: 791, xl: 1079 },
  };
  var SIZE_LABELS = { small: "Small / ranch", medium: "Average 2–3 bed", large: "Large home", xl: "Extra large / estate" };
  var BUNDLE_DISCOUNT = 0.12;   // applied to retail when any wash is added
  var RANGE_LOW = 0.90, RANGE_HIGH = 1.12;

  var form = document.getElementById("est-form");
  if (!form) return;

  var S = { step: 0, size: null, twoStory: null, addons: [] };

  var money = function (n) { return "$" + Math.round(n).toLocaleString(); };

  function calc() {
    if (!S.size) return { windowPrice: 0, retail: 0, discount: 0, yourPrice: 0 };
    var windowPrice = WINDOW_BASE[S.size] * (S.twoStory ? TWO_STORY_MULT : 1);
    var washTotal = S.addons.reduce(function (sum, k) { return sum + WASH[k][S.size]; }, 0);
    var retail = windowPrice + washTotal;
    var discount = S.addons.length ? Math.round(retail * BUNDLE_DISCOUNT) : 0;
    return { windowPrice: windowPrice, retail: retail, discount: discount, yourPrice: retail - discount };
  }

  function rangeText(n) { return money(n * RANGE_LOW) + "–" + money(n * RANGE_HIGH); }

  // ---- steps -------------------------------------------------------------
  var steps = form.querySelectorAll(".est-step");
  var prog = document.getElementById("est-prog");
  var progBar = document.getElementById("est-prog-bar");
  var PCT = [0, 20, 40, 60, 80, 100, 100];

  function go(n) {
    S.step = n;
    Array.prototype.forEach.call(steps, function (el) {
      el.classList.toggle("active", Number(el.dataset.step) === n);
    });
    prog.hidden = (n === 0);
    progBar.style.width = (PCT[n] || 0) + "%";
    if (n === 5) renderEstimate();
    if (n === 6) { var f = document.getElementById("est-name"); if (f) f.focus(); }
    // Keep the active step in view without yanking the page on first paint.
    if (n > 0) {
      var top = form.getBoundingClientRect().top + window.pageYOffset - 90;
      window.scrollTo({ top: top, behavior: "smooth" });
    }
    syncFields();
  }

  // ---- hidden field sync -------------------------------------------------
  function set(name, value) {
    var el = form.querySelector('[name="' + name + '"]');
    if (el) el.value = value;
  }

  function serviceList() {
    return ["Window cleaning"].concat(S.addons.map(function (k) { return WASH[k].label; })).join(", ");
  }

  function syncFields() {
    var c = calc();
    set("home_size", S.size ? SIZE_LABELS[S.size] : "");
    set("stories", S.twoStory === null ? "" : (S.twoStory ? "Two stories" : "Single story"));
    set("services", serviceList());
    set("retail_value", c.retail ? money(c.retail) : "");
    set("bundle_discount", c.discount ? "−" + money(c.discount) : "None");
    set("ballpark", c.yourPrice ? rangeText(c.yourPrice) : "");
  }

  // ---- add-on pricing labels --------------------------------------------
  function refreshAddonPrices() {
    form.querySelectorAll("[data-addon]").forEach(function (btn) {
      var k = btn.dataset.addon;
      var on = S.addons.indexOf(k) !== -1;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.classList.toggle("active", on);
      btn.querySelector("[data-addon-label]").textContent = (on ? "✓ " : "+ ") + WASH[k].label;
      var price = btn.querySelector("[data-addon-price]");
      price.textContent = S.size ? money(WASH[k][S.size]) : "—";
    });
    var next = document.getElementById("est-addon-next");
    if (next) next.textContent = S.addons.length ? "NEXT — ADD A PHOTO →" : "JUST WINDOWS — NEXT →";
  }

  // ---- estimate breakdown ------------------------------------------------
  function renderEstimate() {
    var c = calc();
    var host = document.getElementById("est-lines");
    host.textContent = "";

    // Built with DOM nodes rather than innerHTML — nothing here is ever
    // assembled from user input, and it stays that way by construction.
    function line(label, value, cls) {
      var row = document.createElement("div");
      row.className = "est-line" + (cls ? " " + cls : "");
      var a = document.createElement("span");
      a.textContent = label;
      var b = document.createElement("span");
      b.textContent = value;
      if (cls === "disc") { b.className = "est-disc"; a.className = "est-disc"; }
      row.appendChild(a); row.appendChild(b);
      host.appendChild(row);
      return row;
    }

    line("Window cleaning — " + SIZE_LABELS[S.size] + (S.twoStory ? " (two-story)" : ""), money(c.windowPrice));
    S.addons.forEach(function (k) { line(WASH[k].label, money(WASH[k][S.size])); });

    var retail = line("Retail value", money(c.retail), "total");
    if (c.discount) {
      retail.querySelector("span:last-child").classList.add("est-strike");
      line("A-Team bundle discount (12%)", "−" + money(c.discount), "disc");
    }
    document.getElementById("est-range").textContent = rangeText(c.yourPrice);
  }

  // ---- events ------------------------------------------------------------
  form.addEventListener("click", function (e) {
    var t = e.target.closest("[data-go],[data-size],[data-stories],[data-addon]");
    if (!t) return;

    if (t.dataset.size) {
      S.size = t.dataset.size;
      form.querySelectorAll("[data-size]").forEach(function (b) {
        b.classList.toggle("active", b === t);
      });
      refreshAddonPrices();
      go(2);
      return;
    }
    if (t.dataset.stories) {
      S.twoStory = t.dataset.stories === "2";
      form.querySelectorAll("[data-stories]").forEach(function (b) {
        b.classList.toggle("active", b === t);
      });
      refreshAddonPrices();
      go(3);
      return;
    }
    if (t.dataset.addon) {
      var k = t.dataset.addon;
      var i = S.addons.indexOf(k);
      if (i === -1) S.addons.push(k); else S.addons.splice(i, 1);
      refreshAddonPrices();
      syncFields();
      return;
    }
    if (t.dataset.go) go(Number(t.dataset.go));
  });

  // ---- photo -------------------------------------------------------------
  var file = document.getElementById("est-file");
  var drop = document.getElementById("est-drop");
  var preview = document.getElementById("est-preview");

  if (drop && file) {
    drop.addEventListener("click", function () { file.click(); });
    file.addEventListener("change", function () {
      var f = file.files && file.files[0];
      if (!f) return;
      preview.src = URL.createObjectURL(f);
      preview.hidden = false;
      drop.querySelector("b").textContent = "Photo added — tap to change";
      drop.querySelector("span").textContent = f.name;
    });
  }

  refreshAddonPrices();
  syncFields();
})();
