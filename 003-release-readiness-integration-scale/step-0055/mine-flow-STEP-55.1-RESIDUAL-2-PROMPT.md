# mine-flow — STEP-55.1 RESIDUAL-2: transition the orphaned ReportTypePickerPage

> **How to run:** Tell your agent "run 55.1 residual-2 fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Same tier as 55.1 — bounded reasoning inside master spec §3.

## Context

The 2026-09-21 residual review re-verified the 55.1 residual lane against disk: the owner gate was resolved (branch b — spec §3.1 explicit no-context state), the router's report-config route hunks were edited with staged-index proof (`ReportTypePickerPage` import removed, `ReportConfigPage` rendered without extra), `originFiltersSnapshot` was added to the dialog API, and the test suite expanded (reporting 20/20: cubit 7, config page 5, dialog 8; format/analyze/l10n-guard clean; router CRLF convention preserved). That work is verified complete but was left **uncommitted** — see Pre-flight.

One deviation from the docs was found:

- **`ReportTypePickerPage` is now orphaned dead code.** With the router import removed (commit pending), the file `lib/features/reporting/presentation/pages/report_type_picker_page.dart` has **zero references anywhere** in `lib/` or `test/` (verified 2026-09-21 by reference sweep). The 55.1 residual prompt's scope ended at the router hunks and did not name the file's fate. Master spec §3.1 demoted the generic picker to a compatibility state — a dead file contradicts the "no opportunistic feature-folder rewrite" boundary in one direction and the spec's intent in the other: the picker's UI (including its `reportTypePickerTitle` l10n key, migrated in 48.29) is now unreachable.

## Residual scope (exact — nothing else)

1. **First, gate on the file's disposition — this is an owner decision with three options.** Present it in chat before any edit:
   - (a) **Delete** `report_type_picker_page.dart` (and the now-unreferenced `reportTypePickerTitle` l10n key + ARB entries + any picker-only test helpers) — cleanest, matches spec §3.1's demotion;
   - (b) **Keep** the file with a dated header justification (e.g. retained for potential future standalone Reports landing page) — lowest churn;
   - (c) **Defer** to a later STEP with a risk-register-style note.
   Do not infer; do not delete without the owner's answer.
2. Record the decision + date in FINDINGS. Only the chosen option is executed.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md` (ground rules, evidence contract)
- `Upcoming Prompts/mine-flow-STEP-55.1-FINDINGS.md` (baseline + residual fix 2026-09-21)
- `Code/mine-flow-docs/reports/2026-09-11-step-54-master-polish-spec.md` §3 (D6 contract, picker demotion)
- `lib/features/reporting/presentation/pages/report_type_picker_page.dart` (the orphan)
- `lib/app/router.dart` (report-config route only — confirm the picker import is gone)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app` (expect `step-0055-cohesive-ui-rebuild`). Preserve the untracked 55.11 files listed in the 55.0 residual prompt. Never stash/reset/absorb.
2. **As of the 2026-09-21 review, the tree carried uncommitted 55.0/55.1 residual lanes** (router.dart report-config hunks + `report_config_page.dart` + `app_contextual_report_dialog.dart` + `app_interaction_primitives.dart` + their tests). That work is verified complete (review 2026-09-21). If it is still dirty, commit it FIRST, one commit per owning substep (`fix(55.0): ...`, `fix(55.1): ...`), staged to only each lane's files — or obtain the owner's decision to leave it dirty. Never bundle lanes.
3. Run the owner gate FIRST, in chat, before any edit.

## Likely files (ownership boundary)

- ALLOWED (per owner's choice): delete `report_type_picker_page.dart` + its `reportTypePickerTitle` key in `lib/l10n/app_{id,en}.arb` + regenerated l10n output; or add a header justification to the file; or write the deferral note only in `Upcoming Prompts/mine-flow-STEP-55.1-FINDINGS.md` (append only).
- FORBIDDEN: other feature entry points (they migrate in their own lanes), reporting dialog internals beyond the above, `tool/check_l10n_baseline.dart` (note: the file IS on the exemption list at line 66 — if deleted, remove its exemption line only as part of this lane's ARB/l10n work), docs, index.

## Tests and verification

- `flutter test test/features/reporting/` (expect 20/20 still, or fewer if picker tests are removed with the delete option)
- If ARB touched: `dart run tool/check_l10n_baseline.dart` + regenerate output
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- Verify the orphan claim yourself before executing: `grep -rn "ReportTypePickerPage" lib/ test/ --include="*.dart" -l` must return only the file itself.
- Record exact commands + counts.

## Boundaries and escalation

- No new report type, no PDF semantic change, no Data Bucket/Timeline reports, no dialog API change.
- Stop if the deletion would break a test or import the sweep missed (re-run the reference sweep). Never print secrets.

## Definition of done

- Owner decision recorded with date; the chosen disposition executed and verified by reference sweep + gates; FINDINGS has a dated "Residual fix 2 (55.1)" section with the decision, commands/counts, and the orphan finding.

## Next

Report the exact replacement evidence-cell line for index row 55.1 (do **not** edit the index yourself). Tell the user to run the 55.2 residual-2 in a fresh chat.
