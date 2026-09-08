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

| STEP    | Title                                      | Owner               | Status | Repos (projection) | Scope (one line)                                                                                                                                                                                                                |
| ------- | ------------------------------------------ | ------------------- | ------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| STEP-30 | Phase 2 Tier 2 - ForUI Migration           | Antigravity         | Done   | `mine-flow-app`    | Swap all 15 Tier 1 screens from hand-rolled Material ThemeData to forui/FTheme/FThemes.zinc, per architecture/07-ui-design-system.md v0.2.0.                                                                                    |
| STEP-31 | Navigation Shell & Profile Regrouping      | Antigravity         | Done   | `mine-flow-app`    | Implement collapsible sectioned sidebar (desktop) / group tiles (mobile), add appbar profile card, move theme toggle to appbar, and regroup all features.                                                                       |
| STEP-32 | Shared Creatable Combobox & Zone State     | Antigravity         | Done   | `mine-flow-app`    | Build shared `CreatableCombobox` widget for dynamically adding non-existent options and wire up a shared local database box (e.g., for Zones).                                                                                  |
| STEP-33 | Forms Refactor & Data Model Polish         | DeepSeek            | Done   | `mine-flow-app`    | Update Cut/Fill (BCM/LCM cols, Material Type), Land Clearing (method combobox, plan/actual cols), Daily Log (zone combobox), Inventory (item auto-predict).                                                                     |
| STEP-34 | Reporting Integration & Data Bucket Tweaks | Antigravity         | Done   | `mine-flow-app`    | Integrate Laporan buttons directly into respective feature screens (removing central menu) and remove lat/lon fields from Data Bucket form and table.                                                                           |
| STEP-35 | Settings Page Feature                      |                     | Done   | `mine-flow-app`    | Implement comprehensive Settings page including language, profile, theme configuration, logout, and support contact routing.                                                                                                    |
| STEP-36 | Benchmark Database Feature                 | DeepSeek            | Done   | `mine-flow-app`    | Scaffold domain, data, and presentation layers for the new Benchmark Database feature under Operations.                                                                                                                         |
| STEP-37 | Residual Impeccable Material Purge         | Gemini              | Done   | `mine-flow-app`    | Replace remaining `Card`, `ElevatedButton`, `TextButton`, `MaterialBanner` with ForUI equivalents in Equipment, Timeline, Notifications, and Data Bucket features.                                                              |
| STEP-38 | Phase 2 Tier 2 UI/UX Bug Fixes             | Gemini 3.1 Pro High | Done   | `mine-flow-app`    | Fix 19 UI/UX bugs: FButton appbar consistency, Cut/Fill form labels/layout, Land Clearing tabs, Inventory merged field, Language config, Attendance form extraction, Breadcrumbs, Benchmark nav, Equipment Check mobile layout. |
| STEP-39 | Phase 2 Tier 2 Check-in, Reconciliation & Regression Fixes | Antigravity | Done | `mine-flow-docs`, `mine-flow-app`, `prompts` | Formal check-in, tests, UI drift ADRs, and missing low-battery sync logic implementation. |
| STEP-40 | Phase 2 Tier 2 Check-in Test Suite Bug Fixes | Antigravity | Done | `mine-flow-app` | Fix 8 test failures (7 from STEP-39 check-in + 1 new smoke-test regression): FTheme wrapper gaps, AttendanceScreen FormPage migration, and SyncQueueManager retry timing race. |

## Phase 3 — Release Readiness, Integration & Scale

> Phase 3 opens with the release-readiness baseline. Multi-site support, automated imports,
> full offline expansion, and analytics remain deliberately unplanned until staging and
> release-readiness evidence proves the current single-site baseline.

| STEP    | Title                                             | Owner | Status  | Repos (projection)                  | Scope (one line) |
| ------- | ------------------------------------------------- | ----- | ------- | ----------------------------------- | ---------------- |
| STEP-41 | Release-Readiness Reconciliation & Contract Baseline | Antigravity | Done | `mine-flow-app`, `mine-flow-docs`   | Inventory the actual release gaps against the architecture and Phase 2 record; make Supabase generated-type regeneration/compile checks and Indonesian localization checks reproducible. Establish the implementation/test evidence required by the later staging and release-control STEPs without changing release architecture. |
| STEP-42 | Staging Environment & Promotion Pipeline          | Gemini 3.1 Pro High | Done | `mine-flow-app`, `mine-flow-docs`   | Provision and document a separate high-parity staging Supabase/configuration path with synthetic seed data, CI deployment, and explicit rollback/release procedures. Branch: `step-0042-staging-pipeline`. |
| STEP-43 | Flutter 3.47 Upgrade & Dependency Overhaul        | Antigravity (Claude Sonnet 4.6 Thinking) | Done | `mine-flow-app`, `mine-flow-docs`, `prompts` | Upgrade Flutter SDK to 3.47.0 / Dart 3.13 in CI; fix broken `flutter_bloc ^9.1.1` constraint; upgrade all outdated packages; migrate Hive → hive_ce; fix Android build chain (AGP 9.1.0, KGP 2.4.0); update risks register. Resolves the broken Android CI build. |
| STEP-44 | Security, Privacy & Release-Control Baseline      | Antigravity (Claude Sonnet 4.6 Thinking) | Done | `mine-flow-docs`   | Verify and remediate the pre-release security and privacy controls: RLS/authorization behavior, account lifecycle, privacy notice and retention handling, secrets posture, backups, and a restore fire-drill record. Add appropriate authorization, migration/data, and operational evidence without treating legal review as completed. |
| STEP-45 | Release-Candidate E2E & Runtime Design Review     | Antigravity | Done | `mine-flow-app`, `mine-flow-docs`, `prompts`   | Execute critical Android and web journeys against staging, including field-critical offline/sync behavior, and capture the required runtime Impeccable design-review evidence for responsive, accessible, localized UI states. **STEP-48 delivered the executable journey evidence and branch-head gate; the STEP-45 substep table below records the remaining explicit deferrals:** Drive behavior (D2), crew RLS/cross-role isolation, true browser cold-start deep links, valid screenshot-backed design-review artifacts, and screen-reader evidence. |
| STEP-46 | Comprehensive UI/UX Audit — All Current Screens   | Hermes (Claude Opus 5 Thinking) | Done | `mine-flow-app`, `prompts`, `mine-flow-docs` | Two-pass audit (code-level static scan + screenshot visual review) of all 24 current screens against DESIGN.md and overview.md capabilities; strong-model confirmation; remediation of all 97 confirmed findings. ADR-0012..0016; 6 needs-runtime items feed STEP-45. Branch `step-0046-ui-ux-audit` merged to master. |
| STEP-47 | Android Build Chain Remediation (AGP 9 / local device builds) | Gemini 3.7 Flash High (47.0, 47.8) · Gemini 3.1 Pro High (47.1–47.6) · Hermes/Claude Opus 4.8 (47.7 escalation, 47.9) | Done | `mine-flow-app`, `mine-flow-docs`, `prompts` | Restore a working local Android build so device E2E can run at all. **Actual root cause** (planning corrected the reservation outline's disproven "flutter extension not populated" theory): AGP 9 rejects the unconditional `apply plugin: 'kotlin-android'` in `package_info_plus` 9.0.1 and `file_picker` 11.0.3, aborting script evaluation before their `android { }` block — the `compileSdk not specified` error is a knock-on, and `android.builtInKotlin=false` only moves the failure to `:app:compileDebugJavaWithJavac`. Fixed forward by upgrading to AGP-9-native plugins. **Delivered:** `flutter build apk --debug` exits 0 locally (95.5s clean, APK 194 MB) and in CI `build-android`; `dependency_overrides` **eliminated** (STEP-43's `flutter_secure_storage_windows` 4.0.0 pin deleted, unblocking `win32` 6.4.0) plus a 9-major sweep (`file_picker` 12, `package_info_plus` 10, `flutter_bloc` 9, `bloc_test` 10, `go_router` 18, `googleapis` 17, `googleapis_auth` 2, `proj4dart` 3, `flutter_lints` 6) with `flutter pub outdated` reporting all direct/dev dependencies up to date; STEP-43's Windows Kotlin-daemon workaround removed as obsolete; `flutter analyze` 0 issues, format clean, `flutter test` **448 passing**, `flutter build web --release` OK; ADR-0018; RISK-0006/0008 amended, RISK-0020 raised. CI run [`33195382106`](https://github.com/lvinist/mine-flow-app/actions/runs/33195382106) on the final commit `e3cd9ed3`: `test`, `build-android`, `e2e-web`, `e2e-android` all **success**. **CI E2E green proves the harness executes** — the debug APK builds under AGP 9, the emulator boots, the app installs, and `integration_test` reports honestly; both E2E jobs target `app_boots_test.dart` only and it **self-skips** (`0 tests passed, 1 skipped` — `Unverified: Staging credentials absent`) because `TEST_USER_EMAIL`/`TEST_USER_PASSWORD` are not configured. **No journey, and not even app boot, is runtime-verified: the 14 staging journeys authored in STEP-45 remain Deferred to STEP-48.** |
| STEP-48 | Runtime Evidence — resolve STEP-45's carried-forward findings | User | Done | `mine-flow-app`, `mine-flow-docs`, `prompts` | Runtime evidence and remediation completed. Branch-head CI [run 34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645) on `d53fb7e` passed all four required jobs: `test` 548 passed/5 guard-fixture skips/0 failed, Android 24 passed/2 named skips/0 failed with 24 executed, and web 16/16 files green with 22 executed markers and 3 named skips. Delivered: staging schema/fixture alignment, journey and persistence repairs, offline/LWW verification, execution-proof guards, registry/doc truth repairs, and local gates (`flutter analyze` clean; `flutter test` 553/553 after isolated Hive-flake diagnosis). Not delivered: Drive behavior (D2), crew RLS/cross-role isolation, true browser cold-start deep links, valid screenshot-backed design-review artifacts, screen-reader evidence, and PDF operational regression; residuals remain explicitly tracked. |
| STEP-49 | Throughstone Template Hardening (process feedback) | Gemini 3.7 Flash High (49.0, 49.4) · Gemini 3.1 Pro High (49.1–49.3) · Hermes/Claude Opus 4.8 (49.5 close only) | In progress | Throughstone template repo (upstream `github.com/mherschberg/Throughstone`, clone at `D:\AppDev\Throughstone` outside the workspace) · `prompts` | Feed this project's failure modes back into the scaffold: a mechanical Unverified-vs-Done honesty gate at STEP close, phantom-close detection against disk, a credential/host-toolchain pre-flight substep for runtime STEPs, guidance against accumulating a multi-repo uncommitted close, and the dirty-index/trunk-reservation recovery recipe. Changes reach upstream via fork + PR (user decision 2026-09-09); mine-flow's local scaffold copies are **not** edited — adoption happens later via `UPDATING-THROUGHSTONE.md` manual mode. No mine-flow application code. PLAN authored 2026-09-09 (`Upcoming Prompts/mine-flow-STEP-49-PLAN.md`). |
| STEP-50 | Phase 3 Check-in (post-STEP-47 dependency overhaul) | Hermes (Claude Opus 4.8) | Done | `mine-flow-docs`, `prompts` | Run `runbooks/check-in.md` at the STEP-47 breakpoint, ~10 STEPs after the STEP-39/40 check-in: mechanical `scripts/check.sh` pass, doc-drift reconciliation in both directions across the architecture docs, conditional-session coverage re-evaluation, repo-README / interface-contract / docstring sweep, `registries/risks.yml` review (RISK-0001..0020), the S0/S1/S2 security-review gate, and the full `flutter test` suite. Review-and-verification only — no application code. Sequenced before STEP-48 so its runtime-evidence work starts from reconciled docs. **Closed 2026-09-08 (50.1 + 50.2):** check.sh 0 failures; 6 doc-drift fixes with Version-Log bumps (Doc 11 v0.3.0 + ADR-0019 TS contract of record, Doc 08 v0.2.1, Doc 13 v0.1.1, Doc 15 v0.2.1, repos.yml posture, app README — app commit pair `f693328`+`b9bcce5`); risk register reviewed (RISK-0022 close flipped, RISK-0007/0009 trigger annotations, RISK-0024 raised); conditional coverage 3/3 Included; security gate → **STEP-52** (S0 re-check, invalidated baseline) + **STEP-53** (dependency maintenance) reserved; full `flutter test` **553/553** at branch head `b9bcce5` (known Hive flake silent); workspace-root hygiene executed (~130 debris files removed, cited evidence retained). Report: `Code/mine-flow-docs/reports/2026-09-08-step-0050-check-in-report.md` + `reports/test-results/2026-09-08-step-0050-full-suite-test-results.md`. Next check-in ~STEP-60–70. |
| STEP-51 | UI Debt Closure — CF-087 Material remainder & STEP-46.4 regression coverage | | Planned | `mine-flow-app`, `mine-flow-docs`, `prompts` | Close the UI debt the 2026-09-05 implementation audit proved STEP-46 booked as complete (`Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` §F-2/§F-3). **CF-087 is ~half done:** dialogs, buttons, tiles, dividers, chips and `Icons.` are genuinely at zero, but ~116 Material call sites remain across ~30 files — `SnackBar(` 35, `Scaffold(` 37, `CircularProgressIndicator(` 25, `AppBar(` 19 — with 73 of 240 `lib/` files still importing `flutter/material.dart`, while forui 0.26 ships every equivalent (`FToast`/`FToaster`, `FScaffold`, `FCircularProgress`, `FHeader`). Re-scope the CF-087 register entry honestly first, then sweep per feature with widget tests wherever behaviour changes (dialogs, toasts, selects). **STEP-46.4's test debt:** the register assigned an explicit test tier to 84 of 97 findings (80 "Widget test"), yet the merge `040def9` added 8 net cases and zero new test files, only 13 of 97 CF ids are cited under `test/`, and the prompt's `// TODO(STEP-46.4)` escape hatch was used zero times — add the missing regression coverage or record a per-finding reason. Also carries CF-043's structural half (constrain `method` to the enumerated set; one shared control instead of the two independent Plan/Actual comboboxes) and a disposition for the 5 remaining unreferenced `lib/` files. Depends on STEP-48 closing. |
| STEP-52 | Security Baseline re-check (post-STEP-48) | | Planned | `mine-flow-app`, `mine-flow-docs`, `prompts` | S0 Security Baseline re-run from `runbooks/security-review.md` + S0 checklist. Reserved at STEP-50.1 because the 2026-08-26 baseline (run 5536191, STEP-44) is invalidated per its own cadence rule by later major CI changes: STEP-45 added the dual-platform E2E gate (new secrets, chromedriver/emulator surface), STEP-47 changed the build chain and CI wiring, and STEP-48 added staging schema/fixture/secret surface (TEST_USER_*, Drive secrets, seed alignment). Verify the new E2E surface's secrets handling, re-run the RLS audit including the two STEP-48.17 tables (`timeline_milestones`, `benchmarks`) that postdate the baseline's "all 9 tables" claim, re-check `registries/risks.yml` rows RISK-0011..0013 disposition against current state, and adjudicate RISK-0021 (crew RLS) — separate STEP per the check-in runbook: no S1/S2 inside the check-in. Update `registries/security-reviews.yml` only on a completed review. |
| STEP-53 | Dependency Maintenance — hive_ce / forui / Flutter regression follow-ups | | Planned | `mine-flow-app`, `mine-flow-docs`, `prompts` | Dependency follow-ups surfaced by the STEP-50.1 risk review. (1) RISK-0007 trigger fired: hive_ce last stable release 2.19.3 was 2026-02-03 (~7 months); re-verify maintenance status and Dart-4 trajectory, and decide keep/migrate per ADR-0001. (2) RISK-0009 half-triggered: flutter/flutter#191587 (MergeSemantics isMergedIntoParent assertion fix) merged to flutter master on 2026-09-03; when a stable containing it ships, retest and consider dropping the forui ^0.26 pin and workarounds. (3) RISK-0020: minor transitive drift (file_picker 12.1.2→12.2.0, go_router 18.0.0→18.0.1, lucide_icons_flutter, build_runner, archive pinned by SDK) — fold into this STEP or the next dependency-touching STEP. No functional changes; upgrade-and-verify only. |

### STEP-50 substeps

| # | Title | Status | Evidence |
|---|-------|--------|----------|
| 50.1 | Doc-drift reconciliation, conditional coverage, risks & security gate | Done | `reports/2026-09-08-step-0050-check-in-report.md` (Drift/Conditional/Risks/Security sections); check.sh 0 failures; ADR-0019; STEP-52/53 reserved on prompts/main `c6012c1` |
| 50.2 | Full test run | Done | `reports/test-results/2026-09-08-step-0050-full-suite-test-results.md`; `flutter test` 553/553 at `b9bcce5` (elapsed 01:40, known Hive flake did not reproduce); workspace-root hygiene executed at close |

### STEP-49 substeps

> PLAN: `Upcoming Prompts/mine-flow-STEP-49-PLAN.md` (authored 2026-09-09). Work happens in
> the Throughstone clone at `D:\AppDev\Throughstone` on branch `step-0049-template-hardening`;
> `prompts` is touched only for STEP bookkeeping. No mine-flow application code, and mine-flow's
> local scaffold copies are not edited (adoption deferred to a future
> `UPDATING-THROUGHSTONE.md` manual-mode pass).

| # | Title | Status | Evidence |
|---|-------|--------|----------|
| 49.0 | Upstream recon: clone, verify layout, map the five guards to landing sites | Done | Findings: clone verified at c815347, layout verified against UPDATING-THROUGHSTONE.md, landing-site map & 49.4 verify-loop authored (`Upcoming Prompts/mine-flow-STEP-49.0-FINDINGS.md`) |
| 49.1 | Guards ①+② — Unverified-vs-Done honesty gate + phantom-close detection | Done | Findings: `Upcoming Prompts/mine-flow-STEP-49.1-FINDINGS.md` |
| 49.2 | Guard ③ — credential/host-toolchain pre-flight substep guidance | Done | Findings: `Upcoming Prompts/mine-flow-STEP-49.2-FINDINGS.md` |
| 49.3 | Guards ④+⑤ — commit-per-substep discipline + stranded-trunk recovery recipe | Done | Findings: `Upcoming Prompts/mine-flow-STEP-49.3-FINDINGS.md` |
| 49.4 | Scaffold smoke validation (scratch init + check.sh) + CHANGELOG entry | Done | Findings: `Upcoming Prompts/mine-flow-STEP-49.4-FINDINGS.md` · init/check logs (`step49_smoke_init.log`, `step49_smoke_check.log`) · CHANGELOG commit `f5b7980` |
| 49.5 | Push fork, open upstream PR, close STEP-49 | Planned | — |

### STEP-48 substeps

> **Close note (2026-09-08):** Statuses below are assigned from the latest findings and branch-head run `34225431645`, not from earlier per-substep optimism. `Deferred` rows retain the deliverable and identify the exact remaining boundary.

| Substep | Session / Title | Status | Output / Deliverables |
|---|---|---|---|
| 48.0 | Credential & toolchain pre-flight gate | Done | Findings: staging accounts/secrets verified by name; proof-of-life auth journey passed. |
| 48.1 | Journey-integrity repair audit | Done | Findings: fake green and stubs removed; journey assertions audited. |
| 48.2 | CI gate expansion + evidence artifacts | Done | Findings: full journey targets, CI wiring, artifact paths, and execution guards. |
| 48.3 | Auth & session runtime evidence | Done | Findings: auth journey executed and passed in branch-head run 34225431645. |
| 48.4 | Attendance & Daily Log runtime evidence | Done | Findings: persistence/read-contract repairs confirmed; both journeys passed at branch head. |
| 48.5 | Cut/Fill & Land Clearing runtime evidence | Done | Findings: both journeys passed; RISK-0014 remains a separate PDF/reporting follow-up. |
| 48.6 | Inventory & Equipment Check runtime evidence | Done | Findings: invalid write keys removed; both journeys passed at branch head. |
| 48.7 | Benchmark journey + NR-006 | Deferred | Benchmark journey passed; true browser cold-start deep-link remains unverified under RISK-0019. |
| 48.8 | Reporting / PDF runtime evidence | Done | Findings: reporting journey and NR-001 control lock passed; PDF operational regression remains RISK-0014. |
| 48.9 | Timeline & Notifications runtime evidence | Done | Findings: both journeys passed at branch head. |
| 48.10 | Offline/sync Part A against staging | Done | Findings: Android field path and server-side LWW evidence passed; web relaunch leg is Android-only by Doc 15 §1. |
| 48.11 | Deep-link validation + RISK-0006 | Done | Findings: in-process route matrix and Drive-unavailable route state passed; cold-start browser behavior remains RISK-0019. |
| 48.12 | Live RLS evidence | Deferred | Supervisor/foreman paths passed; crew and cross-role isolation remain unverified under RISK-0021. |
| 48.13 | Runtime design review with automated screenshots | Deferred | Harness executed, but valid screenshot artifacts and screen-reader evidence remain unavailable under RISK-0023/follow-up. |
| 48.14 | Risk-register reconciliation | Done | Findings: residual risks recorded and Drive deferrals re-justified. |
| 48.15 | Docs-true sweep, index correction & close | Done | This close record; Doc 09/12, STEP-45 rows, STEP-48 row, phase summary, and archive. |
| 48.16 | Branch-head failure triage | Done | Findings: branch-head failures classified and assigned. |
| 48.17 | Staging schema completion | Done | Findings: migrations applied and generated types verified. |
| 48.18 | Datasource column-name reconciliation | Done | Findings: schema column reads corrected and tested. |
| 48.19 | Write-path dual-key purge | Done | Findings: invalid write keys removed and emitted key sets tested. |
| 48.20 | Staging fixture & seed alignment | Done | Findings: fixtures aligned and RLS refusal adjudicated. |
| 48.21 | Journey finder repair | Done | Findings: ambiguous and missing finders repaired without weakening assertions. |
| 48.22 | UI/harness defect fixes | Done | Findings: overflow, Material ancestor, Drive state, and screenshot harness defects addressed. |
| 48.23 | Persistence & offline-integrity defects | Done | Findings: persistence and LWW defects fixed and verified. |
| 48.24 | Local full-gate re-run | Done | Findings: local gates and journeys passed; GO handed to commit/gate lanes. |
| 48.25 | Git object-store repair & wave commit | Done | Findings: app history repaired and branch fast-forward pushed. |
| 48.26 | Branch-head CI gate | Done | Findings §0: run 34225431645 GO; four required jobs green with non-zero execution. |
| 48.27 | Post-gate schema/reporting/synchronization remediation | Done | Findings: contract corrections and TZ fixture sweep verified. |
| 48.28 | Registry & documentation truth repair | Done | Findings: YAML corruption repaired and check 10 added. |
| 48.29 | Evidence-guard hardening | Done | Findings: Android/web zero-execution guards and l10n guard hardened. |
| 48.30 | Dead-affordance & shadow-file cleanup | Done | Findings: selection-only combobox behavior and shadow-file deletion verified. |



### STEP-47 substeps

> **Honesty note (2026-08-29, Hermes/Claude Opus 4.8 at close):** every row below was assigned
> from that substep's own evidence in
> `prompts/003-release-readiness-integration-scale/step-0047/mine-flow-STEP-47.0-EVIDENCE.md`,
> not from its optimism. 47.5 and 47.7 are `Done` for what they actually delivered — a building,
> installing APK and a green CI harness — and the part they could not deliver (executing
> `app_boots_test.dart`'s assertions) is stated inline as credential-blocked and carried to
> STEP-48 rather than ticked.

| Substep | Session / Title | Status | Output / Deliverables |
| ------- | --------------- | ------ | --------------------- |
| 47.0 | Pre-flight: baseline evidence & CI failure diagnosis | Done | `mine-flow-STEP-47.0-EVIDENCE.md` — verbatim local failure, host toolchain (Flutter 3.47.1 / Dart 3.13.1 / Temurin 17.0.20.1 / `PUB_CACHE=D:\AppDev\.pub-cache` / `Pixel_6a`), baseline gates (analyze 0, format clean, both guards, 443 tests), per-job CI conclusions for run `33163983709`, and 6 eliminated hypotheses. Q1 answered: `STAGING_*` secrets exist (proven by a historical green `deploy-staging`), `TEST_USER_EMAIL`/`TEST_USER_PASSWORD` do **not**. CI root cause recorded as **Unverified (log bodies 403 unauthenticated)** with a timing inference — honest at the time, and later resolved in 47.7 |
| 47.1 | Dependency graph remediation (pubspec + lock, override deletion) | Done | `pubspec.yaml`/`pubspec.lock` resolving with **zero `dependency_overrides`** (STEP-43's `flutter_secure_storage_windows: 4.0.0` deleted → `win32` 6.4.0); `file_picker` 12.1.2, `package_info_plus` 10.2.1, `flutter_secure_storage_windows` 4.2.2, plus 7 further majors. Post-sweep KGP audit: only `android_file_picker` 1.0.3, `battery_plus` 7.1.1, `package_info_plus` 10.2.1 still apply KGP and **all three guard it behind an AGP-major check**, so built-in Kotlin stays on. RISK-0020 raised for SDK-pinned transitives; RISK-0006 and RISK-0008 amended |
| 47.2 | `file_picker` 12 federated-API migration | Done | `upload_file_page.dart` off `FilePickerResult`/`withData` (repo-wide grep for the v11 API returns nothing); widget + cubit tests. **User-visible change:** the Data Bucket upload now asks for a file **once** instead of twice — `PlatformFile.length()`/`readAsBytes()` replace the v11 two-pick workaround. CF-078's 50 MB cap, its Indonesian message and toast styling are byte-identical and asserted by a boundary test, so the single pick must not later be read as a regression against STEP-46's audit |
| 47.3 | `bloc` 9 / `flutter_bloc` 9 / `bloc_test` 10 migration | Done | Verified: **no source change required** — 53 bloc files and all 11 `bloc_test` suites compile and pass unmodified under the new majors (commit `c217783` records the verification). An explicit no-change outcome, not a skipped substep |
| 47.4 | `go_router` 18, `googleapis` 17, `proj4dart` 3, `flutter_lints` 6 migration | Done | Router, Drive service and CRS utils clean at `flutter analyze` **0 issues** under lints 6 (`unnecessary_underscores` / `use_null_aware_elements` fixed in place, **no rule disabled**). Q3 answered with evidence: go_router 18's material_ui/cupertino_ui move needed no app-code change. CRS tolerances unchanged; no Doc 11 / ADR-0003 impact |
| 47.5 | Local Android build green + emulator boot | Done | `flutter build apk --debug` **exit 0** on this Windows host (95.5s clean / ~13s incremental at close; APK 194 MB at `build/app/outputs/flutter-apk/app-debug.apk`), zero KGP warnings. Installed on `Pixel_6a` (`emulator-5554`) and `integration_test/app_boots_test.dart` ran the harness — **its assertions did not execute**: `All tests skipped`, reason `Unverified: Staging credentials absent` → STEP-48. Q4 answered: STEP-43's `kotlin.compiler.execution.strategy=in-process` / `kotlin.incremental=false` are obsolete under built-in Kotlin and were removed; `newDsl=false` + `builtInKotlin=true` retained and documented in-file |
| 47.6 | CI `e2e-web`: replace `-d chrome` with `flutter drive` + chromedriver | Done | `ci.yml` `e2e-web` green — `flutter test integration_test -d chrome` is rejected by the tool ("Web devices are not supported for integration tests yet"); the job now runs chromedriver on 4444 and drives `test_driver/integration_test.dart`. Same caveat as 47.7: `flutter drive` reports the skipped test as a driver-level pass, so this is a harness gate |
| 47.7 | CI `build-android` + `e2e-android` green | Done | Escalated to Opus 4.8 after Flash and Pro failed across 8 red runs. `build-android` needed **no `ci.yml` change** — 47.1–47.5 fixed it. `e2e-android` root cause found by finally reading the job logs (the GitHub PAT in Git Credential Manager works as a Bearer token; the 302 to Azure blob must be followed *without* the auth header): `reactivecircus/android-emulator-runner` splits `script:` on newlines into separate **dash** `sh -c` calls, so the `\` continuation reached `flutter test` as a stray path and tripped the mixed-target guard. Fixed with a one-line invocation (no `pipefail` — dash), target narrowed to `app_boots_test.dart` per the PLAN's boot-only test plan. Also removed a debug commit's workflow-wide `permissions: contents: write` and its log-force-pushing step. **Ran-vs-skipped: 0 passed, 1 skipped**, reason `Unverified: Staging credentials absent` — the 47.7 prompt's "confirm `app_boots_test.dart` executed (not skipped)" line is **not satisfiable**: credential-blocked, not code-blocked → STEP-48 |
| 47.8 | Documentation: host prerequisites, ADR, risks register | Done | App `README.md` host-prerequisites + local Web-E2E command; `architecture/09-environments.md` **v0.4.0** with a matching Version Log row (parity stated as parity: the CI Flutter pin 3.47.0→3.47.1 fixed nothing — `build-android` was already green on 3.47.0 and the `flutter_tools` guard is byte-identical between the tags); `architecture/12-test-strategy.md` §5–§6 now records the dual-platform E2E commands (`flutter drive`/chromedriver for web and `flutter test` for Pixel 6a), while the honest harness caveat lives in Doc 09 §4; Q5 answered → **ADR-0018** (AGP-9/built-in-Kotlin posture and the reversal of STEP-43's override), registered with no duplicate number; `registries/risks.yml` RISK-0006/0008 amended, RISK-0020 added |
| 47.9 | Final verification & STEP close | Done | Full gate re-run on the branch: analyze **0**, format clean (302 files), `flutter test` **448 passing** (one order-dependent flake in `test/integration/attendance_daily_log_sync_test.dart` on the first full run — file byte-identical to `master`, green twice in isolation and on a clean full re-run, so a flake, not a regression), both contract guards pass, debug APK exit 0, `flutter build web --release` exit 0, `pub outdated` all direct/dev up to date, **no `dependency_overrides`**; emulator boot re-confirmed (harness ran, assertions skipped — credentials); CI run `33195382106` on final commit `e3cd9ed3` all four jobs green. Also repaired a 47.8 defect found at close: commit `31c081c` had re-pasted 194 lines into `registries/risks.yml` (duplicate RISK-0012..0019 + truncated RISK-0019), leaving the file unparseable — de-duplicated with no content authored, now 20 unique ids and `yaml.safe_load` clean. Merged app → docs → prompts; PLAN + 10 substep prompts + evidence + 47.2/47.4/47.6/47.7 handoff notes archived to `prompts/003-release-readiness-integration-scale/step-0047/` |

**Net outcome:** the Android surface is buildable again — a debug APK builds and installs
locally and in CI under AGP 9 built-in Kotlin, with `dependency_overrides` gone and the
dependency graph fully current. What STEP-47 does **not** deliver is runtime evidence: both CI
E2E jobs are green as *harness* gates and `app_boots_test.dart` self-skips for want of
`TEST_USER_EMAIL`/`TEST_USER_PASSWORD`. **STEP-48 inherits three unblocked prerequisites** — an
installable debug APK, a working emulator boot path, and a web E2E invocation that actually runs
— plus two inbound findings: those two secrets must be wired into `ci.yml`, and
`integration_test/journeys/deep_link_journey_test.dart` asserts `expect(true, isTrue)` with no
`markTestSkipped` guard, so it would report a meaningless pass if CI were pointed at the
journeys directory.

### STEP-45 substeps

> **Evidence note (correction, 2026-08-28, Hermes/Claude Opus 4.8):** an earlier close marked
> all 15 substeps `Done`. Disk evidence contradicted that — 14 of the 15 journey tests are
> gated behind `markTestSkipped('Unverified: Staging credentials absent')` and never executed
> against staging, and `reports/2026-08-27-step-0045-runtime-design-review.md` marks every
> design-review item Unverified. The rows below are corrected to distinguish **test/code
> authored** (real, committed, analyze+format clean) from **runtime evidence obtained** (not
> obtained). **STEP-48 outcome (2026-09-08):** The branch-head gate is now evidenced by run `34225431645`; the rows below distinguish journeys that executed and passed from paths that remain deliberately Deferred.

| Substep | Session / Title | Status | Output / Deliverables |
| ------- | --------------- | ------ | --------------------- |
| 45.1 | Reservation, branch & harness scaffold | Done | `integration_test/helpers/` (app harness, staging config, login, offline toggle) + `app_boots_test.dart` |
| 45.2 | Dual-platform E2E CI gate | Done | `e2e-web` and `e2e-android` jobs in `ci.yml`, required before `deploy-staging`; Q2 decided (every push). Never observed green — no CI run has executed them yet |
| 45.3 | Auth & session E2E journey | Done | **Verified in STEP-48.26** — run [34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645), auth journey executed and passed on web and Android; session restore, invalid login, and logout assertions passed. |
| 45.4 | Attendance & Daily Logging E2E | Done | **Verified in STEP-48.26** — run [34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645), both journeys executed and passed; status round-trips and web attendance read-back are covered by the remediation wave. |
| 45.5 | Cut/Fill & Land Clearing E2E | Done | **Verified in STEP-48.26** — run [34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645), both journeys executed and passed; remaining reporting semantic debt is tracked separately as RISK-0014. |
| 45.6 | Inventory & Equipment Checks E2E | Done | **Verified in STEP-48.26** — run [34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645), both journeys executed and passed. |
| 45.7 | Benchmark E2E + route-registration (NR-006) | Deferred | **Partially verified in STEP-48.26** — benchmark journey executed and passed in run [34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645); true cold-start browser deep-link remains unverified and stays with RISK-0019. |
| 45.8 | Data Bucket E2E + real Drive upload (NR-004/005) | Deferred | **Deferred by decision D2; not delivered in STEP-48.** Metadata route coverage executed, but real Drive upload, abandon/cancel, and large-file ceiling remain owned by RISK-0017/RISK-0018. |
| 45.9 | Reporting / PDF E2E (NR-001) | Done | **Verified in STEP-48.26** — run [34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645), reporting journey executed and passed; NR-001 controls and PDF generation are covered. |
| 45.10 | Timeline & Notifications E2E | Done | **Verified in STEP-48.26** — run [34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645), both journeys executed and passed. |
| 45.11 | Field-critical offline/sync full journey | Done | **Verified with platform scope in STEP-48.26** — Android executed and passed the offline/sync journey; web executed the supported Part B contract tests while the Android-only relaunch leg is explicitly skipped per Doc 15 §1/Q12. |
| 45.12 | Live RLS / authorization E2E against staging | Deferred | **Partially verified in STEP-48.26** — supervisor/foreman paths executed and passed; crew RLS and cross-role isolation remain unverified because `TEST_CREW_*` secrets are absent (RISK-0021). |
| 45.13 | go_router v17 deep-link validation | Deferred | **Partially verified in STEP-48.26** — in-process route matrix and upload-route availability executed and passed; true browser cold-start/reload behavior remains unverified (RISK-0019). |
| 45.14 | Runtime Impeccable design review | Deferred | **Harness executed in STEP-48.26, but design-review artifacts are not delivered:** the capture harness is green while screenshot artifacts remain unavailable and the committed placeholder set is not evidence; accessibility/screen-reader behavior remains unverified (RISK-0023 and follow-up). |
| 45.15 | Findings reconciliation, docs, risks & STEP close | Done | ADR-0017; Doc 12 v1.1; Doc 09 v0.3.0; RISK-0015..0019; `reports/2026-08-27-step-0045-findings-reconciliation.md` (NR-001 resolved, NR-002..006 carried forward); archived to `003-release-readiness-integration-scale/step-0045/` |

**Net outcome:** STEP-48 delivered executable staging runtime evidence and a green branch-head gate. The residual boundaries remain explicit in the STEP-48 row and findings: Drive behavior, crew RLS/cross-role isolation, true browser cold-start deep links, valid screenshot-backed design-review artifacts, and screen-reader evidence are not delivered. **Phase 4 planning remains closed pending the user's acceptance or resolution of those residuals.**


### STEP-44 substeps

| Substep | Session / Title                                                | Status      | Output / Deliverables |
| ------- | -------------------------------------------------------------- | ----------- | ---------------------- |
| 44.1    | STEP reservation & branch setup                                | Done        | `step-0044-security-baseline` branches; STEP-index row flipped to In progress |
| 44.2    | RLS / authorization behavior audit                             | Done        | No gaps found — all 9 tables covered; post-migration schemas (migrations 3/4/5) have no new tables; documented in S0 report |
| 44.3    | Account lifecycle verification                                 | Done        | `deleted_at` on users; supervisors-only DELETE; correctly implemented; documented in S0 report |
| 44.4    | Privacy notice (in-app) gap check                              | Done        | Not implemented → RISK-0011 added as pre-release gate |
| 44.5    | Secrets posture audit                                          | Done        | `.env.example` confirmed present (STEP-42); `.env` gitignored; all CI secrets via `secrets.*`; RISK-0013 for unverified items |
| 44.6    | Backup / restore fire-drill record                             | Done        | Free-tier → no auto backup; manual procedure documented in S0 report; RISK-0012 added |
| 44.7    | S0 baseline report & risk / security-reviews registry update   | Done        | `reports/security/2026-08-26-step-0044-s0-security-baseline-report.md`; `registries/risks.yml` (RISK-0011/12/13); `registries/security-reviews.yml` S0 populated |
| 44.8    | Architecture doc update & STEP close                           | Done        | Doc 06 v0.2.0; STEP-44 Done; branches merged; plan archived; `flutter analyze` 0 issues; 435/435 tests |

### STEP-46 substeps

| Substep | Session / Title                                         | Status  | Output / Deliverables                                                       |
| ------- | ------------------------------------------------------- | ------- | --------------------------------------------------------------------------- |
| 46.1    | Pass 1a — Code-level static scan (all 24 screens)       | Done | `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.1-FINDINGS.md` — 125 candidates (P1 53 / P2 52 / P3 20); `flutter analyze` 0 issues, 435/435 tests, l10n guard OK |
| 46.2    | Pass 1b — Screenshot visual review (all 24 screens)     | Done | `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.2-FINDINGS.md` + screenshots |
| 46.3    | Pass 2 — Strong-model confirmation & finding register    | Done | `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md` — 97 confirmed (P1 46 / P2 38 / P3 13), 6 rejected, 6 needs-runtime (→ STEP-45) from 175 raw candidates |
| 46.4    | Remediation implementation                              | Done | 97 confirmed findings fixed (P1 46 / P2 38 / P3 13) on `step-0046-ui-ux-audit`; ADR-0012..0016 for the product/architecture decisions; `flutter analyze` 0 issues; `flutter test` 442 passing (baseline 434), one known order-dependent flake non-reproducible on re-run/isolation; `flutter build web --release` OK; RISK-0014 raised (reporting datasource legacy volume) |

### STEP-42 substeps

| Substep | Session / Title | Status | Output / Deliverables |
| ------- | --------------- | ------ | --------------------- |
| 42.1 | Supabase CLI install, link & migrations | Done | `supabase/config.toml` committed; migration renamed; seed.sql patched |
| 42.2 | Generated types commit & contract guard hardening | Done | `supabase/types/database.ts` committed (real `gen types --lang typescript` output; Dart typegen removed from CLI, supabase/cli#6230); stub `database.dart` deleted; guard hardened with stub-rejection content checks; 434/434 tests |
| 42.3 | Staging GCP service account & GitHub Secrets | Done | `.env.example` updated with `SUPABASE_PROJECT_REF` and `STAGING_*` keys |
| 42.4 | `deploy-staging` CI job | Done | `deploy-staging` job in `ci.yml`; Flutter Web builds and deploys to staging Pages slot; staging URL verified |
| 42.5 | `deploy-production` job & manual gate | Done | `deploy-production` job in `ci.yml` with production environment review gate (release-published trigger) |
| 42.6 | Seed data audit & patch | Done | `supabase/seed.sql` patched for STEP-33/36/38 additions; all 8 feature tables seeded |
| 42.7 | Runbooks, ADR, doc updates & STEP close | Done | `staging-provision.md`, `release-procedure.md`, ADR-0011, Doc 08/09 v0.2.0, RISK-0010; merged to trunk; archived |

### STEP-43 substeps

| Substep | Session / Title | Status | Output / Deliverables |
| ------- | --------------- | ------ | --------------------- |
| 43.1 | CI Workflow Hardening & Flutter Pin | Done | `.github/workflows/ci.yml`: JDK 17 Temurin setup in both jobs; both jobs pinned to Flutter `3.47.0`; STEP-42 prompt CI skeletons forward-fixed |
| 43.2 | Android Build Chain Upgrade | Done | `android/settings.gradle.kts`: AGP `9.0.1` → `9.1.0`; KGP `2.3.20` → `2.4.0`; `android/app/build.gradle.kts`: `compileSdk = 37`, minSdk via `flutter.minSdkVersion` (=24 on Flutter 3.47, satisfies secure-storage v11 ≥23); gradle wrapper 9.3.1 |
| 43.3 | pubspec.yaml Core Package Fixes | Done | Fixed `flutter_bloc ^9.1.1` → `^8.1.6`; upgraded go_router, supabase_flutter, connectivity_plus, build_runner; corrected `bloc_test ^9.1.5`; SDK `>=3.12.0`. No win32 override needed on fresh resolution |
| 43.4 | Hive → hive_ce Migration | Done | 26 Dart files: `package:hive/` → `package:hive_ce/`; `package:hive_flutter/` → `package:hive_ce_flutter/`; hive_ce `2.19.3`, hive_ce_flutter `2.3.4` |
| 43.5 | flutter_secure_storage v11 Upgrade | Done | `pubspec.yaml`: `^9.2.4` → `^11.0.0`; `secure_storage_service.dart`: removed obsolete `encryptedSharedPreferences`; `build.gradle.kts`: minSdk requirement met via `flutter.minSdkVersion` (=24) |
| 43.6 | file_picker v11 API Migration | Done | `pubspec.yaml`: `^9.0.0` → `^11.0.3`; `upload_file_page.dart`: `FilePicker.platform.pickFiles()` → `FilePicker.pickFiles()` |
| 43.7 | forui + fl_chart Upgrade | Done | forui `^0.24.2` → `^0.26.0` (0.26 required: 0.24/0.25 wrap FTextField in MergeSemantics, tripping flutter/flutter#191095 semantics regression on 3.47); fl_chart → `^1.2.0`. Test finders moved TextField → EditableText; inventory entry suffix dropdown wrapped in Flutter material-localizations scope |
| 43.8 | go_router v17 Compatibility | Done | Verified v16→v17 breaking changes (observer only); `lib/app/router.dart` unchanged; `flutter analyze` 0 issues |
| 43.9 | Full Verification Gate | Done | `flutter pub get` exit 0; `flutter analyze` 0 errors/warnings; guards pass; **434/434 tests** (re-verified 2026-08-25 housekeeping; earlier "435" count was wrong); `flutter build apk --debug` exit 0 (Windows Kotlin workaround in gradle.properties) |
| 43.10 | Risk Register & Doc Updates | Done | Canonical register @ `15de557`: RISK-0005 fl_chart v1.x migration, RISK-0006 go_router v17 audit, RISK-0007 hive_ce fork continuity, RISK-0008 secure_storage v9→v11 skip, RISK-0009 flutter#191095/forui 0.26 workaround; audit reports `2026-08-13-flutter-dependency-ci-audit.md`, `2026-08-10-doc-drift-implementation-audit.md`; upgrade report at `reports/2026-08-25-step-0043-upgrade-report.md` (committed + cross-refs aligned by housekeeping) |
| 43.11 | STEP-42 Rebase & Close | Done | Clean 3-commit `step-0042-staging-pipeline` rebased on master (STEP-43 base); full verification gates pass; force-pushed; STEP-42 In progress |

### STEP-41 substeps

| Substep | Session / Title                                              | Status  | Output / Deliverables                                                                                                              |
| ------- | ------------------------------------------------------------ | ------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 41.1    | Release-readiness inventory and acceptance matrix            | Done | `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md`                                             |
| 41.2    | Reproducible Supabase generated-type contract gate           | Done | Guard script (`tool/check_supabase_contracts.dart`) and CI integration                                                             |
| 41.3    | Localization compliance baseline and regression guard        | Done | Documented localization inventory; narrowly scoped static/test guard; tests proving locale configuration                           |
| 41.4    | Fresh release baseline verification and reconciliation close | Done    | Updated final report; appropriate doc/version-log and risk changes; verified commands/results                                      |
| 41.5 | Audit Fix — Guard Correctness & CI Hardening | Done | Fixed ISSUE-4 (l10n regex catches double-quoted strings), ISSUE-8 (CI fetch-depth), ISSUE-1/5/6 (guard robustness); 3 l10n tests, 3 contract tests passing |

### STEP-32 substeps

| Substep | Session / Title                                       | Status | Output / Deliverables                                                                                                          |
| ------- | ----------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| 32.2.F1 | Resolve hardcoded colors in `creatable_combobox.dart` | Done   | `Colors.black` → `theme.colors.foreground`; `Colors.transparent` → semantic muted/background tokens; zero raw colors remaining |

### STEP-33 substeps

| Substep | Session / Title                                       | Status | Output / Deliverables                                                                                                     |
| ------- | ----------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------- |
| 33.1    | Data Model & Repository Polish                        | Done   | Updated entities, models, Supabase sync mappings, and Hive adapters for Cut/Fill, Land Clearing, Daily Log, and Inventory |
| 33.2    | Operations Tracking UI Refactor                       | Done   | Updated `CutFillListScreen`, `LandClearingSummaryScreen` and their entry forms                                            |
| 33.3    | Daily Log & Inventory UI Refactor                     | Done   | Integrated `CreatableCombobox` for Daily Log Zone, implemented auto-predict for Inventory item names                      |
| 33.4    | Tests & Verification                                  | Done   | E2E and Integration test fixes for the updated data shapes and UI elements                                                |
| 33.1.F1 | Verify & reconcile DoD in `mine-flow-STEP-33-PLAN.md` | Done   | All 6 DoD items verified against codebase with evidence citations; no unchecked boxes remain                              |
| 33.3.F1 | Purge Material from `daily_log_form_screen.dart`      | Done   | `Card` → `FCard`; `ElevatedButton` removed; zero Material container/button references remain                              |

### STEP-30 substeps

| Substep | Session / Title                                  | Status | Output / Deliverables                                                                                                                       |
| ------- | ------------------------------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 30.1    | Core Shell & Auth                                | Done   | `pubspec.yaml`, `lib/app/app.dart`, `lib/app/presentation/`, `LoginPage`, `DashboardPage`                                                   |
| 30.2    | Operations & Tracking                            | Done   | `CutFillListScreen`, `LandClearingSummaryScreen`, `InventoryDashboardScreen`                                                                |
| 30.3    | Teams & Field Docs                               | Done   | `AttendanceScreen`, `DailyLogListScreen`, `EquipmentHistoryScreen`                                                                          |
| 30.4    | Reports, Data Bucket & Notifications             | Done   | `TimelinePage`, `ReportDashboardPage`, `ReportConfigPage`, `DataBucketListPage`, `UploadFilePage`, `FileDetailPage`, `NotificationListPage` |
| 30.5    | Analyzer Clean-up                                | Done   | 0 analyzer issues globally                                                                                                                  |
| 30.6    | Final Cross-Screen Material Purge & CI Gate      | Done   | Material purge complete; 273/281 tests pass (8 pre-existing failures in tracking feature files from STEP-30.2 ForUI API mismatches)         |
| 30.6.F1 | Purge Material from Theme & Crew Roster          | Done   | `app_theme.dart` ThemeData purge, `crew_roster_item.dart` FCard/FButton swap, per-screen visual check verified                              |
| 30.6.F3 | Correct ForUI theme variant (FTheme.neutral)     | Done   | API correction confirmed forui 0.24.x uses `FTheme.neutral`, documentation updated                                                          |
| 30.6.F2 | Purge custom color palette from `app_theme.dart` | Done   | `notification_banner.dart` updated to ForUI `destructive` tokens, zero-consumer `app_theme.dart` deleted                                    |

### STEP-31 substeps

| Substep | Session / Title                        | Status | Output / Deliverables                                                                                                                                                                           |
| ------- | -------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 31.1    | Shell Routing & Scaffolding            | Done   | `lib/app/router.dart` (StatefulShellRoute), `lib/app/presentation/pages/app_shell.dart`                                                                                                         |
| 31.2    | Navigation Shell UI (Desktop & Mobile) | Done   | Responsive ForUI sidebar with 5 nav items, profile card & theme toggle; FBottomNavigationBar with kebab menu sheet; `lib/app/presentation/pages/app_shell.dart`; `test/app/app_shell_test.dart` |
| 31.3    | Dashboard Cleanup & Regrouping Wiring  | Done   | Removal/update of `dashboard_page.dart`, wiring the 3 exact groupings                                                                                                                           |
| 31.4    | Test Suite Verification & Fixes        | Done   | Updated AppShell tests (7 tests), added router tests (6 tests), all AppShell+router tests pass. Pre-existing failures (2 attendance, 4 equipment_history) remain unchanged.                     |
| 31.5    | Global App Header                      | Done   | Implement Shadcn Admin style global header for Desktop (breadcrumb, search, theme, avatar) and Search-centric header for Mobile (search, theme, avatar)                                         |

### STEP-34 substeps

| Substep | Session / Title                                       | Status | Output / Deliverables                                                                                                                                   |
| ------- | ----------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 34.1    | Domain & Data Layer Refactor                          | Done   | Updated entity, models, Hive adapters, Supabase migration                                                                                               |
| 34.2    | Data Bucket UI Refactor                               | Done   | Removed lat/lon input fields from UploadFilePage; no lat/lon existed in DataBucketListPage/FileDetailPage — verified clean                              |
| 34.3    | Reporting Integration UI                              | Done   | Removed ReportDashboardPage and its route; added Laporan button to FAppBar of all 6 feature screens; cleaned up dead references; analyzer passes clean  |
| 34.4    | Tests & Verification                                  | Done   | 336 tests passing, `flutter analyze` clean (no issues found) — no regressions from lat/lon removal or router changes                                    |
| 34.1.F1 | Verify & reconcile DoD in `mine-flow-STEP-34-PLAN.md` | Done   | All 6 DoD items verified against codebase with evidence citations; no unchecked boxes remain                                                            |
| 34.2.F1 | Purge Material from Data Bucket & Reporting screens   | Done   | `file_card.dart` Card→FCard; `upload_file_page.dart` and `report_config_page.dart` TextButton/OutlinedButton→FButton; per-screen visual checks verified |

### STEP-35 substeps

| Substep | Session / Title                                       | Status | Output / Deliverables                                                                        |
| ------- | ----------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------- |
| 35.1    | Domain & Data Layer for Settings                      | Done   | `SettingsRepository`, `SettingsEntity`, `SettingsRepositoryImpl`, `SettingsLocalDatasource`  |
| 35.2    | State Management & App Wiring                         | Done   | `SettingsCubit`, `app.dart` integration                                                      |
| 35.3    | Settings Page UI Shell & Integrations                 | Done   | `SettingsPage`, router entry at `/settings`                                                  |
| 35.4    | Verification & Polish                                 | Done   | 13 settings tests passing, `flutter analyze` clean                                           |
| 35.2.F1 | Verify & reconcile DoD in `mine-flow-STEP-35-PLAN.md` | Done   | All 6 DoD items verified against codebase with evidence citations; no unchecked boxes remain |

### STEP-36 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                         |
| ------- | ---------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| 36.1    | Benchmark Domain, Data Layer & CRS | Done   | `lib/features/benchmark/domain/`, `lib/features/benchmark/data/`, `lib/core/utils/crs_utils.dart`, `test/features/benchmark/` |
| 36.2    | Benchmark UI & BLoC                | Done   | `lib/features/benchmark/presentation/`                                                                                        |
| 36.3    | Offline Sync & Verification        | Done   | `SyncRegistrar` implementation, unit/widget tests                                                                             |

### STEP-37 substeps

| Substep | Session / Title                    | Status | Output / Deliverables                                                                                                                                          |
| ------- | ---------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 37.1    | Equipment Check Feature Purge      | Done   | `equipment_check_form_screen.dart` (ElevatedButton→FButton), `sop_checklist_item_card.dart` (Card→Container), `equipment_check_card.dart` (TextButton→FButton) |
| 37.2    | Timeline Feature Purge             | Done   | `milestone_card.dart` (Card→Container + InkWell preserved)                                                                                                     |
| 37.3    | Notifications Feature Purge        | Done   | `notification_list_page.dart` (TextButton→FButton), `notification_banner.dart` (MaterialBanner→Container + FButton)                                            |
| 37.4    | Data Bucket Feature Purge          | Done   | `file_detail_page.dart` (TextButton in AlertDialog→FButton ghost/destructive)                                                                                  |
| 37.5    | Final Verification & Analyzer Gate | Done   | `flutter analyze` clean, `flutter test` zero new failures, manual spot-check all 7 widgets                                                                     |

### STEP-38 substeps

| Substep | Session / Title                             | Status | Output / Deliverables                                                                                  |
| ------- | ------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------ |
| 38.1    | Button and AppBar Consistency               | Done   | FButton with icon+label in FAppBar on all list screens; Laporan icon button; upload form appbar fix    |
| 38.2    | Cut/Fill and Land Clearing Form Fixes       | Done   | BCM/LCM label/unit fix, 2-col layout, remove steppers, CreatableCombobox for Zona and Metode Clearing  |
| 38.3    | Language Configuration Fix                  | Done   | Locale wired from SettingsCubit to MaterialApp.router; SettingsEntity locale field                     |
| 38.4    | Inventory Form and Land Clearing Tab Layout | Done   | Inventory merged Jumlah+Satuan row; Land Clearing Plan/Actual tab layout                               |
| 38.5    | Breadcrumbs and Benchmark Navigation Fix    | Done   | Segment labels title-cased; Benchmark route corrected to /operations/benchmark-db; sidebar entry added |
| 38.6    | Attendance Form Extraction                  | Done   | AttendanceFormPage (new), standalone route at /teams/attendance/form, shows employee name and position |
| 38.7    | Equipment Check Mobile Layout Fix           | Done   | Overflow fixed on narrow mobile; all controls reachable                                                |

### STEP-40 substeps

| Substep | Session / Title                                                         | Status  | Output / Deliverables                                                                         |
| ------- | ----------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------- |
| 40.1    | Fix `FTheme` wrappers in `daily_log_screen_test.dart` (4 form failures) | Done    | 4 `DailyLogFormScreen` widget tests green                                                     |
| 40.2    | Migrate 2 `AttendanceScreen` tests to `AttendanceFormPage`              | Done    | 2 attendance widget tests green (targeting correct screen post-STEP-38 extraction)            |
| 40.3    | Fix `SyncQueueManager` retry test timing race                           | Done    | `handles retries and marks failed items after exceeding max retries` integration test green   |
| 40.4    | Fix smoke test `widget_test.dart` `FAccessibilityScope` crash           | Done    | `app launches without crashing` smoke test green                                              |
| 40.5    | Full verification and close                                             | Done    | `flutter test` 0 failures, `flutter analyze` clean, STEP archived                            |

## How to add a STEP

See `prompts/README.md` for the authoring recipe.
