# mine-flow — STEP-51.9: Dead-file disposition (deletion & record — corrected by 51.1)

> **How to run:** Tell your agent *"run substep 51.9"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** Bounded deletion work with an unambiguous
> signal: exact-path reference greps either hit or they don't. Kept as an explicit substep by
> user decision D6 so the close checklist item stays auditable.

## Context

**CORRECTED BY 51.1 (2026-09-09): this is a real deletion substep, not verify-and-record.**
The original premise — "all 7 candidate files already deleted by 48.30" — was **false**.
48.30 deleted only the two shadowing files (`lib/app/presentation/pages/settings_page.dart`,
`lib/app/presentation/widgets/app_shell.dart`, commit `bb32c92`) and *recommended* the rest for
STEP-51. The paths this prompt originally listed (`lib/tracking.dart`, `lib/data_bucket.dart`, …)
never existed at the top level — the audit's greps hit **basename noise** (e.g.
`features/benchmark/domain/entities/benchmark.dart` for "benchmark.dart"), the same trap 48.30
itself documented. All the real files still exist on the branch head. The authoritative
candidate list is 51.1's findings §5 (exact-path verified, basename-noise-proof). Read the PLAN
(decision D6, as corrected) and **51.1's findings** before anything else.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (decision D6, definition of done)
- `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` (dead-file section + new-file sweep)
- Root `.throughstone/local-user.md`
- `prompts/003-release-readiness-integration-scale/step-0048/mine-flow-STEP-48.30-FINDINGS.md`
  (what 48.30 claimed it deleted)
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** verification of the 7 deletions; the disposition record; disposition of any new
unreferenced `lib/` files 51.1's sweep found (delete/keep-with-reason/wire).

**Does NOT touch:** any referenced file; anything outside `lib/`; `test/`.

## Your task

1. **Verify the true candidate list on the branch head** (from 51.1's findings §5, not from
   memory): the 3 dead feature barrels (`lib/features/tracking/tracking.dart`,
   `lib/features/benchmark/benchmark.dart`, `lib/features/data_bucket/data_bucket.dart`),
   their 4 barrel-twin files (`features/tracking/data/data.dart`,
   `features/tracking/domain/domain.dart`, `features/data_bucket/data/data.dart`,
   `features/data_bucket/domain/domain.dart`), the duplicate never-registered
   `GeospatialFileModelAdapter`
   (`lib/features/data_bucket/data/models/hive/geospatial_file_hive_adapter.dart` — typeId 13
   duplicate of the registered core typeId 7 adapter in
   `lib/core/offline/adapters/model_adapters.dart`; never registered in `hive_service.dart`),
   `lib/app/presentation/models/app_nav_model.dart` (unreferenced since STEP-30.1; the shell
   defines its own `_SidebarItemConfig`/`_SidebarSection`), and the two product-intent widgets
   (`lib/features/notifications/presentation/widgets/notification_badge.dart`,
   `lib/features/reporting/presentation/widgets/report_type_card.dart` — 48.30 parked these as
   an owner decision: **ask the user** whether the notifications feature plans to use the
   badge; default delete if not). For each: re-verify zero references with an exact-path
   `^(import|export|part)` grep (basename grep over-matches — see 51.1 §2 trap notes), delete
   with `git rm`, record the disposition. **The duplicate adapter is data-integrity-shaped:
   escalate to the user/Opus if deleting it changes any Hive registration state; the
   registered one is the core typeId 7 adapter, and `hive_service.dart` must be untouched.**
   Also remove the two stale 48.30-deleted entries from
   `tool/check_l10n_baseline.dart`'s `_legacyExemptFiles` (`:86–87`) — one-line cleanup in
   this lane (guard output should drop 46→44 exempt).
2. **Sweep for any new unreferenced files** (51.1's list was branch-head fresh on 2026-09-09;
   51.2–51.6's edits may have added or orphaned files since): delete, keep-with-reason, or
   wire up — each with a one-line reason in findings. A file whose exact path appears in zero
   `(import|export|part)` statements across `lib/`, `test/`, `integration_test/`, and
   `main.dart` is unreferenced.
3. **Confirm no shadowing duplicates were reintroduced** by 51.2–51.6's edits (two files
   claiming the same import path — the original defect class 48.30 fixed).
4. **Record** all dispositions in `Upcoming Prompts/mine-flow-STEP-51.9-FINDINGS.md` —
   this is the record 51.10 checks the close checklist against.

## Verification

- Every dispositioned file either absent from disk with zero exact-path references, or
  kept with a recorded reason.
- Any new unreferenced file dispositioned with a reason.
- `flutter analyze` → 0; `flutter test` → green with the delta stated (deletions should not
  change the count unless an orphaned test existed).
- If you deleted files: `dart format --set-exit-if-changed` clean after, and
  `dart run tool/check_l10n_baseline.dart` still `[OK]`.

## Keeping the docs true

Dispositions are recorded in findings for 51.10 to fold into the register appendix / close
record. No architecture doc changes (deleting dead files changes nothing the docs describe
— if a doc *does* reference a deleted file, that's a docs-true defect: report it, escalate
rather than editing the architecture doc silently).

## Definition of done

- [ ] Every file on 51.1's §5 list dispositioned: deleted with zero exact-path references, or
      kept with an owner-confirmed reason.
- [ ] New unreferenced files dispositioned with reasons.
- [ ] No shadowing duplicates.
- [ ] `flutter analyze` 0, `flutter test` green with count stated, l10n guard `[OK]`.
- [ ] Findings `Upcoming Prompts/mine-flow-STEP-51.9-FINDINGS.md`; PLAN row updated.

## Escalation (to Opus 4.8 — record in findings if fired)

- Deleting the duplicate `GeospatialFileModelAdapter` would change any Hive registration
  state, or `hive_service.dart`'s registration list does not match 51.1's description
  (data-integrity-shaped — do not improvise).
- A doc or config referencing a deleted file.
- Any file you cannot classify as dead vs load-bearing.

## Next

Tell the user: *"run substep 51.10"* (verification & close, Opus 4.8) — in a **fresh chat**.
