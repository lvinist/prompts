# mine-flow — STEP-36 PLAN: Benchmark Database Feature

**Phase:** Phase 2 Tier 2
**Owner:** DeepSeek V4 Flash High
**Status:** Planned
**Date:** 2026-07-24
**Branch:** `step-0036-benchmark-database`
**Repos (projection):** `mine-flow-app`

> Scaffolds the domain, data, and presentation layers for the new Benchmark Database feature under Operations, allowing field surveyors to track control points offline and sync to Supabase.

## Motivation
With the architecture and core UI established in Phase 2, we need to introduce the Benchmark Database feature to manage survey control points (BMs). These control points require offline creation in the field via UUIDs and a comprehensive data model. This STEP provides the end-to-end implementation for Benchmarks, including automatic coordinate conversion from UTM to Lat/Lon.

## Decisions already locked
- root `.throughstone/local-user.md` — read Experience level before user-facing questions or explanations, and read Communication style before planning discussions.
- `architecture/04-data-model.md` — The `Benchmark` entity structure: `id` (UUID Primary Key), `bm_id` (Text), `northing`, `easting`, `ortho_height`, `code`, `orde`, `geom` (PostGIS geometry), `latitude`, `longitude`, `ellips_height`, and `status`.
- `architecture/07-ui-design-system.md` v0.2.0 — Use ForUI (`FThemes.zinc`) for presentation layers. All new screens must strictly use ForUI widgets (`FCard`, `FButton`, `FTextField`, etc.).
- Offline-first architecture using Hive for local caching and a `SyncRegistrar` pattern to synchronize data to Supabase when online.
- **Coordinate System**: Latitude and Longitude will be automatically calculated based on the entered Northing/Easting and an identified CRS (e.g., UTM Zone 51 South).

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 36.1 | Benchmark Domain, Data Layer & CRS | `lib/features/benchmark/domain/`, `lib/features/benchmark/data/`, `lib/core/utils/` | Data Model | |
| 36.2 | Benchmark UI & BLoC | `lib/features/benchmark/presentation/` | 36.1 | |
| 36.3 | Offline Sync & Verification | `SyncRegistrar` implementation, unit/widget tests | 36.2 | |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Unit | 36.1, 36.2, 36.3 | BLoC, Models, Repository, CRS Utils | Per substep | `flutter test` | Include tests for accurate UTM to Lat/Lon conversion |
| Integration / data | 36.3 | Local/Remote Data Sources, Sync | Per substep | `flutter test` | Ensure offline creation (UUID) works |
| End-to-end / user flow | 36.3 | Benchmark CRUD UI testing | Final verification | `flutter test` | |

## Open questions
- None currently.

## Ground rules
- **Calibrate communication from root `.throughstone/local-user.md`.** Substep prompts should read the recorded Experience level and adjust explanations/questions accordingly.
- **Plan interactively.** Before this PLAN is finalized, confirm scope with the user and ask clarifying questions for ambiguous requirements.
- **Tests ship with the code.** Every substep that writes or changes code also writes or updates the relevant tests for it.
- **Code is documented as it's written.** Every class, function, and method gets a docstring.
- **Accepted risks stay visible.** If this STEP accepts a risk or defers tech debt, add or update `registries/risks.yml`.

## Definition of done
- [x] Substep 36.1 completed (Domain, Data Layer & CRS util).
- [x] Substep 36.2 completed (Presentation Layer).
- [x] Substep 36.3 completed (Sync Integration & Testing).
- [x] The STEP test plan is complete: each code-changing substep either added/updated its relevant tests or records why tests were not applicable.
- [x] All tests named in the STEP test plan pass at the end of this STEP.
- [x] STEP review passed; prompts/STEP-index.md updated; STEP archived to prompts/.
