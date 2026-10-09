# STEP-55.5 Findings — Crew Attendance Workflow Rebuild

**Date:** 2026-09-11 (Residual fix: 2026-09-21)
**STEP status:** Done
**App branch:** ``step-0055-cohesive-ui-rebuild`` at ``02603c1``
**Docs branch:** ``step-0055-cohesive-ui-rebuild``
**Prompts revision:** ``main``

## Pre-flight

- Resumed from existing STEP-55.5 implementation already on
  ``step-0055-cohesive-ui-rebuild``. Prior substeps (55.0–55.4) are all
  complete with passing gates.
- Worktrees were clean for app/docs at session start; prompts on ``main``.
- Baseline from 55.4: format clean, analyzer 0 issues, all tests passing.

## Delivered

### 1. AttendanceCrewDraft — nullable roster draft model

- Form-only entity with nullable ``status``; a crew member without a
  persisted record for the selected date starts **unset** (null), never
  pre-marked present (spec §4.4 item 1 / FC-54.5 contract).
- ``isUnset``, ``requiresReason`` (Izin/Sakit only), ``trimmedRemarks``,
  ``isInvalidForSubmit`` computed properties.
- ``copyWith(clearStatus:, clearRemarks:)`` sentinels close the
  ``remarks ?? existing.remarks`` keep-old bug (spec §4.4 item 5).
- ``toValidatedRecord(...)`` materializes into a non-null-status
  AttendanceRecord; refuses an unset row with StateError.

### 2. AttendanceRecord.copyWith — clearRemarks sentinel

- Added ``clearRemarks: false`` parameter so an explicit null clearing
  intent can be distinguished from a keep-old copy (spec §4.4 item 5).

### 3. AttendanceFormBloc / Event / State

- Owns the batch sheet's editable draft layer.
- AttendanceFormStarted loads roster + persisted records; crew without a
  record start unset.
- AttendanceFormStatusSelected, AttendanceFormRemarksChanged (with clear:
  flag), AttendanceFormBulkMarkPresent (marks only unset rows),
  AttendanceFormDateChanged (reloads roster), AttendanceFormSubmitted.
- Submit validates every row before saving; firstInvalidUserId +
  validationError surface the first offender for focus/scroll.
- AttendanceSyncState (queued/syncing/failed/synced) derived from the
  shared sync queue box via AttendanceFormQueueChanged; attribution by
  record id -> user id mapping.
- AttendanceFormRetrySyncRequested re-enqueues the failed item and drains
  the queue via SyncQueueManager.processQueue(isManual: true).

### 4. AttendanceCrewCard widget

- Real name primary, role/position secondary; UUID never appears.
- Four inline icon+text choices in fixed order (Izin=leave, Sakit=sick,
  Alpa=absent, Masuk=present) with 48dp min-height targets.
- Required trimmed reason field reveals only for Izin/Sakit; explicit
  clear X dispatches AttendanceFormRemarksChanged(clear: true).
- Compact per-record sync indicator row with labelled retry (Coba lagi),
  separate from attendance choice (spec §4.4 item 6 / FC-54.5-007).

### 5. AttendanceFormSheet — route-backed batch sheet

- Durable identity: /teams/attendance/form?date=YYYY-MM-DD&siteId=<id>
- AppResponsiveSheet D1/D2 geometry (>=800dp right, <800dp bottom).
- D4 dirty guard wired to isDirty/isSubmitting.
- Header row: date + AppCalendarDialog left, Tandai Semua Masuk right;
  Wrap preserves date-first order and 48dp targets on narrow.
- Confirmation dialog before discarding a non-empty reason.
- Simpan Absensi (N Kru) footer, disabled during submission, above IME.
- Focus/scroll to first invalid row on failed submit.
- No D7 inspector; contextual report dialog seeded by date/site.

### 6. AttendanceScreen updates

- FABs replaced with FButton actions.
- Contextual report seeded by selected date/site.
- Popover-first status filter via AppFilterPopover.
- Date navigation uses AppCalendarDialog.showSingle.
- Cards read-only; no D7 inspector.

### 7. Router — attendance-form route

- GoRoute(path: form, name: attendance-form) added under attendance branch
  with CustomTransitionPage(opaque: false).

### 8. Localization

- All new attendance UI strings added to app_id.arb and app_en.arb;
  0 hardcoded strings in non-exempt files.

## Traceability

| Finding | Implementation | Status |
|:---|:---|:---|
| FC-54.5-001: Route-backed batch sheet | /teams/attendance/form?date=&siteId= | Satisfied |
| FC-54.5-002: Never pre-mark fresh roster present | AttendanceCrewDraft null status | Satisfied |
| FC-54.5-003: Persisted entity status non-null | toValidatedRecord StateError guard | Satisfied |
| FC-54.5-004: Bulk action changes only unset rows | _onBulkMarkPresent skips set rows | Satisfied |
| FC-54.5-005: Four inline choices fixed order | Izin/Sakit/Alpa/Masuk, 48dp, icon+text | Satisfied |
| FC-54.5-006: Reason required/trimmed Izin/Sakit only | requiresReason + _ReasonField | Satisfied |
| FC-54.5-007: Per-record sync truth | AttendanceSyncState, queue subscription | Satisfied |
| FC-54.5-008: Explicit clearing + confirmation | copyWith(clearRemarks:), confirm dialog | Satisfied |
| FC-54.5-009: First-invalid focus/scroll | firstInvalidUserId + _focusFirstInvalid | Satisfied |
| FC-54.5-010: Batch count / no double-submit | crewCount footer, isSubmitting guard | Satisfied |
| FC-54.5-011: Error retention on save fail | saveError emitted, drafts unchanged | Satisfied |
| FC-54.5-012: Dirty dismissal guard | isDirty/isBusy -> AppDismissController | Satisfied |
| FC-54.5-013: Contextual report, no inspector | showAppContextualReportDialog | Satisfied |

## Verification

- flutter test (attendance_crew_draft + attendance/presentation): **31 passed**
- flutter test (model/repository/datasource/screen/integration): **29 passed**
- dart format --output=none --set-exit-if-changed . — **Passed** (0 changed)
- flutter analyze — **Passed** (0 issues, 65.5s)
- dart run tool/check_l10n_baseline.dart — **Passed** (18 non-exempt, 0 errors)
- dart run tool/check_supabase_contracts.dart — **Passed**

## Unverified

- One bounded Web/Pixel_6a visual inspection: **Unverified** — requires
  authenticated runtime capture; to be consolidated in 55.11.
- impeccable executable not on PATH in this environment; no init/document/
  extract run.

## Changed files

- lib/features/attendance/domain/entities/attendance_crew_draft.dart (new)
- lib/features/attendance/domain/entities/attendance_record.dart
- lib/features/attendance/data/models/attendance_record_dto.dart
- lib/features/attendance/presentation/bloc/attendance_form_bloc.dart (new)
- lib/features/attendance/presentation/bloc/attendance_form_event.dart (new)
- lib/features/attendance/presentation/bloc/attendance_form_state.dart (new)
- lib/features/attendance/presentation/bloc/attendance_state.dart
- lib/features/attendance/presentation/pages/attendance_form_page.dart (deleted)
- lib/features/attendance/presentation/pages/attendance_form_sheet.dart (new)
- lib/features/attendance/presentation/pages/attendance_screen.dart
- lib/features/attendance/presentation/widgets/attendance_crew_card.dart (new)
- lib/features/attendance/presentation/widgets/attendance_summary_card.dart
- lib/features/attendance/presentation/widgets/crew_roster_item.dart
- lib/features/attendance/presentation/widgets/status_toggle_chips.dart
- lib/app/router.dart
- lib/l10n/app_id.arb, app_en.arb, generated localization files
- test/features/attendance/presentation/attendance_form_bloc_test.dart (new)
- test/features/attendance/presentation/attendance_form_sheet_test.dart (new)
- test/unit/attendance_crew_draft_test.dart (new)
- test/unit/attendance_model_test.dart
- test/widget/attendance_form_page_test.dart (deleted)
- test/widget/attendance_screen_test.dart
- tool/check_l10n_baseline.dart
- Upcoming Prompts/mine-flow-STEP-55.5-FINDINGS.md (this file)

## Docs / risk impact

No architecture doc, ADR, or risk register change required. The attendance
domain contract, entity structure, and sync approach remain as established
in prior STEPs; this substep implements the presentation layer only.

## Next handoff

Run **substep 55.6** in a fresh chat.
**Assigned model: Hermes/Claude Opus 4.8.**
55.6 adds the Daily Log role-aware workflow and tabbed review queue.

---

## Residual fix (55.5) — 2026-09-21

### Residual Scope Delivered

1. **Material `FloatingActionButton` Purge on List Screen (`attendance_screen.dart`)**:
   - Replaced both Material `FloatingActionButton` and `FloatingActionButton.extended` with ForUI `FButton`s in a `Positioned` overlay inside `SafeArea`, eliminating all Material FABs from the attendance feature.
   - Report action: `FButton(variant: FButtonVariant.outline)` wrapped in `Semantics(label: 'Buat Laporan Kehadiran', button: true)` with `LucideIcons.fileText` prefix and `l10n.generateReport` label, maintaining contextual report seeding by selected date/site (`_openContextualReport(state)`).
   - Input action: `FButton(variant: FButtonVariant.primary)` wrapped in `Semantics(label: l10n.attendanceFormTitle, button: true)` with `LucideIcons.userPlus` prefix and `l10n.attendanceFormTitle` label, pushing the route-backed attendance form sheet while keeping the list mounted beneath (`_openAttendanceForm(state)`).
   - Preserved disabled gating when attendance state is not `AttendanceLoaded` (`onPress: state is AttendanceLoaded ? ... : null`).
   - Enforced 48dp minimum touch target height via enclosing `SizedBox(height: 48)`.
   - Pinned with widget tests in `test/widget/attendance_screen_test.dart` asserting zero `FloatingActionButton`, button rendering, 48dp touch targets, disabled gating, and sheet navigation.

2. **Mechanical Coverage & Runtime Audit Deferral Note**:
   - `FC-54.5-004,013` runtime audit remains **Unverified at this lane** (deferred to 55.11 multiplatform verification; no runtime visual capture fabricated).
   - Mechanical widget coverage expanded in `test/widget/attendance_screen_test.dart`:
     - FAB purge verification (0 `FloatingActionButton` on screen).
     - Action buttons enabled when `AttendanceLoaded`, disabled when loading/initial.
     - Contextual report dialog seeded with selected date/site (`AppContextualReportDialog`).
     - Route navigation to attendance form sheet (`/teams/attendance/form`).
     - Calendar dialog single-date picker invocation (`AppCalendarDialog.showSingle`).
     - Status filter popover cycle (`AppFilterPopover`) with preview, radio selection, and applied roster filtering.
     - 2.0x text scaling renders without overflow or exceptions.
     - Dark theme (`FTheme.neutral.dark.touch`) renders cleanly without errors.

3. **Status Flip and Findings Hygiene**:
   - Reconciled findings with post-55.11 state and flipped index row 55.5 to `Done` with residual note.

### Tests & Verification

- `flutter test test/widget/attendance_screen_test.dart test/features/attendance/ test/unit/attendance_crew_draft_test.dart test/unit/attendance_model_test.dart` — **51 passed** (8 attendance_screen, 11 attendance_crew_draft, 12 attendance_form_bloc, 8 attendance_form_sheet, 12 attendance_model).
- `dart format --output=none --set-exit-if-changed lib/features/attendance/presentation/pages/attendance_screen.dart test/widget/attendance_screen_test.dart` — **Passed** (0 changed files).
- `flutter analyze` — **Passed** (0 issues found, ran in 5.6s).
- `dart run tool/check_l10n_baseline.dart` — **Passed** (22 non-exempt files scanned, 0 new hardcoded strings).
- `dart run tool/check_supabase_contracts.dart` — **Passed** (Supabase contracts verified).

### Changed Files

- `Code/mine-flow-app/lib/features/attendance/presentation/pages/attendance_screen.dart` (committed at `02603c1`)
- `Code/mine-flow-app/test/widget/attendance_screen_test.dart` (committed at `02603c1`)
- `Upcoming Prompts/mine-flow-STEP-55.5-FINDINGS.md`
- `prompts/STEP-index.md`

