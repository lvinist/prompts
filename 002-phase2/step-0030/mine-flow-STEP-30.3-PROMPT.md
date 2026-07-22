# Substep 30.3: Teams & Field Docs (ForUI)

**Scope:** `AttendanceScreen`, `DailyLogListScreen`, `EquipmentHistoryScreen`.

## 1. Craft
- Rebuild forms and lists using `FTextField`, `FBadge` (for status pills), and `FCard`.

## 2. Polish
- Fix the numerous hardcoded color violations (like `Colors.green.shade700` and `Colors.orange.shade50`) from the 28.1 audit by routing them through standard ForUI semantic tokens (e.g. destructive, primary).

## 3. Audit
- Verify layout constraints on mobile viewports for these dense data screens.
- Fix broken widget finders in tests for these screens.
- Ensure no logic, state, or data-fetching changes occurred.
