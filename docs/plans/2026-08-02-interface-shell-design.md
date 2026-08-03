# Interface Shell Design

## Product position

The dashboard is a beginner-readable Solana observatory for a curious builder
becoming an informed ecosystem participant. Its first screen answers three
questions: whether the network is functioning properly, whether application
and wallet activity is growing or returning, and whether meaningful economic
activity is increasing. It defaults to the latest seven complete days compared
with the preceding seven, with 30-day and 90-day context available later.

The interface does not publish one opaque health score. It shows transparent
component signals and explains how each measurement is defined. The current
PR uses verified network and validator data; unavailable adoption and economy
slices remain visibly unavailable rather than receiving sample values.

## Reader experience

The opening view combines verified facts with an automatic AI briefing. The
briefing covers what changed, why it may matter, and what deserves
investigation. Interpretation is visually distinct from measurements and must
identify supporting metric IDs, uncertainty, gaps, generation time, and model
information. Until the later AI slice exists, the shell displays a truthful
unavailable state instead of generated placeholder prose.

Readers can continue into Network, Adoption, Economy, Validators, Ecosystem,
and Methods sections. Every available metric retains its definition, source,
freshness, confidence, and caveat. Mobile presents the same information as a
vertical briefing.

## Architecture and data flow

Collectors normalize observations into schema `0.2.0`. Contract validation
runs before report generation. Later deterministic comparison and anomaly code
will add seven-day changes without AI involvement. Only validated facts and
deterministic findings may enter the AI adapter.

AI runs once during scheduled report generation, never in a visitor's browser.
Its structured response is embedded in JSON, Markdown, and HTML. This keeps API
keys private, bounds cost, and gives every reader the same reproducible report.
Collector or AI failure degrades visibly and does not prevent the deterministic
outputs from publishing.

## Testing boundary

Renderer tests cover navigation, the three-question overview, evidence fields,
automatic-briefing availability states, mobile behavior, accessibility, and
unavailable measurements. Browser checks cover desktop and mobile overflow,
section counts, and console errors. AI grounding and unsupported-claim checks
belong to PR 6, after deterministic comparison and anomaly inputs exist.
