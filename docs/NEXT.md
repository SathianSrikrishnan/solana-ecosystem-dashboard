# Next

## Current phase

PR 1 interface shell is complete. PR 2 now shows two verified rungs of the
activity-identity ladder: successful fee payers and successful signers.

## Current build target

Verified foundation:

- public standalone repository on `main`;
- direct no-key Solana RPC collection;
- JSON, Markdown, and standalone dark HTML generation;
- responsive overview, section navigation, source-health visibility, and
  explicit planned states for data slices that have not landed;
- thirty-nine passing foundation, contract, interface, query, adapter, and
  import-command tests;
- a clean six-hour GitHub refresh workflow;
- enforced metric schema `0.2.0` shared by collectors and interfaces.
- an automatic briefing presentation contract with visible grounding metadata
  and an honest unavailable state; generation remains a PR 6 dependency.

## Current product slice

Adoption identity using Jupiter:

- daily unique fee payers;
- daily unique successful signers;
- daily unique Jupiter users;
- overlap between those populations;
- clear limitations before bot classification.

## Next technical phase

Add the next rung of the activity-identity ladder: daily unique Jupiter users,
followed by overlap with the network-wide populations. Preserve the same
bounded query, provenance, failure, and wallet-not-people rules. Then add
retention so the product distinguishes one-time addresses from recurring
activity.

## Parallel learning track

After PR 1 review, define one small onchain exercise that uses the dashboard's
concepts in practice. Keep a separate research note for Solana, Ethereum, and
Bitcoin node operation covering current hardware, bandwidth, uptime, capital,
reward, and maintenance requirements. Do not purchase hardware until that
comparison is complete.

Candidate spin-offs should teach one primitive at a time: a local validator,
wallet and token sandbox, devnet staking concepts, swap routing, or simulated
trading and perpetual-risk mechanics. Prefer devnet, fake balances, and
read-only analysis before any exercise involving real funds.
