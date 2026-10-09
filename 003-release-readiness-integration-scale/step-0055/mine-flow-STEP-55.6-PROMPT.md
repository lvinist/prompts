# mine-flow — STEP-55.6: Daily Log Role-Aware Workflow and Data Contract

> **How to run:** Tell your agent “run substep 55.6”. Execute cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** This substep combines a new persisted hazard contract, role/RLS approval semantics, offline truth, and autosave-safe dismissal; silent errors would corrupt safety and approval records.

## Context
Replace the Daily Log list with a role-aware tabbed review workflow—not Kanban—while migrating forms and reporting. Resolve the structured hazard data contract before presenting UI that claims persistence.

## Read first
STEP-55 PLAN; all prior findings; master spec §4.5 plus §§2–3, 6–9; Docs 04, 06, 11, 12, 15, 16; relevant ADRs/risks; app README/ARCHITECTURE; daily log presentation/BLoC/domain/data/sync files; Supabase migrations/types/policies; auth model; router/tests; STEP-54.6 findings.

## Impeccable
Run context once. Use `layout` for tabs/review cards/form grouping, native `adapt` for bottom-sheet/IME/long text, `harden` for permission/offline/approval/autosave/error states, `clarify` for localized approved workflow copy, then bounded `polish`.

## Task
1. Design and document the minimal persisted hazard contract: explicit none/presence, severity, notes/actions, report mapping, migration, domain/model/DTO/Hive/offline/sync behavior. Keep weather single-select. If architecture authority is insufficient, stop for user decision—do not invent fields.
2. Add migration/generated contract and round-trip/offline tests before UI claims.
3. Build tabs `Semua`, `Draft`, `Perlu Disetujui`, `Disetujui` with counts and role defaults: foreman own Draft; supervisor site-wide submitted review queue. No drag/drop status transitions.
4. Use filter popover for date/zone/foreman/other data; calendar dialog for dates; preserve tab/scroll.
5. Make cards review-oriented with date, real foreman identity, zone, weather/hazard summary, updated time, icon+text status.
6. Add explicit supervisor-only `Setujui Log` for submitted logs; confirm named record/date/foreman; call existing approval use case with authenticated supervisor ID; enforce exactly submitted→approved, `approved_by`, duplicate rejection, repository/RLS authorization, honest offline state, progress/error/success, and retained list state.
7. Implement create `/teams/daily-log/form?date=...` and record `/:id/form`; fetch by ID. Submitted/approved records are read-only for foremen; supervisor can inspect submitted before approval; approved is immutable.
8. Make autosave dismissal safe: flush/await pending save; failure retains input and invokes D4.
9. Replace report push with contextual Daily Log report and residual Material form/action controls.

## Tests
Migration/contract round trips including explicit no-hazard; model/DTO/Hive/sync/report mapping; role tab defaults/counts/visibility; supervisor approval success, duplicate, wrong state, unauthorized role, repository/RLS denial, `approved_by`; offline queued/failed truth; route restoration; autosave close success/failure; filters/calendar; report; IME/drag/long text/48dp/focus/screen reader/themes.

Run targeted data/domain/BLoC/widget/router/migration/contract suites, format/analyze/l10n/Supabase guards. Runtime-check supervisor and field-role paths on Web/Pixel_6a where credentials permit; unavailable roles stay Unverified. Produce `mine-flow-STEP-55.6-FINDINGS.md` with exact schema and authorization evidence.

## Boundaries
No Kanban, arbitrary transitions, client-only authorization, hazard UI without persistence, mutable approved log, invented user identity, or secret/PII artifacts. Significant data-contract changes update Docs 04/11/15 and ADR/risk as required.

Escalate on ambiguous hazard policy, RLS mismatch, attribution drift, offline approval uncertainty, migration incompatibility, or repeated failure.

## Definition of done
Daily Log has a durable tested hazard model, authorized role-aware review/approval flow, restorable safe forms, contextual reporting, honest offline/autosave behavior, and bounded multiplatform evidence.

## Next
Run substep 55.7 in a fresh chat.
