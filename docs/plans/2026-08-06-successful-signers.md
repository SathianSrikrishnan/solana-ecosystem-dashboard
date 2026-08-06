# Successful Signers Implementation Plan

> **For Codex:** Use the executing-plans workflow to implement this plan task-by-task.

**Goal:** Add a second verified adoption metric for all distinct addresses that signed successful non-vote Solana transactions during each of the latest seven complete UTC days.

**Architecture:** Preserve the existing fee-payer query and add a separate public Dune query that expands `solana.transactions.signers`. Parse its CSV through a dedicated standard-library adapter, reject signer counts below the matching fee-payer series, and publish atomically to JSON, Markdown, and static HTML.

**Tech Stack:** DuneSQL/Trino SQL, Python standard library, `unittest`, static HTML/Markdown/JSON.

---

### Task 1: Lock the successful-signers query

**Files:**
- Create: `queries/daily_unique_successful_signers.sql`
- Modify: `tests/test_dune_query.py`

**Step 1: Write the failing query-contract test**

Add a test that requires the new query to:

- read `solana.transactions`;
- expand `signers` with `CROSS JOIN UNNEST`;
- count distinct expanded signer addresses;
- require `success = TRUE`;
- include the latest seven days and exclude the current UTC day;
- group and order by `activity_date`.

**Step 2: Run the focused test and verify RED**

Run:

```powershell
python -m unittest tests.test_dune_query -v
```

Expected: FAIL because `queries/daily_unique_successful_signers.sql` does not exist.

**Step 3: Add the minimal bounded SQL**

Implement the query with this shape:

```sql
SELECT
    block_date AS activity_date,
    COUNT(DISTINCT signer_address) AS unique_successful_signers
FROM solana.transactions
CROSS JOIN UNNEST(signers) AS signer_accounts(signer_address)
WHERE block_date >= CURRENT_DATE - INTERVAL '7' DAY
  AND block_date < CURRENT_DATE
  AND success = TRUE
GROUP BY 1
ORDER BY 1;
```

**Step 4: Run focused and full tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_dune_query -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

**Step 5: Commit**

```powershell
git add tests/test_dune_query.py queries/daily_unique_successful_signers.sql
git commit -m "feat: add bounded successful signers query"
```

### Task 2: Normalize the signer export with TDD

**Files:**
- Modify: `src/solana_observatory/dune_adoption.py`
- Modify: `tests/test_dune_adoption.py`

**Step 1: Write failing adapter tests**

Add tests for a wished-for `parse_daily_successful_signers_csv` function. The
valid case must emit:

```python
{
    "id": "daily_unique_successful_signers",
    "section": "adoption",
    "unit": "wallet addresses",
    "status": "ok",
}
```

It must preserve a sorted seven-point series, Dune provenance, collection
time, source time, and a caveat explaining that addresses are not people and
one transaction may have several signers. Add invalid cases for missing
columns, incomplete dates, duplicates, invalid dates, and negative or
non-integer counts.

**Step 2: Run the focused test and verify RED**

Run:

```powershell
python -m unittest tests.test_dune_adoption -v
```

Expected: FAIL because the new parser is missing.

**Step 3: Implement the minimal parser**

Refactor only the shared CSV/date validation needed by both adoption parsers.
Keep each metric's definition, source method, and caveat explicit. Do not add a
generic metric factory beyond the two verified use cases.

**Step 4: Run focused and full tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_dune_adoption -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

**Step 5: Commit**

```powershell
git add tests/test_dune_adoption.py src/solana_observatory/dune_adoption.py
git commit -m "feat: normalize successful signer exports"
```

### Task 3: Add the atomic import and cross-metric invariant

**Files:**
- Create: `scripts/import_dune_successful_signers.py`
- Modify: `tests/test_import_dune_fee_payers.py`

**Step 1: Write failing command tests**

Add tests proving that a valid signer export updates all three output formats.
Add a failure case where any daily signer count is below the matching
fee-payer count already present in the snapshot. Assert that invalid input
leaves JSON, Markdown, and HTML byte-for-byte unchanged.

**Step 2: Run the focused test and verify RED**

Run:

```powershell
python -m unittest tests.test_import_dune_fee_payers -v
```

Expected: FAIL because the signer import command is missing.

**Step 3: Implement the minimal safe command**

The command must accept explicit `--input`, `--snapshot`, `--output`,
`--source-url`, and `--collected-at` arguments. Parse and validate the full CSV,
compare every overlapping day with
`daily_unique_successful_fee_payers.series`, validate the resulting snapshot,
and only then call `write_reports`.

**Step 4: Run focused and full tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_import_dune_fee_payers -v
python -m unittest discover -s tests -v
```

Expected: all tests pass and the invalid-input fixture leaves outputs intact.

**Step 5: Commit**

```powershell
git add tests/test_import_dune_fee_payers.py scripts/import_dune_successful_signers.py
git commit -m "feat: import successful signers safely"
```

### Task 4: Verify a real Dune result and publish it

**Files:**
- Create: `data/dune/daily_unique_successful_signers_<collection-date>.csv`
- Modify: `output/report.json`
- Modify: `output/report.md`
- Modify: `output/index.html`
- Modify: `docs/METRIC-REGISTRY.md`
- Modify: `docs/LEARNING-LOG.md`
- Modify: `docs/COSTS.md`
- Modify: `docs/NEXT.md`
- Modify: `docs/ROADMAP-PR-MAP.md`
- Modify: `docs/plans/2026-08-06-successful-signers.md`

**Step 1: Run and save the public query**

Create a new public Dune query without changing query `8213434`. Confirm the
seven rows cover the latest complete UTC days and record the exact included
credit cost.

**Step 2: Export and import the verified CSV**

Run the new command with the public query URL and an explicit UTC collection
timestamp. Confirm the signer count is at least the fee-payer count for every
overlapping day.

**Step 3: Update evidence receipts**

Record the query URL, dates, latest value, definition, limitation, Dune credit
cost, and $0 extra-spend status. State that successful signers include fee
payers and may include additional co-signers; neither count represents people.

**Step 4: Run the full completion gate**

Run:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
git diff --check
```

Then verify desktop and mobile HTML in Chromium: two Adoption cards, source
links, visible wallet-not-people caveats after expanding evidence, no horizontal
overflow, and no console errors.

**Step 5: Commit**

```powershell
git add data/dune output docs
git commit -m "feat: publish verified successful signer metric"
```
