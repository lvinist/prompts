# Substep 30.2: Operations & Tracking (ForUI)

**Scope:** `CutFillListScreen`, `LandClearingSummaryScreen`, `InventoryDashboardScreen`.

## 1. Craft
- Swap all Material cards, buttons, lists, and inputs for their `forui` equivalents (`FCard`, `FButton`, `FTextField`, etc.).

## 2. Polish
- Apply strict ForUI Zinc theme tokens. 
- Eliminate any hardcoded colors or padding identified in the 28.1 audit for these files.

## 3. Audit
- Ensure no raw Material `ThemeData` calls remain in this feature area.
- Fix broken widget finders in tests for these screens.
- Ensure no logic, state, or data-fetching changes occurred.
