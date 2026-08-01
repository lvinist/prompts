# mine-flow — STEP-32 PLAN: Shared Creatable Combobox & Zone State

**Phase:** Phase 2 Tier 2
**Owner:** Antigravity
**Status:** In progress
**Date:** 2026-07-23
**Branch:** `step-0032-creatable-combobox`
**Repos (projection):** `mine-flow-app`

> Builds a shared `CreatableCombobox` widget using ForUI that allows dynamically adding non-existent options, and wires up a shared local database box (Hive) for storing and retrieving Zones dynamically, replacing hardcoded mock data.

## Motivation

Currently, `ZonePicker` uses hardcoded mock data and `DropdownButtonFormField`. With the transition to ForUI, we need a reusable combobox widget that adheres to `FThemes.zinc` styling and allows users in the field to add new zones dynamically. This widget will be shared across the app, and the Zone state will be persisted locally using Hive to support offline operations.

## Decisions already locked

- root `.throughstone/local-user.md` — read **Experience level** before user-facing questions or explanations, and read **Communication style** before planning discussions.
- `registries/risks.yml` — review relevant accepted risks/debt before planning work that touches their area.
- The Test Strategy architecture doc (`architecture/12-test-strategy.md`) — use it to decide which test tiers this STEP must add or update.
- ADR-0007 / ADR-0008 — Phase 2 UI rebuild utilizing `forui`.
- architecture/07-ui-design-system.md (v0.2.0) — ForUI widgets and Zinc theme.

## Substeps

| #       | Title                                   | Produces                                                | Depends on | Open questions |
| ------- | --------------------------------------- | ------------------------------------------------------- | ---------- | -------------- |
| 32.1 ✅ | Zone Hive Adapter & Local Storage       | Hive TypeAdapter, Zone local storage box                | None       |                |
| 32.2 ✅ | Shared `CreatableCombobox` Widget       | `lib/core/presentation/widgets/creatable_combobox.dart` | 32.1       |                |
| 32.3 ✅ | Integration with `ZonePicker` & Testing | Updated `zone_picker.dart` and BLoC/Cubit, Tests        | 32.2       |                |

## Test plan

| Test tier / surface | Substep(s)    | Tests to create or update                                     | Run timing  | Command / gate | Notes                                         |
| ------------------- | ------------- | ------------------------------------------------------------- | ----------- | -------------- | --------------------------------------------- |
| Unit                | 32.1 ✅, 32.2 | Unit tests for Zone local repo & `CreatableCombobox` UI logic | Per substep | `flutter test` | 17 tests written and passing for 32.1         |
| Integration / UI    | 32.3          | Widget tests for `ZonePicker` and integration tests           | Per substep | `flutter test` | Ensure dynamic addition triggers state update |

## Open questions

- **Q1:** Should newly created zones be immediately synced to Supabase (if online), or simply added to the standard SyncQueue to be pushed during the next batch sync?
  - **Decision:** Simply add to standard SyncQueue (per ADR-0004).
- **Q2:** Is UUIDv4 acceptable for locally generating the `id` of newly created zones in the field?
  - **Decision:** Yes, UUIDv4 is acceptable.

## Ground rules

- **Calibrate communication from root `.throughstone/local-user.md`.**
- **Plan interactively.**
- **Tests ship with the code.**
- **Code is documented as it's written.**
- **Accepted risks stay visible.**

## Definition of done

- [x] Substep 32.1 complete.
- [x] Substep 32.2 complete.
- [x] Substep 32.3 complete.
- [x] The STEP test plan is complete: each code-changing substep either added/updated its relevant tests or records why tests were not applicable.
- [x] All tests named in the STEP test plan pass at the end of this STEP (`flutter test`).
- [x] STEP review passed; prompts/STEP-index.md updated; STEP archived to prompts/.
