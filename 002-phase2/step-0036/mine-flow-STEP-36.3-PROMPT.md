# mine-flow — STEP-36.3: Offline Sync & Verification

> **How to run:** Tell your agent *"run substep 36.3"* (or *"read and run this file"*).

## Context
This is the final substep for STEP-36. We are integrating the Benchmark feature into the global offline sync engine and verifying the end-to-end functionality.

## Read these first
- overview.md
- coding-standards/README.md

## Scope
- Create `BenchmarkSyncRegistrar` and register it with `SyncQueueManager`.
- Final end-to-end and integration tests.

## Your task
1. **Sync Engine**: Create `BenchmarkSyncRegistrar` implementing the required sync interfaces.
2. Register the registrar with the main sync manager (e.g., in `lib/core/sync/` or dependency injection setup).
3. Ensure offline-created benchmarks (using UUIDs) are correctly synced to Supabase when online.

## Verification
- **Write integration tests** for the offline sync flow of Benchmarks.
- Run the full test suite `flutter test` to ensure no regressions.
- Ensure all code conforms to the analyzer rules (zero warnings).

## Keeping the docs true (always)
- If any accepted risks regarding offline data integrity arise, record them in `registries/risks.yml`.

## Definition of done
- [ ] Sync logic implemented.
- [ ] Integration tests pass.
- [ ] Analyzer passes with zero issues.
- [ ] The STEP-36 test plan is fully satisfied.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: run the STEP review.
