# Solana Observatory Walkthrough

Status: ready for Sathian to record after the release branch is approved and published.

## 30-minute recording session

- **0–5 minutes — setup:** close notifications and private tabs, set the browser
  to 100% zoom, use 1920×1080, connect the microphone, and open only the live
  dashboard, public repository, and generated Markdown report.
- **5–8 minutes — rehearsal:** read the opening and closing once. Do not rehearse
  every click.
- **8–23 minutes — record:** aim for one 10–12 minute take. Pause for two seconds
  after each section so the recording can be tightened later.
- **23–30 minutes — check:** confirm the first sentence, evidence drawer, source
  links, and closing are audible. Keep the best complete take.

## 10–12 minute walkthrough

### 0:00–0:45 — the problem

> Most ecosystem dashboards give you more numbers. I built Solana Observatory
> to answer six questions: is the network working, are people and applications
> returning, is useful economic activity growing, is the validator set
> resilient, is the ecosystem compounding, and is Solana becoming financial
> infrastructure?

Show the hero, snapshot time, source health, and thirty-second reading path.

### 0:45–2:00 — how to read it

Move through the six-question map. Explain that `Reporting` describes a source,
not a positive verdict; `Stale` preserves the last verified value; and
`Unavailable` keeps a gap visible.

### 2:00–4:30 — one evidence path

Open Network, then one evidence drawer. Point to the exact value, definition,
source, collection time, confidence, and limitation. Say plainly that non-vote
transactions can still include bots.

### 4:30–6:30 — adoption and economics

Show the Dune adoption cards and their freshness label. Then compare application
fees, application revenue, chain fees, and REV. Explain why these are separate
measurements and why wallets are not presented as people.

### 6:30–8:00 — validators and financial rails

Show the validator table and concentration measures. Then show stablecoins and
financial rails, emphasizing that raw transfers are not automatically payments.

### 8:00–9:15 — automation and honest degradation

Open the GitHub Actions workflows in the public repository. Explain the
six-hour refresh, deterministic tests, three generated formats, anomaly checks,
and the rule that an optional source failure is labeled instead of blanking the
dashboard.

### 9:15–10:15 — reproducibility

Open `report.md`, then `report.json`. Explain that the interactive HTML,
human-readable Markdown, and machine-readable JSON all come from one validated
snapshot.

### 10:15–11:15 — the broader learning system

Return to Learn. Solana Observatory is the system view. `Inside MonkeDAO` is the
community view: a separate firsthand field report that shows what one Solana
community looks like from inside. They reinforce each other but remain separate
submissions.

### 11:15–12:00 — close

> The point is not to replace judgment with a dashboard. It is to make the
> evidence, freshness, and limitations inspectable enough that a newcomer can
> form a better judgment. The dashboard is live, the code and reports are
> public, and the refresh path is designed to fail honestly.

Stop the recording. Do not improvise a bounty claim or disclose private tabs,
wallet addresses, secrets, or unpublished interview material.
