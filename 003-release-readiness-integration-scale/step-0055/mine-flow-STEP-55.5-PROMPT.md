# mine-flow — STEP-55.5: Crew Attendance Workflow Rebuild

> **How to run:** Tell your agent “run substep 55.5”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** The reviewed interaction and persisted status mapping are explicit, but nullable draft state, reason clearing, offline sync truth, and batch validation require careful state modeling.

## Context
Rebuild attendance as one simple route-backed batch sheet. A newly loaded roster must be unset, not falsely present. Persisted records remain non-null after validation.

## Read first
STEP-55 PLAN; prior findings; master spec §4.4 plus §§2–3, 6–7; Doc 07; Docs 04/11/12/15; attendance files/tests, sync queue APIs, auth/site context, router; STEP-54.5 findings.

## Impeccable
Run context once. Use `layout` for the one-row header/card list/footer density, native `adapt` for one-handed choices/IME, `harden` for unset/reason/offline/error/long-name states, and bounded `polish`.

## Task
- Create a form-only roster draft model with nullable status for missing date records; never pre-mark present. Keep persisted entity/DB status non-null.
- Implement `/teams/attendance/form?date=YYYY-MM-DD&siteId=<id>` in shared sheet; validate/default date/site only as authorized; apply universal dirty guard.
- Header: date/calendar dialog left, `Tandai Semua Masuk` right; narrow wrap preserves order/targets. Bulk action changes only unset rows.
- Card: real name primary, role/position secondary, no UUID copy; four inline icon+text choices mapped exactly Izin=`leave`, Sakit=`sick`, Alpa=`absent`, Masuk=`present`.
- Reveal required trimmed reason only for Izin/Sakit using existing `remarks`; implement explicit clearing semantics and confirmation before discarding non-empty reason when status changes.
- Add honest queued/syncing/failed/synced per-record indicator and labelled retry without conflating it with attendance state.
- Preserve search/status/date filters and list position; use popover-first list filters. Keep batch footer `Simpan Absensi (N Kru)` reachable above IME; validate all statuses/reasons before submit.
- Keep no D7 member inspector. Replace report push with contextual attendance report seeded by date/site.

## Tests
Test fresh roster unset; mixed existing/unset; bulk action preserves exceptions; four mappings; reason required/trimmed/persisted; copyWith can explicitly clear remarks; confirmation on clearing; first-invalid focus/scroll; batch count/double submit/error retention; dirty dismissal; sync transitions/retry/announcements; filter/calendar/list preservation; cold route/site authorization; long names/2x text/48dp/IME/themes/report.

Run attendance unit/data/BLoC/widget/integration/router suites, format/analyze/guards, then one bounded Web/Pixel_6a inspection. Produce `mine-flow-STEP-55.5-FINDINGS.md` tracing `FC-54.5-001..013` plus reviewed requirements.

## Boundaries
No nested tabs/pages, default-present draft, UUID labels, hidden inline attendance choices, separate member inspector, or false offline-success claim. Escalate if existing persistence cannot distinguish explicit null clearing or sync state cannot be attributed per record.

## Definition of done
Attendance is a simple, honest, restorable batch workflow with tested status/reason/sync semantics and polished accessible layout on both platforms.

## Next
Run substep 55.6 in a fresh chat.
