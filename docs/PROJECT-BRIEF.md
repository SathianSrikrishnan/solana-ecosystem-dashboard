# Project Brief

## Goal

Create a genuinely useful Solana ecosystem observatory that remains valuable
after the bounty. It should support Sathian's learning, portfolio, content,
future hackathons, and decisions about where to build in Solana.

## Primary product promise

Within 30 seconds, a visitor should understand:

- whether the network appears healthy;
- what changed recently;
- what signals deserve investigation;
- how fresh and trustworthy each signal is.

## Audience hypothesis

Primary: beginner-to-intermediate Solana builders becoming informed ecosystem
participants. They want to understand what changed, what the measurements
actually mean, and where to spend attention.

Secondary:

- ecosystem operators monitoring health and growth;
- founders comparing product categories;
- analysts and investors looking for evidence;
- writers seeking verified story leads;
- newcomers learning how Solana works.

## Winning standard

- Understandable in 30 seconds.
- Trustworthy in 2 minutes.
- Runnable in 5 minutes.
- Live, responsive, and gracefully degraded when a source fails.
- Original multi-signal analysis rather than a pile of copied charts.

## Technical direction

1. A no-key Python standard-library core collects direct Solana RPC data.
2. Free/keyless sources add market and TVL context where terms permit.
3. Dune supplies deeper historical and adoption metrics.
4. A normalized JSON model records value, unit, definition, source, freshness,
   confidence, and caveats.
5. Markdown and standalone HTML are generated from the same verified model.
6. A scheduled AI analyst automatically explains verified changes and proposes
   labeled hypotheses. PR 6 will implement generation; deterministic reports
   remain the source of truth and still publish when analysis is unavailable.

## Deadline

Submission deadline: 2026-08-17 at 23:59 America/Toronto.

## Current product milestone

The release candidate uses normalized schema `0.3.0` and 45 metrics across
Network, Adoption, Economy, Validators, Ecosystem, and Financial Rails. Forty-
one metrics report live and four important gaps remain explicit because their
dependable sources require authentication or a stronger attribution contract.
The product includes deterministic comparisons, anomaly review, an evidence-
bound briefing, a sourced seven-era history, mobile/desktop QA, and automated
Axe checks. Deployment and bounty submission still require Sathian's approval.

## Builder learning goals

This project should also help Sathian move from reading about blockchains to
doing basic, verifiable work on Solana. That includes understanding wallets,
transactions, staking, RPCs, validators, and the operational trade-offs behind
running blockchain infrastructure.

Exploring Solana, Ethereum, and Bitcoin node hardware is a related learning
track, not a requirement for the bounty. We will research current hardware,
bandwidth, uptime, staking, reward, and cost requirements before buying
equipment or presenting node operation as an investment.

The broader builder thesis is that low-cost, high-speed financial rails will
create durable opportunities in payments, decentralized finance, staking, and
new applications. The dashboard is the evidence layer for approaching those
opportunities: learn the primitives, verify the data, build small experiments,
and only then introduce real infrastructure or capital.
