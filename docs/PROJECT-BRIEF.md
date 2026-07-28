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

Primary: curious Solana builders who want to choose where to spend attention.

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
6. An optional AI analyst explains verified changes and proposes hypotheses.

## Deadline

Submission deadline: 2026-08-17 at 23:59 America/Toronto.

