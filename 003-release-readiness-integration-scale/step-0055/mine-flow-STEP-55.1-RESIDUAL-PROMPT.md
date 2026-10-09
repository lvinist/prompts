# mine-flow — STEP-55.1 RESIDUAL: picker escalation, snapshot param, dialog test depth

> **How to run:** Tell your agent "run 55.1 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Same tier as 55.1 — bounded reasoning inside master spec §3.

## Context

The 55.1 dialog works (`AppContextualReportDialog` + `ReportConfigContent`, used by Cut & Fill and Land Clearing with correct prefill) on branch `step-0055-cohesive-ui-rebuild`. The audit (2026-09-19, index row 55.1) found three residuals. **The first is an owner decision, not an implementation default** — the lane must gate on it before coding.

## Residual scope (exact — nothing else)

From the index row 55.1:

1. **OWNER GATE — resolve before any code.** `/reports/config` still serves the generic `ReportTypePickerPage` (`lib/app/router.dart:992-1011`), but spec §3.1 requires only a compatibility redirect or explicit no-context state. CF-030's deep-link usability argues the other way. Ask the owner to pick: (a) bless the picker as an approved deviation via ADR/risk entry (then this lane is docs + tests only, no router change), or (b) implement the spec's redirect/no-context state. Do not infer; do not code both.
2. Add the missing immutable origin-filter snapshot param to the dialog API (spec §3.1 required input) — diagnostics/tests only, must not mutate list state.
3. Expand dialog tests to the prompt's list: context prefill, unsupported-filters-preserved-but-not-shown, loading duplicate prevention, error/retry with config intact, focus trap/return, Escape/back/barrier, localization/text scale, compatibility route without `extra`. The file has **one** test today; land the missing coverage.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md`
- `Code/mine-flow-docs/reports/2026-09-11-step-54-master-polish-spec.md` §3 (D6 contract, report inventory)
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` §4.2
- `Upcoming Prompts/mine-flow-STEP-55.1-FINDINGS.md` (thin baseline)
- `Code/mine-flow-app/lib/features/reporting/presentation/widgets/app_contextual_report_dialog.dart`, `report_config_content.dart`, `lib/features/reporting/presentation/pages/report_config_page.dart`, `report_type_picker_page.dart`, `lib/app/router.dart` (report-config route only)
- `Code/mine-flow-app/test/features/reporting/**` (extend)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app` (expect `step-0055-cohesive-ui-rebuild`). Preserve the untracked 55.11 files listed in the 55.0 residual prompt. Never stash/reset/absorb.
2. Run the owner gate FIRST, in chat, before any edit. Record the decision + date in FINDINGS. Branch (a) → no router edit at all. Branch (b) → router change limited to the report-config route hunks with staged-index proof (`git diff --cached` must show only those hunks).

## Likely files (ownership boundary)

- ALLOWED: `lib/features/reporting/presentation/widgets/app_contextual_report_dialog.dart`, `report_config_content.dart`, `report_config_page.dart` (compat handling only), `test/features/reporting/**`, router report-config hunks only under branch (b), `Upcoming Prompts/mine-flow-STEP-55.1-FINDINGS.md` (append only).
- FORBIDDEN: `lib/features/tracking/**`, `lib/features/benchmark/**`, other feature entry points (they migrate in their own lanes), `lib/l10n/**` unless a compat string proves necessary (then use the ARB workflow + baseline guard).

## Tests and verification

- `flutter test test/features/reporting/`
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- If ARB touched: `dart run tool/check_l10n_baseline.dart`
- Record exact commands + counts. Keep runtime screen-reader flow marked Unverified (mechanical tests only).

## Boundaries and escalation

- No new report type, no PDF semantic change, no Data Bucket/Timeline reports, no list-filter mutation from inside the dialog.
- Stop if dependencies can't be injected without a public architecture change, or the same fix fails twice. Never print secrets.

## Definition of done

- Owner decision recorded; snapshot param present and pinned by tests; dialog coverage lands per the list above; gates green; FINDINGS has a dated "Residual fix (55.1)" section with decision, commands/counts, traceability, and Unverified items.

## Next

Report the exact replacement evidence-cell line for index row 55.1 (do **not** edit the index yourself). Tell the user to run the 55.2 residual in a fresh chat.
