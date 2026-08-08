# Next

## Current phase

PR 1 interface shell is complete. PR 2's verified adoption ladder now shows
successful fee payers, successful signers, Jupiter Swap signers, exact
fee-payer overlap, and seven-day return rate.

## Current build target

Verified foundation:

- public standalone repository on `main`;
- direct no-key Solana RPC collection;
- JSON, Markdown, and standalone dark HTML generation;
- responsive overview, section navigation, source-health visibility, and
  explicit planned states for data slices that have not landed;
- forty-six passing foundation, contract, interface, query, adapter, and
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

Review and merge the completed PR 2 adoption slice, then build PR 3's economy
signals: SOL price, TVL, stablecoins, DEX volume, fees, REV, and tokenized
assets. Keep public/keyless sources primary and display source failures rather
than substituting zeros. Bot classification remains later work built on these
verified base populations.

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
