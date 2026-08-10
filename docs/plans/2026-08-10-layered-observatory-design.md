# Layered Solana Observatory Design

## Product promise

The observatory should let a curious reader move through three layers:

1. **Now:** what is happening across Solana today?
2. **Change:** what moved, what may explain it, and what deserves attention?
3. **Context:** how did Solana arrive here, and which long-term thesis is the
   current evidence supporting or challenging?

It is not a health score, a token-price page, or a collection of unrelated
charts. It is a guided diagnostic whose conclusions remain inspectable.

## Approaches considered

### 1. Current-health monitor

A compact operational dashboard would be easy to scan and maintain. It would
answer whether Solana is functioning, but it would under-serve builders who
want to understand adoption, financial activity, and the network's evolution.

### 2. Historical narrative

A seven-year story would be educational and promotable, but it would age into
a static exhibit and fail the project's promise of a living observatory.

### 3. Layered observatory — selected

Lead with current conclusions, let readers drill into evidence and change, and
finish with historical context. The article uses the same research spine but
remains a separate authored narrative. This gives the bounty a useful product
and gives Sathian a durable learning and publishing asset.

## Six diagnostic questions

### 1. Network — Is Solana working?

Headline candidates: cluster/RPC health, non-vote TPS, successful-transaction
rate, estimated slot time, typical successful-user fee, and incident-free
days. Pair throughput with success and low fees with landing reliability.

### 2. Adoption — Are people and applications returning?

Headline candidates: successful signers, fee payers, new versus returning
addresses, seven-/thirty-day retention, active addresses by application
category, and transparent bot-like activity. Addresses remain explicitly
different from humans.

### 3. Economy — Is useful economic activity growing?

Headline candidates: stablecoin supply, DeFi TVL and net inflows, spot DEX
volume, perpetual volume/open interest, application fees/revenue, and chain
fees/REV. These values are not additive and must retain separate definitions.

### 4. Validators — Is the network resilient and decentralized?

Headline candidates: active/delinquent stake, Nakamoto coefficient, top-ten
and top-twenty-five stake shares, vote participation, client diversity by
stake, and validator economics. Validator count alone is not decentralization.

### 5. Ecosystem — Is Solana continuing to compound?

Headline candidates: active open-source developers, established-developer
retention, active application/category breadth, core releases and deployed
upgrade status, security incidents, and the survival of new projects.

### 6. Financial rails — Is Solana becoming real financial infrastructure?

Headline candidates: non-stablecoin tokenized-asset value, asset-class mix,
issuer/asset breadth, holders and concentration, transfer/trading liquidity,
and the ladder from stablecoin supply to adjusted transfers to identifiable
payments. Stablecoins and other tokenized real-world assets receive separate
totals.

## Page architecture

### Layer 1: Thirty-second overview

The opening shows six compact question cards. Each answers its question with a
one-sentence deterministic reading, one primary metric, one complementary
metric, freshness, and an honest unavailable state. It never compresses the
six questions into one opaque score.

### Layer 2: Diagnostic sections

Every section opens with its human question, a plain-English current reading,
and three to six prioritized cards. Cards show current value, comparison
window, direction, freshness, and status before technical details.

The existing drawer becomes:

- **What this measures** — exact definition;
- **Why it matters** — the decision or thesis it informs;
- **What could fool you** — the main interpretive trap;
- **See the evidence** — source, method, observation time, collection time,
  coverage, and confidence.

### Layer 3: Why now?

A compact timeline links seven eras to today's readings: 2017–2020 invention
and launch; 2021 DeFi/NFT boom; 2022 reliability crisis and market shock;
2023 community-led recovery; 2024 payments/mobile/DePIN/institutional breadth;
2025 uptime/application economics/client diversity; and 2026 stablecoin
settlement/tokenized assets/institutional rails. Foundation claims remain
labeled, and underlying datasets control live metrics.

## Data and interpretation boundary

The deterministic snapshot remains the only measurement source. Each metric
will add an explicit `why_it_matters` field; existing `definition` and `caveat`
become the other two beginner-facing trust explanations. This requires a
schema migration and fixtures, not a renderer-only copy hack.

Deterministic comparison and anomaly records answer what changed. AI may turn
those verified records into a briefing with evidence IDs and uncertainty. If
generation fails, facts and deterministic change summaries still publish.

## Source and failure design

- Public Solana RPC remains the no-key live network/validator core.
- Dune supplies reproducible history, cohorts, attribution, and later bot
  heuristics.
- DeFiLlama remains core only for explicitly tested public endpoints.
- RWA.xyz, Artemis, and developer datasets are optional/authenticated or
  curated until access and terms are verified.
- A failed source disables only affected readings. Planned, unavailable,
  stale, and error remain visibly different states.

## Testing and accessibility

Contract migration, section summaries, card explanations, timeline events,
source failure, comparison periods, and responsive layouts receive tests
before implementation. Keyboard navigation, semantic headings, visible focus,
reduced motion, and narrow-screen behavior remain release requirements.

## Success criteria

- A newcomer can name the six dimensions of Solana health after one minute.
- A reader can explain why each headline matters and how it can mislead.
- Every current claim links to a reproducible measurement or is labeled as
  editorial context.
- The page distinguishes current value, recent change, and historical context.
- The article and dashboard cite the same evidence without copying each
  other's job.
