# Final competitive polish design

## Goal

Make the release candidate easier for a judge to understand in under two
minutes while closing the remaining named validator and automation gaps. Keep
the deterministic, source-visible static-output architecture.

## Selected approach

1. **Dune:** retrieve the latest stored results with the GitHub secret, reject
   malformed or incomplete rows, expose the source date, and preserve prior
   verified evidence on failure. Query execution remains separately gated
   because it can consume credits.
2. **Validator depth:** add a top-ten leaderboard calculated directly from
   `getVoteAccounts`. Rank vote accounts by activated stake and show stake,
   network share, commission, and current/delinquent status. State explicitly
   that vote accounts are not independently verified operators.
3. **Visual trends:** add small inline SVG sparklines only when a metric already
   carries at least four ordered numeric observations. Pair each visual with
   first/latest values and a text description; use one cyan line and neutral
   guides, no extra chart library, gradients, animation, or health coloring.
4. **Anomaly demonstration:** add an overview monitor that separates notable,
   within-range, and unavailable checks. Show the configured threshold and
   supporting metric so the innovation is visible without opening source code.
5. **RWA:** do not scrape RWA.xyz or publish its data without API and
   redistribution permission. Retain the explicit unavailable state and link
   the source contract. A static press-release number is not a live metric.

## Alternatives rejected

- A chart library would add dependency, runtime, and accessibility cost for
  visuals that can be represented by simple series paths.
- A separate validator page would hide a sponsor-named metric from the main
  judging path.
- Scraping RWA.xyz or relabeling an article figure as live would weaken the
  product's central trust claim.

## Verification

Use red-green tests for Dune parsing, leaderboard calculation/contract,
Markdown/HTML rendering, sparklines, and anomaly monitor behavior. Then run the
full Python suite, compile checks, Axe at two widths, keyboard/reflow checks,
visual screenshots, workflow refresh, Pages deployment, and public JSON/HTML
reconciliation.
