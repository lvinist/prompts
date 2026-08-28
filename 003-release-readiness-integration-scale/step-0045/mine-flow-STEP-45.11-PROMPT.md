# mine-flow — STEP-45.11: Field-critical offline/sync full journey

**Recommended model:** Gemini 3.1 Pro — **escalate to Opus 4.8 only if** the conflict-resolution logic can't be gotten right on Pro. This is the most subtle journey in the STEP; it is the one place an Opus escalation is justified.

> **How to run:** *"run substep 45.11"*. Self-contained; runnable cold.

## Context

**The single most important journey in this STEP.** mine-flow is offline-first for field foremen;
this behavior has only ever been unit-tested with mocks. This substep drives the real
airplane-mode → queue → reconnect → conflict-resolution cycle against live staging data. Depends on
45.4–45.6 (entry journeys) and the `offline_helper` from 45.1. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md` (Q5 — deterministic conflict).

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md` — Q5.
- `Code/mine-flow-app/lib/core/network/` — `ConnectivityService` (online/offline stream).
- The `SyncQueueManager` and per-feature sync registrars
  (`lib/features/*/data/sync/*_sync_registrar.dart`) — queue, retry/backoff, conflict handling.
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md` — offline-first / event-based sync design.
- STEP-39 (low-battery sync logic) and STEP-40.3 (SyncQueueManager retry timing) for the current sync contract.

## Scope

Owns `integration_test/journeys/offline_sync_journey_test.dart`. Uses the `forceOffline` helper.

## Your task

Write one comprehensive journey (against staging):
1. **Offline entry:** `forceOffline(true)` → create records across a couple of features (e.g. a
   daily log + an attendance record) → assert they are written to the local Hive queue, not sent.
2. **Queue persistence across relaunch:** re-pump/restart the app harness still offline → assert the
   queued records survive (persisted, not lost).
3. **Reconnect + drain:** `forceOffline(false)` → assert `SyncQueueManager` drains the queue to
   staging and the records now exist server-side with correct attribution.
4. **Conflict resolution:** force a conflict deterministically (Q5 — e.g. seed a server-side change to
   the same row while offline, or two-client edit) → reconnect → assert the app's documented conflict
   strategy resolves it correctly (no silent data loss; the resolution matches the sync contract).
5. Assert retry/backoff behavior at runtime (a transient failure retries, then marks failed after max
   retries) consistent with STEP-40.3.

If staging creds are unavailable, mark the journey **Unverified** with the reason — this is the most
important item to run for real, so escalate the missing-credential blocker to the user rather than
quietly skipping.

## Verification
- Offline/sync journey passes on Chrome **and** `Pixel_6a` (airplane-mode semantics differ by
  platform — run both), or Unverified w/ reason.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch.

## Keeping the docs true (always)
- If runtime sync/conflict behavior diverges from `architecture/15-native-app-architecture.md`,
  record for 45.15 (Version Log bump or ADR).

## Definition of done
- [ ] Full offline journey (offline entry → persist across relaunch → reconnect drain → conflict
      resolution → retry/backoff) passes on both platforms, or Unverified with an escalated reason.
- [ ] Q5 conflict-forcing method documented.
- [ ] analyze 0 / format clean; file documented.

## Next
Run substep 45.12 (Live RLS / authorization E2E) in a fresh chat.
