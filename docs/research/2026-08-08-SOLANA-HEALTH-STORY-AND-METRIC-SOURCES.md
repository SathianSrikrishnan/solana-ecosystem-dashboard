# Solana health story and metric-source research

**Date:** 2026-08-08  
**Purpose:** Define the broad stories a living, beginner-readable Solana observatory should tell, and identify primary or authoritative data sources that can support them reproducibly.  
**Scope rule:** Facts below are source-backed. “Dashboard interpretation” sections are product recommendations, not facts. Source gaps are explicit rather than silently filled.

## Executive conclusion

The dashboard should answer six human questions, not expose a flat wall of blockchain statistics:

1. **Is Solana working?** — network reliability, speed, successful execution, and user cost.
2. **Are real people using it?** — active signers, successful non-vote actions, retention, and app/category mix.
3. **Is useful economic activity growing?** — stablecoin liquidity, DeFi capital, trading, app fees/revenue, and validator economic value.
4. **Is it resilient and decentralized?** — stake concentration, active/delinquent validators, client diversity, infrastructure concentration, and validator economics.
5. **Is the ecosystem compounding?** — developers, retained contributors, releases, applications, security, and upgrades.
6. **Is it becoming financial infrastructure?** — tokenized real-world assets, stablecoin settlement, identifiable payments, issuers, holders, and liquidity.

No one number is “Solana health.” High transaction counts can include validator votes; high address counts can include bots or multiple wallets per person; high trading volume can be speculative or wash activity; TVL can move with asset prices; stablecoin transfers are not automatically payments; and high fees/REV can reflect demand **or** congestion. The observatory should therefore pair each headline metric with a complementary metric and a one-sentence “what could fool you” warning.

## 1. Evidence-backed trajectory: invention to financial rails

### 2017–2020: architecture and launch

**Fact.** Solana’s official history says Anatoly Yakovenko conceived the network in 2017 around bringing distributed-system performance closer to single-node performance, with Proof of History acting as a clock before consensus. The official source supports “conceived in 2017,” not an exact corporate founding date. ([Solana, “8 Innovations,” 2019](https://solana.com/de/news/8-innovations-that-make-solana-the-first-web-scale-blockchain))

**Fact.** Solana created its genesis block and launched Mainnet Beta on March 16, 2020. By the end of 2020 the Foundation reported 350+ validators and 100+ project integrations. These are historical Foundation-reported figures without a reproducible methodology attached. ([Solana Foundation June 2020 newsletter](https://solana.com/en/news/june-newsletter); [Solana Foundation 2020 review](https://solana.com/uk/news/year-in-review-2020))

**Dashboard interpretation.** This is the “technical thesis becomes a live network” chapter. The lasting question is whether cheap, fast shared state can remain reliable and decentralized as demand grows.

### 2021: first application boom

**Fact.** The Foundation’s 2021 retrospective describes rapid DeFi/NFT expansion and reports growth from $100M to $11.4B in TVL, from 360 to 1,328 validators, and from 70 to 5,145 projects between January and December. The post does not define its project-count or TVL methodology, so these values are historical narrative evidence rather than suitable benchmark data for an automated dashboard. ([Solana Foundation December 2021 community update](https://solana.com/news/december-2021-community-update))

**Dashboard interpretation.** This is the first proof that the network could attract capital and apps. It is also why the modern dashboard needs stable definitions: “projects,” wallets, TVL, and people are different things.

### 2022: real-world experiments and reliability failures

**Fact.** The 2022 retrospective highlights Solana Pay, Solana Mobile/Saga, 2,053 active developers, and 1,911 validators, while acknowledging repeated network bugs and a renewed stability focus. ([Solana Foundation, “Solana Solstice 2022”](https://solana.com/news/solana-solstice-2022))

**Fact.** Official incident reports document a June 1, 2022 halt caused by a durable-nonce bug and a September 30, 2022 halt involving duplicate blocks and a consensus implementation bug. ([June outage report](https://solana.com/news/06-01-22-solana-mainnet-beta-outage-report-2); [September outage report](https://solana.com/news/09-30-22-solana-mainnet-beta-outage-report))

**Dashboard interpretation.** Reliability is not a footnote. “Time since a consensus-impacting incident” and incident history belong in the top-level health story.

**Source gap.** A complete account of the 2022 ecosystem contraction and the FTX/Alameda shock cannot be written honestly from Solana first-party sources alone. This note does not fill that history with advocacy or memory; a later historical essay should explicitly authorize high-quality independent sources.

### 2023: community-led recovery

**Fact.** The Foundation’s 2023 review identifies Bonk, Saga, Helium’s migration, state compression, DeFi recovery, and integrations involving Visa, Shopify, Google Cloud, and AWS as major ecosystem developments. ([Solana Foundation 2023 community review](https://solana.com/en/news/solana-solstice-2023-community-review))

**Fact.** A separate Foundation developer report estimated 2,500–3,000 monthly active open-source developers during 2023, while warning that private repositories are excluded. It explicitly recommends looking at monthly active developers, retention, experience, and growth rather than one developer count. ([2023 State of the Solana Developer Ecosystem](https://solana.com/uk/news/2023-state-of-solana-developer-ecosystem))

**Dashboard interpretation.** The recovery story is not just price: retained builders, consumer distribution, DePIN migrations, and renewed onchain use matter more.

### 2024: trading strength broadens into payments, mobile, DePIN, and institutions

**Fact.** The Foundation’s Breakpoint 2024 report groups major growth themes into institutional adoption, mobile, payments/stablecoins, and DePIN. It reported Solana stablecoin market capitalization of $3.8B, up 151% year over year, with PYUSD reaching $332M on Solana in four months. It also reported transaction-fee growth and an average transaction fee of $0.02 over the examined six-month period. ([State of Solana at Breakpoint 2024](https://solana.com/news/state-of-solana-breakpoint-2024))

**Fact.** Electric Capital’s 2024 report says Solana was the leading ecosystem for new developers in 2024, with 83% year-over-year growth. Its methodology analyzes public code repositories and acknowledges attribution and undercounting limits. ([Electric Capital 2024 Developer Report](https://www.developerreport.com/developer-report); [methodology](https://www.developerreport.com/about))

**Dashboard interpretation.** Solana’s use case expanded from predominantly crypto-native markets toward payment distribution, physical infrastructure, mobile access, and institutional assets. The dashboard should show category mix rather than presenting DEX activity as the whole ecosystem.

### 2025: reliability, application economics, and client diversity

**Fact.** The June 2025 Network Health Report said Solana had nearly 16 months of uninterrupted uptime, had released Frankendancer, and had generated more than $1B of application revenue in each of the preceding two quarters. It reported 1,295 consensus validators and a voting-power Nakamoto coefficient of 20 as of April 16, 2025. The report defines that coefficient as the minimum validators needed to reach the roughly one-third stake threshold capable of censoring or stopping consensus. ([Solana Network Health Report, June 2025](https://solana.com/de/news/network-health-report-june-2025))

**Fact.** The same report says multiple independent validator clients reduce single-software failure risk, but Agave/Jito still represented roughly 92% of stake and Firedancer/Frankendancer roughly 7% at the cited April 2025 snapshot. ([Solana Network Health Report](https://solana.com/de/news/network-health-report-june-2025))

**Dashboard interpretation.** Validator count alone is insufficient. The stronger resilience story combines uptime, stake distribution, client diversity, vote performance, infrastructure concentration, and whether validators can operate economically.

### 2026: tokenized assets, stablecoin settlement, and institutional infrastructure

**Fact.** A February 2026 Foundation ecosystem report said RWA market capitalization reached $1.71B and stablecoin transactions exceeded $650B for that month. The metrics were relayed by the Foundation and should ultimately be collected from their underlying datasets rather than scraped from prose. ([Solana Ecosystem Report: February 2026](https://solana.com/tr/news/state-of-solana-february-2026))

**Fact.** The Foundation’s June 2026 roundup said Solana RWA value crossed $3B, cumulative tokenized-stock volume passed $10B, and daily tokenized-stock volume reached $683M. The RWA figure links to RWA.xyz, making RWA.xyz the more appropriate underlying source for reproducible measurement. ([Solana Ecosystem Roundup: June 2026](https://solana.com/pl/news/solana-ecosystem-roundup-june-2026))

**Dashboard interpretation.** The current growth thesis is a convergence of crypto-native markets with stablecoin settlement, tokenized equities/funds/commodities, payments infrastructure, and deeper institutional distribution. The observatory should test that thesis with data rather than repeat it as marketing.

## 2. Recommended metric families

The following are the top five or six metrics that best tell each subsection’s story. “Tier 1” means suitable for the main dashboard if the source is reproducible; “Tier 2” means a useful drill-down or a metric still needing an adapter.

### A. Network — “Is Solana working?”

| Priority | Metric | Beginner meaning | Source and important limitation |
|---|---|---|---|
| Tier 1 | Network/RPC health | Can a normal observer reach a node that is caught up? | Public [`getHealth`](https://solana.com/docs/rpc/http/gethealth) is node-local health, not proof that the whole cluster is healthy. |
| Tier 1 | Non-vote transactions per second | How many user/application transactions are being processed now? | Public [`getRecentPerformanceSamples`](https://solana.com/docs/rpc/http/getrecentperformancesamples) exposes `numNonVoteTransactions`, total transactions, slots, and sample duration. Use non-vote, not total, for the user-activity headline. |
| Tier 1 | Slot/block time | Is the chain advancing at its expected rhythm? | Derive from recent performance samples and epoch/slot data. Fast slots do not prove transactions succeeded. |
| Tier 1 | Successful transaction rate | What share of submitted non-vote activity completed successfully? | Requires block/transaction parsing or an indexed query. RPC [`getTransaction`](https://solana.com/docs/rpc/http/gettransaction) exposes transaction status and fee, but public RPC is not a convenient historical index. |
| Tier 1 | Typical user fee | What did normal successful interactions cost? | Transaction metadata plus official fee semantics. Solana’s fee is a base fee plus optional priority fee; the base is split between burn and validator and priority fee goes to the validator. ([Solana fee docs](https://solana.com/docs/core/fees)) |
| Tier 2 | Uptime and incident-free days | Has consensus recently halted or materially degraded? | Use [Solana Status incident history/feeds](https://status.solana.com/history), with explicit status-page coverage limits. A healthy queried RPC node is not the same as uninterrupted consensus history. |

**Paired reading:** TPS with success rate; low fees with landing reliability; current RPC health with incident history.

### B. Adoption — “Are people and applications using it?”

| Priority | Metric | Beginner meaning | Source and important limitation |
|---|---|---|---|
| Tier 1 | Daily successful signers / fee payers | How many distinct addresses completed at least one successful action? | Dune or another historical index. Addresses are not people; bots and wallet rotation inflate counts. |
| Tier 1 | New vs returning signers | Is use expanding, and do users come back? | Indexed transaction history with a documented first-seen rule and lookback. “New address” is not necessarily a new human. |
| Tier 1 | Successful non-vote transactions | How much application activity actually completed? | Prefer successful, non-vote counts. Public RPC’s cumulative [`getTransactionCount`](https://solana.com/docs/rpc/http/gettransactioncount/) includes ledger transactions and is not a clean human-adoption metric. |
| Tier 1 | Active signers by app/category | Where is activity happening—trading, DeFi, payments, DePIN, gaming, NFTs, social? | Dune queries plus a versioned program-label registry. Aggregators can hide the downstream application, and one transaction can touch several programs. |
| Tier 1 | 7-day / 30-day returning-address rate | Does use persist beyond a one-off event? | Requires cohort logic in an indexer. Wallet changes and bots limit identity interpretation. |
| Tier 2 | Bot-like vs likely-human activity | How much activity has repeated machine-like patterns? | Must be a transparent heuristic panel, never a definitive “bot/person” classification. Publish features and uncertainty. |

**Paired reading:** active signers with returning rate; transaction count with success; app share with concentration; likely-human estimate with the raw unclassified total.

### C. Economy — “Is useful economic activity growing?”

| Priority | Metric | Beginner meaning | Source and important limitation |
|---|---|---|---|
| Tier 1 | Stablecoin supply on Solana | How many dollar-like assets are available for trading, saving, and settlement? | DefiLlama defines chain stablecoin market cap as total stablecoin market cap on the chain. It is liquidity/capacity, not payment volume. ([definition](https://defillama.com/data-definitions); [free API availability](https://defillama.com/docs/api)) |
| Tier 1 | DeFi TVL, plus net USD inflow when available | How much capital is deposited, and is capital entering independently of price moves? | DefiLlama defines chain TVL as summed protocol TVL; it warns TVL changes mix flows with price changes and separately defines USD inflows. ([definitions](https://defillama.com/data-definitions)) |
| Tier 1 | Spot DEX volume | How much spot exchange activity occurred? | DefiLlama defines it as the value of trades through tracked DEXs. Volume is not revenue and can be concentrated or incentive-driven. ([definition](https://defillama.com/data-definitions)) |
| Tier 1 | App fees and app revenue | What users paid apps, and what apps retained? | DefiLlama excludes stablecoins, liquid staking apps, and gas fees from these chain aggregates. “Fees” are user payments; “revenue” is the subset retained by the protocol. ([definitions](https://defillama.com/data-definitions)) |
| Tier 1 | Chain fees and REV | What users paid the base chain, and what economic value reached validators? | DefiLlama defines REV as chain fees plus MEV tips. REV is not app revenue, profit, or GDP. ([definition](https://defillama.com/data-definitions)) |
| Tier 2 | Perpetual volume/open interest | How much leveraged derivatives activity is occurring, and how much risk remains open? | DefiLlama’s metrics page defines perp volume as notional, including leverage, and open interest as outstanding notional. This can dwarf economic capital and should never be added to spot volume as equivalent value. ([metrics](https://defillama.com/metrics)) |

**Paired reading:** TVL with inflows; DEX volume with fees; app fees with retained revenue; REV with fee level and network performance.

### D. Validators and decentralization — “Can the network resist failure or control?”

| Priority | Metric | Beginner meaning | Source and important limitation |
|---|---|---|---|
| Tier 1 | Active and delinquent vote accounts | How many stake-bearing validators are voting, and how many are falling behind? | Public [`getVoteAccounts`](https://solana.com/docs/rpc/http/getvoteaccounts) returns current/delinquent accounts, activated stake, commission, last vote, and epoch credits. Vote accounts are not necessarily distinct operators. |
| Tier 1 | Nakamoto coefficient / 33.4% superminority | What is the smallest validator set whose stake could stop or censor consensus? | Derive from activated stake sorted descending. The Foundation’s definition and historical caveats are in its [2025 health report](https://solana.com/de/news/network-health-report-june-2025). Operator identity can make a validator-count calculation too optimistic. |
| Tier 1 | Top-10 / top-25 stake share | How concentrated is voting power beyond one coefficient? | Derive from `getVoteAccounts`. Display both validator identities and known operator grouping when available. |
| Tier 1 | Vote participation / delinquent stake share | Is stake actively confirming the chain? | Derive from vote-account stake and epoch credits. A raw validator count weights tiny and large validators equally; stake-weighted participation is the meaningful complement. |
| Tier 1 | Validator client diversity by stake | Would one software bug threaten most stake? | RPC [`getClusterNodes`](https://solana.com/docs/rpc/http/getclusternodes) exposes node versions but mapping versions to independently implemented clients and then to stake needs a maintained registry. The 2025 report explains why client diversity matters. |
| Tier 2 | Hosting/geographic concentration and validator economics | Are validators spread across operators/infrastructure, and can healthy operators sustain themselves? | Requires reliable IP/ASN/operator mapping and careful privacy/coverage handling. Economic health needs rewards, commission, fees, MEV/tips, voting costs, hardware, and SOL price—not revenue alone. |

**Paired reading:** count with stake share; Nakamoto coefficient with known operator grouping; client diversity with stake; revenue with estimated costs.

### E. Ecosystem and developers — “Is Solana compounding?”

| Priority | Metric | Beginner meaning | Source and important limitation |
|---|---|---|---|
| Tier 1 | Monthly active open-source developers | How many developers contributed code this month? | [Electric Capital live Solana page](https://www.developerreport.com/ecosystems/solana) and [methodology](https://www.developerreport.com/about). Public repos only; ecosystem attribution and multi-chain counting matter. |
| Tier 1 | Established/full-time developers and retention | Is experienced talent staying? | Electric Capital segments developers, but current programmatic/free access and stable export terms require verification. |
| Tier 1 | Active application/category breadth | Is growth spread across several useful categories? | Combine versioned program attribution with app activity/revenue. A project directory count is not an active-app count. |
| Tier 1 | Core releases and upgrade status | Is the protocol shipping and are validators adopting releases? | Official [Solana developer news/changelog](https://solana.com/news/category/developers), GitHub releases, SIMD status, and node versions. Announced work is not activated mainnet code. |
| Tier 1 | Security and consensus incidents | Are applications and the protocol becoming safer? | Official postmortems and Solana Status. Absence of published incidents is not proof of no exploit. Separate app exploits from consensus/network incidents. |
| Tier 2 | Hackathon submissions, funding, and new projects | Is a new pipeline forming? | Official hackathon reports can show input momentum, but submissions/funding are not retained developers, users, or product-market fit. |

**Paired reading:** monthly developers with retention; releases with deployed node adoption; app count with category activity/revenue; hackathon entries with later survival.

### F. Real-world assets and payments — “Is Solana becoming financial infrastructure?”

| Priority | Metric | Beginner meaning | Source and important limitation |
|---|---|---|---|
| Tier 1 | Non-stablecoin RWA circulating market value | What traditional economic exposure is represented on Solana? | RWA.xyz classifies by underlying exposure and calculates market data from issuer, onchain, and pricing sources. Its API requires authentication, so this is not yet a no-key core metric. ([framework](https://docs.rwa.xyz/frameworks/asset-classes); [sources](https://docs.rwa.xyz/methodology/data-sources); [authentication](https://docs.rwa.xyz/api/authentication)) |
| Tier 1 | RWA value by asset class | Is growth in Treasuries, stocks, credit, commodities, real estate, or funds? | Use RWA.xyz’s asset-class framework; do not mix stablecoins into “investable RWA” without labeling the inclusion. ([asset classes](https://docs.rwa.xyz/frameworks/asset-classes)) |
| Tier 1 | Issuer/asset breadth and concentration | Is value dependent on one issuer or becoming a diverse market? | RWA.xyz’s data model/API is appropriate but keyed. Market value spread across wrappers of the same underlying asset can overstate breadth. ([RWA.xyz quickstart](https://docs.rwa.xyz/api/quickstart)) |
| Tier 1 | RWA holders and holder concentration | Is ownership/distribution broadening? | Onchain token balances plus issuer restrictions. One holder may control many addresses; custodians may represent many customers; permissioned holders differ from public users. |
| Tier 1 | RWA transfer/trading volume and liquidity | Can assets actually move and trade, or do they merely exist? | RWA.xyz/Dune plus venue-specific data. Issuance, redemptions, internal transfers, and spot trades must be separated. High notional volume is not unique capital. |
| Tier 1 | Stablecoin supply, adjusted transfer volume, and identifiable payment volume | Is dollar settlement capacity growing, being used, and used specifically for payments? | These are **three different metrics**. DefiLlama can supply chain stablecoin market cap; Artemis defines adjusted transfer volume; characterized payments require tagged firms/flows. ([DefiLlama definition](https://defillama.com/data-definitions); [Artemis adjusted-volume methodology](https://www.artemis.ai/docs/snowflake-share/stablecoins); [payment-study methodology](https://www.stablecoin.fyi/methodology)) |

**Paired reading:** RWA market value with liquidity and concentration; stablecoin supply with adjusted transfers; adjusted transfers with identifiable payments; tokenized-stock volume with number of assets/issuers and holder breadth.

## 3. Definitions that must not be blurred

### Tokenized asset / RWA

**Fact.** RWA.xyz only tracks assets where blockchain is core to issuance, transfer, and settlement, not merely a record-keeping reference. It classifies assets by underlying economic exposure and currently includes government debt, credit, stocks, private equity/venture capital, active strategies, commodities, real estate, and stablecoins. ([methodology overview](https://docs.rwa.xyz/methodology/overview); [asset classes](https://docs.rwa.xyz/frameworks/asset-classes))

**Interpretation.** The product should use two plainly labeled totals:

- **Stablecoins on Solana** — fiat-pegged settlement/liquidity assets.
- **Other tokenized real-world assets** — Treasuries, funds, equities, credit, commodities, real estate, etc.

That avoids winning a rhetorical point by counting the same stablecoin base both as “stablecoins” and again inside an unexplained “RWA” headline.

### Stablecoin supply, transfer volume, and payments

**Fact.** DefiLlama defines stablecoin market cap on a chain as the value of stablecoins deployed there. Artemis defines its adjusted activity as deduplicated stablecoin transfers less intra-exchange transfers and MEV; it describes the goal as estimating “real” stablecoin activity. Artemis’s payment study instead uses payment-provider data plus estimates and explicitly says its firm sample is not exhaustive and may retain some duplication. ([DefiLlama definitions](https://defillama.com/data-definitions); [Artemis stablecoin schema](https://www.artemis.ai/docs/snowflake-share/stablecoins); [Artemis payment methodology](https://www.stablecoin.fyi/methodology))

**Interpretation.** Never title raw or adjusted stablecoin transfer volume “payments.” The dashboard ladder should read:

1. supply available;
2. raw transfers;
3. adjusted transfers;
4. identifiable payments by category (B2B, cards, payouts, P2P, etc.).

### Fees, revenue, and REV

**Fact.** DefiLlama defines fees as what users pay a protocol; protocol revenue as the subset retained by the protocol; app fees/revenue as chain aggregates excluding stablecoins, liquid staking, and gas fees; and REV as chain fees plus MEV tips. ([DefiLlama definitions](https://defillama.com/data-definitions))

**Fact.** Solana’s own fee documentation says each transaction has a per-signature base fee and optional prioritization fee; the base fee is split 50% burn / 50% validator, while 100% of the priority fee goes to the validator. ([Solana fee docs](https://solana.com/docs/core/fees))

**Interpretation.** Show separate cards for:

- what users paid the base chain;
- what users paid applications;
- what applications retained;
- REV reaching validators (chain fees + MEV tips).

REV should be described as validator-directed economic value, not “Solana profit,” “revenue,” or “GDP.” A spike can be demand, MEV competition, congestion, or speculation, so explain it alongside median user fee, success rate, and app/category mix.

## 4. Source feasibility for the deterministic dashboard

| Source | Authority / methodology | Access reality as of 2026-08-08 | Recommendation |
|---|---|---|---|
| Solana public JSON-RPC | First-party protocol interface; exact method schemas in official docs | No API key for the listed public endpoint, but public nodes have history/rate/availability limits | **Core.** Use for current network, performance, and vote-account metrics. Record endpoint, commitment, slot, and collection time. |
| Solana Status | Official incident/status publication | Public history plus RSS/Atom links | **Core for incident narrative**, with the caveat that published status is an operational record, not an independent uptime oracle. |
| Dune | Reproducible SQL over indexed onchain data; query definition can be public | Authentication/workspace dependency; user has an account. Queries and labels must be versioned/exported | **Optional adapter / curated snapshot** for signer cohorts, app attribution, and bot heuristics. |
| DefiLlama | Public definitions and tracked-protocol methodology | Official site says free and paid APIs exist; free endpoints are available, but premium access covers broader data/rate limits. ([API docs](https://defillama.com/docs/api); [plans](https://defillama.com/subscription)) | **Core where an explicitly tested no-key endpoint exists** (current project: TVL, stablecoin supply, DEX volume). Treat undocumented endpoint stability and coverage changes as visible failure risks. Research fees/REV endpoint access before promising them. |
| RWA.xyz | Strong issuer/onchain/pricing methodology and explicit classifications | Every v4 API request requires a Bearer token; API Tools access may require contacting RWA.xyz. ([auth docs](https://docs.rwa.xyz/api/authentication)) | **Best authoritative RWA adapter, but optional/keyed.** Do not make the no-key dashboard depend on it. A cached, dated, cited snapshot is acceptable if license/terms permit. |
| Artemis | Clear adjusted-stablecoin and payment methodology | REST metric examples require an API key; Snowflake share is authenticated. ([API endpoint docs](https://app.artemisanalytics.com/docs/api-reference/stablecoins/fetch-artemis-filtered-stablecoin-transfer-volume)) | **Optional/keyed.** Use for adjusted volume or payments only if access/cost is explicitly approved; never silently replace it with raw transfers. |
| Electric Capital Developer Report | Public-repository methodology and live ecosystem pages | Human-readable public dashboard; stable free programmatic export/API terms were not established in this research | **Curated periodic evidence**, not a high-frequency automated core metric until export terms are verified. |

## 5. Unresolved source gaps

1. **No verified no-key RWA aggregate adapter.** RWA.xyz is methodologically strong but authenticated. DefiLlama has public RWA pages and paid downloads, but this research did not establish a documented, stable, free RWA-by-chain endpoint with terms suitable for the deterministic core.
2. **No verified no-key characterized-payments feed.** Raw transfers can be queried; true payments require labeling/filtering. Artemis is methodologically clear but keyed.
3. **Fees/REV endpoint contract remains unresolved.** DefiLlama supplies precise definitions and public dashboards, but the currently documented access boundary between free and premium historical chain fee/REV data needs an adapter-level test before implementation.
4. **Validator operator, client, and hosting identities are incomplete onchain.** RPC exposes vote accounts, stake, commission, credits, nodes, and versions, but operator grouping, client mapping, ASN, and geography need external registries and careful coverage reporting.
5. **Historical successful-signers and retention need an index.** Public RPC is not a practical full-history warehouse. Dune is the current reproducible path, but queries and label versions must be preserved.
6. **Bot classification cannot be ground truth.** It should expose deterministic heuristics, an “unclassified” remainder, and sensitivity to thresholds.
7. **Application attribution is many-to-many.** Aggregators route into apps, transactions invoke multiple programs, and program ownership changes. Store a versioned label registry and show “unknown/unclassified.”
8. **The 2022 history needs independent evidence.** Primary-only research cannot fully narrate the FTX/Alameda shock; do not omit it in the eventual long-form story or pretend a first-party retrospective is complete.

## 6. Recommended implementation order

1. **Finish the six-section information architecture** using the human questions above, even where a section initially shows “source not connected.”
2. **Complete validator depth from public RPC:** active/delinquent stake, stake concentration, superminority/Nakamoto coefficient, commissions, vote credits, and cautiously labeled node/client versions.
3. **Add fee semantics before fee numbers:** separate chain fees, app fees, app revenue, and REV in the schema and beginner explanations.
4. **Prototype an RWA adapter behind an optional boundary:** request/verify RWA.xyz access and terms; otherwise publish a dated research snapshot, not a fake live card.
5. **Keep stablecoin payments as a ladder:** current supply first, then raw/adjusted transfers, then characterized payments only when a defensible source exists.
6. **Build the historical “Why now?” timeline** from launch, boom, reliability crisis, recovery, diversification, reliability/economic maturity, and 2026 tokenization/settlement—clearly labeling Foundation claims and third-party dataset dependencies.
7. **Make every trust drawer answer three sentences:** “What this measures,” “Why it matters,” and “What could fool you,” followed by source, timestamp, coverage, and calculation details.

## Bottom line

The strongest product is not “a page of Solana numbers.” It is a guided diagnostic:

> **The chain is running; people and apps are using it; capital and economic value are moving; the validator set can withstand failures; builders keep improving it; and real financial assets are beginning to settle on it.**

Each clause needs its own evidence and counter-metric. That structure lets a beginner understand the system while giving an expert enough definition, provenance, freshness, and caveats to trust—or challenge—the conclusion.
