# mine-flow — STEP-55.9 RESIDUAL: verify-and-record after the residual lane + honest Drive deferral

> **How to run:** Tell your agent "run 55.9 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** Same tier as 55.9 — a bounded verify-and-record pass with mechanical gates; it owns no new product/data policy.

## Why this exists (audit 2026-09-21, do-not-trust-status pass)

55.9 is the **strongest** of the 55.8–55.11 set: index row already reads **Done**, code is on disk (`89077bf`), and the FINDINGS document 90 passing tests with a real per-file breakdown. The residual is therefore **thin** — this is a confirmation pass, not a rebuild — but two things must be reconciled honestly before the STEP can close:

Audit facts, verified on `step-0055-cohesive-ui-rebuild`:
- Routes `/tools/data-bucket`, `/tools/data-bucket/upload`, `/tools/data-bucket/:id` present in `lib/app/router.dart`.
- Files present: `upload_file_page.dart`, `file_detail_page.dart`, `file_detail_route.dart`, `data_bucket_list_page.dart`, `data_bucket_upload_cubit.dart`, `google_drive_service.dart`, timeline `milestone_card.dart`/`timeline_page.dart`.
- `flutter analyze` exit 0 across the whole project (includes data_bucket/timeline).
- The 55.9 FINDINGS' only stated Unverified is **live Google Drive service-account token exchange + multi-GB chunk interruption** — deliberately mocked per spec ("mock Drive externally; never transmit real files in unit tests").

**What must be reconciled:**
1. The shared primitives 55.9 depends on (`AppResponsiveSheet`, `AppCalendarDialog`, `AppStatePanel`, dirty-dismiss) are being **modified right now by the uncommitted 55.1/55.2/55.3 residual lane** (`app_interaction_primitives.dart`, +137 lines). A change there can silently regress the data-bucket sheet/inspector geometry and dirty guard. 55.9's green result predates that dirty lane, so it must be **re-measured on the current tree**.
2. The live-Drive deferral is legitimate but must be carried as an explicit `Unverified` in the durable record, not silently dropped by a close report.

## Residual scope (exact — nothing else)

1. **Re-run the full 55.9 test set on the current tree** and record counts: the data-bucket cubit/list/detail/upload suites, the repository/BLoC suites, and the timeline page/milestone-card suites (the FINDINGS §3.1 lists all six groups, ~90 tests). Confirm still 0 failures / 0 unexpected skips.
2. **Regression check against the residual lane.** After the 55.1/55.2/55.3 residual lane commits (or if it is still dirty, on the current worktree), re-assert data-bucket upload-sheet dirty-dismiss + file-detail inspector geometry still behave — these ride on `app_interaction_primitives.dart`. If a primitive change broke them, that is a **regression to route back to the primitive owner**, not a 55.9 rewrite.
3. **Record the live-Drive deferral** as an explicit `Unverified` line in a dated "Residual (55.9)" section of `mine-flow-STEP-55.9-FINDINGS.md`, cross-referencing RISK-0017 (orphan cleanup) and RISK-0018 (50MB OOM cap, already closed). Do not overwrite the original section.
4. Confirm Timeline and Data Bucket remain **report-free** (no contextual report dialog leaked in from the 55.1 reporting-dialog residual lane) and Timeline remains **read-only** (no create route/FAB).

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md`; `mine-flow-STEP-55.9-PROMPT.md`; `mine-flow-STEP-55.9-FINDINGS.md`
- Master spec §4.8; `registries/risks.yml` RISK-0017, RISK-0018
- `lib/features/data_bucket/**`, `lib/features/timeline/**`, `lib/core/network/google_drive_service.dart`, `lib/core/presentation/widgets/app_interaction_primitives.dart` (read-only — you do not own it), `lib/app/router.dart` (data-bucket routes only)

## Pre-flight (do not skip)

1. `git -C Code/mine-flow-app status --short --branch`. The worktree carries an uncommitted 55.1/55.2/55.3 residual lane + untracked scratch. **Preserve it; do not stage/reset/stash/absorb.** This residual should ideally add **no code** — it is verify-and-record. If a genuine data-bucket regression is found, fix only data-bucket files in a `fix(55.9): ...` commit with staged-index proof.
2. Serialize behind the 55.1/55.2/55.3 residual lane if it is still in flight — both touch shared primitives.

## Ownership boundary

- ALLOWED: `mine-flow-STEP-55.9-FINDINGS.md` (append dated section); data-bucket/timeline `lib/` + tests **only if** a regression is proven.
- FORBIDDEN: `app_interaction_primitives.dart` edits (read-only; route regressions to its owner), reporting dialog, other features, `STEP-index.md`.

## Tests and verification

- `flutter test test/features/data_bucket/ test/features/timeline/`
- `flutter analyze` (expect 0). Record exact commands + counts.

## Boundaries and escalation

No live Drive transmission in unit tests, no new report on Data Bucket/Timeline, no Timeline write path, no primitive edits. Escalate if a shared-primitive change broke the data-bucket sheet (hand to primitive owner) or if two fix attempts fail.

## Definition of done

Full 55.9 suite re-measured green on the current tree; data-bucket sheet/inspector confirmed intact against the primitive residual lane; live-Drive deferral recorded as explicit `Unverified`; report-free + read-only invariants confirmed; FINDINGS has a dated "Residual (55.9)" section.

## Next

Report whether STEP-index row 55.9 stays **Done** as-is (likely yes) with the live-Drive `Unverified` carried, and hand off to the 55.11 close residual. Do not alter the index yourself.
