# mine-flow — STEP-54.10a: Impeccable-Skill Runtime Capture & a11y Evidence Closure

> **How to run:** Tell your agent *"run substep 54.10a"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Hermes/Claude Opus 4.8 — top tier, and it cannot be a different executor.** This
substep drives the project-vendored Impeccable skill at `.agent/skills/impeccable/`, which only a
harness with local script + browser-automation access can run. It is **review-only**: it produces
evidence, never fixes.

## Context

STEP-54's critique substeps (54.1–54.10) are document critiques whose Evidence standard makes static
`file:line` citation the mandatory floor and records runtime claims as `Unverified` when the STEP-48
`flutter drive` harness cannot evidence them. The residual was never closed: RISK-0015/0016/0023
screenshot placeholders, and 45.14's "accessibility/screen-reader behavior remains unverified".

This substep is the **authorized second capture route**. A 2026-09-11 feasibility spike (this
prompt's provenance) proved the Impeccable skill's browser stack captures real rendered artifacts
from the Flutter web build — independently of the `flutter drive` harness — and that Flutter's
accessibility semantics tree is reachable at runtime. It also proved the skill's **detector is blind
on this codebase**, which is itself a finding to record.

**This substep feeds 54.11's master spec.** It runs *after* 54.10 and *before* the consolidation, so
its evidence lands in the spec STEP-55 executes 1:1. It does **not** re-critique the features.

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in
`mine-flow-STEP-54.1-FINDINGS.md`), 54.10 Done (system utilities critique).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — the rubric; your verdicts use its dimensions
- `Upcoming Prompts/mine-flow-STEP-54.10-FINDINGS.md` — system-utilities claims you will evidence
- `Code/mine-flow-docs/runbooks/impeccable-design-review.md` — the project's review-first boundary
- `Code/mine-flow-docs/adr/ADR-0008-impeccable-bridge.md` — **binding**: root `DESIGN.md` /
  `PRODUCT.md` are *generated* bridge files and must never be edited directly
- `Code/mine-flow-docs/adr/ADR-0017-dual-platform-e2e-gate.md` — platform split (Chrome + Pixel_6a)
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon (WCAG 2.1 AA, 150–200ms
  motion, compact density, sidebar Web + 5-item bottom bar Android)
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0015/0016/0023 (screenshot placeholders),
  RISK-0011 (privacy notice), RISK-0004 (l10n)
- `Code/mine-flow-app/README.md` — the `--dart-define` run recipe
- root `.throughstone/local-user.md`

## What the spike already proved (do not re-derive; reproduce and extend)

These are verified facts as of 2026-09-11 on Flutter 3.47.1 / Chrome 152. Treat them as the starting
recipe, not as findings to take on faith — re-confirm as you go and report your own artifact numbers.

1. **Launcher works.** `bash .agent/skills/impeccable/scripts/impeccable context` → exit 0, ~15.7 KB.
   The real binary is `.agent/skills/impeccable/scripts/bin/windows-x64/impeccable.exe`. Use the
   **project-vendored** skill at `.agent/skills/impeccable/`; the Hermes-installed skill has no
   launcher. On a shell without `sh`, call `.agent/skills/impeccable/scripts/impeccable.cmd`.
2. **The skill's canon is Doc 07 itself** — `DESIGN.md` / `PRODUCT.md` are generated from
   `architecture/07-ui-design-system.md`. There is no canon conflict with STEP-54.
3. **`.impeccable/live/roots.json` is misresolved.** It currently reports
   `"repoRoot": "<workspace root>"` with `"hasVisualImplementation": false` and
   `"resolvedFrom": "fallback"` — the skill sees no app. Repoint it at `Code/mine-flow-app` before a
   real run and record the correction (it is untracked local state, safe to edit).
4. **The app builds and serves.** `flutter run -d web-server --web-port=8080 --web-hostname=127.0.0.1`
   with credentials injected per the README (`$(grep ... .env | cut -d= -f2-)`; **never print
   secret values**). The web compile took **~101 s** — loading the page before the
   `lib\main.dart is being served at` line yields a blank bootstrap shell with no canvas. Wait for
   that line, then load.
5. **Rendering is CanvasKit, not DOM.** The app mounts `flutter-view` → `flt-glass-pane` (with a
   **shadow root**) → `flt-canvas-container` → `canvas`. There is no top-level `canvas`, no useful
   DOM text, and no CSS to inspect.
6. **A11y semantics are obtainable.** `document.querySelector('flt-semantics-placeholder')` renders
   with `aria-label="Enable accessibility"`; clicking it produced **16 `flt-semantics` nodes** and
   readable text (`mine-flow / Sistem Monitoring & Manajemen Tambang / Email / Kata Sandi /
   Show password / Masuk`). This is the route to the 45.14 a11y residual.
7. **Real capture artifacts.** A harness screenshot of the login surface produced a
   **19,553-byte, 1258×566 PNG** showing the properly styled dark-theme login — not the 68-byte /
   1×1 placeholder class. The skill's own bundled `modern-screenshot.umd.js`
   (`domToPng(document.querySelector('flutter-view'))`) also rendered a valid image
   (1258×566 data URL, ~21.5 KB). Two independent capture routes; prefer the harness-native path.
8. **The live-server works.** `bash .agent/skills/impeccable/scripts/impeccable live-server
   --background` prints `{pid, port, token}` (auto-port from 8400) and serves `/live.js`,
   `/detect.js` (~2.2 MB), `/modern-screenshot.js`, `/health`. Stop it with
   `impeccable live-server stop`.
9. **THE DETECTOR IS BLIND HERE — record this, do not paper over it.**
   - `impeccable detect --json <dart file or lib/>` → `[]` (3 bytes, exit 0) on Dart source.
   - Injecting `/detect.js` into the live app logged
     `[impeccable] No anti-patterns found.` — zero signal.
   - That "clean" result **contradicts** the CLI URL scan, which returned one
     `wide-tracking / letter-spacing: 6.25em` hit that is a **false positive** (`letter-spacing`
     does not exist anywhere in the app's `web/`).
   - Cause: every detector rule is DOM/CSS-based, and CanvasKit exposes neither.
   - **Therefore: a "no anti-patterns" result is NOT a clean bill of health, and must never be
     reported as design verification.** Record the no-signal behaviour as a finding with the
     evidence above.
10. **`/critique` and `/audit` are not CLI verbs.** `impeccable --help` exposes only `detect`,
    `ignores`, `install`, `link`, `update`, `check`, plus `critique-storage` and `live-server`.
    The slash-commands are *agent playbooks* under `reference/*.md` (e.g. `reference/critique.md`,
    `reference/audit.md`, `reference/audit.native.md`). Running "the skill's critique" means an
    agent follows those playbooks — which overlaps the project's own
    `runbooks/impeccable-design-review.md`. **Do not run a competing heuristic critique pass**;
    this substep's value is the *evidence*, not a second opinion. Use the playbooks only for their
    evidence-gathering mechanics, and cite Doc 07 + the 54.1 rubric as the authority.

## Scope

**In scope — capture and evidence only:**

1. **Shell & navigation** across both platforms: Web sidebar (collapsed/expanded) and Android
   5-item bottom bar (Doc 07 §4).
2. **Shared surfaces** the spec will lean on: the login screen, the dashboard/KPI landing surface,
   and one representative form sheet + one report dialog from the 54.2–54.10 set (pick the
   best-evidenced; don't re-shoot all nine features).
3. **Both themes** (light/dark) and **both platforms** where reachable.
4. **The a11y semantics tree and focus order** for the captured surfaces: enable semantics, walk
   `flt-semantics`, record the focus sequence, and check the Doc 07 WCAG 2.1 AA target against what
   the tree actually exposes (roles, names, states) — including the login form's labels and the
   password-visibility control.
5. **Motion**: Doc 07 specifies 150–200 ms subtle motion, and the app must honour reduced-motion
   preferences. Evidencing this is optional and hard; if you cannot, record `Unverified` with the
   blocker (do not infer from source).

**Does NOT touch:**

- Application code (`Code/mine-flow-app/lib/**` is read-only) — this is review-only.
- Any file the skill would *write*: `DESIGN.md`, `PRODUCT.md`, `DESIGN.md` sidecar, surface briefs,
  config, or harness manifests.
- The 54.1 rubric, other substeps' findings, ADRs, archived STEP-53 history.

## Hard boundaries (violating these is a failed run)

- **Whitelisted verbs only:** `context`, `detect`, `critique-storage`, `live-server` (with `stop`).
  **Never run** `init`, `document`, `extract`, `install`, `link`, or `update` — they mutate the repo
  or the harness (`init`/`document`/`extract` rewrite the ADR-0008-protected bridge files;
  `install`/`link` write harness manifests), and regenerating the bridge is a separately authorized
  task via `scripts/impeccable-bridge.ps1`.
- **Never run a mutating design command** (`polish`, `bolder`, `quieter`, `distill`, `animate`,
  `colorize`, `typeset`, `layout`, `delight`, `overdrive`, `clarify`, `adapt`, `optimize`,
  `harden`, `onboard`, `live`). **STEP-55 is the implementation STEP** — a fix attempted here
  duplicates and pre-empts it.
- **Do not install the design hook** into `.claude/settings.local.json` / `.codex/hooks.json` /
  `.cursor/hooks.json` / `.github/hooks/impeccable.json`.
- **Secrets stay out.** Read `.env` only via `$(grep ... | cut -d= -f2-)` substitution into
  `--dart-define`; never print, echo, quote, or log a value. If a run prints one, stop and report.
- **Unverified is a valid, expected outcome.** A harness that cannot be made to work is recorded as
  a blocker, never as a pass. Never fabricate a verdict a capture did not produce.

## Your task

1. **Pre-flight.** Confirm the branch and that `Code/mine-flow-app` is clean
   (`git status --short`); if a concurrent session left files dirty, classify them and preserve
   them — do not absorb them. Repoint `.impeccable/live/roots.json` at `Code/mine-flow-app` and
   re-run `context` to confirm the app is now visible.
2. **Bring the app up.** Start `flutter run -d web-server` with the README's `--dart-define` recipe.
   **Wait for the "is being served at" line** (≈100 s) before loading. Load in a real browser via
   browser automation.
3. **Capture (Web).** For each surface in scope, at a desktop viewport and at a narrow/mobile
   viewport, in both themes: capture a screenshot and record **byte size and pixel dimensions** for
   every artifact. Anything in the 68-byte / 1×1 class is a **harness defect**, reported as such —
   never as visual evidence. State the command/route that produced each artifact.
4. **Capture (Android).** If a `Pixel_6a` emulator (ADR-0017) is available, repeat the shell capture
   for Android portrait. If it is not available, record the Android leg as **`Unverified`** with the
   blocker — do not substitute a narrow browser window and call it Android.
5. **a11y evidence.** Enable semantics, dump the `flt-semantics` tree for the login form and the
   shell navigation, and record focus order. Score against Doc 07's WCAG 2.1 AA target and the
   54.1 rubric's a11y dimension. Record concrete gaps (missing accessible name, unreachable focus
   stop, touch-target evidence where measurable) as findings.
6. **Detector honesty pass.** Run `detect` against both a Dart source path and the live URL, and
   inject `/detect.js`, and record the **no-signal** outcome (spike fact 9) as a finding with the
   false-positive example. Do not present the empty result as verification.
7. **Write the findings** and hand off. Nothing else.

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.10a-NNN` ID, verdict (`Aligned` / `Needs polish` / `Needs restructure` /
  `Unverified`), `file:line` citation for any source claim, and one sentence of *why* (Explanatory
  style — explain the reason a state is a defect, not just that it is).
- **Every capture artifact records its byte size and pixel dimensions, plus the surface, viewport,
  theme, and the command that produced it.** An artifact without those is not evidence.
- Every runtime claim that could not be evidenced is listed under Limitations with its blocker.
- Anchor your verdicts to Doc 07 sections and the 54.1 rubric dimensions — not to the skill's own
  taste, and not to a detector that cannot see this UI.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.10a-FINDINGS.md` — coverage table (surface ×
  platform × theme × artifact), findings table, a11y tree/focus record, verification record,
  limitations. Follow the STEP-48 runtime-design-review table shape used by 54.1–54.10.

## Cleanup (mandatory — the next substep must inherit a clean machine)

- Stop the skill's live-server (`impeccable live-server stop`) and stop the Flutter process.
- Verify both ports are free (a killed parent can leave a child `dart` process holding the port —
  find it with `netstat -ano | grep LISTENING` and terminate the PID) and that
  `Code/mine-flow-app` `git status --short` is clean.
- Note any runtime state the skill created under `.impeccable/live/` (session/annotation dirs) in
  the findings so it is not mistaken for a tracked change.

## Keeping the docs true  (always)

- Findings only — no doc edits, no code edits, no ADR edits, no `risks.yml` edits (54.11
  consolidates risks).
- **Escalate to the user, and record the escalation**, on: (a) a captured runtime behaviour that
  contradicts a locked decision D1–D8 or an accepted ADR; (b) a D1–D8/ADR conflict; (c) being
  tempted to record a runtime claim the harness cannot evidence; (d) discovering the capture route
  is unavailable in your session — report that plainly rather than improvising a weaker substitute.
- **If the login screen still lacks the In-app Privacy Notice** (RISK-0011 / STEP-48 DR-0003), that
  is a compliance finding surfaced at a live surface — escalate it directly to the user, don't leave
  it as one table row.

## Definition of done

- [ ] `.impeccable/live/roots.json` repointed at `Code/mine-flow-app`; `context` confirms the app is
      visible; the correction is recorded.
- [ ] Web captures for the shell + shared surfaces, both viewports and both themes, each with byte
      size, pixel dimensions, and the producing command — none in the placeholder class.
- [ ] Android leg either genuinely captured (Pixel_6a) or explicitly `Unverified` with its blocker.
- [ ] `flt-semantics` tree + focus order recorded for login and shell navigation; a11y gaps scored
      against Doc 07's WCAG 2.1 AA target.
- [ ] Detector no-signal recorded as a finding, with the false-positive example and the CanvasKit
      cause; no "no anti-patterns" result reported as verification.
- [ ] `FC-54.10a-NNN` findings table with the four required fields; every unevidenced claim under
      Limitations.
- [ ] live-server stopped, Flutter stopped, both ports free, app repo clean.
- [ ] No application code, docs, ADRs, or `risks.yml` modified.
- [ ] PLAN's substep table updated (54.10a → Done).

## Next

Update the PLAN's substep table (54.10a → Done) and tell the user: *"run substep 54.11"* — in a
**fresh chat**. 54.11 consumes this findings file alongside 54.1–54.10 and owes its `Unverified`
items a place in the master spec's evidence appendix.
