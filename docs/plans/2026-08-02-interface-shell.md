# Interface Shell Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Finish PR 1 as a responsive, trustworthy dashboard shell that presents current normalized data, the three opening product questions, and a truthful automatic-AI briefing state.

**Architecture:** Keep the Python standard-library renderer as the single source for standalone HTML. Render verified metrics directly from schema `0.2.0`, reserve a structured interpretation region, and show explicit unavailable states until later data and AI adapters land.

**Tech Stack:** Python 3 standard library, `unittest`, static HTML/CSS, Playwright browser verification.

---

### Task 1: Lock the three-question overview contract

**Files:**
- Modify: `tests/test_renderers.py`
- Modify: `src/solana_observatory/renderers.py`

**Step 1: Write the failing test**

Add a renderer test that expects the opening overview to contain these exact
questions:

```python
def test_html_opens_with_three_product_questions(self):
    rendered = render_html(self.snapshot)
    self.assertIn("Is the network functioning properly?", rendered)
    self.assertIn("Is application and wallet activity growing or returning?", rendered)
    self.assertIn("Is meaningful economic activity increasing?", rendered)
```

**Step 2: Run the test to verify it fails**

Run:

```powershell
python -m unittest tests.test_renderers.RendererTests.test_html_opens_with_three_product_questions -v
```

Expected: `FAIL` because the current overview displays metric labels but not
the agreed product questions.

**Step 3: Implement the minimal overview markup**

Add one labeled overview item per question. Populate the network item from
verified data. Mark adoption and economy as awaiting their verified adapters
when no metric exists in those sections. Do not invent values.

**Step 4: Run the renderer tests**

Run:

```powershell
python -m unittest tests.test_renderers -v
```

Expected: all renderer tests pass.

**Step 5: Commit**

```powershell
git add tests/test_renderers.py src/solana_observatory/renderers.py
git commit -m "feat: align overview with product questions"
```

### Task 2: Define the automatic briefing interface state

**Files:**
- Modify: `tests/test_renderers.py`
- Modify: `src/solana_observatory/renderers.py`

**Step 1: Write failing availability tests**

Add one test for a missing `analysis` object and one for a structured object:

```python
def test_html_shows_automatic_briefing_unavailable_without_analysis(self):
    rendered = render_html(self.snapshot)
    self.assertIn("Automatic AI briefing", rendered)
    self.assertIn("Analysis unavailable for this snapshot", rendered)

def test_html_renders_grounded_analysis_metadata(self):
    self.snapshot["analysis"] = {
        "status": "ok",
        "current_reading": "Network operation is stable.",
        "supporting_metric_ids": ["rpc_health"],
        "uncertainty": "Adoption data is not available yet.",
        "generated_at": "2026-08-02T12:00:00Z",
        "model": "example-model",
    }
    rendered = render_html(self.snapshot)
    self.assertIn("Network operation is stable.", rendered)
    self.assertIn("rpc_health", rendered)
    self.assertIn("Adoption data is not available yet.", rendered)
```

**Step 2: Run tests and confirm the intended failures**

Run:

```powershell
python -m unittest tests.test_renderers.RendererTests.test_html_shows_automatic_briefing_unavailable_without_analysis tests.test_renderers.RendererTests.test_html_renders_grounded_analysis_metadata -v
```

Expected: both tests fail because the shell has no structured analysis region.

**Step 3: Implement presentation only**

Add a renderer helper that displays the structured analysis when present and a
visible unavailable state otherwise. Do not call an AI API in PR 1.

**Step 4: Run all tests**

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests pass.

**Step 5: Commit**

```powershell
git add tests/test_renderers.py src/solana_observatory/renderers.py
git commit -m "feat: add automatic briefing interface contract"
```

### Task 3: Regenerate and inspect the standalone outputs

**Files:**
- Modify: `output/index.html`
- Modify: `output/report.md`

**Step 1: Generate from the verified saved snapshot**

Run the existing report pipeline against `output/report.json` so the tracked
HTML and Markdown match the renderer without requiring a live RPC call.

**Step 2: Verify generated-output hygiene**

Run:

```powershell
git diff --check
```

Expected: exit code `0` with no trailing-whitespace errors.

**Step 3: Run browser verification**

Open `output/index.html` in headless Chromium at desktop and mobile widths.
Assert all sections exist, no horizontal overflow occurs, and no console errors
are emitted.

**Step 4: Commit**

```powershell
git add output/index.html output/report.md
git commit -m "build: refresh interface artifacts"
```

### Task 4: Close the PR 1 documentation and verification receipt

**Files:**
- Modify: `docs/PROJECT-BRIEF.md`
- Modify: `docs/DECISIONS.md`
- Modify: `docs/LEARNING-LOG.md`
- Modify: `docs/NEXT.md`
- Modify: `docs/ROADMAP-PR-MAP.md`
- Modify: `docs/INTERFACE-ARCHITECTURE.md`

**Step 1: Reconcile durable state**

Confirm the docs consistently state: curious-builder audience, three balanced
opening questions, seven-day default, automatic grounded explanation, no
single health score, and AI-generation logic deferred to PR 6.

**Step 2: Run the complete gate**

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
git diff --check
```

Expected: tests pass, compilation exits `0`, and diff hygiene exits `0`.

**Step 3: Review the branch diff**

```powershell
git status --short --branch
git diff --stat main...HEAD
```

Expected: only PR 1 interface, tests, outputs, plans, and durable context are
present.

**Step 4: Commit**

```powershell
git add docs
git commit -m "docs: close interface shell slice"
```

### Task 5: Prepare the learning handoff

**Files:**
- Modify: `docs/NEXT.md`

**Step 1: Record the next product/data dependency**

Point the next technical slice to PR 2 adoption data. Keep the local-validator
learning lab as a separate no-purchase exercise after PR 1 review.

**Step 2: Present the four-part PR receipt**

Report one concept learned, one visible improvement, one evidence receipt, and
one next decision. Do not deploy or submit the bounty.
