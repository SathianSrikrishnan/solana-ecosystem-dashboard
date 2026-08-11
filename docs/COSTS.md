# Cost Guardrail

## Initial target

Build and operate the core for $0.

## Current source plan

| Source | Initial use | Cost posture |
|---|---|---|
| Solana public RPC | Live network and validator state | Free, rate-limited, not production-grade |
| Dune | Historical/adoption SQL | Free allowance first; set spend cap to $0 |
| CoinGecko | SOL price context | Free keyless public endpoint |
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

- Jupiter overlap and retention query `8264526`: 3.65 included credits.
- Jupiter seven-row CSV export: less than 0.01 included credits.
- Total verified Dune use recorded on 2026-08-08: 13.49 included query credits
  plus less than 0.03 included export credits; extra spend remained $0.

## Economy source receipt - 2026-08-08

- CoinGecko public keyless simple-price request: $0 and no API key.
- DeFiLlama public TVL, stablecoin, and DEX requests: $0 and no API key.
- Four bounded requests were made per refresh; no retry loop or paid fallback
  is configured.
- One compact normalized evidence file was retained. Full third-party payloads
  were not archived.

Cash spend for this economy slice: $0.

## Current Dune operating posture - 2026-08-10

- Dune is optional and limited to five adoption measurements; it is not needed
  for the network, economy, validator, ecosystem, price, or stablecoin layers.
- No paid subscription or payment method is required for the current project.
- The account has a 2,500-credit free allowance, a $0 extra-credit limit, and a
  100-credit per-query cap. Recorded cash spend remains $0.
- API query execution and API/CSV result retrieval consume credits. The scheduled
  workflow therefore retrieves stored results but does not execute queries.
- The stored result currently ends on 2026-08-07 and is visibly labeled stale.
  A bounded pre-submission refresh remains a human approval decision.

Official reference: [Dune API billing](https://docs.dune.com/api-reference/overview/billing),
[pricing FAQ](https://docs.dune.com/learning/how-tos/pricing-faqs), and
[how credits work](https://docs.dune.com/resources/credits-billing/how-credits-work).

## Dune execution receipt - 2026-08-11

Sathian explicitly approved one bounded execution of all three saved queries.
GitHub Actions executed them through Dune's account-supported default engine,
then retrieved and published results through 2026-08-10, the latest complete
UTC day.

| Query | Execution credits |
|---|---:|
| Successful fee payers (`8213434`) | 5.5502 |
| Successful signers (`8264418`) | 7.0179 |
| Jupiter overlap and retention (`8264526`) | 5.1163 |
| **Execution total** | **17.6844** |

Cash spend remained $0. The extra-credit limit remained $0 and the per-query
cap remained 100 credits. Using a conservative 17.72-credit execute-and-retrieve
cycle, the estimated monthly use is about 540 credits daily or 2,162 credits
every six hours. Daily execution is the recommended sustainable cadence because
the metrics use complete UTC-day cohorts.

## Approved three-day cadence - 2026-08-11

Sathian approved query execution when the oldest verified Dune adoption date
is three UTC days old. The workflow checks daily but does not execute when the
data is younger than three days. At the conservative 17.72-credit measured
cycle, this is approximately 180 included credits per month or 1,080 over six
months. That remains within the current 2,500-credit monthly Free allowance;
the $0 extra-credit limit prevents cash overage.
