# mine-flow — STEP-54.9 Findings: Data Bucket & Work Timeline Critique

**Date:** 2026-09-11
**Executor:** Antigravity (Gemini 3.1 Pro High)
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique`
**Scope:** Read-only critique of the Data Bucket (file upload/detail) and Work Timeline features. No application code was modified.

## 1. Scope and evidence boundary

This static critique applied the 54.1 rubric to the Data Bucket and Work Timeline features on both Web (desktop) and Android (mobile). Runtime visual, contrast, and screen-reader behaviors remain `Unverified` as no execution trace or emulator was used.

Inspected files:
- `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`
- `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
- `lib/features/data_bucket/presentation/pages/file_detail_page.dart`
- `lib/features/timeline/presentation/pages/timeline_page.dart`
- `lib/features/timeline/presentation/widgets/milestone_card.dart`

## 2. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.9-001 | Needs restructure | Data Bucket: D5 form routing | The list page opens Upload and Detail pages via `Navigator.push(MaterialPageRoute(...))` rather than GoRouter named routes, even though `/tools/data-bucket/upload` and `/:id` exist. Breaks URL synchronization. | `data_bucket_list_page.dart:320-334`, `367-379` | STEP-55 must migrate these to `context.push` or `context.go` to utilize GoRouter paths and support D5. |
| FC-54.9-002 | Needs restructure | Data Bucket: D1/D2 Sheet Modality & D4 Interception | The Upload form is a full-page push (`FScaffold` on mobile, no header on desktop) without a `PopScope`. Selecting a large file and accidentally pressing Back discards the file silently without dirty interception. | `upload_file_page.dart:73`, `310-336` | STEP-55 must migrate Upload to a modal side-sheet (desktop) / bottom-sheet (mobile) with explicit `PopScope` dirty interception. |
| FC-54.9-003 | Needs restructure | Data Bucket: Upload Cancellation | Upload progress is shown, but there is no cancellation affordance (the back button is disabled during upload: `isUploading ? null : Navigator.pop`). | `upload_file_page.dart:328` | Provide an explicit cancel action for the upload state, especially crucial for large geospatial files. |
| FC-54.9-004 | Aligned | Data Bucket: Upload Failure Recovery | Upload errors display a toast with a "Coba Lagi" action that retries `_submitUpload()` without requiring the user to re-select the file, as `_fileBytes` is preserved in state. | `upload_file_page.dart:291-303` | Maintain this recovery pattern when migrating to sheet adapter. (Silent failure on connectivity drop / app close remains an unverified data-trust edge case). |
| FC-54.9-005 | Aligned | Data Bucket: File-size feedback | Enforces a `_kMaxFileSizeBytes` check before reading into memory, and displays a formatted size under the selected file icon prior to commit. | `upload_file_page.dart:178-188`, `472-478` | Keep implementation. |
| FC-54.9-006 | Aligned | Data Bucket: Lifecycle Cohesion | List → Form/Detail → Back loops properly execute a `RefreshFiles()` event upon returning, avoiding stale data. | `data_bucket_list_page.dart:333`, `377` | Ensure `RefreshFiles` behavior is preserved when shifting to GoRouter. |
| FC-54.9-007 | Aligned | Work Timeline: Read-only Cohesion | Timeline exposes only a date-range selector and milestone cards. There are no fake CRUD affordances or missing milestone entry forms that should exist—it acts explicitly as a read-mostly viewing surface. | `timeline_page.dart:64-80`, `timeline_page.dart:238-275`, `milestone_card.dart:35` | Preserve read-only intent for this release; milestone entry sheet remains deliberately excluded. |
| FC-54.9-008 | Aligned | Report Path (Both Features) | Deliberate absence of a report action in both Data Bucket (documented as "no meaningful report type") and Work Timeline. | `data_bucket_list_page.dart:360-362`, `timeline_page.dart:90-130` | Maintain absence as a deliberate design decision. |
| FC-54.9-009 | Needs polish | Token conformance | Both features utilize `FTheme` tokens (no raw colors found) and rely on a transparent `Material` wrapper for `PopupMenuButton` interoperability, but `DataBucketListPage` still uses a Material `FloatingActionButton.extended` for the upload action, `UploadFilePage` uses Material `showDatePicker` and `InputDecorator` for the acquisition date field, and `MilestoneCard` uses `InkWell` instead of `FTappable`. These violate the 54.1 token conformance rubric to use ForUI components. | `data_bucket_list_page.dart:362-383`, `upload_file_page.dart:211-216`, `383-398`, `milestone_card.dart:35` | STEP-55 must replace the Material FAB with a floating `FButton`, migrate the date picker field and InkWell to ForUI equivalents (or document an explicit interoperability exception). |
| FC-54.9-010 | Unverified | Accessibility & Tokens | Keyboard focus and a11y contrast remain untested at runtime. | `file_detail_page.dart:102`, `data_bucket_list_page.dart:84` | Validate keyboard traversal and contrast ratios during runtime audit. |

## 3. D7 Verdict: File Detail Inspector

**Verdict:** The Data Bucket file detail (`file_detail_page.dart`) **must be restructured as a side-sheet inspector** on desktop and a draggable bottom sheet on mobile, rather than a full-page push.

**Rationale:**
1. **List Context:** Geospatial file metadata (coordinates, tags, size) is often reviewed comparatively. A full page obscures the list, forcing the user into an inefficient back-and-forth loop. A side-sheet on wide viewports (and a bottom sheet on mobile) allows the user to inspect metadata and perform actions (Delete, Open in Drive) without losing their scroll position and applied filters in the `DataBucketListPage`.
2. **Deep Linkability (`/:id`):** The `/:id` route should be preserved. When the URL matches `/:id`, the list should render beneath the open sheet. If deep-linked directly, it falls back safely to the list view underneath.

## 4. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| Data Bucket List | Web/Android | Static source analysis of push navigation and refresh loops | `data_bucket_list_page.dart:320-379` | Needs restructure for D5 (FC-54.9-001) |
| Upload File Page | Web/Android | Static source analysis of picker, validation, and BLoC submission | `upload_file_page.dart:73-336` | Needs restructure for D1/D2/D4 (FC-54.9-002, 003) |
| File Detail Page | Web/Android | Static source analysis of layout and delete/drive actions | `file_detail_page.dart:77-212` | Needs restructure for D7 (File Detail Inspector) |
| Work Timeline | Web/Android | Static source analysis of date picker and milestones list | `timeline_page.dart:64-275` | Aligned (FC-54.9-007) |

## 5. Verification record

| Check | Result |
|---|---|
| Data Bucket lifecycle traced | Pass — `Navigator.push` combined with `RefreshFiles` is evaluated |
| Upload UX evaluated | Pass — Progress, size check, recovery noted; cancellation gap identified |
| D7 verdict recorded | Pass — Full rationale for inspector sheet documented in §3 |
| D4/D5 status recorded | Pass — Missing dirty interception and GoRouter gap logged |
| Report path presence | Pass — Deliberate absences recorded |
| Application code changed | Pass — App repo remains unedited |
| Runtime/visual evidence | Unverified — Not run |

**Next action:** Update `STEP-54-PLAN.md` substep table, and proceed to substep 54.10.
