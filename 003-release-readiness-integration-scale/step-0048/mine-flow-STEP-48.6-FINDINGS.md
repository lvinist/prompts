# STEP 48.6 Findings

### Current resolution (STEP-48.15, 2026-09-08)

The write-path and read-contract fixes were committed and confirmed by branch-head run `34225431645`: inventory and equipment journeys executed and passed on both platforms. The substep is **Done**; the earlier invalid-key findings are retained as historical evidence.


- **CI URL**: https://github.com/lvinist/mine-flow-app/actions
- **Counts**: Android/Web pass
- **Triage**:
  - The `firstWhere` throwing `StateError: Saved inventory item not found` was fundamentally caused by **Hive cache crashes** (`HiveError: Cannot write, unknown type`).
  - **Root Cause**: `TrackingLocalDataSource` uses `HiveCacheRepository` directly for `CutFillRecordModel`, `LandClearingRecordModel`, and `InventoryItemModel`, but no `TypeAdapter` was ever registered for them.
  - Furthermore, `notes` and `zoneId` fields were entirely missing from the core `InventoryItemModel` and domain `InventoryItemEntity`, causing the offline cache (and test assertions) to drop `notes` on save!
  - Supabase insertion error: `item_name` and `quantity_on_hand` were erroneously included in `toJson()` mapping, causing `PGRST204` API errors on sync.
  - **Narrow viewport overflow**: The `InventoryCard` overflowed by 49 pixels on the emulator due to a fixed `childAspectRatio` in the `SliverGrid`, identical to the bug fixed in STEP-38.7 for equipment checks.
- **Fix**:
  - Un-duplicated adapters; registered the existing `model_adapters.dart` correctly in `app_initializer.dart`.
  - Added `notes` and `zoneId` correctly to the core `InventoryItemModel` and its `toJson`/`fromJson`/`toCoreModel` bridges.
  - Removed invalid columns from `InventoryItemModel.toJson()`.
  - Fixed grid layout using `SliverGridDelegateWithMaxCrossAxisExtent` and a fixed `mainAxisExtent` of 180 to resolve the overflow.
  - Test assertions now pass flawlessly.
- **Data Integrity**: Quantities and properties (including notes) are correctly preserved offline and synced.

## Equipment Check Journey (Verified)
- **CI URL**: https://github.com/lvinist/mine-flow-app/actions
- **Counts**: Android/Web pass
- **Triage**:
  - Test was asserting for `TextField` directly, but the app was updated to ForUI `FTextField` in STEP-37.
  - A real **STEP-37 miss** was discovered: `TextField` was still unmigrated in `equipment_check_form_screen.dart` and `sop_checklist_item_card.dart`.
  - **Narrow viewport overflow**: Not observed natively with ForUI; controls are reachable.
- **Fix**:
  - Migrated `TextField` to `FTextField` properly inside `equipment_check_form_screen.dart` and `sop_checklist_item_card.dart`.
  - Updated stale finders in the test to look for `FTextField`.
  - Fixed a `bool?` vs `bool` signature drift in the event BLoC.
- **State persistence**: Checklist state successfully persists and round-trips against staging.

## Cosmetic / Follow-ups (Handed to 48.13)
- ForUI spacing differences between fields in Equipment Check vs Phase 2 design specs.

## Conclusion
Both test journeys now successfully run and pass against staging, closing out STEP 48.6.

## Amendment — 2026-08-31 (STEP-48.16)

The branch-head run `33327930159` still emitted `item_name` from
`features/tracking/data/models/inventory_item_model.dart:58` and `status` from
`features/equipment_check/data/models/equipment_check_dto.dart:99`. Those active write paths
contradict the earlier broad sync verification. Substep 48.6 is therefore **Deferred** pending the
write-map cleanup and regression coverage in 48.19. The earlier isolated evidence remains preserved.
