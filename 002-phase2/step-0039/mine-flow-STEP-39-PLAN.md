# mine-flow — STEP-39 PLAN: Phase 2 Tier 2 Check-in, Reconciliation & Regression Fixes

**Phase:** Phase 2
**Owner:** AI
**Status:** Done
**Date:** 2026-07-28
**Branch:** `step-0039-check-in`
**Repos (projection):** `Code/mine-flow-docs`, `Code/mine-flow-app`, `prompts`

> This STEP executes a formal Throughstone Check-in to reconcile validated audit findings across implementation, tests, architecture docs, generated Impeccable bridge files, and risk registers. It resolves the low-battery sync requirement and formalizes UI drift decisions.

## Motivation
Phase 2 Tier 2 audit validation uncovered intentional UI deviations from the documented architecture and test semantic crashes. Before closing Phase 2 Tier 2, we must formally reconcile the codebase with the architectural source of truth, implement the missing low-battery sync logic safely, and ensure all tests (including previously skipped ones) and builds pass.

## Decisions already locked
- **Decision A (Typography):** Approve `Geist` font.
- **Decision B (Mobile Navigation):** Approve 5 permanently visible items.
- `registries/risks.yml` will be reviewed.
- `architecture/12-test-strategy.md` applies.

## Pending Decisions (Low-Battery Operating Rule)
The following state table defines the proposed low-battery operating rule ("Hybrid" approach). **Awaiting owner confirmation.**

| Condition / Scenario | Proposed Behavior |
| --- | --- |
| **Primary Rule** | Pause sync if OS Battery Saver is ON **OR** raw battery is `<= 20%`. |
| **Charging State** | Charging completely bypasses the pause (sync proceeds normally). |
| **Sync Type Scope** | Pauses **automatic/background sync only**. Manual user-triggered sync proceeds. |
| **Resumption Trigger** | Queued sync resumes automatically on the next queue tick once the device no longer meets the low-battery condition (e.g., plugged in or battery > 20% and saver OFF). |
| **Queued Operations** | Preserved securely in Hive storage without retry-count penalties while paused. |
| **Fallback: OS Saver status unavailable** | Treat OS Battery Saver as `false` (OFF). Rely solely on numeric battery level. |
| **Fallback: Battery level unavailable** | Treat numeric battery level as `100%` (Healthy). Rely solely on OS Battery Saver flag. |
| **Fallback: Both unavailable (e.g. Web)** | Treat both as healthy (`false`, `100%`). Sync proceeds normally. |

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 39.1 | Check-in baseline and locked-decision record | Baseline status and test results, confirmed STEP reservation and branch state, audit-report dated amendment, durable record of the three owner decisions, exact affected-document and dependency inventory. | - | Confirm low-battery state table |
| 39.2 | Architecture, ADR, dependency, risk, and bridge reconciliation | Updated `07-ui-design-system.md` & `15-native-app-architecture.md`, correct Version Logs, `ADR-0009-ui-design-system-drift.md` (Accepted), `risks.yml` review, `battery_plus` dependency supply-chain review, regenerated `DESIGN.md`/`PRODUCT.md`, documentation/link checks. | 39.1 | None |
| 39.3 | Analyzer and app-bar discrepancy investigation | Clean `equipment_history_screen.dart`, investigated and resolved app-bar action expectation discrepancies requiring investigation in `inventory_dashboard_screen_test.dart` and `data_bucket_list_page_test.dart`. | 39.2 | None |
| 39.4 | Equipment semantics failure diagnosis and resolution | Isolated test wrapper or pump fix for `equipment_check_form_test.dart`. | 39.3 | None |
| 39.5 | Low-battery sync implementation and tests | `battery_plus` dependency added, `sync_queue_manager.dart` updated, sync unit tests verifying the exact state table. | 39.4 | None |
| 39.6 | Full verification, check-in report, review, and archival | Check-in report, passing gates (all tests, APK build, doctor), archived STEP in `prompts/002-phase2/step-0039/`. | 39.5 | None |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| UI/Widget | 39.3 | Investigate and resolve app-bar action expectation discrepancies requiring investigation (`create_new_inventory_appbar_button` missing in `inventory_dashboard_screen_test.dart`, `upload_file_appbar_button` missing in `data_bucket_list_page_test.dart`) by comparing expectations against STEP PLANs, UI contracts, route implementation, later STEP changes, and intended user workflow | Per substep | `flutter test test/features/tracking` & `test/features/data_bucket` | - |
| UI/Widget | 39.4 | Fix `_RenderObjectSemantics` crash in `Code/mine-flow-app/test/widget/equipment_check_form_test.dart` via wrapper/pump | Per substep | `flutter test test/widget/equipment_check_form_test.dart` | Controlled reproduction first |
| Unit (Sync) | 39.5 | Injectable battery abstraction tests for `Code/mine-flow-app/lib/core/offline/sync_queue_manager.dart` | Per substep | `flutter test test/integration/sync_queue_manager_test.dart` | Mock battery state |
| All | 39.6 | All discovered test files (including previously skipped unit/zone tests) | Final verification | `flutter test` | Complete suite |

## Open questions
- **Low-Battery Rule Confirmation:** Please confirm the proposed state table for the low-battery rule in the Pending Decisions section.

## Ground rules
- **Calibrate communication:** Use concise, professional tone as defined.
- **Tests ship with the code:** Every code change includes a test run.
- **Code is documented as it's written:** Added logic (e.g. `battery_plus` wrapper) gets docstrings.
- **Accepted risks stay visible:** Check `risks.yml`.
- **Reporting Amendment:** Record the audit report's severity-count correction transparently as a dated amendment, do not silently rewrite the artifact.

## Definition of done
- [x] 39.1: Baseline recorded, STEP reserved, audit amended, decisions recorded.
- [x] 39.2: Architecture updated, ADRs (0009, 0010) created and scope-split, Risks reviewed, Links validated, `battery_plus` vetted, Bridge files regenerated.
- [x] 39.2.F1: Documentation Link Repair, Repository Hygiene & Dependency Constraint Finalization.
- [x] 39.2.F2: Pin `battery_plus ^7.1.1` in ADR-0010, reconcile RISK-0003 against ADR-0009, update DoD checkboxes for 39.2/39.2.F1.
- [x] 39.3: Analyzer clean (unused import fixed), app-bar discrepancies investigated and resolved based on intended architecture and workflow.
- [x] 39.4: `equipment_check_form_test.dart` crash diagnosed and fixed.
- [x] 39.5: Low-battery hybrid rule implemented per state table with `battery_plus` abstraction.
- [x] 39.6: End-to-end verification, tests passing, analyzer clean, no drift in UI layout.
      - `flutter pub get`
      - `flutter analyze`
      - every discovered test file (complete `flutter test`)
      - isolated tests for each corrected failure
      - Android debug APK build
      - `doctor.sh status`
      - `doctor.sh check`
      - duplicate STEP and ADR number scans
      - git status for every touched repository
      - verification that generated bridge files contain only expected changes
      - documentation/link validation
      - normalized bridge comparison
      - architecture header and Version Log verification
      - risk-register review
      - conditional-session applicability review
      - durable check-in report (`Code/mine-flow-docs/reports/2026-07-28-phase2-tier2-check-in-report.md`)
      - final STEP review before archival
- [x] The STEP test plan is complete.
- [x] All tests named in the STEP test plan pass at the end of this STEP.
- [x] STEP archived to `prompts/002-phase2/step-0039/`.

