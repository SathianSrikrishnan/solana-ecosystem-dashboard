# Learning Log

## 2026-07-27 — Why ecosystem analytics is difficult

A blockchain is a public event ledger, not a finished analytics product. It can
show which wallet signed a transaction, but not whether that wallet represents
one human, several humans, a bot, or a business system.

## 2026-07-27 — What Dune does

Dune organizes blockchain history into queryable tables. SQL turns a precise
question into a result, and the result can become a chart, scheduled query, or
API input.

The difficult work is defining the question. "Daily active users" can mean
senders, successful signers, application users, likely humans, or other useful
but different populations.

## 2026-07-27 — The agent boundary

Agents can find tables, draft SQL, execute collectors, test code, and produce
reports. Sathian owns purpose, definitions, plausibility checks, and product
judgment.

## 2026-07-27 — The market already has strong pieces

Solana Data, growthepie, L2BEAT, Artemis, and Token Terminal prove that serious
ecosystem analytics products exist. A plain metrics dashboard would be a weak
entry. The differentiated product must connect transparent measurements to
identity nuance, live health, anomalies, explanations, and decisions.

## 2026-07-28 — Activity is an identity ladder

Fee payers, successful signers, application users, likely bots, and likely
human-controlled wallets answer different questions. We will display them as a
ladder and add retention rather than selecting one number and calling it users.

## 2026-07-28 - Why the shared contract comes first

Collectors and the interface can be built separately only when they agree on
the shape of a metric. The contract is the labeled box every source must fill.
Validation prevents a chart from quietly showing a number with no definition,
source, freshness, or limitation.

## 2026-07-30 - A dashboard shell can be honest before it is complete

An unfinished section should not disappear or borrow placeholder numbers. A
visible "data adapter planned" state teaches the reader what the product will
cover while preserving the boundary between verified facts and future work.
The same principle applies to source failure: "Not available" is information;
an invented zero is misinformation.

## 2026-08-03 - AI can be automatic without becoming the source of truth

The interface can promise an automatic explanation while preserving a hard
boundary: validated metrics are evidence, and AI is interpretation. A grounded
briefing identifies its supporting metric IDs, uncertainty, generation time,
and model. If no valid briefing exists, the dashboard says so and still
publishes the deterministic report.

## 2026-08-03 - A wallet count is useful when its boundary is visible

Our first Dune query found 2,252,879 distinct successful fee-paying addresses
on 2026-08-03, the latest complete UTC day at collection time. This does not
mean 2,252,879 people used Solana. It means that many distinct primary signer
addresses paid for at least one successful, non-vote transaction.

The distinction matters because one human or bot can control many addresses,
while a relayer can pay for another user's transaction. The metric is a useful
lower-level activity signal, and later signer, application, overlap, and
retention views will add context rather than relabeling it as users.
