# Metric Registry

Every production metric must define these fields:

| Field | Meaning |
|---|---|
| `id` | Stable machine name |
| `section` | Dashboard area: network, adoption, economy, validators, or ecosystem |
| `label` | Human-readable name |
| `value` | Current measured value |
| `unit` | Unit such as TPS, USD, count, or percent |
| `definition` | Exactly what is counted |
| `source` | Originating system and query or endpoint |
| `collected_at` | When our collector obtained it |
| `source_time` | When the underlying observation occurred, if known |
| `status` | `ok`, `stale`, `unavailable`, or `error` |
| `confidence` | `high`, `medium`, or `experimental` |
| `caveat` | Important limitation in plain English |
| `series` | Optional historical points using `observed_at` and `value` |

The dictionary key must equal `id`. A missing observation uses `null` plus a
visible non-`ok` status; collectors must not invent zeroes. This is schema
version `0.2.0`, shared by collectors, JSON, Markdown, and the interface.

## First metrics

- RPC health
- current slot
- block height
- epoch progress
- recent estimated TPS
- recent estimated slot time
- current and delinquent validator counts

## Adoption metric: daily unique successful fee payers

- `id`: `daily_unique_successful_fee_payers`
- Definition: distinct primary signer (fee payer) addresses on successful
  non-vote Solana transactions during the latest complete UTC day.
- Source: Dune `solana.transactions`, implemented in
  `queries/daily_unique_fee_payers.sql` and published at
  <https://dune.com/queries/8213434>.
- Window: the latest seven complete UTC days; the newest day is the displayed
  value and all seven observations remain in `series`.
- Limitation: addresses are not people. One person or bot may control several
  addresses, and relayers may pay transaction fees for others.
- Collection path: manual CSV export plus the standard-library importer. This
  keeps the core usable without an API key and makes source failure explicit.

## Later metric family: activity identities

- transaction sender wallets;
- successful transaction signer wallets;
- wallets using a selected application;
- likely automated wallets;
- likely human-controlled wallets.

These are related measurements, not interchangeable truths.

## Adoption metric: daily unique successful signers

- `id`: `daily_unique_successful_signers`
- Definition: distinct signer addresses on successful non-vote Solana
  transactions during the latest complete UTC day.
- Source: Dune `solana.transactions.signers`, implemented in
  `queries/daily_unique_successful_signers.sql` and published at
  <https://dune.com/queries/8264418>.
- Window: the latest seven complete UTC days; the newest day is the displayed
  value and all seven observations remain in `series`.
- Relationship: successful signers include fee payers and may also include
  co-signers, so the signer count must not be below the matching fee-payer
  count.
- Limitation: addresses are not people. One person or bot may control several
  addresses, and one transaction may require several signers.
- Collection path: manual CSV export plus the standard-library importer. The
  no-key report remains usable without a Dune API credential.

## Jupiter Swap adoption metrics

The public query <https://dune.com/queries/8264526> uses Dune's curated
[`jupiter_solana.aggregator_swaps`](https://docs.dune.com/data-catalog/curated/dex-trades/solana/jupiter-aggregator-trades)
table. Dune documents one row as a user's intended aggregator swap and exposes
the UTC `block_time` and transaction `tx_signer`. The query also joins
`solana.transactions` for an exact same-day fee-payer address intersection.

- `daily_unique_jupiter_swap_signers`: distinct `tx_signer` addresses on
  curated Jupiter aggregator swaps during the latest complete UTC day.
- `daily_jupiter_fee_payer_overlap`: those Jupiter Swap signer addresses that
  were also the successful transaction fee payer on the same day.
- `jupiter_swap_signer_7d_return_rate`: the share of the day's Jupiter Swap
  signers also seen at least once during the preceding seven complete UTC days.
- Window: fourteen complete days are read to calculate retention; only the
  latest seven complete days are published.
- Limitations: these are wallet addresses, not people. The curated table
  measures Jupiter Swap activity, not use of Jupiter Wallet, Phantom, or
  Solflare. Bots and several wallets controlled by one person remain included.

## Economy metrics

The no-key economy core uses one live market reading and three latest-complete-
day onchain market readings. The different time grains remain explicit.

- `sol_price_usd`: CoinGecko's aggregated USD market price for one SOL. It is
  live context, not evidence of network or application usage.
- `solana_defi_tvl_usd`: USD value locked in Solana DeFi protocols tracked by
  DeFiLlama. Coverage and composability can affect or double-count exposure.
- `solana_stablecoin_value_usd`: the sum of DeFiLlama's USD-valued peg buckets
  circulating on Solana. It is not payment volume or proof of backing.
- `solana_dex_volume_usd`: aggregate Solana spot DEX volume tracked by
  DeFiLlama. Adapter coverage, routing, and deduplication affect the total.
- Window: TVL, stablecoin value, and DEX volume retain fourteen complete UTC
  days. Provider rows for the current partial UTC day are deliberately ignored.
- Failure behavior: every endpoint is collected and normalized independently.
  A failed source produces a `null`, visibly `unavailable` metric while the
  other economy metrics continue reporting.
