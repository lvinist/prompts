# mine-flow — STEP-35 PLAN: Settings Page Feature

**Phase:** Phase 2 Tier 2
**Owner:** Antigravity
**Status:** Planned
**Date:** 2026-07-24
**Branch:** `step-0035-settings-page`
**Repos (projection):** `mine-flow-app`

> Implement comprehensive Settings page including language (English/Indonesian), profile, theme configuration, logout, and support contact routing using ForUI/shadcn-admin style.

## Motivation

The app currently lacks a centralized location for users to configure their experience, toggle app-wide themes, switch locales, and access support or logout functionality. This STEP brings those features together in a polished UI that adheres to the Phase 2 design language.

## Decisions already locked

- root `.throughstone/local-user.md` — read **Experience level** before user-facing questions or explanations, and read **Communication style** before planning discussions; keep that file as the personal local source of truth for both values.
- `registries/risks.yml` — review relevant accepted risks/debt before planning work that touches their area.
- The Test Strategy architecture doc (`architecture/12-test-strategy.md`) — use it to decide which test tiers this STEP must add or update.
- Phase 2 UI rebuild (`architecture/07-ui-design-system.md` v0.2.0) explicitly mandates the use of `forui` and its design tokens (e.g., `FTheme.zinc`).
- Preferences (Theme, Language) will be persisted locally using `Hive` to maintain consistency with the existing offline caching mechanism.
- Supported languages are English (default) and Indonesian (`id`).
- Support contact routing will link to `alvin.geomatics@gmail.com` and `wa.me/+6285156042854`.

## Substeps

| #    | Title                                 | Produces                                 | Depends on | Open questions |
| ---- | ------------------------------------- | ---------------------------------------- | ---------- | -------------- |
| 35.1 | Domain & Data Layer for Settings      | `SettingsRepository`, `Hive` integration | none       | none           |
| 35.2 | State Management & App Wiring         | `SettingsBloc`, `app.dart` listeners     | 35.1       | none           |
| 35.3 | Settings Page UI Shell & Integrations | `SettingsPage`, router entry             | 35.2       | none           |
| 35.4 | Verification & Polish                 | Unit tests, analyzer fixes               | 35.3       | none           |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update                            | Run timing         | Command / gate                                     | Notes |
| ------------------- | ---------- | ---------------------------------------------------- | ------------------ | -------------------------------------------------- | ----- |
| Unit                | 35.1, 35.2 | `SettingsRepositoryImpl` tests, `SettingsBloc` tests | Final verification | `flutter test test/features/settings`              |       |
| UI / Widget         | 35.3       | `SettingsPage` widget test for basic rendering       | Final verification | `flutter test test/features/settings/presentation` |       |
| Lint / Analyzer     | All        | Ensure no analyzer issues                            | Final verification | `flutter analyze`                                  |       |

## Ground rules

- **Calibrate communication from root `.throughstone/local-user.md`.** Substep prompts should read the recorded **Experience level** and adjust explanations/questions accordingly.
- **Tests ship with the code.** Every substep that writes or changes code also writes or updates the relevant tests for it. Tests are batched to the final verification substep (35.4).
- **Code is documented as it's written.** Every class, function, and method gets a docstring; comment the _why_ of non-obvious logic.
- **Accepted risks stay visible.** If this STEP accepts a risk or defers tech debt, add or update `registries/risks.yml`.

## Definition of done

- [x] Substep 35.1 completed (Domain/Data logic for Settings). [Evidence: lib/features/settings/domain/repositories/settings_repository.dart:L1-L26; lib/features/settings/domain/entities/settings_entity.dart:L1-L32; lib/features/settings/data/repositories/settings_repository_impl.dart:L1-L76; lib/features/settings/data/datasources/settings_local_datasource.dart:L1-L68]
- [x] Substep 35.2 completed (SettingsBloc and wiring). [Evidence: lib/features/settings/presentation/bloc/settings_cubit.dart:L1-L66; lib/app/app.dart:L28-L77]
- [x] Substep 35.3 completed (UI & router). [Evidence: lib/features/settings/presentation/pages/settings_page.dart:L1-L443; lib/app/router.dart:L70,L369-L380]
- [x] The STEP test plan is complete: tests added in 35.4. [Evidence: test/features/settings/data/repositories/settings_repository_impl_test.dart:L1-L104; test/features/settings/presentation/settings_cubit_test.dart:L1-L128; test/features/settings/presentation/settings_page_test.dart:L1-L105]
- [x] All tests named in the STEP test plan pass at the end of this STEP. [Evidence: flutter test test/features/settings (13 passed, 0 failed)]
- [x] Analyzer passes cleanly. [Evidence: flutter analyze lib/features/settings test/features/settings lib/app/app.dart lib/app/router.dart (No issues found)]
- [x] STEP review passed; prompts/STEP-index.md updated; STEP archived to prompts/. [Evidence: prompts/STEP-index.md:L272 (STEP-35 status Done)]

