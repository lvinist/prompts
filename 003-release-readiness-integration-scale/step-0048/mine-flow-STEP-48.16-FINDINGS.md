# STEP-48.16 Findings: Branch-Head Failure Triage & Classification Gate

**Date:** 2026-08-31  
**Executor:** GPT 5.6 Terra  
**Branch:** `step-0048-runtime-evidence`  
**Source run:** [33327930159](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159)  
**Android job:** `99301582624`  
**Web job:** `99301582641`

## Verdict

**Complete. The branch-head gate remains blocked.** The Android log contains 10 failed journey/test files, and the Web loop contains 10 `result:false` records. They reduce to 18 distinct failure rows below because the same database and UI failures recur across files and platforms. Every row has exactly one owning remediation substep.

The Android `adb: device offline` messages are normal emulator boot polling; the log later records `Emulator booted.` They are not a failure and are not assigned a remediation substep.

## Branch-head register

| ID | Platform | Journey file + line | Verbatim evidence | Classification | Root cause | Owner | Earlier status |
|---|---|---|---|---|---|---|---|
| BH-001 | Android/Web | timeline, notifications, deep-link; timeline datasource | `PGRST205 Could not find the table 'public.timeline_milestones' in the schema cache` | schema-gap | `timeline_milestones` is queried by the shipped timeline datasource, but no applied migration creates it. The orphan feature fragment is not an applied Supabase migration. | 48.17 | 48.9 and 48.11 treated timeline/route runtime as verified; this is staging schema drift exposed at branch head. |
| BH-002 | Android/Web | benchmark journey | `PGRST205 Could not find the table 'public.benchmarks' in the schema cache` | schema-gap | `benchmark_remote_datasource.dart` queries `benchmarks`, while `supabase/migrations/` contains no table migration. | 48.17 | 48.7 already recorded this as Deferred. |
| BH-003 | Android/Web | timeline, reporting | `column cut_fill_records.measurement_date does not exist` | schema-gap | The database authority defines `measured_at` in `20260718000001_core_schema.sql`; `timeline_remote_datasource.dart:71` and `reporting_remote_datasource.dart:63` still filter on `measurement_date`. | 48.18 | 48.5/48.8 had runtime evidence for narrower journeys, not this reporting/timeline call path. |
| BH-004 | Android/Web | timeline | `column land_clearing_records.date does not exist` | schema-gap | The schema defines `cleared_at`, not `date`; the timeline query path uses the obsolete name. | 48.18 | New cross-feature branch-head evidence. |
| BH-005 | Android/Web | inventory journey | `Could not find the 'item_name' column of 'inventory_items' in the schema cache` | schema-gap | `Code/mine-flow-app/lib/features/tracking/data/models/inventory_item_model.dart:58` emits `item_name` alongside the valid `name` key. The applied schema has `name` only. | 48.19 | 48.6 claimed invalid columns were removed; current branch evidence disproves that claim for this active model path. |
| BH-006 | Android | equipment-check path in branch-head run | `Could not find the 'status' column of 'equipment_checks' in the schema cache` | schema-gap | `Code/mine-flow-app/lib/features/equipment_check/data/models/equipment_check_dto.dart:99` emits `status`; the schema defines `is_operational`. | 48.19 | 48.6's equipment journey did not expose this sync write against the current staging contract. |
| BH-007 | Android/Web | daily-log journey | `invalid input syntax for type uuid: ""` | fixture-drift | The zone payload reaches Supabase with an empty `site_id`/UUID value. A UUID column cannot accept the fixture value. | 48.20 | New branch-head fixture evidence. |
| BH-008 | Android/Web | daily-log journey | `insert or update on table "daily_logs" violates foreign key constraint "daily_logs_zone_id_fkey"` | fixture-drift | The zone insert fails first, so the selected zone does not exist when the daily-log row is inserted. This is the cascading fixture failure, not a separate schema defect. | 48.20 | New branch-head fixture evidence. |
| BH-009 | Android/Web | attendance journey | `invalid input syntax for type uuid: "KRU-001"` | fixture-drift | The attendance fixture uses the natural identifier `KRU-001` where `attendance_records.user_id` requires the UUID of a seeded `users` row. | 48.20 | New branch-head fixture evidence. |
| BH-010 | Android/Web | attendance journey | `invalid input syntax for type uuid: "KRU-002"` | fixture-drift | Same fixture defect as BH-009 for the second crew identifier. | 48.20 | New branch-head fixture evidence. |
| BH-011 | Android | cut-fill / land-clearing journey | `new row violates row-level security policy for table "zones"` (`42501`) | test-defect | `20260718000002_rls_policies.sql:58-60` permits zone writes only for the supervisor role. The journey attempts a zone insert under a role that policy correctly refuses; the refusal is expected authorization behavior, so the test must use an existing zone or assert the refusal. | 48.20 | 48.12 positively verified the same foreman refusal; its evidence remains valid. |
| BH-012 | Android/Web | attendance journey | `Expected: AttendanceStatus:<AttendanceStatus.sick> / Actual: AttendanceStatus:<AttendanceStatus.present>` | app-defect | The branch-head round trip does not preserve the selected sick status. The defect is in the active form/write/read path or save timing, not a reason to weaken the assertion. | 48.23 | 48.4's earlier pass is no longer true for the branch head. |
| BH-013 | Android/Web | daily-log journey | `Expected: LogStatus:<LogStatus.submitted> / Actual: LogStatus:<LogStatus.draft>` | app-defect | The submitted state is not persisted or is read back before the status write is committed. The assertion correctly catches a data-integrity defect. | 48.23 | 48.4's earlier pass is no longer true for the branch head. |
| BH-014 | Android/Web | deep-link journey | `UnimplementedError: GoogleDriveService not wired and no driveService provided` | app-defect | `upload_file_page.dart:59` throws while constructing a routed page. A Drive-out-of-scope configuration must render an explicit unavailable state; navigation must not crash. | 48.22 | 48.11's route matrix claimed `/tools/data-bucket/upload` resolved; that claim is downgraded for this route. |
| BH-015 | Android/Web | timeline journey | `A RenderFlex overflowed by 21 pixels on the right` | app-defect | `timeline_page.dart:289` has a horizontal layout that exceeds the available width at the tested surface. This is an application layout defect. | 48.22 | New branch-head evidence; 48.9's earlier timeline run did not cover this surface/width state. |
| BH-016 | Android/Web | cut-fill / land-clearing journeys | `Bad state: Too many elements` | test-defect | The journey calls `enterText` through a finder that resolves more than one `EditableText` (`cut_fill_journey_test.dart:90`, `land_clearing_journey_test.dart:83`). The app can be correct while the test finder is ambiguous. | 48.21 | 48.5's prior run did not expose the current finder ambiguity. |
| BH-017 | Android/Web | notifications journey | `Bad state: No element` on `find.bySemanticsLabel('Tutup notifikasi')` (`notifications_journey_test.dart:139`) | test-defect | The journey assumes a semantics-labelled dismiss control that is not present in the widget tree. Repair the locator/semantics contract without weakening the notification assertion. | 48.21 | 48.9's earlier notification pass did not cover this current locator state. |
| BH-018 | Android/Web | design-review capture | `Bad state: Call convertFlutterSurfaceToImage() before taking a screenshot` | app-defect | The Android screenshot path calls `takeScreenshot` without first converting the Flutter surface. The harness/test integration is part of the runtime evidence path and must initialize it correctly. | 48.22 | 48.13's committed evidence is web-only; Android capture was not actually verified. |

### Compound records with insufficient detail

The Web inventory and reporting records each say `Multiple exceptions (2) were detected during the running of the current test`. The Android log supplies the actionable underlying evidence for those same surfaces: BH-005/BH-006 plus BH-014/BH-015 for inventory, and BH-003 plus the Material-ancestor error for reporting. The generic wrapper is not promoted to a second invented root cause. The reporting Material failure is recorded as BH-019 below.

| ID | Platform | Journey file + line | Verbatim evidence | Classification | Root cause | Owner |
|---|---|---|---|---|---|---|
| BH-019 | Android | `reporting_journey_test.dart` | `No Material widget found. DropdownButton<String> widgets require a Material widget ancestor` | app-defect | The reporting/cut-fill UI still mounts a Material `DropdownButton` outside a Material ancestor, contradicting the ForUI purge/UI contract. | 48.22 |
| BH-020 | Android | `daily_log_journey_test.dart` | `Found 0 widgets with type "DailyLogListScreen"` | app-defect | After `appRouter.go`, the expected daily-log list route does not resolve to the widget the journey contract requires. This is a navigation/runtime defect, distinct from the earlier failed zone fixture writes. | 48.22 |

## Counts and coverage

- Android: **10 failed files**, matching the CI summary `14 tests passed, 10 failed, 2 skipped`.
- Web: **10 `result:false` records**, corresponding to attendance, benchmark, cut/fill, daily log, deep link, inventory, land clearing, notifications, offline/sync, and reporting. The web loop also records successful records between these failures.
- Distinct register rows: **20**. Repeated PostgREST messages are grouped by root cause; no failure is assigned to more than one owner.
- Android startup polling is not counted as a failure.

## Q7: audit of the ten earlier Done substeps

| Substep | Decision | Reason and amendment |
|---|---|---|
| 48.3 | Stays `Done` | Auth/session evidence is not contradicted by this run. |
| 48.4 | **Downgrade to `Deferred`** | The branch-head attendance and daily-log status assertions fail (BH-012/BH-013). Its earlier feature evidence is known false at branch head. Amendment appended to `48.4-FINDINGS.md`; remediation belongs to 48.23. |
| 48.5 | Stays `Done` | Both failures are ambiguous-finder/test-path failures (BH-011/BH-016), while the earlier volume semantics evidence remains independently valid. The zone RLS refusal is already positively corroborated by 48.12. |
| 48.6 | **Downgrade to `Deferred`** | The active tracking/equipment write paths still emit invalid schema keys (BH-005/BH-006), contradicting the earlier claim that the relevant sync paths were verified. Amendment appended to `48.6-FINDINGS.md`; remediation belongs to 48.19. |
| 48.8 | **Downgrade to `Deferred`** | Branch-head reporting fails with the Material-ancestor defect (BH-019) and the obsolete reporting column (BH-003). Amendment appended to `48.8-FINDINGS.md`; remediation belongs to 48.18/48.22. |
| 48.9 | Stays `Done` | The earlier timeline/notification fixes remain real; the current failures are new staging-contract and locator/width evidence. Remediation belongs to 48.17/48.18/48.21/48.22. |
| 48.10 | Stays `Done` with platform scope clarified | Android offline/sync evidence remains valid. The Web pre-drain row in this run was already present on staging; this is routed to 48.23 for stale-state versus real web-offline diagnosis, without weakening the Android claim. |
| 48.11 | **Downgrade to `Deferred`** | The route matrix is not currently valid because navigating to the upload route throws BH-014. Amendment appended to `48.11-FINDINGS.md`; remediation belongs to 48.22. |
| 48.12 | Stays `Done` (partial) | The `42501` refusal is consistent with the documented policy and was already a positive result. Crew/cross-role coverage remains the existing documented limitation. |
| 48.13 | **Downgrade to `Deferred`** | The Android capture leg fails BH-018, so the earlier design-review verification is incomplete and the committed screenshot set is web-only. Amendment appended to `48.13-FINDINGS.md`; remediation belongs to 48.22. |

**Downgraded:** 5 of the 10 earlier Done substeps: **48.4, 48.6, 48.8, 48.11, and 48.13**. The earlier substeps were honest at their own evidence points, but their claims were too broad for the current branch head or were contradicted by current runtime behavior. The remaining Done statuses are retained with narrower scope where needed.

## PLAN inventory verification

The PLAN inventory is materially confirmed. Corrections/additions:

- The Android boot messages are not infrastructure failures; the emulator recovered.
- The inventory's `land_clearing_records.clearing_method` / `vegetation_type` warning is confirmed as an unfired same-class write defect. The active `tracking/data/models/land_clearing_model.dart:67-68` emits both keys even though the applied schema has `method` and not those legacy names.
- The inventory should separately call out the reporting Material-ancestor exception (BH-019) and the daily-log route-resolution assertion (`Found 0 widgets with type "DailyLogListScreen"`), which is routed to 48.22 as an app/navigation defect rather than silently folded into fixture drift.
- `inventory_items.item_name` is emitted by the tracking model path despite 48.6's earlier claim; it is a current write-path mismatch, not merely historical documentation drift.
- The Web offline failure is not classified as proof of a platform limitation. The row already existed before drain, so 48.23 must distinguish stale test data/pre-clean failure from a real offline suppression defect.

## Unfired same-class sweep

The applied schema source is `20260718000001_core_schema.sql` plus `20260723_step_33_1_data_model_polish.sql`. Model serialization was checked for the active feature models and their DTOs:

| Path | Result |
|---|---|
| `core/data/models/cut_fill_record_model.dart` | Emits current `bcm_volume`, `lcm_volume`, `material_type`, `measured_at`; no legacy write key found. |
| `core/data/models/land_clearing_record_model.dart` | Emits current `plan_area`, `actual_area`, `method`, `cleared_at`; no legacy write key found. |
| `core/data/models/inventory_item_model.dart` | Emits current `name`, `quantity`, and optional current fields; no `item_name`/`quantity_on_hand` write key found. |
| `features/tracking/data/models/land_clearing_model.dart` | **Mismatch:** emits `method`, `clearing_method`, and `vegetation_type`; only `method` exists in the applied schema. → 48.19. |
| `features/tracking/data/models/inventory_item_model.dart` | **Mismatch:** emits `name`, `item_name`, `quantity`, and `quantity_on_hand`; only `name` and `quantity` exist. → 48.19. |
| `features/equipment_check/data/models/equipment_check_dto.dart` | **Mismatch:** emits `status` and `is_operational`; only `is_operational` exists. → 48.19. |
| `features/benchmark/data/models/benchmark_model.dart` | Payload fields match the documented Benchmark shape, but the table itself is absent. → 48.17. |
| `features/timeline/data/models/timeline_milestone_model.dart` | Payload targets the absent `timeline_milestones` table; column compatibility must be checked when 48.17 defines the migration. → 48.17. |
| `features/attendance/data/models/attendance_record_dto.dart`, `features/daily_log/data/models/daily_log_dto.dart` | Current keys match the core schema; no additional missing-column write mismatch found in this sweep. |

Read-side tolerant fallbacks for legacy keys are not themselves write defects. They may remain until the migration wave confirms the compatibility policy.

## Fix sequence and collision warnings

1. **48.17:** define and apply the two missing tables, RLS, generated types, and Doc 04 updates. This is the hard dependency for 48.18–48.20.
2. After 48.17, run **48.18, 48.19, and 48.20 in parallel only with file ownership separated**. 48.18 owns timeline/reporting datasource query names; 48.19 owns tracking models and equipment DTO write maps; 48.20 owns seed/fixture data and RLS test setup.
3. **48.21 and 48.22** can run in parallel with each other and with 48.18–48.20, but 48.22 must coordinate with 48.18 if both touch timeline/reporting screens or tests. 48.21 owns journey finder/semantics changes only.
4. **48.23** can run in parallel after 48.16, but must not edit the same attendance/daily-log journey assertions that 48.21 owns; it owns persistence and offline-integrity diagnosis.
5. **48.24** runs after all fix substeps 48.17–48.23 and is the local integration gate.
6. **48.25** runs only after 48.24, on the branch head, and decides whether 48.15 may re-run.

Potential collisions: `timeline_journey_test.dart` / timeline presentation files may be touched by 48.18, 48.21, and 48.22; `reporting_journey_test.dart` may be touched by 48.18 and 48.22; `inventory_item_model.dart` and `equipment_check_dto.dart` are exclusive to 48.19; `seed.sql` and RLS journey setup are exclusive to 48.20; offline/persistence tests are exclusive to 48.23. Do not run overlapping edits without rebasing or explicit file ownership.

## Escalations

No classification required an Opus escalation. The RLS result is explainable from the committed policy and the earlier 48.12 positive refusal evidence. The Web offline row remains a required high-risk diagnosis for 48.23, not an unverified classification.

## Next action

Run **`run substep 48.17` in a fresh chat**. It needs a scoped Supabase access token (`sbp_...`) supplied interactively when requested; the token must not be written to a file or printed. Active work remains assigned to 48.17, 48.18, 48.19, 48.20, 48.21, 48.22, and 48.23. None of those substeps is `N/A`.
