# STEP-59.2 FINDINGS

## Commitment

Implemented state restoration for daily log and equipment check forms, mirroring
the 59.1 landed pattern (CutFillFormScreen / Attendance reference). Committed on
`step-0059-os-restoration-forms` at `97cbeb5`.

## Design Compliance

- **59.0 §5 (hazard as-entered)**: Daily log hazard fields stored verbatim in the
  snapshot — validation re-runs on restore, never pre-fulfilled. An invalid
  combination (present + null severity) survives decode and is rejected by the
  submit validator exactly as fresh input would be.
- **59.0 §2 (reload-before-apply)**: CONTEXT fields (id, siteId, foremanId,
  status, approvedBy, createdAt, updatedAt, deletedAt) reloaded from repository;
  only ENTRY fields applied from snapshot. Identity gated on siteId + foremanId
  (+ date for daily log, encoded in the status gate).
- **59.0 §7 Q2 Option A**: Equipment check snapshot stores only per-item
  isPassed states + per-item remarks + form-level remarks. equipmentType,
  checkType, serialNumber are UI selection controls — NOT restored (reload fresh).
- **CF-017 (STEP-55.7)**: isPassed stays null until explicitly answered. A null
  answer is preserved as null on restore, never coerced to false.
- **Status-gated restore**: Only `dailylog-draft-v1` snapshots with
  `LogStatus.draft` decode successfully; submitted/approved → null (rejected).

## Snapshot Field Lists

### Daily Log (`dailylog-draft-v1`)
ENTRY fields snapped: `logDate`, `zoneId`, `weather`, `summary`, `notes`,
`hazard{state,severity,hazardNotes,correctiveAction}`.
CONTEXT fields NOT snapped: `id`, `siteId`, `foremanId`, `status`,
`approvedBy`, `createdAt`, `updatedAt`, `deletedAt`.

### Equipment Check (`eqcheck-draft-v1`)
ENTRY fields snapped: per-item `isPassed` (bool? three-state), per-item
`remarks`, form-level `remarks`.
CONTEXT fields NOT snapped: `equipmentType`, `checkType`, `serialNumber`,
`checkTime`, `isSubmitting`, `successMessage`, `siteId`, `foremanId`.

## Files Changed

### Created (4)
- `lib/features/daily_log/presentation/bloc/daily_log_draft_restoration.dart`
- `lib/features/equipment_check/presentation/bloc/equipment_check_draft_restoration.dart`
- `test/features/daily_log/presentation/daily_log_draft_restoration_test.dart`
- `test/features/equipment_check/presentation/equipment_check_draft_restoration_test.dart`

### Modified (6)
- `lib/features/daily_log/presentation/bloc/daily_log_event.dart` — added `DailyLogFormRestoreRequested`
- `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart` — registered handler + `_onRestoreRequested`
- `lib/features/daily_log/presentation/pages/daily_log_form_sheet.dart` — `RestorationMixin`, `RestorableStringN`, `restoreState`, `_restoreIfReady`, dispose, widget params
- `lib/features/equipment_check/presentation/bloc/equipment_check_event.dart` — added `EquipmentCheckFormRestoreRequested`
- `lib/features/equipment_check/presentation/bloc/equipment_check_bloc.dart` — registered handler + `_onRestoreRequested`
- `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart` — `RestorationMixin`, `RestorableStringN`, `restoreState`, `_restoreIfReady`, dispose, widget params

## Tests

| Suite | Tests | Status |
|-------|-------|--------|
| `daily_log_draft_restoration_test.dart` | 14 | All pass |
| `equipment_check_draft_restoration_test.dart` | 16 | All pass |
| Existing daily_log + equipment_check tests | 17 | No regressions |
| **Total** | **47** | **All green** |

Covers: roundtrip equality, version-mismatch fallback (v2 → null), malformed
JSON → null, null snapshot → null, siteId/foremanId mismatch → null, status-gated
restore (submitted/approved → null), hazard-validation-reruns-on-restore (invalid
hazard preserved as-entered), CF-017 null-preservation + mixed states + false
preservation, missing fields → null, malformed date → null, apply() preserves
CONTEXT fields.

## Gates

- `dart analyze` on all touched files: **No errors** (11 info-only lints in test files: prefer_const_constructors, no_leading_underscores_for_local_identifiers — non-blocking style suggestions).
- `flutter format`: not run (touched files follow existing style).
- Existing test suites: no regressions.
- Branch: `step-0059-os-restoration-forms` (on `97c9866` base).
- Commit: `97cbeb5` (no push).

## Deviations

- Used `dart analyze` on individual files instead of full `flutter analyze` for iteration speed.
- Widget-level `restartAndRestore()` test not included — the unit test suites cover encode/decode/apply comprehensively; the `RestorationMixin` wiring mirrors the CutFill/Attendance pattern exactly. Adding a full widget test would require mocking `DailyLogRepository`/`EquipmentCheckRepository` + `ZoneRepository`, which is beyond the focused scope.
