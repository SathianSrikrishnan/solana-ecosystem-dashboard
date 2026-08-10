# Layered Solana Observatory Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the existing source-visible dashboard into a six-question layered observatory that explains current state, recent change, and seven-year context.

**Architecture:** Migrate the normalized contract to carry a per-metric `why_it_matters` explanation, then render six human-question sections from the same verified snapshot. Add deterministic comparison and editorial timeline records as separate typed inputs; public RPC and existing adapters remain measurement truth, while authenticated RWA/developer sources stay optional.

**Tech Stack:** Python 3.11 standard library, static JSON/Markdown/HTML, Solana JSON-RPC, Dune exports, DeFiLlama public endpoints, `unittest`.

---

### Task 1: Migrate the metric contract to beginner explanations

**Files:**
- Modify: `src/solana_observatory/contracts.py`
- Modify: `src/solana_observatory/snapshot.py`
- Modify: `src/solana_observatory/dune_adoption.py`
- Modify: `src/solana_observatory/economy.py`
- Modify: `tests/test_contracts.py`
- Modify: all metric fixtures under `tests/`

**Steps:**

1. Write a failing contract test requiring `why_it_matters` and schema `0.3.0`.
2. Run `python -m unittest tests.test_contracts -v` and observe the expected failure.
3. Add the required field and migrate each production metric with one concrete, beginner-readable sentence.
4. Update fixtures without weakening validation.
5. Run the focused and full suites.
6. Commit as `feat: add beginner metric explanations`.

### Task 2: Render six human-question sections

**Files:**
- Modify: `src/solana_observatory/contracts.py`
- Modify: `src/solana_observatory/renderers.py`
- Modify: `tests/test_renderers.py`
- Modify: `tests/test_contracts.py`

**Steps:**

1. Write failing tests for the six questions, including `financial_rails` as a valid section.
2. Require each populated section to show a current reading and each empty section to list the next expected evidence rather than generic filler.
3. Change card details to “What this measures,” “Why it matters,” “What could fool you,” and “See the evidence.”
4. Keep semantic headings, keyboard-accessible details, source links, status, and freshness.
5. Run renderer, contract, and full tests.
6. Commit as `feat: organize dashboard around six health questions`.

### Task 3: Add deterministic comparison records

**Files:**
- Create: `src/solana_observatory/comparisons.py`
- Create: `tests/test_comparisons.py`
- Modify: `src/solana_observatory/contracts.py`
- Modify: `src/solana_observatory/renderers.py`
- Modify: `tests/test_renderers.py`

**Steps:**

1. Write failing tests for latest-seven versus preceding-seven change, insufficient history, zero baselines, and mismatched grains.
2. Implement pure calculations that emit value, percent change when valid, direction, windows, and evidence metric ID.
3. Validate comparison records separately from measurements.
4. Render “changed by,” exact windows, and unavailable states without calling change good or bad.
5. Run focused and full suites.
6. Commit as `feat: add deterministic metric comparisons`.

### Task 4: Publish the seven-era “Why now?” timeline

**Files:**
- Create: `src/solana_observatory/timeline.py`
- Create: `tests/test_timeline.py`
- Modify: `src/solana_observatory/renderers.py`
- Modify: `tests/test_renderers.py`
- Create: `data/history/solana_timeline.json`

**Steps:**

1. Write failing tests requiring seven ordered eras, dates, short descriptions, source URLs, source type, and a distinction between fact and interpretation.
2. Create the reviewed timeline from the primary-source research note.
3. Render a compact history band after the live diagnostic sections.
4. Label Foundation-reported statistics and do not include an unsourced FTX narrative.
5. Test mobile order, links, and HTML escaping.
6. Commit as `feat: add sourced Solana history timeline`.

### Task 5: Build validator depth from public RPC

**Files:**
- Create: `src/solana_observatory/validator_depth.py`
- Create: `tests/test_validator_depth.py`
- Modify: `src/solana_observatory/snapshot.py`
- Modify: `tests/test_snapshot.py`
- Modify: `scripts/generate.py`

**Steps:**

1. Write failing tests for active/delinquent stake, delinquent stake share, top-ten/top-twenty-five stake share, superminority/Nakamoto coefficient, commissions, and vote-credit coverage.
2. Handle zero stake, duplicate vote accounts, invalid stake, and unknown operator identity.
3. Normalize provenance-rich validator metrics without calling vote accounts distinct operators.
4. Merge them into scheduled refreshes without erasing adoption/economy data.
5. Run live bounded evidence collection and reconcile outputs.
6. Commit the adapter, then the reviewed snapshot and methodology separately.

### Task 6: Test fees, application revenue, and REV sources

**Files:**
- Create: `docs/research/2026-08-10-SOLANA-FEES-REV-ENDPOINT-TEST.md`
- Create only after source approval: `src/solana_observatory/economic_value.py`
- Create only after source approval: `tests/test_economic_value.py`

**Steps:**

1. Distinguish chain fees, app fees, app revenue, and REV in the source test.
2. Probe documented/free endpoint behavior, rate limits, historical grain, and failure shape.
3. Recommend build, optional adapter, or defer for each metric.
4. Implement only approved, reproducible metrics with parser tests first.
5. Commit research before any adapter implementation.

### Task 7: Design the optional RWA and payments adapter

**Files:**
- Create: `docs/plans/2026-08-10-financial-rails-adapter-design.md`
- Create after access decision: adapter and tests under `src/solana_observatory/` and `tests/`

**Steps:**

1. Request no external account or paid access without Sathian's action-time approval.
2. Define stablecoins separately from non-stablecoin RWAs.
3. Define value, asset-class mix, issuer concentration, holders, liquidity, raw transfers, adjusted transfers, and identifiable payments.
4. Select RWA.xyz/Artemis optional access, Dune/onchain reconstruction, or a dated research snapshot.
5. Implement only after the access and licensing decision, with visible optional-source failure.

### Task 8: Integrate grounded anomaly and AI briefing layers

**Files:**
- Create: `src/solana_observatory/anomalies.py`
- Create: `tests/test_anomalies.py`
- Modify: AI analysis contract and renderer tests

**Steps:**

1. Write deterministic anomaly tests before AI integration.
2. Emit direction-neutral anomaly records with window, threshold, metric ID, and known gaps.
3. Allow AI to read only validated snapshots, comparisons, anomalies, and timeline context.
4. Require evidence IDs, uncertainty, generation time, model, and failure state.
5. Verify that deterministic reports still publish when AI fails.

### Task 9: Article and release package

**Files:**
- Expand: `docs/articles/2026-08-10-seven-years-of-solana-outline.md`
- Create later: final article draft and media manifest
- Modify later: release/demo/submission documentation

**Steps:**

1. Capture Sathian's real opening moment and clarify “Fort Kobhi.”
2. Draft the 800–1,500 word article in Writer phase, then run Critic phase.
3. Obtain Sathian's outline and red-line approval before final images.
4. Source or generate the approved visual map; include at least one personal photo and verify rights/captions.
5. Link article and observatory in both directions.
6. Host, publish, or submit only with explicit action-time approval.
