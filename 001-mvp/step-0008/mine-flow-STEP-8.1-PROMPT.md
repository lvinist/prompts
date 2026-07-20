# mine-flow — STEP-8.1: Data Bucket Domain & Data Layer

> **How to run:** Tell your agent _"run substep 8.1"_ (or _"read and run this file"_).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is the first substep of **STEP-8 (Data Bucket Integration)**. It creates the domain and data layers for the **Data Bucket** feature — the `GeospatialFile` entity, its repository interface, the Supabase-backed implementation, Hive offline caching, and the Supabase database migration for the `geospatial_files` table. The `lib/features/data_bucket/` directory exists but is empty (only a `.gitkeep`).

## Read these first

- root `.throughstone/local-user.md` — active user's experience level (Level 2) and communication style (Explanatory); if missing, ask the two local-profile questions from `BOOTSTRAP-PROMPT.md` Stage 0, create it, and calibrate explanations/questions to it
- `Code/mine-flow-docs/architecture/04-data-model.md` — defines the `GeospatialFile` entity, its relationships, and retention rules
- `Code/mine-flow-docs/architecture/03-architecture-overview.md` & `15-native-app-architecture.md` — Clean Architecture layout and BLoC/Cubit state management patterns
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — test tiers, coverage priorities, mocking strategy
- `Code/mine-flow-docs/architecture/11-interface-contracts.md` — App ↔ Supabase and App ↔ Google Drive boundary contracts
- Existing feature implementations for reference patterns: `lib/features/tracking/domain/` and `lib/features/tracking/data/` — follow the same Clean Architecture structure (entities, repository interface, models, datasources, Hive adapters, repository impl, barrel exports)

## Scope

**Owns:**

- Supabase database migration for the `geospatial_files` table
- `lib/features/data_bucket/domain/` — entity, repository interface, domain barrel
- `lib/features/data_bucket/data/` — models (Supabase model + Hive model), datasource (Supabase datasource), Hive adapter, repository implementation, data barrel
- Unit tests for model serialization, Hive adapter mapping, and repository CRUD with offline fallback

**Does NOT touch:**

- Google Drive API integration (substep 8.2)
- UI screens, BLoCs, or presentation logic (substep 8.3)
- SyncQueueManager bindings (substep 8.4)
- Any other feature or core module outside `lib/features/data_bucket/`

## Your task

### 1. Supabase migration

Create a new Supabase migration file in the app repo's `supabase/migrations/` directory (or wherever existing migrations live — check for the pattern from STEP-3). Name it with the next timestamp/number after the latest migration. The migration should create the `geospatial_files` table:

```sql
-- GeospatialFiles: metadata registry for survey files stored on Google Drive
CREATE TABLE geospatial_files (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  site_id       UUID NOT NULL REFERENCES sites(id) ON DELETE RESTRICT,
  zone_id       UUID REFERENCES zones(id) ON DELETE SET NULL,
  file_name     TEXT NOT NULL,
  file_type     TEXT NOT NULL CHECK (file_type IN ('.shp', '.tiff', '.tif', '.dxf', '.dwg', '.csv', '.kml', '.kmz', '.gpx', '.pdf', 'other')),
  mime_type     TEXT,
  drive_file_id TEXT NOT NULL,
  drive_link    TEXT NOT NULL,
  file_size_bytes BIGINT,
  latitude      DECIMAL(10, 7),
  longitude     DECIMAL(10, 7),
  acquisition_date DATE,
  notes         TEXT,
  uploaded_by   UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for search/filter
CREATE INDEX idx_geospatial_files_site ON geospatial_files(site_id);
CREATE INDEX idx_geospatial_files_zone ON geospatial_files(zone_id);
CREATE INDEX idx_geospatial_files_type ON geospatial_files(file_type);
CREATE INDEX idx_geospatial_files_acquisition ON geospatial_files(acquisition_date);
CREATE INDEX idx_geospatial_files_created ON geospatial_files(created_at);

-- RLS
ALTER TABLE geospatial_files ENABLE ROW LEVEL SECURITY;

-- Supervisors and Foremen can read all files; only Supervisors can insert/update/delete
CREATE POLICY "Supervisors full access" ON geospatial_files
  FOR ALL USING (
    EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role = 'supervisor')
  );

CREATE POLICY "Foremen read-only" ON geospatial_files
  FOR SELECT USING (
    EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role = 'foreman')
  );
```

(Adjust role table and `user_roles` lookup to match existing RLS patterns in the project — check a migration from STEP-3 or STEP-4 for the exact pattern used.)

### 2. Domain layer

Create `lib/features/data_bucket/domain/` with these files following the existing pattern (e.g., `lib/features/tracking/domain/`):

**`entities/geospatial_file.dart`** — the domain entity:

```dart
class GeospatialFile {
  final String id;
  final String siteId;
  final String? zoneId;
  final String fileName;
  final String fileType;       // '.shp', '.tiff', etc.
  final String? mimeType;
  final String driveFileId;
  final String driveLink;
  final int? fileSizeBytes;
  final double? latitude;
  final double? longitude;
  final DateTime? acquisitionDate;
  final String? notes;
  final String? uploadedBy;
  final DateTime createdAt;
  final DateTime updatedAt;

  const GeospatialFile({ /* all required + named optional params */ });

  // copyWith, toJson, fromJson if convention uses lightweight json methods
}
```

**`repositories/data_bucket_repository.dart`** — repository interface:

```dart
abstract class DataBucketRepository {
  Stream<List<GeospatialFile>> watchFiles({String? siteId, String? zoneId, String? fileType});
  Future<List<GeospatialFile>> getFiles({String? siteId, String? zoneId, String? fileType, String? searchQuery});
  Future<GeospatialFile?> getFile(String id);
  Future<GeospatialFile> saveFile(GeospatialFile file);  // local cache + Supabase
  Future<void> deleteFile(String id);
  Future<void> syncPendingUploads();
}
```

**`domain.dart`** — barrel export file (follow the pattern in `lib/features/tracking/domain/domain.dart`).

### 3. Data layer

Create `lib/features/data_bucket/data/` with:

**`models/geospatial_file_model.dart`** — Supabase-compatible model with `toJson()`/`fromJson()` mapping between `snake_case` (DB) and `camelCase` (Dart), plus `toHiveJson()`/`fromHiveJson()` for offline cache.

**`datasources/data_bucket_remote_datasource.dart`** — Supabase datasource wrapping `SupabaseClient` queries (select, insert, update, delete, stream). Follow the pattern from an existing datasource like `lib/features/tracking/data/datasources/`.

**`datasources/data_bucket_local_datasource.dart`** — Hive-local datasource for offline caching of `GeospatialFile` metadata. Follow the Hive pattern from existing features.

**`repositories/data_bucket_repository_impl.dart`** — implements `DataBucketRepository`. The pattern:

- **Read:** try remote first, fall back to local cache on failure
- **Write:** write to remote; if offline, cache locally and mark as pending sync
- **Sync:** flush pending local writes to Supabase when connectivity returns

**`models/hive/geospatial_file_hive_adapter.dart`** — Hive TypeAdapter for the local cache model. **EXTENSIVE REQUIREMENT**: Use `typeId: 7` for the `GeospatialFileModelAdapter`. Do not use `typeId` 4, 5, 6, 10, 11, or 12 as they are already taken by other features.

**EXTENSIVE REQUIREMENT ON `DataBucketRepositoryImpl`**:
- When `saveFile()` is called and device is offline or Drive upload succeeds but Supabase is unreachable, you **must** enqueue a mutation using `syncQueueManager.enqueueMutation(entityType: 'data_bucket_metadata_sync', action: SyncAction.update, payloadJson: file.toJson(), ...)`.
- Provide an explicit mapping implementation handling both offline and online states rigorously.

**`data.dart`** — barrel export file.

### 4. Update barrel exports

Ensure `lib/features/data_bucket/data_bucket.dart` (the feature's top-level barrel) exports both `domain.dart` and `data.dart`.

## Verification

- **Write unit tests** for:
  - Model serialization/deserialization (JSON ↔ Model, Hive JSON ↔ Model)
  - Hive adapter mapping
  - Repository CRUD with offline fallback (mock remote datasource; verify local cache serves as fallback)
- **Name the test files:** `test/features/data_bucket/data/models/geospatial_file_model_test.dart`, `test/features/data_bucket/data/repositories/data_bucket_repository_impl_test.dart`, etc.
- **Run:** `flutter test test/features/data_bucket/`
- **Run timing:** Tests are collected in substep 8.4 for final verification; run them now to verify your work, but they're officially gated in 8.4.

## Keeping the docs true

- The `GeospatialFile` entity is defined in `architecture/04-data-model.md`. If any fields are added or changed beyond what's listed there (e.g., new file types, new metadata fields), update the architecture doc and bump its Version Log.
- If a new domain term is coined (e.g., a specific file category), add it to `architecture/13-glossary.md`.
- If the repository interface or data model reveals a structured API surface (beyond what's documented in `11-interface-contracts.md`), update that doc.

## Definition of done

- [ ] Supabase migration created for `geospatial_files` table with proper indexes, RLS policies, and constraints
- [ ] `lib/features/data_bucket/domain/` created with `GeospatialFile` entity, repository interface, and barrel export
- [ ] `lib/features/data_bucket/data/` created with model, Supabase datasource, Hive datasource, repository implementation, and barrel export
- [ ] Unit tests written for model serialization, Hive adapter, and repository CRUD with offline fallback
- [ ] Any architecture doc changes reflected (Version Log bumped, glossary updated if needed)
- [ ] Any accepted risk or deferred tech debt recorded in `registries/risks.yml` or explicitly marked not applicable

## Next

When this substep is done, update its status in the STEP-8 PLAN, then run **substep 8.2** — _"run substep 8.2"_ — in a fresh chat. (STEP-8 PLAN: `Upcoming Prompts/mine-flow-STEP-8-PLAN.md`)
