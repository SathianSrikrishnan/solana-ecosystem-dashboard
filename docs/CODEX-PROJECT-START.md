# Codex Project Start

## Open this folder

`C:\Users\sathi\Projects\solana-ecosystem-dashboard`

## First task prompt

Use this repository as the dedicated Solana Ecosystem Dashboard project.

Read `AGENTS.md`, `README.md`, and every file directly linked from the README
before changing anything. Treat `docs/BIG-PICTURE-MAP.md` as the product compass,
`docs/ROADMAP-PR-MAP.md` as the execution sequence, `docs/DECISIONS.md` as locked
human judgment, and `docs/NEXT.md` as the current checkpoint.

Keep Sathian's explanations short and in plain English. Teach one concept and
request one decision at a time. Implement through small tested vertical slices.
Record decisions, learning, evidence, and the next action after every slice.

For the first turn:

1. inspect branch, status, tests, recent commits, and the current generated
   outputs;
2. make no changes;
3. explain what already exists, what the finished product becomes, and the next
   three steps;
4. identify the one shared data/interface contract that must be locked before
   the interface and Dune worktrees run in parallel.

Do not deploy, spend, change DNS or permissions, post externally, or submit the
bounty without Sathian's explicit action-time approval.

## Task structure

### Primary project task

Owns:

- product map and architecture;
- shared data contracts;
- decisions and sequencing;
- review and merge order;
- release readiness.

### Worktree task: interface shell

Owns:

- responsive application shell;
- overview and section navigation;
- visible source/freshness/methodology treatment;
- connection to normalized sample data.

### Worktree task: Dune adoption

Owns:

- fee payer and successful signer definitions;
- Jupiter application-user query;
- overlap and retention;
- fixtures, normalization, tests, and methodology.

Create later worktrees for economy, validator depth, and ecosystem watch only
after the shared contract and first two PRs are stable.

