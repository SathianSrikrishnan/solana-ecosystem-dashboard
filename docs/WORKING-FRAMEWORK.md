# Working Framework

Each project slice follows the same small loop.

## 1. Learn

Codex explains one concept in plain English.

## 2. Define

We write the exact meaning, source, limitations, and possible alternatives.

## 3. Decide

Sathian answers one short product or judgment question.

## 4. Build

Codex implements one bounded, test-first slice.

## 5. Verify

We check the real output, source freshness, failure behavior, and whether the
result actually answers the question.

## 6. Record

Codex updates the decision log, learning log, metric registry, and next action.

## Human/agent split

Sathian owns:

- the question;
- what matters;
- metric meaning;
- plausibility and product taste.

Codex owns:

- source research;
- SQL and implementation drafts;
- tests and automation;
- documentation and receipts.

## Check-in format

Every normal check-in should return:

1. what changed;
2. what Sathian should understand;
3. one decision or next action.

