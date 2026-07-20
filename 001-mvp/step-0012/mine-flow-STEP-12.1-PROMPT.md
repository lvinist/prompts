# Substep 12.1: Router & UI Shell Integration

**Goal:** Make orphaned capability screens reachable via GoRouter and the Dashboard UI.

**Context:** The following files exist but are completely unregistered in the app's routing table:
- Cut/Fill: `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
- Land Clearing: `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart`
- Crew Attendance: `lib/features/attendance/presentation/pages/attendance_screen.dart`
- Daily Logging: `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart`
- Inventory: `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
- Equipment Check: `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`

**Action Plan:**
1. **Update `lib/app/router.dart`**:
   - Add static route constants in `AppRoutes` (e.g., `cutFill`, `landClearing`, `dailyLog`, `inventory`, `equipmentCheck`). Note: `AppRoutes.attendance` already exists but isn't used in the `routes` list.
   - Inject these routes into the `GoRouter` instance under the authenticated `AppShell` routes. Group them logically (e.g., under the Dashboard branch or new dedicated branches if they should appear in the bottom NavigationBar). Provide any necessary BLoCs on route traversal using `appServices`.

2. **Update `lib/app/presentation/pages/dashboard_page.dart`**:
   - In `_QuickNavGrid`, add new `_NavCard` entries for:
     - Absensi (Attendance) -> `AppRoutes.attendance`
     - Log Harian (Daily Log) -> `AppRoutes.dailyLog`
     - Cut/Fill -> `AppRoutes.cutFill`
     - Land Clearing -> `AppRoutes.landClearing`
     - Inventaris (Inventory) -> `AppRoutes.inventory`
     - Cek Alat (Equipment Check) -> `AppRoutes.equipmentCheck`
   - Adjust `crossAxisCount` and sizing if necessary to accommodate the new cards.

**Acceptance Criteria:**
- All 6 screens can be navigated to via the Dashboard quick navigation cards without throwing exceptions.
- The GoRouter configuration successfully provides necessary Repositories to the destination screens.
