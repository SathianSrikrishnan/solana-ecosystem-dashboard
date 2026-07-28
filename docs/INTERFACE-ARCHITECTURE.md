# Interface Architecture

## Interface promise

The interface should work at two speeds:

1. a 30-second morning briefing;
2. a deeper evidence view for analysts and builders.

## Page structure

### Overview

- plain-English current reading;
- three headline signals;
- one dominant trend;
- what deserves attention;
- freshness and source-health status.

### Network

TPS, non-vote TPS, slot time, epochs, blocks, and direct RPC health.

### Adoption

Fee payers, successful signers, app users, returning wallets, and clearly
labeled human/bot estimates.

### Economy

SOL price, TVL, stablecoins, DEX volume, fees, REV, and tokenized assets.

### Validators

Active/delinquent counts, stake concentration, commissions, and history.

### Ecosystem

Selected announcements, upgrades, proposals, application movements, and
possible metric relationships.

### Methods

Definitions, sources, queries, freshness, confidence, caveats, and known gaps.

## Locked interface rules

- Facts and AI explanations are visually separate.
- Every chart retains its definition, source, and freshness.
- No wallet count is labeled people or users without qualification.
- Dark theme first, responsive down to mobile.
- Public readers need no account.
- The opening screen shows few signals; depth lives in sections.
- Source failure is visible and does not blank the entire product.

## Decisions needed before final polish

- Final name and visual identity.
- Whether to show a single health score or only component signals.
- Default comparison window: 7, 30, or 90 days.
- Whether AI explanations appear automatically or behind an Explain control.
- Which three signals earn the opening screen.

## When to build

Build the interface shell now using the normalized sample data. Connect each
verified data slice as it lands. Delay final typography, brand, animation, and
marketing polish until the core sections contain trustworthy real data.

