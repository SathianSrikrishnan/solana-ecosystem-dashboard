# Solana Ecosystem Dashboard Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a no-key foundation that collects real Solana network health
data and generates JSON, Markdown, and standalone HTML from one verified model.

**Architecture:** Python standard-library collectors call Solana JSON-RPC
through an injectable HTTP transport. A normalizer creates provenance-rich
metric records. Renderers use that single snapshot for every output so numbers
cannot silently disagree between formats.

**Tech Stack:** Python 3 standard library, `unittest`, vanilla HTML/CSS/JS,
GitHub Actions for later scheduling.

---

### Task 1: Establish durable project controls

**Files:**
- Create: `AGENTS.md`
- Create: `README.md`
- Create: `docs/PROJECT-BRIEF.md`
- Create: `docs/DECISIONS.md`
- Create: `docs/LEARNING-LOG.md`
- Create: `docs/NEXT.md`
- Create: `docs/METRIC-REGISTRY.md`
- Create: `docs/COSTS.md`

**Steps:**

1. Record the product promise and deadline.
2. Record the standalone-project and no-key-core decisions.
3. Record the one-decision-at-a-time learning rule.
4. Review the files for contradictions.
5. Commit the documentation.

### Task 2: Define the snapshot behavior with failing tests

**Files:**
- Create: `tests/test_snapshot.py`
- Create: `src/solana_observatory/snapshot.py`

**Steps:**

1. Write a test asserting RPC responses become provenance-rich metrics.
2. Run `python -m unittest discover -s tests -v`.
3. Confirm failure because `solana_observatory.snapshot` does not exist.
4. Implement only the transformation required by the test.
5. Run the test suite and confirm it passes.

### Task 3: Define direct RPC collection with failing tests

**Files:**
- Create: `tests/test_rpc.py`
- Create: `src/solana_observatory/rpc.py`

**Steps:**

1. Write a fake transport test for JSON-RPC request shape and error handling.
2. Run the test and confirm the RPC client is missing.
3. Implement `SolanaRpcClient.call(method, params)`.
4. Add calls for health, slot, block height, epoch info, performance samples,
   vote accounts, and supply.
5. Run the full test suite.

### Task 4: Define reports with failing tests

**Files:**
- Create: `tests/test_renderers.py`
- Create: `src/solana_observatory/renderers.py`

**Steps:**

1. Write tests for JSON, Markdown, and HTML outputs.
2. Require each output to include generation time, source, and status.
3. Run tests and confirm they fail because renderers are missing.
4. Implement minimal renderers.
5. Run the full test suite.

### Task 5: Add the generation command

**Files:**
- Create: `scripts/generate.py`

**Steps:**

1. Write an end-to-end test using a fixture transport.
2. Run it and confirm failure because the command is missing.
3. Implement generation into `output/`.
4. Run against the live public RPC.
5. Inspect freshness, values, and source receipts.

### Task 6: Add free economic context

**Files:**
- Create: `tests/test_market.py`
- Create: `src/solana_observatory/market.py`

**Steps:**

1. Test CoinGecko price and DeFiLlama TVL normalization with saved fixtures.
2. Implement keyless HTTP adapters with timeouts, caching, and visible errors.
3. Add attribution and licensing notes.
4. Run tests and a live collection.

### Task 7: Add scheduled refresh safely

**Files:**
- Create: `.github/workflows/refresh.yml`

**Steps:**

1. Add a scheduled workflow that generates reports without paid services.
2. Add a manual trigger.
3. Prevent overlapping refreshes.
4. Run locally and inspect the generated diff.
5. Enable only after the public repository and hosting route are approved.

### Task 8: Build the first Dune learning slice

**Files:**
- Create: `dune/activity-identities.sql`
- Create: `docs/ACTIVITY-IDENTITIES.md`
- Create: `tests/test_dune_result.py`

**Steps:**

1. Define sender, successful signer, application user, likely bot, and likely
   human as separate measurements.
2. Write the SQL in small reviewed sections.
3. Validate a bounded date range manually in Dune.
4. Export a fixture and test the normalized result.
5. Add the Dune result as an optional module with visible freshness.

### Task 9: Add deterministic anomaly detection

**Files:**
- Create: `tests/test_anomalies.py`
- Create: `src/solana_observatory/anomalies.py`

**Steps:**

1. Test threshold and rolling-baseline alerts.
2. Distinguish source failure from a real network anomaly.
3. Add severity, evidence, and plain-English caveats.
4. Run historical fixture tests before enabling live alerts.

### Task 10: Add an optional AI analyst

**Files:**
- Create: `docs/AI-ANALYST-CONTRACT.md`
- Create: `tests/test_ai_contract.py`
- Create: `src/solana_observatory/ai_contract.py`

**Steps:**

1. Define the verified JSON input and citation-required output schema.
2. Reject unsupported numeric claims.
3. Require uncertainty labels for causal hypotheses.
4. Keep AI failure from affecting deterministic outputs.

### Task 11: Polish and submit

**Files:**
- Modify: `README.md`
- Create: `docs/SUBMISSION-CHECKLIST.md`
- Create: `docs/DEMO-SCRIPT.md`

**Steps:**

1. Verify the bounty requirements line by line.
2. Test a clean Windows setup.
3. Verify mobile and desktop dashboard behavior.
4. Record a short demo.
5. Prepare the Superteam submission without submitting it.

