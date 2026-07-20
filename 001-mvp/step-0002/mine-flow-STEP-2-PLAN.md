# STEP-2 PLAN — Scaffold mine-flow-app Repo & Skeleton

**Phase:** 1 — MVP  
**STEP:** 2  
**Status:** Done  
**Branch:** `step-0002-scaffold-app`  
**Repos touched:** `mine-flow-app` (new), `mine-flow-docs` (registries + ADR), `prompts`  
**Started:** 2026-07-18  
**Closed:** 2026-07-18

---

## Goal

Create the `Code/mine-flow-app/` Flutter repository — the single unified client
described in Doc 03 (Architecture Overview, § Top-Level Components). This STEP
produces **structure only**: directory layout, configuration files, pubspec with
pinned dependencies, placeholder entry point, CI gate, and license files.
No feature logic is written here — that starts at STEP-3.

---

## Substeps

| # | Task | Output | Status |
|---|------|--------|--------|
| 2.1 | Reserve & flip STEP-2 in STEP-index.md | `prompts/STEP-index.md` | Done |
| 2.2 | `flutter create` base app | `Code/mine-flow-app/` | Done |
| 2.3 | Reshape into Clean Architecture folder layout | `lib/` tree | Done |
| 2.4 | Write `pubspec.yaml` with full dependency set | `pubspec.yaml` | Done |
| 2.5 | Write `analysis_options.yaml` | `analysis_options.yaml` | Done |
| 2.6 | Write `lib/main.dart` + `lib/app/` wiring + theme | `lib/` | Done |
| 2.7 | Write `.env.example` | `.env.example` | Done |
| 2.8 | Write `README.md` (from template) | `README.md` | Done |
| 2.9 | Write `ARCHITECTURE.md` | `ARCHITECTURE.md` | Done |
| 2.10 | Write `.github/workflows/ci.yml` (Flutter CI) | `.github/workflows/ci.yml` | Done |
| 2.11 | Apply project license (MIT) | `LICENSE`, `LICENSE-THROUGHSTONE`, `LICENSING.md` | Done |
| 2.12 | `git init` + initial commit | local git history | Done |
| 2.13 | Update `registries/repos.yml` | `mine-flow-docs/registries/repos.yml` | Done |
| 2.14 | Write ADR-0001 (Hive over SQLite) | `mine-flow-docs/adr/ADR-0001-local-storage-hive.md` | Done |
| 2.15 | Run `flutter pub get` + `flutter analyze` + `flutter test` | — | Done |
| 2.16 | Flip STEP-2 to Done in STEP-index.md | `prompts/STEP-index.md` | Done |

---

## Decisions made in this STEP

| # | Decision | Choice | Rationale | Forecloses |
|---|----------|--------|-----------|------------|
| D-1 | Local offline DB (answers OQ-2 from Doc 15) | **Hive** | Works on Web target (no native binary needed), fast for key-value sync queue, pure Dart | SQLite/sqflite (Android-only native binary) |
| D-2 | Flutter SDK constraint | `>=3.12.2 <4.0.0` | Matches installed Flutter 3.44.5 / Dart 3.12.2 | — |
| D-3 | State management scaffolded | BLoC (`flutter_bloc`) | Matches Doc 15 decision; `equatable` included for state value equality | — |
| D-4 | Routing | `go_router` | Declarative, supports deep links, web URL-based nav for supervisor surface | — |

---

## Conditional sessions considered

None — all conditional sessions were addressed in STEP-1.

---

## Environment context

- Flutter: 3.44.5 (stable channel)
- Dart: 3.12.2
- DevTools: 2.57.0
- OS: Windows 11

---

## Next STEP

**STEP-3 — Core Data Layer & Authentication**  
Implement Supabase schema, RLS policies, auth flow, generate Dart models, and
set up the offline caching foundation (Hive boxes + sync queue).  
Start a fresh chat and say: *"Run STEP-3: Core Data Layer & Authentication"*
