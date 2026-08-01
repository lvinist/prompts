# Phase 2 Tier 1 Cross-Screen Consistency Audit (Substep 28.1)

This document outlines the inconsistencies found across the 15 screens built during Phase 2 Tier 1, based on the requirements defined in `DESIGN.md`.

## 1. Animation & Curve Drift
`DESIGN.md` explicitly specifies `Curves.easeOutQuart` for transitions.
- **daily_log_list_screen.dart**: Uses `Curves.easeInQuart` (L96).
- **cut_fill_list_screen.dart**: Uses `Curves.easeInQuart` (L104). Uses `TweenAnimationBuilder` without standard parameters.
- **inventory_dashboard_screen.dart**: Uses `Curves.easeInQuart` (L104) and `Curves.easeOutBack` (L237). Uses `TweenAnimationBuilder` without standard parameters.
- **land_clearing_list_screen.dart**: Uses `Curves.easeInQuart` (L103). Uses `TweenAnimationBuilder` without standard parameters.

## 2. Spacing Scale Violations
`DESIGN.md` defines a strict spacing scale: 4, 8, 12, 16, 20, 24, 32 dp.
The following non-standard values were found and need rounding to the nearest standard scale value:
- **10 dp** (Found in `attendance_screen.dart`, `attendance_summary_card.dart`, `status_toggle_chips.dart`, `auto_save_indicator.dart`, `equipment_history_screen.dart`, `equipment_type_tabs.dart`, `timeline_page.dart`) -> Should be `8` or `12`.
- **6 dp** (Found in `file_detail_page.dart`, `equipment_check_card.dart`, `sop_checklist_item_card.dart`, `timeline_chart.dart`, `timeline_page.dart`, `cut_fill_card.dart`, `inventory_card.dart`, `land_clearing_card.dart`) -> Should be `4` or `8`.
- **14 dp** (Found in `file_detail_page.dart`) -> Should be `12` or `16`.
- **5 dp, 3 dp** (Found in `notification_badge.dart`, `equipment_check_card.dart`) -> Should be `4`.
- **80 dp** (Found in `data_bucket_list_page.dart`) -> Valid for large spacer, but check if needed.
- Usage of `8.0`, `12.0`, `16.0` instead of integer constants (e.g., in `cut_fill_form_screen.dart`, `attendance_screen.dart`).

## 3. Typography Violations (Hardcoded TextStyles)
`DESIGN.md` requires using the theme's text styles (e.g. `Theme.of(context).textTheme...`) rather than hardcoding `TextStyle(...)`.
Many files hardcode `TextStyle` with specific font sizes instead of using semantic text theme.
- **Offending files:** `attendance_screen.dart`, `daily_log_form_screen.dart`, `file_detail_page.dart`, `equipment_check_card.dart`, `inventory_card.dart`, etc.
- **Action for 28.3:** Replace direct `TextStyle(fontSize: X)` instantiations with `Theme.of(context).textTheme.bodySmall` / `bodyMedium` / `titleSmall` / `labelSmall` depending on context, using `.copyWith` if color/weight overrides are needed.

## 4. Hardcoded Color Usage
`DESIGN.md` dictates using theme colors (`colorScheme`) or semantic colors. There are extensive usages of `Colors.red`, `Colors.green`, `Colors.orange`, `Colors.grey`, `Colors.teal`, `Colors.blue` which should be refactored to use semantic theme colors (e.g. `colorScheme.error`, `colorScheme.primary`, `colorScheme.tertiary`, `colorScheme.outline`, or custom semantic color extensions if applicable), especially considering dark/light mode compatibility.
- **Forms/Lists** (`daily_log_form_screen.dart`, `cut_fill_form_screen.dart`, `inventory_item_entry_screen.dart`, `land_clearing_entry_screen.dart`): Extensive use of `Colors.green.shade700`, `Colors.red`, `Colors.grey`.
- **Cards** (`daily_log_card.dart`, `file_card.dart`, `cut_fill_card.dart`, `inventory_card.dart`, `land_clearing_card.dart`): Use of `.shade50`, `.shade800`, `Colors.red.shade300`, etc.
- **Timeline** (`timeline_page.dart`, `timeline_chart.dart`): Uses `Colors.blue`, `Colors.orange`, `Colors.green` directly.

**Next Steps for Substep 28.3**: Go through the findings in this audit and standardise the codebase to conform strictly to `DESIGN.md`.
