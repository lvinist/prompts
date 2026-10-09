# mine-flow — STEP-55.1: Contextual Report Dialog Architecture

> **How to run:** Tell your agent “run substep 55.1”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** The refactor spans report state, focus, responsive dialogs, and compatibility routing, but master spec §3 fully bounds the intended behavior.

## Context
55.0 supplies shared modal primitives. Replace standalone report configuration navigation with one pre-bound contextual dialog while retaining reusable report configuration logic. This substep builds D6; feature entry-point migrations occur in 55.2–55.8.

## Read first
- STEP-55 PLAN and 55.0 findings
- master spec §§3, 6–7, 9 and report inventory
- Doc 07 §§3–5; Test Strategy
- app README/ARCHITECTURE
- `lib/features/reporting/presentation/pages/report_config_page.dart`
- report Cubit/domain/repository files and `lib/app/router.dart`
- existing `test/features/reporting/**`
- STEP-54 `54.1`, `54.10a` findings for D6/runtime evidence

## Impeccable
Run context once; no init/document/extract. Use `layout` for dialog hierarchy/density, `harden` for loading/error/success/long-content behavior, and a bounded `polish` pass. Inspect desktop and narrow/Android dialog layouts together.

## Task
1. Extract presentation-neutral `ReportConfigContent` from the page without duplicating business logic.
2. Implement `AppContextualReportDialog` accepting non-null `ReportType`, source feature/title, initial supported date/zone context, immutable origin-filter snapshot, dependencies, and completion callback.
3. Keep origin route/tree/BLoC/filter/scroll mounted and inert behind the dialog.
4. Implement loading lock/announcement, retry-with-config-preserved, success share/print/download/Tutup states, focus trap/return, barrier/Escape/back semantics, 48dp actions, reduced motion, 640dp desktop max, mobile safe-area/internal scroll.
5. Remove the generic picker from normal feature flows. Keep `/reports/config` only as a safe compatibility redirect or explicit no-context state; no durable behavior may depend only on `extra`.
6. Add APIs/tests that feature substeps can adopt without local report-dialog variants.

## Tests
Update/create report widget/Cubit/router tests for: pre-bound type and no picker; context prefill; unsupported filters preserved but not falsely shown; origin state retained; loading duplicate prevention; error/retry; success actions; desktop/narrow layout; focus trap/return; Escape/back/barrier; localization/text scale; compatibility route without `extra`.

Run focused reporting/router suites, format, analyze, and applicable guards. Produce `mine-flow-STEP-55.1-FINDINGS.md` with changed-file ledger, commands/results, `FC-54.*` traceability, Impeccable evidence, and Unverified items.

## Boundaries
Do not migrate all feature buttons, change PDF business semantics, add a report type, or invent Data Bucket/Timeline reports. Do not alter list filters from within the report dialog.

Escalate if report dependencies cannot be injected without a public architecture change, compatibility routing conflicts with an accepted ADR, or runtime focus/modality cannot be evidenced.

## Definition of done
One canonical contextual report dialog exists, normal API cannot open without a bound type, origin context is preserved, tests/static gates pass, and later feature prompts have a stable integration surface.

## Next
Run substep 55.2 in a fresh chat.
