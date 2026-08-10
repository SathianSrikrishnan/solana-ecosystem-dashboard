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

## 2026-08-08 - A signer count is broader than a fee-payer count

The verified Dune series found 3,628,019 distinct successful signer addresses
on 2026-08-07, compared with 2,046,280 distinct successful fee-payer addresses.
That difference is plausible because every transaction has a fee payer but can
also require additional signers.

Neither number is a count of people. Comparing the two is useful because it
shows how a definition changes the answer. Application-level users, overlap,
retention, and careful automation signals are the next layers needed before we
can responsibly discuss human participation.

## 2026-08-08 - Application use and return behavior are different signals

On 2026-08-07, Dune's curated Jupiter aggregator table recorded 26,816 distinct
swap signer addresses. Of those, 7,087 had also appeared during the preceding
seven complete days, producing a 26.43% address return rate.

All 26,816 were also successful fee payers in the exact address intersection
for that day, and the same 100% overlap appeared on all seven published days.
That result tells us how Dune's curated `tx_signer` behaves for this table; it
does not prove that every application's signer is always its fee payer. More
importantly, a returning address is still not necessarily a returning person.

## 2026-08-08 - Live and daily metrics must not pretend to share a clock

SOL price can change from minute to minute, while TVL, stablecoin value, and
DEX volume are safer to compare after a UTC day is complete. DeFiLlama's public
responses include a partial row for the current day. The first live test made
that provider behavior visible: rejecting partial data was correct, but
rejecting the whole history was not.

The tested fix ignores only today's partial row, retains the latest fourteen
complete days, and still rejects future or incomplete histories. On the first
verified snapshot, the live SOL price was $76.32 at 16:07 UTC; the 2026-08-07
complete-day readings were $4.707 billion TVL, $16.252 billion circulating
stablecoin value, and $1.363 billion DEX volume. These are four different
measurements, not one verdict on the health of Solana.

## 2026-08-10 - More metrics do not create a reason to return

The dashboard can win initial trust through definitions, sources, freshness,
limitations, and reproducible outputs. Repeat use needs a habit loop: what
changed this week, an archive, alerts, or embeddable cards. Those distribution
features are higher-leverage post-bounty work than adding weakly sourced
metrics. For the release, readability and shareability are the correct scope.
