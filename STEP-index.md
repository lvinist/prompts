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

| STEP    | Title                                   | Owner       | Status  | Repos (projection)                           | Scope (one line)                                                                                                                                                                      |
| ------- | --------------------------------------- | ----------- | ------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| STEP-1  | Architecture                            |             | Done    | `mine-flow-docs`, `prompts`                  | Architecture-first: design docs + ADRs, no code. Substeps = the sessions in `templates/architecture-sessions/`. Branch: `step-0001-architecture`.                                     |
| STEP-2  | Scaffold repos & skeleton               |             | Done    | `mine-flow-app`                              | Create the Flutter repository, Clean Architecture structure, apply license, and setup `.env.example` baseline.                                                                        |
| STEP-3  | Core Data Layer & Authentication        | Antigravity | Done    | `mine-flow-app`                              | Implement Supabase schema, RLS policies, auth, generate Dart models, and setup Hive offline caching foundation. Substeps 3.1–3.5. Branch: `step-0003-core-data-auth`.                 |
| STEP-4  | Tier 1 - Attendance & Daily Logging     | Antigravity | Done    | `mine-flow-app`                              | Build UI and offline sync logic for crew attendance and daily structured logs for field operations. Substeps 4.1–4.5. Branch: `step-0004-attendance-daily-logging`.                   |
| STEP-5  | Tier 1 - Equipment Digital Checks       | Antigravity | Done    | `mine-flow-app`                              | Implement SOP-based pre-work and post-work condition checks for GNSS, Total Station, and Drone/UAV with offline sync. Substeps 5.1–5.4. Branch: `step-0005-equipment-digital-checks`. |
| STEP-6  | Mid-Phase Check-in                      | Antigravity | Done    | `mine-flow-docs`, `prompts`                  | Run standard check-in runbook (`runbooks/check-in.md`) to reconcile drift and review risks.                                                                                           |
| STEP-7  | Tier 2 - Field Tracking & Measurement   | Antigravity | Done    | `mine-flow-app`                              | Build manual entry screens and data flow for cut/fill volume tracking, land clearing area, and inventory. Substeps 7.1–7.5. Branch: `step-0007-field-tracking-measurement`.           |
| STEP-8  | Tier 2 - Data Bucket Integration        | Antigravity | Done    | `mine-flow-app`                              | Integrate Google Drive API for uploading heavy geospatial files (.shp, .tiff) and save metadata to Supabase.                                                                          |
| STEP-9  | Tier 3 - Reporting, Timeline & Polish   | Antigravity | Done    | `mine-flow-app`                              | Add visual work timeline, PDF report generation, and in-app notifications. Substeps 9.1–9.5. Branch: `step-0009-reporting-timeline-polish`.                                           |
| STEP-10 | End-to-End Integration & Final Check-in | Antigravity | Done    | `mine-flow-app`, `mine-flow-docs`, `prompts` | Wire capabilities together to ensure launch criteria are met end-to-end, and run final check-in.                                                                                      |
| STEP-11 | Phase 1 Polish & UI Wrap-up             | DeepSeek    | Planned | `mine-flow-app`, `prompts`                   | Implement shadcn-admin collapsible sidebar shell and responsive dashboard, fix 92 analyzer warnings, and archive loose prompts.                                                       |
| STEP-12 | Complete MVP Functional Wiring & Sync   | DeepSeek    | In progress | `mine-flow-app`, `prompts`                   | Wire orphaned UI screens into router, implement missing sync registrars for tracking/attendance/logging/equipment, and clean up duplicate folders.                                    |

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

| Substep | Session / Title                     | Status  | Output / Deliverables                                                              |
| ------- | ----------------------------------- | ------- | ---------------------------------------------------------------------------------- |
| 11.1    | Responsive UI Shell & Navigation    | Planned | `lib/app/router.dart`, new `lib/app/presentation/` shell, dark/light toggle action |
| 11.2    | Card-based Dashboard Stats          | Planned | Updated dashboard placeholder with stat summary cards (shadcn-admin style)         |
| 11.3    | Code Quality Polish (Lint Fixes)    | Done    | Global fix for 92 analyzer warnings (prefer_const_constructors, etc.)              |
| 11.4    | Workspace Hygiene (Archive Prompts) | Done    | Unarchived STEP-7, 8, 9 files moved into `prompts/001-mvp/step-NNNN/`              |
| 11.5    | Notification Rules Implementation   | Planned | Fully implemented rules 2-4 in `NotificationRuleEngine` connected to repos         |

## How to add a STEP

See `prompts/README.md` for the authoring recipe.
