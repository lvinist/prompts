# mine-flow — STEP-48.10: Offline/Sync Part A Against Staging (settles 45.11)

> **How to run:** tell your agent *"run substep 48.10"*. Self-contained — runnable cold.

**Assigned model: Claude Opus 4.8.** One of the three substeps that justify the heaviest tier, and the
only one where a wrong answer means **silent data loss** — a queued mutation overwriting a newer remote
row costs a crew's shift data on a real site. The work requires forcing a last-write-wins conflict
deterministically against live Postgres, asserting on **server** state rather than UI state, and
separating "the manager is wrong" from "the staging round-trip is wrong" while the known Hive
`setUpAll` flake sits in the same blast radius. This is the substep most easily passed by accepting a
green pump as proof. Do not.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings and
`mine-flow-STEP-48.3-FINDINGS.md` — **48.3 (auth) must be Verified first.**

This is the **field-critical journey**. mine-flow is a mining site tool: crews log attendance and
daily work where connectivity is unreliable. If the offline queue loses a shift's data, or if a
conflict silently overwrites a supervisor's correction, the app has failed at the thing it exists to
do. `architecture/15-native-app-architecture.md` §2 commits to offline-first with last-write-wins.

STEP-45 row 45.11 is the strongest of the deferred rows: `Deferred — Partial: sync contract
verified, staging E2E Unverified. Part A (staging) Unverified; Part B verifies the SyncQueueManager
contract unconditionally on-device (offline defer, relaunch persistence, FIFO drain, retry→fail at
maxRetries, last-write-wins). Q5 conflict method documented.`

So **Part B already passes** — the queue's own logic is proven against a real Hive box and a
controllable `NetworkInfo`. It is 455 lines, the largest journey file, and it should stay green.
What has never run is **Part A**: the same behaviours against **real staging data**. Part B proves
the manager honours its contract; Part A proves the contract is the right one when a live Postgres
row is on the other end.

Part A's skip message in the file is exemplary — it names the four `--dart-define` keys and says the
blocker was escalated, not dressed up as a pass. Preserve that standard.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, D1, and **Q5** (how to force the
  conflict).
- `…-48.0/1/2/3-FINDINGS.md` — 48.0's seed record and which user/role you are authenticating as.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-docs/architecture/15-native-app-architecture.md` §2** — the offline-first and
  last-write-wins commitment. This substep's whole purpose is checking runtime behaviour against it.
- `Code/mine-flow-docs/architecture/04-data-model.md` — the `updated_at` / timestamp columns
  last-write-wins depends on.
- `Code/mine-flow-docs/architecture/05-scaling-performance.md` — if it makes claims about queue
  drain behaviour or batch sizes, check them too.
- `Code/mine-flow-app/integration_test/journeys/offline_sync_journey_test.dart` — **all of it**,
  both parts, including the `waitUntil` helper at the top.
- `Code/mine-flow-app/lib/core/sync/` — `SyncQueueManager`, `_defaultSupabaseSync` and its
  skip-when-remote-newer branch, `SyncRegistrar` (STEP-36.3), the battery throttling from STEP-39.
- `Code/mine-flow-app/integration_test/helpers/offline_helper.dart` — `forceOffline()` mocks the
  `dev.fluttercommunity.plus/connectivity` MethodChannel.
- `Code/mine-flow-app/test/integration/sync_queue_manager_test.dart` — the mocked-integration test
  whose fakes Part B mirrors. A green run there is independent corroboration.
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0007 (Hive → `hive_ce` fork migration:
  the queue's durability rests on it), RISK-0009 (`EditableText` finders).

## Scope

**In scope:** running Part A against staging on both platforms; keeping Part B green; comparing
runtime behaviour to Doc 15 §2 and recording divergence or "no divergence".

**Not in scope:** rewriting Part B (it works — do not "improve" it), other feature areas, the design
review (48.13), risk rows (48.14), docs (48.15).

## Your task

### 1. Run the whole file

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/offline_sync_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Both parts run in one invocation. Confirm Part B still passes and Part A now **executes** instead of
skipping. Secrets from the shell environment only.

Note that `processQueue(isManual: true)` bypasses battery gating — Part B relies on this because the
mock channel does not emit on the connectivity event stream. Part A against a real device/emulator
may behave differently; if battery throttling (STEP-39) interferes, use the manual path and say so.

### 2. Prove the four behaviours against real staging data

1. **Offline enqueue defers.** With `forceOffline(true)`, a write from the UI must land in the queue
   and **not** reach staging. Verify the row is absent server-side, not merely that the UI showed a
   pending indicator.
2. **Queue survives relaunch.** Re-pump the app (or construct a fresh manager over the same on-disk
   box) and confirm the queued mutation is still there. This is the behaviour that protects a shift's
   data across an app kill in the field.
3. **Reconnect drains, FIFO by timestamp.** Go online, drain, and confirm the rows appear in
   staging **in the queued order**. Query staging directly to check, do not infer from the UI.
4. **Last-write-wins holds server-side (Q5).** Force the conflict deterministically: write a row
   directly through the Supabase client with a timestamp **newer** than a mutation already sitting in
   the queue, then drain. The newer remote row must **survive** — the older queued mutation must not
   overwrite it. This mirrors `_defaultSupabaseSync`'s skip-when-remote-newer branch. Assert on the
   **server's** state after the drain, which is the whole point of Part A over Part B.

If a queued mutation *does* overwrite a newer remote row, that is **silent data loss** — the most
serious defect class this project can have. Escalate it prominently in your findings, fix the root
cause, check every sibling sync path registered via `SyncRegistrar` for the same flaw, and add a
regression test.

### 3. Corroborate

Run `flutter test test/integration/sync_queue_manager_test.dart` — a green run there is independent
evidence the contract logic is sound and helps separate "the manager is wrong" from "the staging
round-trip is wrong".

Also run `test/integration/attendance_daily_log_sync_test.dart` **in isolation**. It is the known
flake (Hive `setUpAll`, intermittent full-suite, green isolated) and it covers sync for the two
features most likely to expose queue defects. Diagnose it deliberately here rather than treating it
as background noise — if it is now failing for a real reason, this is the substep that would notice.

### 4. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, confirm the file **executes** with Part A running (not
skipped) in `e2e-web` and `e2e-android`, and record the run URL plus real counts. Note honestly if
the emulator/web environment cannot exercise a genuine network transition and what that leaves
unproven. (CI logs without `gh`: PAT from `git credential fill` as a Bearer token;
`/actions/jobs/<id>/logs` 302s to Azure Blob which rejects the auth header — follow `redirect_url`
bare.)

### 5. Record it

`Upcoming Prompts/mine-flow-STEP-48.10-FINDINGS.md`:

- Part A verdict (Verified with URL + counts, or Deferred with named blocker + trigger) and
  confirmation Part B is still green;
- one section per behaviour above, each stating what was asserted **server-side**;
- the exact conflict-forcing mechanism used, so it is reproducible;
- **explicit divergence statement** against Doc 15 §2 — either name the divergence or state "no
  divergence" (48.15 needs this either way);
- the `attendance_daily_log_sync_test.dart` diagnosis: flake or regression, with reasoning;
- anything relevant to RISK-0007 (Hive fork durability) — this is the strongest evidence the project
  has about it.

## Verification

- Part A **executes** (not skipped) on both platforms in a CI run on the branch head, counts quoted;
  or an honest Deferred naming what blocked it.
- Part B remains green.
- All four behaviours asserted against **staging server state**, not just local UI state.
- The conflict test is deterministic and documented.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green, with the known flake diagnosed rather than waved through.
- Any app fix carries a regression test; silent-data-loss findings escalated prominently.
- No secret value in any log, report, or commit.

## Keeping the docs true

If runtime conflict/queue behaviour diverges from
`architecture/15-native-app-architecture.md` §2, that is significant: either the app is wrong (fix
it, file the finding) or the doc records a decision the implementation moved past (hand it to 48.15
with the section and correction, and consider whether it warrants an ADR rather than a Version Log
bump). Say which you concluded. Docstrings on anything you write. Risk rows to 48.14.

## Definition of done

- [ ] Part A observed **executing** against staging on both platforms in CI; Part B still green.
- [ ] Verdict recorded: Verified with URL + counts, or Deferred with a named blocker.
- [ ] Offline defer, relaunch persistence, FIFO drain, and last-write-wins each verified against
      **staging server state**.
- [ ] Conflict-forcing mechanism documented and deterministic.
- [ ] Explicit divergence / "no divergence" statement against Doc 15 §2.
- [ ] `sync_queue_manager_test.dart` corroboration run; `attendance_daily_log_sync_test.dart`
      diagnosed as flake or regression with reasoning.
- [ ] Any data-loss-class defect escalated prominently, root-caused, sibling `SyncRegistrar` paths
      checked, regression test added.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green.
- [ ] `Upcoming Prompts/mine-flow-STEP-48.10-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.11"* (deep-link validation, RISK-0006) in a
**fresh chat**, and update 48.10's status in the STEP PLAN.
