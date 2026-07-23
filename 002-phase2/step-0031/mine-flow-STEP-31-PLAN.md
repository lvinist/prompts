# mine-flow — STEP-31 PLAN: Navigation Shell & Profile Regrouping

**Phase:** Phase 2 Tier 2
**Owner:** Antigravity
**Status:** In progress
**Date:** 2026-07-22
**Branch:** `step-0031-navigation-shell`
**Repos (projection):** `mine-flow-app`

> This STEP introduces a persistent, responsive navigation shell replacing the generic dashboard grid. It implements a collapsible sidebar on desktop and a bottom navigation bar with a collapsible menu on mobile, while rigorously adhering to the exact feature groupings previously specified.

## Motivation
The current grid-tile DashboardPage was a temporary MVP shell. A modern application requires a persistent shell (using `go_router`'s `StatefulShellRoute`) so users can seamlessly switch between domains (Dashboard, Tools, Operations, Teams, Settings) without losing navigation context. This also provides a dedicated space for global actions like the Theme Toggle and User Profile.

## Decisions already locked
- root `.throughstone/local-user.md` — read **Experience level** before user-facing questions or explanations, and read **Communication style** before planning discussions.
- `registries/risks.yml` — review relevant accepted risks/debt before planning work that touches their area.
- The Test Strategy architecture doc (`architecture/12-test-strategy.md`) — use it to decide which test tiers this STEP must add or update and which command or CI gate proves the STEP is done.
- ADR-0007 / Architecture 07-doc v0.2.0 — Use ForUI components (`forui` package) and tokens exclusively. No raw Material widgets or ThemeData.
- **Feature Groupings**: Must exactly follow the specific configuration:
  1. **Dashboard**
  2. **Tools**: Geospatial Data Bucket (Maps and Slope Calculator in later phases)
  3. **Operations**: Cut/fill volume tracking, Land Clearing area tracking, Benchmark Database
  4. **Teams**: Crew Attendance, Digital Equipment Check, Daily Log, Inventory
  5. **Settings**
- **Mobile Pattern**: Must use ForUI bottom navbar (`FBottomNavigationBar`) and a collapsible menu icon (not a traditional hamburger icon).

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 31.1 | Shell Routing & Scaffolding | `lib/app/router.dart` (StatefulShellRoute), `lib/app/presentation/pages/app_shell.dart` | | |
| 31.2 | Navigation Shell UI (Desktop & Mobile) | Responsive Sidebar / Bottom Navbar, Profile Card, Theme Toggle | 31.1 | |
| 31.3 | Dashboard Cleanup & Regrouping Wiring | Removal/update of `dashboard_page.dart`, wiring the 5 exact groupings | 31.2 | |
| 31.4 | Test Suite Verification & Fixes | Updated router tests, widget tests for Shell | 31.3 | |
| 31.5 | Global App Header (Shadcn Style) | Update `app_shell.dart` to add a global header for Desktop and Mobile (search, theme toggle, avatar) | 31.4 | |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Unit / Widget | 31.4 | Test `AppShell` responsive rendering, Profile/Theme toggle actions | Final verification | `flutter test` | Ensure `go_router` shell routes pass |
| Integration | 31.4 | Integration of bottom nav tabs | Final verification | `flutter test` | |

## Open questions

*(None - Scopes resolved via user feedback)*

## Ground rules
- **Calibrate communication from root `.throughstone/local-user.md`.** 
- **Tests ship with the code.** 
- **Code is documented as it's written.**
- **Accepted risks stay visible.**

## Definition of done
- [x] `StatefulShellRoute` correctly manages persistent navigation state.
- [x] Desktop uses ForUI sidebar/equivalent; Mobile uses ForUI bottom navbar + collapsible menu icon.
- [x] Theme toggle and profile moved to global shell.
- [x] The exact 5 navigation groupings are respected.
- [x] Substep 31.5: Global app header implemented correctly for Desktop and Mobile.
- [x] The STEP test plan is complete.
- [x] All tests named in the STEP test plan pass at the end of this STEP (`flutter test`).
- [x] STEP review passed; prompts/STEP-index.md updated; STEP archived to prompts/.
