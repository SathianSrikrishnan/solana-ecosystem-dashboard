# Beginner and Shareable Final Release Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Make the observatory understandable in thirty seconds, useful on repeat visits, and visually compelling when shared without removing its evidence depth.

**Architecture:** Keep one static dashboard and one validated snapshot. Add a beginner orientation layer and six-question visual map above the detailed sections, then produce reproducible social images from a source HTML template. The data collectors, metric contract, and no-cost core remain unchanged.

**Tech Stack:** Python 3.11 standard library, static HTML/CSS/JSON/Markdown, Node Playwright for release-only social image rendering, official Solana SVG assets, built-in image generation for background artwork.

---

## Product decision

Three approaches were considered:

1. **Delete most metrics.** Simplest page, but weaker bounty coverage and less useful for serious readers.
2. **Add a beginner layer above the evidence.** Recommended. It protects breadth while making the first scan easy.
3. **Build beginner/expert mode toggles.** Powerful, but adds state, JavaScript, testing surface, and a second information architecture days before submission.

The release uses approach two. The memorable idea is: **six questions, one living system, every claim inspectable.**

## Visual direction

Colors: near-black `#070a0e`, Solana green `#14F195`, muted cyan, restrained Solana violet `#9945FF`, off-white text.

Fonts: Bahnschrift condensed display; Segoe UI Variable body; Cascadia Mono evidence labels.

Spacing: existing 4/8px-derived observatory scale with generous section gaps.

Mood: editorial scientific instrument; credible, optimistic, measured.

Reference: an engineering field instrument crossed with a financial newspaper graphic. Avoid generic crypto coins, rockets, neon cities, glass cards, and invented health scores.

## Task 1: Beginner orientation layer

**Files:**
- Modify: `tests/test_renderers.py`
- Modify: `src/solana_observatory/renderers.py`

1. Write failing renderer tests requiring a `Start here` orientation panel, three numbered reading steps, and a plain-English data-state legend.
2. Run the focused tests and confirm they fail because the new copy and markup are absent.
3. Add semantic HTML and responsive CSS without JavaScript or hidden detail.
4. Run the focused tests and full Python suite.

## Task 2: Six-question system map

**Files:**
- Modify: `tests/test_renderers.py`
- Modify: `src/solana_observatory/renderers.py`

1. Write a failing test requiring one linked map with all six sections and their beginner questions.
2. Confirm the expected failure.
3. Render six compact links as one connected system, not six new statistic cards.
4. Verify keyboard focus, mobile reflow, and reduced-motion behavior.

## Task 3: Share and cover package

**Files:**
- Create: `assets/brand/observatory-rails-background.png`
- Create: `assets/brand/solana-logomark.svg`
- Create: `assets/brand/social-cover.html`
- Create: `assets/brand/six-question-map.html`
- Create: `scripts/render_social_assets.mjs`
- Modify: `package.json`
- Modify: `tests/test_renderers.py`
- Modify: `src/solana_observatory/renderers.py`
- Create: `output/solana-observatory-cover.png`
- Create: `output/solana-six-question-map.png`

1. Add failing tests for Open Graph and Twitter preview metadata.
2. Add the official Solana logomark without altering its shape, outline, or proportions.
3. Compose exact cover typography over generated editorial artwork in HTML.
4. Render 1200x630 and 1200x1200 PNGs with Playwright.
5. Add absolute public social-preview metadata to the dashboard head.
6. Inspect both images visually.

## Task 4: Honest stale-data language

**Files:**
- Modify: `tests/test_dune_adoption.py`
- Modify: `src/solana_observatory/dune_adoption.py`
- Regenerate: `output/index.html`, `output/report.md`, `output/report.json`

1. Write a failing test that repeated refresh failures replace the public refresh note rather than append internal HTTP errors.
2. Confirm the failure.
3. Publish one stable sentence: the saved Dune result is preserved but needs a fresh query execution.
4. Regenerate outputs and confirm no `HTTP Error 401` appears publicly.

## Task 5: Proof and launch package

**Files:**
- Modify: `README.md`
- Modify: `docs/RELEASE-CHECKLIST.md`
- Modify: `docs/SUBMISSION-DRAFT.md`
- Modify: `docs/content/DEMO-RECORDING-SCRIPT.md`

1. Create a compact bounty proof table mapping criteria to public evidence.
2. Explain Dune's role, free monthly credits, execution/export credit use, and zero-dollar spend cap.
3. Make the demo lead with the beginner layer, then one source drawer and the automation receipt.
4. Keep the future personal-site article and Tooth Fairy Network bridge factual and separate from the bounty proof.

## Task 6: Verification and release

1. Run all Python tests and compile checks.
2. Generate reports and social assets.
3. Run desktop/mobile Axe and visual QA.
4. Run `git diff --check` and scan public artifacts for secrets and internal error strings.
5. Commit, push the release branch and `main`, wait for refresh and Pages deployment, then rerun browser QA against the public URL.

