# mine-flow — STEP-46 PLAN: Comprehensive UI/UX Audit — All Current Screens

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Hermes (Claude Opus 5 Thinking)
**Status:** Done
**Branch:** `step-0046-ui-ux-audit` (in `mine-flow-app`; no docs-hub branch needed unless remediation updates 07-ui-design-system.md)
**Repos touched:** `mine-flow-app`, `prompts` (finding register); `mine-flow-docs` (risks.yml if new risks are created)

---

## Context

The 15 Phase 2 screens were rebuilt in STEP-13–27 and received a cross-screen consistency audit in STEP-28. Since then, STEP-30–43 added new screens (Settings, Benchmark, Attendance Form, GroupLandingPage), reworked every form, migrated to ForUI Zinc, regrouped navigation, and upgraded the entire dependency chain. **No comprehensive audit has swept the full current screen surface since STEP-28.**

This STEP runs a **broad-coverage-first, narrow-verification-second** discovery pass over every screen currently routed in `lib/app/router.dart`, scoped against:
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (v0.3.0) — ForUI Zinc tokens, Geist typography, compact spacing, WCAG 2.1 AA, Indonesian l10n scaffold.
- `Code/mine-flow-docs/overview.md` — stated capabilities and the three user roles (supervisor, foreman, crew).

---

## STEP-45 Fold-in Decision (explicit)

**This is a new STEP (STEP-46), not folded into STEP-45.**

| Factor | Rationale |
|--------|-----------|
| STEP-45 depends on staging | STEP-45 executes journeys against the staging Supabase environment; STEP-42 must complete first. This audit runs against the local dev build — no staging dependency. |
| Different audit moment | STEP-46 = pre-staging static code + screenshot pass. STEP-45 = post-staging runtime device pass. |
| Different toolchain | STEP-46: code reading + Flutter-run Chrome screenshots. STEP-45: physical Android device + Chrome browser against staging. |
| Complementary output | STEP-46's confirmed finding register feeds directly into STEP-45 as the explicit "verify these on device/staging" list, narrowing STEP-45's runtime scope rather than duplicating it. |

---

## Sequencing & Overlap

STEP-42 is In progress (substeps 42.4–42.7 still Planned). It touches `mine-flow-app` (CI, seed.sql) and `mine-flow-docs` (runbooks, ADR). STEP-46 touches presentation-layer Dart files only — the overlap is on different files. Both work on separate branches. ACTION before merging STEP-46: rebase `step-0046-ui-ux-audit` cleanly onto master after STEP-42 closes.

STEP-44 (security baseline, Planned) does not overlap with presentation-layer UI work — no conflict.

STEP-46 can start immediately, in parallel with STEP-42's remaining substeps.

---

## Screen Inventory (24 screens in scope)

All screens currently routed in `lib/app/router.dart`. Route constants from `AppRoutes`.

| ID  | File (relative to `lib/`)                                                            | Route                          | Group      |
|-----|--------------------------------------------------------------------------------------|--------------------------------|------------|
| S01 | `features/auth/presentation/pages/login_page.dart`                                  | `/login`                       | Auth       |
| S02 | `app/presentation/pages/dashboard_page.dart`                                         | `/`                            | Shell      |
| S03 | `app/presentation/pages/group_landing_page.dart`                                     | `/tools`, `/operations`, `/teams` | Shell   |
| S04 | `features/settings/presentation/pages/settings_page.dart`                           | `/settings`                    | Shell      |
| S05 | `features/attendance/presentation/pages/attendance_screen.dart`                      | `/teams/attendance`            | Teams      |
| S06 | `features/attendance/presentation/pages/attendance_form_page.dart`                  | `/teams/attendance/form`       | Teams      |
| S07 | `features/daily_log/presentation/pages/daily_log_list_screen.dart`                  | `/teams/daily-log`             | Teams      |
| S08 | `features/daily_log/presentation/pages/daily_log_form_screen.dart`                  | (pushed from S07)              | Teams      |
| S09 | `features/tracking/presentation/pages/cut_fill_list_screen.dart`                    | `/operations/cut-fill`         | Operations |
| S10 | `features/tracking/presentation/pages/cut_fill_form_screen.dart`                    | (pushed from S09)              | Operations |
| S11 | `features/tracking/presentation/pages/land_clearing_list_screen.dart`               | `/operations/land-clearing`    | Operations |
| S12 | `features/tracking/presentation/pages/land_clearing_entry_screen.dart`              | (pushed from S11)              | Operations |
| S13 | `features/tracking/presentation/pages/inventory_dashboard_screen.dart`              | `/teams/inventory`             | Teams      |
| S14 | `features/tracking/presentation/pages/inventory_item_entry_screen.dart`             | (pushed from S13)              | Teams      |
| S15 | `features/equipment_check/presentation/pages/equipment_history_screen.dart`         | `/teams/equipment-check`       | Teams      |
| S16 | `features/equipment_check/presentation/pages/equipment_check_form_screen.dart`      | `/teams/equipment-check/form`  | Teams      |
| S17 | `features/benchmark/presentation/pages/benchmark_list_screen.dart`                  | `/operations/benchmark-db`     | Operations |
| S18 | `features/benchmark/presentation/pages/benchmark_form_screen.dart`                  | `/operations/benchmark-db/form`| Operations |
| S19 | `features/timeline/presentation/pages/timeline_page.dart`                           | `/teams/timeline`              | Teams      |
| S20 | `features/data_bucket/presentation/pages/data_bucket_list_page.dart`               | `/tools/data-bucket`           | Tools      |
| S21 | `features/data_bucket/presentation/pages/upload_file_page.dart`                    | `/tools/data-bucket/upload`    | Tools      |
| S22 | `features/data_bucket/presentation/pages/file_detail_page.dart`                    | `/tools/data-bucket/:id`       | Tools      |
| S23 | `features/reporting/presentation/pages/report_config_page.dart`                     | `/reports/config`              | Reports    |
| S24 | `features/notifications/presentation/pages/notification_list_page.dart`            | `/notifications`               | Notifs     |

---

## Substep Table

| Substep | Title                                             | Model                        | Status  |
|---------|---------------------------------------------------|------------------------------|---------|
| 46.1    | Pass 1a — Code-level static scan (all 24 screens) | Flash-tier (Gemini Flash)    | Planned |
| 46.2    | Pass 1b — Screenshot visual review (all 24 screens) | Pro-tier + vision (Gemini Pro) | Planned |
| 46.3    | Pass 2 — Strong-model confirmation & finding register | Claude Sonnet 4.6 Thinking | Planned |
| 46.4    | Remediation implementation                        | DeepSeek V4 Pro              | Planned |

46.1 and 46.2 are independent of each other (run concurrently or sequentially).
46.3 requires both 46.1 and 46.2 to be complete.
46.4 requires 46.3 to be complete.

---

## Decisions Locked

1. Full surface: all 24 screens in scope (not just the original 15 from Phase 2).
2. Screenshot mechanism: `flutter run -d chrome`, manual capture per screen from browser.
3. Remediation scope: all confirmed P1, P2, and P3 findings fixed in 46.4. Nothing deferred to STEP-45 from remediation unless it genuinely requires live staging/device runtime evidence.
4. Every code change in 46.4 has an accompanying test or a documented reason why one is infeasible. No silent untested fixes.

---

## Test Tier Assignments (Test Strategy Doc 12 + METHOD.md §5)

| Finding category                               | Test tier(s)                                                                    |
|------------------------------------------------|---------------------------------------------------------------------------------|
| Hardcoded data / data binding mismatch (P1)    | Widget test — pump widget with mocked BLoC state; assert displayed value matches state field, not a literal |
| Layout overflow / missing Expanded/Flexible (P2) | Widget test with ConstrainedBox at 360dp (narrow mobile) and 1280dp (desktop) |
| Raw color / raw TextStyle not using FTheme (P2–P3) | `flutter analyze` clean pass (no raw Color constructors via lint); widget test if analyzer cannot catch it |
| Navigation dead-end / missing route guard (P1) | Widget test asserting correct page is pushed; or integration test if multi-screen |
| i18n hardcoded string (P1–P2)                  | Existing `check_l10n_coverage.dart` static guard + widget test asserting locale-switched text |

---

## Definition of Done

All of the following must be true to close STEP-46:

- [ ] 46.1 raw findings list committed to `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.1-FINDINGS.md`
- [ ] 46.2 visual finding notes committed to `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.2-FINDINGS.md`
- [ ] 46.3 curated confirmed/rejected register committed to `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`
- [ ] All confirmed P1 + P2 + P3 findings implemented in 46.4 on branch `step-0046-ui-ux-audit`
- [ ] Every code change in 46.4 has a test (widget / integration / static guard) or a documented reason
- [ ] `flutter analyze` exits 0, zero issues
- [ ] `flutter test` exits 0, all tests pass, count >= 434 (current baseline as of STEP-43.9)
- [ ] "Needs runtime check" items listed explicitly in 46.3 register and referenced in STEP-45 scope note
- [ ] `registries/risks.yml` updated if any new risk or accepted debt is created
- [ ] STEP-46 index row flipped to Done; STEP archived to `prompts/003-release-readiness-integration-scale/step-0046/`

---

## Ground Rules

- Read `Code/mine-flow-docs/AGENTS.md` and `Code/mine-flow-docs/METHOD.md` before working.
- Branch `step-0046-ui-ux-audit` in `mine-flow-app` and `prompts`. Same branch name in both repos.
- Edit only your own STEP-index rows — do not re-sort or reflow the shared table.
- No silent scope changes. If a screen outside the 24-screen inventory warrants attention, note it in the finding register and flag it explicitly.
- Windows PowerShell: use `& "C:\Program Files\Git\bin\sh.exe" .\script.sh` for .sh scripts. Drive changes need `D:` then `cd D:\path`.

---

## Version Log

| Version | Date       | Change       |
|---------|------------|--------------|
| v0.1    | 2026-08-26 | Initial plan |
