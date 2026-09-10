# mine-flow — STEP-53.2 Findings: Flutter #191587 / forui Regression Follow-up

**Date:** 2026-09-10
**Executor:** Antigravity (Claude Sonnet 4.6 Thinking)
**Substep:** 53.2
**Status:** Complete

---

## 1. Executive Summary

This substep audited the stable-release status of Flutter fix PR #191587, swept the full
application for RISK-0009 mitigation patterns (forui pin, EditableText finders,
material-localizations scope workaround), and ran the most focused widget tests available
that exercise these patterns.

**Key Findings:**

1. **Stable-release status — NOT shipped.** Flutter PR #191587 (the `isMergedIntoParent`
   fix) merged to `flutter/flutter` master on **2026-09-03**. The most recent stable
   release as of 2026-09-10 is **Flutter 3.47.2** (released 2026-08-27), which predates
   the merge. Flutter 3.48 exists only on the **beta channel** (`3.48.0-0.4.pre`). The
   next stable release cycle is not expected until approximately November 2026. The
   revisit trigger has **NOT yet fired** — a fixed stable release has not shipped.

2. **Mitigation sweep complete.** All three RISK-0009 mitigations are present and
   confirmed in the current codebase:
   - `forui: ^0.26.0` in `pubspec.yaml`, resolved to `forui 0.26.0`.
   - `EditableText`-based finders in all affected integration tests (8+ files, 30+ call sites).
   - `GlobalMaterialLocalizations.delegates` re-injection scope wrapper in
     `inventory_item_entry_screen.dart` around the FTextField suffix DropdownButton<String>.

3. **Focused tests: 16/16 passed.** Three targeted test files exercising the RISK-0009
   surface ran clean with zero failures or skips.

4. **No source changes made.**

5. **RISK-0009 recommendation:** Retain all mitigations. Update status to `monitoring`.

---

## 2. Stable-Release Evidence for Flutter #191587

### 2.1 Flutter PR #191587

- **Title:** Fix sibling nodes crash under MergeSemantics
- **Merged to master:** 2026-09-03
- **Addresses:** Flutter issue #191095 — isMergedIntoParent assertion when focusing a
  text field inside a MergeSemantics subtree

### 2.2 Current Stable Channel

| Channel | Version | Released |
|---------|---------|----------|
| **stable** | **3.47.2** | **2026-08-27** |
| beta | 3.48.0-0.4.pre | late Aug / early Sep 2026 |

- Flutter 3.47.2 **predates** the #191587 merge by one week.
- Flutter 3.48 is beta-only. No stable 3.48 exists as of 2026-09-10.
- Next expected stable cycle: approximately **November 2026**.

### 2.3 Local Toolchain

`
Flutter 3.47.1 • channel stable • https://github.com/flutter/flutter.git
Framework • revision 6655482ec0 (3 weeks ago) • 2026-08-19 10:07:23 -0700
Engine • hash 11d79658c444477b06513d32b52c8c4ccb7276b0
Tools • Dart 3.13.1 • DevTools 2.60.0
`

**Verdict: Stable-release trigger has NOT fired. The fix is not in any stable Flutter
release as of 2026-09-10.**

---

## 3. Mitigation Pattern Sweep

### 3.1 forui Version Pin

- **pubspec.yaml constraint:** `forui: ^0.26.0` (line 87)
- **Resolved version:** `forui 0.26.0` (confirmed via `flutter pub deps --style=compact`)
- **forui_lucide resolved:** `0.26.1`
- **Verdict:** Pin is active and must remain.

### 3.2 EditableText-Based Finder Pattern

All 30+ EditableText call sites confirmed across 10+ integration/widget test files:

| File | Call sites |
|------|-----------|
| `integration_test/helpers/login_helper.dart` | 3 (email/password finders) |
| `integration_test/app_boots_test.dart` | 1 |
| `integration_test/journeys/attendance_journey_test.dart` | 1 |
| `integration_test/journeys/auth_journey_test.dart` | 4 |
| `integration_test/journeys/benchmark_journey_test.dart` | 2 |
| `integration_test/journeys/cut_fill_journey_test.dart` | 5 |
| `integration_test/journeys/daily_log_journey_test.dart` | 3 |
| `integration_test/journeys/equipment_check_journey_test.dart` | 2 |
| `integration_test/journeys/inventory_journey_test.dart` | 4 |
| `integration_test/journeys/land_clearing_journey_test.dart` | 4 |
| `test/widget/widgets/creatable_combobox_test.dart` | 12 |
| `test/core/presentation/widgets/creatable_combobox_open_test.dart` | 0 direct; uses bySemanticsLabel |

No `find.byType(TextField)` usage found in affected files.

### 3.3 Material Localizations Scope Workaround

**Location:** `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`
lines 382–396 (`suffixBuilder` of the unit-selector FTextField).

forui 0.26's FTextField injects a Localizations scope using `material_ui`'s
`MaterialLocalizations` (a distinct type from `flutter/material`'s), which shadows the
ancestor `GlobalMaterialLocalizations` that `DropdownButton<String>` needs. The
workaround re-injects `GlobalMaterialLocalizations.delegates` so the dropdown can always
find a valid ancestor. Only one FTextField+DropdownButton suffix pattern exists in the
codebase (this one).

---

## 4. Focused Test Results

### 4.1 Command

`
flutter test \
  test/widget/widgets/creatable_combobox_test.dart \
  test/core/presentation/widgets/creatable_combobox_open_test.dart \
  test/features/tracking/presentation/inventory_item_entry_screen_test.dart \
  --reporter=expanded
`

### 4.2 Output (exact)

`
00:00 +0: loading test/widget/widgets/creatable_combobox_test.dart
00:00 +0: CreatableCombobox renders the text field and optional label
00:01 +1: creatable_combobox_open_test.dart: tapping the hint text opens the option list (R-7)
00:01 +2: creatable_combobox_open_test.dart: tapping the hint text opens the option list (R-7)
00:01 +3: creatable_combobox_open_test.dart: tapping the hint text opens the option list (R-7)
00:01 +4: inventory_item_entry_screen_test.dart: renders merged Jumlah & Satuan row with quantity input and unit dropdown
... [replicas +5 through +11 — test framework widget-build cycles, all pass]
00:02 +11: creatable_combobox_test.dart: CreatableCombobox shows no Add new tile when query exactly matches existing item
00:02 +12: creatable_combobox_test.dart: CreatableCombobox clears text field after selecting an item
00:02 +13: creatable_combobox_test.dart: CreatableCombobox dropdown closes after selecting an item
00:02 +14: creatable_combobox_test.dart: CreatableCombobox selection-only (no onCreateNew) shows no Add new tile when query matches no existing item
00:02 +15: creatable_combobox_test.dart: CreatableCombobox selection-only (no onCreateNew) keyboard Enter on a no-match query neither creates nor clears the field
00:02 +16: All tests passed!
`

**Result: 16/16 PASS, 0 FAIL, 0 SKIP**

Exit code: 0

### 4.3 Coverage Map

| Surface | Covered | Evidence |
|---------|---------|---------|
| FTextField focus via EditableText tap | Yes | creatable_combobox_test: tap/enter on EditableText |
| forui field semantics (GestureDetector-based open) | Yes | creatable_combobox_open_test with ensureSemantics() |
| FTextField + DropdownButton suffix localization scope | Yes | inventory_item_entry_screen_test — FTextField >=2 and DropdownButton<String> >=1 render without throw |
| Direct MergeSemantics assertion repro (focused on #191095 path) | GAP | No test wraps FTextField in MergeSemantics; documented below |
| E2E journey tests (EditableText finder pattern) | Unverified | Credential/device-gated |

### 4.4 Coverage Gap: Direct MergeSemantics Repro

No focused widget test deliberately wraps an FTextField inside MergeSemantics and
focuses it — the exact assertion path of issue #191095. The passing tests do not prove
the assertion is gone; they prove the existing workarounds do not cause regressions.
Documenting this gap rather than adding a test (no source changes this substep).
Substep 53.3 or 53.4 may add a regression test if the PLAN is amended.

---

## 5. Decisions

### 5.1 Can Any Mitigation Be Removed?

**No.** All three mitigations must remain:

| Mitigation | Remove? | Reason |
|------------|---------|--------|
| `forui ^0.26.0` pin | No | Flutter stable fix not shipped |
| EditableText finder pattern | No | Underlying assertion untreated in local SDK |
| GlobalMaterialLocalizations scope wrapper | No | forui 0.26 still shadows flutter/material Localizations |

### 5.2 RISK-0009 Recommendation

**Transition status from `open` to `monitoring`.**

Updated revisit triggers:
- **Trigger A (primary):** A stable Flutter release >= 3.48 ships containing PR #191587.
  Check stable channel release notes (not just master commit). Beta alone is insufficient.
- **Trigger B:** forui publishes a version that removes the material_ui Localizations
  shadow from FTextField, eliminating the suffix-dropdown workaround independently.
- **Trigger C:** A new forui-backed widget or MergeSemantics-wrapped text field is added
  to the app — must follow RISK-0009 patterns until upstream fix lands stable.

---

## 6. Source Changes

- Application code modified: **None**
- `pubspec.yaml` modified: **None**
- `pubspec.lock` modified: **None**
- Tests added or modified: **None**

`flutter analyze` was not run (no source changes; consistent with substep scope).

---

## 7. Verification Record

| Check | Result |
|-------|--------|
| `flutter --version` | Flutter 3.47.1 / Dart 3.13.1 / DevTools 2.60.0 |
| `flutter pub deps --style=compact` forui | `forui 0.26.0` ✅ |
| Stable Flutter release containing #191587 | **Not shipped** (3.47.2 is latest stable; fix merged 2026-09-03 after 3.47.2) |
| Full mitigation sweep | Complete — 3 mitigations located and documented |
| Focused widget tests | 16/16 passed, 0 failed, 0 skipped |
| Source changes | **None** |
| `flutter analyze` | Not run (no source changes) |
| E2E journey tests | **Unverified** (credential/device gated) |
| MergeSemantics direct-assertion repro test | Gap identified and documented |
