# mine-flow — STEP-42.2: Generated Types Commit & Contract Guard Hardening

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-42.2-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-42.1 linked the staging Supabase project and committed `supabase/config.toml`. This substep closes the last STEP-41 handoff: generate and commit `lib/core/data/models/generated/database.dart`, then remove the bootstrap bypass from `tool/check_supabase_contracts.dart` so the contract gate becomes a real enforcement check, not a warning.

**Known state (as of completion of 42.1):**
- `supabase/config.toml` committed on `step-0042-staging-pipeline`.
- `lib/core/data/models/generated/database.dart` does **not** exist.
- `tool/check_supabase_contracts.dart` currently exits `WARNING + bypass` when the generated file is absent.
- Supabase CLI is installed (verified in 42.1).
- 434 tests passing; `flutter analyze` clean.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/tool/check_supabase_contracts.dart` ← you will edit this
- `Code/mine-flow-docs/architecture/11-interface-contracts.md`

## Scope

**Own:** Generate `database.dart` via `supabase gen types dart`; commit it; remove the bootstrap bypass from the contract guard; verify the guard now does a full enforcement pass.

**Do not:** Set GitHub Secrets (substep 42.3). Change application code. Run any migration or seed (42.1 already done).

## Your task

### 1. Confirm branch state

```bash
# In Code/mine-flow-app/:
git status --short --branch
git log --oneline -3
```

Confirm you are on `step-0042-staging-pipeline` and `supabase/config.toml` is in the log.

### 2. Generate Dart types

You need the **Project Reference ID** from `supabase/config.toml` (field `project_id`).

```bash
# From Code/mine-flow-app/:
supabase gen types dart --project-id <STAGING_PROJECT_REF> > lib/core/data/models/generated/database.dart
```

Inspect the generated file:
- Must be non-empty (> 0 bytes).
- Should contain Dart class/type definitions corresponding to the Supabase schema tables.
- Record the first ~10 lines as evidence.

### 3. Remove the bootstrap bypass from the contract guard

Open `Code/mine-flow-app/tool/check_supabase_contracts.dart`. Find the block that handles the missing generated file with a `[WARNING] Bootstrap Action Required` message and `exit(0)`. Remove that bypass path entirely.

After the change, the behaviour must be:
- **Generated file exists + no uncommitted migrations** → exit 0 (pass).
- **Generated file missing** → exit 1 (hard failure — file must now always exist).
- **Uncommitted migrations + generated file out of sync** → exit 1 (existing behaviour — unchanged).

### 4. Run the updated guard

```bash
# From Code/mine-flow-app/:
dart run tool/check_supabase_contracts.dart
```

Expected: exit 0, **no** bypass warning. Record the full output.

### 5. Run the full test suite and analyzer

```bash
flutter pub get
dart format --output=none --set-exit-if-changed lib/ test/ tool/
flutter analyze
flutter test
```

Record: exit codes + test count. Must be 434+ tests, 0 failures, 0 analyzer issues.

### 6. Commit

```bash
# From Code/mine-flow-app/:
git add lib/core/data/models/generated/database.dart tool/check_supabase_contracts.dart
git commit -m "feat(STEP-42.2): commit generated Supabase types and harden contract guard"
git push
```

## Verification

- `lib/core/data/models/generated/database.dart` exists, non-empty, committed.
- `dart run tool/check_supabase_contracts.dart` exits 0 with no bypass warning.
- No `[WARNING] Bootstrap Action Required` text appears in the guard source or output.
- `flutter test` → 434+ tests, 0 failures.
- `flutter analyze` → 0 issues.
- `dart format` → no formatting issues.

## Definition of done

- [ ] `lib/core/data/models/generated/database.dart` committed (non-empty).
- [ ] Bootstrap bypass removed from `tool/check_supabase_contracts.dart`.
- [ ] `dart run tool/check_supabase_contracts.dart` exits 0, full enforcement pass (no bypass).
- [ ] `flutter test` 434+ tests, 0 failures; `flutter analyze` clean; `dart format` clean.
- [ ] Changes committed and pushed on `step-0042-staging-pipeline`.

## Next

After committing, start a fresh chat and run **substep 42.3**: `Upcoming Prompts/mine-flow-STEP-42.3-PROMPT.md`.
