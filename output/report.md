# Solana Ecosystem Report

Generated: `2026-08-04T14:40:47.141363Z`

**Current reading:** The selected Solana RPC endpoint reports healthy.

## What is happening now?

### RPC health: ok status

Health response from the selected public RPC node.

- Status: `ok`
- Source: Solana JSON-RPC / `getHealth`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: This checks one public RPC endpoint, not every validator.

### Current slot: 437,193,598 slot

Latest slot reported by the selected public RPC node.

- Status: `ok`
- Source: Solana JSON-RPC / `getSlot`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: Different RPC nodes can be a few slots apart.

### Block height: 415,248,360 block

Current block height reported by the selected RPC node.

- Status: `ok`
- Source: Solana JSON-RPC / `getBlockHeight`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: This is network progress, not a measure of user adoption.

### Epoch progress: 2.22 percent

Share of the current epoch's slots already completed.

- Status: `ok`
- Source: Solana JSON-RPC / `getEpochInfo`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: Epoch progress describes validator timing, not economic growth.

### Estimated total TPS: 4,631.62 transactions/second

All transactions in the latest RPC performance sample divided by sample seconds.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: Includes validator votes, so it is not the same as user activity.

### Estimated non-vote TPS: 2,988.45 transactions/second

Non-vote transactions in the latest RPC performance sample divided by sample seconds.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: Non-vote transactions can still include bots and automated programs.

### Estimated slot time: 0.42 seconds

Latest performance sample duration divided by slots produced.

- Status: `ok`
- Source: Solana JSON-RPC / `getRecentPerformanceSamples`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: This is a short recent estimate and can move between samples.

### Active validators: 692 validators

Vote accounts currently classified as active by the RPC response.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: A validator count does not describe how evenly stake is distributed.

### Delinquent validators: 7 validators

Vote accounts currently classified as delinquent by the RPC response.

- Status: `ok`
- Source: Solana JSON-RPC / `getVoteAccounts`
- Collected: `2026-08-04T14:40:47.141363Z`
- Confidence: `high`
- Important limitation: Temporary delinquency can recover and is not automatically malicious behavior.

## How to read this

These measurements describe different parts of Solana. They do not, by themselves, prove how many humans are using the network or why activity changed.
