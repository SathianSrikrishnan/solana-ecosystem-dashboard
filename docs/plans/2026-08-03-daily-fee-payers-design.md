# Daily Fee Payers Design

## Goal

Add the first verified adoption signal: the number of distinct fee-paying
addresses on successful non-vote Solana transactions for each of the latest
seven complete UTC days.

This is an address count, not a count of people. One person can control several
addresses, automation can control addresses, and a relayer or sponsor can pay
fees for someone else.

## Source and query

Use Dune's documented `solana.transactions` table. Its `signer` column is the
primary signer and fee payer, `success` identifies completed transactions, and
the table excludes validator vote transactions.

The bounded SQL groups by `block_date`, filters to `success = true`, excludes
the current incomplete UTC day, and returns seven daily rows. Filtering on the
date column keeps the scan bounded.

Official schema:
<https://docs.dune.com/data-catalog/solana/transactions>

## Architecture

Keep Dune optional. PR 2 begins with a committed SQL query and a Python
standard-library CSV importer. The operator runs or exports the query manually
on the free Dune path, then supplies the CSV and public query URL to the
importer. No API key is required for the core path.

The importer validates the complete input before changing a snapshot. It
requires the columns `activity_date` and `unique_fee_payers`, rejects invalid or
duplicate dates and non-integer or negative counts, sorts the series, and emits
one schema `0.2.0` adoption metric. The latest complete day becomes the current
value and all rows remain available as provenance-rich history.

## Failure behavior

Malformed, empty, or missing input fails visibly and leaves the existing
reports unchanged. The importer never converts missing input into zero. A
future authenticated Dune API adapter may automate collection, but it must be
optional and must expose cost, freshness, and failure state.

## Testing and visible result

Tests cover valid unordered input, empty data, missing columns, duplicate days,
invalid dates, and invalid counts. A command-level test proves invalid input
does not overwrite the existing report. After a real Dune result is imported,
the metric appears in the Adoption section supplied by PR 1.
