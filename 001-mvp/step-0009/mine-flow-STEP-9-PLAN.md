# mine-flow — STEP-9 PLAN: Tier 3 - Reporting, Timeline & Polish

**Phase:** Phase 1 — MVP
**Owner:** Antigravity
**Status:** In progress
**Date:** 2026-07-18
**Branch:** `step-0009-reporting-timeline-polish`
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts`

> Delivers the final Tier 3 MVP capabilities: PDF report generation (attendance, cut/fill, inventory), a visual work timeline (planned vs. actual progress), and in-app notifications with persistent banners for critical items (e.g. equipment check reminders). These are the last feature STEPs before the end-to-end integration pass in STEP-10.

## Motivation

STEPs 3–8 delivered all Tier 1 (daily operations) and Tier 2 (tracking & measurement) features. Tier 3 is the final capability layer of the MVP, covering the "polish" features that turn raw data into actionable outputs:

1. **Reports / PDF export** — Supervisors currently cannot generate shareable summaries. This substep delivers PDF reports for crew attendance & overtime, cut/fill volume (weekly/monthly/YTD/PTD), and inventory tracking. Launch criterion LC-3 requires at least one PDF report type.
2. **Work timeline** — A visual planned-vs-actual progress view that gives supervisors a quick overview of site operations over time.
3. **In-app notifications** — Persistent banner notifications for critical items (equipment check reminders, low inventory). Launch criterion LC-4 requires notifications functional for at least equipment check reminders.

Without these, the MVP lacks the reporting and alerting capabilities that justify digitalization (SC-2: report compilation under 30 minutes; SC-4: fewer data discrepancies).

## Decisions already locked

- root `.throughstone/local-user.md` — read **Experience level** (Level 2 - Basic) before user-facing questions/explanations, and read **Communication style** (Explanatory) before planning discussions.
- `Code/mine-flow-docs/architecture/01-system-overview.md` — Tier 3 scope: work timeline (visual planned vs. actual progress), reports/PDF export (crew attendance & overtime, cut/fill weekly/monthly/YTD/PTD, inventory tracking), notifications (in-app only, persistent banner for critical items).
- `Code/mine-flow-docs/architecture/02-phasing-roadmap.md` — Launch criteria LC-3 (at least one PDF report), LC-4 (in-app notifications for equipment check reminders).
- `Code/mine-flow-docs/architecture/03-architecture-overview.md` & `15-native-app-architecture.md` — Clean Architecture layout (`domain`, `data`, `presentation`), BLoC/Cubit state management, repository pattern with `SyncQueueManager` offline sync.
- `Code/mine-flow-docs/architecture/04-data-model.md` — All source entities (AttendanceRecord, CutFillRecord, LandClearingRecord, InventoryItem, EquipmentCheck, DailyLog) already exist in the data layer.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — Forest & Stone palette, Inter typography, compact density, 4px radius, data-dense minimalist principle.
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md` §4 — **In-app notifications only** for MVP. No FCM/push. Alerts display when the app is actively open.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — Unit tests for repositories and BLoCs, Widget tests for UI components, integration verification for data flows.
- **Existing features used as report data sources:**
  - `lib/features/attendance/` — `AttendanceRecord` entity with `AttendanceStatus` enum (present, absent, sick, leave)
  - `lib/features/tracking/` — `CutFillRecord` entity (cutVolumeM3, fillVolumeM3, netVolumeM3, measurementDate, zoneId), `InventoryItem` entity, `LandClearingRecord` entity
  - `lib/features/equipment/` and `lib/features/equipment_check/` — `EquipmentCheck` entity
- **Hive Type IDs in use:** 1–12, 23. Next available: 13–22, 24+. **Use Type ID 13** for `NotificationModel` if Hive caching is needed, **Type ID 14** for `TimelineMilestoneModel`.
- **No existing PDF, charting, or notification packages** in `pubspec.yaml`. This STEP must add them.

## Substeps

| #   | Title                                      | Produces                                                                                                                                                                                                                                                                                                                                          | Depends on    | Open questions |
| --- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | -------------- |
| 9.1 | Reporting Domain, Data Layer & PDF Service | `lib/features/reporting/domain/` (entities: `ReportRequest`, `ReportResult`; repository interface; use cases), `lib/features/reporting/data/` (repository impl, datasources querying existing feature repos). `lib/core/services/pdf_service.dart` — PDF generation engine using `pdf` + `printing` packages. Supabase queries for aggregated data. | None          | None           |
| 9.2 | Report UI Screens & State                  | `lib/features/reporting/presentation/` — BLoC/Cubit for report generation state; Report Dashboard screen (report type selection), Report Preview/Result screen (in-app display + PDF share/download), date-range pickers, zone filters. At least 3 report types: Attendance, Cut/Fill Volume, Inventory.                                           | 9.1           | None           |
| 9.3 | Work Timeline Feature                      | `lib/features/timeline/` — Full Clean Architecture stack: domain entities (`TimelineMilestone`, `TimelineEntry`), data layer (Supabase queries aggregating dates across features), presentation (BLoC + timeline visualization screen showing planned vs. actual progress per zone).                                                                | 9.1           | None           |
| 9.4 | In-App Notification System                 | `lib/features/notifications/` — Full Clean Architecture stack: domain entities (`AppNotification`), data layer (rule-based notification generator checking equipment checks, low inventory thresholds), presentation (BLoC + notification list screen + persistent top banner widget). Integrates into app shell.                                    | 9.1, 9.2, 9.3 | None           |
| 9.5 | Integration, Polish & Test Verification    | Route wiring in `router.dart`, dashboard integration, navigation to new features, comprehensive unit + widget + integration tests for all 9.x features. `flutter test` passes clean. Final polish pass.                                                                                                                                            | 9.1–9.4       | None           |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update                                                                                             | Run timing        | Command / gate                             | Notes                                                           |
| ------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------ | --------------------------------------------------------------- |
| Unit                | 9.1, 9.5   | PDF service generation, report data aggregation, date range filtering, entity serialization                           | Final (Substep 9.5) | `flutter test test/features/reporting/`    | Cover empty data, single-record, multi-zone aggregation         |
| Unit                | 9.3, 9.5   | Timeline data aggregation, milestone ordering, date-range boundary conditions                                         | Final (Substep 9.5) | `flutter test test/features/timeline/`     | Cover no milestones, overlapping dates                          |
| Unit                | 9.4, 9.5   | Notification rule engine, threshold checks, notification deduplication, dismiss/read state                            | Final (Substep 9.5) | `flutter test test/features/notifications/` | Cover below-threshold, at-threshold, above-threshold, no data  |
| Widget / UI         | 9.2, 9.5   | Report type selection, date picker interactions, PDF preview loading states, empty/error states                        | Final (Substep 9.5) | `flutter test test/features/reporting/`    | Cover all 3 report types, loading/success/error                 |
| Widget / UI         | 9.3, 9.5   | Timeline visualization rendering, empty timeline, scroll behavior                                                     | Final (Substep 9.5) | `flutter test test/features/timeline/`     | Cover empty/populated/single-entry states                       |
| Widget / UI         | 9.4, 9.5   | Notification list rendering, banner display/dismiss, notification badge count                                         | Final (Substep 9.5) | `flutter test test/features/notifications/` | Cover zero/one/many notifications, dismiss action              |
| Integration         | 9.5        | Report generation end-to-end (mock data → PDF bytes), notification rule evaluation against real BLoC states           | Final (Substep 9.5) | `flutter test test/features/`              | Full feature integration with mocked repositories               |

## Ground rules

- **Calibrate communication from root `.throughstone/local-user.md`.**
- **CRITICAL — Extra-detailed prompts for external model execution**: This STEP will be executed by an external model (DeepSeek v4 Flash High). Every substep prompt MUST be extraordinarily explicit: specify exact file paths, exact class names, exact method signatures, exact import paths, exact widget trees, and exact test expectations. Leave ZERO ambiguity. The executing model has no memory of prior conversation and must reconstruct everything from the prompt alone.
- **Clean Architecture discipline**: Follow the established project pattern exactly: `domain/entities/`, `domain/repositories/`, `data/datasources/`, `data/models/`, `data/repositories/`, `presentation/bloc/`, `presentation/pages/`, `presentation/widgets/`. Reference existing feature implementations (e.g., `lib/features/tracking/`, `lib/features/data_bucket/`) as templates.
- **Tests ship with the code** — deferred to substep 9.5 as a dedicated final verification substep.
- **Hive Type IDs**: Use **13** for `NotificationModelAdapter`, **14** for `TimelineMilestoneModelAdapter` if needed. Do not conflict with existing IDs 1–12, 23.
- **New dependencies to add**: `pdf: ^3.11.1` and `printing: ^5.13.4` for PDF generation; `fl_chart: ^0.69.2` for timeline charts. No notification packages needed (in-app only, built with standard Flutter widgets).
- **Code is documented as it's written.**
- **Accepted risks stay visible.**
- **Indonesian (ID) locale**: All user-facing strings must be in Indonesian, consistent with the rest of the app.
- **Forest & Stone theme**: All new UI must use the existing `AppTheme` — deep forest green (`#166534`) primary, stone grays, Inter font, 4px radius, compact density.

## Definition of done

- [ ] Substep 9.1: Reporting domain & data layers implemented; PDF service generates valid PDF bytes for 3 report types.
- [ ] Substep 9.2: Report UI complete — report type selection dashboard, date/zone filters, in-app preview, PDF share/download.
- [ ] Substep 9.3: Work timeline feature complete — milestone entry, visual timeline chart (planned vs. actual), zone filtering.
- [ ] Substep 9.4: In-app notification system complete — rule-based notification generation, notification list screen, persistent banner for critical items (equipment check reminders).
- [ ] Substep 9.5: All new routes wired in `router.dart`, dashboard navigation updated, comprehensive test suite passes via `flutter test`.
- [ ] `flutter test` passes cleanly for all new feature tests.
- [ ] All new code is documented; architecture docs updated if any decisions changed.
- [ ] STEP review passed; `prompts/STEP-index.md` updated; STEP archived to `prompts/`.
