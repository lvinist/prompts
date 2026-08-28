# mine-flow — STEP-47.3: `bloc` 9 / `flutter_bloc` 9 / `bloc_test` 10 migration

> **How to run:** Tell your agent *"run substep 47.3"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.1 Pro High. The change is narrow but touches ~53 source files and 11 test
> suites; the risk is a silent behaviour change in a state emission, not a compile error.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`. Substep 47.1 swept the dependency
graph while fixing the AGP-9 build, moving `flutter_bloc` 8.1.6 → 9.1.1, `bloc` 8.1.4 → 9.2.1, and
`bloc_test` 9.1.7 → 10.0.0.

bloc is the app's state-management spine: **~53 files under `lib/` and `test/` reference it**, and
**11 test suites use `bloc_test`**. The upgrade is a major, so it must be verified rather than
assumed — but the changelogs say the breaking surface is small:

**`bloc` 9.0.0**
- **BREAKING** introduces `EmittableStateStreamableSource`; `BlocBase<State>` now implements it
- **BREAKING** removes the deprecated `BlocOverrides` API
- internal: uses `Object.hashAll`

**`flutter_bloc` 9.0.0**
- fix: ensures the widget is mounted before invoking a listener
- depends on `bloc ^9.0.0`

**`bloc_test` 10.0.0**
- `blocTest` now depends on the core interfaces instead of `BlocBase` directly

A grep during planning found **zero** `BlocOverrides` and **zero** `BlocObserver` references in this
codebase, so the loudest breaking change probably does not apply here. **Verify that yourself** —
planning-time greps go stale.

The subtle one is `flutter_bloc`'s mounted-check fix. A `BlocListener` that previously fired during
teardown now does not. If any widget test asserted on a listener side effect that happened after
dispose, it will now fail — and that failure is *correct*, but it needs a deliberate test update,
not a shrug.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — the baseline is `flutter test` **442 passing**
  with one known order-dependent flake. Anything below 442 is a regression until proven otherwise.
- 47.1's analyze log — your bucket is the bloc-related errors
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — tiers, and `mocktail` as the mocking tool
- `Code/mine-flow-docs/architecture/03-architecture-overview.md` — the Clean Architecture layering
  bloc sits in; keep cubits/blocs in the presentation layer
- `Code/mine-flow-app/README.md`
- The 11 `bloc_test` suites:
  `test/features/benchmark/presentation/benchmark_bloc_test.dart`,
  `test/features/data_bucket/presentation/bloc/data_bucket_bloc_test.dart`,
  `test/features/data_bucket/presentation/bloc/data_bucket_upload_cubit_test.dart`,
  `test/features/notifications/presentation/pages/notification_list_page_test.dart`,
  `test/features/notifications/presentation/widgets/notification_banner_test.dart`,
  `test/features/reporting/presentation/bloc/report_cubit_test.dart`,
  `test/features/settings/presentation/settings_cubit_test.dart`,
  `test/features/timeline/presentation/bloc/timeline_cubit_test.dart`,
  `test/features/tracking/presentation/cut_fill_bloc_test.dart`,
  `test/features/tracking/presentation/inventory_bloc_test.dart`,
  `test/features/tracking/presentation/land_clearing_bloc_test.dart`

## Scope

**Owns:** every `lib/` and `test/` file whose breakage traces to bloc/flutter_bloc/bloc_test.

**Does NOT touch:** `pubspec.yaml` (47.1), `upload_file_page.dart`'s file_picker migration (47.2 —
note the *cubit test* for data_bucket is shared, so coordinate: if 47.2 already tightened it, build
on that rather than reverting), `go_router`/`googleapis`/`proj4dart`/lints work (47.4), `android/**`,
`ci.yml`, docs.

**Not a refactor licence.** Do not restructure state classes, rename events, convert Blocs to Cubits,
or "modernize" emissions. Migrate, verify, stop.

## Your task

### 1. Establish the actual breakage

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
flutter analyze 2>&1 | tee "$LOCALAPPDATA/Temp/step47-3-analyze-before.log"
grep -rn "BlocOverrides\|BlocObserver\|Bloc.observer\|Bloc.transformer" lib/ test/ --include=*.dart
grep -rln "flutter_bloc\|package:bloc/" lib/ test/ --include=*.dart | wc -l
```

If the `BlocOverrides`/`BlocObserver` grep is empty (expected), record that — it means bloc 9's
headline breaking change is a no-op here, and you can say so with evidence instead of hedging.

### 2. Migrate source (`lib/`)

Work through the analyzer errors attributable to bloc. Likely categories:

- **`emit` after close / `EmittableStateStreamableSource`** — if any code held a `BlocBase` in a
  variable typed loosely, or implemented a custom base, the interface change may surface. Fix by
  typing against the interface, not by casting.
- **`hashCode` / `props`** — `bloc` 9 uses `Object.hashAll` internally. This codebase uses
  `equatable` (`props` overrides throughout). Watch for any state class that relied on old identity
  behaviour; a state that no longer compares equal will show up as a *duplicate or missing emission*
  in `bloc_test`, not as a compile error.
- **Nothing at all** is a plausible outcome for `lib/`. If so, say so explicitly rather than
  inventing changes to look busy.

### 3. Migrate the 11 `bloc_test` suites

`blocTest` in 10.0.0 accepts core interfaces rather than `BlocBase`. Most suites should compile
unchanged. Where one does not, the usual cause is a `MockBloc`/`MockCubit` from `mocktail` whose
declared type no longer satisfies the new bound — fix the type, don't loosen the assertion.

For each suite, run it in isolation before running the whole file set:

```bash
flutter test test/features/benchmark/presentation/benchmark_bloc_test.dart
# … and so on for all 11
```

**Failure triage rule (from STEP-46's flake experience):** if a suite fails, re-run it *in isolation*
before deciding. A failure that reproduces in isolation is a regression you must fix. A failure that
only appears in a full-suite run is an ordering interaction — record it, and do not label it "flaky"
without an isolated re-run proving it.

### 4. Watch for the mounted-listener behaviour change

`flutter_bloc` 9.0.0 "ensure widget is mounted before invoking listener". Search for tests that
assert a `BlocListener` side effect around teardown:

```bash
grep -rn "BlocListener\|listenWhen\|BlocConsumer" lib/ test/ --include=*.dart | head -30
```

If a widget test now fails because a listener no longer fires after dispose, the *new* behaviour is
correct — update the test to assert the corrected behaviour, and note it in your status update. Do
not add a `pumpAndSettle` or an artificial delay to force the old behaviour back.

### 5. Verify and commit

```bash
flutter analyze
dart format --output=none --set-exit-if-changed lib/ test/
flutter test 2>&1 | tail -25
```

Target: analyze reports **no bloc-related issues** (47.2/47.4 issues may remain if those substeps
have not landed — attribute clearly), and every `bloc_test` suite passes. Once 47.2 and 47.4 are also
done, `flutter test` must reach **≥442 passing**.

```bash
git -C /d/AppDev/mine_flow/Code/mine-flow-app add lib/ test/
git -C /d/AppDev/mine_flow/Code/mine-flow-app commit -m "refactor(STEP-47.3): migrate to bloc 9 / flutter_bloc 9 / bloc_test 10"
```

Stage deliberately — `git add lib/ test/` will also pick up 47.2's or 47.4's work if you share a
worktree. Check `git status` first and stage only your own files.

## Verification

- `grep -rn "BlocOverrides\|Bloc.observer" lib/ test/` returns nothing.
- All 11 `bloc_test` suites pass individually **and** in a full-suite run.
- No test assertion was weakened, deleted, or `skip`ped to get green. If a test genuinely must
  change because bloc 9's behaviour is different, the new assertion must be *stricter or equal* and
  the reason recorded.
- `flutter test` count is ≥442 once the sibling substeps land; report the number you actually see.
- No `Bloc`→`Cubit` conversions, no event/state renames, no state-class restructuring.

If you cannot get a suite green, mark it **Unverified** with the failing output and the diagnosis.
Do not `skip` it and call the substep done — a skipped test that looks green is precisely the failure
mode STEP-45 was corrected for.

## Keeping the docs true (always)

bloc's major version is an implementation detail of the presentation layer; the layering in
`architecture/03-architecture-overview.md` does not change, so no doc edit or ADR here.

For 47.8's status note, record: (a) whether bloc 9's `BlocOverrides` removal affected anything
(expected: no), and (b) any test whose assertion changed because of `flutter_bloc` 9's
mounted-listener fix — that is a real behaviour change worth one line in the STEP record.

No secrets touched.

## Definition of done

- [ ] `flutter analyze` shows no bloc-attributable issues
- [ ] All 11 `bloc_test` suites pass in isolation and in the full run
- [ ] Any test change caused by the mounted-listener fix is documented, not worked around
- [ ] No assertion weakened, deleted, or skipped; no suite left `Unverified` without a diagnosis
- [ ] `dart format` clean
- [ ] `flutter test` count reported honestly against the 442 baseline
- [ ] No files outside this substep's bucket staged or committed
- [ ] Committed on `step-0047-android-build-chain`
- [ ] Notes for 47.8 written

## Next

Update 47.3's status in the PLAN. If 47.2 or 47.4 remain, they run next (fresh chat each). When
47.2 + 47.3 + 47.4 are all done, the next action is **run substep 47.5**.
