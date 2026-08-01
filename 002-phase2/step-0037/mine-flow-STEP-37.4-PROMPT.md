# mine-flow — STEP-37.4: Data Bucket Feature Purge

> **How to run:** Tell your agent *"run substep 37.4"* (or *"read and run this file"*).

## Context

Substep 37.4 of STEP-37 (Residual Impeccable Material Purge). Replace two `TextButton`
widgets used as action buttons in an `AlertDialog` (delete confirmation) inside
`file_detail_page.dart`. Low risk — scoped to a single dialog.

## Read these first (silently)

- `Upcoming Prompts/mine-flow-STEP-37-PLAN.md` — full context and locked decisions

## Target file

| File | Path | Violations |
|---|---|---|
| `file_detail_page.dart` | `lib/features/data_bucket/presentation/pages/file_detail_page.dart` | `TextButton` at L69 (cancel) and L73 (confirm/destructive) |

## Your task

Read the full `file_detail_page.dart` file first to understand the surrounding `showDialog`
call. Then locate the `AlertDialog` actions array (around L60–82) containing:

```dart
actions: [
  TextButton(
    onPressed: () => Navigator.of(ctx).pop(false),
    child: const Text('Batal'),
  ),
  TextButton(
    onPressed: () => Navigator.of(ctx).pop(true),
    style: TextButton.styleFrom(
      foregroundColor: theme.colors.destructive,
    ),
    child: const Text('Hapus'),
  ),
],
```

Replace with `FButton` variants that match the semantic intent:

```dart
actions: [
  FButton(
    style: FButtonStyle.ghost,
    onPress: () => Navigator.of(ctx).pop(false),
    label: const Text('Batal'),
  ),
  FButton(
    style: FButtonStyle.destructive,
    onPress: () => Navigator.of(ctx).pop(true),
    label: const Text('Hapus'),
  ),
],
```

Key points:
- Keep `AlertDialog` as-is — only the action buttons change.
- `ctx` inside `showDialog`'s builder is a different context than the outer `context` — make
  sure `FButton` can access `FTheme` via `ctx`. If ForUI's `FButton` requires `FTheme` in
  context and `ctx` is inside `MaterialApp` without `FTheme` available at that level, wrap
  the dialog in a `Builder` that inherits from the outer `FTheme` context. Check how other
  dialogs in the codebase handle this if needed.
- The confirmed action (`pop(true)`) must still lead to `repository.deleteFile(file.id)` —
  do not change the logic after the dialog returns.

## Verification

- Run: `flutter test test/features/data_bucket`
- All existing tests must still pass.
- Write or update a widget test asserting `find.byType(TextButton)` → `findsNothing`
  within the `AlertDialog` rendered by `file_detail_page.dart`.
- Manual check: in debug mode, open a file detail page, tap delete, confirm the dialog
  opens with correct buttons, cancel dismisses, confirm triggers deletion.

## Definition of done

- [ ] `file_detail_page.dart`: zero `TextButton` references.
- [ ] Delete dialog functional: cancel → pops false, confirm → pops true → `deleteFile` fires.
- [ ] Widget test added/updated; `flutter test test/features/data_bucket` passes.
- [ ] Update substep 37.4 status to **Done** in `Upcoming Prompts/mine-flow-STEP-37-PLAN.md`.

## Next

When this substep is done, tell the user: *"Substep 37.4 complete. Run substep 37.5 in a fresh chat."*
