# mine-flow — STEP-48.22: UI & Harness Defect Fixes (overflow, Material ancestor, Drive guard, Android screenshots)

> **How to run:** tell your agent *"run substep 48.22"*. Self-contained — runnable cold.

**Assigned model: GPT 5.6 Luna.** Four mechanical, self-evidencing fixes: each is reported by the
framework at a named file and line, and each is confirmed fixed by the error no longer appearing. No
judgement call about honesty is the deliverable here, which is why this is the cheap tier.
**Escalate to Opus 4.8** if a fix would require deviating from `architecture/07-ui-design-system.md`
(the review must not silently change the design to match code), or if the same fix fails twice.

## Why this substep exists

Branch-head CI run [`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159)
failed both E2E jobs. Four of the causes are application or harness defects that the framework names
outright:

**1. Layout overflow, fired twice on Android**

```
══╡ EXCEPTION CAUGHT BY RENDERING LIBRARY ╞══
The following assertion was thrown during layout:
A RenderFlex overflowed by 21 pixels on the right.
  Row:file:///…/lib/features/timeline/presentation/pages/timeline_page.dart:289:9
```

That `Row` holds the timeline's summary `_StatBadge`s ("Berjalan", "Selesai", …). At a narrow width
the badges do not fit. It fired in the timeline journey and again in the design-review capture run.

**2. Material ancestor missing in the cut/fill form**

```
══╡ EXCEPTION CAUGHT BY WIDGETS LIBRARY ╞══
The following assertion was thrown building DropdownButton<String>(dirty, …):
No Material widget found.
DropdownButton<String> widgets require a Material widget ancestor within the closest LookupBoundary.
```

The cut/fill form uses `DropdownButtonFormField<String>` for material type
(`cut_fill_journey_test.dart` taps `find.byType(DropdownButtonFormField<String>)`), and it sits inside
a ForUI tree with no `Material` ancestor. This is a survivor of the STEP-37 Material purge.

**3. `UploadFilePage` throws on navigation**

```
══╡ EXCEPTION CAUGHT BY WIDGETS LIBRARY ╞══
The following UnimplementedError was thrown building UploadFilePage(dirty):
GoogleDriveService not wired and no driveService provided.
  upload_file_page.dart:59  ·  routed at router.dart:183
```

This throw is **deliberate** — CF-018 chose it over fabricating an empty-credential Drive client. But
it crashes the **deep-link** journey, which does nothing but navigate past that route, and it would
crash any real deployment where Drive is not configured. See Q11.

**4. Android screenshot capture never worked**

```
Bad state: Call convertFlutterSurfaceToImage() before taking a screenshot
  integration_test/design_review_capture_test.dart:30
```

`design_review_capture_test.dart` fails on Android at the very first `takeScreenshot`. The 73 images
committed under `reports/design-review/step-0048/` are therefore **web-only** — 48.13's 3×2×2 matrix
was never captured on Android at all, even though `architecture/07-ui-design-system.md` says Android
locks to portrait mobile and is a distinct target.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, decision **D2** (Drive out
  of scope), and question **Q11** (which carries the recommendation for `UploadFilePage`).
- **`Upcoming Prompts/mine-flow-STEP-48.16-FINDINGS.md`** — your scope: the `BH-nnn` rows classified
  **app-defect / UI-harness**. Only those.
- `Upcoming Prompts/mine-flow-STEP-48.13-FINDINGS.md` and
  `Code/mine-flow-docs/reports/2026-08-30-step-0048-runtime-design-review.md` — what the design review
  claimed. Its coverage table says "Web (Phone, Tablet, Desktop)" throughout; your fix determines
  whether an Android leg can be added, and **48.25/48.15 must know** whether the report's coverage
  claim needs narrowing. Do not rewrite that report — record the fact and hand it forward.
- `Upcoming Prompts/mine-flow-STEP-48.9-FINDINGS.md` — the timeline work; the overflow is in the file
  it touched.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-docs/architecture/07-ui-design-system.md`** — the canonical UI contract: Compact
  density with ForUI spacing tokens, adaptive layouts, "Web relies on standard breakpoints for sidebar
  expansion; Android locks to portrait mobile", Sidebar (Web) + 5-item Tab Bar (Mobile) per
  **ADR-0009**.
- `Code/mine-flow-docs/adr/ADR-0016-lucide-icon-migration.md` and the other UI ADRs — relevant if you
  replace a widget rather than wrap it.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0003** (accepted Phase 2 spacing/colour drift)
  and **RISK-0017/0018** (Drive upload behaviour, deferred by D2). Do not close or re-scope these;
  recommend only.
- The four sites themselves: `lib/features/timeline/presentation/pages/timeline_page.dart` around
  line 289; the cut/fill form page; `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
  and `lib/app/router.dart:183`; `integration_test/design_review_capture_test.dart` and
  `test_driver/integration_test.dart`.

## Your task

### 1. Timeline overflow

Fix the `Row` at `timeline_page.dart:289` so the summary badges fit at the narrowest supported width.
Use `architecture/07-ui-design-system.md`'s spacing tokens and the file's existing `_kSpacing*`
constants — do not introduce new magic numbers. `Expanded`/`Flexible`, a `Wrap`, or a horizontal
scroll are all plausible; pick the one that keeps the design's intent (the badges are a compact
summary row, not a list) and say why.

Add a **widget regression test** that renders the page at a narrow surface and asserts no overflow.
Use `tester.binding.setSurfaceSize(const Size(400, 800))` — the default 768px test surface is wider
than the phone breakpoint and would not have caught this.

### 2. Material ancestor in the cut/fill form

Two honest routes:

- **Replace** `DropdownButtonFormField` with the ForUI equivalent the design system prescribes. This
  is the better outcome — STEP-37 purged Material for a reason, and a stray Material widget in a ForUI
  form is drift from Doc 07. Check what sibling forms use for the same job (the land-clearing form's
  method combobox, the `CreatableCombobox` pattern) and match it.
- **Wrap** the subtree in a `Material` (or the minimal `flutter_localizations`-scoped Material shell
  this project already uses for Material-inside-ForUI cases). Faster, but it leaves the drift in place.

Prefer replacement. If you wrap instead, record it as accepted drift with a reason and check whether
it belongs under RISK-0003. Either way, `cut_fill_journey_test.dart` currently finds the control via
`find.byType(DropdownButtonFormField<String>)` — if you replace the widget, the finder must be updated
in the same commit, **without weakening what it asserts** (it must still select "OB / Waste" and prove
the selection took).

Note for whichever route you choose: Material widgets inside ForUI builders need an explicit
`flutter_localizations` scope in this codebase — a known pitfall from earlier STEPs.

### 3. `UploadFilePage` — render instead of throwing (Q11)

The PLAN recommends fixing the **page**: a route registered in the router that cannot be built without
an unhandled exception is a defect regardless of any test, and "Drive not configured" is exactly the
state a real deployment may be in (D2 keeps Drive out of scope, and CI has no Drive client id).

Replace the `throw UnimplementedError(...)` at `upload_file_page.dart:59` with a rendered
**unconfigured state**: a clear message that the Drive integration is not configured, in Indonesian
consistent with the rest of the UI, styled with Doc 07 tokens. Do **not**:

- fabricate an empty-credential Drive client (that is what CF-018 rejected, and it would turn a clear
  failure into a confusing one);
- silently `return const SizedBox.shrink()` (a blank screen is a worse defect than a crash);
- remove the route.

Add a widget test asserting the page renders the unconfigured state when no `driveService` is
available, and still builds normally when one is injected. Keep RISK-0017/0018 untouched — real Drive
upload behaviour stays deferred; you are only making the *unconfigured* path survivable.

### 4. Android screenshot capture

`IntegrationTestWidgetsFlutterBinding.takeScreenshot` requires
`await binding.convertFlutterSurfaceToImage()` **on Android** before the first capture, and that call
must **not** be made on web. Read `design_review_capture_test.dart` and
`test_driver/integration_test.dart` (which currently writes bytes to
`../mine-flow-docs/reports/design-review/step-0048/`) and make the harness work on both platforms:

- guard the conversion by platform (`kIsWeb`);
- call it once, after the app has pumped and before the first `takeScreenshot`;
- respect Doc 07's "Android locks to portrait mobile" — the wide/desktop captures are a **web**
  concern, so the Android matrix is the phone (and possibly tablet) leg, not all three breakpoints.
  State what the Android matrix should be and implement that, rather than forcing a desktop width onto
  a portrait-locked platform.

Then run it on the emulator and confirm images are actually written. **Check the count and the file
names** — a capture test that runs green while writing zero files is exactly the kind of vacuous pass
this STEP exists to eliminate.

Commit the new Android images under `Code/mine-flow-docs/reports/design-review/step-0048/` with
self-describing names in the existing convention (`<screen>-<breakpoint>-<theme>-<locale>.png`), and
consider an `android-` prefix or suffix so they are distinguishable from the web set. No screenshot
may contain credentials, tokens, or sensitive operational data.

Record for 48.25/48.15: whether the design review's coverage claim now extends to Android, or whether
it must be narrowed to web-only. That is a docs-truth item, not yours to rewrite.

## Verification

- Each of the four errors reproduced before the fix and absent after, with commands and output
  recorded.
- Regression tests added for the overflow, the `UploadFilePage` unconfigured state, and (where
  testable) the dropdown replacement; all run and passing.
- Root `DESIGN.md` / `PRODUCT.md` **not modified** — they are generated (`git status` proves it).
- `reports/2026-08-27-step-0045-runtime-design-review.md` and
  `reports/2026-08-30-step-0048-runtime-design-review.md` **not rewritten** — archived reports are
  immutable; hand corrections forward.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean; `flutter test` green
  (the `attendance_daily_log_sync_test.dart` / `equipment_check_sync_test.dart` Hive `setUpAll` flake
  is known: re-run isolated and say so).
- Timeline, cut/fill, deep-link, and design-review-capture runs recorded with ran-vs-skipped counts.
- Android screenshots exist on disk — count and sample file names quoted.
- No assertion weakened anywhere; if you replaced the dropdown, the journey still proves the selection.

## Scope

**In scope:** the four named defects, their regression tests, the Android screenshot leg and its
committed images.

**Not in scope:** migrations (48.17), query column names (48.18), write-path keys (48.19), seed and
fixtures (48.20), finder repair (48.21), persistence/offline defects (48.23), `risks.yml` edits,
rewriting the design-review report, building the privacy notice (RISK-0011 stays open), and real Drive
upload behaviour (RISK-0017/0018, deferred by D2).

## Keeping the docs true

If a fix deviates from `architecture/07-ui-design-system.md`, the runbook is unambiguous: the review
does not silently change the design to match code. An intentional deviation needs an explicit owner
decision and, if material, an ADR plus a Doc 07 Version Log entry — hand that to 48.25/48.15 and the
user rather than enacting it here. New and changed widgets get docstrings; comment the *why* on any
non-obvious layout choice.

## Definition of done

- [ ] `timeline_page.dart:289` overflow gone at the narrowest supported width; regression test added.
- [ ] Cut/fill material-type control resolved (replaced per Doc 07, or wrapped with recorded reason);
      the journey finder updated in the same commit without weakening its assertion.
- [ ] `UploadFilePage` renders an unconfigured state instead of throwing; widget test covers both
      wired and unwired cases; route still registered.
- [ ] Android screenshot capture works (`convertFlutterSurfaceToImage` guarded by platform); images
      written, counted, and committed with self-describing names.
- [ ] Android matrix defined in line with Doc 07's portrait-mobile rule, not copied from web.
- [ ] Design-review coverage correction recorded for 48.15/48.25; the report itself untouched.
- [ ] Generated `DESIGN.md` / `PRODUCT.md` unmodified.
- [ ] `flutter analyze` 0, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] Affected journeys run locally; counts recorded.
- [ ] `mine-flow-STEP-48.22-FINDINGS.md` written; PLAN progress table updated.
- [ ] Committed on `step-0048-runtime-evidence` in both `mine-flow-app` and `mine-flow-docs`.

## Next

Tell the user the next action is *"run substep 48.23"* (persistence & offline-integrity defects, Opus
4.8) in a **fresh chat**. Flag any `lib/` file you touched that 48.23 will reopen.
