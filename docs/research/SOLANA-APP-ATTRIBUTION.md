# Solana app attribution: what the observatory can measure honestly

Research date: 2026-08-06
Scope: Jupiter, Phantom, Solflare, Raydium, Kamino, Drift, Jito, Marinade,
Sanctum, and NFT activity. Sources are limited to first-party project material
and Dune's official data catalog.

## Short answer

The observatory can measure **protocol actions** much more reliably than it can
measure **wallet apps**.

- Jupiter Swap, Raydium trading, Kamino lending, Drift trading, and direct
  staking-protocol actions invoke identifiable onchain programs or appear in
  first-party/curated protocol datasets.
- Phantom and Solflare are signing interfaces. In the normal flow, they sign a
  transaction constructed by a dapp; the resulting Solana record identifies
  public keys, signers, and invoked programs, but not the wallet software used.
  Phantom and Solflare both document generic sign/send flows for arbitrary
  transactions ([Phantom transaction guide](https://docs.phantom.com/solana/sending-a-transaction-1),
  [Solflare Wallet SDK](https://docs.solflare.com/solflare/technical/integrate-solflare/solflare-wallet-sdk)).
- Therefore, an onchain chart labelled "Phantom users" or "Solflare users"
  would not be defensible. The same address may also be imported into more than
  one wallet app. Wallet-brand usage requires opt-in first-party telemetry or a
  clearly documented wallet-specific marker, and should be labelled as an
  offchain/vendor-reported metric.

Throughout the product, "users" should mean **distinct addresses satisfying the
stated action rule**, never people.

## What is measurable

| Product/category | Defensible first metric | Best initial source | Attribution limits |
| --- | --- | --- | --- |
| **Jupiter Swap** | Distinct `tx_signer` addresses completing a Jupiter aggregator swap; also swap count and USD volume | Dune's curated [`jupiter_solana.aggregator_swaps`](https://docs.dune.com/data-catalog/curated/dex-trades/solana/jupiter-aggregator-trades) | Call it **Jupiter Swap users**, not Jupiter Wallet users. The table represents one intended swap even if the route has several pool legs. |
| **Raydium** | Distinct traders, trades, and USD volume where `project = 'raydium'`, with the exact Dune values inspected before locking the query | Dune's curated [`dex_solana.trades`](https://docs.dune.com/data-catalog/curated/dex-trades/solana/solana-dex-trades); cross-check against Raydium's [canonical program list](https://docs.raydium.io/reference/program-addresses) | The DEX table records route legs, so rows are not necessarily user intents. A Jupiter route using Raydium can count in both the Jupiter and Raydium cards. Never add those address counts together. |
| **Kamino Lending** | Distinct authorities performing selected lending actions, preferably separated into deposit, borrow, repay, and withdraw | Decoded IDL calls or official Kamino data/SDK surfaces; Kamino documents onchain reads and historical APIs in its [developer toolchain](https://kamino.com/docs) and publishes the [KLend program source](https://github.com/Kamino-Finance/klend) | Label **Kamino Lending**, not all Kamino. Vault, liquidity, lending, and other product families require an explicitly documented union and deduplication rule. Protocol calls may include bots or liquidators as well as end users. |
| **Drift** | Distinct authorities making trades, plus fills/notional; keep deposits and liquidations separate | Drift's official [Data API](https://docs.drift.trade/historical-data/historical-data-v2) and its documented onchain DLOB/user accounts ([DLOB docs](https://docs.drift.trade/developers/drift-sdk/dlob)) | "Any program interaction" mixes traders, keepers, liquidators, and administration. Use action-specific decoded calls or trade records. Revalidate current official program identity immediately before implementation because the docs/product surface is changing. |
| **JitoSOL** | Distinct addresses directly depositing to or withdrawing from the Jito stake pool; separately show JitoSOL holders or transfers if desired | Jito's official [deployed-program and pool addresses](https://www.jito.network/docs/jitosol/jitosol-liquid-staking/security/deployed-programs/) | Jito uses the shared SPL Stake Pool program. Filtering only that program would count other stake pools; the query must also identify the Jito pool account and instruction semantics. Holding, transferring, buying on a DEX, and directly staking are different actions. |
| **Marinade** | Distinct addresses performing selected mSOL deposit/withdraw actions; show native staking separately if coverage permits | Marinade's official [contract and token addresses](https://docs.marinade.finance/developers/contract-addresses) and [IDL](https://docs.marinade.finance/developers/anchor-idl) | mSOL holders are not the same as direct Marinade stakers. Do not merge token transfers, DEX purchases, liquid staking, and native staking into one unexplained count. |
| **Sanctum** | Start with one named surface: Router stake/withdraw/swap actions **or** Infinity liquidity actions | Sanctum's official [Router instruction definitions](https://learn.sanctum.so/docs/technical-documentation/router) and [deployed-program list](https://learn.sanctum.so/docs/for-developers/deployed-programs) | Sanctum spans a router, Infinity, reserve, and many LSTs. "Sanctum users" is ambiguous unless the included programs and actions are enumerated and addresses are deduplicated. |
| **NFT ecosystem** | Distinct NFT transfer signers and transfer count, segmented by token standard; later add verified marketplace trades | Dune's curated [`tokens_solana.nft`](https://docs.dune.com/data-catalog/curated/nft-trades/solana/solana-nft-transfers) and Metaplex's official [program/standard overview](https://developers.metaplex.com/agents/skill/programs-and-operations) | Dune warns that non-standard transfers may be absent. Transfer activity is not equivalent to a sale or marketplace use. Do not label activity as Tensor or Magic Eden until canonical marketplace programs/accounts and action rules are verified from those projects. |
| **Phantom / Solflare** | No general onchain active-user metric | If pursued, request first-party aggregate telemetry with methodology | A signer address does not reveal which wallet UI signed. Phantom may add Lighthouse safety instructions to some transactions ([official explanation](https://docs.phantom.com/developer-powertools/lighthouse)), but that is not documented as a complete or exclusive Phantom-user identifier and must not be used as one. |

## Recommended compact first app panel

Build a category panel rather than a popularity leaderboard. The first version
should contain five comparable seven-complete-day series:

1. **Jupiter Swap traders** — distinct swap signers, swaps, and USD volume.
2. **Raydium pool traders** — distinct traders and USD volume attributable to
   Raydium pool execution, explicitly allowing overlap with Jupiter routes.
3. **Kamino Lending actors** — distinct authorities performing selected
   deposit/borrow/repay/withdraw actions, with action mix.
4. **Drift perp traders** — distinct trading authorities and fills/notional,
   after the current program/data identity is revalidated.
5. **Direct liquid-staking actors** — separate JitoSOL and Marinade action
   series; add Sanctum once one precise surface is selected.

Add **Solana NFT transfer signers** as a sixth ecosystem-category card when the
product wants cultural/consumer activity. It should be an NFT-standard activity
metric, not a marketplace leaderboard in its first version.

Phantom and Solflare should appear in an educational note titled "Wallet apps
are not visible in ordinary onchain transactions," not as fabricated user
counts.

## Query and presentation guardrails

- Use only complete UTC days and show collection time and source freshness.
- Define the unit in every title: addresses, swaps, trade legs, transactions,
  fills, or USD volume.
- For address counts, say "distinct addresses," not "people."
- Count successful actions only unless failure rate is the stated metric.
- Distinguish a **direct app entry** (a top-level program invocation) from
  **protocol reach** (any invocation, including an inner cross-program call).
  Dune exposes this distinction in `solana.instruction_calls` through fields
  such as `is_inner` and the outer/inner executing accounts
  ([official table schema](https://docs.dune.com/data-catalog/solana/instruction-calls)).
  A Jupiter transaction that invokes Raydium internally demonstrates Raydium
  liquidity usage, not that the signer opened the Raydium app.
- Pin the exact program IDs/accounts, included instructions, and version/date in
  the metric registry. Dune's decoded-table documentation explains that IDL
  tables expose program calls but only decode what the submitted IDL covers
  ([Dune decoded Solana tables](https://docs.dune.com/data-catalog/solana/idl-tables)).
- Prefer Dune curated tables for the initial trading panel because Dune states
  that they are normalized, maintained datasets with documented methodology
  ([curated data overview](https://docs.dune.com/data-catalog/curated/overview)).
- Deduplicate addresses within a card, but do not sum cards: one address can use
  several protocols, and one transaction can touch Jupiter plus one or more
  underlying DEXs.
- Keep direct protocol use distinct from token ownership. Someone can acquire
  JitoSOL or mSOL on a DEX without ever invoking the staking protocol.
- When a first-party API is used, preserve its endpoint, parameters, response
  time, and limitations just as rigorously as an onchain query.

## Product conclusion

The strongest story is not "which wallet won?" It is **what kinds of economic
actions people-shaped addresses are taking on Solana**: trading, lending, perp
trading, liquid staking, and digital-asset activity. That story is measurable,
educational, and honest about overlap. Wallet-brand adoption is a separate
offchain research question and should remain visibly outside the deterministic
onchain core until a reliable first-party dataset is available.
