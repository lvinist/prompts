# mine-flow — STEP-7.1: Field Tracking Domain & Data Layer

> **How to run:** Tell your agent *"run substep 7.1"* (or *"read and run this file"*).

## Context
This is substep 7.1 of STEP-7 (Tier 2 - Field Tracking & Measurement). In this substep, you will build the domain entities, repository contracts, data models (with JSON serialization for Supabase Postgres), Hive local storage models, and repository implementations for three key field tracking capabilities:
1. Cut/Fill Volume Tracking (`CutFillRecord`)
2. Land Clearing Area Tracking (`LandClearingRecord`)
3. Inventory Tracking (`InventoryItem` / `InventoryLog`)

## Read these first
- `overview.md`
- `Code/mine-flow-docs/architecture/04-data-model.md`
- `Code/mine-flow-docs/architecture/03-architecture-overview.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-app/README.md`

## Scope
- Domain Layer (`lib/features/tracking/domain/`):
  - `entities/cut_fill_record.dart`: Entity for earthwork volume (cut_volume_m3, fill_volume_m3, net_volume_m3, zone_id, site_id, measurement_date, notes, created_by, timestamps).
  - `entities/land_clearing_record.dart`: Entity for land clearing area (area_cleared_m2, clearing_method, zone_id, site_id, clearing_date, notes, created_by, timestamps).
  - `entities/inventory_item.dart`: Entity for tracked inventory items (item_name, category, unit, quantity_on_hand, min_threshold, zone_id, site_id, notes, timestamps).
  - `repositories/tracking_repository.dart`: Abstract repository interface for Cut/Fill, Land Clearing, and Inventory operations.
- Data Layer (`lib/features/tracking/data/`):
  - `models/cut_fill_model.dart`: Data model extending domain entity with `fromJson`, `toJson`, and Hive TypeAdapter annotations.
  - `models/land_clearing_model.dart`: Data model extending domain entity with `fromJson`, `toJson`, and Hive annotations.
  - `models/inventory_item_model.dart`: Data model extending domain entity with `fromJson`, `toJson`, and Hive annotations.
  - `datasources/tracking_remote_datasource.dart`: Interfacing with Supabase REST API (`cut_fill_records`, `land_clearing_records`, `inventory_items` tables).
  - `datasources/tracking_local_datasource.dart`: Hive boxes for offline caching (`cut_fill_box`, `land_clearing_box`, `inventory_box`).
  - `repositories/tracking_repository_impl.dart`: Implementation managing local caching and remote fetches.

## Your task
1. Implement the domain entities with `Equatable` or immutability support.
2. Implement the data models with Supabase JSON mapping and Hive type adapters (register Hive adapters in service locator/app init if needed).
3. Implement `TrackingRemoteDataSource` using `SupabaseClient`.
4. Implement `TrackingLocalDataSource` using Hive boxes.
5. Implement `TrackingRepositoryImpl` coordinating remote and local sources with offline fallback.

## Verification
- Code compiles without syntax or type errors (`flutter analyze` or Dart compiler check).
- Domain and Data layers follow Clean Architecture guidelines and present clear docstrings.

## Definition of done
- [ ] Domain entities created for `CutFillRecord`, `LandClearingRecord`, and `InventoryItem`.
- [ ] Data models with JSON and Hive conversion implemented.
- [ ] Data sources (remote Supabase & local Hive) created.
- [ ] Repository implementation completed.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user to *"run substep 7.2"* in a fresh chat.
