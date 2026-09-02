# BASELINE — Loop 0
**Date:** 2026-09-02 · **Scope:** `website/` (63 pages), verified against live production.

## Score: 68 / 100

| Dimension | Weight | Score | Why |
|---|---:|---:|---|
| Conversion | 30 | **19** | Path itself is excellent — 1 click, 3 required fields, estimator already defaults to window cleaning. Loses points because the homepage sells rung 2 (soft washing) instead of rung 1 (window cleaning), and because Clean Club — the recurring rung — has no page, no URL and zero links despite 50 pages naming it. |
| Local SEO | 20 | **15** | Genuinely strong: 63 pages, zero duplicate titles/metas, one H1 each, schema on every page, accurate sitemap. Loses points for no Piqua or Dayton hub, no window/soft washing in Piqua or Dayton, an orphaned seal-coating page, and a homepage title that targets a service+city instead of brand + breadth. |
| Speed & technical | 15 | **13** | 1 stylesheet, 0 render-blocking scripts, WebP throughout, `fetchpriority` on LCP, lazy loading, immutable caching, full security headers. Nits only: 3 alt/dimension gaps, 3 over-long metas, 5 over-long titles. |
| Trust | 15 | **11** | Real reviews with names, 5.0 · 32 count, BBB A+, named warranties, 46-image gallery, insured, family-owned. Held back because `aggregateRating` is unverified against the live GBP, and there is no photo of Anthony or the family on the homepage. |
| Copy & voice | 10 | **8** | Sounds like Anthony — short sentences, real words, no stock-photo energy. One "highest-leverage" nit. Homepage hero copy is strong but aimed at the wrong rung. |
| Mobile | 10 | **8** | Responsive, mobile CTA dock, `inputmode`/`autocomplete` set correctly on phone fields, tap targets fine. Not yet measured on a real device or against field CWV. |

## What the prior work got right
This is a well-built site. Technical SEO is near-spotless and the conversion path is
already short. The opportunities below are **not** cleanup — they are alignment between a
good site and the offer ladder that was defined after most of it was built.

## Top 10 opportunities, ranked by (impact × confidence) ÷ effort

| # | Opportunity | Dim | Impact | Conf | Effort | Score |
|---|---|---|---:|---:|---:|---:|
| 1 | Build `/clean-club/` — the recurring rung has no destination | Conv + SEO | 9 | 0.9 | 2 | **4.05** |
| 2 | Re-point homepage title/H1/hero at brand + window-cleaning entry offer | Conv + SEO + Copy | 8 | 0.85 | 2 | **3.40** |
| 3 | Link Clean Club from the 50 pages that name it | Conv | 7 | 0.9 | 2 | **3.15** |
| 4 | Fix the `/seal-coating-piqua-ohio/` orphan + thin seal-coating interlinking | SEO | 5 | 0.9 | 1.5 | **3.00** |
| 5 | Add `/dayton-ohio/` city hub — largest metro, no hub | SEO | 7 | 0.75 | 3 | **1.75** |
| 6 | Trim 3 over-long metas + 5 over-long titles | SEO | 3 | 0.95 | 1 | **2.85** |
| 7 | Fix 3 missing alt / dimension attributes | Tech + A11y | 2 | 0.95 | 0.5 | **3.80** |
| 8 | Add `/piqua-ohio/` hub + window/soft washing for Piqua | SEO | 5 | 0.7 | 3 | **1.17** |
| 9 | Put a real photo of Anthony on the homepage | Trust | 6 | 0.8 | 4 | **1.20** |
| 10 | Install GA4 / GSC — currently flying blind on real data | Measurement | 8 | 0.9 | 3 | **2.40** |

Note #10's true impact is higher than its score suggests — every future loop is guessing
without it — but it is blocked on Anthony's accounts, so it lives in `/needs-anthony.md`.

## Shipping in Loop 1
**#1, #2, #3** — plus #6 and #7 folded in, since they are near-zero effort and touch the same files.
Together they attack the single theme the audit surfaced: **the site is well built but not
pointed at the offer ladder.**
