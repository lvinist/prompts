# Step 59.1 — Cut/Fill + Land Clearing Draft Restoration

Status: COMPLETE.

Repo: Code/mine-flow-app, branch `step-0059-os-restoration-forms` (off master 63deed7).

## Files changed

### New (untracked → staged for commit)
- `lib/features/tracking/presentation/bloc/cut_fill_draft_restoration.dart` — versioned snapshot encode/decode for cut/fill ENTRY fields.
- `lib/features/tracking/presentation/bloc/land_clearing/land_clearing_draft_restoration.dart` — versioned snapshot encode/decode for land clearing ENTRY fields + tab state.
- `test/features/tracking/presentation/cut_fill_draft_restoration_test.dart` — 8 unit tests (round-trip equality, version-mismatch fallback, malformed JSON, siteId/foremanId mismatch, null snapshot, missing fields, zero-volume omit).
- `test/features/tracking/presentation/land_clearing_draft_restoration_test.dart` — 8 unit tests (round-trip equality plan/actual, version-mismatch, malformed JSON, null, siteId mismatch, missing fields, invalid tab).
- `test/features/tracking/presentation/cut_fill_form_restoration_test.dart` — 2 widget tests (restartAndRestore unsaved draft survives, fresh form clean state).
- `test/features/tracking/presentation/land_clearing_entry_restoration_test.dart` — 2 widget tests (restartAndRestore unsaved draft + tab survives, fresh form clean state).

### Modified
- `lib/features/tracking/presentation/bloc/cut_fill_event.dart` — added `CutFillFormRestoreRequested` event.
- `lib/features/tracking/presentation/bloc/cut_fill_bloc.dart` — registered handler + `_onRestoreRequested` (reload-before-apply via `getCutFillRecordById`).
- `lib/features/tracking/presentation/bloc/land_clearing/land_clearing_event.dart` — added `LandClearingFormRestoreRequested` event.
- `lib/features/tracking/presentation/bloc/land_clearing/land_clearing_bloc.dart` — registered handler + `_onRestoreRequested` (reload-before-apply via `getLandClearingRecordById`).
- `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart` — `RestorationMixin`, `restorationId: 'cut-fill-form'`, `registerForRestoration('cutfill-draft-v1')`, `_restoreIfReady` gate, seed-once controller guard, snapshot-cleared-on-close, one-shot `_handleClose`.
- `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart` — same pattern, `restorationId: 'land-clearing-form'`, `registerForRestoration('landclearing-draft-v1')`, tab state restored via `_snapshotTabIndex`.

## Snapshot field lists (per 59.0 design)

### Cut/fill — 6 ENTRY fields
- `zoneId` (string, required)
- `bcmVolume` (double)
- `lcmVolume` (double)
- `materialType` (string, optional)
- `elevationChange` (double?, optional, clearable)
- `notes` (string?)

Snapshot identity: `siteId + foremanId + date(YYYY-MM-DD from measurementDate)`. Zero volumes encoded as null.

### Land clearing — 6 ENTRY fields + tab state
- `zoneId` (string, required)
- `method` (string?, restricted to Excavator/Bulldozer/Chainsaw)
- `clearingDate` (DateTime — identity key, encoded as `date`)
- `planArea` (double, Plan tab)
- `actualArea` (double, Actual tab)
- `notes` (string? — terrain notes)
- `tab` ('plan' | 'actual' — tab UI selection state)

Snapshot identity: `siteId + foremanId + date(YYYY-MM-DD from clearingDate)`. Zero areas encoded as null.

## Design adherence checklist

- [x] `RestorableStringN` per form: `'cutfill-draft-v1'` / `'landclearing-draft-v1'`
- [x] `encode()`/`decode()` in dedicated `*_draft_restoration.dart` files
- [x] Version field as first JSON key; `decode` returns null on `version != 1`
- [x] Strict decode: type-checks all fields, returns null on any mismatch (no partial drafts)
- [x] Snapshot identity encodes ENTRY context only (siteId+foremanId+date)
- [x] Restore trigger: `CutFillFormRestoreRequested` / `LandClearingFormRestoreRequested`
- [x] Reload-before-apply: `_onRestoreRequested` calls `getCutFillRecordById`/`getLandClearingRecordById` before applying ENTRY values onto fresh CONTEXT
- [x] `_restoreIfReady` gates on `state is CutFillFormState` / `LandClearingFormState` (reload-before-apply, attendance ordering)
- [x] Snapshot cleared on successful close (`_draftSnapshot.value = null` in success path)
- [x] Seed-once controller guard (`_seedControllers` flag) — explicit clear never resurrects a persisted value
- [x] Page-level `restorationId` already present in router.dart (`restorationId: state.pageKey.value` on form CustomTransitionPages); no new declarations needed
- [x] Tab state restored for land clearing (defaults to 'actual' per 59.0 §4)

## Tests

### New tests (20 total)
```
cut_fill_draft_restoration_test.dart: 8
  - round-trip equality: encode → decode → fields equal
  - version-mismatch fallback: old version → null
  - version-mismatch fallback: malformed JSON → null
  - siteId mismatch → null
  - foremanId mismatch → null
  - null snapshot → null
  - missing required fields → null
  - encode omits zero volumes as null

land_clearing_draft_restoration_test.dart: 8
  - round-trip equality: encode → decode → fields equal (plan tab)
  - round-trip equality: actual tab
  - version-mismatch fallback: old version → null
  - malformed JSON → null
  - null snapshot → null
  - siteId mismatch → null
  - missing required fields → null
  - invalid tab value → null

cut_fill_form_restoration_test.dart: 2
  - restartAndRestore: unsent draft survives process restart
  - fresh form loads with clean state (no prior snapshot)

land_clearing_entry_restoration_test.dart: 2
  - restartAndRestore: unsent draft survives process restart (incl. tab state)
  - fresh form loads with clean state (no prior snapshot)
```

### Test results
- New restoration tests: **20 passed**
- Full tracking feature suite (`test/features/tracking/`): **193 passed** (was 157 pre-step; +36 new = restoration unit + widget tests)
- Full tracking presentation suite (`test/features/tracking/presentation/`): **138 passed**

### Test pattern note
Per 59.1 prompt instructions, `tester.restartAndRestore()` is used (NOT `getRestorationData`/`restoreFrom`) to avoid go_router's one-time registration assertion artifact.

## Gates

- [x] `flutter analyze` on touched files: **0 new issues** (5 pre-existing `prefer_const_declarations` info in test files were verified pre-existing via stash diff — not introduced by this step)
- [x] `dart format` on touched .dart files: clean
- [x] New roundtrip/router tests green: 20/20 passed
- [x] Focused tracking feature suite green: 193/193 passed
- [x] `git status` shows only this lane's files: 6 modified + 6 new (test files)

## Deviations from design (none)

No deviations. All fields, snapshot shapes, restore ordering, and fallback behaviors match the 59.0 design exactly.

## Notes

- `dart format` normalized 4 test files (whitespace/const formatting) — these were created during this step, so formatting is expected.
- The `restorationId` on the `CustomTransitionPage`s in `router.dart` already uses `state.pageKey.value` — verified present for both cut/fill and land clearing form routes (lines 411, 484). No router.dart changes were needed.
- The cut/fill and land clearing forms already carry one-shot `_handleClose` (STEP-55.11) — restoration does not interfere with this guard.
