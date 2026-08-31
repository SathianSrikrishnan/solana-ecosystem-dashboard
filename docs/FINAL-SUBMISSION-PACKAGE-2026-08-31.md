# Solana Observatory — final submission package

Prepared: 2026-08-31  
Status: ready for final live-link check and owner-authorized form submission

## Recommended title

**Solana Observatory: A Living, Source-Visible Ecosystem Dashboard**

## Submission copy

Solana Observatory is an automatically refreshed, beginner-readable view of the Solana ecosystem. Instead of collapsing the network into one score, it answers six questions: Is Solana working? Are addresses and apps returning? Is useful activity growing? Is the validator set resilient? Is the ecosystem compounding? Are real financial rails emerging?

The reviewed snapshot contains 45 source-carrying records across network health, adoption, economics, validators, ecosystem activity, and financial rails. Collectors use Solana RPC, Dune, DeFiLlama, CoinGecko, GitHub, and official ecosystem sources. Every record preserves its source, collection time, definition, units, confidence, limitation, and failure state. A six-hour workflow validates one evidence contract and publishes the same snapshot as interactive HTML, readable Markdown, and machine-readable JSON. Deterministic anomaly rules flag material changes without asking AI to invent or backfill data.

The public project page includes a three-minute walkthrough, the live dashboard, generated outputs, and repository. Missing evidence remains visible: the August 30 snapshot reports 36 current records, five stale records, and four unavailable records rather than silently treating gaps as zero.

## Public links

- Project and walkthrough: https://sathian.ai/projects/solana-observatory
- Live dashboard: https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/
- Repository and setup: https://github.com/SathianSrikrishnan/solana-ecosystem-dashboard
- Markdown report: https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/report.md
- JSON report: https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/report.json

## Judging proof

| Criterion | Strongest proof |
|---|---|
| Comprehensiveness | Six product questions and 45 source-carrying records across all required layers |
| Automation and maintainability | Six-hour refresh, independent collector failure handling, one normalized evidence contract, automated Pages publication |
| Clarity and presentation | Newcomer-first dashboard, three-minute walkthrough, evidence drawers, Markdown and JSON companions |
| Innovation | Deterministic anomaly review, explicit stale/unavailable states, no opaque aggregate score |
| Technical implementation | 130 Python tests, browser/accessibility checks, public source code, reproducible outputs |
| Originality | An evidence-first observatory organized around questions rather than a wall of metrics |

## Honest limitations

- The reviewed snapshot contains five stale and four unavailable records. Their visible state is part of the trust model, but judges may still reward a competitor with broader live coverage.
- Dune-backed adoption records require the optional authenticated adapter; the no-key core continues without them.
- Automated social/news sentiment is not presented as a verified metric. Official ecosystem and release sources are used instead.
- This is the more competitive of the two entries. Do not hide the gaps; make the evidence contract and graceful degradation the differentiator.

## Action-time checklist

1. Open every public link above in a signed-out browser.
2. Confirm the latest GitHub Actions refresh and Pages deployment are green.
3. Confirm the Superteam form still accepts submissions and re-read its required fields.
4. Paste the title and submission copy without adding unsupported claims.
5. Attach the project page as the demo and the GitHub repository as the code proof.
6. Take a receipt screenshot before submitting.
7. Submit only after Sathian gives action-time approval.

