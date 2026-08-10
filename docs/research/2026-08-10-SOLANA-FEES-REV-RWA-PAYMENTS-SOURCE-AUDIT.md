# Solana fees, REV, RWA, and payments source audit

**Audited:** 2026-08-10  
**Scope:** Solana chain fees, application fees, application revenue, real
economic value (REV), non-stablecoin tokenized real-world assets, stablecoin
transfers, and identifiable payments.  
**Evidence rule:** Primary and first-party sources only: protocol documentation,
provider documentation, provider source code, and provider APIs. Live endpoint
probes were read-only and did not use or expose credentials.

## Decision summary

| Metric | Decision | Source contract | Reason |
|---|---|---|---|
| Chain fees | **Build** | DefiLlama free `summary/fees/solana` endpoint, `dailyFees` | Documented no-key endpoint, long daily history, explicit Solana adapter methodology. |
| Application fees | **Build** | DefiLlama free `overview/fees/solana` endpoint, `dailyAppFees` | The data definition and endpoint behavior are explicit; this is not chain gas. |
| Application revenue | **Build** | Same endpoint, `dailyAppRevenue` | It is the retained subset of app fees, not user spending or chain revenue. |
| REV | **Build as a transparent derivation** | Solana chain fees plus DefiLlama `jito-mev-tips` daily fees | Matches DefiLlama's published formula, but coverage must say "tracked Jito tips," not all possible MEV. |
| Non-stablecoin RWA value | **Optional authenticated adapter** | RWA.xyz v4 assets/aggregates | Strong methodology and suitable schema, but every request contractually requires a Bearer token. |
| Gross stablecoin transfers | **Optional experimental adapter** | Artemis `STABLECOIN_TRANSFER_VOLUME` | A no-key probe works today, but the official contract requires an Enterprise API key and the metric changed meaning in July 2026. |
| Identifiable payments | **Defer as a live metric** | Provider-contributed payment data or a defensible tagged-flow dataset | No complete, no-key, continuously updated feed was verified. Raw or "payment-like" transfers are not payments. |

The no-key implementation can therefore add four economic metrics now. The
financial-rails section should keep RWA and payments in visible
"source not connected" states until authenticated access and source terms are
approved.

## Definitions that must remain separate

### Chain fees

Solana transactions have a per-signature base fee and an optional priority fee.
The base fee is split 50% burn and 50% to the validator; the priority fee goes
100% to the validator. "Chain fees" means the USD value of **base plus priority
fees paid for transactions**, not application fees and not validator profit.
([Solana fee documentation](https://solana.com/docs/core/fees))

DefiLlama's Solana adapter computes base fees as transaction count multiplied by
5,000 lamports, computes priority fees as total transaction fee less base fees,
and reports both in `dailyFees`. The adapter currently queries Allium, so the
dashboard source label must name DefiLlama and its indexed-data dependency rather
than imply a direct public-RPC calculation.
([DefiLlama Solana fee adapter](https://github.com/DefiLlama/dimension-adapters/blob/master/fees/solana.ts))

There is a material adapter caveat: Solana's protocol definition is per
**signature**, while the adapter's current SQL uses transaction count multiplied
by 5,000 lamports for its base-fee estimate. Transactions with more than one
required signature can therefore make the adapter's base/priority split differ
from a signature-count reconstruction. Treat this as a DefiLlama-defined chain
fee series and disclose the approximation.

### Application fees and application revenue

DefiLlama defines protocol fees as all fees users pay and protocol revenue as the
subset retained by the protocol rather than paid to liquidity providers. Its
chain-level **App Fees** and **App Revenue** aggregates exclude stablecoin
protocols, liquid-staking applications, and gas fees. These exclusions are part
of the metric, not missing values.
([DefiLlama data definitions](https://defillama.com/data-definitions))

Therefore:

- app fees answer "what did users pay the covered applications?";
- app revenue answers "what did those applications retain under DefiLlama's
  adapter definitions?";
- neither number includes the chain fee card;
- neither is ecosystem profit, GDP, or cash flow; and
- coverage changes when DefiLlama adds, removes, or revises protocol adapters.

### REV

DefiLlama defines **Real Economic Value** as chain fees plus MEV tips.
([DefiLlama data definitions](https://defillama.com/data-definitions#rev))
For the reproducible Solana card, use:

```text
DefiLlama Solana REV = Solana chain fees + tracked Jito MEV tips
```

The Jito MEV adapter sums transfers received by eight published Jito tip-payment
addresses and labels `dailyFees` as tips paid by users/searchers. Its methodology
allocates 96% as supply-side revenue and 4% as Jito revenue, but REV uses the
**gross tip** series, not Jito's retained 4%.
([DefiLlama Jito MEV tip adapter](https://github.com/DefiLlama/dimension-adapters/blob/master/fees/jito-mev-tips/index.ts))

This is best labeled "REV (chain fees + tracked Jito tips)." It does not prove
that every private or non-Jito MEV payment is captured, and it is not the same as
application revenue, validator profit, or network GDP.

### Non-stablecoin tokenized RWAs

RWA.xyz only includes assets for which blockchain is core to issuance, transfer,
and settlement. It combines issuer reference data, onchain transfer/holder data,
and issuer, exchange, administrator, or blockchain pricing depending on the
asset. It leaves uncertain fields blank rather than filling them speculatively.
([methodology overview](https://docs.rwa.xyz/methodology/overview),
[data sources](https://docs.rwa.xyz/methodology/data-sources))

The dashboard should define the headline as **circulating market value on
Solana, excluding the Stablecoins asset class**. RWA.xyz defines circulating
market value as the USD amount of a token in circulation. Its classifications
include stablecoins, government debt, private credit, commodities, funds,
stocks, and real estate, so the exclusion prevents stablecoins from being
counted once as settlement assets and again in the RWA headline.
([RWA.xyz measures](https://docs.rwa.xyz/schemas/measures),
[coverage and classification](https://docs.rwa.xyz/methodology/data-coverage))

### Stablecoin transfers versus identifiable payments

Artemis changed its REST and Terminal stablecoin transfer metric in July 2026.
It now reports **gross transfers**, excluding only mints and burns. The older
deduplicated series that removed intra-exchange activity and MEV is being
sunset, while field names remain unchanged. A value can therefore change meaning
without the field name changing.
([Artemis July 2026 methodology](https://www.artemis.ai/docs/data-reference/stablecoin-methodology))

Gross transfers can include exchange rebalancing, trading, multi-leg program
execution, bots, and repeated movement of the same dollar. They must never be
titled "payments."

The Artemis/Castle Island bottom-up payments study instead aggregates data from
payment providers and supplements it with onchain estimates. It targets card,
B2C, B2B, P2P, and lending-to-payment-provider activity; acknowledges possible
duplication; covers only a subset of firms; and is not exhaustive. That is a
defensible research estimate, not a complete live chain feed.
([stablecoin payment-study methodology](https://www.stablecoin.fyi/methodology))

## Live endpoint audit

All values below are endpoint observations, not recommendations to publish the
sample figures. Production should select the latest **complete UTC day** and
record collection time, URL, data type, and coverage definition.

### DefiLlama: fees and revenue

DefiLlama documents separate Free and Pro APIs. The Free API uses
`https://api.llama.fi`, requires no authentication, has a "standard" rate limit
without a published numeric quota, and explicitly lists fee/revenue overview and
summary routes among the free endpoints. Historical chart-only v2 endpoints are
Pro, but the free overview/summary responses presently include
`totalDataChart`.
([DefiLlama API documentation](https://api-docs.defillama.com/),
[official SDK fee module](https://github.com/DefiLlama/api-sdk#fees))

Read-only probes on 2026-08-10 returned HTTP 200 without authentication:

| Metric | Request | Relevant response shape | Latest complete point observed |
|---|---|---|---|
| Chain fees | [`GET /summary/fees/solana?dataType=dailyFees`](https://api.llama.fi/summary/fees/solana?dataType=dailyFees) | metadata plus `totalDataChart: [[unix_seconds, usd_number], ...]`, totals, and optional breakdown | 2026-08-09: $650,664 |
| App fees | [`GET /overview/fees/solana?...&dataType=dailyAppFees`](https://api.llama.fi/overview/fees/solana?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=true&dataType=dailyAppFees) | `totalDataChart`, period totals, changes; `protocols` was empty for this aggregate data type | 2026-08-09: $8,376,941.66 |
| App revenue | [`GET /overview/fees/solana?...&dataType=dailyAppRevenue`](https://api.llama.fi/overview/fees/solana?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=true&dataType=dailyAppRevenue) | same aggregate shape | 2026-08-09: $3,887,791.90 |
| Jito MEV tips | [`GET /summary/fees/jito-mev-tips?dataType=dailyFees`](https://api.llama.fi/summary/fees/jito-mev-tips?dataType=dailyFees) | protocol metadata plus `totalDataChart` and methodology | 2026-08-09: $135,394 |
| Derived REV | two preceding component series | join on UTC timestamp, then add | 2026-08-09: $786,058 |

The endpoint included a partial 2026-08-10 point for some series, confirming that
using `total24h` or the final array element blindly can mix incomplete windows.
The collector should choose the newest timestamp strictly before the current UTC
date, require both REV components on the same date, and degrade REV visibly if
either component is missing.

Additional probe findings:

- No rate-limit headers were returned; implement conservative request pacing and
  cache the daily result.
- Unsupported `dailyREV`, `dailyRev`, `dailyChainFees`, and
  `dailyChainRevenue` data types returned HTTP 500. Do not rely on an invented
  REV data type.
- The response carries adapter methodology and protocol metadata. Preserve a
  concise definition in the metric contract and link the exact endpoint plus
  source adapter.
- Use decimal numbers until final display formatting; do not round component
  series before deriving REV.

### RWA.xyz: authoritative but authenticated

RWA.xyz v4 uses `https://api.rwa.xyz`. Every request requires
`Authorization: Bearer ...`; an unauthenticated `GET /v4/assets` probe returned
HTTP 401 with `{"message":"Authorization header missing..."}`. API Tools access
may itself require contacting RWA.xyz.
([authentication](https://docs.rwa.xyz/api/authentication),
[getting started](https://docs.rwa.xyz/api/getting-started))

The useful routes are:

- `GET /v4/assets` for asset classification, issuer, network, and current
  measures;
- `GET /v4/assets/aggregates` for grouped sums; and
- `GET /v4/assets/aggregates/timeseries` for stock/flow histories.

Requests use a URL-encoded JSON `query` object with filters, sorting,
pagination, and aggregation. Successful list responses contain `results`, the
applied `filter` and `sort`, and a `pagination` object. Asset records include
`asset_class_name`, `issuer_name`, `network_names`, and market-value measure
objects; aggregate queries can group by network, asset class, protocol, or date.
([assets endpoints](https://docs.rwa.xyz/api/endpoints/assets),
[request format](https://docs.rwa.xyz/api/requests),
[response format](https://docs.rwa.xyz/api/responses),
[asset schema](https://docs.rwa.xyz/schemas/assets))

RWA.xyz documents 30-minute response caching but does not publish a free/no-key
contract. Build this only as an optional adapter after key access, cost, terms,
and the exact Solana/non-stablecoin aggregate query have been tested. Until
then, a dated manually reviewed research snapshot can support prose, but should
not masquerade as a live card.

DefiLlama has a public human-readable
[Solana RWA page](https://defillama.com/rwa/chain/solana), but its documented
Free API does not list an RWA route and its "active" versus "onchain" market-cap
definitions were not established in this audit. Use it only as a cross-check,
not as an undocumented scraper dependency.

### Artemis: gross stablecoin transfer volume

The documented route is:

```text
GET https://data-svc.artemisxyz.com/data/api/STABLECOIN_TRANSFER_VOLUME
    ?symbols=sol
    &startDate=YYYY-MM-DD
    &endDate=YYYY-MM-DD
    &granularity=DAY
```

Its documented response is:

```json
{
  "data": {
    "symbols": {
      "sol": {
        "STABLECOIN_TRANSFER_VOLUME": [
          {"date": "2026-08-01", "val": 5398226672.518321}
        ]
      }
    }
  }
}
```

([Artemis stablecoin transfer endpoint](https://www.artemis.ai/docs/api-reference/stablecoins/fetch-stablecoin-transfer-volume-unfiltered))

The official reference marks `APIKey` required, and the account documentation
says API keys are available to Enterprise customers. Nevertheless, a read-only
request without `APIKey` returned HTTP 200 on 2026-08-10 and the response shape
above; it returned no numeric rate-limit headers.
([Artemis API-key documentation](https://www.artemis.ai/docs/artemis-api/api-key))

That mismatch makes unauthenticated access observed behavior, not a dependable
contract. If used before authenticated access is approved, isolate it as an
experimental optional adapter with a visible failure state. Label it **gross
stablecoin transfer volume**, pin the July 2026 methodology in the metric note,
and never silently substitute the retired adjusted series.

### Dune: reproducible raw transfers, not no-key payments

Dune's public `tokens_solana.transfers` table covers SPL, Token-2022, and native
SOL transfers and exposes transfer amounts, USD values, owners, mint addresses,
transaction IDs, and executing programs. Filtering a versioned stablecoin mint
registry can create a transparent **raw** stablecoin transfer series.
([Solana token-transfer table](https://docs.dune.com/data-catalog/curated/token-transfers/solana/solana-token-transfers))

However, Dune's purpose-built stablecoin foundation and activity-enriched tables
are now gated. The enriched Solana table classifies DEX, lending, bridge,
internal, and "payment-like" flows, but Dune itself describes transfer intent as
ambiguous and requires entitlement. "Payment-like" is still not provider-
confirmed payment volume.
([Dune stablecoin collection](https://docs.dune.com/data-catalog/curated/stablecoins/overview),
[Solana activity-enriched table](https://docs.dune.com/data-catalog/curated/stablecoins/activity-enriched/stablecoins-solana-activity-enriched))

Programmatic query execution requires an API key and consumes credits. Responses
are asynchronous execution objects followed by result retrieval; keys must not
appear in reports, screenshots, or URLs.
([Dune authentication](https://docs.dune.com/api-reference/overview/authentication),
[execute-query contract](https://docs.dune.com/api-reference/executions/endpoint/execute-query))

Recommendation: Dune remains a good optional, version-controlled path for raw
transfers and bespoke tag-based research, but it does not solve the no-key or
identifiable-payment requirements.

## Implementation contract for the next dashboard batch

### Build now

1. Add four metric IDs with daily USD values and fourteen complete UTC days of
   history:
   - `solana_chain_fees_usd`
   - `solana_app_fees_usd`
   - `solana_app_revenue_usd`
   - `solana_rev_usd`
2. Fetch the two overview series and two summary series above.
3. Select complete days only and align REV components by Unix UTC date.
4. Derive REV from unrounded chain fees plus gross tracked Jito tips.
5. Record both REV component URLs, the formula, collection timestamp, date
   window, and source limitation.
6. Fail each metric independently; a missing Jito series should make REV
   unavailable, not collapse the full report.

Suggested beginner copy:

| Card | What this measures | What could fool you |
|---|---|---|
| Chain fees | What users paid the Solana network in base and priority fees. | Higher fees can mean stronger demand, congestion, speculation, or MEV competition. |
| App fees | What users paid covered Solana applications, excluding gas, stablecoin issuers, and liquid staking. | Adapter coverage changes, and fees paid are not money retained. |
| App revenue | The portion of covered app fees retained by protocols. | It is not profit; incentives, operating costs, and token emissions are separate. |
| REV | Chain fees plus tracked Jito MEV tips. | It is not GDP or profit, and non-Jito/private MEV may be outside coverage. |

### Keep optional or deferred

- **RWA adapter:** optional, keyed, and disabled by default. Require
  `RWA_API_KEY`, never log it, and display the authentication failure explicitly.
- **Gross stablecoin transfers:** optional/experimental unless Artemis confirms
  a supported no-key contract. Keep the existing stablecoin-supply card as the
  reliable no-key core.
- **Identifiable payments:** defer until there is either provider-contributed
  data with repeatable publication or an approved tagged dataset with a coverage
  denominator, label version, and unclassified remainder.

## Acceptance checks

- Dashboard copy never uses "fees," "revenue," "REV," "stablecoin transfers," or
  "payments" interchangeably.
- Latest values are for a named complete UTC day, not a rolling or partial day.
- `app_revenue <= app_fees` is monitored as a sanity check, not assumed as proof
  of correctness.
- `REV == chain_fees + tracked_jito_tips` within decimal precision for every
  published day.
- Authenticated/optional failures render as unavailable and preserve the rest of
  the report.
- Every metric shows definition, source URL, collection time, coverage, and a
  one-sentence limitation.

## Bottom line

The economic panel can become meaningfully deeper without a paid dependency:
chain fees, app fees, app revenue, and a transparent DefiLlama-style REV
derivation are buildable now. Stablecoin transfer volume is accessible today but
not contractually no-key and recently changed meaning. Non-stablecoin RWA value
has a high-quality authenticated source. True payment volume remains the hardest
metric because it requires offchain business context or defensible attribution,
not merely a large onchain transfer count.
