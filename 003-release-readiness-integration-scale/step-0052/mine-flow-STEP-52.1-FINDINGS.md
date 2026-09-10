# mine-flow — STEP-52.1 FINDINGS: Security Baseline Surface Audit & Risk Adjudication

**Substep:** 52.1
**Date:** 2026-09-10
**Status:** Complete (all audits executed, findings derived from code and configuration evidence)
**Branch:** `step-0052-security-baseline-recheck` (all repos)
**Author:** Antigravity

---

## 1. Executive Summary & Review Scope

This audit re-evaluates the project's S0 Security Baseline post-STEP-48. The original baseline established in STEP-44
(2026-08-26, commit `5536191`) was invalidated by subsequent major changes to CI, runtime infrastructure, and database schema:
1. **STEP-45 dual-platform E2E gate:** Headless Chrome/chromedriver, Android emulator runner, `e2e-web` and `e2e-android` workflows.
2. **STEP-47 build chain modernization:** Android AGP 9, Kotlin 2.4, JDK 17 temurin, AGP-9 native plugins.
3. **STEP-48 staging & runtime surface:** Staging credentials (`TEST_USER_*`, `TEST_SUPERVISOR_*`, `TEST_FOREMAN_*`), Google Drive service account integration, staging database fixtures, and two new Supabase tables (`timeline_milestones` and `benchmarks`).

### Change Markers

| Marker | STEP-44 Baseline (2026-08-26) | STEP-52 Re-check (2026-09-10) | Delta / Notes |
|---|---|---|---|
| Reviewed App Commit | `5536191` | `6fbce5e` | +75 commits across STEPs 45–51 |
| Elapsed Time | First S0 | 15 days (~2 weeks) | Cadence rule triggered |
| Rough SLOC (`lib/`) | ~11,000 Dart LOC | ~14,000 Dart LOC | +~3,000 LOC from new features & test helpers |
| Supabase Tables with RLS | 9 tables | 11 tables | +2 tables (`timeline_milestones`, `benchmarks`) |
| CI E2E Surface | None (unit/widget only) | Dual-platform (Web + Android emulator) | Added in STEP-45/48 |
| Active Risks Tracked | RISK-0011..0013 | RISK-0011..0013, RISK-0021 | RISK-0021 added in STEP-48.12 |

---

## 2. RLS Audit Across All 11 Supabase Tables

All database migration files under `Code/mine-flow-app/supabase/migrations/` were audited for table definition,
RLS activation (`ENABLE ROW LEVEL SECURITY`), and role-based policies across `supervisor`, `foreman`, and `crew`.

| # | Table Name | Migration File | RLS Enabled | Policies Defined | Isolation / Security Posture |
|---|---|---|:---:|---|---|
| 1 | `public.users` | `20260718000002_rls_policies.sql` | YES | `supervisor_users_all` (ALL to supervisor); `users_read_active` (SELECT to foreman/crew for active); `users_update_self` (UPDATE own row) | **AUDIT FINDING (FINDING-52.1-01 — Privilege Escalation):** Role resolution uses `public.current_user_role()` (`SECURITY DEFINER`, search_path fixed). However, `users_update_self` (`USING (id = auth.uid()) WITH CHECK (id = auth.uid())`) lacks column restrictions or an update trigger. Any authenticated non-supervisor (foreman or crew) can issue `UPDATE public.users SET role = 'supervisor' WHERE id = auth.uid()`, escalating their role to supervisor and immediately inheriting full permissions across all 11 tables. Remediation required via trigger guard (`prevent_user_role_escalation`) or column-level permissions prior to production release. |
| 2 | `public.zones` | `20260718000002_rls_policies.sql` | YES | `supervisor_zones_all` (ALL to supervisor); `zones_read_active` (SELECT to foreman/crew) | **Verified.** Foremen and crew have read-only access to active zones (`deleted_at IS NULL`). Writes strictly refused. |
| 3 | `public.attendance_records` | `20260718000002_rls_policies.sql` | YES | `supervisor_attendance_all` (ALL to supervisor); `foreman_attendance_*` (SELECT/INSERT/UPDATE for site); `crew_attendance_*` (SELECT/INSERT own row) | **Verified.** Crew members can only SELECT and INSERT rows where `user_id = auth.uid()`. Cross-crew data leakage is impossible at SQL level. |
| 4 | `public.equipment_checks` | `20260718000002_rls_policies.sql` | YES | `supervisor_equipment_all` (ALL to supervisor); `foreman_equipment_*` (SELECT/INSERT/UPDATE); `crew_equipment_select` (SELECT active) | **Verified.** Foreman manages checks; crew has read-only access. Zero crew write privileges. |
| 5 | `public.daily_logs` | `20260718000002_rls_policies.sql`<br>`20260902000001_step_48_21_notes_columns.sql` | YES | `supervisor_daily_logs_all` (ALL to supervisor); `foreman_daily_logs_*` (SELECT/INSERT/UPDATE); `crew_daily_logs_select` (SELECT where `status = 'approved'`) | **Verified.** Strict read filtering: crew can ONLY see approved logs (`status = 'approved' AND deleted_at IS NULL`). Drafts and unapproved logs are completely hidden from crew. |
| 6 | `public.cut_fill_records` | `20260718000002_rls_policies.sql`<br>`20260723_step_33_1_data_model_polish.sql` | YES | `supervisor_cut_fill_all` (ALL to supervisor); `foreman_cut_fill_*` (SELECT/INSERT/UPDATE); `crew_cut_fill_select` (SELECT active) | **Verified.** Foreman manages records; crew has read-only access. Only supervisor can delete. |
| 7 | `public.land_clearing_records` | `20260718000002_rls_policies.sql`<br>`20260723_step_33_1_data_model_polish.sql` | YES | `supervisor_land_clearing_all` (ALL to supervisor); `foreman_land_clearing_*` (SELECT/INSERT/UPDATE); `crew_land_clearing_select` (SELECT active) | **Verified.** Foreman manages records; crew has read-only access. |
| 8 | `public.inventory_items` | `20260718000002_rls_policies.sql`<br>`20260723_step_33_1_data_model_polish.sql` | YES | `supervisor_inventory_all` (ALL to supervisor); `foreman_inventory_*` (SELECT/INSERT/UPDATE); `crew_inventory_select` (SELECT active) | **Verified.** Foreman manages records; crew has read-only access. |
| 9 | `public.geospatial_files` | `20260718000002_rls_policies.sql`<br>`20260718000003_data_bucket_enhancements.sql`<br>`20260724_step_34_1_drop_geospatial_file_lat_lon.sql` | YES | `supervisor_geospatial_all` (ALL to supervisor); `foreman_geospatial_insert` (INSERT to foreman); `foremen_crew_geospatial_select` (SELECT active) | **Verified.** Foremen can upload metadata; foremen and crew can read active metadata; only supervisors can update/delete. |
| 10 | `public.timeline_milestones` | `20260831000001_step_48_17_timeline_milestones.sql` | YES | `supervisor_timeline_milestones_all` (ALL to supervisor); `foreman_timeline_milestones_*` (SELECT/INSERT/UPDATE); `crew_timeline_milestones_select` (SELECT active) | **Verified (new post-STEP-44 table).** `ENABLE ROW LEVEL SECURITY` explicit. Supervisor has full access; foreman can select/insert/update; crew has read-only access to non-deleted records; anon access denied. |
| 11 | `public.benchmarks` | `20260831000002_step_48_17_benchmarks.sql` | YES | `supervisor_benchmarks_all` (ALL to supervisor); `foreman_benchmarks_*` (SELECT/INSERT/UPDATE); `crew_benchmarks_select` (SELECT active) | **Verified (new post-STEP-44 table).** `ENABLE ROW LEVEL SECURITY` explicit. Unique constraint `(site_id, bm_id)` enforced. Supervisor has full access; foreman can select/insert/update; crew has read-only access; anon access denied. |

### RLS Summary Verdict
- **11 of 11 tables** have RLS explicitly enabled.
- **100% of policies** target `TO authenticated`. Zero public or anonymous policies exist.
- Helper function `public.current_user_role()` is configured with `SECURITY DEFINER` and hardcoded `SET search_path = public` to prevent search-path hijacking.
- Soft-delete filtering (`deleted_at IS NULL`) is consistently applied on non-supervisor SELECT policies.
- DELETE privileges are restricted exclusively to the `supervisor` role across all 11 tables.
- **VULNERABILITY IDENTIFIED (FINDING-52.1-01 — Privilege Escalation in `public.users`):** The self-update policy `users_update_self` fails to enforce column immutability on `role`, `site_id`, and `is_active`. A non-supervisor session can update their own row to `role = 'supervisor'`, instantly breaking all RLS role boundaries across the system. Must be remediated prior to production release.

---

## 3. Risk Adjudication

### RISK-0021: Partial RLS matrix and cross-role isolation unverified
- **Static Analysis:**
  - The SQL policies across operational tables (`zones`, `attendance_records`, `equipment_checks`, `daily_logs`, `cut_fill_records`, `land_clearing_records`, `inventory_items`, `geospatial_files`, `timeline_milestones`, `benchmarks`) establish proper role separation for operational data.
  - **Critical Defect (FINDING-52.1-01):** As discovered in this audit, `public.users` policy `users_update_self` lacks role immutability checks, allowing self-escalation to `supervisor`.
- **Runtime Test & CI State:**
  - `integration_test/journeys/rls_authorization_journey_test.dart` contains complete tests for supervisor, foreman, and crew roles. Supervisor and foreman legs run green in CI.
  - The crew leg was previously unwired in `.github/workflows/ci.yml` (missing `--dart-define` parameters for `TEST_CREW_*`). STEP-52.1 resolved this in commit `be44843`.
  - The crew leg now correctly passes through CI flags and skips with an honest named marker solely because `TEST_CREW_EMAIL` and `TEST_CREW_PASSWORD` are not yet provisioned in GitHub Repository Secrets.
- **Adjudication:**
  - CI harness gap resolved (`be44843`).
  - Automated CI execution of the crew leg remains an accepted test-infrastructure gap (`monitoring`) until GitHub secrets are provisioned.
  - FINDING-52.1-01 documented as a pre-release security finding for remediation.

### RISK-0011: In-app Privacy Notice absent from first-login flow
- **Audit Findings:** Scanned `lib/` for `privacy`, `privasi`, and `terms`. Zero matches found. The first-login privacy notice required by Doc 17 §3 has not yet been implemented.
- **Adjudication:** Remains **Open** (Severity: High). Must be retained as a strict pre-release gate before production release.

### RISK-0012: Supabase free-tier: no automatic daily backups; restore not fire-drilled
- **Audit Findings:** The Supabase project is on the free tier without automatic daily backups or PITR. Manual backup/restore procedure documented in STEP-44 S0 report §Backup. No live restore fire-drill has been conducted.
- **Adjudication:** Remains **Open** (Severity: High). Acceptable for pre-production development, but must be upgraded to a paid plan or scheduled backup before real production data is loaded.

### RISK-0013: S0 baseline operations cluster (branch protection, secret scanning, Dependabot, monitoring)
- **Audit Findings:**
  - `gh` CLI is not installed on the local developer environment, meaning GitHub repository settings (branch protection, secret scanning toggle, Dependabot alerts toggle) cannot be audited via API locally.
  - Third-party CI actions remain tag-pinned (`@v4`, `@v2`) rather than SHA-pinned.
  - Security monitoring is limited to Supabase Auth logs.
- **Adjudication:** Remains **Accepted Risk** (Severity: Medium) for the current MVP phase with a single active developer and small team. Revisit trigger: Before external contributors or production release.

---

## 4. CI/CD & Secrets Handling Audit

### Workflows Audited: `.github/workflows/ci.yml`
1. **Trigger Surface:** `push`, `pull_request`, and `release: [published]`. Uses standard `pull_request` (not `pull_request_target`), preventing untrusted fork PRs from accessing base repository secrets.
2. **Secrets Scope & Injection:**
   - Secrets are injected via `${{ secrets.* }}` into `--dart-define` compile-time flags or process environment variables.
   - `deploy-staging` is scoped to the `staging` environment.
   - `deploy-production` is scoped to the `production` environment with a required reviewer approval gate.
3. **Log Exposure & Artifacts:**
   - In `e2e-web`, `flutter drive` does not echo `--dart-define` parameters to `web_current.log` or `all_web.log`.
   - In `e2e-android`, `flutter test` does not echo command-line arguments to `integration_test.log`.
   - GitHub Actions runner masks all secret values with `***`.
4. **Local Configuration (.env.example) & CI Workflows:**
   - Remediation applied in commit `6fbce5e`: Added documentation for `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`, `TEST_SUPERVISOR_EMAIL`, `TEST_SUPERVISOR_PASSWORD`, `TEST_FOREMAN_EMAIL`, `TEST_FOREMAN_PASSWORD`, `TEST_CREW_EMAIL`, and `TEST_CREW_PASSWORD`.
   - Remediation applied in commit `be44843`: Wired `--dart-define=TEST_CREW_EMAIL=${{ secrets.TEST_CREW_EMAIL }}` and `--dart-define=TEST_CREW_PASSWORD=${{ secrets.TEST_CREW_PASSWORD }}` into both `e2e-web` and `e2e-android` workflows in `.github/workflows/ci.yml`.

---

## 5. S0 Baseline Decision Table (Complete 34 Rows)

| Area | Baseline Item | Status | Decision Date | Owner | Reason / Evidence | Revisit Trigger | Risk Ref |
|---|---|:---:|:---:|---|---|---|:---:|
| Setup | Read last S0 report & ledger | **Done** | 2026-09-10 | Antigravity | Read `reports/security/2026-08-26-step-0044-s0-security-baseline-report.md` (commit `5536191`); evaluated +75 commits across STEPs 45–51, +3k LOC, 2 new tables. | Next S0 review / S1 sweep | — |
| Release posture | First-release security baseline recorded | **Done** | 2026-09-10 | Team | STEP-52 re-check confirms updated security posture post-STEP-48. | Before public release | — |
| Release posture | Release runbook security pre-flight | **Done** | 2026-09-10 | Team | `runbooks/release-procedure.md`, `release-deploy.md`, `staging-provision.md`; `deploy-production` gated by manual reviewer. | After deployment changes | — |
| Ownership | Security owners identified | **Accepted Risk** | 2026-09-10 | Project Manager | Internal MVP; owner is Project Manager / Site Supervisor; no formal role separation yet. | Team growth / production handoff | RISK-0013 |
| Ownership | Access review cadence | **Deferred** | 2026-09-10 | Project Manager | Small team; reviews tied to Throughstone check-in cadence (~10–20 STEPs). | Before production with real data | — |
| Repository hygiene | Default branch protection configured | **Accepted Risk** | 2026-09-10 | Project Manager | Unverified locally (`gh` CLI not installed). Strict CI gates on all pushes. | Before external contributors | RISK-0013 |
| Repository hygiene | Required status checks configured | **Accepted Risk** | 2026-09-10 | Project Manager | CI runs on all pushes/PRs; GitHub branch protection settings unverified locally without `gh`. | Before external contributors | RISK-0013 |
| Repository hygiene | Security policy / reporting path | **N/A** | 2026-09-10 | Team | Internal enterprise mining tool; source and app not publicly distributed. | Before public source / release | — |
| Repository hygiene | OpenSSF Scorecard repo hygiene | **Deferred** | 2026-09-10 | Team | Internal MVP; automated Scorecard badge adds disproportionate overhead. | Before public launch | — |
| Repository hygiene | Release provenance recorded | **Done** | 2026-09-10 | Team | GitHub release tags trigger `deploy-production`; `softprops/action-gh-release@v2` attaches APK by SHA. | Before distributing signed APKs | — |
| CI hygiene | CI runs from reviewed repository code | **Done** | 2026-09-10 | Team | `.github/workflows/ci.yml` reviewed; uses standard `pull_request` (not `pull_request_target`). | After workflow changes | — |
| CI hygiene | CI token permissions least-privilege | **Done** | 2026-09-10 | Team | `test` and `build` jobs have no write permissions; `contents: write` scoped only to deploy jobs. | After modifying permissions | — |
| CI hygiene | Third-party CI actions controlled/pinned | **Accepted Risk** | 2026-09-10 | Team | Major-version tag pinned (`@v4`, `@v2`), not full commit SHA digest pinned. Standard for MVP. | Before regulated/audit use | RISK-0013 |
| CI hygiene | CI secrets exposed only to trusted jobs | **Done** | 2026-09-10 | Team | Staging and Production environments segregated; production requires manual approval. | After CI environment changes | — |
| CI hygiene | Build/test workflows cover release branches | **Done** | 2026-09-10 | Team | Required CI gates include execution guards (`check_e2e_executed.dart`, contract & l10n guards); fail closed. | Before adding release branches | — |
| Secrets handling | Secrets stored in CI/secret manager | **Done** | 2026-09-10 | Team | Stored in GitHub Secrets; `.env` gitignored; zero hardcoded secrets in repository files. | After adding integrations | — |
| Secrets handling | Secret scanning enabled | **Accepted Risk** | 2026-09-10 | Team | GitHub push protection / secret scanning unverified locally (no `gh` CLI). Git history clean. | Before production release | RISK-0013 |
| Secrets handling | Suspected secret exposure response path | **Done** | 2026-09-10 | Team | `runbooks/secrets-rotation.md` covers Supabase keys, Google Drive credentials, and GitHub PATs. | After adding secret classes | — |
| Secrets handling | Local dev uses ignored files & templates | **Done** | 2026-09-10 | Antigravity | `.gitignore` covers `.env`; `.env.example` updated with E2E test runner credentials (`6fbce5e`). | After adding config keys | — |
| Dependency alerts | Vulnerability alerting enabled | **Accepted Risk** | 2026-09-10 | Team | Dependabot status unverified locally. Regular review during Throughstone check-ins. | Before production release | RISK-0013 |
| Dependency alerts | Dependency update policy exists | **Done** | 2026-09-10 | Team | `runbooks/dependency-supply-chain.md` exists; dependency checks at check-in cadence (~10–20 STEPs). | After major SDK upgrades | — |
| Dependency alerts | Lockfiles committed & checked | **Done** | 2026-09-10 | Team | `pubspec.lock` committed and verified by `flutter pub get` in CI. | After adding package managers | — |
| Dependency alerts | License compatibility review planned | **N/A** | 2026-09-10 | Team | Internal tool; no external redistribution. All packages use permissive licenses (MIT/BSD/Apache). | Before commercial redistribution | — |
| Static analysis | Security linting / SAST configured | **Done** | 2026-09-10 | Team | `flutter analyze` with `flutter_lints`, plus contract and l10n custom guards in CI. | After Flutter SDK upgrades | — |
| Static analysis | Findings triaged & clean | **Done** | 2026-09-10 | Team | `flutter analyze` reports 0 issues globally; CI enforces zero errors/warnings. | Each S1 sweep / check-in | — |
| Artifacts | Container / image scanning | **N/A** | 2026-09-10 | Team | No Docker/container images; static Web on GitHub Pages and Android APK directly from Gradle. | If containers introduced | — |
| Artifacts | Release artifacts reproducible & traceable | **Done** | 2026-09-10 | Team | Built from tagged release commit with pinned Flutter `3.47.1` and committed lockfile; APK traceable to SHA. | After pipeline changes | — |
| Infrastructure | IaC / cloud config scanning | **N/A** | 2026-09-10 | Team | No IaC (Terraform/Pulumi). Supabase managed via SQL migrations and ClickOps. | If IaC is introduced | RISK-0010 |
| Infrastructure | Production environments access controlled | **Accepted Risk** | 2026-09-10 | Team | Staging separated from Production. RLS enabled on 11/11 tables. FINDING-52.1-01 identified that `users_update_self` permits role escalation if not guarded; tracked for remediation before production. | Before production release | FINDING-52.1-01 / Doc 06 |
| SBOM | SBOM generation | **Deferred** | 2026-09-10 | Team | Internal MVP; no customer or regulatory distribution requirement. | Before enterprise distribution | — |
| Monitoring | Security operational signals identified | **Accepted Risk** | 2026-09-10 | Team | Supabase Auth logs capture login failures. No custom alerting/SIEM dashboard configured for MVP. | Before production use | RISK-0013 |
| Incident readiness | Incident response entry point documented | **Done** | 2026-09-10 | Team | `runbooks/incident-postmortem.md` defines RCA, patch, and postmortem workflow. Owner: Project Manager. | Before production use | — |
| Backup/recovery | Backup, restore, rollback assumptions | **Accepted Risk** | 2026-09-10 | Team | Supabase free-tier (no automated backups/PITR). Manual CLI procedure documented; no fire-drill yet. | Before production data load | RISK-0012 |
| Data handling | Sensitive data classes & controls reflected | **Done** | 2026-09-10 | Team | Doc 06 (Threat Model) and Doc 17 (Privacy) identify NIK, DOB, emergency contacts, and geospatial data. | When data scope changes | RISK-0011 |

---

## 6. Handoff to Substep 52.2

Substep 52.1 is complete. Deliverables produced:
1. `Upcoming Prompts/mine-flow-STEP-52-PLAN.md` authored.
2. `Upcoming Prompts/mine-flow-STEP-52.1-PROMPT.md` and `52.2-PROMPT.md` authored.
3. `Code/mine-flow-app/.env.example` updated with E2E test runner credentials (`commit 6fbce5e`).
4. `Code/mine-flow-app/.github/workflows/ci.yml` wired with `TEST_CREW_EMAIL` and `TEST_CREW_PASSWORD` in `e2e-web` and `e2e-android` (`commit be44843`).
5. Full 11-table RLS audit completed; FINDING-52.1-01 (privilege escalation in `users_update_self`) identified and recorded for pre-release remediation.
6. Outstanding risks RISK-0011..0013 and RISK-0021 adjudicated with concrete evidence.
7. All 34 rows of the S0 checklist evaluated.
8. This FINDINGS document published.

**Next Action:** Run **substep 52.2** (S0 report finalization, registry & doc updates, verification gate & close).
