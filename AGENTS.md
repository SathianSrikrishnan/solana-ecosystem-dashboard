# Solana Ecosystem Dashboard Agent Rules

## Product purpose

Build a trustworthy, beginner-readable Solana ecosystem observatory for the
Superteam Canada bounty due 2026-08-17 at 23:59 America/Toronto.

## Working style

- Explain one concept and request one human decision at a time.
- Keep user-facing explanations short and plain English.
- Preserve durable context in `docs/PROJECT-BRIEF.md`, `docs/DECISIONS.md`,
  `docs/LEARNING-LOG.md`, and `docs/NEXT.md`.
- Never present one activity metric as "the truth." Show its definition,
  source, freshness, limitations, and relevant alternatives.
- The deterministic data pipeline is the source of truth. AI may explain
  verified data but must not invent, silently modify, or backfill metrics.
- Prefer a useful no-key core. Paid or authenticated sources must be optional
  adapters with explicit cost and failure behavior.
- Use test-driven development for behavior changes.
- Do not deploy, purchase API credits, change DNS, publish social content, or
  submit the bounty without Sathian's explicit action-time approval.

## Architecture guardrails

- Python standard library for core collection and report generation.
- Static HTML, Markdown, and JSON are required outputs.
- Every metric carries provenance and collection time.
- A failed source degrades visibly; it must not break the full report.
- Secrets belong in `.env`, never Git, chat, reports, or screenshots.

