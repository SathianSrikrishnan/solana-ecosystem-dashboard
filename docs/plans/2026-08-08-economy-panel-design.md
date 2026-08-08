# Economy Panel Design

## Product question

The Economy section answers: **Is meaningful economic activity on Solana
growing, or are we only seeing a large number of transactions?**

The first screen needs a small group of complementary signals rather than one
opaque score. Price describes the market's current valuation. TVL describes
capital deposited in tracked DeFi protocols. Stablecoin supply describes
dollar-like liquidity available on Solana. DEX volume describes completed spot
trading activity. None is a complete measure of ecosystem health by itself.

## Approaches considered

### 1. Split-source public core — selected

Use CoinGecko's keyless public API for live SOL/USD price and DeFiLlama's free
public endpoints for Solana TVL, stablecoins, and DEX volume. This preserves
source specialization and avoids credentials or cash spend. The trade-off is
that the collector must expose independent source health and reconcile
different time grains.

### 2. DeFiLlama-only economy panel

One provider could supply all four headline values. This would simplify the
collector, but it would concentrate source risk and make the price signal less
independent from the rest of the economy panel.

### 3. Dune-first onchain reconstruction

Dune could reproduce several economy metrics with auditable SQL. It would be
more customizable, but would consume credits, add query maintenance, and delay
the bounty's useful free core. Dune remains appropriate for later diagnostic
queries when the public aggregate cannot answer a specific question.

## Metric definitions

### Live SOL price

- Metric ID: `sol_price_usd`
- Value: CoinGecko's aggregated SOL price in USD.
- Grain: live observation; source time comes from `last_updated_at`.
- Important limitation: price is market context, not evidence of network use.

### Solana DeFi TVL

- Metric ID: `solana_defi_tvl_usd`
- Value: USD value locked in Solana protocols tracked by DeFiLlama.
- Grain: latest complete UTC day, with fourteen complete daily observations.
- Important limitation: TVL methodology and protocol coverage can change;
  liquid staking and recursively used assets can complicate interpretation.

### Solana stablecoin circulating value

- Metric ID: `solana_stablecoin_value_usd`
- Value: sum of DeFiLlama's USD-valued `totalCirculatingUSD` peg buckets on
  Solana for the latest complete UTC day.
- Grain: latest complete UTC day, with fourteen complete daily observations.
- Important limitation: this is circulating token value, not payment volume or
  cash held in bank accounts.

### Solana daily DEX volume

- Metric ID: `solana_dex_volume_usd`
- Value: DeFiLlama's aggregate Solana DEX spot volume for the latest complete
  UTC day.
- Grain: latest complete UTC day, with fourteen complete daily observations.
- Important limitation: routing can touch several pools; provider adapters and
  deduplication rules determine coverage.

## Data-quality decision

On 2026-08-08, DeFiLlama's live stablecoin-chain endpoint returned about
$15.6B for its USD-pegged bucket while the latest complete historical day was
about $16.2B across USD-valued peg buckets. The difference may represent a
partial-day update, changed composition, or upstream refresh timing. Publishing
the live value beside complete-day TVL and volume would create a misleading
comparison.

Therefore TVL, stablecoins, and DEX volume all use the latest complete UTC day.
The collector enforces continuous, unique dates and rejects future or partial
observations. Live SOL price remains clearly labeled as live rather than being
mixed into the complete-day comparison.

## Architecture and failure behavior

The standard-library collector calls four bounded public endpoints: one
CoinGecko price endpoint and three DeFiLlama history/overview endpoints. Pure
parsers turn reviewed JSON into schema `0.2.0` metrics. A refresh command loads
the prior report, collects each source independently, validates the full
snapshot, and regenerates JSON, Markdown, and HTML once.

If CoinGecko fails, only SOL price becomes visibly unavailable. If one
DeFiLlama dataset fails, its metric becomes unavailable without replacing the
other economy values or breaking the whole report. Errors carry the attempted
source URL and collection time but never invent zero. Tests use saved minimal
fixtures, while one live evidence receipt proves the current endpoints still
match the expected shapes.

## Follow-on economy diagnostics

After the four headline metrics are verified, add chain fees, chain revenue,
REV, and tokenized assets as a separate diagnostic batch. Those definitions
need extra care because DeFiLlama distinguishes chain fees from application
fees and may expose RWA data through different product/API surfaces. They must
not delay or contaminate the trustworthy headline layer.
