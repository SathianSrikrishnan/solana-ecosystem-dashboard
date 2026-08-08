# Solana Ecosystem Report

Generated: `2026-08-08T16:09:03.167075Z`

**Current reading:** The selected Solana RPC endpoint reports healthy.

## What is happening now?

### Active validators: 692 validators

Vote accounts currently classified as active by the RPC response.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: A validator count does not describe how evenly stake is distributed.

### Block height: 413,812,365 block

Current block height reported by the selected RPC node.

- Status: `ok`
- Source: Solana JSON-RPC / `getBlockHeight`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: This is network progress, not a measure of user adoption.

### Current slot: 435,753,787 slot

Latest slot reported by the selected public RPC node.

- Status: `ok`
- Source: Solana JSON-RPC / `getSlot`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: Different RPC nodes can be a few slots apart.

### Jupiter signer and fee-payer overlap: 26,816 wallet addresses

Jupiter Swap signer addresses that were also the successful transaction fee payer on the same UTC day.

- Status: `ok`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-08T15:31:00Z`
- Confidence: `high`
- Important limitation: This is an address intersection, not a count of people; sponsored or relayed transactions can fall outside it.

### Daily unique Jupiter Swap signers: 26,816 wallet addresses

Distinct tx_signer addresses on intended swaps recorded by Dune's curated Jupiter aggregator table during the latest complete UTC day.

- Status: `ok`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-08T15:31:00Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people, and this measures Jupiter Swap signers rather than users of a particular wallet app.

### Daily unique successful fee payers: 2,046,280 wallet addresses

Distinct primary signer (fee payer) addresses on successful non-vote Solana transactions during the latest complete UTC day.

- Status: `ok`
- Source: Dune / `solana.transactions / daily_unique_fee_payers.sql`
- Collected: `2026-08-08T15:19:39Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people: one person or bot can control many addresses, and relayers may pay fees for others.

### Daily unique successful signers: 3,628,019 wallet addresses

Distinct signer addresses on successful non-vote Solana transactions during the latest complete UTC day.

- Status: `ok`
- Source: Dune / `solana.transactions.signers / daily_unique_successful_signers.sql`
- Collected: `2026-08-08T15:19:39Z`
- Confidence: `high`
- Important limitation: Wallet addresses are not people: one person or bot can control many addresses, and one transaction may require several signers.

### Delinquent validators: 15 validators

Vote accounts currently classified as delinquent by the RPC response.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: Temporary delinquency can recover and is not automatically malicious behavior.

### Epoch progress: 68.93 percent

Share of the current epoch's slots already completed.

- Status: `ok`
- Source: Solana JSON-RPC / `getEpochInfo`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: Epoch progress describes validator timing, not economic growth.

### Estimated non-vote TPS: 2,081.32 transactions/second

Non-vote transactions in the latest RPC performance sample divided by sample seconds.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: Non-vote transactions can still include bots and automated programs.

### Estimated slot time: 0.44 seconds

Latest performance sample duration divided by slots produced.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: This is a short recent estimate and can move between samples.

### Estimated total TPS: 3,670.50 transactions/second

All transactions in the latest RPC performance sample divided by sample seconds.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: Includes validator votes, so it is not the same as user activity.

### Jupiter Swap seven-day return rate: 26.43 percent

Share of the day's Jupiter Swap signer addresses also seen at least once during the preceding seven complete UTC days.

- Status: `ok`
- Source: Dune / `jupiter_solana.aggregator_swaps + solana.transactions / daily_jupiter_swap_signers.sql`
- Collected: `2026-08-08T15:31:00Z`
- Confidence: `high`
- Important limitation: Returning addresses are not necessarily returning people; bots and one person using several wallets remain included.

### RPC health: ok status

Health response from the selected public RPC node.

- Status: `ok`
- Source: Solana JSON-RPC / `getHealth`
- Collected: `2026-07-28T13:43:19.325189Z`
- Confidence: `high`
- Important limitation: This checks one public RPC endpoint, not every validator.

### SOL price: 76.32 USD

CoinGecko's aggregated market price for one SOL in USD.

- Status: `ok`
- Source: CoinGecko / `simple/price?ids=solana`
- Collected: `2026-08-08T16:09:03.167075Z`
- Confidence: `high`
- Important limitation: Market price is volatile context, not evidence that network or application usage is growing.

### Solana DeFi TVL: 4,707,203,417.00 USD

USD value locked in Solana DeFi protocols tracked by DeFiLlama on the latest complete UTC day.

- Status: `ok`
- Source: DeFiLlama / `v2/historicalChainTvl/Solana`
- Collected: `2026-08-08T16:09:03.167075Z`
- Confidence: `high`
- Important limitation: TVL depends on protocol coverage and methodology and can double-count economic exposure through composable assets.

### Solana daily DEX volume: 1,362,519,430.02 USD

Aggregate Solana spot DEX volume tracked by DeFiLlama on the latest complete UTC day.

- Status: `ok`
- Source: DeFiLlama / `overview/dexs/Solana?dataType=dailyVolume`
- Collected: `2026-08-08T16:09:03.167075Z`
- Confidence: `high`
- Important limitation: Routing can touch several pools, and provider adapter and deduplication coverage determine the reported total.

### Solana stablecoin circulating value: 16,252,010,540.00 USD

USD value of circulating stablecoins on Solana across DeFiLlama's peg buckets on the latest complete UTC day.

- Status: `ok`
- Source: DeFiLlama / `stablecoincharts/Solana`
- Collected: `2026-08-08T16:09:03.167075Z`
- Confidence: `high`
- Important limitation: Circulating stablecoin value is not payment volume or proof that every token is backed by cash.

## How to read this

These measurements describe different parts of Solana. They do not, by themselves, prove how many humans are using the network or why activity changed.
