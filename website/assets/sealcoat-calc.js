/*
 * Live square-footage calculator for the seal coating pages
 * (seal-coating-*-ohio/). One flat, published rate: $2 per square foot,
 * for concrete or roof surfaces alike. Unlike the /estimate/ quiz's other
 * add-ons (fixed price per home-size tier), this is a genuine sqft x rate
 * calculation, because the owner published an actual per-square-foot rate
 * for this service rather than a size-tier estimate.
 *
 * Drives a number input + range slider pair, a live price display, and an
 * SMS deep link whose body is rebuilt on every change so the text arrives
 * with the customer's own number already in it.
 */
(function () {
  "use strict";

  var RATE = 2;

  var form = document.getElementById("calc");
  if (!form) return;

  var numInput = document.getElementById("calc-sqft");
  var rangeInput = document.getElementById("calc-sqft-range");
  var priceOut = document.getElementById("calc-price");
  var cta = document.getElementById("calc-cta");

  var money = function (n) { return "$" + Math.round(n).toLocaleString(); };

  function update(source) {
    var raw = source === "range" ? rangeInput.value : numInput.value;
    var sqft = Math.max(0, Math.min(20000, parseInt(raw, 10) || 0));

    numInput.value = sqft || "";
    rangeInput.value = Math.min(sqft, Number(rangeInput.max));

    var price = sqft * RATE;
    priceOut.textContent = sqft ? money(price) : "—";

    if (cta) {
      var body = sqft
        ? "Hi, I'd like a quote for seal coating — about " + sqft + " sq ft, roughly " + money(price) + "."
        : "Hi, I'd like a quote for seal coating.";
      cta.href = "sms:+19377779093?&body=" + encodeURIComponent(body);
    }
  }

  numInput.addEventListener("input", function () { update("number"); });
  rangeInput.addEventListener("input", function () { update("range"); });
  update("number");
})();
