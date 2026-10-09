# mine-flow — STEP-55.11: Multiplatform Impeccable Audit, Verification, Docs, and Close

> **How to run:** Tell your agent “run substep 55.11”. Execute cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** The deliverable is an honest release-quality verdict from runtime evidence plus durable docs/risks/close records; a falsely green result would be silent and expensive.

## Context
Audit and close STEP-55 only after 55.0–55.10 are complete. Do not use this substep to hide feature implementation gaps. It may fix audit defects in one bounded batch when they remain within the approved specification; architecture/product conflicts require user review.

## Read first
- STEP-55 PLAN and every 55.0–55.10 findings file
- master spec §§7–9 and complete traceability appendix
- Doc 07 v0.5.0; Docs 04/06/08/09/11/12/15/16/17; ADR/risk registries
- app/docs/prompts READMEs, branch/worktree state, CI workflow, E2E guards
- STEP-54.10a findings and runtime-evidence reference
- Impeccable `audit`, native audit, `polish`, and applicable platform guidance

## Pre-flight
- Reconcile app/docs/prompts current heads, dirty files, substep commits, PLAN rows, and every claimed test/evidence result.
- Verify sensitive-header redaction tests before launching Android or browser capture. Stop and destroy/redact unsafe output if any credential appears.
- Prove all required test/evidence paths exist and note substitutions. Do not reuse stale screenshots or previous wrappers.

## Impeccable audit protocol
Run context once; no init/document/extract. Use Web technical audit and native Android audit as structured rubrics, adapted to Flutter CanvasKit. `impeccable detect` may run once as a mechanical supplement, but its known DOM/CSS blindness and false positives cannot score or pass the app.

Execute a maximum two-round cycle: (1) capture all required states/platforms together, score and batch defects; (2) after one consolidated fix batch, recapture only affected/required confirmations. Stop after confirmation and report remaining gaps.

## Required runtime matrix
- Web widths: 799, 800, 801, 1024, >=1280 logical px; practical height >=720.
- Android: Pixel_6a portrait; authenticated supervisor plus field role where credentials permit.
- Themes: Light, Dark, and live System brightness change.
- Text: 1.0x, 1.3x, 2.0x on representative short and long surfaces.
- Inputs: mouse, keyboard-only Web, touch, Escape, browser navigation, Android/predictive back, IME.
- Routes: representative create/edit/detail cold URL, refresh, back/forward, invalid and unauthorized ID.
- States: loading, first-use, filtered empty, validation, backend error/retry, success, dirty, busy, offline queued/failed.
- Paths: shell/login/privacy, one short form, Attendance batch, Daily Log long form/review, Equipment/Inventory long detail, report dialog, Data Bucket cancel/retry.

Every image record includes command/route, platform/viewport/device, theme/state, bytes, and dimensions. Use browser AX/`flt-semantics` plus Android accessibility evidence; source `Semantics` is not proof.

## Measured acceptance
- Contrast: WCAG AA 4.5:1 normal text, 3:1 large text and essential UI/focus.
- Every interactive target >=48x48 logical px.
- Desktop AX navigation/header; five mobile tabs; modal titles/modality; explicit field/status/error names.
- Web language follows active locale; Indonesian UI uses `id`.
- Keyboard order/focus/trap/return and all dirty dismissals behave identically.
- No overflow, sidebar obstruction, nested scroll trap, clipped footer, or IME collision.
- Motion 150–200ms; reduced motion removes spatial movement without hiding state change.
- Durable routes reconstruct without extra; filters/date behavior obeys popover/dialog rules.
- Artifacts contain no credentials, PII, tokens, or sensitive operational data.

Generate `Code/mine-flow-docs/reports/2026-09-11-step-55-multiplatform-impeccable-audit.md` (use actual run date if different) with separate Web and Android 0–20 health scores, severity-counted findings, positive findings, evidence inventory, fixed vs remaining issues, and explicit Unverified blockers.

## Automated gates
Run and record exact exit/results:
- `dart format --output=none --set-exit-if-changed .`
- `flutter analyze`
- l10n/Supabase/generated contract guards used by CI
- `flutter test` (100% pass; adjudicate flakes per workflow, never erase first result)
- `flutter build web --release`
- Android build required by CI
- Web and Android E2E jobs with non-zero journey guards on the exact branch head
- `./doctor.sh check` and duplicate STEP scan

## Reconciliation and close
1. Reconcile all 127 `FC-54.*` IDs and every master-spec completion item to implementation commits/tests/evidence or explicit approved escalation.
2. Update architecture docs/version logs, ADRs, risks, generated contracts, README/test records wherever implementation changed truth. Do not rewrite accepted ADR decisions.
3. Write `mine-flow-STEP-55.11-FINDINGS.md` and finish the PLAN checklist/status.
4. Present the accountable user with the audit verdict, remaining risks/Unverified items, and exact proposed close side effects. **Stop for explicit approval** before index Done, archive, merge/push, or branch deletion.
5. After approval: commit/push app and docs branches, merge per project conventions, archive PLAN/prompts/findings/evidence to `prompts/003-release-readiness-integration-scale/step-0055/`, update phase README and STEP-index to Done, commit/push prompts, delete verified merged branches, rerun status/check/duplicate/clean-sync checks.

## Boundaries and escalation
No detector-only PASS, fake Android evidence from narrow Web, skipped E2E called green, secret printing, production mutation, legal approval claim, broad redesign, or silent acceptance of P0/P1 failures. If a P0/P1 remains, STEP-55 cannot close without explicit ADR/risk/owner disposition.

## Definition of done
The complete matrix and automated gates pass or are honestly dispositioned; traceability is complete; audit artifacts are valid and safe; docs/risks are true; user approved close; all repos are clean/synchronized and STEP-55 is archived Done.

## Next
Run `./doctor.sh status` and tell the user the mechanically resolved next action in a fresh chat.
