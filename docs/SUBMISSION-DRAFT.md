# Superteam submission draft

Status: release candidate; public links are verified and final byline/demo remain.

- Live dashboard: https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/
- Public repository: https://github.com/SathianSrikrishnan/solana-ecosystem-dashboard
- Official bounty: https://superteam.fun/earn/listing/develop-solana-ecosystem-auto-updating-report-and-interactive-dashboard

## One-line pitch

Solana Observatory is a living, source-visible dashboard that explains whether
Solana is working, attracting durable use, producing economic value, remaining
decentralized, compounding its ecosystem, and becoming financial infrastructure.

## Short description

Most ecosystem dashboards show many numbers but leave newcomers to decide what
they mean. Solana Observatory combines direct RPC data, Dune adoption cohorts,
DeFiLlama economic measurements, validator stake analysis, application breadth,
and release signals in one automatically refreshed report. Every metric exposes
its definition, source, freshness, confidence, and limitation. Wallets are not
called people; transfers are not called payments; missing evidence stays visible.

## What is original

- Six product questions instead of one opaque health score.
- Separate measurements for fee payers, successful signers, Jupiter users,
  returning addresses, app fees, app revenue, chain fees, and REV.
- Deterministic anomaly detection and evidence-bound plain-English briefing.
- Exact values and provenance in JSON, Markdown, and interactive HTML generated
  from one validated contract.
- Honest degradation: one failed source cannot blank or silently corrupt the report.

## Reproducibility

```powershell
# Source / context:
# Solana Observatory clean local verification

cd "C:\path\to\solana-ecosystem-dashboard"

# Commands:
python -m unittest discover -s tests -v
python scripts\generate.py
python scripts\refresh_economy.py --snapshot output\report.json --output output
python scripts\refresh_ecosystem.py --snapshot output\report.json --output output
npm ci
npx playwright install chromium
npm run test:a11y
```

## Demo script (75 seconds)

1. **0-10s:** “Most dashboards show activity. This one shows what the activity
   means—and what it cannot prove.”
2. **10-25s:** Show the six questions and automatic evidence briefing.
3. **25-40s:** Open Economy; compare app fees, app revenue, chain fees, and REV.
4. **40-52s:** Open one evidence drawer: definition, source, freshness, caveat.
5. **52-62s:** Show Financial Rails and explain why transfers are not payments.
6. **62-75s:** Show JSON/Markdown outputs and the six-hour refresh workflow.

## Final fields still needed

- Sathian's public byline and 1-2 sentence builder bio.
- Final screenshots/demo URL.
