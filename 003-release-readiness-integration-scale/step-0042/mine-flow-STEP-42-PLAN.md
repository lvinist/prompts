# mine-flow — STEP-42 PLAN: Staging Environment & Promotion Pipeline

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Gemini 3.1 Pro High
**Status:** In progress (42.1–42.3 done; 2026-08-25 audit fixed 42.2 — see Amendment below)
**Date:** 2026-08-09
**Amendment (2026-08-25):** The earlier "Deferred → STEP-46 / superseded by STEP-46" header
was stale — execution resumed on this STEP after the STEP-43 rebase (43.11); no STEP-46 exists.
A 2026-08-25 verification audit found the committed `database.dart` was a hand-written stub
(Dart typegen has been removed from the Supabase CLI; supabase/cli#6230 to restore it is an
unmerged draft). Per owner decision, Option 1 was adopted: the contract artifact is now real
`supabase gen types --lang typescript` output committed at `supabase/types/database.ts`, the
stub was deleted, and `tool/check_supabase_contracts.dart` gained stub-rejection content checks.
Remote evidence: all 5 migrations confirmed applied on staging (`supabase migration list --linked`);
all five `STAGING_*` GitHub Secrets confirmed set by the project owner.
**Branch:** `step-0042-staging-pipeline` (to be renamed `step-0046-staging-pipeline` on start)
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts` (completion archive only)

> Provision and wire the staging environment (already-provisioned Supabase project, separate GCP service account, GitHub Secrets), expand the CI pipeline to deploy staging on `main`/`master` push and production on Release with a manual gate, audit and patch seed data, commit the generated Dart types, harden the contract guard, and document rollback and release procedures. Verify staging on Android and web delivery paths. No application feature code changes.

---

## Background

STEP-41 established the release-readiness baseline: CI guards for contract staleness and
localization regressions, a minimal l10n scaffold, and an evidence-backed reconciliation
report. It explicitly made **no remote changes** and handed the following to STEP-42:

- Provision a separate Supabase project for staging (A1: already exists — skip creation).
- Generate and commit `lib/core/data/models/generated/database.dart` via `supabase gen types dart`.
- Set all `STAGING_*` GitHub Secrets.
- Wire `deploy-staging` and `deploy-production` GitHub Actions jobs.
- Remove the `WARNING + bypass` bootstrap exemption from `tool/check_supabase_contracts.dart`.
- Audit `supabase/seed.sql` for schema additions since STEP-3 (STEP-33, STEP-36, STEP-38).
- Write `runbooks/staging-provision.md` and `runbooks/release-procedure.md`.
- Bump Doc 08 and Doc 09 to v0.2.0; write ADR-0011; add RISK-0005.

---

## Decisions locked (pre-answered by project owner)

- **Staging Supabase project:** Already exists. Skip dashboard creation. Start at `supabase link`.
- **GitHub Pages staging slot:** Use GitHub Actions **environments** (`staging`, `production`). No branch-per-environment.
- **Google Drive for staging:** A **fully separate GCP service account** is used for staging. Create a new service account in Google Cloud Console, scoped only to the staging Drive folder. Secrets are distinct from any production equivalents.
- **`supabase/config.toml`:** Missing (STEP-41 gap). Created via `supabase link` in substep 42.1.

---

## Current repository state (as of 2026-08-09)

- **`Code/mine-flow-app`**: on `master` (STEP-41 merged). 434 tests, 0 failures. `flutter analyze` clean. `check_supabase_contracts.dart` exits `WARNING + bypass` (no `database.dart` yet). `check_l10n_baseline.dart` exits 0.
- **`Code/mine-flow-docs`**: on `main` (STEP-41 merged). All docs current.
- **`prompts`**: STEP-41 = Done. STEP-42 = Planned → flip to In progress on branch cut.
- **Supabase CLI**: Not in PATH locally (STEP-41 blocker). Must be installed before substep 42.1.
- **GitHub Secrets**: `STAGING_SUPABASE_URL`, `STAGING_SUPABASE_ANON_KEY`, `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL`, `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY`, `STAGING_GOOGLE_DRIVE_FOLDER_ID` — **not yet set**.
- **`supabase/migrations/`**: 5 SQL files (last: `20260723_step_34_1_drop_geospatial_file_lat_lon.sql`).
- **`supabase/seed.sql`**: Missing rows for benchmark (STEP-36), BCM/LCM/material_type (STEP-33), clearing_method (STEP-33), second attendance record (STEP-38).

---

## Scope boundaries

### In scope
1. Install Supabase CLI; link existing staging project; apply migrations; run seed; generate and commit Dart types.
2. Create staging GCP service account; set all `STAGING_*` GitHub Secrets.
3. Expand `.github/workflows/ci.yml` with `deploy-staging` and `deploy-production` jobs.
4. Remove the bootstrap bypass from `tool/check_supabase_contracts.dart`.
5. Patch `supabase/seed.sql` for schema additions since STEP-3.
6. Write `runbooks/staging-provision.md` and `runbooks/release-procedure.md`.
7. Bump Doc 08 and Doc 09 to v0.2.0; write ADR-0011; add RISK-0005; update `.env.example`.

### Explicitly out of scope
- Any application feature code changes.
- Security posture verification, RLS/auth auditing, backup fire-drill (STEP-43).
- Full E2E journeys, runtime design review (STEP-44).
- Full Indonesian localization migration (RISK-0004, separate future STEP).
- Creating a production Supabase project (production uses existing project per architecture).

---

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 42.1 | Supabase CLI install, link & migrations | `supabase/config.toml` committed; migrations applied; seed loaded; staging URL confirmed reachable | Supabase CLI installed | None — staging project already exists |
| 42.2 | Generated types commit & contract guard hardening | `lib/core/data/models/generated/database.dart` committed; `tool/check_supabase_contracts.dart` bypass removed; CI passes full contract check | 42.1 complete | None |
| 42.3 | Staging GCP service account & GitHub Secrets | New GCP staging service account created; all `STAGING_*` secrets set in GitHub repo; CI test job confirmed green | 42.1 complete | None |
| 42.4 | `deploy-staging` CI job | `deploy-staging` job in `ci.yml`; Flutter Web builds and deploys to staging Pages slot on `master` push; staging URL confirmed reachable in browser | 42.3 complete | None |
| 42.5 | `deploy-production` job & manual gate | `deploy-production` job in `ci.yml`; `production` GitHub environment created with required reviewer; dry-run tag confirms gate blocks without approval | 42.4 complete | None |
| 42.6 | Seed data audit & patch | `supabase/seed.sql` patched for STEP-33/36/38 schema additions; `supabase db seed` re-run on staging; all 8 feature tables confirmed populated in dashboard | 42.1 complete | None |
| 42.7 | Runbooks, ADR, doc updates & STEP close | `staging-provision.md`, `release-procedure.md`, ADR-0011, Doc 08/09 v0.2.0, RISK-0005, `.env.example`; STEP-index.md Done; plan archived | 42.2–42.6 complete | None |

---

## Detailed substep specs

### Substep 42.1 — Supabase CLI install, link & migrations

**Deliverables:**
- Supabase CLI installed and verified (`supabase --version`).
- `supabase link --project-ref <STAGING_PROJECT_REF>` run from `Code/mine-flow-app/` — generates `supabase/config.toml`.
- `supabase/config.toml` committed.
- `supabase db push` run — applies all 5 migrations (idempotent; safe if already applied).
- `supabase db seed --file supabase/seed.sql` run — synthetic data loaded.
- Staging Project URL confirmed reachable.

**Windows notes:**
- Install via `scoop install supabase` or the official `.msi` from https://supabase.com/docs/guides/local-development/cli/getting-started.
- All `supabase` commands must be run from inside `Code/mine-flow-app/`.
- Staging Project Reference ID: Supabase Dashboard → Project Settings → General → Reference ID.

---

### Substep 42.2 — Generated types commit & contract guard hardening

**Deliverables:**
- `supabase gen types dart --project-id <STAGING_PROJECT_REF> > lib/core/data/models/generated/database.dart` run.
- `lib/core/data/models/generated/database.dart` committed (non-empty).
- `tool/check_supabase_contracts.dart`: remove the bootstrap bypass block (the `[WARNING] Bootstrap Action Required` path that calls `exit(0)`). Absence of the file must be a hard failure (exit 1).
- `dart run tool/check_supabase_contracts.dart` exits 0 — **no bypass message**, full pass.
- `flutter test` still 434+ tests, 0 failures. `flutter analyze` still clean.

---

### Substep 42.3 — Staging GCP service account & GitHub Secrets

**Deliverables (ClickOps — document steps taken in `staging-provision.md`):**
- New GCP service account created: Google Cloud Console → IAM → Service Accounts.
- Google Drive API enabled for the GCP project (if not already).
- Service account JSON key downloaded; `client_email` and `private_key` extracted.
- A staging Google Drive folder created; service account email granted Editor access.
- GitHub Secrets set (repo Settings → Secrets and variables → Actions):
  - `STAGING_SUPABASE_URL`
  - `STAGING_SUPABASE_ANON_KEY`
  - `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL`
  - `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY`
  - `STAGING_GOOGLE_DRIVE_FOLDER_ID`
- CI `test` job confirmed green on push.

---

### Substep 42.4 — `deploy-staging` CI job

**New job skeleton for `.github/workflows/ci.yml`:**

```yaml
deploy-staging:
  name: Deploy to Staging
  runs-on: ubuntu-latest
  needs: build-android
  if: github.ref == 'refs/heads/master'
  environment:
    name: staging
    url: ${{ steps.deploy.outputs.page_url }}
  steps:
    - uses: actions/checkout@v4
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: "3.47.0"
        channel: stable
        cache: true
    - run: flutter pub get
    - name: Build Flutter Web (staging)
      run: |
        flutter build web --release \
          --dart-define=SUPABASE_URL=${{ secrets.STAGING_SUPABASE_URL }} \
          --dart-define=SUPABASE_ANON_KEY=${{ secrets.STAGING_SUPABASE_ANON_KEY }} \
          --dart-define=GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL=${{ secrets.STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL }} \
          --dart-define=GOOGLE_DRIVE_FOLDER_ID=${{ secrets.STAGING_GOOGLE_DRIVE_FOLDER_ID }} \
          --dart-define=APP_ENV=staging
    - name: Deploy to GitHub Pages (staging)
      id: deploy
      uses: peaceiris/actions-gh-pages@v4
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: build/web
        destination_dir: staging
        publish_branch: gh-pages-staging
    - name: Upload staging APK artifact
      uses: actions/upload-artifact@v4
      with:
        name: staging-apk-${{ github.sha }}
        path: build/app/outputs/flutter-apk/app-debug.apk
        retention-days: 14
```

**Verification:** push to `master`; staging URL loads in browser; login with `supervisor@mineflow.dev` succeeds.

---

### Substep 42.5 — `deploy-production` job & manual gate

**New job skeleton for `.github/workflows/ci.yml`:**

```yaml
deploy-production:
  name: Deploy to Production
  runs-on: ubuntu-latest
  if: github.event_name == 'release' && github.event.action == 'published'
  environment:
    name: production
    url: https://<org>.github.io/<repo>/
  steps:
    - uses: actions/checkout@v4
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: "3.47.0"
        channel: stable
        cache: true
    - run: flutter pub get
    - name: Build Flutter Web (production)
      run: |
        flutter build web --release \
          --dart-define=SUPABASE_URL=${{ secrets.PROD_SUPABASE_URL }} \
          --dart-define=SUPABASE_ANON_KEY=${{ secrets.PROD_SUPABASE_ANON_KEY }} \
          --dart-define=GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL=${{ secrets.PROD_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL }} \
          --dart-define=GOOGLE_DRIVE_FOLDER_ID=${{ secrets.PROD_GOOGLE_DRIVE_FOLDER_ID }} \
          --dart-define=APP_ENV=production
    - name: Deploy to GitHub Pages (production)
      uses: peaceiris/actions-gh-pages@v4
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: build/web
        publish_branch: gh-pages
    - name: Build Android release APK
      run: |
        flutter build apk --release \
          --dart-define=SUPABASE_URL=${{ secrets.PROD_SUPABASE_URL }} \
          --dart-define=SUPABASE_ANON_KEY=${{ secrets.PROD_SUPABASE_ANON_KEY }} \
          --dart-define=GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL=${{ secrets.PROD_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL }} \
          --dart-define=GOOGLE_DRIVE_FOLDER_ID=${{ secrets.PROD_GOOGLE_DRIVE_FOLDER_ID }} \
          --dart-define=APP_ENV=production
    - name: Attach APK to GitHub Release
      uses: softprops/action-gh-release@v2
      with:
        files: build/app/outputs/flutter-apk/app-release.apk
```

**ClickOps required (document in runbook):** GitHub repo → Settings → Environments → `production` → Required reviewers → add yourself.

**Dry-run verification:** push tag `v0.0.0-test` as a pre-release; confirm `deploy-production` waits for approval; cancel without approving; delete test tag.

---

### Substep 42.6 — Seed data audit & patch

Audit `supabase/seed.sql` against current migration set. Add rows for:
- **`benchmark_records`** (STEP-36).
- **`cut_fill_records`** additional row with `material_type`, `bcm_volume`, `lcm_volume` (STEP-33).
- **`land_clearing_records`** additional row with `clearing_method` (STEP-33).
- **`attendance_records`** second row to exercise `AttendanceFormPage` (STEP-38).

After patching: `supabase db seed --file supabase/seed.sql` re-run on staging; confirm rows in Supabase dashboard for all 8 feature tables.

---

### Substep 42.7 — Runbooks, ADR, doc updates & STEP close

**New files:**

`Code/mine-flow-docs/runbooks/staging-provision.md` — step-by-step runbook:
- CLI install, `supabase link`, `db push`, `db seed`, `gen types dart`.
- GCP staging service account creation and key extraction.
- GitHub Secrets checklist.
- GitHub Actions environments ClickOps steps.
- Rollback: web (re-run last passing job), APK (download artifact / re-publish Release).

`Code/mine-flow-docs/runbooks/release-procedure.md` — promotion checklist (Staging → Production):
1. Staging web URL loads; login works with `supervisor@mineflow.dev`.
2. Staging APK from CI artifact smoke-tested on device/emulator.
3. `flutter test` green on `master`.
4. Create GitHub Release (tag: `v1.x.x`).
5. Approve `deploy-production` manual gate.
6. Verify production web URL + APK attached to release.
7. Rollback: re-publish previous release tag.

`Code/mine-flow-docs/adr/ADR-0011-staging-promotion-pipeline.md` (Status: Accepted):
- Decision: GitHub Actions environments over branch-per-environment.
- Decision: ClickOps + runbook over Terraform.
- Decision: fully separate GCP service account for staging.
- Alternatives considered; trade-offs documented.

**Modified files:**

`Code/mine-flow-docs/adr/README.md` — add ADR-0011 row.

`Code/mine-flow-docs/architecture/09-environments.md` — v0.1.0 → v0.2.0:
- §4 Promotion Flow: concrete CI job names; Status: Draft → Active.
- Add §5 Rollback Procedures.

`Code/mine-flow-docs/architecture/08-infrastructure-deployment.md` — v0.1.0 → v0.2.0:
- §2 Build & Deploy Pipeline: two-job promotion model + production manual gate.

`Code/mine-flow-docs/registries/risks.yml` — add RISK-0005 (ClickOps-only staging provisioning; low severity; runbook mitigates).

`Code/mine-flow-app/.env.example` — add `SUPABASE_PROJECT_REF=` key and `STAGING_*` comment block documenting each required CI secret.

`prompts/STEP-index.md` — flip STEP-42 to Done; add substep table.

---

## Test plan

| Surface | Substep | Gate | Notes |
|---------|---------|------|-------|
| Contract guard | 42.2 | `dart run tool/check_supabase_contracts.dart` → exit 0, no bypass | Confirms `database.dart` exists and is in sync |
| l10n guard | 42.2 | `dart run tool/check_l10n_baseline.dart` → exit 0 | Must not regress |
| Full unit/widget suite | 42.2, 42.6 | `flutter test` → 434+ tests, 0 failures | After each code change |
| Static analysis | 42.2, 42.4, 42.5 | `flutter analyze` → 0 issues | After each CI file change |
| Android debug build | 42.4 | `flutter build apk --debug` with staging secrets → exit 0 | Confirms staging secrets valid |
| Web build | 42.4 | `flutter build web --release` with staging secrets → exit 0 | Confirms web toolchain works |
| Staging URL | 42.4 | Browser: staging Pages URL loads, login works | Manual |
| Staging APK | 42.4 | Install on device/emulator; login + attendance + sync smoke | Manual |
| Supabase dashboard | 42.6 | All 8 feature tables have seeded rows | Manual spot-check |
| Production gate | 42.5 | Dry-run tag → gate blocks without reviewer approval; cancel | Manual |
| Rollback test | 42.4 | Re-run prior `deploy-staging` job; staging URL reflects that build | Manual |

---

## Ground rules

- **ClickOps steps must be documented** in `staging-provision.md` as they happen.
- **No secrets in committed files.** `config.toml` contains only the project reference ID. `.env.example` shows key names only.
- **Evidence over assertion.** Every verification result must cite the actual command, exit code, and output.
- **Dry-run the production gate** — do not publish an actual production release; test with a pre-release tag and cancel.
- **Calibrate from root `.throughstone/local-user.md`.**
- **Windows PowerShell:** switch drive with `D:` then `cd`; run `.sh` scripts via `& "C:\Program Files\Git\bin\sh.exe"`.

---

## Definition of done

- [ ] `supabase/config.toml` committed; staging migrations applied; seed loaded.
- [ ] `lib/core/data/models/generated/database.dart` committed; `check_supabase_contracts.dart` bootstrap bypass removed; CI exits 0 (full pass, no bypass).
- [ ] All `STAGING_*` GitHub Secrets set; CI `test` job passes green on push.
- [ ] `deploy-staging` job deploys Flutter Web to staging Pages slot on `master` push; staging URL confirmed in browser.
- [ ] `deploy-production` job wired with production manual approval gate; dry-run tag confirms gate blocks.
- [ ] `supabase/seed.sql` patched for STEP-33/36/38 additions; all 8 feature tables seeded in staging dashboard.
- [ ] `runbooks/staging-provision.md` and `runbooks/release-procedure.md` written.
- [ ] ADR-0011 written and Accepted; Doc 08/09 bumped to v0.2.0; RISK-0005 added; `.env.example` updated.
- [ ] `flutter test` 434+ tests, 0 failures; `flutter analyze` clean; `dart format` clean.
- [ ] STEP review passed; `prompts/STEP-index.md` updated to Done; STEP archived to `prompts/003-release-readiness-integration-scale/step-0042/`.
