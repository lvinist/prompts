# mine-flow — STEP-41.4: Fresh Baseline Verification and Reconciliation Close

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-41.4-PROMPT.md`."**
> Run only after 41.1, 41.2, and 41.3 are all committed. This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-41 establishes a release-readiness baseline for Phase 3. Its PLAN is at `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`.

**Substeps completed before this one:**
- **41.1:** Verified repository baseline; updated draft reconciliation report.
- **41.2:** Verified `tool/check_supabase_contracts.dart` + CI gate; added `test/tool/check_supabase_contracts_test.dart`; updated README and Doc 11; live type generation remains **Unverified** (Supabase CLI not installed; STEP-42 owner).
- **41.3:** Created `l10n.yaml`, `lib/l10n/app_id.arb`, `lib/l10n/app_en.arb`; wired `AppLocalizations.delegate` into `app.dart`; created `tool/check_l10n_baseline.dart`; added `test/app/locale_configuration_test.dart` and `test/tool/check_l10n_baseline_test.dart`; updated Doc 07 and reconciliation report; added risk register row.

**Your job in 41.4 is to:**
1. Run a fresh complete validation gate and record actual results.
2. Finalize the reconciliation report with all evidence.
3. Make any remaining narrow doc/risk corrections.
4. Archive STEP-41 and close it.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`
- `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md` (updated through 41.3)
- `.throughstone/local-user.md`
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-app/.github/workflows/ci.yml`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/09-environments.md`
- `Code/mine-flow-docs/architecture/11-interface-contracts.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/registries/risks.yml`
- `prompts/STEP-index.md`

## Scope

**Own:** fresh validation results; finalized reconciliation report; STEP archive; STEP-index update to Done.

**Do not:** implement new features or fix pre-existing test failures that exist outside STEP-41 scope. Provision staging. Run remote Supabase commands. Bypass a failing test with a skip. Declare a visual review done without runtime evidence.

## Your task

### 1. Confirm worktree state

```bash
# Code/mine-flow-app:
git status --short --branch
git log --oneline -8

# Code/mine-flow-docs:
git status --short --branch
git log --oneline -5

# prompts:
git status --short --branch
```

Expected: both repos clean on `step-0041-release-readiness-baseline`. If any unexpected uncommitted changes exist, document them before proceeding.

### 2. Run the full fresh validation gate

Run each command exactly as shown, from `Code/mine-flow-app/`. Record the actual output (exit code, test count, any issues).

```bash
# Step 1 — ensure dependencies are current:
flutter pub get

# Step 2 — l10n generation (confirms ARBs → AppLocalizations):
flutter gen-l10n

# Step 3 — formatting:
dart format --output=none --set-exit-if-changed lib/ test/

# Step 4 — static analysis:
flutter analyze

# Step 5 — contract guard:
dart run tool/check_supabase_contracts.dart

# Step 6 — l10n guard:
dart run tool/check_l10n_baseline.dart

# Step 7 — full test suite:
flutter test --reporter=compact 2>&1 | tail -5
```

**Acceptance criteria:**
- Steps 1–6: exit code 0.
- Step 7: same or greater test count vs. the pre-41.3 baseline from the 41.3 report; zero new failures.

If step 4 (`flutter analyze`) reports issues introduced by STEP-41 changes (not pre-existing), fix them in this substep before closing. If it reports pre-existing issues from before STEP-41, document them and do not fix them here.

If step 7 reports failures introduced by STEP-41 changes (e.g. the new locale tests fail), fix them. If it reports pre-existing failures from before STEP-41, document them as pre-existing and do not count them as blocking.

**Build smoke gate:**
```bash
# Android debug build — requires --dart-define secrets; UNVERIFIED locally.
# Document the exact command and record as Unverified (CI job: build-android).
flutter build apk --debug \
  --dart-define=SUPABASE_URL=$STAGING_SUPABASE_URL \
  --dart-define=SUPABASE_ANON_KEY=$STAGING_SUPABASE_ANON_KEY \
  --dart-define=GOOGLE_DRIVE_CLIENT_ID=$STAGING_GOOGLE_DRIVE_CLIENT_ID \
  --dart-define=APP_ENV=staging
```

Do not run the build command with empty or fabricated values. Record it as:
> **Build smoke gate: Unverified locally** — requires staging secrets from STEP-42. CI job `build-android` will execute this on GitHub Actions once STEP-42 provisions staging credentials.

### 3. Run git diff checks

```bash
# In Code/mine-flow-app:
git diff --check

# In Code/mine-flow-docs:
git diff --check
```

Both must pass (exit 0).

### 4. Verify CI YAML consistency

Open `.github/workflows/ci.yml` and confirm the expected step order:
1. Checkout
2. Setup Flutter
3. Get dependencies (`flutter pub get`)
4. `Check Supabase Contract` (`dart run tool/check_supabase_contracts.dart`)
5. `Check Localization Baseline` (`dart run tool/check_l10n_baseline.dart`) ← added in 41.3
6. `Check formatting` (`dart format ...`)
7. `Analyze` (`flutter analyze`)
8. `Run tests` (`flutter test`)

And the `build-android` job must still exist with correct `--dart-define` calls using `secrets.STAGING_*` names.

If any step is missing or out of order, fix it in this substep.

### 5. Finalize the reconciliation report

Open `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md`.

Add a **STEP-41.4 Final Verification** section containing:

| Command | Working Dir | Exit Code | Result Summary |
|---------|-------------|-----------|----------------|
| `flutter pub get` | `Code/mine-flow-app` | 0 | Dependencies resolved |
| `flutter gen-l10n` | `Code/mine-flow-app` | 0 | AppLocalizations generated |
| `dart format --output=none ...` | `Code/mine-flow-app` | 0 | No formatting issues |
| `flutter analyze` | `Code/mine-flow-app` | 0 | 0 issues |
| `dart run tool/check_supabase_contracts.dart` | `Code/mine-flow-app` | 0 | WARNING + bypass (no generated file) |
| `dart run tool/check_l10n_baseline.dart` | `Code/mine-flow-app` | 0 | OK |
| `flutter test` | `Code/mine-flow-app` | 0 | N tests, 0 failures |
| `flutter build apk --debug ...` | `Code/mine-flow-app` | Unverified | Requires staging secrets (STEP-42) |
| `git diff --check` (app) | `Code/mine-flow-app` | 0 | Clean |
| `git diff --check` (docs) | `Code/mine-flow-docs` | 0 | Clean |

Fill in actual values for N (test count) and any actual output.

Also add the **Explicit Handoffs** section:

- **STEP-42 (Staging Environment & Promotion Pipeline):** Provision separate high-parity Supabase staging project; configure `STAGING_SUPABASE_URL`, `STAGING_SUPABASE_ANON_KEY`, `STAGING_GOOGLE_DRIVE_CLIENT_ID` as GitHub secrets; run `supabase gen types dart --project-id $SUPABASE_PROJECT_ID > lib/core/data/models/generated/database.dart` and commit the generated file; execute Android debug build smoke gate; verify staging deployment.
- **STEP-43 (Security, Privacy & Release-Control Baseline):** RLS and authorization behavior verification; account lifecycle; privacy notice/retention; secrets posture; backup and restore fire-drill.
- **STEP-44 (Release-Candidate E2E & Runtime Design Review):** Critical Android and web journey testing against staging; field-critical offline/sync behavior; runtime Impeccable responsive/accessible/localized UI review.
- **Localization full migration:** All ~35 presentation files on the `_legacyExemptFiles` list require migration to `AppLocalizations`. This must be planned as a separate user-approved STEP before a public multi-language release. See risk register RISK-XXXX.

### 6. Verify risks.yml is accurate

Open `registries/risks.yml`. Confirm the risk row added in 41.3 (localization migration) has:
- An assigned risk ID (e.g., RISK-0002 or the next available number).
- Severity, owner, revisit_trigger, and a reference to the reconciliation report.

If any field is missing, fill it in now. Do not add a risk row for the Supabase CLI absence — that is an accepted, documented deferred capability tracked in the reconciliation report and assigned to STEP-42, not a risk requiring an ongoing entry.

### 7. Mark definition of done in PLAN

Open `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`. Check off each definition-of-done item that is now satisfied:

```markdown
- [x] The contract gate (`tool/check_supabase_contracts.dart` + CI) is verified...
- [x] A minimal Flutter `l10n.yaml`, baseline ARB files, and a deterministic regression guard...
- [x] Fresh `dart format`, `flutter analyze`, `flutter test` results are recorded...
- [x] The reconciliation report is complete...
- [x] Architecture docs, CI, README, and `registries/risks.yml` match verified reality...
- [ ] STEP review passed; `prompts/STEP-index.md` updated; STEP archived to `prompts/`.
```

The last item will be checked once the archive steps below are done.

### 8. Archive STEP-41

**8a. Gather files from `Upcoming Prompts/`:**

The following files belong to STEP-41:
- `mine-flow-STEP-41-PLAN.md`
- `mine-flow-STEP-41.1-PROMPT.md`
- `mine-flow-STEP-41.2-PROMPT.md`
- `mine-flow-STEP-41.3-PROMPT.md`
- `mine-flow-STEP-41.4-PROMPT.md`

**8b. The Phase 3 folder already exists:**

The Phase 3 archive folder is `prompts/003-release-readiness-integration-scale/`. Create the STEP-41 subfolder inside it:
```
prompts/003-release-readiness-integration-scale/step-0041/
```

**8c. Copy STEP-41 files into the archive:**

Move (copy then delete from `Upcoming Prompts/`) all five STEP-41 files into `prompts/003-release-readiness-integration-scale/step-0041/`.

**8d. Update the Phase 3 README.md:**

Open `prompts/003-release-readiness-integration-scale/README.md` and add STEP-41 to the summary table.

**8e. Update `prompts/STEP-index.md`:**

Change STEP-41's status from `In progress` to `Done`:
```markdown
| STEP-41 | Release-Readiness Reconciliation & Contract Baseline | Antigravity | Done | `mine-flow-app`, `mine-flow-docs` | ... |
```

Also update the substep table to mark all four substeps Done.

**8f. Commit the prompts archive:**

```bash
# In prompts/:
git add .
git commit -m "archive(STEP-41): Release-Readiness Reconciliation & Contract Baseline"
```

### 9. Commit final changes on step branches

Commit any remaining changes to `Code/mine-flow-app` and `Code/mine-flow-docs` on `step-0041-release-readiness-baseline`:

- `Code/mine-flow-app`: updated `ci.yml` (if step order needed fixing), updated PLAN (DoD checks).
- `Code/mine-flow-docs`: finalized reconciliation report, updated risks.yml (if final edits needed).

Use commit messages like:
- `docs(STEP-41.4): finalize release-readiness reconciliation report and close STEP-41`
- `chore(STEP-41.4): update risks.yml with final localization migration risk row`

## Verification

- All validation commands in section 2 passed (recorded in report).
- CI YAML has correct step order including the l10n guard.
- Reconciliation report is final: contains actual test counts, all matrix rows updated, explicit STEPs 42/43/44 handoffs, and no unresolved Blocking findings.
- `registries/risks.yml` has the localization migration risk row with all required fields.
- STEP-41 PLAN has all DoD items checked (except the final archive item, which is checked in this substep).
- STEP-41 archived in `prompts/003-release-readiness-integration-scale/step-0041/`.
- `prompts/STEP-index.md` shows STEP-41 as `Done` and all substeps as `Done`.
- Both `Code/mine-flow-app` and `Code/mine-flow-docs` have clean worktrees.
- `Upcoming Prompts/` has no remaining STEP-41 files (moved to archive).

## Keeping the docs true

Do not edit `DESIGN.md` or `PRODUCT.md`. Do not weaken architectural requirements (Doc 07 must still say full localization is required). The reconciliation report reflects evidence gaps accurately. The archive is write-once — do not edit archived files after archiving.

## Definition of done

- [ ] Fresh validation gate passed: format ✓, analyze ✓, contract guard ✓, l10n guard ✓, full test suite ✓ — all with recorded actual results.
- [ ] Build smoke gate documented as Unverified with STEP-42 as the owner.
- [ ] Reconciliation report finalized: all matrix rows updated, actual test counts, explicit STEP-42/43/44 handoffs, no fabricated results.
- [ ] `registries/risks.yml` localization risk row has all required fields.
- [ ] STEP-41 archived to `prompts/003-release-readiness/step-0041/`; `Upcoming Prompts/` is clean.
- [ ] `prompts/STEP-index.md` shows STEP-41 and all substeps as `Done`.
- [ ] Both repo worktrees are clean.

## Next

If — and only if — all definition-of-done criteria are met, start a fresh chat and begin **STEP-42: Staging Environment & Promotion Pipeline** (the next `Planned` STEP in `prompts/STEP-index.md`).

If any criteria are not met, state the exact Blocking finding and wait for the user's decision before proceeding.
