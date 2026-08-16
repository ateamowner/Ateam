# Polymarket Arbitrage Detectors

A clean-room implementation of the arbitrage *definitions* from
"Unravelling the Probabilistic Forest: Arbitrage in Prediction Markets"
(Saguillo, Ghafouri, Kiffer, Suarez-Tangil, 2025). Pure standard library,
no dependencies, no network calls.

    polymarket_arbitrage.py          the four functions
    test_polymarket_arbitrage.py     28 cases covering the payout arithmetic

## Run it

From this folder:

    python3 polymarket_arbitrage.py          # the worked examples
    python3 test_polymarket_arbitrage.py     # prints "OK  28 cases, 0 failed"

Python 3.7+ (dataclasses). No `pip install` needed.

## The four functions

**`single_condition_arbitrage(yes_price, no_price)`** — one market's YES and NO
must sum to $1, because exactly one of them pays $1 at resolution. If they sum
to less, buy both and collect the difference. If they sum to more, mint a
YES/NO pair for $1 and sell both.

**`market_rebalancing_arbitrage(yes_prices)`** — the same logic across a NegRisk
market's N mutually exclusive conditions (e.g. Republican / Democrat /
Third-party). Exactly one resolves True, so the YES prices should sum to $1.
Under $1: buy one YES of each for a guaranteed $1. Over $1: buy one NO of each —
exactly one NO expires worthless, so N−1 of them pay $1.

**`combinatorial_arbitrage(p1, p2, ...)`** — two logically dependent markets. If
subset S in Market 1 must resolve together with subset S' in Market 2, their YES
prices should be equal. If they aren't, the spread is the edge. **You supply the
dependency** — nothing here verifies that the two subsets actually imply each
other, and a wrong pairing turns a "guaranteed" trade into a directional bet.

**`vwap(trades)`** — volume-weighted average price, how the paper prices tokens
from raw trade history.

Every function takes `min_profit` (default `0.0`) and returns
`{"type": None, "profit": 0.0}` when nothing clears that bar.

## Using it on live data

The module is deliberately a pure calculator — it takes prices and returns
verdicts. To point it at real markets you need to add a price source:

1. Pull prices from Polymarket's public CLOB API (`clob.polymarket.com`) —
   `/markets` for the token IDs in a market, `/book` or `/price` for the current
   quotes on each token.
2. Feed the YES/NO prices of one market into `single_condition_arbitrage`, and
   the map of `{condition_name: yes_price}` for a NegRisk market into
   `market_rebalancing_arbitrage`.
3. Set `min_profit` to a real number rather than `0.0` — see below.

## What this does not model

The returned `profit` is **gross and per unit**. Before treating any of it as
money:

- **Order book depth.** These functions take one price per token. A real book
  gives you a few hundred dollars at the top quote and worse prices below it, so
  the achievable size is usually much smaller than the edge suggests.
- **Fees and gas.** Trading fees and Polygon gas come off every leg, and these
  strategies are multi-leg by construction.
- **Execution risk.** The trade is only riskless if *all* legs fill. A partial
  fill leaves you holding a directional position, not an arbitrage.
- **Resolution risk.** "Guaranteed payout" assumes the market resolves as
  written. Ambiguous resolution criteria and UMA disputes are the real tail risk.
- **Latency.** Published edges of a few cents rarely survive long enough for a
  script polling a REST endpoint to take them.

Set `min_profit` above your all-in round-trip cost so the detector stops
reporting edges you cannot actually capture.

Nothing here places orders, holds keys, or touches an exchange.
