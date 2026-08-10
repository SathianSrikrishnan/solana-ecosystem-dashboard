# Solana Ecosystem Report

Generated: `2026-08-10T10:05:07.171029Z`

**Current reading:** The selected Solana RPC endpoint reports healthy.

## What is happening now?

### Active validators: 690 validators

Vote accounts currently classified as active by the RPC response.

**Why it matters:** Active vote accounts show how many validators are currently participating, before considering stake concentration.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T10:05:00.128941Z`
- Confidence: `high`
- Important limitation: A validator count does not describe how evenly stake is distributed.

### Block height: 416,434,991 block

Current block height reported by the selected RPC node.

**Why it matters:** Block height is a second progress marker that helps detect a stalled or lagging data source.

- Status: `ok`
- Source: Solana JSON-RPC / `getBlockHeight`
- Collected: `2026-08-10T10:05:00.128941Z`
- Confidence: `high`
- Important limitation: This is network progress, not a measure of user adoption.

### Current slot: 438,381,182 slot

Latest slot reported by the selected public RPC node.

**Why it matters:** A rising slot confirms that this observer sees the chain continuing to advance.

- Status: `ok`
- Source: Solana JSON-RPC / `getSlot`
- Collected: `2026-08-10T10:05:00.128941Z`
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

### Delinquent validators: 8 validators

Vote accounts currently classified as delinquent by the RPC response.

**Why it matters:** Delinquency is an early operational signal that part of the validator set is falling behind.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-10T10:05:00.128941Z`
- Confidence: `high`
- Important limitation: Temporary delinquency can recover and is not automatically malicious behavior.

### Epoch progress: 77.13 percent

Share of the current epoch's slots already completed.

**Why it matters:** Epoch progress provides timing context for validator rewards, stake activation, and network operations.

- Status: `ok`
- Source: Solana JSON-RPC / `getEpochInfo`
- Collected: `2026-08-10T10:05:00.128941Z`
- Confidence: `high`
- Important limitation: Epoch progress describes validator timing, not economic growth.

### Estimated non-vote TPS: 1,383.62 transactions/second

Non-vote transactions in the latest RPC performance sample divided by sample seconds.

**Why it matters:** This is the closest live RPC measure of application and user transaction throughput.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-10T10:05:00.128941Z`
- Confidence: `high`
- Important limitation: Non-vote transactions can still include bots and automated programs.

### Estimated slot time: 0.42 seconds

Latest performance sample duration divided by slots produced.

**Why it matters:** Slot time indicates how quickly the chain is advancing in the most recent sample.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-10T10:05:00.128941Z`
- Confidence: `high`
- Important limitation: This is a short recent estimate and can move between samples.

### Estimated total TPS: 2,994.98 transactions/second

All transactions in the latest RPC performance sample divided by sample seconds.

**Why it matters:** Total throughput shows network load, but must be separated from user activity because it includes validator votes.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-10T10:05:00.128941Z`
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

### RPC health: ok status

Health response from the selected public RPC node.

**Why it matters:** It is the first check that the dashboard's live network data path is responding normally.

- Status: `ok`
- Source: Solana JSON-RPC / `getHealth`
- Collected: `2026-08-10T10:05:00.128941Z`
- Confidence: `high`
- Important limitation: This checks one public RPC endpoint, not every validator.

### SOL price: 76.57 USD

CoinGecko's aggregated market price for one SOL in USD.

**Why it matters:** Price supplies market context for SOL-denominated capital and validator economics.

- Status: `ok`
- Source: CoinGecko / `simple/price?ids=solana`
- Collected: `2026-08-10T10:05:07.171029Z`
- Confidence: `high`
- Important limitation: Market price is volatile context, not evidence that network or application usage is growing.

### Solana DeFi TVL: 4,792,264,217.00 USD

USD value locked in Solana DeFi protocols tracked by DeFiLlama on the latest complete UTC day.

**Why it matters:** TVL shows how much capital is deposited in tracked Solana DeFi protocols.

- Status: `ok`
- Source: DeFiLlama / `v2/historicalChainTvl/Solana`
- Collected: `2026-08-10T10:05:07.171029Z`
- Confidence: `high`
- Important limitation: TVL depends on protocol coverage and methodology and can double-count economic exposure through composable assets.

### Solana daily DEX volume: 1,223,391,334.98 USD

Aggregate Solana spot DEX volume tracked by DeFiLlama on the latest complete UTC day.

**Why it matters:** DEX volume shows how much spot exchange activity occurred across tracked Solana venues.

- Status: `ok`
- Source: DeFiLlama / `overview/dexs/Solana?dataType=dailyVolume`
- Collected: `2026-08-10T10:05:07.171029Z`
- Confidence: `high`
- Important limitation: Routing can touch several pools, and provider adapter and deduplication coverage determine the reported total.

### Solana stablecoin circulating value: 16,255,726,011.00 USD

USD value of circulating stablecoins on Solana across DeFiLlama's peg buckets on the latest complete UTC day.

**Why it matters:** Stablecoin value shows the dollar-like liquidity available for trading, saving, and settlement on Solana.

- Status: `ok`
- Source: DeFiLlama / `stablecoincharts/Solana`
- Collected: `2026-08-10T10:05:07.171029Z`
- Confidence: `high`
- Important limitation: Circulating stablecoin value is not payment volume or proof that every token is backed by cash.

## How to read this

These measurements describe different parts of Solana. They do not, by themselves, prove how many humans are using the network or why activity changed.
