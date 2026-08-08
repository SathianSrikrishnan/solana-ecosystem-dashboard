# Cost Guardrail

## Initial target

Build and operate the core for $0.

## Current source plan

| Source | Initial use | Cost posture |
|---|---|---|
| Solana public RPC | Live network and validator state | Free, rate-limited, not production-grade |
| Dune | Historical/adoption SQL | Free allowance first; set spend cap to $0 |
| CoinGecko | SOL price context | Free Demo/keyless allowance first |
| DeFiLlama | TVL and ecosystem context | Free public endpoints where permitted |
| X API | Announcements and public conversation | Optional, pay-per-use, hard budget and cache |
| Hosting | Static dashboard | Existing/free infrastructure first |

Sathian approved a hard $20 X API research cap on 2026-07-28. Auto-recharge
stays disabled. No other paid plan, credit purchase, or auto-recharge may be
enabled without explicit approval.

## Dune receipt - 2026-08-03

- Account plan shown by Dune: free trial at $0/month with 2,500 included
  credits and no payment method.
- Extra-credit limit: locked at $0.
- Per-query limit: enabled at 100 credits.
- Query `8213434`: 3.8919 included credits.
- Seven-row CSV export: 0.0003 included credits.
- Total used for this slice: 3.892 credits; extra credits used: 0 ($0).

No paid plan, payment method, API key, or auto-recharge was enabled.

## Dune receipt - 2026-08-08

- Account remained on the free trial; no payment method or paid plan was added.
- Refreshed fee-payer query `8213434`: 3.37 included credits.
- New successful-signers query `8264418`: 6.47 included credits.
- Each seven-row CSV export: less than 0.01 included credits.
- Extra credits used: 0; cash spend: $0.

The successful-signers query scans the same seven complete UTC days but expands
each transaction's signer list, so it costs more compute than the fee-payer
query. We run it deliberately rather than polling or retrying it automatically.
