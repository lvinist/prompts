# mine-flow — STEP-42.7: Runbooks, ADR, Doc Updates & STEP Close

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-42.7-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.

## Context

All infrastructure and pipeline work is complete (substeps 42.1–42.6). This final substep writes the permanent documentation: two runbooks, ADR-0011, Doc 08/09 v0.2.0 updates, RISK-0005 in the risk register, then closes STEP-42 cleanly: merge to trunk, flip index to Done, archive the plan.

**Known state (as of completion of 42.2–42.6):**
- `supabase/config.toml` committed; staging seeded and verified.
- `lib/core/data/models/generated/database.dart` committed; contract guard hardened.
- All `STAGING_*` secrets set; CI `test` job green.
- `deploy-staging` live; staging URL confirmed in browser.
- `deploy-production` wired; production manual gate verified.
- `supabase/seed.sql` patched; all feature tables populated.
- Both repos on `step-0042-staging-pipeline`.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-docs/architecture/08-infrastructure-deployment.md` ← bump to v0.2.0
- `Code/mine-flow-docs/architecture/09-environments.md` ← bump to v0.2.0
- `Code/mine-flow-docs/adr/README.md` ← next ADR = ADR-0011 (max is ADR-0010)
- `Code/mine-flow-docs/templates/adr-template.md`
- `Code/mine-flow-docs/registries/risks.yml`
- `prompts/STEP-index.md`

## Scope

**Own:** Write `staging-provision.md`, `release-procedure.md`, `ADR-0011`, update Doc 08/09, add RISK-0005, update `adr/README.md`. Then run final verification, merge to trunk, flip index to Done, archive plan.

**Do not:** Change any application code. Re-run CI or seeds (already done in earlier substeps). Add new features or alter existing runbooks (except adding the two new ones).

## Your task

### 1. Write `Code/mine-flow-docs/runbooks/staging-provision.md`

Write a step-by-step runbook that documents exactly what was done in substeps 42.1–42.3, so a future developer (or agent) can reproduce the staging environment from scratch. Include:

- **Prerequisites:** Supabase CLI version, Flutter version, Git access.
- **Step 1 — Supabase CLI install** (scoop / .msi).
- **Step 2 — Link to staging project** (`supabase link`; where to find the Project Reference ID).
- **Step 3 — Apply migrations** (`supabase db push`; idempotent note).
- **Step 4 — Seed data** (`supabase db seed`).
- **Step 5 — Generate Dart types** (`supabase gen types dart`; where to commit).
- **Step 6 — GCP staging service account** (Cloud Console steps; Drive API enable; JSON key download; Drive folder share).
- **Step 7 — GitHub Secrets** (table of all 5 `STAGING_*` secrets and where each value comes from).
- **Step 8 — GitHub Actions environments** (how to create `staging` and `production` in Settings; required reviewer on `production`).
- **Rollback procedures:**
  - Web: re-run the last passing `deploy-staging` workflow run in GitHub Actions.
  - Android APK: download the `staging-apk-<sha>` artifact from the last passing run.
  - Production: re-publish the previous GitHub Release tag (triggers re-deploy).

### 2. Write `Code/mine-flow-docs/runbooks/release-procedure.md`

Write the promotion checklist (Staging → Production). Format as a numbered checklist:

1. Confirm staging web URL loads; login with `supervisor@mineflow.dev` succeeds.
2. Install staging APK from the latest `staging-apk-<sha>` CI artifact on a test device or emulator; smoke-test: login → attendance entry → data sync attempt.
3. Run `flutter test` on `master` — must be 434+ tests, 0 failures.
4. Run `flutter analyze` — must be 0 issues.
5. Create a GitHub Release: tag format `v<MAJOR>.<MINOR>.<PATCH>` (semver). Mark as **latest** (not pre-release). Write brief release notes.
6. In GitHub Actions: find the triggered `deploy-production` run → **Review deployments** → approve.
7. Verify production web URL loads correctly post-deploy.
8. Verify the release APK asset is attached to the GitHub Release.
9. **Rollback if production breaks:** go to GitHub Releases → re-publish the previous release tag. This triggers `deploy-production` again with the previous build. Approve the gate.

### 3. Write `Code/mine-flow-docs/adr/ADR-0011-staging-promotion-pipeline.md`

Use `Code/mine-flow-docs/templates/adr-template.md` as the base. Fill in:

- **Status:** Accepted
- **Date:** 2026-08-09
- **Context:** The project reached Phase 3 and needed a real, reproducible staging environment and a deliberate production promotion gate. Three key decisions were made simultaneously.
- **Decision 1:** Use GitHub Actions **environments** (`staging`, `production`) rather than branch-per-environment for the Pages deployment. Reason: keeps branch topology simple; environment-level approval gates are native to GitHub Actions; no extra branch management overhead.
- **Decision 2:** Use **ClickOps + a runbook** (not Terraform) for Supabase staging provisioning. Reason: per Doc 08 §3 ("ClickOps + Database as Code"), the infrastructure footprint is too small to justify IaC. The runbook provides reproducibility without toolchain complexity.
- **Decision 3:** Use a **fully separate GCP service account** for staging (not shared with production). Reason: credential isolation — a staging leak cannot affect production Drive data; separate accounts also make access auditing straightforward.
- **Alternatives considered:** branch-per-environment (rejected: complex topology, no native approval gate); Terraform (rejected: overkill for 3 managed services); shared GCP service account with separate folder (rejected: no credential isolation, harder to audit).
- **Consequences:** Staging provisioning is ClickOps-only; runbook is the recovery path if the project is reprovisioned. Tracked as RISK-0005.

Add ADR-0011 row to `Code/mine-flow-docs/adr/README.md`:
```
| ADR-0011 | Staging Promotion Pipeline | Accepted | 2026-08-09 |
```

### 4. Update Doc 09 — Environments to v0.2.0

In `Code/mine-flow-docs/architecture/09-environments.md`:
- Bump Version to v0.2.0, Last updated to 2026-08-09 (STEP-42.7), Status to Active.
- Update §4 Promotion Flow:
  - "Local to Staging": push/merge to `master` triggers `deploy-staging` CI job automatically.
  - "Staging to Production": publishing a GitHub Release triggers `deploy-production` CI job with a required reviewer approval gate.
- Add §5 Rollback Procedures (summarise from runbook: web rerun, APK artifact, release tag re-publish).
- Update Version Log with v0.2.0 entry.

### 5. Update Doc 08 — Infrastructure & Deployment to v0.2.0

In `Code/mine-flow-docs/architecture/08-infrastructure-deployment.md`:
- Bump Version to v0.2.0, Last updated to 2026-08-09 (STEP-42.7).
- Update §2 Build & Deploy Pipeline:
  - On push to `master`: `test` → `build-android` → `deploy-staging` (Flutter Web to `gh-pages-staging`; debug APK artifact 14-day retention).
  - On GitHub Release publish: `deploy-production` (requires reviewer approval; Flutter Web release to `gh-pages`; signed APK attached to release).
- Update Version Log.

### 6. Add RISK-0005 to `registries/risks.yml`

```yaml
  - id: RISK-0005
    status: open
    title: "Staging Supabase project provisioned via ClickOps only"
    category: operations
    severity: low
    owner: "TBD"
    opened: "2026-08-09"
    source: "runbooks/staging-provision.md"
    description: "Staging Supabase project linked and seeded via CLI commands documented in the runbook; no IaC. If the project is deleted, manual reprovisioning is required."
    impact: "Reprovisioning requires following the runbook manually; no single-command restore."
    mitigation: "runbooks/staging-provision.md documents all steps reproducibly."
    revisit_trigger: "If staging project is deleted or must be fully reprovisioned."
    refs:
      - "runbooks/staging-provision.md"
    closed:
      date:
      reason:
```

### 7. Final verification gate

Run from `Code/mine-flow-app/`:
```bash
flutter pub get
dart format --output=none --set-exit-if-changed lib/ test/ tool/
flutter analyze
dart run tool/check_supabase_contracts.dart   # must exit 0, no bypass
dart run tool/check_l10n_baseline.dart        # must exit 0
flutter test                                  # must be 434+ tests, 0 failures
```

Record all exit codes and outputs.

### 8. Commit all doc changes

```bash
# Code/mine-flow-docs:
git add runbooks/staging-provision.md runbooks/release-procedure.md \
        adr/ADR-0011-staging-promotion-pipeline.md adr/README.md \
        architecture/08-infrastructure-deployment.md \
        architecture/09-environments.md \
        registries/risks.yml
git commit -m "docs(STEP-42.7): runbooks, ADR-0011, Doc 08/09 v0.2.0, RISK-0005"
git push
```

### 9. Merge to trunk

```bash
# mine-flow-app:
cd D:\AppDev\mine_flow\Code\mine-flow-app
git checkout master
git merge --no-ff step-0042-staging-pipeline -m "merge(STEP-42): Staging Environment & Promotion Pipeline"
git push origin master

# mine-flow-docs:
cd D:\AppDev\mine_flow\Code\mine-flow-docs
git checkout main
git merge --no-ff step-0042-staging-pipeline -m "merge(STEP-42): Staging Environment & Promotion Pipeline"
git push origin main
```

### 10. Update STEP-index and archive the plan

In `prompts/STEP-index.md`:
- Flip STEP-42 row from `In progress` to `Done`.
- Add the STEP-42 substep table (substeps 42.1–42.7, all Done).

```bash
cd D:\AppDev\mine_flow\prompts
git add STEP-index.md
git commit -m "close(STEP-42): mark Done, all substeps complete and branches merged"
git push
```

Archive the plan and substep prompts:
```powershell
New-Item -ItemType Directory -Path "D:\AppDev\mine_flow\prompts\003-release-readiness-integration-scale\step-0042" -Force
Move-Item "D:\AppDev\mine_flow\Upcoming Prompts\mine-flow-STEP-42*.md" `
          "D:\AppDev\mine_flow\prompts\003-release-readiness-integration-scale\step-0042\"
```

Commit the archive:
```bash
cd D:\AppDev\mine_flow\prompts
git add 003-release-readiness-integration-scale/step-0042/
git commit -m "archive(STEP-42): move plan and substep prompts to prompts/"
git push
```

### 11. Run `doctor.sh status`

```powershell
& "C:\Program Files\Git\bin\sh.exe" .\doctor.sh status
```

Expected output: `"no STEP In progress; next up is STEP-43 (Security, Privacy & Release-Control Baseline)."`

Record the exact output.

## Verification

- `staging-provision.md` and `release-procedure.md` exist in `Code/mine-flow-docs/runbooks/`.
- `ADR-0011-staging-promotion-pipeline.md` exists in `Code/mine-flow-docs/adr/`; `README.md` has the row.
- Doc 08 and Doc 09 show v0.2.0 in their Version Log.
- `registries/risks.yml` has RISK-0005.
- `flutter test` → 434+ tests, 0 failures; `flutter analyze` → 0 issues; `dart format` → clean.
- `dart run tool/check_supabase_contracts.dart` → exit 0, no bypass.
- Both repos merged to trunk.
- `prompts/STEP-index.md` STEP-42 = Done.
- Plan and substep prompts archived to `prompts/003-release-readiness-integration-scale/step-0042/`.
- `doctor.sh status` shows STEP-43 as next.

## Definition of done

- [ ] `runbooks/staging-provision.md` written with all ClickOps steps and rollback procedures.
- [ ] `runbooks/release-procedure.md` written with Staging → Production promotion checklist.
- [ ] `ADR-0011-staging-promotion-pipeline.md` written (Status: Accepted); `adr/README.md` row added.
- [ ] Doc 08 and Doc 09 bumped to v0.2.0 with correct pipeline descriptions.
- [ ] RISK-0005 added to `registries/risks.yml`.
- [ ] Final verification gate: all commands exit 0, 434+ tests pass.
- [ ] Both repos merged to trunk (`master` / `main`).
- [ ] `prompts/STEP-index.md` STEP-42 = Done, substep table complete.
- [ ] Plan and substep prompts archived to `prompts/003-release-readiness-integration-scale/step-0042/`.
- [ ] `doctor.sh status` shows STEP-43 as the next action.

## Next

STEP-42 is complete. Start a fresh chat for **STEP-43: Security, Privacy & Release-Control Baseline**.
