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

