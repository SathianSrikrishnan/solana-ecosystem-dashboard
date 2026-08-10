# Decision Log

## Locked

### 2026-07-27 — Treat this as an enduring product

The dashboard is not a disposable bounty mockup. It should remain useful for
learning, portfolio proof, future Solana hackathons, research, and content.

### 2026-07-27 — Use a standalone project

The source code and deployment live independently from the personal-site
repository. Sathian's site will later link to or feature the product.

### 2026-07-27 — Keep a no-cost, no-key core

Direct Solana RPC and standard-library report generation form the dependable
base. Authenticated and paid services are optional enhancements.

### 2026-07-27 — Separate facts from AI interpretation

Deterministic collectors own metrics. AI may summarize verified facts, identify
relationships, and draft explanations with citations and uncertainty.

### 2026-07-28 — Set a $20 X research budget

Sathian approved a hard $20 X API cap for targeted ecosystem research.
Auto-recharge stays disabled, posts are cached, and X remains optional rather
than a dependency for core health reporting. Sathian will top up the existing X
balance only if required.

### 2026-07-28 — Use Jupiter for the first application study

The first Dune adoption slice will compare network-level fee payers and
successful signers with wallets using Jupiter. Jupiter is a useful first case
because its substantial routing and trading activity exposes the difference
between app usage, direct usage, aggregators, humans, and automation.

### 2026-07-28 - Lock one shared metric contract

Every collector and interface uses schema version `0.2.0`. Each metric carries
a stable ID, dashboard section, value, definition, source, collection time,
source time, status, confidence, caveat, and optional historical series. The
pipeline rejects incomplete metrics before publishing any report.

### 2026-07-30 - Use a progressive observatory shell

The interface opens with three current signals and source health, then groups
all normalized metrics by product section. Future sections stay visible as
honest planned states instead of sample or invented data. Facts and
interpretation use separate visual containers, and an unavailable measurement
renders as "Not available" rather than zero.

### 2026-07-30 - Design first for the curious Solana builder

The primary reader is a beginner-to-intermediate builder becoming an informed
Solana participant. The interface should help that reader understand what
changed, what each measurement actually means, and what deserves investigation
without assuming analyst or validator-operator knowledge. Operator, investor,
and writer use cases remain secondary.

### 2026-07-30 - Balance the three opening questions

The opening screen should answer one question from each layer of the ecosystem:

1. Is the Solana network functioning properly?
2. Is application and wallet activity growing or returning?
3. Is meaningful economic activity increasing?

Each question may use a small set of component signals rather than pretending
one metric is a complete health score. Exact headline metrics can change as
verified data slices land.

### 2026-07-30 - Default to a seven-day comparison

The interface compares the latest seven complete days with the preceding seven
days by default. This is responsive enough to reveal meaningful movement while
reducing the noise of a single day. Thirty-day and ninety-day views provide
deeper context where historical data is available.

### 2026-07-30 - Make grounded AI explanation automatic

Every completed snapshot should include an automatic plain-English briefing.
AI is the product's interpretation layer, not an optional accessory. It may
only receive validated metrics and deterministic changes or anomalies; it
cannot invent, backfill, or alter measurements.

The briefing must remain visually distinct from verified facts and expose its
generation time, supporting measurements, uncertainty, and known gaps. If AI
generation fails, the deterministic dashboard still publishes and shows the
explanation as unavailable rather than hiding the failure.

### 2026-07-30 - Do not publish an opaque health score

The product will not compress network operation, adoption, and economic
activity into one numerical score. The opening view uses transparent component
signals and an automatic plain-English briefing. Readers can inspect the
measurements behind every conclusion instead of trusting subjective hidden
weights.

## Open

- Final product name and domain.
- First monitored X account list.
- Hosting provider and production schedule.

## 2026-08-10 — Use a six-question layered observatory

Sathian approved a layered product organized around Network, Adoption,
Economy, Validators, Ecosystem, and Financial Rails. The experience moves from
current conditions to recent change to seven-year context. Tokenized assets
and payments are first-class rather than being buried inside DeFi TVL.

The dashboard and article share evidence but not purpose: the dashboard is a
living deterministic diagnostic, while the article is Sathian's authored
account of learning Solana by building the instrument panel.

### 2026-08-10 — Separate data reliability from network meaning

An `ok` collector status means data is reporting; it is not a green verdict on
Solana. Seven-day comparison arrows remain direction-neutral. Green, yellow,
and red conclusions are reserved for metrics with explicit, documented
benchmarks where good and bad direction can be defended.

### 2026-08-10 — Keep the article short and defer it

The article will be drafted only after the dashboard is feature-complete. It
will target 325-450 words and frame Solana through low cost, ease of learning,
ease of building, maturation beyond its scam/meme-coin reputation, and its
potential as financial rails. Tooth Fairy Network is the concrete build story;
future product features remain labeled as planned.

### 2026-08-10 - Keep fees, revenue, REV, transfers, and payments distinct

The no-key core publishes chain fees, application fees, application revenue,
and REV as separate measurements. REV is transparently derived from chain fees
plus tracked gross Jito tips. Stablecoin circulating value remains separate
from transfer volume, and raw transfers are never labeled as payments.

RWA.xyz stays an optional authenticated adapter. Identifiable payment volume
stays visibly unavailable until a repeatable attribution source with a clear
coverage boundary exists.

### 2026-08-10 - Do not scrape RWA.xyz or hide stale Dune results

RWA.xyz's no-key API rejects requests, while full API and redistribution rights
require an enterprise agreement. The release will keep the RWA card explicitly
unavailable rather than scraping a public page or relabeling dated press-release
figures as live data.

Dune stored results must cover the latest seven complete UTC days. When they do
not, the scheduled pipeline preserves their provenance but marks only the Dune
metrics stale. Query execution remains bounded and credit-gated.
