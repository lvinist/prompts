# mine-flow — STEP-47.2: `file_picker` 12 federated-API migration

> **How to run:** Tell your agent *"run substep 47.2"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.1 Pro High — this is a real API migration with a behavioural constraint to
> preserve (CF-078's memory cap), not a mechanical rename.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`. Substep 47.1 upgraded
`file_picker` 11.0.3 → 12.1.x because version 11 applies the Kotlin Gradle Plugin unconditionally
and AGP 9 refuses to build it. Version 12 is a **federated rewrite** with breaking API changes, so
the one call site in the app no longer compiles.

Exactly one file uses the API: `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
(the Data Bucket upload screen, S21 in STEP-46's screen inventory). No test file references
`file_picker` today — part of this substep's job is to change that.

### What version 12 changed

| v11 | v12 |
|---|---|
| `FilePicker.pickFiles(...)` → `Future<FilePickerResult?>` with `.files` / `.count` | `pickFiles(...)` → `Future<List<PlatformFile>>` (empty list, never null); **`FilePickerResult` is gone** |
| single selection via `allowMultiple: false` | dedicated `FilePicker.pickFile(...)` → `Future<PlatformFile?>`; `allowMultiple` deprecated and now defaults to `true` |
| `PlatformFile.bytes` (`Uint8List?`, populated by `withData: true`) | `Future<Uint8List> PlatformFile.readAsBytes()` / `Stream<Uint8List> readAsByteStream()`; `withData` deprecated |
| `PlatformFile.size` (`int`) | `Future<int> PlatformFile.length()` — **now async** |
| `PlatformFile.extension` | still present (restored in 12.1.0), dot-less, derived from `name` |
| `PlatformFile.path` | still present; `null` when the file is not on local disk |

`PlatformFile` is now `abstract base class` from `file_picker_platform_interface`, exposing:
`name`, `extension`, `uri`, `path`, `xFile`, `length()`, `readAsBytes()`, `readAsByteStream()`.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md` — Q2 is this substep's decision
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — baseline test count you must not regress
- `Code/mine-flow-app/lib/features/data_bucket/presentation/pages/upload_file_page.dart` — the only call site
- `Code/mine-flow-app/lib/features/data_bucket/presentation/bloc/data_bucket_upload_cubit.dart` —
  `uploadFile({required bytes, required fileName, required mimeType, zoneId, acquisitionDate, notes, uploadedBy})`
- `Code/mine-flow-app/test/features/data_bucket/presentation/bloc/data_bucket_upload_cubit_test.dart` — the existing cubit test
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — test tiers and the mocking boundary
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the upload screen's UI is ForUI/Zinc;
  keep tokens and Indonesian copy exactly as they are
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** `upload_file_page.dart` and its tests.

**Does NOT touch:** `pubspec.yaml` (47.1 owns it), bloc/`bloc_test` migrations (47.3), `go_router`
/`googleapis`/`proj4dart`/lints (47.4), `android/**`, `ci.yml`, docs. If `flutter analyze` still
reports errors outside this file when you finish, that is expected — they belong to 47.3/47.4.

## Your task

### 1. Understand the behaviour you must preserve

The current `_pickFile()` calls `pickFiles` **twice** on purpose. STEP-46 finding **CF-078** put a
50 MB cap (`_kMaxFileSizeMb = 50`) on uploads and enforced it *before* pulling the file into memory:

1. first pick with `withData: false` — metadata only, then compare `size` against `_kMaxFileSizeBytes`
   and bail with the Indonesian toast *"File terlalu besar (maks 50 MB)."*
2. second pick with `withData: true` — only reached if the size check passed, to get the bytes

That double-pick is a v11 workaround: v11 had no way to read bytes lazily, so avoiding the memory hit
meant asking the user to pick twice. **v12 removes the need**: `length()` reads the size without
loading content, and `readAsBytes()` fetches bytes on demand.

**Q2 is settled — collapse to a single pick.** One `pickFile()` call, then `await length()` for the
cap check, then `await readAsBytes()` only if it passes. This preserves CF-078's real intent (never
load an oversized file into memory) and fixes a UX wart (the user picking the same file twice). The
cap value, the message text, and the destructive-colour toast must stay byte-identical.

### 2. Migrate the picker call

Replace the two-call `_pickFile()` with something equivalent to:

- `final file = await FilePicker.pickFile(type: FileType.custom, allowedExtensions: const [...]);`
  — keep the existing 10-extension list (`shp`, `tiff`, `tif`, `dxf`, `dwg`, `csv`, `kml`, `kmz`,
  `gpx`, `pdf`) exactly as it is.
- `if (file == null) return;` — v12 returns `null` for a cancelled single pick, not an empty wrapper.
- `final size = await file.length();` then the existing `size > _kMaxFileSizeBytes` guard, unchanged
  in message and styling.
- `final bytes = await file.readAsBytes();` only after the guard passes.
- `setState(() { _selectedFile = file; _fileBytes = bytes; _selectedFileSize = size; });`

Do **not** pass the deprecated `withData` / `allowMultiple` — under `flutter_lints` 6 they will
produce deprecation output, and they no longer do anything useful.

**`mounted` discipline:** you are adding `await`s inside a `State` method. Every `BuildContext` use
after an `await` needs a `if (!mounted) return;` guard. The file already does this in `_submitUpload`
— match that pattern. `flutter_lints` 6 (`use_build_context_synchronously`) will flag misses, and
47.4 must not have to clean up after this substep.

### 3. Fix the two synchronous `.size` reads in the UI

`PlatformFile.size` no longer exists. Lines ~446–448 render the picked file's size in the card:

```dart
if (_selectedFile!.size > 0)
  Text(_formatSize(_selectedFile!.size), …)
```

You cannot `await` in `build`. Store the size in state when picking (`_selectedFileSize`, set in
step 2) and render from that. Do **not** introduce a `FutureBuilder` here — the value is already
known at pick time, and a rebuild-triggered re-read would be a needless I/O call on every frame.

`_formatSize` itself needs no change.

### 4. Keep `mimeType` derivation working

`_submitUpload` derives the MIME type from `_selectedFile!.extension`. That getter survives in v12
(dot-less, parsed from `name` by `package:path`), so the `_mimeTypeForExtension` call keeps working —
**but confirm it against the resolved source** rather than trusting this prompt:
`$PUB_CACHE/hosted/pub.dev/file_picker_platform_interface-*/lib/src/platform_file.dart`.

Note one subtlety worth a code comment: v12's `extension` uses `package:path`'s rules, so a dotfile
like `.gitignore` yields `null` rather than `gitignore`. For this screen's 10 allowed geospatial
extensions the behaviour is identical, but say so in a comment so a future reader doesn't wonder.

### 5. Check the `List<int>` / `Uint8List` seam

`_fileBytes` is declared `List<int>?`; `readAsBytes()` returns `Uint8List` (which *is* a `List<int>`,
so it assigns fine). Verify what `DataBucketUploadCubit.uploadFile({required bytes, …})` and
`GoogleDriveService.uploadFile` actually expect. If either wants `Uint8List`, prefer tightening
`_fileBytes` to `Uint8List?` over inserting a copy — but **do not change the cubit's signature**;
that would widen this substep into 47.3's territory and into the Drive-service surface.

### 6. Write the tests

There is currently **no test** covering the picker path — CF-078's cap is unprotected. Add coverage:

- **Cubit test** (extend `test/features/data_bucket/presentation/bloc/data_bucket_upload_cubit_test.dart`):
  keep it green after any `Uint8List` tightening. Do not weaken existing assertions.
- **New widget test** for the upload page's picker path. Mock at the `FilePickerPlatform.instance`
  boundary (per Doc 12's mocking strategy) with a fake `PlatformFile` subclass — `PlatformFile` is
  `abstract base`, so implement `name`, `uri`, `xFile`, `length()`, `readAsBytes()`,
  `readAsByteStream()`. Cover:
  - happy path — a 1 MB `.shp` is accepted, name + formatted size render, submit becomes enabled
  - **boundary** — exactly `_kMaxFileSizeBytes` is accepted; one byte over is rejected with
    *"File terlalu besar (maks 50 MB)."* and `_selectedFile` stays null
  - cancellation — `pickFile` returns `null`, nothing changes, no exception
  - `readAsBytes()` throwing — the existing "Gagal membaca file" error path still fires

**RISK-0009 applies:** if a test needs to reach a text field, find `EditableText`, never `TextField`
(flutter/flutter#191095 semantics regression on Flutter 3.47). If a `FTextField.suffixBuilder`
Material widget is in the tree, the test needs a `flutter_localizations` scope.

### 7. Verify and commit

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
flutter analyze lib/features/data_bucket test/features/data_bucket
dart format lib/features/data_bucket test/features/data_bucket
flutter test test/features/data_bucket
```

Then the full suite, understanding it may still fail on 47.3/47.4's files:

```bash
flutter test 2>&1 | tail -20
```

Report your own file's results separately from the tree-wide state. Saying "tests pass" while the
suite cannot compile would be exactly the dishonesty this STEP exists to correct.

```bash
git -C /d/AppDev/mine_flow/Code/mine-flow-app add lib/features/data_bucket test/features/data_bucket
git -C /d/AppDev/mine_flow/Code/mine-flow-app commit -m "refactor(STEP-47.2): migrate upload page to file_picker 12 federated API; single-pick size cap"
```

## Verification

- `flutter analyze` reports **0 issues for `lib/features/data_bucket` and `test/features/data_bucket`**.
- `flutter test test/features/data_bucket` fully passes.
- The 50 MB cap is enforced by a test at the boundary and one byte over it.
- The UI still shows the picked file's name and formatted size.
- Indonesian strings and ForUI tokens are unchanged (compare with `git diff`).
- No deprecated `withData` / `allowMultiple` / `FilePickerResult` reference remains:
  `grep -rn "FilePickerResult\|withData\|allowMultiple" lib/ test/` returns nothing.

## Keeping the docs true (always)

This is an implementation-level dependency migration; it changes no architecture decision, so no
`architecture/*` doc edit and no ADR here.

Two things to hand to 47.8 in your status note:
1. The upload flow now asks the user to pick **once** instead of twice. That is a user-visible
   behaviour change to a STEP-46 remediation (CF-078). It needs a line in the STEP record so the
   change is not mistaken later for a regression against the audit.
2. If you tightened `_fileBytes` to `Uint8List?`, say so — it slightly narrows the internal contract
   between the page and the cubit.

No secrets: this substep touches no credential and no `.env`.

## Definition of done

- [ ] `upload_file_page.dart` compiles against `file_picker` 12 with no deprecated parameters
- [ ] Single `pickFile()` call; size checked via `length()` before `readAsBytes()`
- [ ] 50 MB cap, its Indonesian message, and the destructive-colour toast unchanged
- [ ] Synchronous `.size` UI reads replaced by state captured at pick time (no `FutureBuilder`)
- [ ] `mounted` guards after every new `await` preceding a `BuildContext` use
- [ ] `mimeType` derivation verified against the resolved `platform_file.dart`, with a comment on
      `package:path` extension semantics
- [ ] New widget test covers happy path, exact-cap boundary, over-cap rejection, cancellation, and
      read failure; `EditableText` finders used if any field is touched
- [ ] Existing cubit test still green, with no weakened assertions
- [ ] `flutter analyze` 0 issues for the touched directories; `dart format` clean
- [ ] Nothing outside `lib/features/data_bucket` + `test/features/data_bucket` modified
- [ ] Committed on `step-0047-android-build-chain`
- [ ] Notes for 47.8 written (single-pick UX change; any `Uint8List` tightening)

## Next

Update 47.2's status in the PLAN. If 47.3 and 47.4 are not yet done, they run next (fresh chat each,
parallel is fine). Once 47.2 + 47.3 + 47.4 are all done, the next action is **run substep 47.5**.
