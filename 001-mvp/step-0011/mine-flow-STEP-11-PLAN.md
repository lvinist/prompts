# mine-flow — STEP-11 PLAN: Phase 1 Polish & UI Wrap-up

**Phase:** Phase 1 — MVP
**Owner:** DeepSeek        <!-- one owner for the whole STEP and all its substeps; also shown in prompts/STEP-index.md; solo: optional -->
**Status:** Planned        <!-- Planned → In progress → Done; or Deferred / Abandoned (see METHOD.md §1) -->
**Date:** 2026-07-19
**Branch:** `step-0011-ui-polish`   <!-- same name in every repo this STEP touches -->
**Repos (projection):** `mine-flow-app`, `prompts`   <!-- same label as prompts/STEP-index.md; lists repos + merge order; powers the overlap warning -->

> This STEP addresses the design and technical debt gaps found at the end of MVP Phase 1. It implements the missing `shadcn-admin` responsive layout (collapsible sidebar), adds a real dashboard summary, resolves 92 analyzer warnings, and cleans up unarchived prompt files.

## Motivation
During the STEP-10 final check-in, an audit revealed that while all core capabilities function correctly, the intended desktop/mobile responsive UI shell (`shadcn-admin` style collapsible sidebar) and dashboard stat cards were never implemented. The app uses a basic placeholder grid. Additionally, 92 non-fatal Flutter analyzer warnings remain, and several completed STEP prompt files were left unarchived in the workspace. This polish pass resolves these issues before calling Phase 1 complete.

## Decisions already locked
- root `.throughstone/local-user.md` — read **Experience level** before user-facing questions or explanations, and read **Communication style** before planning discussions; keep that file as the personal local source of truth for both values.
- `registries/risks.yml` — review relevant accepted risks/debt before planning work that touches their area. (Specifically RISK-0002 for analyzer warnings).
- The Test Strategy architecture doc (`architecture/12-test-strategy.md`) — use it to decide which test tiers this STEP must add or update and which command or CI gate proves the STEP is done.
- `architecture/07-ui-design-system.md` — The design reference mandates `shadcn-admin` elements, dark/light mode, and specific spacing.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 11.1 | Responsive UI Shell & Navigation | `lib/app/router.dart`, `lib/app/presentation/` | None | How best to integrate theme toggle? |
| 11.2 | Card-based Dashboard Stats | Dashboard UI updates | 11.1 | Which exact dummy/real stats to show? |
| 11.3 | Code Quality Polish (Lint Fixes) | `lib/**/*.dart` lint fixes | None | None |
| 11.4 | Workspace Hygiene (Archive Prompts) | Moves files to `prompts/001-mvp/` | None | None |
| 11.5 | Notification Rules Implementation | Fully wired `NotificationRuleEngine` | None | None |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Unit / Widget | 11.1, 11.2 | Update existing widget tests for dashboard/router | Final verification | `flutter test` | Ensure `_DashboardPlaceholder` tests are updated for new ShellRoute |

## Open questions
- Q1 (DeepSeek): Should the dashboard use real repository calls to fetch stats (e.g. counting total attendance today) or mock stats for now?

## Ground rules
- **Calibrate communication from root `.throughstone/local-user.md`.** Substep prompts should read the recorded **Experience level** and adjust explanations/questions accordingly. 
- **Plan interactively.** Confirm scope before drafting.
- **Tests ship with the code.** Ensure `flutter test` still passes after lint fixes and UI layout changes.
- **Code is documented as it's written.**
- **Accepted risks stay visible.** Once lint warnings are fixed, close RISK-0002 in `registries/risks.yml`.

## Definition of done
- [ ] Responsive `ShellRoute` is implemented (sidebar for wide screens, bottom nav for narrow).
- [ ] Dashboard features actual statistic summary cards matching `shadcn-admin` aesthetics.
- [ ] Dark/light mode toggle is accessible in the UI.
- [ ] 0 analyzer warnings remain (`flutter analyze` is clean).
- [ ] Loose files in `Upcoming Prompts/` from STEPs 7, 8, 9 are archived to their respective folders in `prompts/001-mvp/`.
- [ ] Notification rules 2, 3, and 4 are fully implemented and connected to repositories.
- [ ] The STEP test plan is complete.
- [ ] `flutter test` passes cleanly.
- [ ] STEP review passed; `prompts/STEP-index.md` updated; STEP archived to `prompts/`.
