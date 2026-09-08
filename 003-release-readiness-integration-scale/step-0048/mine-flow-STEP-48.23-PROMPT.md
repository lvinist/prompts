# mine-flow — STEP-48.23: Persistence & Offline-Integrity Defects

> **How to run:** tell your agent *"run substep 48.23"*. Self-contained — runnable cold.

**Assigned model: Claude Opus 4.8.** The only new substep in the remediation wave that earns the
heaviest tier. Three failures share one shape — **a write appears to succeed and the persisted value
is wrong** — which is the signature of silent data loss, the same class 48.10 was escalated for. Each
has at least two candidate explanations, and the cheap resolution for all three is to edit the
assertion until it passes. That would launder a real defect into a green suite and defeat the STEP.
Deciding correctly *is* the deliverable.

## The three failures

From branch-head CI run
[`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159), both platforms:

**A — attendance status does not persist.** `attendance_journey_test.dart:120`

```
Expected: AttendanceStatus:<AttendanceStatus.sick>
  Actual: AttendanceStatus:<AttendanceStatus.present>
```

The journey opens the attendance form, sets a crew member to *Izin sakit* with remarks
`'Izin sakit shift pagi'`, taps **Simpan** in the dialog, taps **Simpan Absensi** for the batch, then
reads back through `appServices!.attendanceRepository.getAttendanceForDate(now)`. The record exists,
`loggedBy` is correct — and `status` came back `present`, the column default.

**B — daily log status does not persist.** `daily_log_journey_test.dart:134`

```
Expected: LogStatus:<LogStatus.submitted>
  Actual: LogStatus:<LogStatus.draft>
```

Same shape. The journey fills the form, taps submit, reads back via
`getDailyLogs(siteId: defaultSiteId)`, finds the row by its summary — and `status` is `draft`. Note
the journey reached step 9, so the row was written; only the status is wrong. Note also that on
Android the subsequent navigation assertion failed too (`Found 0 widgets with type
"DailyLogListScreen"` after `appRouter.go`) — decide whether that is a second defect or a consequence
of the first, and route it if it is not yours.

**C — offline queue leaks to staging before the drain, on web.**
`offline_sync_journey_test.dart:220`

```
Expected: null
  Actual: { 'id': '14f9dc1c-…', 'status': 'draft',
            'summary': 'E2E offline daily log A (airplane mode)', … }
offline daily log must NOT exist on staging before drain
```

This assertion is the whole point of Part A: after `forceOffline(true)`, a mutation must sit in the
Hive queue and **not** reach Postgres. On web it was already there. Note the row's
`created_at == updated_at == 2026-08-30T18:56:56.551+00:00` — a single write, not an update — so
either the offline gate did not hold, or a previous run left the row and the pre-clean missed it.

## Why these are one substep

All three are "the store disagrees with what the user did". On a mining site that means a crew's shift
data. 48.10 already found four data-loss-class defects in exactly this area — an unregistered Hive
adapter, adapter guards testing placeholder typeIds, a re-entrancy flag set after the first `await`
causing double-send, and sync registrars routing drained items back through local-first writes so the
queue never drained at all. That last one is instructive: the symptom was "sync doesn't work", the
cause was four layers down, and a lesser fix would have been to relax the test.

Assume the same depth here.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, the honesty rule, and
  question **Q12** (is web a supported platform for offline Part A at all?).
- **`Upcoming Prompts/mine-flow-STEP-48.16-FINDINGS.md`** — your scope: the `BH-nnn` rows classified
  persistence / data-integrity.
- **`Upcoming Prompts/mine-flow-STEP-48.10-FINDINGS.md`** — read this one closely. It documents the
  four defects it fixed, the sibling sweep it did across sync registrars, how it forced a
  last-write-wins conflict (staging's `update_updated_at_column` trigger blocks fake timestamps, so it
  used wall-clock ordering), and that it already narrowed the relaunch-persistence assertion to
  Android. Your failure C sits inside that work.
- `Upcoming Prompts/mine-flow-STEP-48.4-FINDINGS.md` — attendance and daily-log runtime work; it fixed
  a `users` FK ambiguity and invalid `full_name` references. Its evidence is what failure A and B now
  contradict, so Q7's status question may apply.
- `Upcoming Prompts/mine-flow-STEP-48.1-FINDINGS.md` — the journey-integrity standard, and the
  `defaultSiteId` ≠ seed `site_id` handoff.
- `Upcoming Prompts/mine-flow-STEP-48.20-FINDINGS.md` if it has run — fixture state materially affects
  failure C's "stale row" hypothesis.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-docs/architecture/15-native-app-architecture.md` §1–§2** — the platform scope and
  the offline-first / last-write-wins commitment. §1 scopes offline-first to the **Android field app**.
  This is the authority for Q12.
- `Code/mine-flow-docs/architecture/04-data-model.md` — the timestamp columns last-write-wins depends
  on; note 48.10 handed forward a "server-side `updated_at` authority" clarification for the docs.
- `Code/mine-flow-app/supabase/migrations/20260718000001_core_schema.sql` — `attendance_records.status`
  is `public.attendance_status NOT NULL DEFAULT 'present'` with a
  `UNIQUE (user_id, date)` constraint; `daily_logs.status` defaults to `draft`. **The defaults are
  exactly the wrong values you observed** — that is a strong hint about where the field is being lost.
- The write paths, end to end, for both features: form/bloc → repository → local datasource → sync
  queue → sync registrar → remote datasource. Read all of it; the bug in 48.10 was in the registrar,
  four layers from the symptom.

## Hypotheses to test — do not stop at the first plausible one

**A and B (status defaults to the column default):** the value is being dropped somewhere between the
UI and Postgres. Candidates, each with a distinguishing test:

1. **Form state never commits.** The dialog's status selection is not written back before Simpan.
   *Distinguish:* assert the entity's status in memory immediately after the tap, before any
   persistence.
2. **Repository/DTO drops the field.** A `toJson` omits `status`, or an upsert sends a partial row and
   Postgres applies the default. *Distinguish:* inspect the payload the sync registrar sends; check
   whether the enum→string mapping produces a value the `attendance_status` enum accepts (a rejected
   enum value could land as the default, or the whole row could fail).
   **Coordinate with 48.19** — it removed phantom keys from write paths, and `equipment_check_dto`'s
   `status` was one of them. Make sure a legitimate `status` was not removed along with the phantom
   ones; if 48.19 has run, diff its changes to these models first.
3. **The `UNIQUE (user_id, date)` constraint turns the write into a conflicting insert** that is
   resolved by keeping the existing row (created earlier in the same journey, or seeded by
   `seed.sql`, which seeds a `present` attendance row for the crew user on `CURRENT_DATE`). *This is
   a strong candidate for A* — look at whether the save path upserts or inserts, and what it does on
   conflict. **Check `seed.sql` before concluding the app is wrong.**
4. **Read-back path is wrong.** `getAttendanceForDate(now)` returns a *different* record than the one
   written (wrong site, wrong user, first-of-many). *Distinguish:* assert on the id you wrote.

**C (row on staging while offline, web only):** candidates:

1. **`forceOffline` does not suppress the network on web.** Read `integration_test/helpers/offline_helper.dart`
   and whatever `NetworkInfo` implementation web uses. If web has no way to gate the Supabase client,
   the queue is bypassed and writes go straight out — that is a **real platform limitation**, and per
   Q12 the honest outcome is an explicit Android-only scope for Part A, not a weakened assertion.
2. **Stale row from a previous run.** The test pre-cleans by id, and ids are fresh `Uuid().v4()` per
   run, so a stale row would need to share the id — unlikely, but the `created_at == updated_at`
   timestamp is worth checking against the run's own start time to rule it in or out definitively.
3. **Local-first write reaching remote anyway** — the exact class 48.10 fixed for three registrars.
   Check whether the daily-log path on web takes a branch that Android does not.

## Your task

1. **Reproduce all three locally** — A and B on the emulator, C on web via
   `flutter drive --driver=test_driver/integration_test.dart --target=… -d web-server --browser-name=chrome`
   (plain `flutter test integration_test -d chrome` is unsupported on 3.47.x). Record commands and
   output. Take `--dart-define` values from the user or the workflow's secret **names**; never print a
   value.
2. **Diagnose to root cause.** For each, name the file:line that is wrong and state the evidence that
   rules out the other hypotheses. "Fixed by changing X" without a ruled-out list is not a diagnosis.
3. **Sweep siblings.** If attendance drops a field, check daily log, equipment check, cut/fill, land
   clearing, and inventory for the same flaw. 48.10's sibling sweep is the precedent: fix the class.
4. **Fix the root cause**, not the assertion. If the honest answer is that a platform cannot support a
   behaviour, narrow the **scope** explicitly — a `markTestSkipped` with a named reason followed by
   `return`, in the style 48.1 established and 48.10 used for the Android-only relaunch assertion —
   and record it as a **Deferred** item with a revisit trigger. That is a legitimate outcome. A
   relaxed `expect` is not.
5. **Assert server-side.** 48.10's standard: for anything involving sync, assert against the real
   Postgres row (`client.from(...).select().eq('id', id).maybeSingle()`), not the UI or the local
   cache. A green pump is not proof.
6. **Pin each fix at the lowest tier that can catch it.** A journey-only fix is insufficient: add a
   repository, bloc, or DTO test that fails without the fix and needs no staging round-trip. These
   defects survived to a branch-head run precisely because nothing below the E2E tier covered them.
7. **Answer Q12 in writing**, citing Doc 15 §1. If Part A becomes Android-only, say what the web leg
   would need in order to be supported, so a future STEP has a starting point.

## Escalation and honesty

- If a failure cannot be classified as app-defect vs test-defect from the evidence, say so and stop —
  do not flip a coin.
- If runtime behaviour appears to contradict `architecture/15-native-app-architecture.md`, an ADR is
  superseded **deliberately**, never retrofitted to match drifted code. Report the contradiction; do
  not edit the doc to bless it.
- If the same fix fails twice, stop, re-diagnose, and escalate to the user rather than iterating.
- If you find yourself about to mark something verified that the harness cannot evidence, label it
  **Unverified** and say why.

## Verification

- All three failures reproduced before the fix and absent after; commands and output recorded.
- Each diagnosis names a file:line root cause with the competing hypotheses explicitly ruled out.
- Sibling sweep completed across the other features' write paths; results stated even where clean.
- Sync-affecting assertions are **server-side**.
- New lower-tier tests fail without the fix and pass with it; you have demonstrated both.
- Any narrowed platform scope is an explicit `markTestSkipped` + `return` with a named reason and a
  revisit trigger, recorded as Deferred — never a weakened matcher.
- Assertion counts per journey ≥ the 48.1 baseline; no `expect` deleted.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean; `flutter test` green.
  The `attendance_daily_log_sync_test.dart` / `equipment_check_sync_test.dart` Hive `setUpAll` flake is
  known — re-run isolated to confirm and say so; **never wave a red suite through**.
- `sync_queue_manager_test` and the per-feature sync tests still green (48.10's corroboration set).
- Q12 answered in writing against Doc 15 §1.

## Scope

**In scope:** the three failures, their root causes anywhere in the write path, the sibling sweep,
lower-tier regression tests, and any platform-scope narrowing.

**Not in scope:** migrations or staging DDL (48.17), read-query column names (48.18), write-path key
sets (48.19 — but coordinate), seed and fixture data (48.20 — but coordinate on the seeded attendance
row), finder repair (48.21), layout/Material/Drive/screenshot defects (48.22), `risks.yml` status
edits, and doc rewrites (48.15).

## Definition of done

- [ ] Failure A diagnosed to a root cause and fixed, or narrowed with an honest Deferred; the
      `UNIQUE (user_id, date)` and seeded-row hypotheses explicitly addressed.
- [ ] Failure B diagnosed and fixed; the Android `DailyLogListScreen` navigation failure either fixed
      or routed to its owner.
- [ ] Failure C resolved: real defect fixed, or web scope narrowed per Q12 with Doc 15 §1 cited and a
      revisit trigger recorded.
- [ ] Sibling sweep across all feature write paths complete and reported.
- [ ] Lower-tier regression tests added for each fix, demonstrated failing without it.
- [ ] Server-side assertions used for everything sync-related.
- [ ] No assertion weakened; counts stated against 48.1's baseline.
- [ ] `flutter analyze` 0, `dart format` clean, `flutter test` green (flake diagnosed isolated).
- [ ] Attendance, daily-log, and offline/sync journeys run on both platforms where supported; counts
      recorded per file.
- [ ] Q12 answered; any doc-truth handoff written for 48.15.
- [ ] `mine-flow-STEP-48.23-FINDINGS.md` written; PLAN progress table updated.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.24"* (local full-gate re-run) in a **fresh chat**,
and that 48.24 requires 48.17–48.23 all complete. Name anything you left Deferred, so 48.25 knows what
may legitimately still be red.
