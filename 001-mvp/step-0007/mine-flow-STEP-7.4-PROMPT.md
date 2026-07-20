# mine-flow — STEP-7.4: Inventory Tracking UI & State

> **How to run:** Tell your agent *"run substep 7.4"* (or *"read and run this file"*).

## Context
This is substep 7.4 of STEP-7 (Tier 2 - Field Tracking & Measurement). In this substep, you will implement the UI screens and state management for Inventory Tracking (materials, tools, consumables).

## Read these first
- `overview.md`
- `Code/mine-flow-docs/architecture/04-data-model.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Upcoming Prompts/mine-flow-STEP-7-PLAN.md`

## Scope
- BLoC / State Management (`lib/features/tracking/presentation/bloc/inventory/`):
  - `inventory_bloc.dart`, `inventory_event.dart`, `inventory_state.dart`: Load inventory items, add/edit inventory items, adjust stock quantity (+/-), filter by category/zone, low stock alerts.
- Presentation Screens & Widgets (`lib/features/tracking/presentation/pages/inventory/`):
  - `inventory_dashboard_screen.dart`: Inventory catalog list with stock level badges (Normal, Low Stock warning banner), filter tabs (All, Fuel/Lubricants, Explosives/Blasting, Spare Parts, Consumables, Safety Equipment).
  - `inventory_item_entry_screen.dart`: Form to register a new inventory item or edit details (name, category, unit, quantity on hand, minimum threshold level).
  - `stock_adjustment_dialog.dart`: Quick modal/dialog to increment/decrement item stock with transaction reason/notes.

## Your task
1. Implement `InventoryBloc` supporting item listing, stock updates, filtering, and low-stock state evaluation.
2. Build `InventoryDashboardScreen` with category filter tabs and visual low-stock indicator badges when `quantity_on_hand <= min_threshold`.
3. Build `InventoryItemEntryScreen` for item creation and editing.
4. Build `StockAdjustmentDialog` for fast field updates (e.g. logging 500L diesel consumed).

## Verification
- UI components render without layout errors.
- Low-stock badge correctly triggers when threshold criteria are met.

## Definition of done
- [ ] `InventoryBloc` implemented.
- [ ] `InventoryDashboardScreen` built with category filtering and low-stock alerts.
- [ ] `InventoryItemEntryScreen` and `StockAdjustmentDialog` completed.

## Next
**Before finishing this task, you MUST do the bookkeeping:**
1. Open `prompts/STEP-index.md` and change the Status of Substep 7.4 from `Planned` to `Done`. Update the Output / Deliverables column with the paths you created.
2. Open `Upcoming Prompts/mine-flow-STEP-7-PLAN.md` and check off `[x] Substep 7.4` in the Definition of done section.
3. Finally, tell the user to *"run substep 7.5"* in a fresh chat.
