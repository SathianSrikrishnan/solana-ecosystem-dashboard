# Roadmap and Pull Request Map

## Operating model

We build vertical slices. Each slice contains:

- one defined question;
- one source adapter or query;
- one normalized data contract;
- tests and failure behavior;
- one visible dashboard section;
- a learning and methodology update.

## Release sequence

| PR | Worktree | Outcome | Dependency |
|---|---|---|---|
| 1 | `interface-shell` | Responsive dashboard shell using current normalized data | Existing foundation |
| 2 | `dune-adoption` | Fee payer, signer, Jupiter user, overlap, and retention data | Shared metric contract |
| 3 | `economy` | Price, TVL, stablecoin, DEX, fees, REV, tokenized assets | Shared metric contract |
| 4 | `validator-depth` | Stake, commission, delinquency history | Shared metric contract |
| 5 | `ecosystem-watch` | Bounded X/web source collection and upgrade tracking | $20 X cap |
| 6 | `anomaly-intelligence` | Deterministic anomalies and grounded AI explanation | PRs 2–5 |
| 7 | `release` | Final design, hosting, clean setup proof, demo, submission | All verified slices |

## Parallelization rule

PRs 1 and 2 can begin together after the interface/data contract is locked.
PRs 3, 4, and 5 can then run independently. Shared schema and renderer changes
stay small and are merged before dependent work begins.

Do not run parallel branches that all rewrite the same core files.

## Review rhythm

After each PR, Sathian receives:

1. one concept learned;
2. one visible improvement;
3. one evidence receipt;
4. one next decision.

## Repository status

The standalone repository already exists and is public:

<https://github.com/SathianSrikrishnan/solana-ecosystem-dashboard>

Canonical local folder:

`C:\Users\sathi\Projects\solana-ecosystem-dashboard`

## Completion receipts

- PR 1 (`interface-shell`) — completed locally 2026-08-03. The standalone HTML
  now has a responsive overview, all planned product sections, grouped
  normalized data, visible source health and unavailable states, evidence
  details, and a separate automatic-briefing boundary. It renders grounded
  analysis metadata when supplied and an honest unavailable state otherwise;
  AI generation is intentionally deferred to PR 6.
- PR 2 (`dune-adoption`) - first vertical slice completed locally 2026-08-03.
  Public Dune query <https://dune.com/queries/8213434> returns seven complete
  UTC days of distinct successful fee-payer addresses. A strict no-key CSV
  importer publishes the normalized metric to JSON, Markdown, and HTML; bad
  input leaves prior reports untouched. The newest value is visibly labeled
  as wallet addresses rather than people. Dune usage was 3.892 included
  credits and $0 extra spend.
- PR 2 (`dune-adoption`) - successful-signers rung completed locally
  2026-08-08. Public Dune query <https://dune.com/queries/8264418> returns the
  latest seven complete UTC days of distinct signer addresses on successful
  non-vote transactions. The latest value is 3,628,019 addresses on
  2026-08-07, versus 2,046,280 fee payers. Both measures explicitly say that
  wallets are not people. The two refreshed queries used 9.84 included credits
  plus less than 0.02 for exports, with $0 extra spend.
- PR 2 (`dune-adoption`) - application, overlap, and retention rung completed
  locally 2026-08-08. Public query <https://dune.com/queries/8264526> measures
  curated Jupiter Swap signers, their exact successful fee-payer intersection,
  and preceding-seven-day returns. On 2026-08-07 it found 26,816 signers,
  26,816 fee-payer overlaps, and 7,087 returning addresses (26.43%). The query
  used 3.65 included credits and less than 0.01 for export, with $0 extra spend.
  PR 2 now has all five planned adoption outputs and forty-six passing tests.
- PR 3 (`economy`) - no-key core completed locally 2026-08-08. CoinGecko
  supplies live SOL/USD; DeFiLlama supplies the latest complete UTC day's TVL,
  stablecoin circulating value, and DEX volume plus fourteen-day series. Each
  source fails independently and visibly. The first verified snapshot recorded
  $76.32 SOL, $4.707B TVL, $16.252B stablecoin value, and $1.363B DEX volume at
  $0 cost. Fees, REV, and tokenized assets remain behind a source-definition
  review rather than being published from ambiguous endpoints.
