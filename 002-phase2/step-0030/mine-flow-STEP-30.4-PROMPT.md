# Substep 30.4: Reports, Data Bucket & Notifications (ForUI)

**Scope:** `TimelinePage`, `ReportDashboardPage`, `ReportConfigPage`, `DataBucketListPage`, `UploadFilePage`, `FileDetailPage`, `NotificationListPage`.

## 1. Craft
- Replace all lists, file pickers buttons, and timeline UI elements with ForUI widgets. 
- Use `FBadge` for file types and notification severities.

## 2. Polish
- Remove the `Colors.red`, `Colors.blue` etc., hardcodes used in file icons and notification banners. Route them through `FTheme` semantic tokens.

## 3. Audit
- Ensure `SingleTickerProviderStateMixin` animations from the Phase 2 polish still behave correctly with ForUI widgets.
- Fix broken widget finders in tests for these screens.
- Ensure no logic, state, or data-fetching changes occurred.
