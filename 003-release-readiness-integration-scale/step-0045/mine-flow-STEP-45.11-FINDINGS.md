# STEP-45.11 Findings — Field-critical offline/sync full journey

## Deliverable
`integration_test/journeys/offline_sync_journey_test.dart` — the field-critical
offline → queue → reconnect → conflict-resolution → retry/backoff journey.

Structured in two parts so the sync **contract** produces genuine runtime
evidence even when staging is unavailable:

- **Part A (staging-gated, full E2E):** login → offline entry through the real
  app services (daily log + attendance) → assert queued to local Hive, not sent
  → app relaunch still offline → assert queue survives → reconnect + manual
  drain → assert server-side existence with correct attribution → conflict /
  no-silent-loss assertion. Skipped as **Unverified** (via `markTestSkipped`)
  when staging credentials are absent — never reported as a pass.
- **Part B (unconditional contract):** offline enqueue defers execution; the
  Hive-backed queue survives a fresh `SyncQueueManager` (relaunch semantics);
  reconnect drains FIFO by timestamp; transient failure retries then permanently
  fails after `maxRetries` (STEP-40.3); and last-write-wins keeps a newer remote
  timestamp over an older offline mutation (Q5). Needs only the on-device Hive
  store + a controllable network, so it is real runtime evidence on any device.

## Q5 — deterministic conflict forcing (documented)
A server-side row is treated as carrying a timestamp **newer** than the queued
offline mutation before reconnect. Per the documented **last-write-wins**
strategy (Doc 15 §2 / offline-strategy decision), the newer remote record must
win and the older local mutation must be skipped — no silent data loss. Part B
asserts this deterministically against the manager's timestamp-based resolution
(mirroring `SyncQueueManager._defaultSupabaseSync`); Part A asserts the synced
record survives against real staging data.

## Verification status
- `flutter analyze integration_test/journeys/offline_sync_journey_test.dart` →
  **No issues found**.
- `dart format` → clean.
- Existing `test/integration/sync_queue_manager_test.dart` (same fake-network /
  retry / FIFO / battery patterns this file reuses) → **8/8 pass**, corroborating
  the Part B contract logic.
- **E2E execution on device: UNVERIFIED on this host.** Three independent
  blockers, none introduced by this substep:
  1. **No staging credentials** — `SUPABASE_URL` / `SUPABASE_ANON_KEY` /
     `TEST_USER_EMAIL` / `TEST_USER_PASSWORD` are not injected locally (only
     `.env.example` exists). Part A skips as Unverified by design.
  2. **Android debug build broken on this Windows host** — `flutter build apk
     --debug` fails identically **without** this test involved:
     `package_info_plus does not specify compileSdk` under AGP 9 `newDsl`, plus a
     cross-drive Gradle "different roots" error (PUB_CACHE on `C:`, project on
     `D:`). This is a host/toolchain regression on local Flutter 3.47.1, out of
     scope for a test-authoring substep; CI pins 3.47.0 and runs the
     `e2e-android` emulator job there.
  3. **Web unsupported** — `flutter test integration_test -d chrome` returns
     "Web devices are not supported for integration tests yet" on this Flutter;
     the `e2e-web` CI job uses chromedriver, which is not installed locally.

The Pixel_6a emulator WAS booted successfully (`emulator-5554`, `sys.boot_completed=1`)
and the test was dispatched to it — the failure is the Gradle assembleDebug step,
not the test.

## Escalation (per PLAN ground rules)
This is the single most important journey in STEP-45. To convert it from
Unverified to a real pass, the STEP-45 owner needs to run it in CI (or a host
with a working Android build) with staging secrets set:

```
flutter test integration_test/journeys/offline_sync_journey_test.dart \
  -d <device> \
  --dart-define=SUPABASE_URL=... \
  --dart-define=SUPABASE_ANON_KEY=... \
  --dart-define=TEST_USER_EMAIL=... \
  --dart-define=TEST_USER_PASSWORD=... \
  --dart-define=APP_ENV=staging
```

The existing CI `e2e-web` / `e2e-android` jobs already inject the `STAGING_*`
secrets and pick up every file under `integration_test/`, so this journey runs
automatically there on the next push to the STEP-45 branch — that CI run is the
authoritative pass/Unverified evidence for 45.15.

## Docs-true note for 45.15
Runtime sync/conflict behaviour matches `architecture/15-native-app-architecture.md`
§2 (offline-first, background sync, last-write-wins). No divergence found; no
Version Log bump or ADR required from this substep.
