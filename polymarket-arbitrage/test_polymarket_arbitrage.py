"""Tests for the arbitrage definitions.

Every case checks the *payout arithmetic*, not just the sign of the gap --
a detector that fires in the right direction but sizes the trade wrongly is
the expensive kind of bug.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from polymarket_arbitrage import (
    Trade,
    combinatorial_arbitrage,
    market_rebalancing_arbitrage,
    single_condition_arbitrage,
    vwap,
)

failures = 0
checks = 0


def check(ok: bool, label: str, detail: str = "") -> None:
    global failures, checks
    checks += 1
    if ok:
        print(f"  ok    {label}")
    else:
        failures += 1
        print(f"  FAIL  {label}{'  ' + detail if detail else ''}")


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol


def run() -> int:
    print("single_condition_arbitrage")

    # Underpriced pair: 0.55 + 0.38 = 0.93, buy both for $0.93, collect $1.
    r = single_condition_arbitrage(0.55, 0.38)
    check(r["type"] == "long", "underpriced pair is a long", str(r))
    check(close(r["cost"], 0.93), "long cost is the sum of both legs", str(r))
    check(close(r["profit"], r["guaranteed_payout"] - r["cost"]),
          "long profit = payout - cost", str(r))

    # Overpriced pair: mint for $1, sell for $1.07.
    r = single_condition_arbitrage(0.60, 0.47)
    check(r["type"] == "short", "overpriced pair is a short", str(r))
    check(close(r["profit"], r["proceeds"] - r["cost_to_mint"]),
          "short profit = proceeds - mint cost", str(r))

    # Fairly priced.
    r = single_condition_arbitrage(0.42, 0.58)
    check(r["type"] is None, "exact $1 pair is not an opportunity", str(r))
    check(r["profit"] == 0.0, "no opportunity means no profit", str(r))

    # min_profit is a floor, not a suggestion: a 1c edge must not clear a 2c bar.
    r = single_condition_arbitrage(0.55, 0.44, min_profit=0.02)
    check(r["type"] is None, "1c edge is filtered out by a 2c min_profit", str(r))
    r = single_condition_arbitrage(0.55, 0.42, min_profit=0.02)
    check(r["type"] == "long", "3c edge clears a 2c min_profit", str(r))

    print("\nmarket_rebalancing_arbitrage")

    # 0.30 + 0.55 + 0.08 = 0.93. Exactly one resolves True -> $1 back.
    r = market_rebalancing_arbitrage(
        {"Republican": 0.30, "Democrat": 0.55, "Third-party": 0.08})
    check(r["type"] == "long", "YES prices summing below $1 is a long", str(r))
    check(close(r["cost"], 0.93), "long cost is the sum of the YES legs", str(r))
    check(close(r["profit"], 1.0 - 0.93), "long profit = $1 - cost", str(r))

    # 0.40 + 0.45 + 0.25 = 1.10. Buy all 3 NOs for 3 - 1.10 = 1.90,
    # exactly one NO expires worthless, so 2 of them pay $1 each.
    r = market_rebalancing_arbitrage({"A": 0.40, "B": 0.45, "C": 0.25})
    check(r["type"] == "short", "YES prices summing above $1 is a short", str(r))
    check(close(r["cost"], 1.90), "short cost is the sum of the NO legs", str(r))
    check(close(r["guaranteed_payout"], 2.0),
          "n-1 of the n NO legs pay out", str(r))
    check(close(r["profit"], r["guaranteed_payout"] - r["cost"]),
          "short profit = payout - cost", str(r))

    # Two-condition market is the single-condition case in disguise.
    pair = market_rebalancing_arbitrage({"Yes": 0.55, "No": 0.38})
    single = single_condition_arbitrage(0.55, 0.38)
    check(close(pair["profit"], single["profit"]),
          "2-way market agrees with the single-condition detector",
          f"{pair} vs {single}")

    r = market_rebalancing_arbitrage({"A": 0.5, "B": 0.3, "C": 0.2})
    check(r["type"] is None, "YES prices summing to exactly $1 is fair", str(r))

    print("\ncombinatorial_arbitrage")

    # Dependent subsets must price equally; a 9c spread is the edge.
    r = combinatorial_arbitrage(0.42, 0.51)
    check(r["type"] == "arbitrage", "priced-apart subsets are an opportunity", str(r))
    check(close(r["profit"], 0.09), "profit is the absolute spread", str(r))

    # Direction matters: buy the cheap side.
    cheap_second = combinatorial_arbitrage(0.51, 0.42, "M1", "M2")
    check("Buy YES on M2" in cheap_second["action"],
          "buys the cheaper of the two subsets", cheap_second["action"])
    cheap_first = combinatorial_arbitrage(0.42, 0.51, "M1", "M2")
    check("Buy YES on M1" in cheap_first["action"],
          "buys the cheaper side when the order flips", cheap_first["action"])
    check(close(cheap_first["profit"], cheap_second["profit"]),
          "spread is symmetric", f"{cheap_first} vs {cheap_second}")

    r = combinatorial_arbitrage(0.42, 0.42)
    check(r["type"] is None, "equally priced subsets are consistent", str(r))

    print("\nvwap")

    # (0.58*100 + 0.60*50 + 0.57*200) / 350 = 0.5771...
    v = vwap([Trade(0.58, 100), Trade(0.60, 50), Trade(0.57, 200)])
    check(close(v, 202.0 / 350.0), "weights by size, not by trade count", str(v))
    check(vwap([]) == 0.0, "empty history is 0.0")
    check(vwap([Trade(0.5, 0)]) == 0.0, "zero total size does not divide by zero")
    check(close(vwap([Trade(0.33, 10)]), 0.33), "single trade is its own VWAP")

    print(f"\n{'FAIL' if failures else 'OK'}  {checks} cases, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
