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

## Later metric family: activity identities

- transaction sender wallets;
- successful transaction signer wallets;
- wallets using a selected application;
- likely automated wallets;
- likely human-controlled wallets.

These are related measurements, not interchangeable truths.
