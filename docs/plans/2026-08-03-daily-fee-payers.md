# Daily Fee Payers Implementation Plan

**Goal:** Deliver the first PR 2 adoption slice as a bounded Dune query and a
safe, no-key import path into the normalized dashboard.

**Architecture:** Merge the completed PR 1 interface baseline, add a Dune SQL
artifact, parse exported CSV with the Python standard library, and publish only
after the full normalized snapshot validates.

### Task 1: Adopt the completed interface baseline

1. Merge `codex/interface-shell` into `codex/dune-adoption`.
2. Run all tests and confirm the worktree is clean apart from this plan.

### Task 2: Lock the Dune query definition

1. Add a test that checks the query uses `solana.transactions`, `signer`,
   `success = true`, a seven-day lower bound, and excludes the current day.
2. Run the test and confirm it fails because the query file is absent.
3. Add `queries/daily_unique_fee_payers.sql` with the minimal bounded query.
4. Run the focused and full test suites.

### Task 3: Build the normalized CSV adapter with TDD

1. Add failing tests for a valid export and each invalid-input class.
2. Implement `parse_daily_fee_payers_csv` in
   `src/solana_observatory/dune_adoption.py`.
3. Confirm focused tests and the complete suite pass.

### Task 4: Add a safe import command

1. Add command-level tests proving valid data updates all three outputs and
   invalid data leaves existing outputs untouched.
2. Implement `scripts/import_dune_fee_payers.py` with explicit input,
   snapshot, output, source URL, and collection time arguments.
3. Run the focused and complete suites.

### Task 5: Verify a real result and close the slice

1. Run the SQL manually in Dune without purchasing credits.
2. Export the seven-row result and import it with the public query URL.
3. Verify JSON, Markdown, desktop HTML, and mobile HTML.
4. Update the metric registry, learning log, costs, next steps, and PR receipt.
5. Run tests, compilation, diff hygiene, and browser verification before
   committing the completed slice.
