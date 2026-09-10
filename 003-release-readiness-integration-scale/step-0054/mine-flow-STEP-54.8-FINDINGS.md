# mine-flow — STEP-54.8 Findings: Inventory Management Critique

**Date:** 2026-09-11
**Executor:** Antigravity (Gemini 3.1 Pro High)
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique`
**Scope:** Inventory Management (under tracking module) - Dashboard, Item Entry, Stock Adjustment, and Report entry point.

This is a static critique. Branch-head `file:line` citations provide the mandatory evidence floor. No runtime capture was performed, so dialog sizing/scrim behavior, IME insets, rendered hit targets, contrast, focus, screen-reader output, and URL behavior remain `Unverified`.

## 1. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| Stock Dashboard | Web + Android | List loading, empty, category filters, low-stock banner | `inventory_dashboard_screen.dart:154-461` | Needs restructure (Routing, D6) |
| Item Entry Form | Web + Android | Dirty state interception, routing, field layout | `inventory_item_entry_screen.dart:188-530` | Needs restructure (D1/D2/D4/D5) |
| Stock Adjustment Dialog | Web + Android | Static quantity/reason/confirmation flow and D6 precedent | `stock_adjustment_dialog.dart:48-272` | Aligned modality; Needs restructure for transaction integrity/history; runtime sizing/IME Unverified |
| Architecture / Placement | N/A | Module boundaries and state coupling (`inventory` under `tracking`) | `inventory/inventory_bloc.dart:13-34` | Aligned |

## 2. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.8-001 | Needs restructure | D1/D2/D5 Routing | The dashboard pushes `InventoryItemEntryScreen` via `MaterialPageRoute` for both creation and editing. The router lacks a `/teams/inventory/form` route, violating GoRouter URL synchronization and the D1/D2 modal sheet pattern. | `inventory_dashboard_screen.dart:398-417`, `463-482` | Migrate the form to the route-backed modal sheet adapter. |
| FC-54.8-002 | Needs restructure | D4 Dirty Intercept | The item entry form uses `Navigator.of(context).pop()` without a `PopScope`. Unsaved edits are not intercepted and are silently discarded when the user navigates back. | `inventory_item_entry_screen.dart:203-205`, `295-297` | Implement D4 dirty-intercept wrapper for the form. |
| FC-54.8-003 | Needs restructure | D6 Report Modal | The "Buat Laporan" action pushes a standalone `report-config` route via `context.pushNamed`, losing the dashboard's category filter context. This conflicts with D6's contextual modal dialog pattern. | `inventory_dashboard_screen.dart:116-119` | Replace standalone routing with a contextual report `FDialog`. |
| FC-54.8-004 | Needs polish | Dashboard UI | Low-stock state is color-independent because both the dashboard and item card pair destructive styling with an alert icon and explicit threshold copy, and the summary card balances aggregate metrics against item cards. However, the domain collapses zero stock and below-threshold stock into one `isLowStock` boolean, so the dashboard cannot distinguish out-of-stock from reorder-warning severity. | `inventory_dashboard_screen.dart:267-333`; `inventory_card.dart:92-120`; `inventory_item.dart:35-37` | Preserve the summary/detail balance, but add explicit out-of-stock vs. low/reorder states and semantic labels during STEP-55 polish. |
| FC-54.8-005 | Needs restructure | **Data Integrity** | The dialog captures a reason and includes it in `AdjustStockEvent`, but `_onAdjustStock` calls a repository contract accepting only ID and delta; persistence clamps and overwrites quantity without creating a transaction, so the reason and adjustment history are irretrievably lost. | `stock_adjustment_dialog.dart:250-263`; `inventory/inventory_bloc.dart:240-248`; `tracking_repository.dart:45-49`; `tracking_repository_impl.dart:302-315` | **CRITICAL:** Persist an immutable adjustment transaction (reason, signed delta, actor/time/idempotency metadata) and update quantity atomically. |
| FC-54.8-006 | Aligned | Module Placement | Although inventory resides under `tracking`, it has dedicated `InventoryBloc`/event/state types and its load/error paths depend only on inventory repository methods; no Cut/Fill or Land Clearing presentation state leaks into this UI. | `inventory/inventory_bloc.dart:8-34, 47-68` | Accept placement for STEP-55 unless a broader module-boundary refactor is separately justified. |
| FC-54.8-007 | Needs restructure | D7 Detail View | Tapping an item opens the edit form directly. The stock adjustment dialog is the only place stock changes occur, but adjustment history is not visible anywhere. | `inventory_dashboard_screen.dart:397-407` | Implement an item detail view (D7) to display stock history/logs instead of directly jumping to edit mode. |
| FC-54.8-008 | Needs polish | Token / Material | Residual Material primitives remain: dashboard FABs, the entry form's `DropdownButtonFormField`, and adjustment-dialog `TextFormField`s. | `inventory_dashboard_screen.dart:108-143`; `inventory_item_entry_screen.dart:330-361`; `stock_adjustment_dialog.dart:166-196` | Swap residual primitives for ForUI equivalents while preserving numeric keyboard behavior. |
| FC-54.8-009 | Aligned | Stock adjustment modality | Adjustment already uses `showFDialog` + `FDialog`, keeps the dashboard mounted, shows current stock/threshold and a computed next-stock preview, and offers explicit cancel/confirm actions; this is a useful contextual-dialog precedent. | `inventory_dashboard_screen.dart:419-435`; `stock_adjustment_dialog.dart:43-128, 198-268` | Preserve contextual modality while adding transaction persistence and responsive runtime tests. |
| FC-54.8-010 | Needs polish | Mobile touch targets / semantics | Inventory-card adjust/delete actions explicitly remove `IconButton` constraints and padding; the delete action also lacks a tooltip/semantic label, so source does not guarantee 48dp targets or an accessible name. | `inventory_card.dart:154-177` | Use labelled `FIconButton`s or enforce 48x48dp semantic hit regions for both actions. |
| FC-54.8-011 | Unverified | Runtime dialog / accessibility | Static code cannot prove FDialog scrim dismissal, narrow-screen sizing, numeric IME inset handling, focus order, contrast, rendered touch targets, or screen-reader announcements. | `stock_adjustment_dialog.dart:43-272`; `inventory_card.dart:154-177` | Verify Web and Android dialog behavior in STEP-55.11 with valid runtime and accessibility evidence. |

## 3. D7 Verdict

The current implementation lacks an item detail view, navigating directly to the edit form upon tapping an item card. Furthermore, stock adjustments capture reasons that are completely discarded because there is no stock history log. A read-only detail view **must be implemented** to display the item's adjustment transaction history, satisfying D7.

## 4. Verification record

- **Evidence standard:** All findings use `file:line` citations from the branch head.
- **Visual / Runtime claims:** Explicitly Unverified in FC-54.8-011 and the coverage table; no runtime pass is inferred from source.
- **Findings ledger:** Pass — 11 sequential IDs; every finding has a verdict and branch-head citation.
- **Code modification:** No application code was modified. App repo is clean on `step-0054-feature-cohesion-critique`.
- **Escalation:** Data-integrity loss (FC-54.8-005) explicitly escalated.

## 5. Limitations

- Static analysis only. Dialog scrim/sizing, Android IME behavior, rendered targets, focus, screen-reader output, contrast, and deep-link behavior remain Unverified.
