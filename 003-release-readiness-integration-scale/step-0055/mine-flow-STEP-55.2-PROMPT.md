# mine-flow — STEP-55.2: Cut & Fill Migration and Polish

> **How to run:** Tell your agent “run substep 55.2”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** This is a bounded adoption of the tested 55.0/55.1 primitives with explicit routes, no D7 inspector, and focused regression signals.

## Context
Migrate the Cut & Fill lifecycle to route-backed responsive create/edit sheets and contextual reporting. Preserve its direct-to-edit D7 decision and existing domain semantics.

## Read first
- STEP-55 PLAN; 55.0/55.1 findings and shared APIs
- master spec §4.1, route/report/D7 tables, §§6–7
- Doc 07 v0.5.0; Test Strategy; app README/ARCHITECTURE
- `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
- `cut_fill_form_screen.dart`, CutFill BLoC/entities/repository, `lib/app/router.dart`
- matching tests and STEP-54.2 findings

## Impeccable
Run context once; no init/document/extract. Use `layout` for list/sheet hierarchy, native `adapt` for bottom-sheet/IME behavior, then one bounded `polish` pass across list → form → report in light/dark and wide/narrow states.

## Task
- Add canonical create `/operations/cut-fill/form` and edit `/operations/cut-fill/:id/form` behavior; cold edit fetches by ID and `extra` remains optional cache.
- Open form through `AppResponsiveSheet`; preserve `from`, `to`, `zoneId`, scroll, list BLoC/data, and invoker focus.
- Bind all close paths to D4 using the form’s real dirty state.
- Replace report route push with `ReportType.cutFill` contextual dialog seeded from active date/zone.
- Preserve direct list → edit; do not add a detail inspector.
- Replace actionable Material FAB/date/text controls with shared/ForUI equivalents without altering volume/domain calculations.
- Add localized strings only through ARB.

## Tests and verification
Add/update router, BLoC, and widget tests for create/edit cold routes, absent `extra`, invalid/not-found ID, query/filter preservation, all dirty dismissals, failed save retaining input, report context/state retention, direct-to-edit, Web sheet geometry, Android IME/back/drag, validation/error/empty states, semantics/48dp/text scale/themes.

Run focused Cut & Fill + router/shared suites, format, analyze, and guards. Create `mine-flow-STEP-55.2-FINDINGS.md` with `FC-54.2-001..007` traceability and real runtime artifact metadata.

## Boundaries
No new inspector, schema change, report type, formula change, or local modal implementation. Escalate on data-unit/precision drift, unresolved route reconstruction, or two failed attempts at the same fix.

## Definition of done
Every Cut & Fill create/edit/report path uses shared contracts, restores by URL, preserves list state, passes focused/static gates, and has bounded Web/Android polish evidence.

## Next
Run substep 55.3 in a fresh chat.
