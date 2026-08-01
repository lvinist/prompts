# mine-flow — STEP-37.3: Notifications Feature Purge

> **How to run:** Tell your agent *"run substep 37.3"* (or *"read and run this file"*).

## Context

Substep 37.3 of STEP-37 (Residual Impeccable Material Purge). This is the most significant
substep: it replaces a `TextButton.icon` in the notification list page and completely
replaces the `MaterialBanner` + `TextButton` in `notification_banner.dart` with a
ForUI-based `Container`. Low–Moderate risk due to the `MaterialBanner` placement change.

## Read these first (silently)

- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — Impeccable mandate
- `Upcoming Prompts/mine-flow-STEP-37-PLAN.md` — full context and locked decisions

## Target files

| File | Path | Violations |
|---|---|---|
| `notification_list_page.dart` | `lib/features/notifications/presentation/pages/notification_list_page.dart` | `TextButton.icon` at L68 |
| `notification_banner.dart` | `lib/features/notifications/presentation/widgets/notification_banner.dart` | `MaterialBanner` at L39, `TextButton` at L54 |

## Your task

### 1. `notification_list_page.dart` — dismiss-all button (L64–77)

Before changing: read the file to understand the full `Semantics` + `TextButton.icon` block.

Replace the `TextButton.icon(...)` with `FButton(style: FButtonStyle.ghost, ...)`.
**The `Semantics` wrapper must be preserved exactly around the new button:**

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

### 2. `notification_banner.dart` — full MaterialBanner replacement

Before changing: read the entire `notification_banner.dart` file.

**Step A — Find where `NotificationBanner()` is used:**
Search for `NotificationBanner` in the lib/ directory to find its insertion point in the
widget tree. Note the exact position (e.g., inside `app_shell.dart` Column, or wrapping
a Scaffold). This determines if placement needs adjustment after the swap.

**Step B — Replace `MaterialBanner` with a `Container`:**

Replace the `return MaterialBanner(...)` block (L39–60) with:

```dart
return Container(
  color: theme.colors.destructive.withValues(alpha: 0.1),
  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
  child: SafeArea(
    bottom: false,
    child: Row(
      children: [
        Icon(
          Icons.warning_amber_rounded,
          color: theme.colors.destructive,
          size: 20,
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            notification.message,
            style: theme.typography.body.sm.copyWith(
              color: theme.colors.foreground,
            ),
          ),
        ),
        FButton(
          style: FButtonStyle.ghost,
          onPress: () =>
              context.read<NotificationCubit>().dismiss(notification.id),
          label: const Text('Tutup'),
        ),
      ],
    ),
  ),
);
```

Keep the `BlocBuilder<NotificationCubit, NotificationState>` wrapper, the
`if (state is! NotificationLoaded) return const SizedBox.shrink()` guard,
the `critical.isEmpty` guard, and the `notification = critical.first` logic — all
unchanged. Only replace the `return MaterialBanner(...)` expression.

**Step C — Clean up imports:**
After replacement, check if `MaterialBanner` is still referenced anywhere in the file.
If not, it will no longer be needed from `material.dart` — but `material.dart` likely
provides other used symbols too (check `Icon`, `SizedBox`, `Row`, etc.), so only remove
the import if nothing else from it is used. If `material.dart` is still needed, leave
it and note it in your execution log.

**Step D — Verify banner placement:**
From Step A, if `NotificationBanner` was previously placed as a Scaffold `bottomSheet`
or as a child inside `MaterialApp` at a special slot, the `Container` version may render
differently. Confirm it renders visually at the top of content where expected. If
placement adjustment is needed, document what you changed and why.

## Verification

- Run: `flutter test test/features/notifications`
- All existing tests must still pass.
- Write or update widget tests asserting:
  - `find.byType(TextButton)` → `findsNothing` in `notification_list_page.dart`'s tree
  - `find.byType(MaterialBanner)` → `findsNothing` in `notification_banner.dart`'s tree
- **Manual visual check (required):**
  Open the app in debug mode. Navigate to the Notification List page. Confirm:
  1. The "Tutup Semua" button renders and triggers dismiss-all.
  2. Trigger or simulate a critical notification. Confirm the banner appears at the
     correct position with the destructive background and "Tutup" button works.
  Record this check in your execution notes.

## Definition of done

- [ ] `notification_list_page.dart`: zero `TextButton`; `Semantics` wrapper preserved.
- [ ] `notification_banner.dart`: zero `TextButton`; zero `MaterialBanner`.
- [ ] Banner renders at correct position in the app with destructive styling (manual check done).
- [ ] Widget tests added/updated; `flutter test test/features/notifications` passes.
- [ ] Update substep 37.3 status to **Done** in `Upcoming Prompts/mine-flow-STEP-37-PLAN.md`.

## Next

When this substep is done, tell the user: *"Substep 37.3 complete. Run substep 37.4 in a fresh chat."*
