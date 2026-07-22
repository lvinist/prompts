# Substep 30.6: Final Cross-Screen Material Purge & CI Gate

**Scope:** Global presentation layer.

## 1. Audit
- Run a workspace-wide search for `Colors.`, `TextStyle(`, and `Theme.of(context).colorScheme` (which should now be `FTheme.of(context)`). 
- Eradicate any lingering instances in the presentation layer.

## 2. Test
- Run the full test suite (`flutter test`). 
- Fix any integration tests that broke because they were looking for specific Material widgets that no longer exist.

## 3. Verify
- Confirm the CI gate is 100% passing.
