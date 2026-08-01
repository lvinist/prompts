# mine-flow — STEP-36.1: Benchmark Domain & Data Layer

> **How to run:** Tell your agent *"run substep 36.1"* (or *"read and run this file"*).

## Context
This is the first substep for STEP-36 (Benchmark Database Feature). We are creating the Domain and Data layers for the `Benchmark` entity in `mine-flow-app`. We will also implement a Coordinate Reference System (CRS) utility to convert UTM coordinates into Latitude and Longitude.

## Read these first
- overview.md
- architecture/04-data-model.md (Focus on Benchmark entity)
- coding-standards/README.md

## Scope
- Create the Domain layer (Entities, Repository interfaces, Usecases).
- Create the Data layer (Models, Local/Remote Data Sources, Repository implementations).
- Implement a CRS conversion utility (e.g., using `proj4dart`) to convert UTM (like Zone 51 South) to Lat/Lon.
- Do NOT build the UI in this substep.

## Your task
1. **CRS Utility**: Implement a coordinate conversion utility in `lib/core/utils/crs_utils.dart`. Add required packages (like `proj4dart`) to `pubspec.yaml` if needed. The utility should accept Northing, Easting, and a CRS identifier (e.g. 'UTM Zone 51S') and return Latitude and Longitude.
2. **Domain Layer**: Create `Benchmark` entity in `lib/features/benchmark/domain/entities/benchmark.dart`. Include fields: `id` (String UUID), `bmId` (String), `northing` (double), `easting` (double), `orthoHeight` (double), `code` (String), `orde` (String), `geom` (dynamic/String? for PostGIS geometry), `latitude` (double), `longitude` (double), `ellipsHeight` (double), `status` (String).
3. Create repository interface `BenchmarkRepository` and CRUD usecases.
4. **Data Layer**: Create `BenchmarkModel` extending the entity with `fromJson`/`toJson` methods.
5. Create `BenchmarkLocalDataSource` (using Hive) and `BenchmarkRemoteDataSource` (using Supabase).
6. Implement `BenchmarkRepositoryImpl`.
7. Generate required adapters (`build_runner`) if using Hive TypeAdapters.

## Verification
- **Write unit tests** for `crs_utils.dart` to verify UTM to Lat/Lon conversions are mathematically accurate.
- **Write unit tests** for `BenchmarkModel` JSON serialization/deserialization.
- **Write unit tests** for `BenchmarkRepositoryImpl`.
- Run timing: Run `flutter test` for these tests before marking this substep done.

## Keeping the docs true (always)
- Update any architectural references if you deviate from the planned data model.

## Definition of done
- [ ] CRS utility implemented and tested.
- [ ] Domain layer created.
- [ ] Data layer created.
- [ ] Code is covered by relevant unit tests, and those tests pass.
- [ ] Classes and methods are properly documented.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 36.2"*, in a fresh chat.
