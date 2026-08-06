# Solana Activity Map Design

## Goal

Extend the observatory from one adoption number into a behavior-first map of
what distinct Solana addresses are doing: signing successful transactions,
swapping, lending, trading perpetuals, staking, paying, and participating in
digital-asset markets.

The map must remain beginner-readable without calling addresses people or
claiming wallet-brand attribution that the blockchain does not contain.

## Product model

The Adoption section will have three layers:

1. **Identity ladder** - successful fee payers and all successful signers.
2. **Activity map** - comparable category cards for swaps, lending, perpetuals,
   liquid staking, payments, and later NFT activity.
3. **Wallet access context** - Phantom and Solflare explained as important
   signing interfaces, with no fabricated onchain active-user counts.

The first application panel will cover Jupiter Swap, Raydium pool execution,
Kamino Lending, Drift perpetuals, and direct JitoSOL/Marinade staking. Stablecoin
payments follow as a behavior category. NFT transfers can join later after the
core financial paths are trustworthy.

## Attribution rules

Every application metric names a precise action and unit. A card may count
distinct signing addresses, swaps, trade legs, fills, deposits, borrows, or USD
volume, but it may not use the generic label "users" without defining the
underlying address rule.

Direct app entry and protocol reach stay separate. A top-level Jupiter action
that invokes Raydium internally proves that Raydium liquidity was used; it does
not prove that the signer opened Raydium. Cards may overlap and must never be
summed into a total population. Exact program IDs, included instructions,
source tables, collection times, and known gaps belong in metric provenance.

Phantom and Solflare do not receive deterministic onchain user counts because
ordinary Solana transactions do not record the signing wallet software.
First-party aggregate telemetry may be shown later as a separate offchain
source if its methodology and freshness are documented.

## Architecture and data flow

Each behavior lands as a small vertical slice:

1. Commit a bounded Dune query for the latest seven complete UTC days.
2. Run it manually through the free/no-key path and preserve the public URL.
3. Validate the exported CSV completely with Python's standard library.
4. Compare related metrics where a safe invariant exists.
5. Publish the normalized metric only after the full snapshot validates.
6. Render the same evidence in JSON, Markdown, and standalone HTML.

Successful signers are the next slice. It expands each successful non-vote
transaction's `signers` array, counts distinct signing addresses per day, and
must never be lower than the corresponding fee-payer count for the same day.
The original fee-payer query and result remain untouched.

Application metrics should prefer Dune curated or decoded tables when their
methodology matches the question. Raw program-call queries are acceptable only
when the included programs, instructions, and inner-call behavior are pinned.

## Failure behavior and testing

Missing, malformed, incomplete, duplicate, or negative observations fail
before any report file changes. A source outage produces a visible unavailable
or stale state rather than zero. A failed cross-metric invariant blocks the
import and preserves the prior snapshot.

Every behavior change follows red-green-refactor. Tests lock query bounds,
columns, success filters, parser validation, cross-metric invariants, atomic
output behavior, provenance, rendering, mobile layout, and visible caveats.
Real-data plausibility checks are receipts, not substitutes for automated
tests.

## Delivery sequence

1. Daily unique successful signers.
2. Jupiter Swap traders and swap activity.
3. Raydium execution activity with routing caveat.
4. Kamino lending actions.
5. Drift perpetual traders and fills.
6. Direct JitoSOL and Marinade staking actions.
7. Stablecoin payment activity.
8. Cross-category overlap and returning-address retention.

The supporting attribution research is recorded in
`docs/research/SOLANA-APP-ATTRIBUTION.md`.
