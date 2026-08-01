# Substep 28.4: Complete UI Token Standardization (Forest & Stone)

**Scope:** Standardize colors, typography, and spacing across the 15 Phase 2 screens to strictly adhere to the Forest & Stone theme (`app_theme.dart`). There are approximately 157 remaining instances of hardcoded values to fix.
**Targets:** `lib/features/*/presentation/pages/*.dart` and `lib/features/*/presentation/widgets/*.dart`.

## Instructions for DeepSeek v4 Flash

**1. Floating Action Buttons & Cyan (_kAccent):**
- Remove all local declarations of `const Color _kAccent = Color(0xFF0891B2);` across the presentation layer.
- Update all `FloatingActionButton` and `FloatingActionButton.extended` widgets to use:
  `backgroundColor: Theme.of(context).colorScheme.primary`
  `foregroundColor: Theme.of(context).colorScheme.onPrimary`
- Replace any other `_kAccent` usage (e.g., in `FilterChip` selected/checkmark colors) with `Theme.of(context).colorScheme.primary`.

**2. Hardcoded Semantic Colors:**
- Search for and replace `Colors.red` with `Theme.of(context).colorScheme.error`.
- Search for and replace `Colors.green` with `Theme.of(context).colorScheme.primary` (or the success semantic color).
- Remove `.shade` modifiers from raw colors and use `colorScheme.primaryContainer` or `surfaceContainerHighest` where tinted backgrounds are needed.

**3. Typography:**
- Remove hardcoded `TextStyle(fontSize: X)` used directly in `Text()` widgets (e.g., in `attendance_screen.dart`, `cut_fill_card.dart`, `land_clearing_entry_screen.dart`).
- Replace them with the appropriate semantic text theme (e.g., `Theme.of(context).textTheme.bodySmall`, `labelLarge`, `titleMedium`). Use `.copyWith()` only when strictly necessary for overriding color or font weight.

**4. Spacing:**
- Ensure margins and padding strictly follow the spacing scale: `4`, `8`, `12`, `16`, `20`, `24`, `32`.
- Replace non-standard spacing constants (like `10`, `6`, `14`, `5`, `3` dp) with their closest strict scale equivalents.

**Rule:** This is a pure styling pass. Do NOT modify any business logic, data fetching, or state management. Run `flutter analyze` when finished to guarantee no compilation errors were introduced.
