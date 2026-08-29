# Bounty Finalization Design

Date: 2026-08-29
Status: approved for local implementation; production publication remains a review gate

## Outcome

Return Solana Observatory to a healthy, source-visible refresh path, preserve
its six-question beginner interface, and prepare a concise walkthrough and
submission package. The dashboard remains a standalone submission. It links to
`Inside MonkeDAO` as a complementary community field report rather than
presenting the two projects as one deliverable.

## Failure repair

### Official upgrade status

The official Alpenglow page now says `In Development`, while the collector
expects `Under Development`. Accept only those two bounded official phrases,
still require `Q3 2026`, and normalize the published value to
`In development · Q3 2026`. Unsupported wording continues to fail visibly.

### Dune capacity failure

Dune query execution currently returns a provider capacity/billing-limit
error. Do not buy capacity or change account settings. Treat execution as an
optional source failure:

1. attempt the three bounded queries only when due;
2. continue the workflow if execution is unavailable;
3. skip the stored-result refresh after a failed execution;
4. mark the last verified Dune metrics stale with a generic public note;
5. regenerate and commit HTML, Markdown, and JSON so the dashboard remains
   honest and the core report keeps publishing.

Provider billing details and secrets must never appear in public output.

## Public UX

Keep the current hero, six-question map, evidence drawers, history, Learn, and
Methods sections. Add a compact two-layer learning bridge in Learn:

- **System layer:** Solana Observatory explains the network through evidence.
- **Community layer:** Inside MonkeDAO shows one community through a firsthand
  interview and field report.

Add direct public links to the repository and the generated Markdown/JSON
artifacts in Methods. These are proof surfaces, not decorative navigation.

## Submission and walkthrough

Create:

- `docs/DEMO-SCRIPT.md` — a 10–12 minute recorded walkthrough with a bounded
  30-minute recording session;
- `docs/SUBMISSION-CHECKLIST.md` — final URLs, criteria proof, privacy checks,
  CI state, and explicit action-time approval gates;
- a tightened `docs/SUBMISSION-DRAFT.md` that positions the Observatory as the
  system view and Inside MonkeDAO as optional corroborating fieldwork.

The recording route must show the user experience first, one evidence drawer,
the generated artifacts, source code, and the automation/degradation story.

## Verification

- New tests fail before implementation for the current Alpenglow wording,
  Dune fallback workflow, public bridge, proof links, and submission documents.
- Full Python tests, deterministic report generation, and accessibility checks
  pass.
- Desktop and mobile browser QA confirm no clipping, broken anchors, or hidden
  provenance.
- No production push, merge, or bounty submission occurs without the final
  action-time review.

