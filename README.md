# Solana Observatory

Live dashboard: https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/

A trustworthy, automatically updating view of Solana's network health,
adoption, economics, validators, ecosystem changes, and financial rails.

Built for the [Superteam Canada Solana Ecosystem Auto-Updating Report &
Interactive Dashboard bounty](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard).

## What it publishes

- [`output/index.html`](output/index.html): standalone dark interactive dashboard
- [`output/report.md`](output/report.md): human-readable report
- [`output/report.json`](output/report.json): structured facts and provenance

The same validated snapshot drives all three formats. Every metric carries its
definition, source, collection time, confidence, and a limitation. Wallets are
not labeled as people, raw transfers are not labeled as payments, and a source
failure remains visible instead of becoming zero.

## Run it locally

Python 3.11+ is the only production dependency. Node is used only for the
repeatable Axe accessibility and visual QA checks.

```powershell
# Source / context:
# Solana Observatory local refresh and verification

cd "C:\Users\sathi\Projects\solana-ecosystem-dashboard"

# Commands:
python -m unittest discover -s tests -v
python scripts\generate.py
python scripts\refresh_economy.py --snapshot output\report.json --output output
python scripts\refresh_ecosystem.py --snapshot output\report.json --output output
python scripts\refresh_updates.py --snapshot output\report.json --output output
python scripts\refresh_dune.py --snapshot output\report.json --output output
npm ci
npm run test:a11y
npm run test:visual
```

Open `output/index.html` after the refresh completes.

## Data integration

| Source | What it supplies | Access and failure behavior |
|---|---|---|
| Solana JSON-RPC | health, slots, blocks, epoch, TPS, slot time, recent fees, validators and stake | Public/no-key; refreshed first |
| Dune | successful fee payers/signers, Jupiter signers, overlap and return rate | Optional `DUNE_API_KEY`; stale stored results are labeled instead of presented as current |
| DeFiLlama | TVL, stablecoins, DEX volume, chain/app fees, app revenue and tracked Jito tips | Public/no-key; sources fail independently |
| CoinGecko | SOL price and 24-hour movement | Public/no-key; bounded request |
| Solana RSS and upgrade pages | current official news, Alpenglow roadmap | Public/no-key; editorial source is explicitly labeled |
| Solana SIMD repository | SIMD-0525 proposal status | Public/no-key; proposal status is not deployment status |
| RWA.xyz | non-stablecoin tokenized-asset value | Optional authenticated adapter remains a documented gap |

The production collectors use Python's standard library. Authenticated sources
are optional and never silently become required for the dashboard to publish.

## Automation

`.github/workflows/refresh.yml` runs every six hours and can also be started
manually. It:

1. runs the Python tests;
2. refreshes RPC, economy, ecosystem, official-news and upgrade data;
3. attempts a Dune stored-result refresh when `DUNE_API_KEY` is configured and
   visibly marks only those metrics stale when freshness validation fails;
4. runs desktop and mobile Axe checks;
5. commits changed report outputs.

`.github/workflows/pages.yml` deploys `output/` to GitHub Pages after changes
reach `main`. Concurrency guards prevent overlapping refreshes and deployments.

The Dune API requires authentication. Configure it without exposing the value:

```powershell
# Source / context:
# Optional automatic Dune result refresh

cd "C:\Users\sathi\Projects\solana-ecosystem-dashboard"

# Commands:
gh secret set DUNE_API_KEY
```

The repository secret is configured. The workflow retrieves the latest stored
results, but those results currently end on 2026-08-07 and do not satisfy the
latest-complete-day contract. Executing the queries can consume Dune credits
and remains a separate, explicitly approved action after billing caps are set.

## Anomaly detection

Deterministic rules flag evidence for review without calling movement good or
bad. Four sponsor-named operational checks cover:

- non-vote TPS versus the median of recent RPC samples (25%);
- slot time versus the median of recent RPC samples (20%);
- delinquent stake share (5%);
- SOL's 24-hour price move (10%).

Fourteen-day economic series also compare the latest seven complete UTC days
with the preceding seven and flag absolute movement of at least 15%. Thresholds
are code-visible, tests cover both sides, and insufficient evidence is reported
as unavailable rather than anomalous.

The overview exposes the review queue, and supported metric series include
compact accessible sparklines. Validators include a live top-ten vote-account
table alongside concentration, delinquency, commission, and superminority
measurements. Vote accounts are ranked without claiming they are distinct
operators.

## How to interpret it

Start with the six overview questions. A green reporting badge means the source
returned valid data; it is not a verdict that Solana is healthy. Follow any
movement into its evidence drawer and read the definition and limitation before
drawing a conclusion. The deterministic briefing may summarize validated
records but cannot identify causes.

## Known boundaries

- Dune authentication is configured, but fresh query execution is credit-gated;
  stale results are preserved as evidence and visibly labeled.
- RWA.xyz's no-key API returns unauthorized, and full API plus redistribution
  rights require an enterprise agreement. Tokenized-asset value is therefore
  not scraped or backfilled from press releases.
- Raw stablecoin transfer volume is not presented as payment volume.
- Official news is one editorial feed, not total community sentiment.

For architecture and research, see [the big-picture map](docs/BIG-PICTURE-MAP.md),
[metric registry](docs/METRIC-REGISTRY.md), [release checklist](docs/RELEASE-CHECKLIST.md),
and [official bounty audit](docs/research/2026-08-10-SUPERTEAM-BOUNTY-REQUIREMENTS-AUDIT.md).
