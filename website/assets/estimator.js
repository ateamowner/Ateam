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

  // "What we noticed" — see netlify/functions/photo-note.mjs. The key lives on
  // the server; this page never sees it. If the function is missing, the key
  // is unset, or anything at all goes wrong, the card simply never appears.
  var PHOTO_NOTE_ENDPOINT = "/.netlify/functions/photo-note";
  // 768, not the full photo: Netlify caps synchronous functions at 10s and a
  // 1024px image measured 7.0–8.5s end to end against the live preview. Image
  // tokens dominate that, so the smaller edge buys back most of the margin.
  // The customer's original file is untouched and is what gets submitted.
  var PHOTO_MAX_EDGE = 768;
  var PHOTO_TIMEOUT_MS = 12000; // generous; the customer is never waiting on it

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
      requestNote(f);
    });
  }

  // ---- "What we noticed" -------------------------------------------------
  // Entirely optional colour on the estimate screen. It is deliberately
  // impossible for this to hold up the estimate or the form: the note is
  // fetched in the background the moment a photo is chosen, and every failure
  // path just hides the card. The photo itself always rides along on the
  // Netlify Forms POST whether or not any of this works.

  var noteBox = document.getElementById("est-note");
  var noteBody = document.getElementById("est-note-body");
  var noteTitle = document.getElementById("est-note-title");
  var noteState = "idle";   // idle | loading | done | none
  var noteText = "";
  var noteToken = 0;        // guards against a stale response for an old photo

  function renderNote() {
    if (!noteBox || !noteBody) return;
    if (noteState === "loading") {
      noteBox.hidden = false;
      noteBox.classList.add("loading");
      noteTitle.textContent = "Looking at your photo";
      noteBody.textContent = "One moment…";
    } else if (noteState === "done") {
      noteBox.hidden = false;
      noteBox.classList.remove("loading");
      noteTitle.textContent = "What we noticed";
      noteBody.textContent = noteText;
    } else {
      // idle or failed — no card, no error, no explanation owed to anyone.
      noteBox.hidden = true;
      noteBox.classList.remove("loading");
      noteBody.textContent = "";
    }
  }

  // Full-resolution phone photos are far larger than the model needs and slow
  // the round trip badly. Shrink a copy for the API; the original file is
  // untouched and is what actually gets submitted.
  function downscale(f, cb) {
    var url;
    try { url = URL.createObjectURL(f); } catch (e) { cb(null); return; }
    var img = new Image();
    img.onload = function () {
      try {
        var scale = Math.min(1, PHOTO_MAX_EDGE / Math.max(img.width, img.height));
        var canvas = document.createElement("canvas");
        canvas.width = Math.max(1, Math.round(img.width * scale));
        canvas.height = Math.max(1, Math.round(img.height * scale));
        canvas.getContext("2d").drawImage(img, 0, 0, canvas.width, canvas.height);
        cb(canvas.toDataURL("image/jpeg", 0.75));
      } catch (e) {
        cb(null);   // tainted canvas, out of memory, unsupported format
      }
      URL.revokeObjectURL(url);
    };
    img.onerror = function () { URL.revokeObjectURL(url); cb(null); };
    img.src = url;
  }

  function requestNote(f) {
    if (!noteBox || !window.fetch) return;
    var token = ++noteToken;
    noteState = "loading";
    noteText = "";
    set("photo_note", "");
    renderNote();

    downscale(f, function (dataUrl) {
      if (token !== noteToken) return;
      if (!dataUrl) { noteState = "none"; renderNote(); return; }

      var ctrl = window.AbortController ? new AbortController() : null;
      var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, PHOTO_TIMEOUT_MS) : null;

      var done = function (state, text) {
        if (timer) clearTimeout(timer);
        if (token !== noteToken) return;
        noteState = state;
        noteText = text || "";
        set("photo_note", noteText);
        renderNote();
      };

      fetch(PHOTO_NOTE_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: dataUrl, services: serviceList(), home_size: S.size ? SIZE_LABELS[S.size] : "" }),
        signal: ctrl ? ctrl.signal : undefined,
      })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (d && d.note) done("done", d.note);
          else done("none", "");           // { unavailable: true } lands here
        })
        ["catch"](function () { done("none", ""); });
    });
  }

  refreshAddonPrices();
  syncFields();
})();
