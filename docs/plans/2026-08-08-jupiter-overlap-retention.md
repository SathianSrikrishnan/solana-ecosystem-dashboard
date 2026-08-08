# Jupiter Overlap and Retention Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add verified daily Jupiter Swap signer, fee-payer overlap, and seven-day return-rate metrics without calling wallet addresses people.

**Architecture:** One bounded public Dune query uses the curated `jupiter_solana.aggregator_swaps` table for swap signers, joins the matching seven-day fee-payer population for exact overlap, and looks back seven additional days for retention. A standard-library parser validates the reviewed CSV, and an atomic importer checks it against the already-published fee-payer and successful-signer series before regenerating JSON, Markdown, and HTML.

**Tech Stack:** DuneSQL/Trino SQL, Python standard library, `unittest`, static JSON/Markdown/HTML.

---

### Task 1: Lock the bounded Jupiter query

**Files:**
- Create: `queries/daily_jupiter_swap_signers.sql`
- Modify: `tests/test_dune_query.py`

**Step 1: Write the failing test**

Require the query to:

- read `jupiter_solana.aggregator_swaps`;
- use `tx_signer` and `block_time`;
- read fourteen complete UTC days for the retention lookback;
- publish only the latest seven complete UTC days;
- count daily distinct Jupiter Swap signers;
- count the exact intersection with successful transaction fee payers;
- count current-day signers also seen during the preceding seven days;
- use the Jupiter table's `block_month` partition.

**Step 2: Run the test to verify RED**

Run: `python -m unittest tests.test_dune_query -v`

Expected: FAIL because `queries/daily_jupiter_swap_signers.sql` does not exist.

**Step 3: Write the minimal query**

Use three explicit populations: `jupiter_signers`, `fee_payers`, and the latest
seven `output_days`. Join current-day Jupiter signers to prior Jupiter signers
with a date range of one through seven days, and join to fee payers by date and
address. Emit exactly:

```text
activity_date
unique_jupiter_swap_signers
jupiter_fee_payer_overlap
returning_jupiter_swap_signers
```

Do not call the result Jupiter Wallet users. It measures signers of swaps
recorded by Dune's curated Jupiter aggregator table.

**Step 4: Run the focused test to verify GREEN**

Run: `python -m unittest tests.test_dune_query -v`

Expected: all query tests pass.

**Step 5: Commit**

```powershell
git add tests/test_dune_query.py queries/daily_jupiter_swap_signers.sql
git commit -m "feat: add bounded Jupiter adoption query"
```

### Task 2: Normalize the Jupiter export with TDD

**Files:**
- Modify: `src/solana_observatory/dune_adoption.py`
- Modify: `tests/test_dune_adoption.py`

**Step 1: Write failing parser tests**

Add a wished-for `parse_daily_jupiter_swap_csv` function. A valid seven-row
fixture must return three schema `0.2.0` metrics:

- `daily_unique_jupiter_swap_signers`, in wallet addresses;
- `daily_jupiter_fee_payer_overlap`, in wallet addresses;
- `jupiter_swap_signer_7d_return_rate`, in percent.

Assert Dune provenance, the public query URL, exact dates, sorted series,
source time, and visible limitations. Add invalid cases for missing columns,
duplicate or incomplete dates, negative values, overlap above Jupiter users,
returning users above current-day users, and a naive or timezone-free
collection time.

**Step 2: Run the parser tests to verify RED**

Run: `python -m unittest tests.test_dune_adoption -v`

Expected: FAIL because the parser does not exist.

**Step 3: Implement the minimal parser**

Reuse the shared date/context validation. Parse all three integer columns in
one pass, enforce the within-row relationships, and derive return rate as
`returning / unique * 100`, rounded to two decimals. A zero-user day must also
have zero overlap and zero returning users and produces a measured 0% rate.

Definitions must say:

- Jupiter Swap signer means `tx_signer` on a curated Jupiter aggregator swap;
- overlap means the same address was also the successful fee payer that day;
- returning means the same address appeared on that day and at least once in
  the preceding seven complete UTC days.

**Step 4: Run focused tests to verify GREEN**

Run: `python -m unittest tests.test_dune_adoption -v`

Expected: all adapter tests pass.

**Step 5: Commit**

```powershell
git add tests/test_dune_adoption.py src/solana_observatory/dune_adoption.py
git commit -m "feat: normalize Jupiter overlap and retention"
```

### Task 3: Import all Jupiter metrics atomically

**Files:**
- Create: `scripts/import_dune_jupiter.py`
- Create: `tests/test_import_dune_jupiter.py`

**Step 1: Write failing command tests**

Prove a valid CSV updates JSON, Markdown, and HTML with all three metrics. Prove
any invalid relationship leaves existing output bytes untouched. Require the
snapshot to contain matching fee-payer and signer series, then reject any day
where:

- Jupiter users exceed all successful signers;
- fee-payer overlap exceeds all fee payers;
- source dates do not match.

**Step 2: Run the command tests to verify RED**

Run: `python -m unittest tests.test_import_dune_jupiter -v`

Expected: FAIL because the command does not exist.

**Step 3: Implement the command**

Follow the existing import commands: parse everything before writing, validate
all cross-series relationships, add all three metrics in memory, update
`generated_at`, then call `write_reports` once. Catch input, JSON, and validation
errors and return a nonzero status without touching previous reports.

**Step 4: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_import_dune_jupiter -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

**Step 5: Commit**

```powershell
git add tests/test_import_dune_jupiter.py scripts/import_dune_jupiter.py
git commit -m "feat: import Jupiter adoption metrics atomically"
```

### Task 4: Verify the live Dune result and publish the evidence

**Files:**
- Create: `data/dune/daily_jupiter_swap_signers_2026-08-08.csv`
- Modify: `output/report.json`
- Modify: `output/report.md`
- Modify: `output/index.html`
- Modify: `docs/METRIC-REGISTRY.md`
- Modify: `docs/LEARNING-LOG.md`
- Modify: `docs/COSTS.md`
- Modify: `docs/NEXT.md`
- Modify: `docs/ROADMAP-PR-MAP.md`
- Modify: `docs/plans/2026-08-08-jupiter-overlap-retention.md`

**Step 1: Create and run one public query**

Save the tested SQL as a new public Dune query. Confirm exactly seven complete
UTC output days and record execution ID, included credits, runtime, and the
public URL. Do not repeatedly rerun a valid result.

**Step 2: Export and import the reviewed CSV**

Record the export charge and use an explicit UTC collection time. Import
against the current report so cross-population checks run before publication.

**Step 3: Update methodology and cost receipts**

Document the exact definitions, dates, latest values, source table, query URL,
freshness, limitations, credits, and $0 extra-spend status. Cite Dune's current
schema documentation for `tx_signer`, `block_time`, and one-row-per-intended-
swap behavior.

**Step 4: Run the completion gate**

Run:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
git diff --check
```

Verify the static HTML shows five Adoption cards with correct source links,
wallet-not-people caveats, no invented zeros, and readable desktop/mobile
layout. If the controlled browser cannot access a local file, record that
constraint and rely on renderer tests plus Sathian's already-open local preview
for the manual visual gate.

**Step 5: Commit**

```powershell
git add data/dune output docs
git commit -m "feat: publish verified Jupiter adoption metrics"
```

## Execution receipt - 2026-08-08

- Public query: <https://dune.com/queries/8264526>
- Dune execution ID: `01KZGZVJ5516ERAWVG5KBXYWF4`
- Complete UTC output dates: 2026-08-01 through 2026-08-07
- Latest Jupiter Swap signers: 26,816 wallet addresses
- Latest exact successful fee-payer overlap: 26,816 wallet addresses
- Latest preceding-seven-day returning signers: 7,087 wallet addresses
- Latest address return rate: 26.43%
- Query runtime: 30.95 seconds; cost: 3.65 included credits
- Export: less than 0.01 included credits; extra spend: $0
- Visual gate: the controlled Chrome security policy blocked direct `file:`
  navigation, so automated visual inspection could not replace the renderer
  tests. Sathian's existing in-app local preview remains the manual desktop
  visual gate; the HTML includes the tested responsive/mobile rules.

All seven days showed a 100% exact address overlap between the curated Jupiter
`tx_signer` field and successful transaction fee payers. This is recorded as a
dataset-specific finding, not generalized to other applications. The reviewed
CSV was imported with collection time `2026-08-08T15:31:00Z`.
