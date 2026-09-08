# mine-flow — STEP-48.13: Runtime Impeccable Design Review with Automated Screenshots (settles 45.14)

> **How to run:** tell your agent *"run substep 48.13"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** The heaviest engineering task in the STEP — a screenshot
harness under `flutter drive` with an `onScreenshot` hook, driven across a 3×2×2 matrix — but
`architecture/07-ui-design-system.md` and the design-review runbook state the expected answers, so the
judgement is bounded. **Escalate to Opus 4.8** if the implementation appears to deviate from Doc 07 in a
way that might warrant an ADR rather than a finding (the runbook forbids silently changing the design to
match code), or if you find yourself tempted to PASS a visual verdict the harness cannot actually
evidence — label it Unverified and escalate instead.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings (48.2 set up the
screenshot artifact plumbing) and any journey findings available — 48.11's route work informs the
sidebar check, 48.6's and 48.9's cosmetic observations were handed here deliberately.

STEP-45 row 45.14: `Deferred — reports/2026-08-27-step-0045-runtime-design-review.md records every
item (responsive, themes, localization, a11y, NR-002, NR-003, RISK-0011) as Unverified; no
screenshots captured; RISK-0015, RISK-0016 raised → STEP-48`.

That existing report is worth reading precisely because it is a catalogue of what *not* to produce.
Every one of its six sections says **Unverified**, for two stated reasons: no staging credentials,
and *"running in a text-only, headless automation environment without a visual web driver or UI
inspection tool"*. Both blockers are now gone — 48.0 supplied credentials and a working
chromedriver/emulator, and PLAN decision **D4** requires **automated screenshot capture**, committed
under `Code/mine-flow-docs/reports/design-review/`.

This substep settles **three named risks** at once:

- **RISK-0015** (`monitoring`, NR-002) — *"LoginPage light-mode fidelity on device"*: confirm the
  login card follows the theme in light mode.
- **RISK-0016** (`monitoring`, NR-003) — *"Sidebar active-state on group routes on web"*: navigate to
  `/operations`, `/teams`, `/tools` on a web build and confirm the correct sidebar item highlights.
- **RISK-0011** (`open`, **high**, privacy) — *"In-app Privacy Notice absent from first-login flow"*:
  Doc 17 §3 requires a "Terms of Use & Privacy Notice" on first login; STEP-44 found **zero** matches
  for privacy/terms/privasi patterns across all Dart presentation files. Your job is to **record the
  runtime status**, not to build the notice. If it is still absent, RISK-0011 stays open as a
  pre-release gate — that is the honest outcome, and it must not be quietly downgraded.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — decision D4 (automated screenshots, committed), the
  honesty rule, and **Q6** (screenshot storage).
- `…-48.0-FINDINGS.md` (chromedriver/emulator status), `…-48.2-FINDINGS.md` (artifact plumbing), plus
  any journey findings that handed cosmetic issues here.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-docs/runbooks/impeccable-design-review.md`** — the procedure. Follow it. Note its
  **review-first boundary**: gather evidence and present findings *before* remediating; a separately
  authorised substep owns fixes. Note also its instruction that if runtime access is unavailable, all
  visual verdicts are **Unverified** — never PASSed from source.
- **`Code/mine-flow-docs/templates/reports/design-review/impeccable-design-review-report-template.md`**
  — your report's structure (coverage table, contract/bridge parity, findings table with DR-NNNN ids,
  verification record).
- **`Code/mine-flow-docs/architecture/07-ui-design-system.md`** — the canonical contract. Relevant
  specifics: **Compact** density with ForUI spacing tokens; *"Adaptive layouts. Web relies on standard
  breakpoints for sidebar expansion; Android locks to portrait mobile"*; navigation is
  **Sidebar (Web) + Tab Bar with 5 visible items (Mobile)**; Geist font and the 5-item mobile nav were
  formalised in **ADR-0009**.
- `Code/mine-flow-docs/adr/ADR-0008-impeccable-bridge.md` and later UI ADRs (ADR-0009, ADR-0012…0016).
- `Code/mine-flow-docs/reports/2026-08-27-step-0045-runtime-design-review.md` — the all-Unverified
  predecessor. **Do not rewrite it**; archived reports are immutable. You write a new one.
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0011, RISK-0015, RISK-0016 verbatim; also
  RISK-0003 (accepted Phase 2 spacing/colour drift) and RISK-0004 (~28 legacy files with hardcoded
  strings — relevant to the localization check).
- `Code/mine-flow-app/lib/app/` — theme setup, `AppShell`, and the `SettingsCubit` locale wiring from
  STEP-38.3 (locale flows to `MaterialApp.router` via `SettingsEntity.locale`).

## Scope

**In scope:** capturing real screenshots across breakpoints, themes, and locales; verifying
responsive layout, theme fidelity, localization, and accessibility at runtime; settling NR-002 and
NR-003; recording RISK-0011's runtime status; writing the report.

**Not in scope:** remediating findings (the runbook forbids it in the same pass — findings go to a
named owner and, if needed, a follow-up STEP), building the privacy notice, editing
`architecture/07-ui-design-system.md`, hand-editing root `DESIGN.md` / `PRODUCT.md` (**generated —
never edit**), `risks.yml` edits (48.14), other doc edits (48.15).

## Your task

### 1. Build the screenshot capture harness

`IntegrationTestWidgetsFlutterBinding` exposes `takeScreenshot(name)`, which only works under
`flutter drive` (the driver writes the bytes out). Create a dedicated target — e.g.
`integration_test/design_review_capture_test.dart` — that logs in and walks the key screens,
capturing at each configuration. On web, `binding.takeScreenshot` requires the driver's
`onScreenshot` hook; wire it in `test_driver/integration_test.dart` to write files to a directory
you choose. Read the current driver file first — it is currently the one-line default
`integrationDriver()`.

Capture matrix (**3 breakpoints × 2 themes × 2 locales**):

- **Breakpoints:** a narrow phone width, a tablet width, and a wide desktop width. Derive the exact
  values from the app's own breakpoint constants rather than inventing them — and note Doc 07's rule
  that **Android locks to portrait mobile**, so the wide captures are a web concern.
- **Themes:** light and dark.
- **Locales:** `id` and `en`, driven through the `SettingsCubit` locale path (STEP-38.3).

Key screens, not every screen (Q6: keep the committed image count bounded): login, dashboard, one
data-dense list, one form, and the sidebar/nav in each of the three route groups.

### 2. Settle NR-002 (RISK-0015)

Capture the login page in **light mode** on a device/emulator and confirm the login card follows the
theme — background, border, and text tokens from Doc 07, not a hardcoded dark-assumption colour.
Attach the screenshot as evidence. Verdict: Verified, or a DR finding with the mismatch named.

### 3. Settle NR-003 (RISK-0016)

On a **web** build, navigate to `/operations`, `/teams`, and `/tools` and confirm the correct sidebar
item shows its active state for each group route. This is the finding STEP-46 could not settle
statically. 48.11's route work may already tell you whether group routes resolve; the *active-state
highlight* is this substep's question. Attach a screenshot per group route.

### 4. Record RISK-0011's runtime status

Log in as a **fresh** user (or clear stored state) and observe whether any Terms/Privacy notice
appears. STEP-44's static scan found none. If none appears, record: **still absent — RISK-0011
remains an open pre-release gate**. Do not build it, and do not soften the risk. If one has since
appeared, capture it and say so.

### 5. Run the runbook's verification record

Complete every row of the template's verification table with real evidence: information hierarchy and
density (Doc 07 says **Compact**), mobile/responsive layout, desktop/sidebar layout, theme and token
consistency, interaction and navigation (touch, click, keyboard, back), accessibility (focus order,
semantics, text scaling, contrast), and localization.

On accessibility, be precise about what an automated pass can and cannot show. Semantics-tree
inspection and contrast measurement are checkable; a screen-reader experience is not, from this
harness. Label the latter **Unverified** with the reason rather than guessing — that is exactly the
distinction the runbook demands.

On localization, expect gaps: **RISK-0004** records ~28 legacy presentation files still holding
hardcoded strings. Mixed-language screens are likely a **known** deferral, not a new finding — check
RISK-0004 before raising one, and note which screens you observed.

### 6. Contract and bridge parity

Per the runbook: confirm root `DESIGN.md` / `PRODUCT.md` still derive from Doc 07 and report **bridge
drift** if their substance diverges. **Do not edit them** — they are generated by
`scripts/impeccable-bridge.ps1`, and regeneration is a separately authorised task. Record drift as a
finding for 48.15 to route.

### 7. Commit the evidence

Write screenshots to `Code/mine-flow-docs/reports/design-review/step-0048/` and commit them (D4/Q6).
CI artifacts expire; a design review whose evidence is a dead artifact link cannot be re-reviewed.
Keep the count bounded and the filenames self-describing
(`<screen>-<breakpoint>-<theme>-<locale>.png`). No screenshot may contain credentials, tokens, or
sensitive operational data.

### 8. Write the report

`Code/mine-flow-docs/reports/2026-08-29-step-0048-runtime-design-review.md` (adjust the date to the
actual run date), from the template. Every finding gets a `DR-NNNN` id, a verdict
(Verified / Blocking / Needs remediation / Approved deviation / Unverified), runtime evidence (the
committed screenshot path), and a **named owner plus follow-up STEP** where remediation is needed.
The runbook is explicit: a Blocking / Needs-remediation / Unverified result must carry an owning STEP,
not float.

## Verification

- Screenshots exist and are committed for the full matrix of key screens; paths cited in the report.
- NR-002 and NR-003 each carry a verdict backed by a specific image.
- RISK-0011's runtime status recorded truthfully.
- Every verification-record row completed — anything not provable by this harness labelled
  **Unverified with a reason**, never passed from source.
- The report follows the template and every non-Verified finding names an owner and follow-up STEP.
- Root `DESIGN.md` / `PRODUCT.md` **not modified** (`git status` proves it).
- `Code/mine-flow-docs/reports/2026-08-27-step-0045-runtime-design-review.md` **not modified**.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean (the capture test is
  Dart code and is held to the same bar).
- `flutter test` → green (the `attendance_daily_log_sync_test.dart` Hive flake is known: re-run
  isolated to confirm, and say so).
- No credentials or sensitive data in any screenshot, log, or report.

## Keeping the docs true

If the implementation deviates from Doc 07, the runbook is unambiguous: **the review does not
silently change the design to match code.** An intentional deviation needs an explicit owner decision
and, if material, an ADR plus a Doc 07 version-log entry — hand that to 48.15 and the user, do not
enact it here. New/changed functions (the capture harness) get docstrings. `risks.yml` edits belong to
48.14; supply evidence and a close-or-re-justify recommendation for RISK-0011, RISK-0015, RISK-0016.

## Definition of done

- [ ] Screenshot capture harness working under `flutter drive` on web and on the emulator; committed.
- [ ] Full matrix captured for the key screens: 3 breakpoints × light/dark × `id`/`en`.
- [ ] Images committed under `Code/mine-flow-docs/reports/design-review/step-0048/` with
      self-describing names and no sensitive content.
- [ ] **NR-002 / RISK-0015** settled with image evidence.
- [ ] **NR-003 / RISK-0016** settled with per-group-route web image evidence.
- [ ] **RISK-0011** runtime status recorded honestly; not built, not downgraded.
- [ ] Every verification-record row completed; unprovable items labelled Unverified with reasons.
- [ ] Bridge parity checked; drift reported without editing the generated files.
- [ ] Report written from the template at
      `Code/mine-flow-docs/reports/2026-08-29-step-0048-runtime-design-review.md`, every finding with
      a DR id, verdict, evidence path, and owner/follow-up STEP.
- [ ] Close-or-re-justify recommendations for RISK-0011/0015/0016 written for 48.14.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green.
- [ ] Committed on `step-0048-runtime-evidence` in both `mine-flow-app` and `mine-flow-docs`.

## Next

Tell the user the next action is *"run substep 48.14"* (risk-register reconciliation) in a **fresh
chat**, and update 48.13's status in the STEP PLAN. Note that 48.14 needs every journey substep's
findings, so confirm 48.3–48.12 are all complete before it starts.
