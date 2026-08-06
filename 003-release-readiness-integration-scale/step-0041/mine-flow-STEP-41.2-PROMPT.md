# mine-flow — STEP-41.2: Verify and Document Supabase Contract Gate

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-41.2-PROMPT.md`."**
> Run only after 41.1 has committed the updated report. This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-41 establishes a release-readiness baseline. Its PLAN is at `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`.

A prior session implemented two artifacts:
- **`Code/mine-flow-app/tool/check_supabase_contracts.dart`** — a Dart script that detects when migrations are modified without a corresponding update to the generated-types artifact. It gracefully skips with a WARNING when the artifact does not yet exist (expected until STEP-42 provisions a non-production Supabase project).
- **`.github/workflows/ci.yml`** — already has a `Check Supabase Contract` step calling the script, running before `flutter analyze`.

**Your job in 41.2 is to:**
1. Verify the existing implementation is correct, well-documented, and does what its comments claim.
2. Write a focused Dart test that proves both the passing and failing conditions deterministically.
3. Update `architecture/11-interface-contracts.md` if the actual artifact location or CI behavior differs from what the doc states.
4. Update the reconciliation report with verified evidence.

**You are not implementing a new contract gate — you are verifying and testing the one that exists.**

**Known facts (from 41.1):**
- `tool/check_supabase_contracts.dart` exists; passing condition (no generated file → WARNING + exit 0) and failing condition (staged migration + generated file present → exit 1) have been verified manually.
- Generated file path: `lib/core/data/models/generated/database.dart` (does not exist yet).
- Supabase CLI not installed locally — live `supabase gen types dart` is **Unverified** until STEP-42.
- Flutter 3.44.5 / Dart 3.12.2.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`
- `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md` (updated by 41.1)
- `.throughstone/local-user.md`
- `Code/mine-flow-app/tool/check_supabase_contracts.dart`
- `Code/mine-flow-app/.github/workflows/ci.yml`
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-docs/architecture/11-interface-contracts.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/architecture/06-security-threat-model.md`
- `Code/mine-flow-docs/registries/risks.yml`

## Scope

**Own:** Code review of the existing contract guard; a focused test file for the guard; README update with regeneration instructions; Doc 11 update if the artifact location/workflow diverges from what it states; reconciliation report update.

**Do not:** Rewrite the guard from scratch. Run remote Supabase commands. Read `.env`. Add new packages. Change CI gates that already exist and work. Modify the generated-types file or create a fake one.

## Your task

### 1. Confirm worktree and read the 41.1 report

```bash
# Confirm clean state:
git status --short --branch   # (in Code/mine-flow-app)
git status --short --branch   # (in Code/mine-flow-docs)
```

Read the updated reconciliation report from 41.1. Confirm the contract guard rows show the results from the 41.1 failing-condition test.

### 2. Review the existing implementation

Read `tool/check_supabase_contracts.dart` in full and verify:

- **Correct target path:** The script checks for `lib/core/data/models/generated/database.dart`. Verify this path is consistent with `architecture/11-interface-contracts.md`. If the doc specifies a different location, document the discrepancy — do not silently accept either without evidence.
- **Regeneration command accuracy:** The printed command is `supabase gen types dart --project-id $SUPABASE_PROJECT_ID > lib/core/data/models/generated/database.dart`. Verify this matches the Supabase CLI flag for generating Dart types (the flag is `--project-id`, not `--project-ref` for older CLI versions). Document whichever flag matches the Supabase CLI version that will be used in STEP-42.
- **Local check logic:** When the generated file is absent, the tool exits 0 (bootstrap mode). When the file is present and a migration is staged but the generated file is unchanged/absent from staged: exits 1. This is correct — confirm by re-reading the code, not by re-running the test.
- **CI check logic:** In GitHub Actions, the tool diffs against `GITHUB_BASE_REF` (for PRs) or `HEAD^` (for pushes). Verify the logic handles the edge case where `GITHUB_BASE_REF` is empty (push to non-PR branch) correctly — it falls back to `HEAD^`. Note whether an initial push to a brand-new branch with only 1 commit would fail `HEAD^` (shallow clone scenario) and document it if so.
- **Docstrings:** Every function/block should have a comment explaining what it does and why. The current file uses `// ignore_for_file: avoid_print`. Verify this suppression is intentional (the file is a CLI tool, not library code).

### 3. Write a focused test for the guard

Create `Code/mine-flow-app/test/tool/check_supabase_contracts_test.dart`.

> **Important:** The guard is a Dart script (`void main()`), not a library. You cannot import it directly. Instead, test its behavior by running it as a subprocess using `dart run`. Use `dart:io`'s `Process.run` / `Process.runSync` in the test.

The test must:

1. **Passing condition (no generated file):** Run `dart run tool/check_supabase_contracts.dart` from the repo root. Assert exit code is 0. Assert stdout contains `[WARNING] Bootstrap Action Required`. Assert stdout does NOT contain `[ERROR]`.

2. **Failing condition (generated file present + uncommitted migration):** This requires temporarily creating the generated file and a temp migration. Use `Directory.systemTemp` for temp files to avoid polluting the worktree:
   - Write a dummy generated file to `lib/core/data/models/generated/database.dart`.
   - Create `supabase/migrations/99999999_temp.sql` and stage it with `git add`.
   - Run `dart run tool/check_supabase_contracts.dart`. Assert exit code is 1. Assert stdout contains `[ERROR]`.
   - Clean up: remove both temp files, run `git restore --staged supabase/migrations/99999999_temp.sql`, confirm `git status --porcelain` is clean.
   - Use `try/finally` in the test to ensure cleanup even if the assertion fails.

3. **Passing condition (generated file present + no migration change):** Write the dummy generated file, do NOT stage any migration, run the tool, assert exit code is 0 and stdout contains `[OK] Contract verification passed.`. Clean up the dummy file.

Add the standard docstring to the test file explaining its purpose, that it runs as a subprocess, and that it requires a clean git worktree.

### 4. Update README with contract regeneration instructions

Open `Code/mine-flow-app/README.md`. Find or create a **Contract Regeneration** section (place it near the existing Supabase/setup section). It must document:

```markdown
## Contract Regeneration

The generated Supabase type file at `lib/core/data/models/generated/database.dart`
must be regenerated whenever you modify the schema in `supabase/migrations/`.

**Prerequisites:**
- Supabase CLI installed: `brew install supabase/tap/supabase` (or see https://supabase.com/docs/guides/cli)
- A non-production project provisioned (see STEP-42 for staging setup)

**Command:**
```bash
supabase gen types dart --project-id $SUPABASE_PROJECT_ID \
  > lib/core/data/models/generated/database.dart
```

Set `SUPABASE_PROJECT_ID` to your non-production project's ID (never production).
Commit the regenerated file in the same commit as the migration.

**CI gate:** `dart run tool/check_supabase_contracts.dart` fails the build if
migrations change without a corresponding update to the generated file.
```

Do not add any actual values, URLs, keys, or project IDs.

### 5. Verify architecture Doc 11

Open `Code/mine-flow-docs/architecture/11-interface-contracts.md`.

Check whether it mentions:
- The generated Dart types file location (`lib/core/data/models/generated/database.dart`).
- The `supabase gen types dart` command.
- The requirement to commit the generated file with the migration.

If these are missing or the file location differs from what the guard uses, update the relevant section. Add a version log entry: `v1.x → STEP-41: Documented generated-type artifact path and CI enforcement gate.` Use the existing version log format.

If Doc 11 already accurately describes this, record "no change needed" in the report.

### 6. Update the reconciliation report

Update `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md`:

- Add a **41.2 Verification** section with:
  - Result of the code review (implementation notes, any issues found or confirmed-correct).
  - Focused test file created: `test/tool/check_supabase_contracts_test.dart` — pass/fail results.
  - README update: yes/no + section added.
  - Doc 11 update: yes/no + what changed or why unchanged.
  - Update the contract gate matrix row status to **Verified** (the guard itself is confirmed working with tests).
  - Live type generation status: **Unverified** — Supabase CLI not installed locally; STEP-42 owner must provision a non-production project and run `supabase gen types dart`.

### 7. Run verification commands

```bash
# From Code/mine-flow-app:
flutter pub get
dart format --output=none --set-exit-if-changed lib/ test/
flutter analyze
flutter test test/tool/check_supabase_contracts_test.dart
git diff --check
```

```bash
# From Code/mine-flow-docs:
git diff --check
```

Record actual results (exit codes, test counts, any analyzer issues). If any command fails, fix the issue before marking 41.2 done.

### 8. Commit

Commit all changes on `step-0041-release-readiness-baseline`:
- `Code/mine-flow-app`: test file, README update (if changed).
- `Code/mine-flow-docs`: Doc 11 update (if changed), reconciliation report update.

Use a commit message like: `test(STEP-41.2): verify Supabase contract guard and add focused tests`.

## Verification

- `flutter test test/tool/check_supabase_contracts_test.dart` passes all 3 tests.
- `flutter analyze` reports 0 issues.
- `dart format` reports 0 formatting changes needed.
- `git diff --check` passes in both repos.
- Worktrees are clean (no temp files, no staged changes) after the test run.
- Reconciliation report contract section shows **Verified** for the guard and **Unverified** for live generation, with explicit STEP-42 ownership.

## Keeping the docs true

Doc 11 covers Interface Contracts. If the generated-type artifact location or CI gate are now concrete and were previously undocumented or incorrect, updating Doc 11 is the right action — bump the version log. If updating Doc 11 would represent a material change in contract policy (not just making an undocumented workflow explicit), write an ADR first.

Do not edit `DESIGN.md`, `PRODUCT.md`, or historical archived STEP artifacts.

## Definition of done

- [ ] Existing `tool/check_supabase_contracts.dart` implementation is confirmed correct (or issues are documented).
- [ ] `test/tool/check_supabase_contracts_test.dart` passes: 3 tests (passing, failing, passing-with-file conditions).
- [ ] Worktree is clean after test run (no temp files, no staged artifacts).
- [ ] `README.md` has a Contract Regeneration section with accurate non-secret instructions.
- [ ] Doc 11 reflects the actual artifact path and CI gate, version log updated.
- [ ] Reconciliation report updated: guard **Verified**, live generation **Unverified** with STEP-42 owner.
- [ ] `flutter analyze` and `dart format` pass; `git diff --check` clean in both repos.
- [ ] Changes committed on `step-0041-release-readiness-baseline`.

## Next

After committing, start a fresh chat and run **substep 41.3**: `Upcoming Prompts/mine-flow-STEP-41.3-PROMPT.md`.
