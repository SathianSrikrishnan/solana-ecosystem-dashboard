# Solana Ecosystem Report

Generated: `2026-08-10T11:18:12.204135Z`

**Current reading:** The selected Solana RPC endpoint reports healthy.

## What is happening now?

### Active stake: 434,005,084.36 SOL

Activated stake assigned to currently active vote accounts.

**Why it matters:** It shows how much voting power is currently participating.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Vote accounts are not necessarily distinct operators or organizations.

### Active validators: 689 validators

Vote accounts currently classified as active by the RPC response.

**Why it matters:** Active vote accounts show how many validators are currently participating, before considering stake concentration.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: A validator count does not describe how evenly stake is distributed.

### Block height: 416,445,416 block

Current block height reported by the selected RPC node.

**Why it matters:** Block height is a second progress marker that helps detect a stalled or lagging data source.

- Status: `ok`
- Source: Solana JSON-RPC / `getBlockHeight`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: This is network progress, not a measure of user adoption.

### Current slot: 438,391,609 slot

Latest slot reported by the selected public RPC node.

**Why it matters:** A rising slot confirms that this observer sees the chain continuing to advance.

- Status: `ok`
- Source: Solana JSON-RPC / `getSlot`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Different RPC nodes can be a few slots apart.

### Jupiter signer and fee-payer overlap: 26,816 wallet addresses

Jupiter Swap signer addresses that were also the successful transaction fee payer on the same UTC day.

**Why it matters:** The overlap reveals how often the visible application signer also pays the transaction fee.

- Status: `ok`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-08T15:31:00Z`
- Confidence: `high`
- Important limitation: This is an address intersection, not a count of people; sponsored or relayed transactions can fall outside it.

### Daily unique Jupiter Swap signers: 26,816 wallet addresses

Distinct tx_signer addresses on intended swaps recorded by Dune's curated Jupiter aggregator table during the latest complete UTC day.

**Why it matters:** It shows the scale of intended swap activity through one of Solana's major application routes.

- Status: `ok`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-08T15:31:00Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people, and this measures Jupiter Swap signers rather than users of a particular wallet app.

### Daily unique successful fee payers: 2,046,280 wallet addresses

Distinct primary signer (fee payer) addresses on successful non-vote Solana transactions during the latest complete UTC day.

**Why it matters:** Fee payers approximate how many distinct addresses initiated successful activity and paid for execution.

- Status: `ok`
- Source: Dune / `solana.transactions / daily_unique_fee_payers.sql`
- Collected: `2026-08-08T15:19:39Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people: one person or bot can control many addresses, and relayers may pay fees for others.

### Daily unique successful signers: 3,628,019 wallet addresses

Distinct signer addresses on successful non-vote Solana transactions during the latest complete UTC day.

**Why it matters:** Successful signers capture a broader set of participating addresses than fee payers alone.

- Status: `ok`
- Source: Dune / `solana.transactions.signers / daily_unique_successful_signers.sql`
- Collected: `2026-08-08T15:19:39Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people: one person or bot can control many addresses, and one transaction may require several signers.

### Delinquent stake share: 0.01 percent

Delinquent activated stake as a share of all activated stake in this response.

**Why it matters:** Stake share is more meaningful than a raw delinquent-validator count.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: One RPC snapshot can change quickly as validators recover or fall behind.

### Delinquent stake: 43,931.79 SOL

Activated stake assigned to vote accounts currently classified as delinquent.

**Why it matters:** It sizes the voting power currently failing to participate normally.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Delinquency can be temporary and does not imply malicious behavior.

### Delinquent validators: 9 validators

Vote accounts currently classified as delinquent by the RPC response.

**Why it matters:** Delinquency is an early operational signal that part of the validator set is falling behind.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Temporary delinquency can recover and is not automatically malicious behavior.

### Epoch progress: 79.54 percent

Share of the current epoch's slots already completed.

**Why it matters:** Epoch progress provides timing context for validator rewards, stake activation, and network operations.

- Status: `ok`
- Source: Solana JSON-RPC / `getEpochInfo`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Epoch progress describes validator timing, not economic growth.

### Estimated non-vote TPS: 1,975.97 transactions/second

Non-vote transactions in the latest RPC performance sample divided by sample seconds.

**Why it matters:** This is the closest live RPC measure of application and user transaction throughput.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Non-vote transactions can still include bots and automated programs.

### Estimated slot time: 0.42 seconds

Latest performance sample duration divided by slots produced.

**Why it matters:** Slot time indicates how quickly the chain is advancing in the most recent sample.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: This is a short recent estimate and can move between samples.

### Estimated total TPS: 3,601.02 transactions/second

All transactions in the latest RPC performance sample divided by sample seconds.

**Why it matters:** Total throughput shows network load, but must be separated from user activity because it includes validator votes.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Includes validator votes, so it is not the same as user activity.

### Jupiter Swap seven-day return rate: 26.43 percent

Share of the day's Jupiter Swap signer addresses also seen at least once during the preceding seven complete UTC days.

**Why it matters:** Return rate distinguishes repeat use from one-time address activity.

- Status: `ok`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-08T15:31:00Z`
- Confidence: `high`
- Important limitation: Returning addresses are not necessarily returning people; bots and one person using several wallets remain included.

### Median validator commission: 5.00 percent

Median advertised commission among active vote accounts with valid values.

**Why it matters:** Commission affects how staking rewards are divided between validators and delegators.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: The median does not include operating cost, MEV, or total validator profitability.

### RPC health: ok status

Health response from the selected public RPC node.

**Why it matters:** It is the first check that the dashboard's live network data path is responding normally.

- Status: `ok`
- Source: Solana JSON-RPC / `getHealth`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: This checks one public RPC endpoint, not every validator.

### SOL price: 76.66 USD

CoinGecko's aggregated market price for one SOL in USD.

**Why it matters:** Price supplies market context for SOL-denominated capital and validator economics.

- Status: `ok`
- Source: CoinGecko / `simple/price?ids=solana`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `high`
- Important limitation: Market price is volatile context, not evidence that network or application usage is growing.

### Solana application fees: 8,376,941.66 USD

Fees users paid covered Solana applications on the latest complete UTC day, excluding gas, stablecoin issuers, and liquid staking.

**Why it matters:** App fees show what users paid applications for covered services.

- Status: `ok`
- Source: DeFiLlama / `overview/fees/solana?dataType=dailyAppFees`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `high`
- Important limitation: Adapter coverage can change, and fees paid are not money retained by applications.

- 7-day average change: `+15.9%`
- Direction is not a health verdict.

### Solana application revenue: 3,887,791.90 USD

The portion of covered Solana application fees retained by protocols on the latest complete UTC day.

**Why it matters:** App revenue shows captured value under provider definitions.

- Status: `ok`
- Source: DeFiLlama / `overview/fees/solana?dataType=dailyAppRevenue`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `high`
- Important limitation: This is not profit; incentives, token emissions, and operating costs are separate.

- 7-day average change: `+14.4%`
- Direction is not a health verdict.

### Solana chain fees: 650,664.00 USD

Base and priority transaction fees paid to the Solana network on the latest complete UTC day, as indexed by DeFiLlama.

**Why it matters:** Chain fees show demand for scarce transaction execution.

- Status: `ok`
- Source: DeFiLlama / `summary/fees/solana?dataType=dailyFees`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `high`
- Important limitation: Higher fees can reflect demand, congestion, speculation, or MEV. DeFiLlama's adapter estimates base fees from transaction count although Solana's protocol fee is charged per signature.

- 7-day average change: `+15.5%`
- Direction is not a health verdict.

### Solana DeFi TVL: 4,792,264,217.00 USD

USD value locked in Solana DeFi protocols tracked by DeFiLlama on the latest complete UTC day.

**Why it matters:** TVL shows how much capital is deposited in tracked Solana DeFi protocols.

- Status: `ok`
- Source: DeFiLlama / `v2/historicalChainTvl/Solana`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `high`
- Important limitation: TVL depends on protocol coverage and methodology and can double-count economic exposure through composable assets.

- 7-day average change: `-0.7%`
- Direction is not a health verdict.

### Solana daily DEX volume: 1,347,434,364.98 USD

Aggregate Solana spot DEX volume tracked by DeFiLlama on the latest complete UTC day.

**Why it matters:** DEX volume shows how much spot exchange activity occurred across tracked Solana venues.

- Status: `ok`
- Source: DeFiLlama / `overview/dexs/Solana?dataType=dailyVolume`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `high`
- Important limitation: Routing can touch several pools, and provider adapter and deduplication coverage determine the reported total.

- 7-day average change: `-7.0%`
- Direction is not a health verdict.

### Identifiable payment volume: Not available USD

Value transferred for identifiable commerce or remittance, with a published attribution method and coverage boundary.

**Why it matters:** Payments would show use of Solana as financial settlement rather than only trading infrastructure.

- Status: `unavailable`
- Source: No approved live source / `deferred pending defensible payment attribution`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `experimental`
- Important limitation: Raw stablecoin transfers are not payments: they can include trading, bots, rebalancing, and repeated movement.

### Tokenized real-world assets (excluding stablecoins): Not available USD

Circulating market value of tokenized real-world assets on Solana, excluding the stablecoin asset class.

**Why it matters:** This would show adoption of tokenized treasuries, equities, credit, commodities, funds, and other off-chain claims.

- Status: `unavailable`
- Source: RWA.xyz (optional adapter) / `v4 assets aggregate; Solana; exclude Stablecoins`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `experimental`
- Important limitation: Source not connected: dependable API access requires authentication. No historical article value is substituted.

### Solana REV (chain fees + tracked Jito tips): 786,058.00 USD

Solana chain fees plus gross Jito MEV tips tracked by DeFiLlama for the latest complete UTC day.

**Why it matters:** REV estimates direct economic value paid for blockspace and transaction ordering.

- Status: `ok`
- Source: DeFiLlama / `dailyFees(Solana) + dailyFees(jito-mev-tips)`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `high`
- Important limitation: REV is not GDP, profit, or app revenue; private or non-Jito MEV may be outside coverage. Jito component: https://api.llama.fi/summary/fees/jito-mev-tips?dataType=dailyFees

- 7-day average change: `+13.0%`
- Direction is not a health verdict.

### Solana stablecoin circulating value: 16,255,726,011.00 USD

USD value of circulating stablecoins on Solana across DeFiLlama's peg buckets on the latest complete UTC day.

**Why it matters:** Stablecoin value shows the dollar-like liquidity available for trading, saving, and settlement on Solana.

- Status: `ok`
- Source: DeFiLlama / `stablecoincharts/Solana`
- Collected: `2026-08-10T11:18:12.204135Z`
- Confidence: `high`
- Important limitation: Circulating stablecoin value is not payment volume or proof that every token is backed by cash.

- 7-day average change: `-1.4%`
- Direction is not a health verdict.

### Stake superminority coefficient: 18 vote accounts

Minimum largest vote accounts whose combined activated stake reaches one third.

**Why it matters:** A larger value means more vote accounts are required to reach consensus-blocking stake.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: This is calculated by vote account, not verified independent operator.

### Top 10 stake share: 24.39 percent

Share of activated stake assigned to the ten largest vote accounts.

**Why it matters:** It exposes concentration hidden by the total validator count.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Vote accounts are not operators; one organization may control several accounts.

### Top 25 stake share: 40.12 percent

Share of activated stake assigned to the twenty-five largest vote accounts.

**Why it matters:** It provides a broader view of stake concentration beyond the largest validators.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: Vote accounts are not operators and ownership identity is not inferred.

### Stake with recent vote credits: 100.00 percent

Share of active stake on vote accounts whose latest epoch-credit record increased.

**Why it matters:** It checks whether active voting power shows evidence of recent vote participation.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T11:18:11.006306Z`
- Confidence: `high`
- Important limitation: One credit record is a bounded participation check, not a full performance history.

## How to read this

These measurements describe different parts of Solana. They do not, by themselves, prove how many humans are using the network or why activity changed.
