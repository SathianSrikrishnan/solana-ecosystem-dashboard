# Solana Ecosystem Dashboard

Working repository for a trustworthy, automatically updating view of Solana's
network health, adoption, economics, validators, ecosystem changes, and news.

Public repository:
<https://github.com/SathianSrikrishnan/solana-ecosystem-dashboard>

The project is being built for the Superteam Canada **Develop Solana Ecosystem
Auto-Updating Report & Interactive Dashboard** bounty.

## Product promise

Help a curious Solana builder answer three questions:

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
```

Project status and the next decision are tracked in [docs/NEXT.md](docs/NEXT.md).
