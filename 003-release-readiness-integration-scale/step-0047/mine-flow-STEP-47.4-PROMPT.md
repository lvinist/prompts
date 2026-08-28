# mine-flow — STEP-47.4: `go_router` 18, `googleapis` 17, `proj4dart` 3, `flutter_lints` 6 migration

> **How to run:** Tell your agent *"run substep 47.4"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.1 Pro High. Four unrelated migrations in one substep, one of which
> (`googleapis` 17) crosses two majors and touches the Google Drive surface.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`. Substep 47.1 swept the dependency
graph while fixing the AGP-9 Android build. This substep absorbs the remaining four major bumps that
are not bloc (47.3) and not file_picker (47.2):

| Package | From | To | Changelog highlights |
|---|---|---|---|
| `go_router` | 17.5.0 | 18.0.0 | *"Migrates to material_ui and cupertino_ui"*; min SDK Flutter 3.44 / Dart 3.12 |
| `googleapis` | 14.0.0 | 17.0.0 | 15.0.0 requires Dart ^3.7; **many APIs removed across 14→17** due to Google API security changes |
| `googleapis_auth` | 1.6.0 | 2.3.3 | 2.0.0 removed deprecated `RefreshFailedException` and the deprecated `auth.dart` library; browser flows removed from `auth_browser.dart` |
| `proj4dart` | 2.1.0 | 3.0.0 | Dart ≥3.0, dependency refresh (`mgrs_dart` 2→3 comes along) |
| `flutter_lints` | 5.0.0 | 6.0.0 | adds `strict_top_level_inference` and `unnecessary_underscores`; `lints` 6.1.0 |

They are grouped because each is small in this codebase, and because `flutter_lints` 6 must land
*last* — new lint rules will flag code the other three substeps just wrote.

**Affected files, from a planning-time grep (re-verify):**
- `go_router`: 21 files reference it; the router itself is `lib/app/router.dart` (`GoRouter(` at line 92)
- `googleapis` / `googleapis_auth`: **only** `lib/core/network/google_drive_service.dart` and
  `test/core/network/google_drive_service_test.dart` — it imports `googleapis/drive/v3.dart as drive`,
  `googleapis_auth/googleapis_auth.dart as auth`, and `googleapis_auth/auth_io.dart as auth_io`, and
  uses `drive.DriveApi`, `drive.File`, `drive.Media`, `drive.UploadOptions`,
  `drive.DetailedApiRequestError`
- `proj4dart` / `mgrs_dart`: **only** `lib/core/utils/crs_utils.dart` (`proj4.Projection.parse`,
  `proj4.ProjectionException`)
- `flutter_lints`: whole tree, via `analysis_options.yaml`

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md` — **Q3** is this substep's question
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — analyze must return to **0 issues**;
  `flutter test` baseline **442**
- 47.1's analyze log — your bucket
- `Code/mine-flow-app/lib/app/router.dart` and `lib/app/app.dart`
- `Code/mine-flow-app/lib/core/network/google_drive_service.dart` + its test
- `Code/mine-flow-app/lib/core/utils/crs_utils.dart`
- `Code/mine-flow-app/analysis_options.yaml`
- `Code/mine-flow-docs/architecture/11-interface-contracts.md` — the Drive service is an external
  interface surface; if its contract shifts, this doc and its named artifact are in scope
- `Code/mine-flow-docs/architecture/06-security-threat-model.md` — Drive uses **service-account**
  auth; `googleapis_auth` 2 removed browser flows, so confirm the auth path is unaffected
- **ADR-0003** (Google Drive for geospatial files), **ADR-0014** (persist CRS identifier) — the
  decisions these two files implement
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0006** (`go_router` v17 deep-link E2E
  unverified, still `open`)
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** router files, `google_drive_service.dart` + test, `crs_utils.dart` + test,
`analysis_options.yaml`, and any lint-6 fix anywhere in the tree.

**Does NOT touch:** `pubspec.yaml` (47.1), the file_picker migration (47.2), bloc migrations (47.3),
`android/**`, `ci.yml`, docs. If a lint-6 finding lands inside a file 47.2 or 47.3 owns and those
substeps have not merged yet, note it and let them fix it — otherwise you will collide.

**Do not "fix" RISK-0006 here.** Deep-link E2E evidence is STEP-48's. This substep only ensures
`go_router` 18 compiles and its unit/widget tests pass.

## Your task

### 1. `go_router` 18 — answer Q3 with evidence

The changelog line *"Migrates to material_ui and cupertino_ui"* is ambiguous about whether app code
must change. Determine it from the resolved package, not from guesswork:

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
flutter analyze lib/app test 2>&1 | grep -i "go_router\|router\|MaterialPage\|CupertinoPage"
grep -rn "MaterialPage\|CupertinoPage\|NoTransitionPage\|CustomTransitionPage\|pageBuilder" lib/ --include=*.dart
```

If page-type classes moved packages, fix the imports. If nothing breaks, state that explicitly with
the analyze output as proof — a clean answer to Q3 is a deliverable.

Also confirm the SDK floor: `go_router` 18 needs Flutter ≥3.44 / Dart ≥3.12. Local is Flutter 3.47.1
/ Dart 3.13.1 and CI pins 3.47.0 — both satisfy it. `pubspec.yaml` declares
`sdk: ">=3.12.0 <4.0.0"`, which is compatible; leave it alone unless the solver demands otherwise.

Then run the router's own tests plus anything that navigates:

```bash
flutter test test/app 2>&1 | tail -10
```

### 2. `googleapis` 14 → 17 + `googleapis_auth` 1 → 2 — the highest-risk item

Two changelog entries matter:

- `googleapis` 14.0.0 and 15.0.0 both **removed many APIs**. Confirm `drive/v3` still exists and that
  `DriveApi`, `File`, `Media`, `UploadOptions`, and `DetailedApiRequestError` all still carry the
  members this service uses. Check the resolved source:
  `$PUB_CACHE/hosted/pub.dev/googleapis-17.*/lib/drive/v3.dart`.
- `googleapis_auth` 2.0.0 **removed the deprecated `auth.dart` library** and
  `RefreshFailedException`, and dropped browser flows from `auth_browser.dart`. This service imports
  `googleapis_auth/googleapis_auth.dart` and `googleapis_auth/auth_io.dart` — verify both still
  exist and that the service-account path (`ServiceAccountCredentials` / `clientViaServiceAccount`)
  is intact. Per ADR-0003 + Doc 06, Drive access is service-account based, so the removed browser
  flows should be irrelevant — **confirm, don't assume**.

```bash
grep -rn "RefreshFailedException\|googleapis_auth/auth.dart\|clientViaUserConsent\|BrowserOAuth" lib/ test/
flutter test test/core/network/google_drive_service_test.dart
```

**Progress-reporting media upload:** `_createProgressMedia` builds a `drive.Media(byteStream(), total)`
to report upload progress. If `Media`'s constructor or `UploadOptions` changed shape, the progress
callback contract to `DataBucketUploadCubit` (which emits `UploadUploading(progress:…)`) must be
preserved exactly — the UI depends on it. If it cannot be preserved, **stop and report** rather than
silently degrading progress to a two-state spinner.

If any Drive-facing signature does change, that is an interface-contract change: record it for 47.8
(Doc 11 + possibly ADR-0003), and keep the test's assertions at least as strict.

**Credentials:** do not read, print, or exercise real Drive service-account credentials. The unit
test mocks `DriveApi` via `setApiForTesting`. NR-004/NR-005 (real Drive upload + large-file ceiling,
RISK-0017/0018) stay **deferred** — they need credentials nobody has.

### 3. `proj4dart` 3 + `mgrs_dart` 3

Both are "min Dart 3.0 + dependency refresh" releases with no documented API break. `crs_utils.dart`
uses `proj4.Projection.parse` and catches `proj4.ProjectionException` (ADR-0014's persisted CRS
identifier depends on this).

```bash
flutter test test/core/utils 2>&1 | tail -10
```

CRS transforms are numeric — a silent precision change would not fail to compile. If the existing
tests assert coordinates with tolerances, verify they still pass at the *same* tolerances. Do **not**
loosen a tolerance to get green; a widened tolerance is a hidden accuracy regression on survey data.
If numbers actually moved, stop and report with the before/after values.

### 4. `flutter_lints` 6 — do this LAST

New rules: `strict_top_level_inference` (top-level and static declarations need explicit types) and
`unnecessary_underscores`. Land this only after §1–§3 and, ideally, after 47.2 and 47.3 have merged,
so you fix each finding once.

```bash
flutter analyze 2>&1 | tee "$LOCALAPPDATA/Temp/step47-4-lints6.log"
flutter analyze 2>&1 | grep -cE "^\s+(info|warning|error)"
```

Fix findings by **adding the missing type annotation** or renaming the unnecessary underscore
parameter. Do **not** silence rules in `analysis_options.yaml` to reach zero. If a rule genuinely
does not fit this codebase, that is a project-convention decision for the user — surface it with the
count of affected sites and a recommendation, don't decide unilaterally.

`flutter analyze` must end at **0 issues**; that is a CI gate.

### 5. Verify and commit

```bash
flutter analyze
dart format --output=none --set-exit-if-changed lib/ test/
flutter test 2>&1 | tail -25
flutter build web --release 2>&1 | tail -15
dart run tool/check_supabase_contracts.dart
dart run tool/check_l10n_baseline.dart
```

The web build matters here specifically: `go_router` 18's material_ui/cupertino_ui migration and
`googleapis_auth` 2's browser-flow removal both land on the web surface, which is a shipped target
(GitHub Pages, per Doc 09).

```bash
git -C /d/AppDev/mine_flow/Code/mine-flow-app status --short   # stage only your files
git -C /d/AppDev/mine_flow/Code/mine-flow-app commit -m "refactor(STEP-47.4): go_router 18, googleapis 17, proj4dart 3, flutter_lints 6"
```

## Verification

- `flutter analyze` **0 issues** under `flutter_lints` 6, with no rule disabled to get there.
- `dart format` gate clean.
- `flutter test` ≥442 passing (report the real number; attribute any remaining failure to 47.2/47.3
  if those have not landed).
- `flutter build web --release` succeeds.
- Both contract guards pass.
- Drive service tests pass with unchanged (or stricter) assertions; the progress-callback contract is
  intact.
- CRS tests pass at their **original** tolerances.
- Q3 answered with analyze output as evidence.

Anything you cannot verify — say **Unverified** with the reason. In particular: do not claim the
Drive upload path works end-to-end. Only the mocked unit test ran; real Drive verification is
RISK-0017/0018 and stays deferred.

## Keeping the docs true (always)

Most of this is dependency-level and needs no doc change. Two exceptions to hand to **47.8**:

1. **If any `googleapis`/`googleapis_auth` change altered a Drive-facing signature or the progress
   contract**, that is an interface-contract change → `architecture/11-interface-contracts.md` and
   possibly ADR-0003. Report it; do not edit the docs here.
2. **If `flutter_lints` 6 required a convention decision** (a rule you believe should be disabled),
   that is a coding-standards change → `coding-standards/`. Surface it to the user via 47.8; do not
   change the standard on your own initiative.

Also record for 47.8: `go_router` 18 landed, so RISK-0006's wording ("go_router v17 deep-link E2E
unverified") needs its version reference refreshed — the risk itself stays **open** until STEP-48
supplies runtime evidence. Do not close it.

No secrets: no `.env` read, no service-account key touched, no remote Drive or Supabase state mutated.

## Definition of done

- [ ] Q3 answered with evidence: whether `go_router` 18 required app-code changes
- [ ] `googleapis` 17 / `googleapis_auth` 2 compile; `drive/v3` members verified against resolved source
- [ ] Service-account auth path confirmed intact; no `RefreshFailedException` or removed-library import
- [ ] Upload progress-callback contract to `DataBucketUploadCubit` preserved exactly
- [ ] `proj4dart` 3 / `mgrs_dart` 3 pass CRS tests at original tolerances (none loosened)
- [ ] `flutter_lints` 6 findings fixed by annotation/rename, **not** by disabling rules
- [ ] `flutter analyze` 0 issues; `dart format` clean; both contract guards pass
- [ ] `flutter test` ≥442; `flutter build web --release` succeeds
- [ ] Only this substep's files staged and committed
- [ ] Notes for 47.8 written (Doc 11/ADR-0003 impact, any lint convention question, RISK-0006 wording)

## Next

Update 47.4's status in the PLAN. When 47.2 + 47.3 + 47.4 are all done, the next action is **run
substep 47.5** — the first point where the whole tree must build and the Android APK is attempted.
