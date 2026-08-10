# Release-candidate product audit

Audited: 2026-08-10

## Scope

The primary flow is a new visitor opening the observatory, understanding the
six questions, inspecting Economy, Financial Rails, Ecosystem, and Learn, and
opening evidence when a claim needs verification.

Accessibility target: WCAG 2.1 A/AA automated coverage plus keyboard-visible
focus, responsive reflow, zoom-safe markup, and explicit evidence limits.

## Accepted evidence

1. `01-overview-desktop.png` - desktop entry and current reading.
2. `02-economy-desktop.png` - economy cards and seven-day comparisons.
3. `03-financial-rails-desktop.png` - live stablecoin value plus explicit gaps.
4. `04-learn-desktop.png` - beginner guide and progressive disclosure.
5. `05-overview-mobile.png` - mobile entry and source-health stack.
6. `06-economy-mobile.png` - mobile single-column metric flow.
7. `07-ecosystem-desktop.png` - application breadth, releases, and developer gaps.

The rejected `01-desktop-full.png` is not evidence; the browser incorrectly
stitched the sticky header during a full-page capture.

## Confirmed strengths

- The opening promise and six questions establish a distinctive editorial
  instrument rather than a generic analytics grid.
- Facts, deterministic interpretation, and source limitations are visually
  separated.
- Data-unavailable states explain the missing evidence instead of inventing
  zeroes.
- Large values now use compact scan formatting while exact values remain in
  each evidence drawer and the JSON output.
- Desktop navigation no longer scrolls itself when an anchor is selected.
- Mobile reflows to one column without horizontal page overflow.
- Axe reports no WCAG 2.1 A/AA violations at 1280x720 and 390x844.

## UX risks

- Thirty-eight metrics still create a long page. The six-signal overview must
  remain the default judging surface; the detail sections are supporting proof.
- Four documented gaps can be misread as broken sources. The release copy now
  labels them as gaps and prefers a live section signal where one exists.
- “Compounding” cannot be reduced to protocol count or release cadence. The
  developer-count and retention gaps remain visible.
- The product has a deterministic evidence briefing, not yet an optional
  model-generated narrative. That is a differentiation decision, not a hidden
  implementation detail.

## Accessibility evidence limits

Axe cannot prove good screen-reader phrasing, complete keyboard usability,
comprehension, or contrast under every display condition. Before submission,
manually tab through all navigation links and evidence drawers at 200% zoom and
check VoiceOver or Narrator reading order once on the deployed URL.

## Release recommendations

1. Keep the current editorial/industrial visual system; do not redesign it.
2. Deploy the static artifact and show the six-question overview first.
3. Record a 60-90 second demo: overview, one changed signal, evidence drawer,
   one honest gap, automatic refresh architecture.
4. Verify the official bounty listing line by line before submitting.
5. Add a real model-backed briefing only if its provider, budget, and fallback
   are approved; the deterministic briefing remains the safe baseline.
