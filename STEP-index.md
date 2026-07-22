# mine-flow — STEP Index

The living roadmap. Every STEP, its status, and a one-line scope. **This is the first
place to look to understand where the project is.** Keep it current as STEPs are planned,
worked, and completed.

> Status values: **Planned** · **In progress** · **Done** (archived to `prompts/`) ·
> **Deferred** (consciously not needed now; keep a revisit trigger) ·
> **Abandoned** (reserved but won't be built — keep the row so the number is never reused).
> Flip a STEP to **In progress** when you start it, so the overlap warning can see it.
> STEP numbers are global and never reset (see `METHOD.md` §1, §8).
> **What to do next** is always derivable from this index — see the next-action resolver in
> `METHOD.md` §10.
>
> **Reserving a number (teams):** adding a STEP row _is_ reserving its number, on `prompts/`'s
> shared trunk (not a `step-NNNN` branch). Pull `prompts/`, take `max + 1`, add the row, then
> **commit and push immediately** — before branching or working. If the push is rejected, pull,
> renumber, push again. Before every push, even a clean merge, scan for duplicates
> (`grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md | grep -oE 'STEP-[0-9]+' | sort | uniq -d`)
> — two appended rows merge with no
> conflict into a silent duplicate. See `runbooks/collaboration.md`.
> **Owner** = who's on it; **Repos** = the repos it expects to touch (a _projection_ that may
> change — it powers the overlap warning, it doesn't reserve anything). Solo, leave them blank.

## Phase 1 — MVP

| STEP    | Title                                   | Owner       | Status | Repos (projection)                           | Scope (one line)                                                                                                                                                                      |
| ------- | --------------------------------------- | ----------- | ------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| STEP-1  | Architecture                            |             | Done   | `mine-flow-docs`, `prompts`                  | Architecture-first: design docs + ADRs, no code. Substeps = the sessions in `templates/architecture-sessions/`. Branch: `step-0001-architecture`.                                     |
| STEP-2  | Scaffold repos & skeleton               |             | Done   | `mine-flow-app`                              | Create the Flutter repository, Clean Architecture structure, apply license, and setup `.env.example` baseline.                                                                        |
| STEP-3  | Core Data Layer & Authentication        | Antigravity | Done   | `mine-flow-app`                              | Implement Supabase schema, RLS policies, auth, generate Dart models, and setup Hive offline caching foundation. Substeps 3.1–3.5. Branch: `step-0003-core-data-auth`.                 |
| STEP-4  | Tier 1 - Attendance & Daily Logging     | Antigravity | Done   | `mine-flow-app`                              | Build UI and offline sync logic for crew attendance and daily structured logs for field operations. Substeps 4.1–4.5. Branch: `step-0004-attendance-daily-logging`.                   |
| STEP-5  | Tier 1 - Equipment Digital Checks       | Antigravity | Done   | `mine-flow-app`                              | Implement SOP-based pre-work and post-work condition checks for GNSS, Total Station, and Drone/UAV with offline sync. Substeps 5.1–5.4. Branch: `step-0005-equipment-digital-checks`. |
| STEP-6  | Mid-Phase Check-in                      | Antigravity | Done   | `mine-flow-docs`, `prompts`                  | Run standard check-in runbook (`runbooks/check-in.md`) to reconcile drift and review risks.                                                                                           |
| STEP-7  | Tier 2 - Field Tracking & Measurement   | Antigravity | Done   | `mine-flow-app`                              | Build manual entry screens and data flow for cut/fill volume tracking, land clearing area, and inventory. Substeps 7.1–7.5. Branch: `step-0007-field-tracking-measurement`.           |
| STEP-8  | Tier 2 - Data Bucket Integration        | Antigravity | Done   | `mine-flow-app`                              | Integrate Google Drive API for uploading heavy geospatial files (.shp, .tiff) and save metadata to Supabase.                                                                          |
| STEP-9  | Tier 3 - Reporting, Timeline & Polish   | Antigravity | Done   | `mine-flow-app`                              | Add visual work timeline, PDF report generation, and in-app notifications. Substeps 9.1–9.5. Branch: `step-0009-reporting-timeline-polish`.                                           |
| STEP-10 | End-to-End Integration & Final Check-in | Antigravity | Done   | `mine-flow-app`, `mine-flow-docs`, `prompts` | Wire capabilities together to ensure launch criteria are met end-to-end, and run final check-in.                                                                                      |
| STEP-11 | Phase 1 Polish & UI Wrap-up             | DeepSeek    | Done   | `mine-flow-app`, `prompts`                   | Implement shadcn-admin collapsible sidebar shell and responsive dashboard, fix 92 analyzer warnings, and archive loose prompts.                                                       |
| STEP-12 | Complete MVP Functional Wiring & Sync   | DeepSeek    | Done   | `mine-flow-app`, `prompts`                   | Wire orphaned UI screens into router, implement missing sync registrars for tracking/attendance/logging/equipment, and clean up duplicate folders.                                    |

<!-- STEP-1 is the ONLY row at bootstrap. STEP-2 onward are the implementation STEPs — don'
     add them by hand: after STEP-1's review passes, run the planning session
     (templates/planning-session.md) and it outlines all the Phase-1 implementation STEPs
     here (a couple of sentences each), in dependency order after STEP-1. Each STEP's detailed
     PLAN and substeps are written later, when you start that STEP. Example row shape:
     | STEP-2 | Scaffold repos & skeleton | | Planned | `mine-flow-api` | … | -->

### STEP-1 substeps (architecture sessions)

> Like every STEP, STEP-1 has **one owner**, run on one machine — substeps aren't split
> across people (see `runbooks/collaboration.md` §3). But architecture is a shared
> foundation, so **decide it as a group**: the best setup is the whole team in a room walking
> the sessions together while one person drives the keyboard and commits the docs.

| Substep | Session                                      | Status | Output doc                                     |
| ------- | -------------------------------------------- | ------ | ---------------------------------------------- |
| 1.1     | System Overview, Requirements & Non-Goals    | Done   | `architecture/01-system-overview.md`           |
| 1.2     | Phasing & Roadmap                            | Done   | `architecture/02-phasing-roadmap.md`           |
| 1.3     | Architecture Overview & Component Boundaries | Done   | `architecture/03-architecture-overview.md`     |
| 1.3a    | Native App Architecture                      | Done   | `architecture/15-native-app-architecture.md`   |
| 1.4     | Data Model, Ownership & Retention            | Done   | `architecture/04-data-model.md`                |
| 1.5     | Scaling & Performance                        | Done   | `architecture/05-scaling-performance.md`       |
| 1.6     | Security & Threat Model                      | Done   | `architecture/06-security-threat-model.md`     |
| 1.6a    | Identity & Auth                              | Done   | `architecture/16-identity-auth.md`             |
| 1.6b    | Privacy, Compliance & Data Governance        | Done   | `architecture/17-privacy-compliance.md`        |
| 1.7     | UI / Design System                           | Done   | `architecture/07-ui-design-system.md`          |
| 1.8     | Infrastructure & Deployment                  | Done   | `architecture/08-infrastructure-deployment.md` |
| 1.9     | Environments                                 | Done   | `architecture/09-environments.md`              |
| 1.10    | Observability                                | Done   | `architecture/10-observability.md`             |
| 1.11    | Interface Contracts                          | Done   | `architecture/11-interface-contracts.md`       |
| 1.12    | Test Strategy                                | Done   | `architecture/12-test-strategy.md`             |
| 1.13    | Glossary                                     | Done   | `architecture/13-glossary.md`                  |
| 1.14    | Cross-Cutting Review                         | Done   | review doc                                     |

<!-- Conditional sessions: enumerate every conditional-*.md template and include/defer/skip it
     in the STEP-1 PLAN's "Conditional sessions considered" table. Add an index row only when
     one is included. Slot included conditionals under a LETTERED substep after the related
     owning session, and run them BY NAME, not number (for example, "run the identity-auth
     session" → conditional-identity-auth.md). The output doc takes the next number above the
     core set. EXAMPLE ONLY — do not parse this as a real row; real rows start at the left
     margin above this comment, with the assigned substep and doc number:
       | 1.Xa | Conditional topic | Planned | `architecture/NN-topic.md` |
     If a conditional row is later added and then consciously not needed under the current
     project shape, mark it Deferred with the revisit trigger in the PLAN/risk register. -->

### STEP-4 substeps

| Substep | Session / Title                         | Status | Output / Deliverables                                              |
| ------- | --------------------------------------- | ------ | ------------------------------------------------------------------ |
| 4.1     | Attendance Domain & Data Layer          | Done   | `lib/features/attendance/domain/`, `lib/features/attendance/data/` |
| 4.2     | Crew Attendance UI Screens & State      | Done   | `lib/features/attendance/presentation/`                            |
| 4.3     | Daily Logging Domain & Data Layer       | Done   | `lib/features/daily_log/domain/`, `lib/features/daily_log/data/`   |
| 4.4     | Daily Logging UI Screens & State        | Done   | `lib/features/daily_log/presentation/`                             |
| 4.5     | Offline Sync Integration & Verification | Done   | `test/`, `SyncQueueManager` bindings                               |

### STEP-5 substeps

| Substep | Session / Title                         | Status | Output / Deliverables                                            |
| ------- | --------------------------------------- | ------ | ---------------------------------------------------------------- |
| 5.1     | Equipment Checks Domain & Data Layer    | Done   | `lib/features/equipment/domain/`, `lib/features/equipment/data/` |
| 5.2     | SOP Inspection UI & Form Screens        | Done   | `lib/features/equipment/presentation/`                           |
| 5.3     | Inspection History & Summary Screen     | Done   | `lib/features/equipment/presentation/`                           |
| 5.4     | Offline Sync Integration & Verification | Done   | `test/`, `SyncQueueManager` bindings                             |

### STEP-6 substeps

| Substep | Session / Title                                 | Status | Output / Deliverables                                                     |
| ------- | ----------------------------------------------- | ------ | ------------------------------------------------------------------------- |
| 6.1     | Doc-drift Reconciliation & Conditional Coverage | Done   | `reports/2026-07-18-step-0006-check-in-report.md`, doc fixes, risk review |
| 6.2     | Full Test Run & Verification                    | Done   | Test execution results (`flutter test`)                                   |

### STEP-7 substeps

| Substep | Session / Title                         | Status | Output / Deliverables                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------- | --------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7.1     | Field Tracking Domain & Data Layer      | Done   | `lib/features/tracking/domain/`, `lib/features/tracking/data/`                                                                                                                                                                                                                                                                                                                                                                     |
| 7.2     | Cut/Fill Volume Tracking UI & State     | Done   | `lib/features/tracking/presentation/bloc/`, `lib/features/tracking/presentation/pages/`, `lib/features/tracking/presentation/widgets/`                                                                                                                                                                                                                                                                                             |
| 7.3     | Land Clearing Area Tracking UI & State  | Done   | `lib/features/tracking/presentation/bloc/land_clearing/`, `lib/features/tracking/presentation/pages/land_clearing_*`, `lib/features/tracking/presentation/widgets/`                                                                                                                                                                                                                                                                |
| 7.4     | Inventory Tracking UI & State           | Done   | `lib/features/tracking/presentation/bloc/inventory/`, `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`, `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`, `lib/features/tracking/presentation/pages/stock_adjustment_dialog.dart`, `lib/features/tracking/presentation/widgets/inventory_card.dart`, `lib/features/tracking/presentation/widgets/inventory_summary_card.dart` |
| 7.5     | Offline Sync Integration & Verification | Done   | `test/features/tracking/`, `lib/features/tracking/data/sync/tracking_sync_registrar.dart`, `SyncQueueManager` bindings, 77 tests passing                                                                                                                                                                                                                                                                                           |

### STEP-8 substeps

| Substep | Session / Title                   | Status | Output / Deliverables                                                                                                                                                                             |
| ------- | --------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 8.1     | Data Bucket Domain & Data Layer   | Done   | `lib/features/data_bucket/domain/`, `lib/features/data_bucket/data/` (GeospatialFile entity, models, datasources, repository impl, Hive adapters, Supabase migration)                             |
| 8.2     | Google Drive Integration Service  | Done   | `lib/core/network/google_drive_service.dart`, `test/core/network/google_drive_service_test.dart` — Drive API client with service account auth, upload with progress, lookup, graceful degradation |
| 8.3     | Data Bucket UI Screens & State    | Done   | `lib/features/data_bucket/presentation/bloc/`, `lib/features/data_bucket/presentation/pages/`, `lib/features/data_bucket/presentation/widgets/` (list, upload, detail screens)                    |
| 8.4     | Offline Queue & Test Verification | Done   | `test/features/data_bucket/`, `lib/features/data_bucket/data/sync/data_bucket_sync_registrar.dart`, `SyncQueueManager` bindings                                                                   |

### STEP-9 substeps

| Substep | Session / Title                            | Status | Output / Deliverables                                                                                       |
| ------- | ------------------------------------------ | ------ | ----------------------------------------------------------------------------------------------------------- |
| 9.1     | Reporting Domain, Data Layer & PDF Service | Done   | `lib/features/reporting/domain/`, `lib/features/reporting/data/`, `lib/core/services/pdf_service.dart`      |
| 9.2     | Report UI Screens & State                  | Done   | `lib/features/reporting/presentation/` — BLoC/Cubit, Report Dashboard, Report Preview/Result, date filters  |
| 9.3     | Work Timeline Feature                      | Done   | `lib/features/timeline/` — Full Clean Architecture stack, timeline visualization                            |
| 9.4     | In-App Notification System                 | Done   | `lib/features/notifications/` — Full Clean Architecture stack, notification list screen, persistent banner  |
| 9.5     | Integration, Polish & Test Verification    | Done   | Route wiring, dashboard integration, comprehensive unit + widget + integration tests, `flutter test` passes |

### STEP-11 substeps

| Substep | Session / Title                     | Status | Output / Deliverables                                                              |
| ------- | ----------------------------------- | ------ | ---------------------------------------------------------------------------------- |
| 11.1    | Responsive UI Shell & Navigation    | Done   | `lib/app/router.dart`, new `lib/app/presentation/` shell, dark/light toggle action |
| 11.2    | Card-based Dashboard Stats          | Done   | Updated dashboard placeholder with stat summary cards (shadcn-admin style)         |
| 11.3    | Code Quality Polish (Lint Fixes)    | Done   | Global fix for 92 analyzer warnings (prefer_const_constructors, etc.)              |
| 11.4    | Workspace Hygiene (Archive Prompts) | Done   | Unarchived STEP-7, 8, 9 files moved into `prompts/001-mvp/step-NNNN/`              |
| 11.5    | Notification Rules Implementation   | Done   | Fully implemented rules 2-4 in `NotificationRuleEngine` connected to repos         |

## Phase 2 — Impeccable UI Rebuild

| STEP    | Title                                               | Owner       | Status | Repos (projection)                | Scope (one line)                                                                                                                                                                          |
| ------- | --------------------------------------------------- | ----------- | ------ | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| STEP-13 | Phase 2 UI pass - LoginPage                         | Gemini      | Done   | `mine-flow-app`                   | Impeccable-driven styling and markup rebuild of LoginPage matching shadcn-admin conventions. Branch: `step-0013-phase2-loginpage`.                                                        |
| STEP-14 | Phase 2 UI pass - DashboardPage                     | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for DashboardPage. Substeps: 14.1 craft, 14.2 polish, 14.3 audit. Branch: `step-0014-phase2-dashboardpage`.                         |
| STEP-15 | Phase 2 UI pass - AttendanceScreen                  | Antigravity | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for AttendanceScreen. Substeps: 15.1 craft, 15.2 polish, 15.3 audit. Branch: `step-0015-phase2-attendancescreen`.                   |
| STEP-16 | Phase 2 UI pass - DailyLogListScreen                | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for DailyLogListScreen. Substeps: 16.1 craft, 16.2 polish, 16.3 audit. Branch: `step-0016-phase2-dailyloglistscreen`.               |
| STEP-17 | Phase 2 UI pass - CutFillListScreen                 | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for CutFillListScreen. Substeps: 17.1 craft, 17.2 polish, 17.3 audit. Branch: `step-0017-phase2-cutfilllistscreen`.                 |
| STEP-18 | Phase 2 UI pass - LandClearingSummaryScreen         | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for LandClearingSummaryScreen. Substeps: 18.1 craft, 18.2 polish, 18.3 audit. Branch: `step-0018-phase2-landclearingsummaryscreen`. |
| STEP-19 | Phase 2 UI pass - InventoryDashboardScreen          | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for InventoryDashboardScreen. Substeps: 19.1 craft, 19.2 polish, 19.3 audit. Branch: `step-0019-phase2-inventorydashboardscreen`.   |
| STEP-20 | Phase 2 UI pass - EquipmentHistoryScreen            | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for EquipmentHistoryScreen. Substeps: 20.1 craft, 20.2 polish, 20.3 audit. Branch: `step-0020-phase2-equipmenthistoryscreen`.       |
| STEP-21 | Phase 2 UI pass - TimelinePage                      | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for TimelinePage. Substeps: 21.1 craft, 21.2 polish, 21.3 audit. Branch: `step-0021-phase2-timelinepage`.                           |
| STEP-22 | Phase 2 UI pass - DataBucketListPage                | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for DataBucketListPage. Substeps: 22.1 craft, 22.2 polish, 22.3 audit. Branch: `step-0022-phase2-databucketlistpage`.               |
| STEP-23 | Phase 2 UI pass - UploadFilePage                    | Antigravity | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for UploadFilePage. Substeps: 23.1 craft, 23.2 polish, 23.3 audit. Branch: `step-0023-phase2-uploadfilepage`.                       |
| STEP-24 | Phase 2 UI pass - FileDetailPage                    | DeepSeek    | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for FileDetailPage. Substeps: 24.1 craft, 24.2 polish, 24.3 audit. Branch: `step-0024-phase2-filedetailpage`.                       |
| STEP-25 | Phase 2 UI pass - ReportDashboardPage               | DeepSeek    | Done   | `mine-flow-app`, `prompts`        | Phase 2 styling, markup, and shadcn-admin conventions for ReportDashboardPage. Substeps: 25.1 craft, 25.2 polish, 25.3 audit. Branch: `step-0025-phase2-reportdashboardpage`.             |
| STEP-26 | Phase 2 UI pass - ReportConfigPage                  | Antigravity | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for ReportConfigPage. Substeps: 26.1 craft, 26.2 polish, 26.3 audit. Branch: `step-0026-phase2-reportconfigpage`.                   |
| STEP-27 | Phase 2 UI pass - NotificationListPage              |             | Done   | `mine-flow-app`                   | Phase 2 styling, markup, and shadcn-admin conventions for NotificationListPage. Substeps: 27.1 craft, 27.2 polish, 27.3 audit. Branch: `step-0027-phase2-notificationlistpage`.           |
| STEP-28 | Phase 2 Tier 1 Check-in, Audit & Bug Fixes          |             | Done   | `mine-flow-app`, `mine-flow-docs` | Final cross-screen consistency audit of all 15 rebuilt screens, standard check-in (reconcile docs, test suite). Bug Fixes (28.3) deferred to STEP-30+ (ForUI rebuild).                    |
| STEP-29 | Impeccable/Throughstone Bridge & Doc Reconciliation | Antigravity | Done   | `mine-flow-docs`, `mine-flow-app` | Impeccable/Throughstone Bridge & Doc Reconciliation.                                                                                                                                      |

### STEP-20 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                                                                                            |
| ------- | ---------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 20.1    | Craft (Markup & layout foundation) | Done   | `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart` — Phase 2 shadcn-admin styling, CustomScrollView layout, responsive filter chips, search bar, FAB, animated loading/error states |
| 20.2    | Polish (Animations & Details)      | Done   | `lib/features/equipment_check/presentation/widgets/equipment_check_card.dart` — Micro-interactions, standard status color token usage, expanded SOP state styling.                                               |
| 20.3    | Audit (Cross-check & Consistency)  | Done   | Antigravity verified: Code accurately reflects `shadcn-admin` token usage, Git branches synced, all layout constraints handle breakpoints cleanly.                                                               |

### STEP-19 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                    |
| ------- | ---------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 19.1    | Craft (Markup & layout foundation) | Done   | `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart` — Phase 2 shadcn-admin styling, markup and layout foundation. |
| 19.2    | Polish (Animations & Details)      | Done   | `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart` — Spacing, typography, micro-interactions applied.            |
| 19.3    | Audit (Cross-check & Consistency)  | Done   | Antigravity verified: Code accurately reflects `shadcn-admin` token usage, accessibility, and responsive checks.                         |

### STEP-21 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                                              |
| ------- | ---------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 21.1    | Craft (Markup & layout foundation) | Done   | `lib/features/timeline/presentation/pages/timeline_page.dart` — Phase 2 shadcn-admin styling, CustomScrollView layout.                                             |
| 21.2    | Polish (Animations & Details)      | Done   | `lib/features/timeline/presentation/widgets/timeline_chart.dart`, `milestone_card.dart` — Micro-interactions, standard status color token usage, updated tooltips. |
| 21.3    | Audit (Cross-check & Consistency)  | Done   | Antigravity verified: Code accurately reflects `shadcn-admin` token usage, Git branches synced, all layout constraints handle breakpoints cleanly.                 |

### STEP-22 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                                                                                                                                          |
| ------- | ---------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 22.1    | Craft (Markup & layout foundation) | Done   | `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart` — Phase 2 shadcn-admin styling, CustomScrollView layout, SliverAppBar, polished empty/error states.                                                                                   |
| 22.2    | Polish (Animations & Details)      | Done   | `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart` — `easeOutQuart` curves per DESIGN.md, staggered slide+fade card entrance, refined file count label typography and spacing, `TickerProviderStateMixin` for multiple anim controllers. |
| 22.3    | Audit (Cross-check & Consistency)  | Done   | Verified against DESIGN.md: `easeOutQuart` curves, staggered slide+fade entrance, spacing scale (4,8,12,16,20,24,32), theme tokens (no raw colors), shadcn-admin style, analyzer passes with zero issues. Git branch synced.                                   |

### STEP-23 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                                                                                         |
| ------- | ---------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 23.1    | Craft (Markup & layout foundation) | Done   | `lib/features/data_bucket/presentation/pages/upload_file_page.dart` — Phase 2 shadcn-admin styling, layout adjustments, spacing, and border radius usage.                                                     |
| 23.2    | Polish (Animations & Details)      | Done   | `lib/features/data_bucket/presentation/pages/upload_file_page.dart` — `AnimatedCrossFade` with `easeOutQuart` curves for file picker transitions, semantic labels, micro-interactions for file removal.       |
| 23.3    | Audit (Cross-check & Consistency)  | Done   | Verified against DESIGN.md: `easeOutQuart` curves, spacing scale, theme tokens (no raw colors), shadcn-admin style, analyzer passes with zero issues (fixed deprecated `value` parameter). Git branch synced. |

### STEP-26 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------- | ---------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 26.1    | Craft (Markup & layout foundation) | Done   | `lib/features/reporting/presentation/pages/report_config_page.dart` — Phase 2 shadcn-admin styling, DESIGN.md spacing scale, theme tokens, Semantics, 1px border card surfaces, card-based sections (report type header, date range, zone filter), error banner, action buttons.                                                                                                                                                                                                                                                                     |
| 26.2    | Polish (Animations & Details)      | Done   | `lib/features/reporting/presentation/pages/report_config_page.dart` — staggered entrance animations with `easeOutQuart` curves per DESIGN.md §33, `SingleTickerProviderStateMixin`, `BlocListener` replay for success view transition, raw `_kBrandPrimary`/`_kAccent` replaced with theme `colorScheme` tokens (primaryContainer, primary), refined spacing using DESIGN.md scale, analyzer passes with zero issues.                                                                                                                                |
| 26.3    | Audit (a11y & Responsive)          | Done   | `lib/features/reporting/presentation/pages/report_config_page.dart` — verified a11y: semantic headers, labels, button roles, `excludeSemantics` on decorative elements, `container` on error banner. Fixed: raw `TextStyle(error message)` replaced with theme `bodySmall`, raw `TextStyle(Buat Laporan)` replaced with theme `labelLarge`, `CircularProgressIndicator` now uses `colorScheme.onPrimary`. Responsive: success view action buttons now constrained to `maxWidth: 480` matching config form pattern. Analyzer passes with zero issues. |

### STEP-27 substeps

| Substep | Session / Title                                  | Status | Output / Deliverables                                                                                                                                                                                                                                                                                        |
| ------- | ------------------------------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 27.1    | Craft (Markup & layout foundation)               | Done   | `lib/features/notifications/presentation/pages/notification_list_page.dart` — Phase 2 shadcn-admin styling, DESIGN.md spacing scale, theme tokens, Semantics, 1px border card surfaces with severity accent, icon containers, error/empty states.                                                            |
| 27.2    | Polish (Spacing, typography, micro-interactions) | Done   | `lib/features/notifications/presentation/pages/notification_list_page.dart` — Staggered card entrance animations with `easeOutQuart` curves per DESIGN.md §33, `SingleTickerProviderStateMixin`, `FadeTransition` + `SlideTransition` per card, refined spacing constants, analyzer passes with zero issues. |
| 27.3    | Audit (a11y & Responsive)                        | Done   | `lib/features/notifications/presentation/pages/notification_list_page.dart` — Merged card semantics with `excludeSemantics` for clean screen-reader utterances, `enabled: true` on dismiss-all button, responsive `ConstrainedBox(maxWidth: 720)` for desktop layout, analyzer passes with zero issues.      |

### STEP-25 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                                                                                                                                               |
| ------- | ---------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 25.1    | Craft (Markup & layout foundation) | Done   | `lib/features/reporting/presentation/pages/report_dashboard_page.dart`, `lib/features/reporting/presentation/widgets/report_type_card.dart` — Phase 2 shadcn-admin styling, DESIGN.md spacing scale, theme tokens, Semantics, responsive grid, 1px border surfaces. |
| 25.2    | Polish (Animations & Details)      | Done   | `lib/features/reporting/presentation/widgets/report_type_card.dart`, `report_dashboard_page.dart` — micro-interactions with `easeOutQuart`, hover/focus states, brand colors, keyboard accessibility (Enter/Space), refined spacing.                                |
| 25.3    | Audit (Cross-check & Consistency)  | Done   | Antigravity verified: Code accurately reflects `shadcn-admin` token usage, accessibility, analyzer passes with zero issues. Git branch synced.                                                                                                                      |

### STEP-24 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                                                   |
| ------- | ---------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 24.1    | Craft (Markup & layout foundation) | Done   | `lib/features/data_bucket/presentation/pages/file_detail_page.dart` — Phase 2 shadcn-admin styling, layout adjustments, responsive details row, and semantic labelling. |
| 24.2    | Polish (Animations & Details)      | Done   | `lib/features/data_bucket/presentation/pages/file_detail_page.dart` — Custom transition intervals, micro-interactions applied with robust Theme colour usage.           |
| 24.3    | Audit (Cross-check & Consistency)  | Done   | Verified against DESIGN.md: theme tokens (no raw colors), layout breakpoints, analyzer passes with zero issues. Git branch synced.                                      |

### STEP-28 substeps

| Substep | Session / Title                  | Status   | Output / Deliverables                                                                              |
| ------- | -------------------------------- | -------- | -------------------------------------------------------------------------------------------------- |
| 28.1    | Audit 15 Phase 2 screens         | Done     | `mine-flow-STEP-28.1-AUDIT.md` (identified bugs and inconsistencies)                               |
| 28.2    | Check-in (Doc reconcile & tests) | Done     | `reports/2026-07-21-step-0028-check-in-report.md`, ADR-0007                                        |
| 28.3    | Bug Fixes                        | Deferred | Deferred to STEP-30+ (ForUI rebuild)                                                               |
| 28.4    | Token Standardization            | Done     | Standardization of colors (Forest & Stone), typography, and spacing across the presentation layer. |

### STEP-29 substeps

| Substep | Session / Title                      | Status | Output / Deliverables                                                  |
| ------- | ------------------------------------ | ------ | ---------------------------------------------------------------------- |
| 29.1    | Update Architecture 07-doc to v0.2.0 | Done   | `architecture/07-ui-design-system.md` updated to v0.2.0                |
| 29.2    | ADR-0008 & METHOD.md Amendment       | Done   | `adr/ADR-0008-impeccable-bridge.md`, `METHOD.md`, risk register update |
| 29.3    | Impeccable Bridge Script             | Done   | `scripts/impeccable-bridge.ps1`                                        |

### Phase 2 Tier 2 (ForUI Migration & Feature Regrouping)

| STEP    | Title                                      | Owner       | Status      | Repos (projection) | Scope (one line)                                                                                                                                            |
| ------- | ------------------------------------------ | ----------- | ----------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| STEP-30 | Phase 2 Tier 2 - ForUI Migration           | Antigravity | Done        | `mine-flow-app`    | Swap all 15 Tier 1 screens from hand-rolled Material ThemeData to forui/FTheme/FThemes.zinc, per architecture/07-ui-design-system.md v0.2.0.                |
| STEP-31 | Navigation Shell & Profile Regrouping      |             | Planned     | `mine-flow-app`    | Implement collapsible sectioned sidebar (desktop) / group tiles (mobile), add appbar profile card, move theme toggle to appbar, and regroup all features.   |
| STEP-32 | Shared Creatable Combobox & Zone State     |             | Planned     | `mine-flow-app`    | Build shared `CreatableCombobox` widget for dynamically adding non-existent options and wire up a shared local database box (e.g., for Zones).              |
| STEP-33 | Forms Refactor & Data Model Polish         |             | Planned     | `mine-flow-app`    | Update Cut/Fill (BCM/LCM cols, Material Type), Land Clearing (method combobox, plan/actual cols), Daily Log (zone combobox), Inventory (item auto-predict). |
| STEP-34 | Reporting Integration & Data Bucket Tweaks |             | Planned     | `mine-flow-app`    | Integrate Laporan buttons directly into respective feature screens (removing central menu) and remove lat/lon fields from Data Bucket form and table.       |
| STEP-35 | Settings Page Feature                      |             | Planned     | `mine-flow-app`    | Implement comprehensive Settings page including language, profile, theme configuration, logout, and support contact routing.                                |
| STEP-36 | Benchmark Database Feature                 |             | Planned     | `mine-flow-app`    | Scaffold domain, data, and presentation layers for the new Benchmark Database feature under Operations.                                                     |

### STEP-30 substeps

| Substep | Session / Title                             | Status | Output / Deliverables                                                                                                                       |
| ------- | ------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 30.1    | Core Shell & Auth                           | Done   | `pubspec.yaml`, `lib/app/app.dart`, `lib/app/presentation/`, `LoginPage`, `DashboardPage`                                                   |
| 30.2    | Operations & Tracking                       | Done   | `CutFillListScreen`, `LandClearingSummaryScreen`, `InventoryDashboardScreen`                                                                |
| 30.3    | Teams & Field Docs                          | Done   | `AttendanceScreen`, `DailyLogListScreen`, `EquipmentHistoryScreen`                                                                          |
| 30.4    | Reports, Data Bucket & Notifications        | Done   | `TimelinePage`, `ReportDashboardPage`, `ReportConfigPage`, `DataBucketListPage`, `UploadFilePage`, `FileDetailPage`, `NotificationListPage` |
| 30.5    | Analyzer Clean-up                           | Done   | 0 analyzer issues globally                                                                                                                  |
| 30.6    | Final Cross-Screen Material Purge & CI Gate | Done   | Material purge complete; 273/281 tests pass (8 pre-existing failures in tracking feature files from STEP-30.2 ForUI API mismatches)         |

## How to add a STEP

See `prompts/README.md` for the authoring recipe.
