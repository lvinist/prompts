# mine-flow — STEP-41.1: Verify Inventory Report and Repository Baseline

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-41.1-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-41 opens Phase 3 by establishing a trustworthy release-readiness baseline. Its PLAN is at `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`.

A prior session partially completed this substep: it produced a draft reconciliation report at `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md`, committed `tool/check_supabase_contracts.dart`, and updated `ci.yml`. **Your job in 41.1 is to verify the actual repository state against what the draft report claims, close any gaps in the report, and confirm the baseline is accurate before 41.2 and 41.3 proceed.** Do not recreate files that already exist.

**Known state (confirmed on 2026-08-06):**
- Both `Code/mine-flow-app` and `Code/mine-flow-docs` are on `step-0041-release-readiness-baseline` with clean worktrees.
- `tool/check_supabase_contracts.dart` exists and runs; the CI gate in `.github/workflows/ci.yml` calls it.
- `l10n.yaml` and `.arb` files are absent; `pubspec.yaml` has `generate: true` and `intl` declared.
- No `lib/core/data/models/generated/database.dart` exists (expected — Supabase CLI not installed locally).
- Supabase CLI is not installed locally.
- Flutter 3.44.5, Dart 3.12.2.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md` ← the draft to verify/complete
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-app/pubspec.yaml`
- `Code/mine-flow-app/.github/workflows/ci.yml`
- `Code/mine-flow-app/tool/check_supabase_contracts.dart`
- `Code/mine-flow-app/lib/app/app.dart`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/11-interface-contracts.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/registries/risks.yml`

## Scope

**Own:** Verify the repository state matches what the draft report claims. Identify and document any discrepancies. Confirm the baseline facts 41.2 and 41.3 will rely on. Update the draft report with any corrections.

**Do not:** Implement anything new (contracts, l10n, tests). Change CI or app code. Make remote calls. Read `.env`.

## Your task

### 1. Confirm worktree state

Run and record:
```bash
# In Code/mine-flow-app:
git status --short --branch
git log --oneline -5

# In Code/mine-flow-docs:
git status --short --branch
git log --oneline -5

# In prompts:
git status --short --branch
```

Confirm both app and docs repos are clean on `step-0041-release-readiness-baseline`. Confirm `prompts` is on `main` with STEP-41 showing `In progress` in `STEP-index.md`. If any discrepancy is found, document it as a blocker and stop.

### 2. Verify the contract tooling

Run each of these exactly as shown and record the actual output:

```bash
# From Code/mine-flow-app:
dart run tool/check_supabase_contracts.dart
```

Expected: WARNING + bypass (exit 0) because the generated file does not exist.

Then verify the CI integration:
- Open `.github/workflows/ci.yml` and confirm the `Check Supabase Contract` step calls `dart run tool/check_supabase_contracts.dart`.
- Confirm the step runs **before** `flutter analyze`.
- Confirm no secrets are used in this step.

Record: "Verified", "Partially evidenced", or "Unverified" with the evidence.

### 3. Verify the localization baseline

Run and record:
```bash
# From Code/mine-flow-app:
find . -name 'l10n.yaml' -o -name '*.arb' 2>/dev/null
```

Expected: no output (no files found).

Then verify:
- Open `pubspec.yaml` and confirm `generate: true` is present under `flutter:`.
- Open `lib/app/app.dart` and confirm `supportedLocales`, `localizationsDelegates` configuration.
- Confirm `AppLocalizations` is **not** imported anywhere (hardcoded strings only).

Record the localization classification: **locale selection** (locale switching works via SettingsCubit, but no ARB-based string routing exists).

### 4. Run the contract check tool's failing-condition test

To verify the tool correctly detects a stale contract, create a temporary migration file and run the tool, then immediately remove the temp file:

```bash
# From Code/mine-flow-app:
# 1. Create a temp migration to simulate a new schema change:
echo "-- temp test migration" > supabase/migrations/99999999_temp_test.sql

# 2. Stage it so git status shows it as modified:
git add supabase/migrations/99999999_temp_test.sql

# 3. Run the tool — should still exit 0 (WARNING bypass) because generated file doesn't exist:
dart run tool/check_supabase_contracts.dart

# 4. Create a dummy generated file:
mkdir -p lib/core/data/models/generated
echo "// dummy" > lib/core/data/models/generated/database.dart

# 5. Run again — the tool should now EXIT 1 because migration is staged but generated file is:
#    a) uncommitted (staged mig + unstaged/untracked generated file)
dart run tool/check_supabase_contracts.dart

# 6. Clean up every temp artifact:
git restore --staged supabase/migrations/99999999_temp_test.sql
rm supabase/migrations/99999999_temp_test.sql
rm lib/core/data/models/generated/database.dart
rmdir lib/core/data/models/generated 2>/dev/null || true
```

Record the exit codes and stdout from steps 3 and 5. This proves the guard has both a passing and a failing path. Verify the cleanup leaves the worktree clean (`git status --porcelain` is empty after cleanup).

### 5. Update the draft report

Open `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md` and:

- Update **Inspected Revisions** to reflect the actual current branch/revision (both repos on `step-0041-release-readiness-baseline`, clean worktrees).
- Update **Blockers and Assumptions** — remove the STEP-40 uncommitted changes note (worktrees are now clean). Keep the Supabase CLI absence note.
- Update the contract staleness guard row to **Verified** (the guard works — you just ran the passing and failing conditions and confirmed CI integration).
- Add a row confirming the failing-condition test result.
- Ensure the localization row accurately says **locale selection** — locale switching works via SettingsCubit but no ARB/AppLocalizations delegate exists.
- Add a **Tooling Verification** section with the actual `dart run tool/check_supabase_contracts.dart` output recorded.
- Add explicit next-substep notes: 41.2 will verify/document the contract gate; 41.3 will create `l10n.yaml`, ARBs, and the l10n guard.

Commit the updated report to `Code/mine-flow-docs` on the step branch.

## Verification

- `git status --porcelain` in `Code/mine-flow-app` is empty after cleanup.
- `git status --porcelain` in `Code/mine-flow-docs` shows only the updated report file (before commit).
- The draft report contains: actual branch names, actual tool output (with exit codes), the passing + failing guard run evidence, and explicit 41.2/41.3 handoffs.
- No secrets, `.env` content, or private URLs appear in the report.
- `git diff --check` passes in both repos.

## Keeping the docs true

This substep is verification/documentation only. Do not update architecture docs in this substep. If you discover a discrepancy between what the draft report says and what is actually in the repository, document the discrepancy accurately in the updated report — do not silently accept the prior claim.

## Definition of done

- [ ] Worktree state confirmed clean on `step-0041-release-readiness-baseline` in both repos, with recorded `git log` and `git status` output.
- [ ] Contract guard verified: passing-condition (no generated file → WARNING + exit 0) and failing-condition (staged migration + dummy generated file present → exit 1) both run and recorded.
- [ ] CI integration of `check_supabase_contracts.dart` confirmed with no secrets in that step.
- [ ] Localization state confirmed: no `l10n.yaml`, no ARB, no `AppLocalizations` delegate; `generate: true` and `intl` present; classified as **locale selection**.
- [ ] Draft report updated with corrected revisions/state, actual tool outputs, and explicit 41.2/41.3 handoffs; committed.
- [ ] Worktree is clean after all temp-file cleanup.

## Next

After committing the updated report, start a fresh chat and run **substep 41.2**: `Upcoming Prompts/mine-flow-STEP-41.2-PROMPT.md`.
