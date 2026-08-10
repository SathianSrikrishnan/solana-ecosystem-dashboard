# Superteam bounty requirements audit

Checked: 2026-08-10
Primary source: [Superteam Canada — Develop Solana Ecosystem Auto-Updating Report & Interactive Dashboard](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard)

## Listing facts

- Mission: create a comprehensive, automatically updating report on the current
  state of the Solana ecosystem.
- Eligibility: regional listing open only to people in Canada. The listing's
  first-party metadata classifies it as human-only.
- Published: July 27, 2026.
- Deadline: `2026-08-18T03:59:59.999Z`, or **August 17, 2026 at 11:59:59 p.m.
  America/Toronto**.
- Winner announcement: September 1, 2026.
- Prize pool: 1,000 USDG — 500 first, 300 second, 200 third.
- The page showed nine submissions when checked.

All facts above come from the [official listing and its embedded first-party
listing data](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard).

## Sponsor scope mapped to current evidence

The listing says priority is given to automated extraction from Dune,
Solana ecosystem reports/sites, relevant X/Twitter accounts, Solana RPC, and
off-chain sources such as DeFiLlama and CoinGecko. These are priority signals,
not a statement that every example RPC method or source is mandatory.

| Sponsor request | Current evidence | Assessment |
|---|---|---|
| TPS, slot time, block height, epoch progress | Live metrics in `output/report.json` from direct RPC | Complete |
| Active/delinquent validator counts and stake distribution | Live counts, active/delinquent stake, top-10/top-25 share, superminority and vote-credit coverage | Strong |
| Top validators by stake | Concentration aggregates only; no ranked validator table | Partial |
| Commission tracking | Current median commission only; no validator-level or historical tracking | Partial |
| Delinquency alerts | Current delinquency measurements exist; anomaly rules do not cover validator delinquency | Partial |
| SOL price movements | Live CoinGecko spot price exists, but no price history/comparison or price-move anomaly | Partial |
| Stablecoin supply, DEX volume and REV | Live DeFiLlama series and seven-day comparisons | Complete |
| Median transaction fees | Aggregate chain fees are present, but median transaction fee is not | **Missing named metric** |
| Daily active addresses | Dune fee-payer and successful-signer cohorts are a well-defined alternative; the product correctly avoids calling wallets people | Strong |
| Tokenized-asset volumes, especially equities | Explicit unavailable state because the verified RWA source requires authentication | Honest gap, but still missing |
| Ecosystem and community news | Historical narrative exists, but no current automated news surface | **Missing named section** |
| Upcoming upgrades, including Alpenglow and SIMD-525 | Agave release cadence is live, but a current upgrade/proposal tracker is absent | **Missing named section** |
| Dune latest data | Dune queries/importers and samples exist, but the six-hour workflow does not refresh Dune; current adoption evidence is therefore not fully automatic | **Major automation gap** |
| DeFiLlama and CoinGecko | Automated no-key adapters with visible source isolation | Complete |
| Solana ecosystem sites and X/Twitter | Used in research/history and planned architecture, but not an automated current source | Partial |
| Configurable, low-maintenance refresh | Six-hour GitHub Actions schedule; independent source failures degrade visibly | Strong, except Dune and news/upgrades |
| Optional anomaly detection | Deterministic 15% review threshold covers economic series; it does not yet cover the sponsor's TPS, slot-time, validator-delinquency or SOL-price examples | Partial |
| No-key/minimal dependency preference | Python standard-library production core; Node is QA-only; authenticated sources remain optional | Excellent alignment |

Scope and examples in this table are from the [official bounty
description](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard).
Current-state assessments were checked against `README.md`,
`.github/workflows/refresh.yml`, `output/report.json`, and the release documents
on branch `codex/economy` at commit `bf683d2`.

## Required outputs and submission package

| Official requirement | Current evidence | Remaining action |
|---|---|---|
| Interactive HTML dashboard; dark theme preferred | `output/index.html` | Deploy and verify the public URL |
| Human-readable Markdown report | `output/report.md` | Include/link the sample in submission |
| Structured machine-readable JSON | `output/report.json` | Include/link the sample in submission |
| Public GitHub repository with all code | Repository URL is in `README.md` | Merge/push the release candidate and verify it is publicly visible |
| Clear README explaining setup, execution and interpretation | README has commands and product promise | Expand with prerequisites, configuration, architecture/source integration, automation, anomaly behavior and interpretation guidance |
| Brief write-up: sources, integration, automation, anomaly detection and setup | Evidence is spread across README and docs | Consolidate into README or one obvious submission document |
| Live demo/hosted dashboard | Not yet deployed | **High priority: the sponsor explicitly grants higher consideration** |

These are the exact package requirements stated on the [official
listing](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard).
The public listing does **not** enumerate the generic authenticated Superteam
submission form's individual UI fields; verify those field names and character
limits in the form before final submission.

## Judging criteria and competitive posture

The official criteria are:

1. **Comprehensiveness** — breadth and detail of Solana state coverage.
2. **Automation & Maintainability** — automatic collection/generation and ease
   of keeping the report current.
3. **Clarity & Presentation** — readable, actionable HTML, Markdown and JSON.
4. **Innovation** — novel collection, analysis or presentation, including
   anomaly detection and multi-source correlation.
5. **Technical Implementation** — code quality, documentation and setup ease.
6. **No Plagiarism** — original work.

Source: [official judging criteria](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard).

The release candidate is strongest on clarity, provenance, graceful failure,
original metric distinctions, multi-format output and the sponsor's preferred
no-key Python architecture. Its largest judging risks are not visual polish;
they are visible scope and automation gaps: no hosted demo, no automatic Dune
refresh, no current news/upgrade tracker, no median transaction fee, and
anomaly coverage that misses most sponsor-named examples.

## Recommended order before submission

1. Deploy a public demo and test the deployed refresh path.
2. Make the Dune adoption refresh automatic or label its update contract and
   freshness prominently if full automation cannot be completed safely.
3. Add median transaction fee and sponsor-named network/validator/price anomaly
   checks using deterministic thresholds and sufficient history.
4. Add a bounded current upgrades/news panel covering official sources first,
   including Alpenglow and SIMD-525; keep X optional.
5. Expand the README into the sponsor's requested setup-and-interpretation
   document and link the three sample outputs directly.
6. Only then consider lower-priority scope such as a ranked validator table,
   commission history, authenticated RWA data or model-backed prose.
