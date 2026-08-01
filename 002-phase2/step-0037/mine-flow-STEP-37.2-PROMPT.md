# mine-flow — STEP-37.2: Timeline Feature Purge

> **How to run:** Tell your agent *"run substep 37.2"* (or *"read and run this file"*).

## Context

Substep 37.2 of STEP-37 (Residual Impeccable Material Purge). Replace the raw `Card(`
widget in `milestone_card.dart` with a ForUI-compatible `Container` that preserves the
exact visual output and the `InkWell` tap behaviour.

## Read these first (silently)

- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — Impeccable mandate
- `Upcoming Prompts/mine-flow-STEP-37-PLAN.md` — full context and locked decisions

## Target file

| File | Path | Violation |
|---|---|---|
| `milestone_card.dart` | `lib/features/timeline/presentation/widgets/milestone_card.dart` | `Card(` at L23 |

## Your task

Read the entire `milestone_card.dart` file first. Then replace:

```dart
return Card(
  elevation: 0,
  margin: const EdgeInsets.only(bottom: 8),
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(4),
    side: BorderSide(color: theme.colors.border, width: 0.5),
  ),
  child: InkWell(
    onTap: onTap,
    borderRadius: BorderRadius.circular(4),
    child: Padding(
      padding: const EdgeInsets.all(12),
      child: Row(...),
    ),
  ),
);
```

With a `Container` + `InkWell` that replicates the same visual:

```dart
return Container(
  margin: const EdgeInsets.only(bottom: 8),
  decoration: BoxDecoration(
    color: theme.colors.background,
    borderRadius: BorderRadius.circular(4),
    border: Border.all(color: theme.colors.border, width: 0.5),
  ),
  child: ClipRRect(
    borderRadius: BorderRadius.circular(4),
    child: InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(...),  // unchanged interior — do NOT modify
      ),
    ),
  ),
);
```

Key points:
- Use `ClipRRect` wrapping `InkWell` so the ink ripple is clipped to the rounded corners
  (the same behaviour `Card` provided).
- The `theme.colors.background` fill ensures the card surface uses the ForUI surface token,
  not a Material default white.
- The interior `Row(...)` content is **unchanged** — only replace the outer `Card` shell.
- `theme` is already in scope as `FTheme.of(context)` at L18 — do not add another reference.

Before any change, check `cut_fill_card.dart` or `clearing_summary_card.dart` to see if
there is an established tap-on-FCard pattern in the codebase. If so, prefer that pattern
and document the choice inline.

## Verification

- Run: `flutter test test/features/timeline`
- All existing tests must still pass.
- Add or update a widget test that asserts `find.byType(Card)` → `findsNothing` in
  `MilestoneCard`'s widget tree and that `onTap` fires correctly when tapped.
- Manual check: open the Timeline page in debug mode; confirm milestone cards render
  with border, correct background, and that tapping a card triggers `onTap`.

## Definition of done

- [ ] `milestone_card.dart`: zero `Card(`.
- [ ] `onTap` callback is functionally preserved (tapping triggers the callback).
- [ ] Widget test added/updated; `flutter test test/features/timeline` passes.
- [ ] Update substep 37.2 status to **Done** in `Upcoming Prompts/mine-flow-STEP-37-PLAN.md`.

## Next

When this substep is done, tell the user: *"Substep 37.2 complete. Run substep 37.3 in a fresh chat."*
