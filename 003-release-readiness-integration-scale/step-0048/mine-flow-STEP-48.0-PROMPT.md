# mine-flow — STEP-48.0: Credential & Toolchain Pre-flight Gate

> **How to run:** tell your agent *"run substep 48.0"*. A substep is self-contained — it is
> executable cold in a fresh chat with no prior conversation.

**Assigned model: Gemini 3.7 Flash High.** This substep is procedural — create accounts, set secrets,
boot the emulator, install chromedriver, run one journey, read the count. The pass/fail signal is
unambiguous, so it does not need a heavier model. **Escalate to Opus 4.8** if the proof-of-life run
fails in a way you cannot classify, or if a credential/permission problem looks like it might be an
app defect rather than a setup gap. Recording an escalation in the findings is expected, not a
failure.


## Context

STEP-48 is the STEP where mine-flow finally produces the **runtime evidence** that STEP-45
deferred. Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` before starting.

STEP-45 authored 15 `integration_test` files and a dual-platform CI gate, but **not one journey
has ever executed against a real backend**. Every one self-skips because
`integration_test/helpers/staging_config.dart` finds no credentials. STEP-47 made both CI E2E
jobs green — which proves the harness runs, and nothing else.

**This substep is a gate, not a formality.** If it cannot complete, STEP-48 must **stop and
report** rather than proceed. Authoring or "fixing" more tests that cannot run would repeat
STEP-45's failure exactly. You are the substep that makes the difference between a real STEP-48
and a second round of theatre.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the STEP PLAN, especially the "Pre-flight
  reality check" section (the facts below were established there) and the open questions Q1–Q3.
- root `.throughstone/local-user.md` — the user is **Experience level 2, Explanatory**. Explain
  what you are doing and why, in plain language. Do not assume deep tooling knowledge.
- `Code/mine-flow-docs/architecture/09-environments.md` v0.4.0 — §2 (secret storage: GitHub
  Repository Secrets), §4 (promotion flow, and the "harness only" note this STEP will rewrite).
- `Code/mine-flow-docs/architecture/12-test-strategy.md` v1.2 — the E2E tier and CI gates.
- `Code/mine-flow-app/README.md` — local host prerequisites (written in STEP-47.8).
- `Code/mine-flow-app/integration_test/helpers/staging_config.dart` — the exact gate that
  decides whether a journey runs or skips.
- `Code/mine-flow-app/.github/workflows/ci.yml` — the `e2e-web` and `e2e-android` jobs.
- `Code/mine-flow-app/supabase/seed.sql` and `supabase/migrations/20260718000002_rls_policies.sql`
  — the seed data and the three-role RLS model (`supervisor`, `foreman`, `crew`).
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0006, RISK-0011, RISK-0015…RISK-0019.

## Scope

**In scope:** proving that a real staging journey can execute. Credentials, seed data, a booted
Android emulator, a working web driver, and one observed green journey run as proof of life.

**Not in scope:** running the 14 journeys (48.3–48.12), repairing the stub/fake-green journey
files (48.1), expanding the CI job targets (48.2), Google Drive credentials of any kind
(explicitly Deferred per PLAN decision D2), touching `registries/risks.yml` (48.14), or editing
any architecture doc (48.15).

## Facts already established (verified from disk 2026-08-29 — do not re-derive, but do re-confirm)

The `lvinist/mine-flow-app` repository has exactly **five** Actions secrets:

```
STAGING_SUPABASE_URL
STAGING_SUPABASE_ANON_KEY
STAGING_GOOGLE_DRIVE_FOLDER_ID
STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL
STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY
```

`TEST_USER_EMAIL` and `TEST_USER_PASSWORD` **do not exist**. `staging_config.dart:16` requires
all four of `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `TEST_USER_EMAIL`, `TEST_USER_PASSWORD` to be
non-empty, so `isStagingConfigured` is **false on every CI run**. That single fact is why
`e2e-web` and `e2e-android` report `0 tests passed, 1 skipped` and still exit 0.

`ci.yml` also passes `secrets.STAGING_GOOGLE_DRIVE_CLIENT_ID`, which is **not in the secret
list** — it silently resolves to an empty string.

Host state: `flutter devices` shows Windows, Chrome, Edge — **no Android device attached**,
though a `Pixel_6a` AVD exists. `chromedriver` is **not on PATH**.

Re-confirm each of these at the start of your run (the secret list can be read with the GitHub
API using the PAT in Git Credential Manager: `printf 'protocol=https\nhost=github.com\n\n' | git
credential fill`, then `GET /repos/lvinist/mine-flow-app/actions/secrets` with the password as a
Bearer token). If any fact has changed, say so and adapt.

## Your task

### 1. Resolve the open questions with the user (ask, do not assume)

Ask these together, in one message, calibrated to Experience level 2 — explain the consequence
of each choice rather than just presenting the option:

- **Q1 — per-role accounts.** The staging schema defines three roles (`supervisor`, `foreman`,
  `crew`) with genuinely different RLS policies. With one shared test user, substep 48.12 can
  only prove what a single role sees, and the authorization matrix stays Deferred for a third
  time. **Recommend: create all three accounts** — it is a few minutes of work in the Supabase
  dashboard and it closes a security gate instead of deferring it again.
- **Q2 — seeding.** Several journeys assert on list contents (zones, employees, inventory items).
  Against an empty staging database they will fail for reasons that have nothing to do with the
  code, which would produce misleading findings. **Recommend: seed staging from
  `supabase/seed.sql` first** and record which revision was applied.
- **Q3 — the phantom `STAGING_GOOGLE_DRIVE_CLIENT_ID`.** It is referenced by CI but does not
  exist. **Recommend: remove that `--dart-define` line from the E2E jobs** (Drive is out of
  STEP-48's scope per D2) so no job depends on an empty value. Note the removal in your findings.

### 2. Create the staging test user(s)

The **user** does this — you cannot create Supabase accounts or set repository secrets on their
behalf without credentials you must never hold. Guide them:

1. In the staging Supabase project → Authentication → Users → add user(s) with a password.
2. In `public.users`, set each new row's `role` column to the intended role (`supervisor`,
   `foreman`, or `crew`) — the RLS policies read `public.current_user_role()`, which reads that
   column, so an auth user without a matching `public.users` row will fail every policy check.
3. Confirm each account can sign in (the Supabase dashboard can test this).

Give them the exact steps. Do not ask them to paste the password into the chat.

### 3. Set the repository secrets

Again, the **user** does this. Provide the exact commands or the settings path:

```bash
# via gh CLI, run by the user in their own terminal
gh secret set TEST_USER_EMAIL --repo lvinist/mine-flow-app
gh secret set TEST_USER_PASSWORD --repo lvinist/mine-flow-app
# only if Q1 is answered "create all three":
gh secret set TEST_FOREMAN_EMAIL --repo lvinist/mine-flow-app
gh secret set TEST_FOREMAN_PASSWORD --repo lvinist/mine-flow-app
gh secret set TEST_SUPERVISOR_EMAIL --repo lvinist/mine-flow-app
gh secret set TEST_SUPERVISOR_PASSWORD --repo lvinist/mine-flow-app
```

(Or Settings → Secrets and variables → Actions → New repository secret.)

Then **verify by name only** — re-read the secret list via the API and confirm the new names
appear. Never read, print, log, or commit a value. If the user offers to paste a password into
the chat, decline and point them at `gh secret set`, which reads from a prompt.

For **local** runs you need the same values on the host. Have the user place them in the
gitignored `Code/mine-flow-app/.env` (see `.env.example`) or export them in their own shell, and
pass them via `--dart-define` from environment variables — never inline a literal into a command
you write into a file or a log.

### 4. Seed staging (if Q2 is yes)

Apply `supabase/seed.sql` to the staging project. Record the migration/seed state you observed
(which migrations are applied, whether the seed ran clean) in the findings file. If the seed
fails or the schema is behind `supabase/migrations/`, that is a finding in its own right — report
it; do not silently continue against a half-built database.

### 5. Bring up the local toolchain

```bash
# Android
flutter emulators --launch Pixel_6a
adb wait-for-device
flutter devices          # expect an emulator-5554 entry

# Web driver — chromedriver must match the installed Chrome major version
chromedriver --version   # if this fails, install it and put it on PATH
```

Chrome on this host is 151.x. Install the matching chromedriver (Chrome for Testing
distribution) and confirm `chromedriver --port=4444` starts and `curl -sf
http://localhost:4444/status` answers.

If either cannot be made to work, record it precisely — the CI jobs remain authoritative per
PLAN decision D1, so a missing local web driver degrades iteration speed but does not block the
STEP. A missing emulator does block local Android iteration; say so.

### 6. Proof of life — run one journey for real

This is the actual gate. Pick `integration_test/journeys/auth_journey_test.dart` (it is the
best-formed of the fourteen: 16 assertions, no stubs, and it exercises login/session/logout,
which everything else depends on).

```bash
# Android, from Code/mine-flow-app, with the values coming from your shell env
flutter test integration_test/journeys/auth_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" \
  --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" \
  --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Read the output carefully. **`+0 -0 ~1` / "1 skipped" is a FAILURE of this substep**, not a
pass — it means `isStagingConfigured` is still false. The gate is satisfied only by an
observed **executed** test.

If the journey executes and *fails*, that is a **success for this substep** — the harness is
alive and you have found a real defect. Record the failure verbatim and hand it to 48.1/48.3;
do not fix it here.

### 7. Write the findings file

`Upcoming Prompts/mine-flow-STEP-48.0-FINDINGS.md`, containing:

- The confirmed secret inventory **by name**, before and after.
- Q1/Q2/Q3 answers as the user gave them.
- Which accounts exist and what role each carries (emails are fine; **no passwords**).
- Seed/migration state of the staging database.
- Emulator and chromedriver status, with versions.
- The proof-of-life run: exact command (with values redacted to `$VAR` form), verbatim output
  tail, and the executed/skipped/failed counts.
- An explicit **GATE: PASSED** or **GATE: BLOCKED** verdict. If blocked, name precisely what is
  missing and stop — tell the user STEP-48 cannot proceed and what they need to provide.

## Verification

- The secret list read back from the API contains `TEST_USER_EMAIL` and `TEST_USER_PASSWORD`
  (plus the per-role names if Q1 was yes).
- `flutter devices` lists a booted Android emulator.
- `chromedriver --version` answers, or its absence is recorded as a known local limitation.
- **At least one journey test is observed executing** — a real `+1` in the output, not `~1`.
- `flutter analyze` still reports 0 issues and `dart format --set-exit-if-changed .` is clean
  (this substep should change little or no Dart; if it changed the `ci.yml` Drive line, that is
  YAML and analyze does not cover it — confirm the workflow still parses).
- No secret value appears anywhere in the findings file, the commit, or the terminal transcript
  you report back.

## Keeping the docs true

If the credential/host setup differs from what `architecture/09-environments.md` §2 or
`Code/mine-flow-app/README.md` describes — for instance if the required `TEST_*` secret names are
not documented anywhere — note the gap in your findings and hand it to **48.15**, which owns the
doc sweep. Do not edit architecture docs in this substep.

If you removed the phantom `STAGING_GOOGLE_DRIVE_CLIENT_ID` line, that is a CI change: commit it
on the STEP branch with a message naming the substep, and note that 48.2 owns the rest of the
workflow edits.

Accepted risk: if Q1 comes back "single user only", that is a **deliberate deferral of the RLS
matrix**. Do not add the risk row yourself — record it in the findings and hand it to 48.14,
which owns `registries/risks.yml`.

## Definition of done

- [ ] Q1, Q2, Q3 answered by the user and recorded verbatim.
- [ ] Staging test user(s) exist with correct `public.users.role` values, sign-in confirmed.
- [ ] `TEST_USER_EMAIL` / `TEST_USER_PASSWORD` (and per-role names if applicable) confirmed
      present **by name** in the repository secrets.
- [ ] Staging database seed/migration state recorded.
- [ ] `Pixel_6a` booted and visible to `flutter devices`; chromedriver working or its absence
      explicitly recorded.
- [ ] **One journey observed executing** against staging, with counts quoted.
- [ ] `Upcoming Prompts/mine-flow-STEP-48.0-FINDINGS.md` written, ending in an explicit
      GATE: PASSED / GATE: BLOCKED verdict.
- [ ] No secret value read, printed, logged, or committed.
- [ ] Work committed on `step-0048-runtime-evidence` in the repos it touched.

## Next

If **GATE: PASSED** — tell the user the next action is *"run substep 48.1"* (journey-integrity
repair audit) in a **fresh chat**, and update this substep's status in the STEP PLAN.

If **GATE: BLOCKED** — do not proceed to 48.1. Tell the user exactly what is missing, that
STEP-48 is paused (not failed), and that the row stays `In progress`. Never mark a blocked gate
`Done`.
