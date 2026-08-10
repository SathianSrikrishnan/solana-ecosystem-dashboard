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
repeatable Axe accessibility test.

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
```

Open `output/index.html` after the refresh completes.

## Data integration

| Source | What it supplies | Access and failure behavior |
|---|---|---|
| Solana JSON-RPC | health, slots, blocks, epoch, TPS, slot time, recent fees, validators and stake | Public/no-key; refreshed first |
| Dune | successful fee payers/signers, Jupiter signers, overlap and return rate | Optional `DUNE_API_KEY`; last verified data is preserved when absent |
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
3. refreshes Dune data when `DUNE_API_KEY` is configured;
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

The workflow retrieves the latest stored results; executing the queries on Dune
can consume credits and remains a separate, explicitly approved schedule.

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

## How to interpret it

Start with the six overview questions. A green reporting badge means the source
returned valid data; it is not a verdict that Solana is healthy. Follow any
movement into its evidence drawer and read the definition and limitation before
drawing a conclusion. The deterministic briefing may summarize validated
records but cannot identify causes.

## Known boundaries

- Dune auto-refresh needs a secret; the public no-key core remains usable.
- RWA.xyz requires authenticated access, so tokenized-asset value is not
  backfilled from press releases. This is especially important because RWAs and
  tokenized equities are central to the financial-rails thesis.
- Raw stablecoin transfer volume is not presented as payment volume.
- Official news is one editorial feed, not total community sentiment.

For architecture and research, see [the big-picture map](docs/BIG-PICTURE-MAP.md),
[metric registry](docs/METRIC-REGISTRY.md), [release checklist](docs/RELEASE-CHECKLIST.md),
and [official bounty audit](docs/research/2026-08-10-SUPERTEAM-BOUNTY-REQUIREMENTS-AUDIT.md).
