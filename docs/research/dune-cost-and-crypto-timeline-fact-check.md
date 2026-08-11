# Dune cost and crypto timeline fact-check

Research date: 2026-08-11  
Scope: current Dune pricing for the three adoption queries, plus a primary-source
fact-check of the proposed Bitcoin-to-Solana beginner timeline.

## Executive conclusions

1. **The three Dune queries should fit inside the Free plan even at a six-hour
   execution cadence.** Using the latest measured batch cost, the estimate is
   about **2,162 credits per average month**, below the 2,500 included monthly
   credits. The expected Dune cash cost is therefore **$0**, provided these costs
   remain representative and the account has little other Dune usage.
2. **Putting “$5” into Dune is not a six-month prepaid balance.** On Free, usage
   beyond the monthly allowance is billed at $5 per 100 credits. Dune says extra
   credits cannot be bought in bulk; the account-level control is a **monthly
   extra-spend limit**. A $5 monthly limit could therefore permit up to $30 over
   six months, while a $10 monthly limit could permit up to $60.
3. **Retrieval is not refresh.** Reading the latest saved result through the API
   consumes export credits, but it does not rerun the SQL. The result advances
   beyond August 7 only after the three queries are executed again.
4. **The proposed history has the right broad arc but needs important
   corrections.** Ethereum did not launch with proof of stake; it launched with
   proof of work in 2015 and switched to proof of stake in 2022. The Ethereum
   whitepaper and Yellow Paper are separate documents. ERC-20 arrived after
   mainnet. Layer 2 is a later scaling branch, not a step that “launched” before
   Solana. Solana's Proof of History is best described as a cryptographic clock
   used alongside proof-of-stake consensus, not as a consensus mechanism by
   itself.

## 1. Dune: what is being paid for

The relevant Dune operations are distinct:

| Operation | What it does | Credit behavior |
|---|---|---|
| Query execution | Reruns SQL against current Dune data | Uses credits based on actual compute; manual and programmatic executions are metered according to the resources used. |
| Result retrieval/export | Reads rows already produced by an execution | Uses export credits on every request. |
| Stored-result retrieval without execution | Downloads the last result again | Uses export credits but **does not make the underlying result newer**. |
| Subscription | Buys a recurring plan and its feature/credit bundle | Not required for the current workload; Free includes API access and 2,500 monthly credits. |
| Extra credits | Covers usage after the plan allowance | On Free, $5 per 100 credits; billed as used, not purchased as a bulk prepaid pack. |

Dune says API query execution is charged on actual compute and result exports
also consume credits. Its current FAQ says the Free plan API can trigger
executions and export data, although the zero-cost Small Engine is limited to
manual app executions; API usage still consumes plan credits. Dune also provides
both a per-execution query cap and a monthly extra-credit limit. Setting the
extra-credit limit to $0 prevents additional-usage billing.

Primary sources:

- [Dune API billing](https://docs.dune.com/api-reference/overview/billing)
- [Dune pricing FAQ](https://docs.dune.com/learning/how-tos/pricing-faqs)
- [How Dune credits work](https://docs.dune.com/resources/credits-billing/how-credits-work)

### Project-specific measured cost

The durable receipts in [`docs/COSTS.md`](../COSTS.md) record this complete
three-query refresh on 2026-08-08:

| Saved query | Measured execution cost |
|---|---:|
| Successful fee payers (`8213434`) | 3.37 credits |
| Successful signers (`8264418`) | 6.47 credits |
| Jupiter overlap and retention (`8264526`) | 3.65 credits |
| **Execution subtotal** | **13.49 credits** |
| Three small result exports | **less than 0.03 credits** |

An approved API execution on 2026-08-11 used 5.5502, 7.0179, and 5.1163 credits,
or **17.6844 execution credits total**. For forward planning, this note uses a
deliberately rounded estimate of **17.72 credits per complete
execute-and-retrieve cycle**. Actual execution cost can
change because Dune meters real compute, data scanned, engine choice, and runtime;
Dune does not promise a fixed per-query formula.

### Six-month cadence estimates

Assumptions:

- 183 days as a conservative six-month planning window;
- every refresh executes all three queries and retrieves all three small results;
- 17.72 credits per complete cycle;
- Free allowance resets monthly and unused credits do not roll over;
- no material competing Dune workload on the same account.

| Cadence | Approx. cycles in 6 months | Estimated credits in 6 months | Average credits/month | Estimated cash cost on Free |
|---|---:|---:|---:|---:|
| Every 6 hours | 732 | 12,971 | 2,162 | **$0** |
| Daily | 183 | 3,243 | 540 | **$0** |
| Weekly | 27 | 478 | 80 | **$0** |

The six-month total is not compared with a single 2,500-credit bucket: Dune's
allowance resets each month. The highest estimate is about 2,162 credits in an
average month, leaving only approximately 338 included credits of monthly
headroom. Daily execution is safer and matches the metrics' daily grain.

If the GitHub workflow merely retrieves the same stored results every six hours
without executing SQL, its export-only use should remain very small: applying
the recorded “less than 0.03 credits” to 732 retrieval cycles gives **less than
22 credits over six months**, but the data would remain stale.

### What a $5 or $10 limit actually means

- **Recommended starting posture:** remain on Free, keep the per-query cap at
  100 credits, and keep the extra-credit limit at $0 while observing two to four
  weeks of automated execution costs.
- If reliability requires a buffer, set a **$5 monthly extra-spend limit**. At
  Free's current rate, this covers up to 100 credits beyond that month's included
  allowance. It is a ceiling, not a charge that happens automatically every month.
- A **$10 monthly limit** covers up to 200 extra credits in a month.
- Because Dune's limit is monthly, the maximum cash exposure over six months is
  $30 at a $5 monthly ceiling or $60 at a $10 monthly ceiling. A one-time $5 or
  $10 six-month deposit is not an option described by Dune.
- The current paid Analyst plan is $75/month and includes 4,000 credits; it is
  economically unnecessary for these three queries at their recorded cost.

This is an estimate, not a guarantee. The workflow should record
`execution_cost_credits`, stop on the existing per-query cap, and surface stale
data instead of retrying aggressively.

## 2. Beginner crypto timeline: corrected version

### 2008–2009 — Bitcoin: scarce peer-to-peer money without a central operator

- Satoshi Nakamoto posted *Bitcoin: A Peer-to-Peer Electronic Cash System* to
  the Cryptography mailing list on **October 31, 2008**. The paper describes a
  peer-to-peer payment system that uses a chain of hash-based proof of work to
  order transactions and resist double spending.
- The clean beginner lesson is not “Bitcoin invented every blockchain idea.” It
  demonstrated a working way for strangers to maintain scarce digital money
  without a trusted payment intermediary.

Primary sources: [Satoshi's October 31 mailing-list
post](https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html)
and the [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf).

### 2013–2015 — Ethereum: a general-purpose programmable blockchain

- Vitalik Buterin circulated the Ethereum **whitepaper in late 2013**. It set out
  the vision for a blockchain with a general-purpose programming environment for
  smart contracts and decentralized applications.
- Gavin Wood's **Yellow Paper, released in 2014**, was the formal technical
  specification. It was not a replacement name for the whitepaper.
- Ethereum conducted its ether sale in **July–September 2014** and launched the
  Frontier mainnet on **July 30, 2015**.
- Crucial correction: Ethereum mainnet launched using **proof of work**, not
  proof of stake. The Merge completed Ethereum's switch to proof of stake on
  **September 15, 2022**.
- Smart-contract ideas predated Ethereum and Bitcoin has a deliberately limited
  scripting system. Ethereum's key advance was making general-purpose onchain
  programs the platform's central product.

Primary sources: [Ethereum whitepaper](https://ethereum.org/whitepaper/),
[Ethereum protocol timeline](https://ethereum.org/ethereum-forks/), [2014 ether
sale announcement](https://blog.ethereum.org/2014/07/22/launching-the-ether-sale),
[2015 Frontier launch announcement](https://blog.ethereum.org/2015/07/30/ethereum-launches),
and [The Merge](https://ethereum.org/roadmap/merge/).

### 2015 onward — ERC-20 and token fundraising

- ERC-20 was created on **November 19, 2015** as a standard interface for tokens
  implemented by Ethereum smart contracts. A shared interface made tokens easier
  for wallets, exchanges, and applications to reuse.
- Avoid saying Ethereum or ERC-20 “launched ICOs.” Token fundraising existed
  before ERC-20, and Ethereum itself held a public ether sale before its mainnet
  and before ERC-20. A defensible claim is: **Ethereum's programmable contracts
  and ERC-20 standard made issuing and integrating fungible tokens much easier,
  helping token sales scale into a major ecosystem pattern.**

Primary sources: [ERC-20 specification](https://eips.ethereum.org/EIPS/eip-20)
and [Ethereum's 2014 ether sale
announcement](https://blog.ethereum.org/2014/07/22/launching-the-ether-sale).

### Later — Layer 2: scale while settling back to a base chain

- Layer 2 should be shown as a later scaling branch, not placed between ERC-20
  and Solana as though all L2 blockchains launched in one era.
- In Ethereum's current framing, rollups process batches away from mainnet and
  submit their output to Ethereum, reducing per-user cost while relying on the
  base layer for data/security properties. Layer 2 designs have different
  maturity and trust assumptions.

Primary sources: [What is layer
2?](https://ethereum.org/layer-2/learn/) and [Scaling
Ethereum](https://ethereum.org/roadmap/scaling/).

### 2017–2020 — Solana: optimize a layer 1 around verifiable ordering and parallelism

- It is reasonable to label **2017** as the beginning of the Solana project and
  Proof-of-History design, but the strongest directly citable official public
  explainer located for the interface is dated **April 18, 2018**. If the page
  needs a documentary milestone, use “2017: project/design begins” and “2018:
  Proof of History publicly explained,” rather than claiming a 2017 whitepaper
  publication without a dated primary artifact.
- Solana's whitepaper defines Proof of History (PoH) as a proof for verifying the
  order and passage of time between events. **PoH is not, by itself, Solana's
  consensus mechanism.** Solana uses proof-of-stake consensus with Tower BFT,
  while PoH supplies a cryptographic clock/order that reduces coordination
  overhead.
- The accurate beginner claim is: **Solana was designed as a high-throughput,
  low-fee layer 1, using PoH, Tower BFT, parallel transaction execution, and
  other engineering choices to reduce latency and increase capacity.** Do not
  reduce the story to “Proof of History made transactions cheap,” because cost
  and throughput come from the system design as a whole.

Primary sources: [Solana
whitepaper](https://solana.com/solana-whitepaper.pdf), [2018 Proof of History
explainer](https://solana.com/news/proof-of-history--a-clock-for-blockchain),
[Solana consensus comparison](https://solana.com/developers/evm-to-svm/consensus),
and [Solana solutions overview](https://solana.com/solutions).

## Recommended public-facing four-beat version

> **Bitcoin made digital scarcity work without a central payment operator.**  
> **Ethereum made blockchains programmable.**  
> **Token standards and layer 2 networks expanded what people could issue and
> scale.**  
> **Solana redesigned a layer 1 for fast, inexpensive, consumer-scale activity —
> with real tradeoffs that the Observatory measures rather than hides.**

This wording is short enough for an intro experience and avoids the major
technical and chronological errors. The following dashboard should then test
the final claim with evidence about cost, reliability, adoption, validator
health, ecosystem depth, and financial-rail usage.
