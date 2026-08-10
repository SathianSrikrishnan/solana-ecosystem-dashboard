# Solana RWA live-source contract

**Decision (2026-08-10): NO-GO for automated publication from RWA.xyz until
RWA.xyz grants API access and redistribution rights in writing.** Keep the
dashboard's RWA metric visibly unavailable rather than scrape the public site
or turn a dated Foundation claim into a live value.

## What is authoritative and available

RWA.xyz is the strongest source evaluated. It only admits assets for which the
blockchain is core to issuance, transfer, and settlement; its supported classes
include stablecoins, government debt, private credit, commodities,
institutional funds, stocks, and real estate. It sources qualitative data from
issuers, prices primarily from CoinGecko or issuers/networks, and quantitative
onchain data from blockchains, with manual and automated validation.
([coverage](https://docs.rwa.xyz/methodology/data-coverage),
[sourcing](https://docs.rwa.xyz/methodology/data-sourcing))

Its public Solana page currently reports, **as of 2026-08-10**, $3.76B of
distributed asset value, $125.86M of represented asset value, 333,642 RWA
holders, $3.12B of 30-day transfer volume, and 2,599 RWAs. Stablecoin figures
are displayed separately. These are useful dated evidence, not an automation
contract. ([RWA.xyz Solana](https://app.rwa.xyz/networks/solana))

The v4 API is technically suitable. Production is `https://api.rwa.xyz`; calls
use `Authorization: Bearer $RWA_API_KEY`. `GET /v4/assets` exposes
`circulating_market_value_dollar.val`, asset class, and network membership.
`GET /v4/assets/aggregates`, `/aggregates/timeseries`, and
`/aggregates/meta` provide filtered aggregation, history, and field discovery.
The documented response envelope is `results`, applied filters/sort, and
pagination. ([getting started](https://docs.rwa.xyz/api/getting-started),
[assets endpoint](https://docs.rwa.xyz/api/endpoints/assets),
[responses](https://docs.rwa.xyz/api/responses))

Freshness is adequate for a daily observatory: RWA.xyz says price and onchain
data refresh once per day at midnight UTC, while API responses are cached for
30 minutes. Missing upstream values are left blank rather than guessed.
([updates](https://docs.rwa.xyz/methodology/data-update),
[API cache](https://docs.rwa.xyz/api/getting-started))

## Why it is not safe to automate now

1. **Authentication:** direct no-key probes of `/v4/assets` and `/v4/networks`
   returned HTTP 401 on 2026-08-10, matching the documented error contract.
2. **Cost and license:** the published Free plan covers the public platform and
   one CSV download per day; Pro is $500/seat/month. Full API access plus
   redistribution and commercial-license rights are listed only under the
   custom-priced Enterprise plan. ([pricing](https://app.rwa.xyz/pricing))
3. **Public-page scraping is not a substitute:** the site terms grant personal,
   noncommercial access and restrict copying, redistribution, commercial use,
   and access used to build a similar service. The observatory is public,
   bounty-facing, and intended as a flagship brand asset, so scraping would be
   an avoidable licensing risk. ([terms, sections 2.1-2.2](https://app.rwa.xyz/terms-of-use))
4. **The aggregate query must be validated against live metadata:** public docs
   show the filter and grouping grammar, but `/aggregates/meta` is the source of
   truth for available measures and filterable fields. Guessing a query could
   double-count multi-network assets or silently mix distributed, represented,
   and stablecoin value.

No authoritative **no-key, machine-readable, definition-stable** endpoint was
found that reproduces a Solana-wide non-stablecoin RWA or tokenized-equities
aggregate. Solana Foundation's RWA page is excellent supporting narrative, but
it points to Tokens.xyz, presents localized headline values, and does not
publish a stable response schema suitable for this deterministic pipeline.
([Solana RWA overview](https://solana.com/solutions/real-world-assets))

## Implementation contract if permission is obtained

Only activate after RWA.xyz confirms API access and public redistribution for
this dashboard.

- Secret: `RWA_API_KEY` in GitHub Actions; never print or persist it.
- Discovery: fetch `GET /v4/assets/aggregates/meta` first and fail closed unless
  it confirms `network_slug`, asset-class filtering, and the exact circulating
  market-value measure.
- Target metric: **circulating market value of Solana tokenized real-world
  assets, excluding Stablecoins**. Keep distributed and represented values
  separate if that is how the API models them; do not silently add them.
- Candidate filter, subject to metadata validation: `network_slug equals
  solana` AND `asset_class_name notEquals Stablecoins`; aggregation `sum`,
  grouped by `network_id` (and asset class for the breakdown).
- Companion metrics: RWA count, holders, and trailing-30-day transfer volume;
  label addresses as addresses, not people, and transfers as transfers, not
  trades or payments.
- Cadence: once daily after 00:30 UTC. Persist collection time, upstream source
  time, applied query, raw-response hash, and a seven-day comparison series.
- Failure behavior: preserve the previous verified value with its original
  timestamp, mark it stale, and show the API/authentication error category.
- Acceptance test: reconcile the API output to the public Solana page for the
  same source date before first publication, then test stablecoin exclusion and
  multi-network asset allocation with known examples.

## Recommended bounty treatment

Keep the current honest unavailable card, but link to the dated RWA.xyz Solana
evidence and explain that licensed automation is the blocker. Do **not** use the
2026-08-10 website values as if they auto-update. For a post-bounty flagship
version, request RWA.xyz's advertised startup/student terms and explicit public
redistribution permission; if granted, the contract above can be implemented
and verified quickly without changing the deterministic architecture.
