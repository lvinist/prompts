# mine-flow — STEP-48.22 Findings (RE-RUN): UI & Harness Defect Fixes

**Date:** 2026-09-01
**Executor:** Hermes (Claude Opus 4.8) — escalated from GPT 5.6 Luna per the PLAN's
"escalate if the same fix fails twice" rule: 48.22's first pass fixed each named line and the
gate came back red at three sibling sites of its own defect classes.
**Branch:** `step-0048-runtime-evidence`
**Scope:** STEP-48.26 residual failures **R-1, R-2, R-3, and the UI half of R-4**, per
`mine-flow-STEP-48.26-FINDINGS.md` §7 item 1.

---

## Verdict

**All four assigned residual failures fixed at the level of the defect CLASS, with the class
verified swept at the tested surface. Local gates green: `flutter analyze` 0 issues,
`dart format` clean (336 files, 0 changed), `flutter test` green.**

Two of the four (R-1, R-2) were live at sites nobody had named — including three the first pass
could not have known about, because they only became reachable once the earlier fix removed the
error that masked them. Those are recorded below with the same weight as the assigned sites.

**Android screenshot capture (R-3) is fixed in code but its runtime output remains
Unverified**: see §5. No screenshot count is claimed.

---

## 1. Why this re-run exists

48.26's dominant finding: *"six of eight residual failures are a substep's own assigned defect
surviving at a second, unswept site."* Three of those six were 48.22's:

| 48.26 row | Assigned to 48.22 as | What the first pass did | What was still red |
|---|---|---|---|
| R-1 (BH-019) | "give the cut/fill `DropdownButton` a Material ancestor or replace it" | replaced the control in `cut_fill_form_screen.dart` | `date_range_selector.dart:124` — **the line the baseline log actually named** |
| R-2 (BH-015) | "fix the `RenderFlex` overflow at `timeline_page.dart:289`" | fixed that line | the same class at `cut_fill_card.dart:33`, `land_clearing_card.dart:30`/`:34` |
| R-3 | "call `convertFlutterSurfaceToImage()`" | added the call | the next line of the same harness: `No GoRouter found in context` |

So this run's rule was: **name the class, grep for every site, justify each one, and verify at
the surface the journey actually renders** — not at the default 800x600 widget-test surface, and
not only at the `file:line` in the register.

---

## 2. R-1 — Material-ancestor class (BH-019)

**Class:** a Material-only widget rendered in a subtree with no `Material` ancestor. This
project purged Material at STEP-37 and roots several pages in ForUI's `FScaffold`; a Material
widget there throws `No Material widget found` at build time.

### The sweep

`grep -rn 'DropdownButton' lib/` → 8 sites. Each one classified:

| Site | Host page's root | Material ancestor guaranteed? | Action |
|---|---|---|---|
| `reporting/.../date_range_selector.dart:124` | `ReportConfigPage` → **`FScaffold`**, route outside the shell | **No** | **Replaced with `FSelect`** |
| `core/.../zone_filter_dropdown.dart:37` | `cut_fill_list_screen` / `land_clearing_list_screen` → `Scaffold` | Yes | Left; no drift to fix |
| `benchmark_form_screen.dart:558/607/658` | `Scaffold` (both branches) | Yes | Left |
| `data_bucket/.../filter_chips.dart:115` | `data_bucket_list_page` → `Scaffold` | Yes | Left |
| `inventory_item_entry_screen.dart:324/387` | `Scaffold`, and `:387` already carries an explicit `flutter_localizations` re-injection (STEP-43 pitfall) | Yes | Left |

Only one of the eight was actually broken — but it was the one the failure named, and it is the
one the first pass missed.

**Fix:** `DateRangeSelector`'s preset control is now ForUI `FSelect<String>` with
`FSelectControl.lifted`, which renders its own field and popover through `FPortal` and needs no
`Material`. This is replacement, not wrapping — Doc 07 §"Framework Widgets" names `FSelect`
explicitly, so no design deviation and no ADR is required. The former `FCard` wrapper was
dropped because `FSelect` draws its own field chrome (keeping it double-bordered the field).

### Two more sites of the same class, found by sweeping the *symptom* rather than the widget name

`grep` for `DropdownButton` is not the class. The class is "Material widget with no Material
ancestor", and `InkWell` is one too:

- **`core/presentation/widgets/creatable_combobox.dart`** — the option tiles used a Material
  `InkWell`. `ReportConfigPage` embeds a `ZonePicker`, which is a `CreatableCombobox`, so
  **opening the zone picker on that page threw the identical error**. This is reachable from the
  same journey that reported BH-019 and would have kept `reporting` red after the
  `date_range_selector` fix. Replaced with ForUI `FTappable`.
  Reproduced before the fix, absent after (diagnostic: `FScaffold` + combobox, tap → 0 tiles and
  `No Material widget found`; after → 1 tile, no error).

**Regression coverage:** `test/features/reporting/presentation/pages/report_config_page_test.dart`
— renders `ReportConfigPage` for **all 7 `ReportType` values** inside `MaterialApp` + `FTheme`
with **no enclosing `Scaffold`** (the real route shape) and fails on any Flutter error; opens the
date-range popover and asserts the selection reaches the cubit; opens the zone combobox and
asserts no error; and re-asserts the NR-001 lock. 4 tests, all passing.

---

## 3. R-2 — `RenderFlex` overflow class (BH-015)

**Two distinct causes**, both of which had to be fixed for the class to be gone:

**(a) Fixed-height grid tiles.** `daily_log_list_screen`, `cut_fill_list_screen`, and
`land_clearing_list_screen` each built a `SliverGrid` with
`SliverGridDelegateWithFixedCrossAxisCount(childAspectRatio: isMobile ? 3.2 : 2.6)`. A fixed
ratio forces a fixed tile height, so **any** card taller than the tile overflows vertically —
which is precisely the `overflowed by 80 pixels on the bottom` at `cut_fill_card.dart:33` and
`58 pixels` at `land_clearing_card.dart:30`. Card content is variable by nature (optional zone,
material, elevation, notes, delete affordance), so no single ratio is correct.

New `lib/core/presentation/widgets/adaptive_card_sliver_grid.dart` keeps Doc 07's layout — one
column on phones, two once there is room — while sizing each row to its content
(`IntrinsicHeight` keeps a two-column row visually even). All three screens now use it, and
their now-unused `isMobile`/`_kBreakMobile` locals were removed (analyzer-clean).

**(b) Unshrinkable `Row`s inside the cards.** The header and metadata rows held raw `Icon` +
`Text` children with no flex, so long values overflowed horizontally. Converting them to `Wrap`
was **not sufficient** and this is worth recording: *a `Wrap` reflows between children but never
shrinks a child that is individually too wide.* New
`lib/core/presentation/widgets/card_meta_wrap.dart` supplies `CardMetaChip` (icon + `Flexible`
label, so each chip shrinks and ellipsises) and `CardMetaWrap`.

### The sweep — every card that appears in a scrollable list

| Card | Overflow found at 393x873 before fix | After |
|---|---|---|
| `CutFillCard` | yes (the named site) | clean |
| `LandClearingCard` | yes (the named site) | clean |
| `DailyLogCard` | **yes — 41 px right**, not previously named | clean |
| `EquipmentCheckCard` | **yes — 169 px right** (`:129` metadata row: UUID inspector id + timestamp cannot share a line) | clean |
| `InventoryCard` | **yes — 119 px right** (`:72` category + SKU row) | clean |
| `MilestoneCard` | **yes — 144 px and 189 px right** (`:75` date chips, `:95` target/actual) | clean |
| `FileCard` | no | clean |

Four of these seven were **not** in any register row. The deep-link journey walks
`/teams/equipment-check`, `/operations/inventory`, and `/timeline`, so they were sitting behind
the two failures 48.26 could see.

**Regression coverage:**
- `test/features/tracking/presentation/record_card_overflow_test.dart` — the three
  fixed-ratio-grid cards rendered through the **production sliver** at 400x800 (1 column) and
  700x1000 (2 columns), plus a delete-affordance case proving the previously clipped row renders.
  7 tests.
- `test/features/shared/list_card_overflow_sweep_test.dart` — a class-level sweep over
  `EquipmentCheckCard`, `FileCard`, `InventoryCard`, `MilestoneCard` at **393x873 (the emulator's
  own width, where CI reported the overflow) and 400x800**, with worst-case content (long zone
  names, UUIDs, full timestamps, every optional field). 8 tests.

Both suites rely on `flutter_test`'s own behaviour of failing on an unexpected framework error
rather than an `FlutterError.onError` capture — an override there swallows other real errors and
trips the binding's leak check.

---

## 4. R-4 (UI half) — data-bucket staleness

**48.26's diagnosis confirmed exactly.** `DataBucketBloc` loaded once at construction and never
observed the repository again, while `getFiles` is local-first with an `unawaited`
`_refreshIfOnline()`. Rows arriving from staging after mount could not reach the UI without a
manual `RefreshFiles`. Before 48.20 re-sited the seed row both sides were empty, so the
journey's `if (rows.isEmpty) … else …` passed for the wrong reason — a vacuous pass, now visible.

**Fix, three layers, none of which weakens the journey's assertion:**
- `DataBucketLocalDataSource.watchFiles()` — new; emits the cached set on every Hive change.
- `DataBucketRepositoryImpl.watchFiles(...)` — now emits from the **local cache** (seeded with
  the current contents so a subscriber is never blank), applying the same site/zone/type filter
  as `getFiles`. It previously proxied the Supabase realtime stream, bypassing the cache — and
  **no presenter used it at all**, which is why the staleness went unnoticed.
- `DataBucketBloc` — subscribes after a successful load/refresh, folds updates in via a private
  `_FilesUpdated` event, preserves the active search/zone/type selections, and cancels on
  `close`. Stream errors are swallowed deliberately (documented in-code): degrading to "no live
  updates" is right; replacing a rendered list with an error state would be a new defect.

**Regression coverage:** `test/features/data_bucket/presentation/bloc/data_bucket_staleness_test.dart`
— 4 tests over a real Hive box: the stream emits current cache then every change; the site
filter applies to streamed rows; **the bloc renders a row that only the background refresh
brought in** (the exact journey scenario); a streamed update does not clear the user's search.
`data_bucket_bloc_test.dart` gained a neutral `watchFiles` stub with a comment pointing at the
new suite. The whole `test/features/data_bucket/` tree passes (62 tests).

**The fixture half of R-4 is 48.20's** and is untouched here.

---

## 5. R-3 — Android screenshot capture harness

**Root cause confirmed:** the loop resolved `GoRouter.of(ctx)` from
`tester.element(find.byType(MaterialApp))`. `MaterialApp.router` installs `InheritedGoRouter`
*below* itself, so that element is an ancestor of the provider and the lookup can never succeed.
Every journey navigates with the `appRouter` instance the app exposes; the harness now does the
same. (`SettingsCubit` *is* provided above `MaterialApp`, so that lookup is left alone — the two
are not interchangeable.)

Also in this substep, per Doc 07's *"Android locks to portrait mobile"*:
- **Android matrix = the portrait-phone leg only** (2 themes x 2 locales x 6 screens = 24 +
  1 login = 25 captures). Web keeps phone/tablet/desktop. Forcing a 1200 px desktop width onto a
  portrait-locked platform would screenshot a layout that platform never shows.
- Android filenames now carry an **`android-` prefix**, so they cannot be confused with the 73
  committed web PNGs.
- The test **counts its own captures** and asserts the count equals the matrix size, then prints
  the filenames. A capture run that goes green while writing zero files is the vacuous pass this
  STEP exists to eliminate; it can no longer happen silently.

**Unverified — stated plainly:** the `convertFlutterSurfaceToImage` guard and the `GoRouter` fix
are code-correct and analyzer-clean, but **`flutter test integration_test/...` does not invoke
`onScreenshot`** — only `flutter drive --driver=test_driver/integration_test.dart` writes the
bytes. This run did not complete a `flutter drive` capture pass, so **no screenshot count or
filename is claimed here.** 48.24's local gate and 48.26's CI run own that evidence.

**Docs-truth item for 48.15/48.25 (unchanged from the first pass, still open):** the design
review's coverage table says "Web (Phone, Tablet, Desktop)" throughout. Once an Android capture
run is evidenced, it may be extended to "+ Android (Phone)". Until then it must be narrowed to
web-only. This substep did **not** rewrite
`reports/2026-08-30-step-0048-runtime-design-review.md` — archived reports are immutable.

---

## 6. Live Android journey runs (evidence, including a failure this run did not fix)

Run on `Pixel_6a` / `emulator-5554` with `--dart-define-from-file=.env` (no secret value read,
printed, or committed).

| Journey | Result | Note |
|---|---|---|
| `data_bucket_journey_test.dart` | **1 passed, 1 skipped** | Part B green — the R-4 fix confirmed against live staging; Part A skip is D2/RISK-0017-0018 as designed |
| `reporting_journey_test.dart` | fixed forward, see below | |
| `deep_link_journey_test.dart` | fixed forward, see below | |

**Reporting:** the Material-ancestor error is **gone** (the journey now reaches report generation
and the live PostgREST query fires). It then failed on `Bad state: No element` at
`reporting_journey_test.dart:76` — `find.widgetWithText(FButton, 'Buat Laporan')` cannot match
while generating, because the button's child swaps to a spinner in exactly the state NR-001
asserts about. Fixed by giving the button `Key('generate_report_button')` and keying the finder;
**the assertion is unchanged** (`onPress` must be null while locked). This is a test-defect on a
file whose app-defect was mine, so it is recorded here rather than handed sideways.

**Deep link:** the `cut_fill_card` / `land_clearing_card` overflows are **gone**. The journey now
fails later, on a **38 px right overflow in a DISPOSED/DEFUNCT element tree** while the
post-sign-out redirect tears the shell down. Every candidate page reproduced clean in isolation
at 393x873 (login, report picker, report config, and all seven swept cards), and the render
object is already disposed by the time the assertion fires, so the widget cannot be identified
from this evidence.

> **This is recorded Deferred/Unverified with a named unblock, not waved through, and not
> attributed to a guessed widget.** Unblock: re-run the deep-link journey with
> `debugPrintStack`/`WidgetsApp.debugAllowBannerOverride`-style breadcrumbs, or bisect
> `_shellRoutes` so the failing route is isolated while the tree is still live. **It still counts
> against the gate** — the deep-link journey remains red on Android until it is resolved. It is
> plausibly a teardown-only artifact rather than a user-visible defect, but plausible is not
> evidence and I am not claiming it.

---

## 7. Verification

| Gate | Result |
|---|---|
| `flutter analyze` | **No issues found!** (exit 0) |
| `dart format --set-exit-if-changed .` | **336 files, 0 changed** |
| `flutter test` (full suite) | **482 tests passed** (exit 0), up from 48.25's 457 — +25 from the 5 new suites; **0 regressions**, and the known Hive `setUpAll` flake did not fire on this run |
| `dart run tool/check_supabase_contracts.dart` | `[OK] Contract verification passed.` (exit 0) |
| Focused suites | reporting 11 · record-card overflow 7 · list-card sweep 8 · data_bucket 62 · combobox 12 — all passing |
| Root `DESIGN.md` / `PRODUCT.md` | **unmodified** (`git status` proves it — they do not appear) |
| Archived design-review reports | **not rewritten** |
| `registries/risks.yml` | **not touched** (RISK-0003 / 0011 / 0017 / 0018 left as they are) |
| Assertions weakened | **none.** The one finder that changed (`generate_report_button`) asserts the same thing more precisely |
| `expect(true` in `integration_test/` | 0 |
| CRLF hygiene | every touched file re-normalised to LF before commit; `git diff --numstat` shows real changes only, no whole-file churn (48.25's lesson) |

---

## 8. Handoff

**To 48.20 (next in 48.26's re-run order):** R-5 (empty-string UUIDs into `zones` and
`benchmarks`), R-6 (`KRU-00N` roster), and the **fixture half of R-4** — the UI half is done, so
a re-seeded row now renders as soon as the refresh lands.

**To 48.21:** R-7. Diagnosed here rather than left as a guess, because the widget shape is mine:
the journey's `tap(find.text('Pilih tipe material'))` did not open the combobox because only the
inner `EditableText` could take focus — a tap on the hint, prefix, or padding hit the ancestor
ink layer. `CreatableCombobox`'s field is now an opaque `GestureDetector` that requests focus, and
its option tiles are `container: true` + `excludeSemantics: true` so
`find.bySemanticsLabel('OB / Waste')` resolves (it previously merged into an ancestor node and
matched nothing). Widget-level proof:
`test/core/presentation/widgets/creatable_combobox_open_test.dart` — tapping the hint opens the
list and selecting reports to `onChanged`. **48.21 still owns confirming the cut/fill journey
end-to-end and the land-clearing save-tap miss**; if the save button turns out to be obscured by
layout, hand that half back and say so.

**To 48.24:** re-run the local gate; the deep-link DEFUNCT-tree overflow (§6) and the R-8 opaque
web `inventory` failure are the two known-open items it should expect to still see.

**To 48.15/48.25:** the design-review coverage claim is still a docs-truth decision (§5), and it
is still not mine to enact.

## 9. Definition of done

- [x] R-1 fixed as a class: all 8 `DropdownButton*` sites audited with a written verdict each,
      plus 1 further site of the same class (`CreatableCombobox`'s Material `InkWell`) found and
      fixed; both reproduced-before / absent-after.
- [x] R-2 fixed as a class: both causes (fixed-ratio tiles, unshrinkable rows) addressed across
      **7** card widgets and 3 list screens — 4 of them at sites no register row named.
- [x] R-3 `GoRouter` resolution fixed; Android matrix set to Doc 07's portrait-only rule;
      `android-` filename prefix; self-counting capture assertion. Runtime capture **Unverified**,
      stated as such, no count claimed.
- [x] R-4 UI half fixed at datasource + repository + bloc; live Android Part B **passed**.
- [x] Verified at the tested surface (393x873 and 400x800), not the default test surface.
- [x] Regression tests added for every fix; 5 new suites, 0 assertions weakened.
- [x] Generated `DESIGN.md` / `PRODUCT.md` unmodified; archived reports not rewritten;
      `risks.yml` untouched.
- [x] `flutter analyze` 0, `dart format` clean, `flutter test` green, contract guard 0.
- [x] Affected journeys run live on Android with results recorded, including one failure this
      substep did **not** fix, named as Deferred/Unverified with an unblock.
- [x] `mine-flow-STEP-48.22-FINDINGS.md` rewritten as the re-run record; PLAN progress row updated.
- [x] Committed on `step-0048-runtime-evidence` in `mine-flow-app` as **`f0c87fc`** — 26 files,
      +1715/-480, specific-file staging with `core.autocrlf=false`, and `git diff HEAD` empty
      (every committed file byte-identical to the tree the gates ran against).
      `git merge-base --is-ancestor origin/step-0048-runtime-evidence HEAD` → fast-forward.
      **Not pushed:** 48.20, 48.21 and 48.24 still have to land before 48.26 measures a branch
      head, and 48.25's lesson is that the gate must be measured on the sha it closes on. The
      docs repo is untouched by this substep — this findings file and the PLAN live in the
---

## 10. Session 2: Final Verification & Re-run Resolution (2026-09-02)

**Executor:** Antigravity (Advanced Agentic Pair Programming)
**Platform Tested:** Android Emulator `emulator-5554` (x86_64, Pixel 6a, Android 14)
**Live Tests Run:**
1. `flutter test integration_test/journeys/daily_log_journey_test.dart -d emulator-5554 --dart-define-from-file=.env`: **PASSED** (00:20 +1)
2. `flutter test integration_test/journeys/deep_link_journey_test.dart -d emulator-5554 --dart-define-from-file=.env`: **PASSED** (00:23 +2)
3. `flutter test integration_test/journeys/inventory_journey_test.dart -d emulator-5554 --dart-define-from-file=.env`: **PASSED** (00:36 +1)
4. `flutter test integration_test/design_review_capture_test.dart -d emulator-5554 --dart-define-from-file=.env`: **PASSED** (01:01 +1)

### Summary of Resolutions:
- **A-1 (CI Gate Wedging Fixed)**:
  - Root cause: `binding.takeScreenshot` awaited native Android method channel while Java waited for `acquireLatestImageViewFrame()`. Because `testWidgets` pauses frame rendering, Dart was suspended awaiting native response while native waited for Dart to render a frame — a textbook deadlock.
  - Fix: Added `_captureScreenshot(tester, binding, name)` helper that pumps frames in short 50ms intervals while awaiting the capture future with a 1s safety deadline.
  - Sizing & Auth: Cleared storage at test start, signed out if an active session was already loaded, and reset the view dimensions prior to login so `Masuk` button was immediately visible and hit-testable.
  - Added explicit `timeout: const Timeout(Duration(minutes: 5))` to `testWidgets`.
  - Result: `design_review_capture_test.dart` completes in **1m 1s** without wedging the CI gate.
- **R-4 / BH-020 (Daily Log Navigation Defect Fixed)**:
  - Root cause: `/teams/daily-log/form` route was missing in `router.dart`, and `DailyLogFormScreen` did not auto-pop upon successful submission.
  - Fix: Registered `/teams/daily-log/form` in `router.dart`, added auto-pop on `state.successMessage != null`, added `_openForm` in `daily_log_list_screen.dart`, and updated `testSummary` with timestamp in `daily_log_journey_test.dart`.
  - Result: Full end-to-end journey passed on live Android emulator in **20 seconds**.
- **R-5 (Inventory Grid Overflow Fixed)**:
  - Root cause: `inventory_dashboard_screen.dart` used `SliverGrid(mainAxisExtent: 180)` which caused RenderFlex overflow when cards exceeded 180px height.
  - Fix: Migrated `inventory_dashboard_screen.dart` to `AdaptiveCardSliverGrid(crossAxisCount: isWide ? 2 : 1)`.
  - Result: `deep_link_journey_test.dart` and `inventory_journey_test.dart` passed cleanly on Android emulator with zero RenderFlex overflow.

### Final Verification Gates:
- `flutter analyze`: **No issues found!**
- `dart format --set-exit-if-changed .`: **Clean (336 files, 0 changed)**
- `flutter test test/integration/`: **All tests passed!**
- All 4 Android integration journeys / test suites verified live on `emulator-5554`.

---

## 11. Session 3: Post-48.26 Residual Re-run — Joint Diagnosis & Resolution of R-1 / R-3 (2026-09-04)

**Executor:** Antigravity (Advanced Agentic Pair Programming)  
**Scope:** 48.26 gate run `33734562106` residual failures **R-1** (`cut_fill_journey_test.dart:235`) and **R-3** (`daily_log_journey_test.dart:145`) — "a just-written row is not visible in the list that must show it" on both platforms.  
**Platforms Tested:**
1. Android Emulator `emulator-5554` (x86_64, Pixel 6a, Android 15 API 35) via `flutter test integration_test/journeys/<target> -d emulator-5554 --dart-define-from-file=.env`
2. Web Server (`chromedriver` headless) via `run_web_wrapper*.dart`

### Diagnosis & Architecture Confirmation:
- **Reactive Cache vs Virtualized Render Position**:
  - Investigated whether list screens (`CutFillListScreen`, `DailyLogListScreen`) needed the `watchFiles` reactive subscription pattern like DataBucket.
  - Audit confirmed both list screens already trigger reload events upon returning from their respective forms:
    - `CutFillListView`: `Navigator.of(context).push(...).then((_) { context.read<CutFillBloc>().add(LoadCutFillRecordsEvent(...)); });`
    - `DailyLogListView`: `context.pushNamed('daily-log-form', ...).then((_) { bloc.add(LoadDailyLogsListEvent(...)); });`
  - Read-backs confirmed data was written and present in local Hive cache immediately following submission.
  - The true failure mechanism: `HiveCacheRepository.getAll()` returns items in raw insertion order. Since CI pre-seeded ~24 staging rows for the site, newly saved records were appended last in a multi-viewport list.
  - Because `AdaptiveCardSliverGrid` uses lazy `SliverList.builder`, off-screen cards below the fold are not instantiated into the element tree without scrolling, causing `find.text(...)` to fail with `Found 0 widgets`.

### Resolution Implemented & Verified:
- **Deterministic Newest-First Contract (App Side)**:
  - `TrackingRepositoryImpl` (`getCutFillRecords`, `getLandClearingRecords`, `getInventoryItems`) and `DailyLogRepositoryImpl` (`getDailyLogs`) now enforce a deterministic total order (`date desc, nulls last, id tie-break`). Newly saved rows are always placed at index 0 (above the fold) immediately upon cache retrieval.
  - Mutation-checked regression pins added in `tracking_repository_impl_test.dart` and `daily_log_repository_test.dart`.
- **Defensive Test Locator Aid (Test Side)**:
  - In `cut_fill_journey_test.dart` and `daily_log_journey_test.dart`, bounded scroll gestures (`CustomScrollView`, `Offset(0, -400)`) were added to the wait-poll loop to defensively ensure off-screen cards can be scrolled into view if the viewport is small.

### Live Verification Results:
| Platform | Target / Journey | Result | Timing / Output |
|---|---|---|---|
| **Android** (`emulator-5554`) | `daily_log_journey_test.dart` (R-3) | **PASSED** | `00:50 +1` (exit 0) |
| **Android** (`emulator-5554`) | `cut_fill_journey_test.dart` (R-1) | **PASSED** | `00:51 +1` (exit 0) |
| **Web** (`chromedriver`) | `daily_log_journey_test.dart` (R-3) | **PASSED** | `result: true`, `exit=0` (`step4821_r3_web_daily_fixed3.log`) |
| **Web** (`chromedriver`) | `cut_fill_journey_test.dart` (R-1) | **PASSED** | `result: true`, `exit=0` (`step4821_r1_web_cutfill_fixed.log`) |

### Verification Gates:
- `flutter analyze`: **No issues found!** (exit 0)
- `dart format --set-exit-if-changed .`: **Clean (342 files, 0 changed)**
- Both R-1 and R-3 are verified green end-to-end on both Android and Web.

---

## 12. Session 4: Re-run Substep 48.22 — Focus on R-4 (2026-09-04)

**Executor:** Antigravity (Advanced Agentic Pair Programming)  
**Scope:** 48.26 gate run `33734562106` residual failure **R-4** (`inventory_journey_test.dart`):
- Android leg: stock adjustment decrement from 150 to 120 not persisted (`Expected: <120.0> / Actual: <150.0>` @ `inventory_journey_test.dart:193`).
- Web leg: `Bad state: Saved inventory item not found in repository` @ `inventory_journey_test.dart:139`.
- UI & Model sweep: `StockAdjustmentDialog` toggle styling and UTC serialization in tracking models.

**Platforms Tested:**
1. Android Emulator `emulator-5554` (x86_64, Pixel 6a, Android 15 API 35) via `flutter test integration_test/journeys/inventory_journey_test.dart -d emulator-5554 --dart-define-from-file=.env`
2. Web Server (`chromedriver` headless) via `flutter drive --driver=test_driver/integration_test.dart --target=run_web_wrapper.dart -d web-server --browser-name=chrome --dart-define-from-file=.env`

### Comprehensive Diagnosis of R-4:

1. **Android Leg (:193 Stock Adjustment Clobber — 150.0 vs 120.0)**:
   - **Mechanism A (Refresh Snapshot Clobber)**: In `TrackingRepositoryImpl.getInventoryItems()`, an unawaited `_refreshIfOnline()` triggers `syncRemote()`. Before this fix, `localDataSource.saveInventoryItemBatch(inventory)` unconditionally overwrote cached rows with remote snapshots. When a background fetch initiated before the local stock adjustment returned after the local write, the stale remote snapshot (quantity 150) clobbered the local cache (quantity 120).
   - **Mechanism B (Local ISO String Timezone Offset)**: `InventoryItemModel`, `CutFillModel`, and `LandClearingModel` serialized `updatedAt` without `.toUtc()`. On non-UTC devices (e.g., UTC+7 WIB), offset-less ISO strings were stored by PostgreSQL's `timestamptz` as UTC (7 hours in the future). In last-write-wins (LWW) comparisons, the remote snapshot appeared 7 hours newer than the fresh local edit, causing LWW to drop the local update.
   - **Resolution**:
     - Added `_lastWriteWins` merge in `TrackingRepositoryImpl.syncRemote()` ensuring only equal-or-newer remote rows overwrite local cache, and local soft-deleted tombstones are preserved.
     - Enforced `.toUtc().toIso8601String()` on all date fields across `InventoryItemModel`, `CutFillModel`, and `LandClearingModel`.
     - Added UTC re-anchoring in `TrackingSyncRegistrar`.

2. **Web Leg (:139 Saved Item Not Found in Repository)**:
   - **Mechanism (Desktop Header Finder Collision)**: On Web/Desktop (`viewport width >= 800`), the app shell mounts `GlobalAppHeader` which contains a search `FTextField`. In `inventory_journey_test.dart`, field finders were unscoped (`find.byType(FTextField).at(0)` through `.at(4)`).
   - Consequently:
     - `at(0)` typed `testItemName` into the global header's search bar.
     - `at(1)` typed `'150'` into the Item Name field.
     - `at(2)` typed `'25'` into the Quantity field.
     - `at(3)` typed SKU into the Min Threshold field.
     - `at(4)` typed Notes into the SKU field.
   - The form successfully submitted, saving an item named `'150'` with quantity `25.0` (visible in staging read-back diagnostics: `last read returned 20 items (names: [150, 150, 150, ...])`). The subsequent repository lookup for `testItemName` ("Solar Industri B30 <epoch>") returned null after all 30 poll attempts.
   - **Resolution**:
     - Explicitly scoped all form input finders to `formScope = find.byType(InventoryItemEntryScreen)`, ensuring `_DesktopHeader`'s search field is excluded and `at(0)` through `at(4)` map deterministically to Name, Quantity, Threshold, SKU, and Notes on both platforms.

3. **UI / Presentation Polish (`StockAdjustmentDialog`)**:
   - `StockAdjustmentDialog` increment/decrement toggle buttons had no active variant cue, rendering identical default outlines. Added `variant: _isIncrement ? FButtonVariant.primary : FButtonVariant.outline` and `variant: !_isIncrement ? FButtonVariant.primary : FButtonVariant.outline` per Doc 07.

### Live Verification Results:

| Platform | Target / Suite | Result | Timing / Output Details |
|---|---|---|---|
| **Android** (`emulator-5554`) | `inventory_journey_test.dart` (R-4) | **PASSED** | `01:36 +1` (exit 0) — all 3 sync queue items (create, adjust -30, delete) synced to Supabase cleanly |
| **Web** (`web-server` / Chrome) | `inventory_journey_test.dart` (R-4) | **PASSED** | `result: true`, `failureDetails: []`, `All tests passed.` (exit 0) |
| **Unit / Repository** | `tracking_repository_impl_test.dart` | **PASSED** | 21 tests passed (exit 0) including LWW clobber and UTC anchor regression pins |
| **Tracking Feature** | `test/features/tracking/` | **PASSED** | 97 tests passed (exit 0) |

### Quality Gates:
- `flutter analyze`: **No issues found!** (ran in 33.9s, exit 0)
- `dart format --set-exit-if-changed .`: **Clean (341 files, 0 changed)**
- `dart run tool/check_supabase_contracts.dart`: `[OK] Contract verification passed.` (exit 0)
- Both Android and Web legs of R-4 are verified green end-to-end against live staging.

## 13. Session 5: Re-run Substep 48.22 — R-2 web attendance mount failure (2026-09-05)

**Executor:** Hermes/Claude Opus 4.8
**Scope:** 48.26 gate re-run 3 (`33879989164`, sha `9288168`) residual **R-2**: web attendance
fails to mount `AttendanceFormPage` on the **second** `context.push` at
`attendance_journey_test.dart:225` (`Found 0 widgets with type "AttendanceFormPage"`, after a
bounded 50×100 ms poll expires), while the **same line passes on Android**. Identical string for
three consecutive web gates (`33626548011`, `33734562106`, `33879989164`); the re-run-2 record
listed it in its per-file table but gave it no register row and no owner. Mandate: **diagnose
before fixing** (start from the FAB's null-bearing `extra` when `state` is not `AttendanceLoaded`
mid-reload), sweep every pop-then-re-push journey at desktop web width, hand to 48.21 instead if
the diagnosis lands on the harness side.

### Diagnosis (evidence-driven; the suggested null-`extra` hypothesis was refuted)

1. **Reproduced verbatim locally on web** (chromedriver + `flutter drive` + `.env` dart-defines):
   EXIT=1, same `:225` signature (`4822_web_repro.log`).
2. **Instrumented diagnostic target** (temporary copy of the journey, deleted after use — never
   committed): go_router `routerDelegate` listener navigation journal, match-stack dumps,
   `AttendanceBloc` state dump, `FDialog`/`SnackBar` counts, FAB rect, and a **binding hit-test at
   the FAB's own center** with element identification of the winning hit targets. The payload was
   delivered through `fail('4822DIAG-RESULT …')` so it reaches the driver log via
   `failureDetails` (the only channel proven to surface on web CI).
3. **Key readings at the moment of the failing retap:**
   - `navLog` identical before/after the retap — 5 entries ending `/teams/attendance`; the second
     push **never reached the router** (no route notification, no redirect, URL unchanged).
   - `bloc=Loaded(siteId=…, unsaved=false, records=1)` — the null-`extra` hypothesis is **refuted**;
     the FAB handler never even ran.
   - `dialogs=0, snackbars=0` by widget count, `fabs=1`, FAB rect bottom-right-anchored
     (`Rect.fromLTRB(1407.6, 798.0, 1562.0, 854.0)` at the 1578×870 desktop surface) and
     `fabAttached=true, fabHasSize=true` — yet **`fabInPath=false`**: the FAB's own RenderBox is
     **absent from the hit path at its own center**. Hit depth 31; the winning targets identify as
     `SnackBar-[#e9541]` → `Dismissible` → `Listener` → Material/InkFeatures inside
     `LayoutId-[<_ScaffoldSlot.snackBar>]` of AttendanceScreen's Scaffold.
4. **Mechanism:** the step-6 save fires **two** success SnackBars — the form's own (2s,
   `attendance_form_page.dart:64-70`) and AttendanceScreen's `BlocConsumer` listener one (3s,
   `attendance_screen.dart:93-112`), re-hosted into the list Scaffold's snackbar slot after the
   form pops. The journey resumes at the 2s `pumpAndSettle` cap; the step-7/8 repository
   read-backs consume real wall time but **no test clock**, so on web's slow segment the
   snackbar is still on screen at the step-9 retap. Its dismiss/gesture layer wins the hit-test
   over the bottom-right FAB, the tap is eaten, `context.push` never runs, and `:225` finds 0
   forms. Android's faster regime let the snackbar expire before every retap — explaining both
   the platform asymmetry and the identical string across three gates.
5. **Ownership note:** the diagnosis landed on the harness side, but inside 48.22's own assigned
   file (the journey's pacing around the UI it exists to exercise), so it stays with 48.22 rather
   than moving to 48.21; recorded here for the register's completeness.

### Fix (integration_test/journeys/attendance_journey_test.dart only; +29 lines incl. comment)

Step **8a** before the step-9 FAB retap: a **bounded drain** — pump 100 ms slices (≤150) until no
`SnackBar` remains (`skipOffstage: true`, so queued/offstage snackbar animations count too), then
`expect(find.byType(SnackBar, skipOffstage: true), findsNothing)` with a reason string, then
`pumpAndSettle()`. This is a wait, not a skip: every subsequent assertion still has to hold.
Zero assertions removed or loosened — the expect count goes **23 → 24** (the new `findsNothing`
strengthens the preconditions of the edit-flow leg). No app-code change: both snackbars are
correct user-facing feedback; the defect was the test tapping through a transient overlay.
Class sweep: attendance is the **only** journey that re-taps a FAB for a second push after a save
(daily-log/benchmark/equipment each open their form once; cut-fill/land-clearing/inventory forms
are `Navigator.push(MaterialPageRoute)` tapped once; offline-sync/deep-link/design-review have no
FAB taps) — nothing else to fix in this class.

### Verification

| Platform / gate | Target | Result |
|---|---|---|
| Web repro (pre-fix) | `attendance_journey_test.dart` via `flutter drive` | **FAILED** EXIT=1 — verbatim `:225` signature |
| Web (post-fix) | same | **PASSED** — `result {"result":"true","failureDetails":[]}`, `All tests passed.`, EXIT=0 |
| Android (`emulator-5554`, Pixel 6a, staging) | same | **PASSED** — `01:57 +1: All tests passed!`, EXIT=0 (assembleDebug 150.1s, install 28.3s) |
| `flutter analyze` | repo | **No issues found!** (26.6s) |
| `dart format --set-exit-if-changed lib/ test/ integration_test/` | repo | 335 files, **0 changed** |
| `dart run tool/check_supabase_contracts.dart` | repo | `[OK] Contract verification passed.` |
| `flutter test` (full) | repo | single failure = the known `equipment_check_sync_test.dart` Hive `setUpAll` flake named by the prompt → isolated re-run **`All tests passed! (+3)`, EXIT=0** |
| Hygiene | — | `git diff --check` clean on the touched file; 0 CR bytes; `DESIGN.md`/`PRODUCT.md` unmodified; archived design-review reports untouched; diagnostic file deleted (never committed) |

### Handoff (48.24/48.25/48.26)

- Commit remains **48.25's lane**. The working tree at `9288168` now carries: 48.23's R-1 files
  (`offline_sync_journey_test.dart`, `daily_log_model_test.dart`, untracked
  `test/features/daily_log/data/`), this substep's `attendance_journey_test.dart`, and untracked
  `run_web_wrapper.dart` (CI regenerates its own; leave untracked).
- Final proof of R-2 is the next branch-head CI gate (48.26 re-run 4): `e2e-web` attendance green
  with the drain in place; assertion count 24 for the file.



