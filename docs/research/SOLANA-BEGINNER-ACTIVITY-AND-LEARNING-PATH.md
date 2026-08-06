# What people do on Solana, and a beginner-safe learning path

Research date: 2026-08-06
Scope: a current, educational overview of Solana activity and a cautious path
through Kamino, Drift, Jito, and Marinade. This is not financial advice, a
return forecast, or a recommendation to buy or trade any asset.

## The simple reality

There is no trustworthy single answer to "what most people do." One address
can be a person, a bot, a protocol, or several people, and one person can use
many addresses. Activity rankings also change with the time window and unit.
The observatory should therefore show several answers, each with a definition.

The best-supported current picture is that Solana is heavily used for:

1. **Sending tokens and paying fees.** This is the broad base layer, but a
   transaction count is not a people count. Dune's Solana transaction table
   contains successful status, fee payer, all signers, and instructions, and
   excludes validator votes
   ([Dune transaction schema](https://docs.dune.com/data-catalog/solana/transactions)).
2. **Spot swaps and token trading.** Jupiter routes a user's intended swap
   across liquidity venues; Raydium, Orca, and Meteora are examples of the
   pools or exchanges that may execute it. Dune maintains Solana DEX and
   Jupiter datasets and explicitly supports analysis of traders, trades,
   volume, slippage, and routes
   ([Dune Solana trading data](https://docs.dune.com/data-catalog/curated/dex-trades/solana/overview)).
3. **Perpetual-futures trading.** This is leveraged long/short trading rather
   than buying the underlying token. It is a major economic flow, but volume
   can be generated repeatedly by the same traders and bots.
4. **Lending and borrowing.** Depositors supply assets for interest; borrowers
   post more collateral than they borrow. Kamino is a major Solana venue for
   this activity
   ([Kamino Borrow overview](https://kamino.com/docs/products/borrow)).
5. **Staking and liquid staking.** SOL holders support validators and receive
   staking rewards. Liquid-staking protocols issue a transferable receipt such
   as JitoSOL or mSOL, adding utility and additional risk.
6. **Stablecoin payments and transfers.** The large stablecoin supply on
   Solana makes payments and settlement an important category, though token
   supply is not the same as payment usage.
7. **NFTs, consumer apps, games, and DePIN.** These matter culturally and as
   product experiments, but current economic volume is much smaller than
   trading and DeFi by the chosen measures.

As a volatile snapshot, not a timeless ranking, DeFiLlama showed roughly
$4.9B of Solana DeFi TVL, $16.5B of stablecoins, $1.4B of 24-hour DEX volume,
$1.3B of 24-hour perpetual volume, 2.3M active addresses, and 80.8M
transactions when checked for this note
([Solana chain dashboard](https://defillama.com/chain/solana?volume=true)).
These values are useful scale indicators, not directly comparable "user"
counts, and they will change.

## Common apps, described by what they do

| Need | Example apps/protocols | Plain-English job | A defensible dashboard measure |
| --- | --- | --- | --- |
| Wallet and signing | Phantom, Solflare | Hold keys, show balances, and approve transactions | Do not infer wallet brand from ordinary onchain activity |
| Best swap route | Jupiter | Finds routes across exchanges and pools | Distinct swap signers, intended swaps, USD volume |
| Pool execution | Raydium, Orca, Meteora | Supplies liquidity and executes swaps | Distinct traders, route legs, USD volume |
| Lending | Kamino | Supply assets, or borrow against collateral | Suppliers, borrowers, deposits, debt, liquidations |
| Perpetuals | Drift and other perp venues | Long or short without owning the asset | Traders, fills, notional volume, open interest, liquidations |
| Liquid staking | Jito, Marinade | Turn staked SOL into a usable receipt token | Direct stakers, withdrawals, LST supply; keep token holders separate |
| Native staking | Wallet validator selection, Marinade Native | Delegate SOL without receiving a DeFi token | Stake accounts, delegated SOL, validators |

Jupiter, Kamino, Jito, and Marinade are clearly significant by capital or
volume, but "most common app" depends on whether the ranking uses addresses,
transactions, volume, fees, or TVL. For context, the same-day DeFiLlama pages
showed about $1.5B TVL for Jupiter, $1.1B for Kamino, $0.74B for Jito, and
$0.49B for Marinade
([Jupiter](https://defillama.com/protocol/jupiter),
[Kamino](https://defillama.com/protocol/kamino),
[Jito](https://defillama.com/protocol/jito),
[Marinade](https://defillama.com/protocol/marinade)). TVL measures capital
inside tracked contracts; it is not a user count or a safety score.

## What the four named protocols teach

### Kamino: lending mechanics

Kamino's shared pools let suppliers earn borrower-paid interest and let
borrowers take overcollateralized loans. Borrow positions are governed by
current, maximum, and liquidation loan-to-value ratios; variable interest can
grow the debt even when prices do not move
([supplying](https://kamino.com/docs/products/borrow/supplying),
[borrowing](https://kamino.com/docs/products/borrow/borrowing)). Kamino also
documents withdrawal-liquidity and bad-debt risk and says there is no
protocol-wide insurance fund ([risk disclosure](https://kamino.com/docs/risk)).

**Beginner judgment:** learn supply-only first. Do not borrow, use Multiply, or
loop collateral during the first pass. Supplying still has smart-contract,
asset, oracle, bad-debt, and withdrawal-liquidity risk; it is not a savings
account.

### Jito: liquid staking plus MEV rewards

Depositing SOL produces JitoSOL. Its SOL exchange rate accrues staking and MEV
rewards, while the token remains transferable and usable in DeFi
([JitoSOL overview](https://www.jito.network/docs/jitosol/jitosol-liquid-staking/mev-and-staker-rewards-api-info/)).
Jito says the pool is non-custodial and uses the audited SPL Stake Pool program
([security overview](https://www.jito.network/docs/jitosol/jitosol-liquid-staking/security/overview/)).
Its glossary nevertheless lists management/withdrawal fees and smart-contract,
validator, and market/slippage risks
([JitoSOL glossary](https://www.jito.network/docs/jitosol/resources/jitosol-glossary/)).

**Beginner judgment:** stake a tiny amount, hold the receipt, observe the
JitoSOL/SOL exchange-rate model, and practice exiting. Jito's official Phantom
walkthrough says to use the canonical staking page, review SOL spent,
JitoSOL received, and the network fee, and retain SOL for fees
([official flow](https://www.jito.network/docs/jitosol/get-started/stake-sol-for-jitosol-flow/staking-with-phantom/)).
Do not immediately reuse JitoSOL as loan collateral; that stacks liquidation
risk on top of liquid-staking risk.

### Marinade: native staking versus mSOL

Marinade offers two useful comparisons. Marinade Native automates validator
delegation while the user retains withdrawal authority and does not receive a
DeFi receipt token. Liquid staking issues mSOL, which can be used elsewhere,
but introduces smart-contract and secondary-market risk
([protocol overview](https://docs.marinade.finance/marinade-protocol/protocol-overview),
[FAQ](https://docs.marinade.finance/marinade-protocol/faq)). An instant mSOL
exit is a market swap and can have price impact; delayed unstaking follows the
epoch flow.

**Beginner judgment:** native staking is the clearer first staking lesson.
Then use one small, separate mSOL experiment to learn what an LST changes.
JitoSOL and mSOL teach almost the same base concept, so there is no need to use
both immediately.

### Drift: perpetual futures, currently devnet/paper only

Perpetuals provide long or short exposure without an expiry. Leverage equals
position notional divided by collateral, funding transfers between long and
short positions, and the maintenance-margin boundary can trigger liquidation
([perpetuals](https://docs.drift.trade/protocol/trading/perpetuals-trading),
[glossary](https://docs.drift.trade/protocol/glossary)). Drift's own liquidation
documentation says extreme losses can reach insurance funds and, if backstops
are exhausted, be socialized
([liquidation engine](https://docs.drift.trade/protocol/trading/liquidations/liquidation-engine)).

There is an overriding current fact: Drift states that an April 1, 2026 attack
caused approximately $295M of user losses, core functions were suspended, and
the protocol is being rebuilt and relaunched
([May recovery plan](https://www.drift.trade/updates/recovery-plan-for-affected-users),
[June update](https://www.drift.trade/updates/drift-recovery-update-june-3-2026)).

**Beginner judgment:** do not deposit real money based on old Drift tutorials.
Use devnet if the official current interface still supports it, or paper-trade
locally. Reassess only after an official relaunch, fresh audits, live withdrawal
verification, and an updated independent risk review. Even then, perps should
be the last exercise: one market, tiny disposable collateral, no complex
cross-margin positions, and a predefined close rule. Treat any real loss as
tuition, never expected income.

## A safe learning sequence

First clarify whether "200 of Solana" means **about $200 worth of SOL** or
**200 SOL**. Those are radically different balances. The curriculum below is
the same either way; a larger balance is not a reason to make the experiments
larger.

1. **Observe without money.** Read the wallet prompt, program, assets in/out,
   network fee, and resulting explorer receipt for sample transactions.
2. **Use Devnet/local simulation.** Solana describes Devnet as a playground
   with valueless tokens and faucets
   ([clusters](https://solana.com/docs/references/clusters),
   [faucet guide](https://solana.com/developers/guides/getstarted/solana-token-airdrop-and-faucets)).
3. **Create a separate learning wallet.** Never use a seed phrase supplied by
   anyone, never enter it into a website, keep it offline, verify canonical
   domains, and disconnect/revoke apps after exercises. Phantom warns that
   blockchain transactions are irreversible and a shared recovery phrase gives
   full wallet control
   ([security guidance](https://help.phantom.com/hc/en-us/articles/5487893286291-I-was-scammed)).
4. **Learn native staking.** Use a deliberately small amount and observe
   activation, rewards by epoch, and delayed unstaking.
5. **Learn one LST.** Choose JitoSOL or mSOL, not both. Record the receipt-token
   amount, protocol exchange rate, available exit paths, quote, fee, and actual
   amount returned.
6. **Learn lending supply-only.** Deposit a tiny amount into one conservative
   Kamino pool, observe the receipt/exchange-rate mechanics, then withdraw.
   Do not enable borrowing or leverage.
7. **Paper-trade perps.** Log a hypothetical entry, long/short direction,
   notional, collateral, funding, fees, liquidation price, and exit. For Drift,
   remain off mainnet while its documented recovery/relaunch is unresolved.

If the balance is roughly $200, a fully simulated curriculum is reasonable;
real DeFi experiments can be so small that learning, not yield, is the only
goal. If it is 200 SOL, first establish hardware-wallet custody and keep the
main holdings completely separate from a fixed-size hot learning wallet. In
both cases, decide a maximum learning loss in ordinary currency before moving
anything. This is a risk-control exercise, not an allocation recommendation.

## Risk checklist in plain English

- **Wallet/security risk:** a malicious site or leaked seed can drain the
  wallet. Use a separate learning wallet, canonical bookmarks, offline seed
  storage, and a hardware wallet for material holdings.
- **Smart-contract/admin risk:** audited code can still fail, and governance or
  signer controls can be compromised. Drift's 2026 incident is a direct
  reminder that audits and reputation do not make losses impossible.
- **Liquidation/leverage risk:** prices, interest, funding, and oracle values can
  move a leveraged position into forced closure. A stop order is not a guarantee
  in a fast or illiquid market.
- **LST price/liquidity risk:** JitoSOL or mSOL represents staked SOL, but an
  immediate DEX exit can trade below the protocol redemption value or incur
  slippage. Delayed redemption has an opportunity and timing cost.
- **Validator/staking risk:** rewards vary; stake activation/deactivation takes
  epochs; delegation strategy, validator performance, and protocol fees matter.
- **Stablecoin/oracle risk:** a stablecoin can lose its target value and an
  oracle can be delayed, wrong, or manipulated. These risks can affect lending
  and perp collateral at the same time.

## Adjacent project: Solana Learning Lab

Build a small **read-only transaction and risk journal** beside the observatory.
It should never hold keys or execute trades. A learner pastes a devnet or
mainnet transaction signature, and the app produces:

- which wallet signed and which programs were invoked;
- assets sent and received, fees, and explorer links;
- an action label: transfer, stake, LST mint, lend supply, borrow, swap, or perp;
- a risk card showing whether leverage, liquidation, oracle, LST, or smart-
  contract exposure was added;
- a before/after balance and a plain-English explanation;
- a personal experiment journal with hypothesis, expected result, actual
  result, and lesson learned.

This complements the observatory cleanly: the observatory answers **"What is
the ecosystem doing?"** while the Learning Lab answers **"What did my test
transaction actually do?"** It also creates a strong bounty story: public,
source-backed ecosystem metrics paired with private, non-custodial education.
Start with Devnet transfer and native-staking receipts; add LST and Kamino
parsers later. Drift remains paper-only until the current recovery state is
resolved.

## Evidence versus judgment

Protocol mechanics, current incident statements, schemas, and snapshot metrics
above are sourced facts. The ordering of exercises, small fixed caps,
supply-only first pass, one-LST limit, and Drift devnet/paper-only boundary are
conservative educational judgments. They reduce exposure but do not guarantee
safety or returns.
