# Solana Ecosystem Dashboard

Working repository for a trustworthy, automatically updating view of Solana's
network health, adoption, economics, validators, ecosystem changes, and news.

Public repository:
<https://github.com/SathianSrikrishnan/solana-ecosystem-dashboard>

The project is being built for the Superteam Canada **Develop Solana Ecosystem
Auto-Updating Report & Interactive Dashboard** bounty.

## Product promise

Help a curious Solana builder answer three layers of questions:

1. What is happening now?
2. What changed?
3. What deserves attention?

The project will show multiple definitions where a metric has multiple valid
interpretations. It will not pretend that wallets equal humans.

## Planned outputs

- `output/report.json` — machine-readable facts and provenance
- `output/report.md` — beginner-readable briefing
- `output/index.html` — standalone interactive dashboard

## Local development

The core pipeline uses Python's standard library.

```powershell
# Source / context:
# Solana Ecosystem Dashboard local development

cd "C:\Users\sathi\Projects\solana-ecosystem-dashboard"

# Commands:
python -m unittest discover -s tests -v
python scripts\generate.py
python scripts\refresh_economy.py --snapshot output\report.json --output output
python scripts\refresh_ecosystem.py --snapshot output\report.json --output output
npm ci
npm run test:a11y
```

The Python standard-library pipeline remains the production core. Node is used
only for repeatable Axe accessibility testing at desktop and mobile widths.

Start with the [big-picture map](docs/BIG-PICTURE-MAP.md), then check
[the interface architecture](docs/INTERFACE-ARCHITECTURE.md),
[the PR roadmap](docs/ROADMAP-PR-MAP.md), and [docs/NEXT.md](docs/NEXT.md) for
the current learning and build slice.

When opening this repository as a new Codex project, use
[docs/CODEX-PROJECT-START.md](docs/CODEX-PROJECT-START.md).
