# STEP-55 Feature-Accessibility Evidence Preflight — Cut & Fill, Land Clearing, Attendance

**Date:** 2026-10-07
**Heads verified on disk:** app `mine-flow-app` @ `1486826` (`step-0055-cohesive-ui-rebuild`, == origin), docs @ `ff896a5` (same branch, == origin), prompts on `main`. App worktree: 3 dirty generated `lib/l10n/app_localizations*.dart` (parent-proven EOL-only; untouched) + untracked scratch (`.step55*`, `tool/verify_test_driver_adversarial.dart`) — all preserved.
**Read-only audit.** No app/docs/prompts edits, no Flutter/device runs, no remote mutations. No finding closed, no STEP closed.

**Acceptance authority:** `Code/mine-flow-docs/reports/2026-09-11-step-54-master-polish-spec.md` §4.1 item 6 (`FC-54.2-007`, line 234), §4.2 item 7 (`FC-54.3-007`, line 246), §4.4 item 11 (`FC-54.5-004,013`, line 274); ledger §8.3 lines 484–487; `architecture/07-ui-design-system.md` §5 lines 65–66 (WCAG 2.1 AA; 48×48dp mobile; "source `Semantics` wrappers alone are not acceptance evidence").

---

## 1. Prior-adjudication baseline (why these four FCs are Unverified)

`Code/mine-flow-docs/reports/2026-10-06-step-0055-resume-verification.md` §Per-FC verdicts (lines 122–133): the archived 73/73 web matrix (`reports/design-review/step-0055/2026-10-07-web-matrix-index.md`) covers **six shell routes only** (`design_review_capture_test.dart:183–190`: `/`, `/teams/daily-log`, `/teams/daily-log/form`, `/operations`, `/teams`, `/tools`). No `/operations/cut-fill*`, `/operations/land-clearing*`, or `/teams/attendance*` route is captured, and captures cannot measure contrast/targets/semantics regardless. All four FCs remain Unverified; the required follow-up is named at lines 145–156.

## 2. Current source state (verified at `1486826`)

### 2.1 Cut & Fill
- `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart` — `AppResponsiveSheet` form (D1/D2), one-shot close guard `:140–160`, save `FButton` key `save_cut_fill_button` `:319` (footer promoted md→lg = 48×48 touch via `_wrapSheetFooter`, `lib/core/presentation/widgets/app_interaction_primitives.dart:96–126`).
- Date tile: `AppAccessibleIconButton` tooltip `'Ubah tanggal'` `:364–381` (48×48, `app_interaction_primitives.dart:709–722`); opens `AppCalendarDialog.showSingle` (in-context, no route change).
- **A11y gap (product):** `VolumeInputField` (`lib/features/tracking/presentation/widgets/volume_input_field.dart:92–116`) renders its label as a plain `Text` in an `FCard` (`:79–86`); the `TextField` has **no `labelText`, no `Semantics` label** — accessible name is only hint `'0.0'`. Same pattern in `AreaInputField` (`area_input_field.dart:92–116`) and the elevation `FTextField` (`cut_fill_form_screen.dart:462–473` — `hint` only, no `label` param; forui `FTextField` supports `label`, `forui-0.26.0/lib/src/widgets/text_field/input/input.dart:312` renders it through `FLabel`, which does **not** attach an AT-visible name to the input either — `label.dart` has only `Semantics(validationResult:)` at `:300`).
- Validation: toasts (`:162–184`, `:227–249`) — `showFToast` has no liveRegion; error announcements are not guaranteed for AT.
- Routes: `/operations/cut-fill`, `/form`, `/:id/form` (`lib/app/router.dart:87–89, 347–425`); cold edit fetches by ID (`cut_fill_bloc.dart:69–92`). No D7 inspector (per FC-54.2-006).

### 2.2 Land Clearing
- `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart` — Material `TabBar`+`TabController` retained with documented interop justification `:1–12`; tabs `:475–491` (`Rencana (Plan)` / `Realisasi (Actual)`); tab↔URL two-way sync `:150–176`, invalid-tab fallback to Actual `:150–156`.
- **A11y gap (evidence, not product):** `TabBar` here has no per-tab `Semantics(selected:)` assertion anywhere, and Material `Tab` semantics rely on framework defaults — runtime selected-state evidence must come from a Semantics-tree probe, not source.
- Shared single `CreatableCombobox` (CF-043) `:452–468`; on mobile it focuses a text field (IME rises) — occlusion behavior is unproven at runtime.
- `AreaInputField` label-association gap as above (`:528`, `:610`).
- Inspector: `land_clearing_inspector_screen.dart` (read-only, `_openEdit` `:86–104` pushes `land-clearing-edit`), routes `router.dart:438–523`.
- Existing `FC-54.3-007 Mechanical Coverage` group (`test/features/tracking/presentation/land_clearing_entry_screen_test.dart:574–625`): dark render = exception-free only (`:575–587`), 2.0× text = exception-free only (`:589–599`), 48dp = `AppAccessibleIconButton` sizes + **save `>= 40.0` height (`:623`) — stale/weak vs the 48dp standard** (test-only fix).

### 2.3 Attendance
- `lib/features/attendance/presentation/pages/attendance_form_sheet.dart` — durable URL `?date&siteId` `:24–30`; header row date+bulk `:283–331` (`Tandai Semua Masuk`, only-unset semantics via `AttendanceFormBulkMarkPresent`); footer `Simpan Absensi (N Kru)` `:430–457` (key `save_attendance_batch_button`, disabled only while submitting); `_focusFirstInvalid` `:417–426`; reason-controller seeding on cold reconstruct `:205–215`; discard-reason confirmation `:333–390`.
- `attendance_crew_card.dart` — card `Semantics(container:, label:)` with name+status+sync `:54–65`; four inline choices with `Semantics(button, selected)` + 48dp constraints `:174–233`; `_ReasonField` `:243–303` (labelled, keyed, clear button); sync indicator `:307–371` with `Semantics(label:)` + labelled retry.
- **A11y gap (product):** per-record sync-state **changes** are never announced — the card label is static (re-read only on refocus); `SemanticsService.sendAnnouncement` exists only for busy-dismiss (`app_interaction_primitives.dart:332–343`) and the report dialog (`app_contextual_report_dialog.dart:109`). No `liveRegion` on the sync indicator. `AppStatePanel` is `liveRegion: true` (`:778`) but that covers loading/error panels, not sync churn.
- **Restoration:** **no `RestorationMixin`/`restorablePush`/`RestorationManager` anywhere in `lib/`** (git grep, zero hits). "Restoration" per §4.4 item 11 is satisfiable only as durable-URL cold reconstruction + controller seeding (`attendance_form_sheet.dart:205–215`); OS-level process-death restoration is unimplemented and must be named as a blocker or scoped out by the owner.
- Bloc validation/sync truth: `attendance_form_bloc.dart:239–316` (unset/blank-reason refusal, firstInvalid), sync derivation `:370–383`; draft entity nullable-status + explicit remarks clearing `attendance_crew_draft.dart:47–122`.

### 2.4 Existing test inventory (exact paths)
| Path | Covers | A11y coverage |
|---|---|---|
| `test/features/tracking/presentation/cut_fill_form_screen_test.dart` (356 ln) | render, clean/dirty/scrim/back dismissal, cold edit, AppStatePanel, responsive geometry, validation toast, failed-save retention, zoneId query | **none** (no contrast/48dp/semantics/focus/keyboard) |
| `test/features/tracking/presentation/cut_fill_list_screen_test.dart` (595 ln) | list, filters, popover reset, focus-return-to-invoker `:508` | focus-return only |
| `test/features/tracking/presentation/land_clearing_entry_screen_test.dart` (626 ln) | tabs resolution/sync/fallback `:341–511`, combobox CF-043 `:126–210`, cold-ID `:513–572` | `FC-54.3-007 Mechanical Coverage` `:574–625` — weak (above) |
| `test/features/tracking/presentation/land_clearing_entry_screen_deep_link_test.dart` (250 ln) | cold edit, invalid/not-found, inspector hierarchy | textual only |
| `test/features/attendance/presentation/attendance_form_sheet_test.dart` (253 ln) | layout, cold route, four choices (label presence, not measured targets) `:147–160`, reason reveal/confirm/clear, submit validation, bulk | label-text presence only |
| `test/features/attendance/presentation/attendance_form_bloc_test.dart` | unset/blank validation `:348+`, bulk exceptions `:258–346`, sync truth + retry `:485–562` | bloc-level (mocked), not runtime |
| `test/unit/attendance_crew_draft_test.dart` | nullable rows, reason trim, explicit clearing | n/a |
| `test/widget/attendance_screen_test.dart` (457 ln) | list screen; 48dp SizedBox height==48 for list FABs `:255–268`; `bySemanticsLabel('Buat Laporan Kehadiran')` `:247` | partial |
| `test/widget/sheet_popup_dismiss_regression_test.dart` | popup-dismiss guard pin | n/a |
| `integration_test/design_review_capture_test.dart` | 73-cell shell matrix; **omits all three features** `:183–190` | screenshots only |
| `integration_test/journeys/{cut_fill,land_clearing,attendance}_journey_test.dart` | E2E behavior (green at pushed head run 139 / CI `37535200023` per resume-verification report) | no sync announcements, no 2.0× leg, no IME reachability, no contrast, no mixed-unset/existing bulk exception leg in the journey |
| `integration_test/helpers/{app_harness,capture_viewport,login_helper,offline_helper,staging_config}.dart` | real-app boot, aligned viewport, staged login + privacy-gate ack | reuse these |

Static guards already green at head: `flutter analyze` 0, `dart format` clean, full unit suite green (per close-report reconciliation banners).

## 3. Measured static contrast (forui 0.26.0 neutral palette + app dark override)

Computed from `forui-0.26.0/lib/src/theme/colors.dart:144–186` (`neutralLight`/`neutralDark`) and the app's dark `destructiveForeground` override (`lib/app/app.dart:80–88`), WCAG 2.1 relative-luminance ratios:

| Pair | Ratio | AA |
|---|---|---|
| light foreground / background (0A0A0A/FFFFFF) | 19.80:1 | pass |
| light mutedForeground / background (737373/FFFFFF) | 4.74:1 | pass (normal text) |
| light mutedForeground / card | 4.74:1 | pass |
| light primary / background | 17.93:1 | pass |
| **light mutedForeground / secondary (737373/F5F5F5)** | **4.35:1** | **fails AA normal text** (large-text only) |
| dark foreground / background | 18.97:1 | pass |
| dark mutedForeground / background (A1A1A1/0A0A0A) | 7.66:1 | pass |
| dark mutedForeground / card (0xFF171717) | 6.94:1 | pass |
| dark mutedForeground / secondary (0xFF262626) | 5.86:1 | pass |
| dark primary / background | 15.72:1 | pass |
| light destructiveForeground / destructive | 4.57:1 | pass |
| dark destructive override (0A0A0A on FF6467) | 6.85:1 | pass |
| selected attendance choice: primary on primary@12% tint (blended E3E3E3 light / 303030 dark) | 13.97 / 10.48:1 | pass |

**Borderline finding:** `mutedForeground on secondary` = 4.35:1 < 4.5. Wherever muted-foreground text sits on a secondary/outline surface (e.g. secondary `FButton` variants use `secondaryForeground` = pass; but any `mutedForeground` text on `F5F5F5` fails normal-text AA). The runtime harness should assert the pinned token hexes at runtime and enumerate actual muted-on-secondary usages on the three features before adjudicating contrast as pass/fail.

## 4. Runnable evidence plan (smallest sound program; no `lib/**` edits)

### 4.1 Widget-layer a11y probes (new `test/` files, extend existing suites — no product edits)
1. **FC-54.2-007 — extend `cut_fill_form_screen_test.dart`** with an `FC-54.2-007 a11y` group:
   - 48dp: measure `AppAccessibleIconButton` (48×48), footer save (≥48 height under `FTheme.neutral.*.touch`), date/bulk controls — mechanical, mirrors `land_clearing_entry_screen_test.dart:601–624`.
   - Focus/keyboard: sheet `FocusScope` autofocus + `TraversalEdgeBehavior.closedLoop` (`app_interaction_primitives.dart:233–236`); Escape → dirty guard (`:378–383`); tab-traversal order via `tester.sendKeyEvent(LogicalKeyboardKey.tab)` walk.
   - Semantics traversal: header `Semantics(header:true)` (`:512–519`), close label `'Tutup'`, barrier label, save label. **Expected honest failure:** volume/elevation fields have no accessible name (§2.1) — record as product defect, do not assert a pass.
   - Contrast: assert `FTheme.of(context).colors` hexes match the pinned neutral palette at runtime (light+dark), plus the §3 ratio table as the measured record.
2. **FC-54.3-007 — extend `land_clearing_entry_screen_test.dart` `FC-54.3-007 Mechanical Coverage`:**
   - Tab semantics: Semantics-tree probe asserting exactly the active tab carries `selected == true` and both tab labels are AT-reachable (source currently proves nothing — §2.2).
   - Strengthen save assertion `:623` from `>= 40.0` → `>= 48.0` under touch theme (test-only; footer promotes md→lg).
   - Combobox occlusion: at 480dp sheet width, open the method combobox, simulate `view.viewInsets` (IME), assert the option overlay renders above the keyboard and selection lands — the interactive check captures cannot provide.
   - Summary hierarchy: inspector heading Semantics (`Semantics(header:)`) + read-only mode (`AppDetailInspector`) assertions in the deep-link test file.
   - Dark/light token contrast (as in 4.1) + focus order across shared fields → tabs → footer.
3. **FC-54.5-004 / FC-54.5-013 — extend `attendance_form_sheet_test.dart`:**
   - Semantics traversal: card container labels (`attendanceCrewStatusLabel` + sync phrase), choice `Semantics(button, selected)` toggling with selection, reason `labelText`, measured 48dp on choice chips (rendered size, not `constraints` alone) and footer.
   - 2.0× text scale: `TextScaler.linear(2.0)` pump, assert no overflow (m2-style) and labels readable — currently only LC has a 2.0× leg, and it is exception-free-only.
   - Sync announcements: Semantics-tree probe on sync-state change. **Expected honest failure:** no liveRegion/`sendAnnouncement` on per-record sync churn (§2.3) — record as product defect for owner decision.
   - Restoration: cold-URL reconstruction of saved reasons (exists `:205–215`; pin with a remount test); add explicit "process-death restoration unimplemented" blocker note (no `RestorationMixin` in `lib/`).
   - IME/keyboard: footer reachable with simulated `viewInsets` (pattern: `login_helper.dart:126–128`), `_focusFirstInvalid` scroll+focus assertion at widget level; validation for all four persisted status mappings incl. Alpa collapse-clear (widget-level; bloc-level exists).
4. **Journey-level (runtime Web + Android):**
   - Extend `design_review_capture_test.dart` `screens` list (`:183–190`) with `/operations/cut-fill`, `/operations/cut-fill/form`, `/operations/land-clearing`, `/operations/land-clearing/<id>` (detail), `/teams/attendance`, `/teams/attendance/form`. The login helper already clears the privacy gate;
the capture loop needs the resize/reset/settle sequence per cell (the `CaptureViewport` + `setCaptureSize` pattern at `:84–88, 140–142`) and a per-cell `MediaQuery` size assert (`:194–198`).
   - Complement with a real integration a11y leg: a small `integration_test/journeys/feature_a11y_journey_test.dart` that drives the three feature routes on the real app (staging, like existing journeys), runs the same Semantics-tree/48dp/focus probes against runtime widgets, and writes per-FC verdicts to `binding.reportData` (the supported app-to-driver evidence channel). Web + Android; Android pixel evidence stays separate from widget/runtime semantics.
5. **What stays Unverified even after all of the above** (must not be inferred): hardware screen-reader (TalkBack/VoiceOver) evidence — mark separately from widget/runtime semantics; authenticated-shell AX tree on Android; OS process-death restoration; reduced-motion; real-device IME behavior beyond simulated insets.

### 4.2 Product defects found (block evidence-only completion; flag for owner decision — do not fix here)
1. **Volume/area/elevation fields have no accessible name** — `volume_input_field.dart:92–116`, `area_input_field.dart:92–116` (plain `Text` label, no `labelText`/`Semantics`), `cut_fill_form_screen.dart:462–473` (FTextField `hint` only; forui `FLabel` does not attach the name to the input either). Blocks FC-54.2-007's "field names" acceptance on all platforms.
2. **Per-record sync-state changes are never announced to AT** — `attendance_crew_card.dart:307–371` (static label, no liveRegion/announcement). Blocks FC-54.5-013's "sync-status announcement" acceptance.
3. **LC save-target test asserts `>= 40.0` height** — `land_clearing_entry_screen_test.dart:623` vs the 48dp standard. Test-only fix, allowed in the evidence lane; but if the rendered save button is genuinely < 48dp in some state, that is a product geometry defect.
4. **Borderline AA contrast: mutedForeground on secondary = 4.35:1** (`forui colors.dart:144–186`) — needs an inventory of actual muted-on-secondary text usages on the three features before contrast is adjudicated; a failure would be an owner decision (token override, as already done for dark `destructiveForeground` in `app.dart:80–88`).
5. **No process-death restoration** (no `RestorationMixin` in `lib/`) — FC-54.5-013 "restoration" can only be satisfied as durable-URL cold reconstruction + controller seeding; scope must be owner-confirmed.

FC-54.2-007/54.3-007/54.5-004 are otherwise **not product-blocked**: routes, sheets, tabs, bulk/exception logic, validation, reason handling, and semantics scaffolding are implemented and journeied green at the pushed head; the gaps are evidence (runtime probes, routes in the matrix) plus defects 1–2 above.

## 5. Constraints honored
- Read-only: no app/docs/prompts edits; the only file written is this report.
- Untracked scratch and the 3 dirty generated `lib/l10n/app_localizations*.dart` untouched; all 12 a11y l10n keys confirmed present in all three delegates.
- No `.env`/credential values read or printed; `login_helper.dart` references `--dart-define` keys only.
- No gates inferred: the 73/73 matrix is a shell-only harness pass; the four FCs remain Unverified pending the §4 program and defects 1–2 (and owner adjudication of 3–5).
- No finding or STEP closed.
