"""
polymarket_arbitrage.py

Implements the core arbitrage-detection logic described in:
"Unravelling the Probabilistic Forest: Arbitrage in Prediction Markets"
(Saguillo, Ghafouri, Kiffer, Suarez-Tangil, 2025)

Covers:
  1. Single-condition arbitrage      (YES + NO != $1)
  2. Market Rebalancing Arbitrage    (sum of YES prices across a NegRisk
                                       market's conditions != $1)
  3. Combinatorial Arbitrage         (two dependent markets priced
                                       inconsistently against each other)

This is a clean-room re-implementation of the paper's *definitions*
(Defs 3 & 4), not a copy of their codebase.

All prices are per-token prices in dollars, in [0, 1]. Every "profit"
returned here is gross and per unit -- fees, gas, slippage and order-book
depth are not modelled. See README.md.
"""

from dataclasses import dataclass
from typing import Dict, List


# ---------------------------------------------------------------------------
# 1. Single-condition arbitrage  (Definition 3, footnote 6)
# ---------------------------------------------------------------------------
def single_condition_arbitrage(yes_price: float, no_price: float,
                               min_profit: float = 0.0) -> Dict:
    """
    A single condition's YES and NO tokens should sum to $1.
    If they don't, there's a guaranteed-profit trade.
    Returns a dict describing the opportunity (or none).
    """
    total = yes_price + no_price
    gap = 1.0 - total

    if gap > min_profit:
        return {
            "type": "long",
            "action": "Buy 1 YES + 1 NO",
            "cost": round(total, 4),
            "guaranteed_payout": 1.0,
            "profit": round(gap, 4),
        }
    elif -gap > min_profit:
        return {
            "type": "short",
            "action": "Split $1 -> mint 1 YES + 1 NO, sell both immediately",
            "proceeds": round(total, 4),
            "cost_to_mint": 1.0,
            "profit": round(-gap, 4),
        }
    return {"type": None, "profit": 0.0}


# ---------------------------------------------------------------------------
# 2. Market Rebalancing Arbitrage across N conditions (Definition 3)
# ---------------------------------------------------------------------------
def market_rebalancing_arbitrage(yes_prices: Dict[str, float],
                                 min_profit: float = 0.0) -> Dict:
    """
    yes_prices: {condition_name: yes_token_price}

    Exactly one condition in the market should resolve True, so
    sum(YES prices) should equal $1.
    """
    n = len(yes_prices)
    total_yes = sum(yes_prices.values())
    gap = 1.0 - total_yes

    if gap > min_profit:
        return {
            "type": "long",
            "action": f"Buy 1 YES of each of the {n} conditions",
            "cost": round(total_yes, 4),
            "guaranteed_payout": 1.0,
            "profit": round(gap, 4),
        }
    elif -gap > min_profit:
        # Short: buy all the NO tokens instead (sum(NO) = n - sum(YES)).
        # Exactly one condition resolves True, so exactly one NO pays $0
        # and the other n-1 pay $1 each.
        total_no = n - total_yes
        return {
            "type": "short",
            "action": f"Buy 1 NO of each of the {n} conditions",
            "cost": round(total_no, 4),
            "guaranteed_payout": float(n - 1),
            "profit": round(total_yes - 1.0, 4),
        }
    return {"type": None, "profit": 0.0}


# ---------------------------------------------------------------------------
# 3. Combinatorial (cross-market) arbitrage (Definition 4)
# ---------------------------------------------------------------------------
def combinatorial_arbitrage(market1_subset_price: float,
                            market2_subset_price: float,
                            market1_label: str = "Market 1 subset",
                            market2_label: str = "Market 2 subset",
                            min_profit: float = 0.0) -> Dict:
    """
    If two markets are logically dependent -- e.g. subset S in Market 1
    implies subset S' in Market 2 (they must resolve together) -- then
    the YES prices of S and S' should be equal. If not, buy the cheap
    side (and NO on the complement of the expensive side).
    """
    diff = market1_subset_price - market2_subset_price

    if diff > min_profit:
        return {
            "type": "arbitrage",
            "action": f"Buy YES on {market2_label} (cheap), "
                      f"buy NO on complement of {market1_label} (expensive)",
            "profit": round(diff, 4),
        }
    elif -diff > min_profit:
        return {
            "type": "arbitrage",
            "action": f"Buy YES on {market1_label} (cheap), "
                      f"buy NO on complement of {market2_label} (expensive)",
            "profit": round(-diff, 4),
        }
    return {"type": None, "profit": 0.0}


# ---------------------------------------------------------------------------
# 4. VWAP helper -- how the paper prices tokens from raw trade history
# ---------------------------------------------------------------------------
@dataclass
class Trade:
    price: float
    size: float  # token amount


def vwap(trades: List[Trade]) -> float:
    """Volume-weighted average price, as used in the paper (Section 6)."""
    if not trades:
        return 0.0
    total_value = sum(t.price * t.size for t in trades)
    total_size = sum(t.size for t in trades)
    return total_value / total_size if total_size else 0.0


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 1. Single-condition arbitrage ===")
    # e.g. "Will Assad remain President of Syria through 2024?" (Fig. 5)
    result = single_condition_arbitrage(yes_price=0.55, no_price=0.38)
    print(result)

    print("\n=== 2. Market Rebalancing Arbitrage (3-way NegRisk market) ===")
    # e.g. Republican / Democrat / Third-party wins NY
    prices = {"Republican": 0.30, "Democrat": 0.55, "Third-party": 0.08}
    result = market_rebalancing_arbitrage(prices)
    print(result)

    print("\n=== 3. Combinatorial arbitrage across two dependent markets ===")
    # e.g. "Dem wins popular vote AND presidency" vs a linked margin market
    result = combinatorial_arbitrage(
        market1_subset_price=0.42,
        market2_subset_price=0.51,
        market1_label="Dem wins popular vote & presidency",
        market2_label="Dem wins popular vote (any presidency outcome)",
    )
    print(result)

    print("\n=== 4. VWAP from raw trade history ===")
    trades = [Trade(price=0.58, size=100), Trade(price=0.60, size=50),
              Trade(price=0.57, size=200)]
    print(f"VWAP: {vwap(trades):.4f}")
