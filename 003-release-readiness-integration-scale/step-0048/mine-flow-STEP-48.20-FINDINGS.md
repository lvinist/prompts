# STEP 48.20 Findings: Staging Fixture & Seed Alignment

**First pass:** 2026-09-01 (Gemini 3.1 Pro High per PLAN assignment). **Re-run:** 2026-09-01
(Opus 4.8 escalation) — completes the first pass, which was cut off mid-verification, and
closes the 48.26 NO-GO routing for R-5 (empty-string UUIDs), R-6 (roster/KRU-00N), and the
fixture half of R-4. The re-run discovered the **root cause of the whole "saved edit
vanishes" class** (details in §6–§7).

## 1. Site-ID Mismatch (Q10)
**Settled on:** `f47ac10b-58cc-4372-a567-0e02b2c3d479` (defaultSiteId in app_constants.dart).
Replaced all occurrences of `00000000-0000-0000-0000-000000000001` across the codebase
(including seed.sql, widget tests, unit tests, and models). The schema migrations retain
their documented defaults as DDL changes are out of scope (per 48.17).

Grep evidence (re-run): zero occurrences of the legacy UUID remain under `lib/`,
`supabase/seed.sql`, `integration_test/`, `test/`. The only remaining sites are the
`site_id … DEFAULT '00000000-…-0001'` column defaults in migrations (DDL, out of scope) —
and the re-run's BenchmarkModel change (§7) makes app writes carry `site_id` explicitly so
the default is never used.

## 2. Invalid UUIDs in Writes (App Defects)
- **Empty-string UUID (22P02)**: `ZoneCubit.createZone` defaulted `siteId` to `''`; the
  journey's CreatableCombobox "Tambah" flow sent it to Supabase → `22P02`. **Fixed in the
  re-run** (48.26 R-5): `ZonePicker.siteId` now defaults to `defaultSiteId` (never `''`) and
  passes it through to `createZone`; `zone_cubit.dart` never fabricates an empty site.
- **Benchmarks 22P02 (found by 48.26)**: `BenchmarkBloc._onSubmitBenchmark` passed
  `id: ''` for new rows. **Fixed in the re-run**: generates a `Uuid().v4()`;
  `BenchmarkModel` gained an explicit `siteId` (default `defaultSiteId`) that is always
  emitted in `toJson`, so new rows land under the settled site instead of the schema
  default.
- **KRU-001 / KRU-002**: the debug roster seeder fabricated non-UUID crew codes. **Fixed
  in the re-run** (48.26 R-6): `SeedDefaultRosterEvent.userIds` is now test-only; in the
  app the seeder loads the **real site roster** through the new
  `AuthRepository.getSiteRoster` (SELECT under the `users_read_active` RLS policy — no
  privilege escalation), and `_NoopAuthRepository` (tests) degrades to a no-op roster.
  The journey waits in pump slices for the network roster to render.

## 3. RLS Refusal (42501 on zones)
- **Verdict: refusal is correct.** `supervisor_zones_all` (`20260718000002_rls_policies.sql`)
  restricts zone INSERT to supervisors; `zones_read_active` grants SELECT-only to
  foreman/crew.
- **Context:** the 42501 fired only because the zone dropdown was empty (site-id
  mismatch) and the journey tapped the "Tambah" tile — an *accidental* insert attempt, not
  a policy defect. With the fixture fix the dropdown populates and the journey selects an
  existing zone. No policy was weakened; no ADR needed.

## 4. Fixture Provisioning
- **Decision:** reuse `supabase/seed.sql`. It is idempotent (`ON CONFLICT … DO NOTHING`)
  and provides zones/users under the settled site id.
- **Revision:** branch `step-0048-runtime-evidence`, commit `451a77e` ("STEP-48.20: staging
  fixture & seed alignment to defaultSiteId") plus the re-run's uncommitted-to-that-point
  seed comment update (benchmarks intentionally unseeded — the journey creates its own row
  and a seeded `bm_id` could collide under `UNIQUE (site_id, bm_id)`).

## 5. Staging Verification (completed)
The seed was applied to staging and executed **twice** to confirm idempotency (no
conflicts on the second run). Census after the move (first pass), quoted:

```
zones_new 2 · users_total 6 · cut_fill_new 3 · equipment_new 4 · inventory_new 3
attendance_new 2 · daily_logs_new 6 · geospatial_new 1 · land_clearing_new 3
users_new_site 6 · attendance_today 0 · benchmarks_total 0 · users_legacy_site 0
attendance_legacy_site 0 · stranded_seed_fixture_rows 0
```

All seeded rows sit under `f47ac10b-…` (`*_legacy_site` counts are 0), and the three
staging accounts (`supervisor@`, `foreman@`, `crew@`) exist. The crew account still has no
secrets (`TEST_CREW_*` absent) — the crew RLS leg remains credential-blocked, RISK-0021
stays open.

## 6. Journey Re-runs (re-run, 2026-09-01, emulator-5554, staging `.env`)

| Journey | Result | Classification |
|---|---|---|
| `attendance_journey_test.dart` | **PASS** (`+1: All tests passed!`, EXIT 0) — after §7 fixes | R-6 closed: sick save + leave edit persist end-to-end, **0 LWW conflicts** |
| `rls_authorization_journey_test.dart` | **PASS** (`+1 ~2`, EXIT 0) | 1 pass + 2 legit skips (`crew@` secrets absent; per-role matrix needs `TEST_SUPERVISOR_*`) — RISK-0021 unchanged |
| `daily_log_journey_test.dart` | fail at **step 10** (`DailyLogListScreen` 0 widgets), twice (2nd run on the fixed build) | **Steps 1–9 pass live — including the submit→`submitted` repository read-back that 48.23 deferred as failure B: the persistence class is dead** (§7 fixes). The remaining failure is the **BH-020 nav defect (48.22 class)** — the list screen does not mount after `appRouter.go`; not fixture drift; **0** `22P02`/`23503` |
| `cut_fill_journey_test.dart` | fail | R-7 verbatim: `Pilih tipe material` tap off-screen → combobox never opened → `OB / Waste` unfindable → **48.21**; **0** `22P02`/`23503` |

**The 48.20 success criterion holds:** across all four assigned journeys the failure
classes the substep was created to kill (`22P02`, `23503`, `42501`) are **gone** —
`42501` appears only inside the RLS journey's deliberate refusal assertions, which pass.

## 7. Root causes discovered by the re-run (the "phantom-future timestamp" class)

Run 1 failed at journey step 8 (UI list reflection), run 2 at step 7 (read-back). The logs
exposed two stacked defects that no fixture change could fix:

**(a) Client timestamps were local wall time without an offset.** The bloc stamps
edits with `DateTime.now()` (local, +07) and DTOs emit `updated_at` via
`toIso8601String()` with no UTC conversion, so Postgres stored 21:32 **local** as
21:32 **UTC** — 7h in the future. Every later last-write-wins comparison (registrar,
refresh merge) then correctly honors the phantom-future row and drops the fresh edit.
Evidence: `AttendanceSyncRegistrar: Conflict for attendance [43d91746…]: remote
(2026-09-01 21:32:34.455711Z) is newer than queued mutation (2026-09-01 21:46:24.014032)
. Remote wins.` — remote was actually 7h *older*.
**Fixed:** `AttendanceRepositoryImpl.saveAttendance` re-anchors to UTC
(`(record.updatedAt ?? DateTime.now()).toUtc()`); `SyncQueueManager._defaultSupabaseSync`
emits `item.timestamp.toUtc()`; the daily-log repository's four write sites stamp UTC
(`autoSaveDraft`, submit, approve, soft-delete). Pinned by a new unit test asserting the
queued payload's `updated_at` ends in `Z` and is not in the future.

**(b) The DB trigger overwrote every client stamp.** `update_updated_at_column()` set
`NEW.updated_at = NOW()` on **every** write, so the server replaced the client's
(un-mangled) timestamp with its own write-processing time — which is always later than a
follow-up edit made while the previous write was in flight. The client LWW guard was
therefore structurally broken: the *second* edit of any row always lost (verified live in
run 4: queued `16:07:21.066Z` vs remote `16:07:24.510Z`). **This is the true root cause
of the "saved edit vanishes" class** (48.26 R-6, and 48.23's sick/submitted failures).
**Fixed (user-approved):** migration `20260901000001_step_48_20_updated_at_respects_client.sql`
replaces the trigger function with an IF-NULL fill (client-supplied stamps are kept; the
DEFAULT backfills INSERTs without one). Applied to staging via `supabase db push` and
verified by `pg_get_functiondef`. Changing trigger semantics is schema DDL — recorded in
Doc 04 v0.1.5 (client-supplied `updated_at` contract).

**(c) Journey determinism.** The journey assumed an empty form; against leftover staging
rows its unscoped `.first` finders could hit another crew member's chips, and its
userId-keyed read-backs were ambiguous. **Fixed:** pick a crew member without a row for
today (fallback: first item), scope chip/remarks taps to the target `CrewRosterItem`, use
a unique-per-run remark, and key both read-backs by the captured record id (userId
fallback). Repeated runs are now idempotent against a dirty staging site.

**(d) Staging remediation (user-approved).** The 3 leftover attendance rows from today's
pre-fix runs carried the phantom-future stamps; no app fix can converge against
corrupted data. Per explicit user approval ("Normalize timestamps"), a guarded UPDATE
shifted `updated_at`/`created_at` by −7h for those 3 rows only (`AND … > now()` prevents
double-shifting). Post-fix query: all rows `still_future: false`, no rows deleted.

**(e) Migration-history reconciliation (bookkeeping).** Staging's history held two
uncommitted CLI-created entries (`20260831091435`, `20260831091601`) duplicating 48.17's
work, and 48.17's repo migrations were unrecorded remotely. Verified equivalence first
(live tables = repo set; live policies = exactly the 10 the repo files declare), then
`migration repair --status reverted` the phantoms, `--status applied` 48.17's files, and
pushed — the push applied only the new trigger-function migration.

## 8. Verification (re-run gates)

- `flutter analyze`: **0 issues**. `dart format`: clean on all touched files.
- `flutter test` full suite: **487 passed, 0 failed** (EXIT 0), including the new
  UTC-stamp test and the first pass's LWW-merge tests (Hive flake not observed; the known
  `attendance_daily_log_sync_test` flake class monitored — suite fully green).
- Daily-log unit/widget tests: 3 passed after the syncRemote merge fix.
- Journeys: see §6 table.
- Contract types: unaffected — the migration changes a function, no columns; TS
  `database.ts` unchanged.

## 9. Hand-offs and residuals

- **48.21 (re-run):** cut/fill R-7 remains — `Pilih tipe material` tap misses (off-screen
  at default viewport); also the `OB / Waste` finder. Evidence: `step4820_cut_fill…
  .log` hit-test warning at Offset(205.7, 631.3).
- **48.22 class:** daily-log's `DailyLogListScreen` nav failure (BH-020) reproduced live
  **twice**; steps 1–9 (through the submitted read-back) pass on the fixed build.
- **48.23's failure B:** the refresh-clobber race hypothesis is now **confirmed and
  fixed in code** (daily-log `syncRemote` LWW merge + UTC stamps + IF-NULL trigger) —
  the daily-log journey's submit→`submitted` read-back passed live on the fixed build;
  the next full wave (48.24/48.26) re-verifies the whole journey after BH-020 is fixed.
- **Named residual (same class, not exercised by 48.20's journeys):** the tracking
  (cut/fill, land clearing, inventory), equipment-check, and data-bucket repositories and
  their datasources still stamp `DateTime.now()` without `.toUtc()` (6 soft-delete sites
  in datasources). Their journeys did not expose it in this run, but the class is proven.
  Recommend a mechanical sweep in the next wave.
- **RISK-0021:** unchanged — crew leg still credential-blocked (no `TEST_CREW_*`).
- **No staging row was deleted.** One approved timestamp normalization (3 rows) and one
  approved trigger-function migration were applied; both recorded above.

## 10. Safety

The scoped `sbp_…` token was used for session-only staging queries/pushes and was never
written to a file, echoed, or committed. **User: revoke the token now that 48.20's
staging work is complete.**
