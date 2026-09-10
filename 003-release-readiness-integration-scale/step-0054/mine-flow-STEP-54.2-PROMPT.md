# mine-flow — STEP-54.2: Operations Suite 1 — Cut & Fill Volume Tracking Critique

> **How to run:** Tell your agent *"run substep 54.2"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, but bounded by written authority — blueprint D1–D8, Doc 07, and the 54.1 rubric. Weak findings are caught by 54.11's consolidation and STEP-55's implementation.

## Context

STEP-54 critiques each feature as a cohesive lifecycle (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android. This substep covers **Cut & Fill Volume Tracking**, the first Operations feature and the highest-volume data-entry workflow in the app (foremen log cut/fill volumes daily, supervisors review and report on them).

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric published in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**: dimensions, checks, `FC-54.2-NNN` ID scheme, verdict vocabulary, coverage-table shape. Apply it exactly; do not invent your own scheme.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8; this feature is the blueprint's §54.2 exemplar ("list table/cards, entry form sheet, and contextual PDF report dialog")
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md`
- `Code/mine-flow-docs/architecture/04-data-model.md` — the cut/fill fields and their semantics (volume units, zones) so the critique judges the form against real data constraints
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head — the feature lives under `lib/features/tracking/`):
- List: `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
- Form: `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart`
- Supporting widgets: `lib/features/tracking/presentation/widgets/cut_fill_card.dart`, `volume_input_field.dart`, `volume_summary_card.dart`
- Report entry point: how this list reaches `lib/features/reporting/presentation/pages/report_config_page.dart` / `report_type_picker_page.dart` and `lib/core/services/pdf_service.dart` (trace the actual navigation path — is it contextual per D6, or a redirect to a separate screen?)
- BLoC states: `lib/features/tracking/presentation/bloc/` — for the states dimension (loading/empty/error/success/dirty)

**Does NOT touch:** application code (read-only), other features' screens, the rubric itself (propose rubric changes to the user as an escalation, don't fork it).

## Your task

Apply **every** 54.1 rubric dimension to this feature, on both platforms (Web desktop ≥ 1200px, Android portrait ≈ 400dp):

1. **Lifecycle cohesion:** complete the loop List → Form (create/edit) → back to List → Report dialog. Where does the loop break (state lost on return, form not pre-filled on edit, report loses list filters per D6)?
2. **Platform conformance:** the form today is (verify!) a full screen/page — spec its migration to D1 (right side-sheet on Web) / D2 (bottom sheet on Mobile): what must change, what must not. D5: does `/operations/cut-fill/form` exist as a route (router.dart shows `cut-fill` without a form subroute — confirm) — record the deep-link gap.
3. **Interaction states:** enumerate loading/empty/error/success/dirty for both list and form. The dirty-state question is the D4 core: does the current form intercept unsaved changes on X/back/ESC/Android-back at all?
4. **Accessibility & tokens:** contrast, touch targets on mobile, semantics, ForUI-only widgets, Zinc/compact/Lucide conformance. Note any residual Material (cf. STEP-51's anchored-zero sweeps) with the anchored grep pattern.
5. **Report dialog:** per D6 the list's "Buat Laporan" should open a modal pre-bound to this feature's ReportType, preserving filters. Critique the current implementation against that, including what `pdf_service.dart` needs from the dialog contract.
6. **D7 verdict:** does cut/fill need a detail view at all (list card → form-in-edit-mode may suffice), or a side-sheet inspector? Give a verdict + rationale.

## Verification (evidence standard — from the PLAN, mandatory)

- **Every finding:** `FC-54.2-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, and one-sentence *why* (Explanatory style — Level 2 user).
- **Runtime optional and honest:** if you run the app to verify a claim, name the command and report artifact byte-size + pixel dimensions; the 1×1-placeholder class is a harness-defect call-out, not evidence. Unverifiable runtime claims → `Unverified` + blocker.
- **No code changes:** `git status` clean in the app repo at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.2-FINDINGS.md` with the coverage table (STEP-48 shape), findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits in this substep (54.11 consolidates).
- Escalate to the user (record it in findings) if: a finding conflicts with D1–D8 or an accepted ADR; runtime contradicts Doc 07; you're tempted to record an unevidenced runtime claim; the same classification problem recurs twice.
- Accepted-risk-shaped discoveries (e.g. "cannot do X without breaking Y") are recorded as findings for 54.11's risk reconciliation — not edited into `risks.yml` here.

## Definition of done

- [ ] All rubric dimensions scored for list, form, and report path, both platforms.
- [ ] D4 dirty-intercept status and D5 deep-link gap explicitly answered with citations.
- [ ] D7 verdict recorded with rationale.
- [ ] Coverage table, findings table (IDs + verdicts + citations), verification record, limitations — all present.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.2 → Done) and tell the user: *"run substep 54.3"* — in a **fresh chat**.
