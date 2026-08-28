# mine-flow — STEP-47.1: Dependency graph remediation (AGP-9-native plugins, override deletion)

> **How to run:** Tell your agent *"run substep 47.1"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.1 Pro High. This is the substep that unblocks everything else — a wrong
> constraint here costs the whole STEP.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`; 47.0's findings are in
`Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md`. Read both.

The local Android build fails because `package_info_plus` 9.0.1 and `file_picker` 11.0.3 apply the
Kotlin Gradle Plugin **unconditionally**, which AGP 9 rejects. Newer versions of both guard that
apply behind an AGP-major check. But you cannot upgrade just one: all three of
`package_info_plus`, `file_picker`, and `flutter_secure_storage` are coupled through `win32`, and
STEP-43 added a `dependency_overrides` entry pinning `flutter_secure_storage_windows` to 4.0.0
(hence `win32` 5.x) to work around that coupling. **That override is now the blocker.**

This substep changes only dependency metadata. Dart source stays untouched — the resulting
compile errors are real and expected, and 47.2/47.3/47.4 fix them.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md` — "Why this becomes a full dependency sweep"
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — baseline gate numbers you must not regress
- `Code/mine-flow-app/pubspec.yaml` — note the comment block above `dependency_overrides`
  (lines ~111–119) explaining STEP-43's reasoning. You are reversing that decision; understand it first.
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0008** (`flutter_secure_storage` v9→v11 skipped
  the v10 key migration) and **RISK-0009** (forui ≥0.26 / `EditableText` finders)
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — the gate set

## Scope

**Owns:** `pubspec.yaml`, `pubspec.lock`, and the KGP audit of the resolved graph.

**Does NOT touch:** any `.dart` file, `android/**`, `ci.yml`, docs. Do not "helpfully" fix the
compile errors this substep creates — they are 47.2/47.3/47.4's work, deliberately split so a
migration break is attributable to one package family.

## Your task

### 1. Verify the starting graph

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
flutter pub outdated
```

Expect ~29 packages behind, including `package_info_plus` 9.0.1 (10.2.1 available) and `file_picker`
11.0.3 (12.1.1 available), plus a line marking `flutter_secure_storage_windows` as **overridden**.

### 2. Make the three coupled changes together

They must be one edit. Any subset fails to resolve — verified during planning:

- `package_info_plus ^10.2.1` while the override stays → *"flutter_secure_storage_windows >=4.0.0
  <4.2.0 depends on win32 ^5.5.4 and package_info_plus >=10.1.0 depends on win32 ^6.0.1"*
- `file_picker ^12.1.1` while `package_info_plus` stays at 9.0.1 → *"every version of
  windows_file_picker depends on win32 ^6.3.0"*

In `pubspec.yaml`:

1. `file_picker: ^11.0.3` → `file_picker: ^12.1.1`
2. `package_info_plus: ^9.0.1` → `package_info_plus: ^10.2.1`
3. Delete the entire `dependency_overrides:` block, including its `flutter_secure_storage_windows: 4.0.0`
   entry **and** the now-obsolete explanatory comment above it (lines ~111–119). Leaving a comment
   that describes a workaround which no longer exists is documentation drift.

Then:

```bash
flutter pub get
```

Expected resolution (verified in a scratch project during planning):

| Package | Version |
|---|---|
| `file_picker` | 12.1.2 |
| `android_file_picker` | 1.0.3 |
| `windows_file_picker` | 1.1.0 |
| `package_info_plus` | 10.2.1 |
| `flutter_secure_storage` | 11.0.0 (unchanged) |
| `flutter_secure_storage_windows` | 4.2.2 (was pinned to 4.0.0) |
| `win32` | 6.4.0 (was 5.15.0) |
| `dependency_overrides` | **none** |

If resolution fails, **stop and report the solver's exact message.** Do not reintroduce an override
to force it — an override is what caused this.

### 3. Sweep the remaining majors

The user explicitly asked for the full sweep while the graph is open.

```bash
flutter pub upgrade --major-versions
```

Expected to change 7 constraints (verified during planning):

| Package | From | To |
|---|---|---|
| `flutter_bloc` | ^8.1.6 | ^9.1.1 |
| `bloc_test` | ^9.1.5 | ^10.0.0 |
| `go_router` | ^17.3.0 | ^18.0.0 |
| `googleapis` | ^14.0.0 | ^17.0.0 |
| `googleapis_auth` | ^1.6.0 | ^2.3.3 |
| `proj4dart` | ^2.1.0 | ^3.0.0 |
| `flutter_lints` | ^5.0.0 | ^6.0.0 |

Transitively this also moves `bloc` 8.1.4 → 9.2.1, `mgrs_dart` 2 → 3, `unicode` 0.3.1 → 1.1.9, and
adds `google_cloud` + `simple_sparse_list`.

Then confirm:

```bash
flutter pub outdated
```

Target: *"direct dependencies: all up-to-date"* and *"dev_dependencies: all up-to-date"*. A few
transitives (`archive`, `qr`, `package_config`, `material_color_utilities`, analyzer/test family)
stay behind because Flutter's own SDK constraints pin them — that is expected and fine. Record which
ones, so 47.9 doesn't treat them as an unfinished job.

**Guardrails on this sweep:**

- **`forui` stays at ^0.26.0.** RISK-0009: forui ≤0.25 wraps `FTextField` in `MergeSemantics`, which
  trips flutter/flutter#191095 and crashes widget tests. 0.26.0 is the latest published; do not
  downgrade it and do not let the solver do so either. `forui_lucide` 0.26.0 → 0.26.1 is fine.
- **`flutter_secure_storage` stays at ^11.0.0.** RISK-0008 accepted the skipped v10 key migration;
  changing the major would reopen a settled security decision.
- **`supabase_flutter` must not change major.** The contract guard
  (`tool/check_supabase_contracts.dart`) and the committed `supabase/types/database.ts` are keyed to
  it. Verify it resolves to the same major it does today.
- Do **not** hand-edit `pubspec.lock`. Let the solver write it.

### 4. Audit KGP in the resolved graph

The whole point of the upgrade is that no plugin applies KGP unconditionally under AGP 9. Verify it
against what actually resolved, not against what you expect:

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
python - <<'PY'
import re, os, glob
lock = open('pubspec.lock', encoding='utf-8').read()
root = os.path.join(os.environ.get('PUB_CACHE', r'D:\AppDev\.pub-cache'), 'hosted', 'pub.dev')
for name, body in re.findall(r'^  ([a-z0-9_]+):\n((?:    .*\n)+)', lock, re.M):
    v = re.search(r'version: "?([^"\n]+)', body)
    if not v:
        continue
    d = os.path.join(root, f'{name}-{v.group(1)}', 'android')
    if not os.path.isdir(d):
        continue
    for f in glob.glob(os.path.join(d, 'build.gradle*')):
        s = open(f, encoding='utf-8', errors='ignore').read()
        if 'kotlin.android' in s or 'kotlin-android' in s:
            guarded = any(k in s for k in ('agpMajor', 'isAgp9', 'builtInKotlin',
                                           'ANDROID_GRADLE_PLUGIN_VERSION'))
            print(f'{name:32} {v.group(1):10} {"guarded" if guarded else "UNCONDITIONAL"}')
PY
```

Expected — exactly three rows, all `guarded`: `android_file_picker` 1.0.3, `battery_plus` 7.1.1,
`package_info_plus` 10.2.1. **Any `UNCONDITIONAL` row is a blocker**: name the package, check
whether a newer version guards it, and if none exists, stop and report it rather than reintroducing
`android.builtInKotlin=false` (the PLAN documents why that flag does not work here).

Also record each `compileSdk` value for those Android plugins. Flutter's Gradle plugin errors when a
plugin's `compileSdk` exceeds the project's (`android/app/build.gradle.kts` pins `compileSdk = 37`
for `flutter_secure_storage` v11).

### 5. Record, don't fix, the fallout

`flutter analyze` will now report errors — expected. Capture the count and group them by owning
substep so the next agents know their scope:

```bash
flutter analyze 2>&1 | tee "$LOCALAPPDATA/Temp/step47-1-analyze.log"
flutter analyze 2>&1 | grep -oE "lib/[^ :]+" | sort -u
```

Expected owners: `file_picker` API breaks in
`lib/features/data_bucket/presentation/pages/upload_file_page.dart` → **47.2**; bloc 9 breaks across
the ~53 bloc files and 11 `bloc_test` suites → **47.3**; `go_router` 18 / `googleapis` 17 /
`proj4dart` 3 / lints 6 findings → **47.4**. If an error lands outside all three buckets, flag it —
it means the sweep touched something the PLAN did not anticipate.

### 6. Commit

```bash
git -C /d/AppDev/mine_flow/Code/mine-flow-app add pubspec.yaml pubspec.lock
git -C /d/AppDev/mine_flow/Code/mine-flow-app commit -m "build(STEP-47.1): AGP-9-native plugin upgrade; drop STEP-43 win32 override; sweep 7 majors"
```

Commit even though the tree does not compile. The PLAN requires per-substep commits so a later
bisect is cheap; a dependency-only commit is a legitimate, reviewable unit.

## Verification

No new tests here — this substep writes no code. Its proof is resolution plus the audit:

- `flutter pub get` exits 0.
- `flutter pub outdated` shows all direct + dev dependencies up to date.
- `pubspec.yaml` contains **no** `dependency_overrides` block.
- The KGP audit shows zero `UNCONDITIONAL` rows.
- `forui` ^0.26.x, `flutter_secure_storage` ^11.0.0, and `supabase_flutter`'s major are unchanged.
- `flutter analyze` errors are recorded and bucketed by owning substep.

`flutter test` is **expected to fail to compile** at this point. Do not mark it as a passing gate,
and do not silence it — say plainly that the suite cannot run until 47.2–47.4 land. That honesty is
the STEP's ground rule, not a formality.

## Keeping the docs true (always)

You are reversing a recorded STEP-43 decision (the `flutter_secure_storage_windows` override) and
moving that package 4.0.0 → 4.2.2 with `win32` 5.x → 6.x. That is an architecture-relevant change,
but **do not write the ADR or edit `risks.yml` here** — 47.8 owns documentation for the whole STEP,
and splitting it causes double edits.

What you **must** do now: write a short "for 47.8" note at the end of your status update listing
(a) the override removal and why it was safe, (b) the `flutter_secure_storage_windows`/`win32` bump
and its Windows-desktop-only surface, and (c) whether RISK-0008's wording still holds. 47.8 turns
that into the ADR and register rows.

No secrets touched: this substep reads no `.env` and prints no credential.

## Definition of done

- [ ] `package_info_plus ^10.2.1` and `file_picker ^12.1.1` in `pubspec.yaml`
- [ ] `dependency_overrides` block and its stale comment deleted
- [ ] `flutter pub get` resolves; lock shows the expected versions (incl. `win32` 6.4.0,
      `flutter_secure_storage_windows` 4.2.2)
- [ ] 7 major constraints swept; `flutter pub outdated` clean for direct + dev deps
- [ ] `forui` ^0.26.x, `flutter_secure_storage` ^11.0.0, `supabase_flutter` major all unchanged
- [ ] KGP audit run against the resolved lock; zero `UNCONDITIONAL`; table recorded
- [ ] Plugin `compileSdk` values recorded; none exceeds the project's 37
- [ ] `flutter analyze` output captured and bucketed into 47.2 / 47.3 / 47.4
- [ ] No `.dart`, `android/**`, `ci.yml`, or docs file modified
- [ ] Committed on `step-0047-android-build-chain`
- [ ] "For 47.8" documentation note written into the status update

## Next

Update 47.1's status in `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`, then tell the user the next
action: **47.2, 47.3, and 47.4 may now run** — each in its own fresh chat, in parallel if desired,
since they touch disjoint files. 47.5 needs all three.
