# Metric Registry

Every production metric must define these fields:

| Field | Meaning |
|---|---|
| `id` | Stable machine name |
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

## First metrics

- RPC health
- current slot
- block height
- epoch progress
- recent estimated TPS
- recent estimated slot time
- current and delinquent validator counts

## Later metric family: activity identities

- transaction sender wallets;
- successful transaction signer wallets;
- wallets using a selected application;
- likely automated wallets;
- likely human-controlled wallets.

These are related measurements, not interchangeable truths.

