# Superteam submission draft

Status: final candidate. The current automated refresh and GitHub Pages deployment are green, the 3:03 demo is owner-approved, and its public project URL is prepared. Action-time submission approval remains.

- Live dashboard: https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/
- Social cover: https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/solana-observatory-cover.png
- One-page guide: https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/solana-six-question-map.png
- Public repository: https://github.com/SathianSrikrishnan/solana-ecosystem-dashboard
- Public project and walkthrough: https://sathian.ai/projects/solana-observatory
- Official bounty: https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard

## One-line pitch

Solana Observatory is a living, source-visible dashboard that explains whether
Solana is working, attracting durable use, producing economic value, remaining
decentralized, compounding its ecosystem, and becoming financial infrastructure.

It stands alone as the dashboard submission. [Inside MonkeDAO](https://sathian.ai/writings/inside-monkedao)
is optional supporting fieldwork: the Observatory is the system view; the field
report is the community view.

## Short description

Most ecosystem dashboards show many numbers but leave newcomers to decide what
they mean. Solana Observatory combines direct RPC data, Dune adoption cohorts,
DeFiLlama economic measurements, validator stake analysis, application breadth,
and release signals in one automatically refreshed report. Every metric exposes
its definition, source, freshness, confidence, and limitation. Wallets are not
called people; transfers are not called payments; missing evidence stays visible.

## What is original

- Six product questions instead of one opaque health score.
- Separate measurements for fee payers, successful signers, Jupiter users,
  returning addresses, app fees, app revenue, chain fees, and REV.
- Deterministic anomaly detection and evidence-bound plain-English briefing.
- Exact values and provenance in JSON, Markdown, and interactive HTML generated
  from one validated contract.
- Honest degradation: one failed source cannot blank or silently corrupt the report.

## Proof against the brief

| Requirement | Public proof |
|---|---|
| Auto-updating | Six-hour workflow, independently degrading collectors, visible freshness |
| Interactive | Hosted dashboard with navigation, evidence drawers, sparklines and validator table |
| Comprehensive | Network, adoption, economy, validators, ecosystem and financial rails |
| Explainable | Definition, source, collection time, confidence and limitation per metric |
| Reproducible | JSON, Markdown and HTML generated from the same validated snapshot |
| Beginner-readable | Start Here path plus a shareable six-question system map |

## Reproducibility

```powershell
# Source / context:
# Solana Observatory clean local verification

cd "C:\path\to\solana-ecosystem-dashboard"

# Commands:
python -m unittest discover -s tests -v
python scripts\generate.py
python scripts\refresh_economy.py --snapshot output\report.json --output output
python scripts\refresh_ecosystem.py --snapshot output\report.json --output output
npm ci
npx playwright install chromium
npm run test:a11y
```

## Demo

Use [`DEMO-SCRIPT-3-MINUTE.md`](DEMO-SCRIPT-3-MINUTE.md) for the 3:03 product
walkthrough. The owner-approved cut combines the live dashboard sequence with
Sathian's complete narration and a small presenter window. It covers the six
product questions, all six dashboard layers, the evidence contract, honest
source degradation, and the automated output pipeline without opening private
tabs or exposing credentials. The public walkthrough is embedded at
https://sathian.ai/projects/solana-observatory.

## Current proof snapshot

- 45 source-carrying records: 36 current, five visibly stale, four unavailable.
- 130 Python tests pass on the current merged submission branch.
- Social, companion-page, refresh-control, WCAG A/AA, and desktop/mobile visual checks pass.
- The latest public refresh and GitHub Pages deployment completed successfully on 2026-08-30.

## Final fields still needed

- Recommended byline: **Sathian Srikrishnan**.
- Recommended builder bio, pending Sathian's approval: **Sathian Srikrishnan is
  a Toronto builder learning in public at the intersection of AI, programmable
  payments, and family-focused products on Solana.**
- Action-time approval to submit the bounty.
