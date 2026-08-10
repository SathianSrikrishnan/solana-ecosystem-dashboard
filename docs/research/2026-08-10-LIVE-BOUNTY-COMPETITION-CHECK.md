# Live bounty competition check — 2026-08-10

## Current field and timing

- The official Superteam Earn listing currently reports **9 submissions** for
  **$1,000 USDG** total prizes: $500 first, $300 second, and $200 third.
- The deadline in the listing's first-party metadata is
  `2026-08-18T03:59:59.999Z`, which is **August 17, 2026 at 11:59:59 p.m.
  America/Toronto**. The sponsor schedules the winner announcement for
  September 1, 2026.
- This is a **Canada-only** listing and its metadata marks access as
  `HUMAN_ONLY`.
- Competitor identities and projects are **not publicly exposed at this time**:
  the official count endpoint returns 9, while the first-party submissions
  page/API returns an empty public submission list. We can measure the field's
  size, but cannot credibly compare individual entries.

Sources: [official bounty listing](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard),
[official submissions page](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard/submission),
[official submission-count endpoint](https://superteam.fun/api/listings/676a10c9-d5c7-49ce-9877-a91c647c0e8b/submission-count/).

## What judges explicitly score

1. **Comprehensiveness** — breadth and depth of Solana state coverage.
2. **Automation and maintainability** — current data with minimal intervention.
3. **Clarity and presentation** — understandable, actionable HTML, Markdown,
   and JSON.
4. **Innovation** — especially anomaly detection and multi-source correlation.
5. **Technical implementation** — code quality, documentation, and setup ease.
6. **Originality** — no plagiarism.

The listing gives priority to automated extraction from Dune, Solana ecosystem
sites, relevant X/Twitter accounts, Solana RPC, DeFiLlama, and CoinGecko. It
specifically names network performance, validator health, news, economic
indicators, daily active addresses, tokenized assets/equities, and upgrades such
as Alpenglow and SIMD-525. Anomaly detection is optional but "highly valued."

Source: [official bounty listing](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard).

## Submission requirements and constraints

The entry must provide:

- a public GitHub repository with code, setup instructions, and a README that
  explains how to run and interpret the report;
- samples of generated Markdown and JSON reports;
- a brief explanation of sources/integration, automation, anomaly detection,
  and local setup;
- preferably a live or hosted interactive dashboard, which receives higher
  consideration.

The official page does not publish character limits or additional visible form
field constraints before an authenticated submission. Submission itself is
human-only and regional eligibility must be satisfied.

Source: [official bounty listing](https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard).

## Ranked remaining competitive gaps for Solana Observatory

1. **Activate the built Dune refresh in production.** Adding the repository
   `DUNE_API_KEY` converts preserved snapshots into genuinely current automated
   adoption data. This is the clearest remaining mismatch with a source the
   sponsor explicitly prioritizes.
2. **Close one headline tokenized-asset/equities gap if a reproducible source is
   available.** The honest unavailable state is trustworthy, but a live RWA
   value or dated trend would materially strengthen both comprehensiveness and
   the project's financial-rails thesis. Do not backfill from marketing claims.
3. **Make the innovation leg unmistakable in the pitch.** Demonstrate one
   evidence drawer and one anomaly end-to-end, then explain the original trust
   layer: definition, provenance, freshness, limitation, independent source
   failure, and grounded briefing. This is more defensible than adding many
   shallow charts.
4. **Show automation rather than merely describe it.** In the demo, point to
   the six-hour workflow, most recent refresh time, visible source health, and
   generated HTML/Markdown/JSON from the same contract. This directly answers
   the maintainability criterion.
5. **Finish a judge-first submission package.** Lead with the hosted dashboard,
   a 60–90 second walkthrough, the public repository, and direct Markdown/JSON
   links. Keep the copy short enough that a judge can understand the product,
   originality, and verification evidence in under two minutes.
6. **Treat X/community monitoring as optional polish, not a deadline-critical
   dependency.** Official Solana RSS and upgrade tracking already cover current
   first-party developments. A bounded X adapter could improve source breadth,
   but it should not weaken the no-key core or consume time needed for the Dune
   activation, RWA evidence, and pitch.

## Competitive judgment

With only nine visible entries, the Observatory already has a credible winning
shape: hosted multi-format output, broad metric coverage, deterministic anomaly
checks, source-visible explanations, graceful degradation, and a scheduled
refresh. The greatest risk is no longer insufficient scope; it is leaving a
sponsor-prioritized Dune adapter inactive or failing to communicate the
technical trust model quickly. The strongest final push is therefore **proof of
automation + one distinctive evidence/anomaly story + concise presentation**,
not another large feature batch.

