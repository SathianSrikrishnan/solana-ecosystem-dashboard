# Economy Panel Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Publish live SOL price plus latest-complete-day Solana TVL, stablecoin value, and DEX volume from free public sources with independent failure states.

**Architecture:** Pure standard-library parsers normalize bounded CoinGecko and DeFiLlama responses into schema `0.2.0`. A small HTTP client fetches each source independently, and one refresh command merges successful or visibly unavailable metrics into the prior snapshot before atomically regenerating JSON, Markdown, and HTML.

**Tech Stack:** Python standard library, CoinGecko Public API, DeFiLlama free API, `unittest`, static JSON/Markdown/HTML.

---

### Task 1: Lock and normalize live SOL price

**Files:**
- Create: `src/solana_observatory/economy.py`
- Create: `tests/test_economy.py`

**Step 1: Write the failing test**

Create a minimal CoinGecko fixture containing `usd`, `usd_24h_change`, and
`last_updated_at`. Require a wished-for `parse_coingecko_sol_price` function to
return `sol_price_usd` with section `economy`, USD unit, live source time,
CoinGecko provenance, collection time, high confidence, no fake series, and a
caveat that price is not network usage. Add invalid cases for missing Solana,
non-numeric/negative price, missing timestamp, future source time, a naive
collection time, and a non-CoinGecko source URL.

**Step 2: Run the test to verify RED**

Run: `python -m unittest tests.test_economy.EconomyParserTests -v`

Expected: FAIL because the module or parser does not exist.

**Step 3: Implement the minimal parser**

Validate the timezone-aware collection timestamp and public CoinGecko URL.
Accept finite positive USD price, finite 24-hour percentage change, and an
integer Unix source timestamp no later than collection time. Preserve the
change in an optional metric metadata field only if schema validation permits;
otherwise keep the first production slice to the price metric alone.

**Step 4: Run focused tests to verify GREEN**

Run: `python -m unittest tests.test_economy.EconomyParserTests -v`

Expected: all CoinGecko parser tests pass.

**Step 5: Commit**

```powershell
git add tests/test_economy.py src/solana_observatory/economy.py
git commit -m "feat: normalize live SOL price"
```

### Task 2: Normalize complete-day DeFiLlama economy series

**Files:**
- Modify: `src/solana_observatory/economy.py`
- Modify: `tests/test_economy.py`

**Step 1: Write failing tests**

Create minimal fourteen-day fixtures for:

- `historicalChainTvl/Solana` rows with `date` and `tvl`;
- `stablecoincharts/Solana` rows with `date` and `totalCirculatingUSD`;
- `overview/dexs/Solana` with `totalDataChart` timestamp/value pairs.

Require a wished-for `parse_defillama_economy` function to return exactly
`solana_defi_tvl_usd`, `solana_stablecoin_value_usd`, and
`solana_dex_volume_usd`. Each metric must publish the latest complete UTC day,
fourteen sorted points, DeFiLlama provenance, exact endpoint method, freshness,
and a plain-English caveat.

Add invalid cases for missing fields, duplicate/missing dates, negative or
non-finite values, future/current-day points, stale latest dates, non-daily
gaps, and a non-DeFiLlama URL.

**Step 2: Run the test to verify RED**

Run: `python -m unittest tests.test_economy.EconomyParserTests -v`

Expected: FAIL because the DeFiLlama parser does not exist.

**Step 3: Implement the minimal parser**

Use one shared complete-day series validator. Convert Unix seconds to UTC
dates, require the fourteen days ending one day before collection, and round
currency values to two decimals. Stablecoin value is the sum of all finite,
non-negative values inside `totalCirculatingUSD` for each day. DEX chart rows
are timestamp/value pairs; ignore provider summary fields so partial rolling
windows cannot replace complete days.

**Step 4: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_economy.EconomyParserTests -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

**Step 5: Commit**

```powershell
git add tests/test_economy.py src/solana_observatory/economy.py
git commit -m "feat: normalize Solana economy series"
```

### Task 3: Fetch sources with independent failure behavior

**Files:**
- Create: `src/solana_observatory/economy_client.py`
- Create: `tests/test_economy_client.py`

**Step 1: Write failing client tests**

Use an injected opener to prove the client sends a user agent, enforces a
timeout, decodes JSON objects/lists, and rejects HTTP, malformed JSON, and
unexpected top-level shapes. Prove the high-level collection function returns
successful CoinGecko and DeFiLlama payloads independently rather than failing
all sources when one request fails.

**Step 2: Run the test to verify RED**

Run: `python -m unittest tests.test_economy_client -v`

Expected: FAIL because the client does not exist.

**Step 3: Implement the minimal client**

Use `urllib.request.Request` and an injected `urlopen`-compatible callable.
Define endpoint constants for CoinGecko simple price, DeFiLlama historical TVL,
stablecoin history, and DEX overview. No key, query secret, retry loop, or paid
fallback belongs in this core.

**Step 4: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_economy_client -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

**Step 5: Commit**

```powershell
git add tests/test_economy_client.py src/solana_observatory/economy_client.py
git commit -m "feat: collect public economy sources"
```

### Task 4: Refresh the report without hiding source failures

**Files:**
- Create: `scripts/refresh_economy.py`
- Create: `tests/test_refresh_economy.py`
- Modify: `.github/workflows/refresh.yml`

**Step 1: Write failing command tests**

Prove a successful refresh adds all four metrics to JSON, Markdown, and HTML.
Then simulate one source failure and prove only the affected metric is
`unavailable`, its value is `null`, the attempted source and error caveat are
visible, and the other metrics remain `ok`. Prove invalid snapshots leave
existing output files untouched. Add a workflow test that the scheduled job
runs the economy refresh after the RPC refresh.

**Step 2: Run tests to verify RED**

Run: `python -m unittest tests.test_refresh_economy -v`

Expected: FAIL because the command does not exist.

**Step 3: Implement the refresh**

Load the prior JSON snapshot, collect each source, normalize valid payloads,
and build unavailable metrics for isolated failures. Render all output strings
before replacing report files. Do not print secrets or accept paid credentials.

**Step 4: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_refresh_economy -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

**Step 5: Commit**

```powershell
git add scripts/refresh_economy.py tests/test_refresh_economy.py .github/workflows/refresh.yml
git commit -m "feat: refresh economy metrics with graceful degradation"
```

### Task 5: Capture live evidence and publish the economy panel

**Files:**
- Create: `data/economy/economy_snapshot_2026-08-08.json`
- Modify: `output/report.json`
- Modify: `output/report.md`
- Modify: `output/index.html`
- Modify: `docs/METRIC-REGISTRY.md`
- Modify: `docs/LEARNING-LOG.md`
- Modify: `docs/COSTS.md`
- Modify: `docs/NEXT.md`
- Modify: `docs/ROADMAP-PR-MAP.md`
- Modify: `docs/plans/2026-08-08-economy-panel.md`

**Step 1: Run one bounded live refresh**

Capture collection time, endpoint URLs, latest complete source date, the four
values, and request cost. Save only the compact reviewed source fields needed
to reproduce the metrics; do not archive full third-party responses.

**Step 2: Reconcile the rendered outputs**

Confirm cards, Markdown, and JSON agree exactly. Record current/live versus
latest-complete-day grains and never compare them as though they share a
timestamp.

**Step 3: Update methodology and learning receipts**

Document definitions, freshness, limitations, free/keyless status, source
failure behavior, and why partial-day stablecoin data was excluded.

**Step 4: Run completion verification**

Run:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
git diff --check
```

Use the already-open local preview for manual visual inspection because the
controlled Chrome security policy blocks direct `file:` navigation. Verify four
Economy cards, source links, expandable caveats, no horizontal overflow, and
readable narrow layout.

**Step 5: Commit**

```powershell
git add data/economy output docs
git commit -m "feat: publish verified Solana economy panel"
```

### Task 6: Research fees, REV, and tokenized assets

**Files:**
- Create: `docs/research/SOLANA-FEES-REV-RWA-SOURCES.md`

**Step 1: Compare source definitions**

Distinguish chain transaction fees, application fees, chain revenue, REV, and
RWA active market cap. Confirm whether each required free endpoint is public,
documented, stable enough to automate, and consistent with DeFiLlama's visible
Solana page.

**Step 2: Record the next implementation decision**

Recommend build, optional adapter, or defer for each metric. Do not publish
values whose free source cannot be reproduced or whose definition remains
ambiguous.

**Step 3: Commit**

```powershell
git add docs/research/SOLANA-FEES-REV-RWA-SOURCES.md
git commit -m "docs: research advanced economy metrics"
```

## Execution status

- Tasks 1-3 completed and committed.
- Task 4 completed: independent source failure states, tested refresh command,
  scheduled refresh integration, and preservation of prior verified metrics.
- Task 5 completed locally: bounded live evidence, four Economy cards, and
  methodology/cost/learning receipts. Manual visual review is the checkpoint.
- Task 6 remains next after visual review.
