# Solana Ecosystem Report

Generated: `2026-08-30T05:27:49.650704Z`

**Current reading:** The selected Solana RPC endpoint reports healthy.

## What is happening now?

### Active stake: 436,112,641.33 SOL

Activated stake assigned to currently active vote accounts.

**Why it matters:** It shows how much voting power is currently participating.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Vote accounts are not necessarily distinct operators or organizations.

### Active validators: 684 validators

Vote accounts currently classified as active by the RPC response.

**Why it matters:** Active vote accounts show how many validators are currently participating, before considering stake concentration.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: A validator count does not describe how evenly stake is distributed.

### Latest stable Agave release age: 16.40 days

Elapsed days since the newest non-draft, non-prerelease Agave release.

**Why it matters:** Release recency is one bounded sign of maintained core software.

- Status: `ok`
- Source: Anza Agave GitHub releases / `GitHub releases; latest stable tag v4.2.1`
- Collected: `2026-08-30T05:27:48.509182Z`
- Confidence: `medium`
- Important limitation: A recent release is not automatically safe or widely adopted, and release age is not a developer-count metric.

### Stable Agave releases in 90 days: 10 releases

Non-draft, non-prerelease Agave releases published in the trailing 90 days.

**Why it matters:** Release cadence shows whether core client work is shipping publicly.

- Status: `ok`
- Source: Anza Agave GitHub releases / `GitHub releases; stable releases; trailing 90 days`
- Collected: `2026-08-30T05:27:48.509182Z`
- Confidence: `medium`
- Important limitation: Release count is not adoption, code quality, contributor count, or proof that validators upgraded.

### Alpenglow upgrade status: In development · Q3 2026 official roadmap

Current phase and expected activation window shown on Solana's official upgrade page.

**Why it matters:** It tracks the named consensus upgrade without implying that a roadmap date is guaranteed.

- Status: `ok`
- Source: Official Solana source / `Alpenglow Phase 1 - Votor`
- Collected: `2026-08-30T05:27:49.650704Z`
- Confidence: `high`
- Important limitation: Roadmap dates can move; announced development is not mainnet activation.

### Block height: 420,847,275 block

Current block height reported by the selected RPC node.

**Why it matters:** Block height is a second progress marker that helps detect a stalled or lagging data source.

- Status: `ok`
- Source: Solana JSON-RPC / `getBlockHeight`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: This is network progress, not a measure of user adoption.

### Current slot: 442,799,480 slot

Latest slot reported by the selected public RPC node.

**Why it matters:** A rising slot confirms that this observer sees the chain continuing to advance.

- Status: `ok`
- Source: Solana JSON-RPC / `getSlot`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Different RPC nodes can be a few slots apart.

### Jupiter signer and fee-payer overlap: 21,869 wallet addresses

Jupiter Swap signer addresses that were also the successful transaction fee payer on the same UTC day.

**Why it matters:** The overlap reveals how often the visible application signer also pays the transaction fee.

- Status: `stale`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-15T18:49:40.811356Z`
- Confidence: `high`
- Important limitation: This is an address intersection, not a count of people; sponsored or relayed transactions can fall outside it. Automatic refresh note: The saved Dune result is preserved but needs a fresh query execution.

### Daily unique Jupiter Swap signers: 21,869 wallet addresses

Distinct tx_signer addresses on intended swaps recorded by Dune's curated Jupiter aggregator table during the latest complete UTC day.

**Why it matters:** It shows the scale of intended swap activity through one of Solana's major application routes.

- Status: `stale`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-15T18:49:40.811356Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people, and this measures Jupiter Swap signers rather than users of a particular wallet app. Automatic refresh note: The saved Dune result is preserved but needs a fresh query execution.

### Daily unique successful fee payers: 1,932,287 wallet addresses

Distinct primary signer (fee payer) addresses on successful non-vote Solana transactions during the latest complete UTC day.

**Why it matters:** Fee payers approximate how many distinct addresses initiated successful activity and paid for execution.

- Status: `stale`
- Source: Dune / `solana.transactions / daily_unique_fee_payers.sql`
- Collected: `2026-08-15T18:49:40.811356Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people: one person or bot can control many addresses, and relayers may pay fees for others. Automatic refresh note: The saved Dune result is preserved but needs a fresh query execution.

### Daily unique successful signers: 3,500,599 wallet addresses

Distinct signer addresses on successful non-vote Solana transactions during the latest complete UTC day.

**Why it matters:** Successful signers capture a broader set of participating addresses than fee payers alone.

- Status: `stale`
- Source: Dune / `solana.transactions.signers / daily_unique_successful_signers.sql`
- Collected: `2026-08-15T18:49:40.811356Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people: one person or bot can control many addresses, and one transaction may require several signers. Automatic refresh note: The saved Dune result is preserved but needs a fresh query execution.

### Delinquent stake share: 0.00 percent

Delinquent activated stake as a share of all activated stake in this response.

**Why it matters:** Stake share is more meaningful than a raw delinquent-validator count.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: One RPC snapshot can change quickly as validators recover or fall behind.

### Delinquent stake: 21,647.81 SOL

Activated stake assigned to vote accounts currently classified as delinquent.

**Why it matters:** It sizes the voting power currently failing to participate normally.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Delinquency can be temporary and does not imply malicious behavior.

### Delinquent validators: 13 validators

Vote accounts currently classified as delinquent by the RPC response.

**Why it matters:** Delinquency is an early operational signal that part of the validator set is falling behind.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Temporary delinquency can recover and is not automatically malicious behavior.

### Epoch progress: 99.88 percent

Share of the current epoch's slots already completed.

**Why it matters:** Epoch progress provides timing context for validator rewards, stake activation, and network operations.

- Status: `ok`
- Source: Solana JSON-RPC / `getEpochInfo`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Epoch progress describes validator timing, not economic growth.

### Estimated median transaction fee: 5,000.00 lamports

One-signature base fee plus the median recent prioritization fee reported by the selected RPC node.

**Why it matters:** It provides a bounded, user-scale fee benchmark alongside aggregate chain fees.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPrioritizationFees + protocol base fee`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `medium`
- Important limitation: This is an estimate for a one-signature transaction using one RPC node's recent cache, not the median fee of every executed transaction.

### Estimated non-vote TPS: 1,210.12 transactions/second

Non-vote transactions in the latest RPC performance sample divided by sample seconds.

**Why it matters:** This is the closest live RPC measure of application and user transaction throughput.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Non-vote transactions can still include bots and automated programs.

### Non-vote TPS vs recent sample median: -7.64 percent

Latest non-vote TPS relative to the median of earlier RPC performance samples.

**Why it matters:** It detects short-run throughput drops or spikes without calling them good or bad.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `medium`
- Important limitation: The RPC sample window is short and non-vote transactions can include automation.

### Estimated slot time: 0.32 seconds

Latest performance sample duration divided by slots produced.

**Why it matters:** Slot time indicates how quickly the chain is advancing in the most recent sample.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: This is a short recent estimate and can move between samples.

### Slot time vs recent sample median: 1.60 percent

Latest estimated slot time relative to the median of earlier RPC performance samples.

**Why it matters:** It detects a short-run slowdown in chain progression.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `medium`
- Important limitation: This compares a bounded set of recent samples from one RPC endpoint.

### Estimated total TPS: 3,321.52 transactions/second

All transactions in the latest RPC performance sample divided by sample seconds.

**Why it matters:** Total throughput shows network load, but must be separated from user activity because it includes validator votes.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Includes validator votes, so it is not the same as user activity.

### Jupiter Swap seven-day return rate: 44.15 percent

Share of the day's Jupiter Swap signer addresses also seen at least once during the preceding seven complete UTC days.

**Why it matters:** Return rate distinguishes repeat use from one-time address activity.

- Status: `stale`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-15T18:49:40.811356Z`
- Confidence: `high`
- Important limitation: Returning addresses are not necessarily returning people; bots and one person using several wallets remain included. Automatic refresh note: The saved Dune result is preserved but needs a fresh query execution.

### Latest official Solana news age: 3.10 days

Elapsed days since the newest item in Solana's official RSS feed.

**Why it matters:** It keeps current ecosystem developments visible without treating social sentiment as fact.

- Status: `ok`
- Source: Official Solana source / `RSS latest item: The Token Supercycle Is Here: Solana Brings Breakpoint 2026 to London`
- Collected: `2026-08-30T05:27:49.650704Z`
- Confidence: `high`
- Important limitation: This is one official editorial feed, not a complete view of community news or sentiment.

### Median validator commission: 5.00 percent

Median advertised commission among active vote accounts with valid values.

**Why it matters:** Commission affects how staking rewards are divided between validators and delegators.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: The median does not include operating cost, MEV, or total validator profitability.

### RPC health: ok status

Health response from the selected public RPC node.

**Why it matters:** It is the first check that the dashboard's live network data path is responding normally.

- Status: `ok`
- Source: Solana JSON-RPC / `getHealth`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: This checks one public RPC endpoint, not every validator.

### SIMD-0525 shorter-slot proposal: Draft proposal status

Current status declared in the official SIMD-0525 proposal for staged shorter slots.

**Why it matters:** It tracks a sponsor-named proposal that could materially change Solana latency.

- Status: `ok`
- Source: Official Solana source / `SIMD-0525 front matter`
- Collected: `2026-08-30T05:27:49.650704Z`
- Confidence: `high`
- Important limitation: A SIMD status is not proof that code is deployed or activated on mainnet.

### SOL 24-hour price change: 0.85 percent

CoinGecko's 24-hour percentage change for SOL/USD.

**Why it matters:** It supplies a bounded price-move signal for anomaly review.

- Status: `ok`
- Source: CoinGecko / `simple/price?include_24hr_change=true`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: A price move does not explain network health or user adoption.

### SOL price: 105.01 USD

CoinGecko's aggregated market price for one SOL in USD.

**Why it matters:** Price supplies market context for SOL-denominated capital and validator economics.

- Status: `ok`
- Source: CoinGecko / `simple/price?ids=solana`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: Market price is volatile context, not evidence that network or application usage is growing.

### Solana application fees: 9,925,828.47 USD

Fees users paid covered Solana applications on the latest complete UTC day, excluding gas, stablecoin issuers, and liquid staking.

**Why it matters:** App fees show what users paid applications for covered services.

- Status: `ok`
- Source: DeFiLlama / `overview/fees/solana?dataType=dailyAppFees`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: Adapter coverage can change, and fees paid are not money retained by applications.

- 7-day average change: `+26.1%`
- Direction is not a health verdict.

### Solana application revenue: 4,480,953.73 USD

The portion of covered Solana application fees retained by protocols on the latest complete UTC day.

**Why it matters:** App revenue shows captured value under provider definitions.

- Status: `ok`
- Source: DeFiLlama / `overview/fees/solana?dataType=dailyAppRevenue`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: This is not profit; incentives, token emissions, and operating costs are separate.

- 7-day average change: `+24.1%`
- Direction is not a health verdict.

### Solana chain fees: 826,698.00 USD

Base and priority transaction fees paid to the Solana network on the latest complete UTC day, as indexed by DeFiLlama.

**Why it matters:** Chain fees show demand for scarce transaction execution.

- Status: `ok`
- Source: DeFiLlama / `summary/fees/solana?dataType=dailyFees`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: Higher fees can reflect demand, congestion, speculation, or MEV. DeFiLlama's adapter estimates base fees from transaction count although Solana's protocol fee is charged per signature.

- 7-day average change: `+23.1%`
- Direction is not a health verdict.

### Solana DeFi TVL: 5,869,684,259.00 USD

USD value locked in Solana DeFi protocols tracked by DeFiLlama on the latest complete UTC day.

**Why it matters:** TVL shows how much capital is deposited in tracked Solana DeFi protocols.

- Status: `ok`
- Source: DeFiLlama / `v2/historicalChainTvl/Solana`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: TVL depends on protocol coverage and methodology and can double-count economic exposure through composable assets.

- 7-day average change: `+13.2%`
- Direction is not a health verdict.

### Solana daily DEX volume: 1,519,983,985.31 USD

Aggregate Solana spot DEX volume tracked by DeFiLlama on the latest complete UTC day.

**Why it matters:** DEX volume shows how much spot exchange activity occurred across tracked Solana venues.

- Status: `ok`
- Source: DeFiLlama / `overview/dexs/Solana?dataType=dailyVolume`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: Routing can touch several pools, and provider adapter and deduplication coverage determine the reported total.

- 7-day average change: `+8.6%`
- Direction is not a health verdict.

### Identifiable payment volume: Not available USD

Value transferred for identifiable commerce or remittance, with a published attribution method and coverage boundary.

**Why it matters:** Payments would show use of Solana as financial settlement rather than only trading infrastructure.

- Status: `unavailable`
- Source: No approved live source / `deferred pending defensible payment attribution`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `experimental`
- Important limitation: Raw stablecoin transfers are not payments: they can include trading, bots, rebalancing, and repeated movement.

### Monthly active Solana developers: Not available developers

Developers contributing to attributable open-source Solana repositories in a month.

**Why it matters:** It would show the current size of the attributable builder base.

- Status: `unavailable`
- Source: Electric Capital Developer Report / `optional reproducible developer dataset`
- Collected: `2026-08-30T05:27:48.509182Z`
- Confidence: `experimental`
- Important limitation: Source not connected: no dependable no-key live export and repository-attribution contract has been verified.

### Tokenized real-world assets (excluding stablecoins): Not available USD

Circulating market value of tokenized real-world assets on Solana, excluding the stablecoin asset class.

**Why it matters:** This would show adoption of tokenized treasuries, equities, credit, commodities, funds, and other off-chain claims.

- Status: `unavailable`
- Source: RWA.xyz (optional adapter) / `v4 assets aggregate; Solana; exclude Stablecoins`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `experimental`
- Important limitation: Source not connected: dependable API access requires authentication. No historical article value is substituted.

### Retained Solana developers: Not available developers

Attributable Solana developers active across a defined prior and current period.

**Why it matters:** Retention would separate durable building from one-time repository activity.

- Status: `unavailable`
- Source: Electric Capital Developer Report / `optional reproducible developer dataset`
- Collected: `2026-08-30T05:27:48.509182Z`
- Confidence: `experimental`
- Important limitation: Source not connected: no dependable no-key live export and repository-attribution contract has been verified.

### Solana REV (chain fees + tracked Jito tips): 984,553.00 USD

Solana chain fees plus gross Jito MEV tips tracked by DeFiLlama for the latest complete UTC day.

**Why it matters:** REV estimates direct economic value paid for blockspace and transaction ordering.

- Status: `ok`
- Source: DeFiLlama / `dailyFees(Solana) + dailyFees(jito-mev-tips)`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: REV is not GDP, profit, or app revenue; private or non-Jito MEV may be outside coverage. Jito component: https://api.llama.fi/summary/fees/jito-mev-tips?dataType=dailyFees

- 7-day average change: `+28.8%`
- Direction is not a health verdict.

### Solana stablecoin circulating value: 16,345,475,514.00 USD

USD value of circulating stablecoins on Solana across DeFiLlama's peg buckets on the latest complete UTC day.

**Why it matters:** Stablecoin value shows the dollar-like liquidity available for trading, saving, and settlement on Solana.

- Status: `ok`
- Source: DeFiLlama / `stablecoincharts/Solana`
- Collected: `2026-08-30T05:27:42.823675Z`
- Confidence: `high`
- Important limitation: Circulating stablecoin value is not payment volume or proof that every token is backed by cash.

- 7-day average change: `+1.2%`
- Direction is not a health verdict.

### Tracked Solana DeFi categories: 45 categories

Distinct DeFiLlama categories among positive-TVL protocol records that include Solana.

**Why it matters:** Category breadth shows whether activity spans several use cases.

- Status: `ok`
- Source: DeFiLlama / `protocols; distinct category; Solana; tvl > 0`
- Collected: `2026-08-30T05:27:48.509182Z`
- Confidence: `medium`
- Important limitation: Provider category labels can change and do not measure usage, quality, or economic importance.

### Solana protocols with tracked TVL: 399 protocols

DeFiLlama protocol records that include Solana and currently report positive TVL.

**Why it matters:** It provides a reproducible lower-bound view of deployed DeFi breadth.

- Status: `ok`
- Source: DeFiLlama / `protocols; chains includes Solana; tvl > 0`
- Collected: `2026-08-30T05:27:48.509182Z`
- Confidence: `medium`
- Important limitation: This is provider coverage, not all Solana apps, active users, developer retention, or product quality.

### Stake superminority coefficient: 18 vote accounts

Minimum largest vote accounts whose combined activated stake reaches one third.

**Why it matters:** A larger value means more vote accounts are required to reach consensus-blocking stake.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: This is calculated by vote account, not verified independent operator.

### Top 10 stake share: 24.15 percent

Share of activated stake assigned to the ten largest vote accounts.

**Why it matters:** It exposes concentration hidden by the total validator count.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Vote accounts are not operators; one organization may control several accounts.

### Top 25 stake share: 39.90 percent

Share of activated stake assigned to the twenty-five largest vote accounts.

**Why it matters:** It provides a broader view of stake concentration beyond the largest validators.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: Vote accounts are not operators and ownership identity is not inferred.

### Stake with recent vote credits: 100.00 percent

Share of active stake on vote accounts whose latest epoch-credit record increased.

**Why it matters:** It checks whether active voting power shows evidence of recent vote participation.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-30T05:27:41.647932Z`
- Confidence: `high`
- Important limitation: One credit record is a bounded participation check, not a full performance history.

## Top vote accounts by activated stake

| Rank | Vote account | Stake (SOL) | Share | Commission | Status |
|---:|---|---:|---:|---:|---|
| 1 | `CcaHc2L43ZWjwCHART3oZoJvHLAe9hzT2DJNUpBzoTN1` | 16,991,835.27 | 3.90% | 7.00% | current |
| 2 | `he1iusunGwqrNtafDtLdhsUQDFvo13z9sUa36PauBtk` | 16,035,736.89 | 3.68% | 0.00% | current |
| 3 | `3N7s9zXMZ4QqvHQR15t5GNHyqc89KduzMP7423eWiD5g` | 12,393,242.27 | 2.84% | 0.00% | current |
| 4 | `CatzoSMUkTRidT5DwBxAC2pEtnwMBTpkCepHkFgZDiqb` | 11,460,006.58 | 2.63% | 5.00% | current |
| 5 | `26pV97Ce83ZQ6Kz9XT4td8tdoUFPTng8Fb8gPyc53dJx` | 9,292,131.09 | 2.13% | 7.00% | current |
| 6 | `8GbwASqdpw4dVcwbWUxbHXMrjyQx2aKkoBR5H1GJF8iD` | 9,081,212.54 | 2.08% | 0.00% | current |
| 7 | `51JBzSTU5rAM8gLAVQKgp4WoZerQcSqWC7BitBzgUNAm` | 9,001,203.78 | 2.06% | 10.00% | current |
| 8 | `CvSb7wdQAFpHuSpTYTJnX5SYH4hCfQ9VuGnqrKaKwycB` | 7,294,487.37 | 1.67% | 5.00% | current |
| 9 | `9QU2QSxhb24FUX3Tu2FpczXjpK3VYrvRudywSZaM29mF` | 7,192,557.27 | 1.65% | 7.00% | current |
| 10 | `DumiCKHVqoCQKD8roLApzR5Fit8qGV5fVQsJV9sTZk4a` | 6,585,995.53 | 1.51% | 0.00% | current |

**Important limitation:** Ranks are vote accounts, not operators; one organization may control multiple accounts and ownership is not inferred.

## How to read this

These measurements describe different parts of Solana. They do not, by themselves, prove how many humans are using the network or why activity changed.
