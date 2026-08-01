# mine-flow — STEP-37.1: Equipment Check Feature Purge

> **How to run:** Tell your agent *"run substep 37.1"* (or *"read and run this file"*).

## Context

This is substep 37.1 of STEP-37 (Residual Impeccable Material Purge). You are replacing
the last remaining Blocking Impeccable violations in the Equipment Check feature: an
`ElevatedButton`, a raw `Card(`, a `Theme.of(context)` call, a hardcoded `Color(0xFFFFFFFF)`,
and a `TextButton.icon` — all in 3 files.

## Read these first (silently)

- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — Impeccable mandate
- `Code/mine-flow-docs/ADR-0008-impeccable-bridge.md` (or `adr/ADR-0008-impeccable-bridge.md`) — token rules
- `Upcoming Prompts/mine-flow-STEP-37-PLAN.md` — full context and locked decisions

## Target files

| File | Path | Violations |
|---|---|---|
| `equipment_check_form_screen.dart` | `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart` | `ElevatedButton` at L238, `Color(0xFFFFFFFF)` at L252 |
| `sop_checklist_item_card.dart` | `lib/features/equipment_check/presentation/widgets/sop_checklist_item_card.dart` | `Card(` at L23, `Theme.of(context).textTheme.bodySmall` at L124 |
| `equipment_check_card.dart` | `lib/features/equipment_check/presentation/widgets/equipment_check_card.dart` | `TextButton.icon` at L257 |

## Your task

### 1. `equipment_check_form_screen.dart`

Replace the `SizedBox > ElevatedButton` block (L234–262) with `FButton` (primary style —
no explicit `style:` arg needed, primary is the default):

```dart
SizedBox(
  width: double.infinity,
  child: FButton(
    onPress: loadedState.isSubmitting
        ? null
        : () => bloc.add(const SubmitEquipmentCheckEvent()),
    label: loadedState.isSubmitting
        ? SizedBox(
            height: 20,
            width: 20,
            child: CircularProgressIndicator(
              strokeWidth: 2,
              valueColor: AlwaysStoppedAnimation<Color>(
                theme.colors.primaryForeground,   // was Color(0xFFFFFFFF)
              ),
            ),
          )
        : Text(
            'Simpan Inspeksi SOP (${loadedState.passedCount}/${loadedState.totalCount} Lolos)',
          ),
  ),
)
```

Confirm `theme` is already in scope as `FTheme.of(context)` in the same `build` method
before making this change. The `SizedBox(height: 48)` constraint can be removed since
`FButton` handles its own height, but keep `width: double.infinity`.

### 2. `sop_checklist_item_card.dart`

Replace `Card(elevation: 0, margin: ..., color: ..., shape: ..., child: Padding(...))` (L23–130)
with a `Container` that replicates the visual exactly:

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
    child: Column(
      // ... unchanged interior content
    ),
  ),
)
```

At L124, replace `Theme.of(context).textTheme.bodySmall` with `theme.typography.body.sm`.
If `body.sm` is not available in forui 0.24.3, use `theme.typography.body.xs` and add a
comment: `// forui 0.24.3: body.sm unavailable; using body.xs`.

### 3. `equipment_check_card.dart`

Replace `TextButton.icon(onPressed: onDelete, icon: Icon(...), label: Text(...))` at L257–270
with `FButton` ghost style, keeping the `Align` wrapper:

```dart
Align(
  alignment: Alignment.centerRight,
  child: FButton(
    style: FButtonStyle.ghost,
    onPress: onDelete,
    prefix: Icon(
      Icons.delete_outline,
      size: 16,
      color: theme.colors.destructive,
    ),
    label: Text(
      'Hapus Record',
      style: theme.typography.body.xs.copyWith(
        color: theme.colors.destructive,
      ),
    ),
  ),
)
```

## Verification

- Run: `flutter test test/features/equipment_check`
- All existing tests must still pass. Write or update widget tests that assert:
  - `find.byType(ElevatedButton)` → `findsNothing` in `equipment_check_form_screen.dart`'s widget tree
  - `find.byType(Card)` → `findsNothing` in `sop_checklist_item_card.dart`'s widget tree
  - `find.byType(TextButton)` → `findsNothing` in `equipment_check_card.dart`'s widget tree
- If no widget test files exist for these widgets, create minimal ones.

## Definition of done

- [ ] `equipment_check_form_screen.dart`: zero `ElevatedButton`; zero `Color(0xFFFFFFFF)`.
- [ ] `sop_checklist_item_card.dart`: zero `Card(`; zero `Theme.of(context).textTheme`.
- [ ] `equipment_check_card.dart`: zero `TextButton`.
- [ ] Widget tests added/updated; `flutter test test/features/equipment_check` passes.
- [ ] Update substep 37.1 status to **Done** in `Upcoming Prompts/mine-flow-STEP-37-PLAN.md`.

## Next

When this substep is done, tell the user: *"Substep 37.1 complete. Run substep 37.2 in a fresh chat."*
