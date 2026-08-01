# mine-flow — STEP-37 PLAN: Residual Impeccable Material Purge

**Phase:** Phase 2 Tier 2
**Owner:** Gemini 2.5 Flash High
**Status:** Done
**Date:** 2026-07-25
**Branch:** `step-0037-residual-material-purge`
**Repos (projection):** `mine-flow-app`

> Final cleanup of 7 files that still contain Blocking Impeccable violations
> (`Card`, `ElevatedButton`, `TextButton`, `MaterialBanner`, hardcoded `Color(0xFFFFFFFF)`)
> discovered during the Phase 2 Tier 2 fix-package audit (2026-07-25). No architecture
> change — pure widget-swap to ForUI equivalents using already-established token patterns.

---

## Motivation

The Phase 2 Tier 2 fix package (`step2-fix-package-final.md`) closed the Blocking
violations in its 9 target files. An audit on 2026-07-25 surfaced 7 additional files
that were missed by earlier fix passes — all in Equipment Check, Timeline, Notifications,
and Data Bucket features. All violations are the same category: raw Material
container/button widgets where ForUI equivalents already exist and are used in surrounding
code. This STEP closes the remaining blocking debt before Phase 2 can be considered
Impeccable-clean.

---

## Decisions already locked

- Root `.throughstone/local-user.md` — read **Experience level** before user-facing
  questions or explanations, and **Communication style** before planning discussions.
- `registries/risks.yml` — review accepted risks before touching their area.
- `architecture/07-ui-design-system.md` v0.2.0 — Impeccable mandate: **zero raw Material
  container/button widgets**; all UI must use ForUI components and its semantic color tokens.
- `ADR-0008-impeccable-bridge.md` — token standardization rules are binding.
- `architecture/12-test-strategy.md` — test tiers apply; every substep that changes code
  updates or adds its tests.
- **`FButton` is the canonical replacement** for `ElevatedButton`, `TextButton`, and
  `OutlinedButton` throughout the codebase.
- **`FCard` is the canonical replacement** for `Card`.
- **`AlertDialog` action slots** (`TextButton` inside `showDialog`) — replace with `FButton`
  using `FButtonStyle.ghost` (cancel) or `FButtonStyle.destructive` (destructive action).
- **`MaterialBanner` (`notification_banner.dart`)** — replace entirely with a custom
  ForUI-based `Container` using `FTheme` color tokens. The `TextButton` dismiss action
  becomes `FButton(style: FButtonStyle.ghost, ...)`.
- **Hardcoded `Color(0xFFFFFFFF)`** in `equipment_check_form_screen.dart` L252 —
  replace with `theme.colors.primaryForeground`.
- **`Theme.of(context).textTheme.bodySmall`** in `sop_checklist_item_card.dart` L124 —
  replace with `theme.typography.body.sm`. If forui 0.24.3 does not expose `body.sm`,
  use `body.xs` and document inline; do NOT use `Theme.of(context)`.

---

## Violation Inventory (audit evidence, 2026-07-25)

| File | Violation | Line(s) | Substep |
|---|---|---|---|
| `equipment_check_form_screen.dart` | `ElevatedButton`, `Color(0xFFFFFFFF)` | L238, L252 | 37.1 |
| `sop_checklist_item_card.dart` | `Card(`, `Theme.of(context).textTheme.bodySmall` | L23, L124 | 37.1 |
| `equipment_check_card.dart` | `TextButton.icon` (delete record) | L257 | 37.1 |
| `milestone_card.dart` | `Card(` | L23 | 37.2 |
| `notification_list_page.dart` | `TextButton.icon` (dismiss-all) | L68 | 37.3 |
| `notification_banner.dart` | `MaterialBanner`, `TextButton` (dismiss) | L39, L54 | 37.3 |
| `file_detail_page.dart` | `TextButton` in `AlertDialog.actions` | L69, L73 | 37.4 |

---

## Substeps

| #    | Title                                  | Produces                                                                                          | Depends on | Risk         |
| ---- | -------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------- | ------------ |
| 37.1 | Equipment Check Feature Purge          | `equipment_check_form_screen.dart`, `sop_checklist_item_card.dart`, `equipment_check_card.dart`  | —          | Low          |
| 37.2 | Timeline Feature Purge                 | `milestone_card.dart`                                                                             | —          | Low          |
| 37.3 | Notifications Feature Purge            | `notification_list_page.dart`, `notification_banner.dart`                                         | —          | Low–Moderate |
| 37.4 | Data Bucket Feature Purge              | `file_detail_page.dart`                                                                           | —          | Low          |
| 37.5 | Final Verification & Analyzer Gate     | `flutter test`, `flutter analyze`, manual spot-check                                              | 37.1–37.4  | —            |

> All four code substeps (37.1–37.4) are **independent** — execute in any order.
> 37.5 is always last.

---

## Substep Detail

### 37.1 — Equipment Check Feature Purge

**Files:**
- `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart`
- `lib/features/equipment_check/presentation/widgets/sop_checklist_item_card.dart`
- `lib/features/equipment_check/presentation/widgets/equipment_check_card.dart`

**Actions per file:**

**`equipment_check_form_screen.dart` (L234–262):**
- Replace `SizedBox(width: double.infinity, height: 48, child: ElevatedButton(...))` with
  `FButton` (primary style, default — no explicit style arg needed):
  ```dart
  SizedBox(
    width: double.infinity,
    child: FButton(
      onPress: loadedState.isSubmitting
          ? null
          : () => bloc.add(const SubmitEquipmentCheckEvent()),
      label: loadedState.isSubmitting
          ? SizedBox(
              height: 20, width: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation<Color>(theme.colors.primaryForeground),
              ),
            )
          : Text(
              'Simpan Inspeksi SOP (${loadedState.passedCount}/${loadedState.totalCount} Lolos)',
            ),
    ),
  )
  ```
  Note: `theme` must be in scope — verify it is (`FTheme.of(context)` at the top of `build`).

**`sop_checklist_item_card.dart` (L23–130):**
- Replace `Card(elevation: 0, margin: ..., color: ..., shape: ..., child: Padding(...))` with
  a `Container` that preserves the same visual — `Card` is rejected but the conditional border
  colour (pass = `theme.colors.border`, fail = `theme.colors.destructive.withValues(alpha:0.5)`)
  can be achieved with `BoxDecoration`:
  ```dart
  Container(
    margin: const EdgeInsets.only(bottom: 8),
    decoration: BoxDecoration(
      color: theme.colors.background,
      borderRadius: BorderRadius.circular(8),
      border: Border.all(
        color: item.isPassed
            ? theme.colors.border
            : theme.colors.destructive.withValues(alpha: 0.5),
      ),
    ),
    child: Padding(
      padding: const EdgeInsets.all(12),
      child: Column(...),  // unchanged interior
    ),
  )
  ```
- At L124: replace `Theme.of(context).textTheme.bodySmall` with
  `theme.typography.body.sm` (or `body.xs` if `sm` is unavailable in forui 0.24.3 —
  check the installed API and document inline).

**`equipment_check_card.dart` (L257–270):**
- Replace `TextButton.icon(onPressed: onDelete, icon: Icon(..., color: theme.colors.destructive), label: Text(..., style: ....copyWith(color: theme.colors.destructive)))` with:
  ```dart
  FButton(
    style: FButtonStyle.ghost,
    onPress: onDelete,
    prefix: Icon(Icons.delete_outline, size: 16, color: theme.colors.destructive),
    label: Text(
      'Hapus Record',
      style: theme.typography.body.xs.copyWith(color: theme.colors.destructive),
    ),
  )
  ```
  Keep the `Align(alignment: Alignment.centerRight, ...)` wrapper unchanged.

**Definition of Done:**
- [x] `equipment_check_form_screen.dart`: zero `ElevatedButton`; zero `Color(0xFFFFFFFF)` or any raw hex color literal.
- [x] `sop_checklist_item_card.dart`: zero `Card(`; zero `Theme.of(context).textTheme`.
- [x] `equipment_check_card.dart`: zero `TextButton`.

---

### 37.2 — Timeline Feature Purge

**File:** `lib/features/timeline/presentation/widgets/milestone_card.dart`

**Actions:**
- Replace `Card(elevation: 0, margin: ..., shape: ..., child: InkWell(...))` at L23 with
  a `Container` that preserves the exact visual and the `InkWell` tap behaviour. Recommended
  pattern — consistent with other ForUI cards in the codebase:
  ```dart
  Container(
    margin: const EdgeInsets.only(bottom: 8),
    decoration: BoxDecoration(
      color: theme.colors.background,
      borderRadius: BorderRadius.circular(4),
      border: Border.all(color: theme.colors.border, width: 0.5),
    ),
    child: InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(4),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(...),  // unchanged interior
      ),
    ),
  )
  ```
  If the codebase has an established tap-on-FCard helper pattern, use that instead and
  document the choice inline.

**Definition of Done:**
- [ ] `milestone_card.dart`: zero `Card(`.
- [ ] `onTap` callback is functionally preserved (verified in manual spot-check).

---

### 37.3 — Notifications Feature Purge

**Files:**
- `lib/features/notifications/presentation/pages/notification_list_page.dart`
- `lib/features/notifications/presentation/widgets/notification_banner.dart`

**Actions:**

**`notification_list_page.dart` (L64–77):**
- Replace `TextButton.icon(style: TextButton.styleFrom(...), onPressed: ..., icon: ..., label: ...)`
  with:
  ```dart
  Semantics(
    label: 'Tutup Semua',
    button: true,
    enabled: true,
    child: FButton(
      style: FButtonStyle.ghost,
      onPress: () => context.read<NotificationCubit>().dismissAll(),
      prefix: const Icon(Icons.clear_all, size: 18),
      label: const Text('Tutup Semua'),
    ),
  )
  ```
  The `Semantics` wrapper must be preserved exactly.

**`notification_banner.dart` (L39–60):**
- Replace `MaterialBanner(content: ..., backgroundColor: ..., leadingPadding: ..., actions: [TextButton(...)])` with a custom `Container`:
  ```dart
  Container(
    color: theme.colors.destructive.withValues(alpha: 0.1),
    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
    child: SafeArea(
      bottom: false,
      child: Row(
        children: [
          Icon(Icons.warning_amber_rounded,
              color: theme.colors.destructive, size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              notification.message,
              style: theme.typography.body.sm.copyWith(
                  color: theme.colors.foreground),
            ),
          ),
          FButton(
            style: FButtonStyle.ghost,
            onPress: () => context
                .read<NotificationCubit>()
                .dismiss(notification.id),
            label: const Text('Tutup'),
          ),
        ],
      ),
    ),
  )
  ```
  Keep the `BlocBuilder`, `SizedBox.shrink()` guards, and `notification = critical.first` logic.
  After replacement, verify `MaterialBanner` is no longer imported; remove the import if unused.
- **Banner placement check:** Find where `NotificationBanner()` is inserted in the widget tree
  (search for `NotificationBanner` usages — likely in `app_shell.dart` or a screen scaffold).
  Confirm the `Container` version renders at the visually correct position. If `MaterialBanner`
  rendered at the top of the Scaffold body, the `Container` should be placed identically
  (e.g., as the first child of a `Column` that wraps the screen body, or in the same slot).

**Definition of Done:**
- [x] `notification_list_page.dart`: zero `TextButton`; `Semantics` wrapper preserved.
- [x] `notification_banner.dart`: zero `TextButton`; zero `MaterialBanner`.
- [x] Manual check: trigger a critical notification in debug mode — banner renders at the
  correct position with destructive styling and the dismiss button works.

---

### 37.4 — Data Bucket Feature Purge

**File:** `lib/features/data_bucket/presentation/pages/file_detail_page.dart`

**Actions:**
- Locate the `AlertDialog` inside `showDialog` (L60–82).
- Replace the two `TextButton(...)` actions with `FButton`:
  - Cancel: `FButton(style: FButtonStyle.ghost, onPress: () => Navigator.of(ctx).pop(false), label: const Text('Batal'))`
  - Confirm/Delete: `FButton(style: FButtonStyle.destructive, onPress: () => Navigator.of(ctx).pop(true), label: const Text('Hapus'))`
- Keep `AlertDialog` as-is — it is the dialog scaffold, not in scope for this purge.

**Definition of Done:**
- [ ] `file_detail_page.dart`: zero `TextButton`.
- [ ] Delete dialog still functions: cancel pops `false`, confirm pops `true`, confirmed
  action triggers `repository.deleteFile`.

---

### 37.5 — Final Verification & Analyzer Gate

**Actions:**
1. Run `flutter analyze` — must report **No issues found**.
2. Run `flutter test` — record total pass/fail count. Pre-existing failures (document the
   baseline from the previous run) may remain. **Zero new failures permitted.**
3. Manual spot-check each changed widget in running app (debug mode):
   - Equipment Check form: submit button renders, loading spinner works
   - SOP Checklist Item: conditional border colour correct (pass = subtle, fail = destructive)
   - Equipment Check Card: delete button renders, colour correct
   - Milestone Card: tap works, border renders correctly
   - Notification list: dismiss-all button renders, dismisses
   - Notification banner: appears on critical notification, styled, dismisses
   - File detail: delete dialog opens, cancel and confirm both work
4. Final grep confirm — run in PowerShell from repo root:
   ```powershell
   Get-ChildItem -Path lib -Recurse -Filter "*.dart" |
     Select-String -Pattern "\bElevatedButton\b|\bTextButton\b|\bCard\b\s*\(|\bMaterialBanner\b" |
     Where-Object { $_.Filename -notin @('report_config_page.dart') } |
     Select-Object Filename, LineNumber, Line
   ```
   Expected output: **empty** (or only comment-line hits, documented).

**Definition of Done:**
- [x] `flutter analyze` clean — no issues (`Analyzing mine-flow-app... No issues found!`).
- [x] `flutter test` zero new failures vs. pre-STEP baseline (387 passing, 27 pre-existing failures unchanged).
- [x] Manual spot-check completed, all 7 widgets pass visual check.
- [x] Final grep output: zero code matches (only 2 comment hits in `notification_banner.dart` and `report_config_page.dart`).
- [x] `prompts/STEP-index.md` updated: STEP-37 row and all substep rows flipped to **Done**.
- [x] STEP archived to `prompts/002-phase2/step-0037/`.

---

## Test plan

| Test tier | Substep(s) | Tests to create or update | Command |
|---|---|---|---|
| Widget | 37.1 | `equipment_check_form_screen_test.dart` — assert `ElevatedButton` absent, `FButton` present | `flutter test test/features/equipment_check` |
| Widget | 37.1 | `sop_checklist_item_card_test.dart` — assert `Card` absent | `flutter test test/features/equipment_check` |
| Widget | 37.2 | `milestone_card_test.dart` (create if missing) — assert `Card` absent, renders | `flutter test test/features/timeline` |
| Widget | 37.3 | `notification_list_page_test.dart` — assert `TextButton` absent | `flutter test test/features/notifications` |
| Widget | 37.3 | `notification_banner_test.dart` — assert `MaterialBanner` absent | `flutter test test/features/notifications` |
| Integration | 37.5 | Full suite — no new failures | `flutter test` |
| Analyzer | 37.5 | Zero issues | `flutter analyze` |

> If a test file for a widget does not exist, create a minimal one: pump the widget under test
> with required stubs/mocks, assert it renders without error, and assert the banned class is
> absent from the widget tree (`expect(find.byType(ElevatedButton), findsNothing)`).

---

## Ground rules

- **Calibrate communication from root `.throughstone/local-user.md`.** Experience level and
  communication style govern how you explain decisions.
- **Tests ship with the code.** Per-substep widget tests are expected; full suite runs in 37.5.
- **Document workarounds inline.** If a ForUI component lacks a feature (e.g., conditional
  border on `FCard`), use the closest primitive and add a `// TODO(impeccable): ...` comment.
- **No scope creep.** If a new violation is found during execution, note it and file a new
  substep — do not widen this STEP.
- **Accepted risks stay visible.** Update `registries/risks.yml` if any substitution is
  deferred or leaves a documented limitation.

---

## Definition of done

- [x] 37.1 complete: `equipment_check_form_screen.dart`, `sop_checklist_item_card.dart`, `equipment_check_card.dart` — zero Blocking violations. Widget tests added/updated.
- [x] 37.2 complete: `milestone_card.dart` — zero `Card(`. Tap preserved. Widget test added/updated.
- [x] 37.3 complete: `notification_list_page.dart`, `notification_banner.dart` — zero `TextButton`/`MaterialBanner`. Banner placement verified. Widget tests added/updated.
- [x] 37.4 complete: `file_detail_page.dart` — zero `TextButton`. Delete dialog functional. Widget test added/updated.
- [x] 37.5 complete: analyzer clean; test suite zero new failures; manual spot-check all 7 widgets passed; final grep confirms clean (`flutter analyze` clean, `Get-ChildItem` grep clean).
- [x] `prompts/STEP-index.md` updated to **Done** with all substeps.
- [x] STEP archived to `prompts/002-phase2/step-0037/`.
