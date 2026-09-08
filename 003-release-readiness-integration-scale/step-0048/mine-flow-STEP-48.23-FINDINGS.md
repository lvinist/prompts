# mine-flow — STEP-48.23 Findings — Re-run 5 (R-1, 2026-09-05)

**Date:** 2026-09-05
**Executor:** Hermes / Claude Opus 4.8 (this session)
**Branch:** `step-0048-runtime-evidence` (local HEAD = `c73a00e` = `origin/step-0048-runtime-evidence`, tree clean at session start, fsck clean)
**Mandate:** PLAN amendment 2026-09-05 (48.26 gate-5 re-run 4, run [`33953949570`](https://github.com/lvinist/mine-flow-app/actions/runs/33953949570), sha `c73a00e`) — **R-1**: web daily-log `:136` read-back `Expected: LogStatus:<LogStatus.submitted> / Actual: LogStatus:<LogStatus.draft>`. Classified by 48.26 re-run 4 as **app defect (concurrency) + a test-hardening half — NOT a flake and NOT a regression** (`git diff --stat 9288168..c73a00e -- lib/` empty). The run also counts as failure B's deliberate re-assertion (fired red on web). Re-run order: 48.23 → 48.24 → 48.25 → 48.26. This pass's record replaces the 2026-09-04 R-1 re-run as the current record; prior records (first pass 2026-08-31; gate-evidence amendments 2026-09-02/03/04; the 2026-09-04 R-1 re-run) are preserved in the PLAN's progress row and in the PLAN/FINDINGS history.

---

## Verdict

| Item | Classification | Outcome |
|---|---|---|
| **R-1** — web daily-log `:136` autosave-vs-submit race | **App defect (concurrency)**, exactly per 48.26 re-run 4's source derivation | **Fixed** — two-layer fix: (1) `autoSaveDraft` never demotes a cached non-draft row (persistence contract, closes every dispatcher); (2) the bloc drops `AutoSaveDraftEvent` while `isSubmitting`/`isSubmitted` (closes every path at the bloc). 3 concurrency pins added (2 repository-tier, 1 bloc-tier), all demonstrated fail-shape-true on the unfixed tree |
| Failure B (`Deferred` since first pass) | This gate **was** the deliberate re-assertion | Write path + read-back now fixed and verified: submit → `submitted` holds on web (2× drive pass), pinned below E2E |

**Zero regressions:** no assertion removed or loosened — the journey `:136` expect is byte-identical to HEAD (`git diff` empty on the journey file); full suite **508/508** on the fix tree (505 baseline + 3 new pins; one order-dependent `SyncQueueManager` drain-timing flake failed once, passed isolated and on full re-run — §4). No staging mutation beyond the journeys' own pre-clean/tidy rows.

## §1 Fix choice (register offered three non-equivalent candidates — this pass took two)

1. **Persistence contract — the register's "strongest" (option C): `autoSaveDraft` refuses to demote a non-draft row** (`daily_log_repository_impl.dart:120-149`). When the row is already cached, the stored status is `max(incoming, cached)`; a late autosave persists its FIELD edits without touching status; with **no cached row the legacy force-draft is kept** (the submit flow's own first write is transiently draft and immediately promoted — and a get→put pair here has no `await` between them, so a null read cannot interleave with a concurrent submit's promotion). This keeps the first-pass failure-B write-path pin (`test/unit/daily_log_repository_test.dart:203`) valid **unmodified**.
2. **Bloc guard — option B: drop the autosave while a submit is in flight** (`daily_log_bloc.dart:195-204`): `if (currentState.isSubmitting || currentState.isSubmitted) return;` — the first-pass guard checked only `log.status != draft`, which the mid-submit autosave passed because the submit handler holds a pre-submit draft in state across its two awaits.
3. **Not taken — option A (cancel the debounce timer in the widget):** fixes only this widget, couples persistence to UI lifecycle, and is redundant under 1+2 (any other late dispatcher — e.g. the zone/weather pickers' direct `AutoSaveDraftEvent` dispatches — is already closed by the repo contract + bloc guard).

**Doc 04 note (register-mandated, since this changes the persistence contract):** `Code/mine-flow-docs/architecture/04-data-model.md` §5 "Client write-path status contract (daily_logs)" + Version Log **v0.1.7** (header version and Last-updated reconciled; the header was stale at v0.1.5 from 48.20).

## §2 Mechanism (confirmed in source; matches the register's derivation line-for-line)

- `_debouncedAutoSave()` arms a 500 ms `Timer` (`daily_log_form_screen.dart:95-101`) that the submit button never cancels (`:389-405`); zone/weather pickers also dispatch `AutoSaveDraftEvent` **directly** (`:298-300`, `:313-315`) — so the register's debounce-only framing was conservative.
- bloc 9.2.1 processes events **concurrently by default**; `DailyLogBloc`'s constructor (`daily_log_bloc.dart:17-28`) registers no transformer.
- `_onAutoSaveDraft` guarded only on `status != draft` (`:194`); `_onSubmitDailyLog` holds the log at `draft` in state across `autoSaveDraft(promoted)` + `submitDailyLog(id)` (`:242-248`).
- `autoSaveDraft` force-wrote `status: draft` (`daily_log_repository_impl.dart:123`) → the late autosave overwrote the promoted row at the cache AND enqueued a `draft` payload that wins LWW at the drain → `:136` read `draft`.

## §3 RED→GREEN (honest evidence, three pins)

**RED (unfixed tree `c73a00e`):**

| Pin | Command | Result |
|---|---|---|
| Repo pin 1 (`daily_log_repository_test.dart:285`) | `flutter test test/unit/daily_log_repository_test.dart --plain-name 'STEP-48.23 re-run 5'` | `Expected: 'submitted' / Actual: 'draft'` at `:285` — **the CI signature reproduced at repository tier**, exit 1 |
| Repo pin 2 (`:304`) | `flutter test test/unit/daily_log_repository_test.dart --plain-name 'persists field edits without demotion'` | same signature at `:304`, exit 1 |
| Bloc pin (`daily_log_bloc_test.dart`) | `flutter test test/features/daily_log/presentation/daily_log_bloc_test.dart` | emission order proved concurrent processing: `[isSubmitting] → [isSavingDraft:true 'Menyimpan draft...'] → [isSaved:true 'Draft tersimpan otomatis'] → [submitted]`; and `verifyNever(autoSaveDraft(draft-entity))` unmet — exit 1 |

**GREEN (fix applied):** repo suite **12/12** (exit 0; the pre-existing failure-B pin at `:203` passes unmodified); bloc pin **1/1** (exit 0); all four daily-log touched suites **28/28**; **full `flutter test`: 508 passed / 0 failed** (exit 0).

## §4 Full-suite flake (classified, not hidden)

Run 1: `507 +1 — Some tests failed` — `attendance_daily_log_sync_test.dart` "Timestamp conflict resolution during offline queue sync processing". Classification: **order-dependent timing flake (the documented `SyncQueueManager` drain class), not a regression** — (1) the test body (`:239-296`) exercises only `SyncQueueManager` + attendance DTOs behind a 100 ms drain-timing wait; the daily-log repository/bloc are imported but not on its execution path; (2) isolated re-run 3/3 pass; (3) full-suite re-run **508/508** exit 0. Matches the §6 flaky-vs-regression disambiguation (isolated pass + full re-run pass; no assertion touched).

## §5 Web verification (register: "must verify on web")

CI-exact per-file invocation (`ci.yml:158-181` shape), secrets via `--dart-define-from-file=.env` (never printed), `--dart-define=APP_ENV=staging`, chromedriver on `:4444`:

- **Run 1: PASS** — `result {"result":"true","failureDetails":[]}` / `All tests passed.` (`step4823_r5_web_daily_log.log`)
- **Run 2: PASS** — same command, same bytes (`step4823_r5_web_daily_log_run2.log`)

Two consecutive web passes on the fix tree at the exact assertion history shows red ~50% of the time; the journey file is byte-identical to HEAD, so this is the fix, not a test change. Android not re-run here: the defect's actual has appeared in **0** Android logs of the wave, and the full local suite (which includes the same write paths at unit/integration tiers) is green — final proof is 48.26's next gate.

## §6 Sweep

48.26 re-run 4's sweep is already complete and re-checked here: of 4 `Timer(const Duration(milliseconds` debounce sites in `lib/`, only daily-log's dispatches a **write** event; **zero** handlers anywhere guard on `isSubmitting` (4 blocs carry the flag); the only status-forcing repository write was `daily_log_repository_impl.dart:123` — now guarded. The attendance analog is structurally immune (attendance writes flow through `setAttendanceForDate` upserts, no draft-forcing path). No other file needed the contract.

## §7 Files changed (uncommitted — commit is 48.25's lane)

1. `lib/features/daily_log/data/repositories/daily_log_repository_impl.dart` — never-demote contract (+26/−1 payload lines; file is CRLF at HEAD, churn preserved at 0 net)
2. `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart` — mid-submit autosave guard (+9/−0 payload lines; worktree CRLF checkout artifact normalized back to LF before staging — raw diff read 337/328 until normalized, per the line-ending-churn-audits protocol)
3. `test/unit/daily_log_repository_test.dart` — 2 concurrency pins (+66)
4. `test/features/daily_log/presentation/daily_log_bloc_test.dart` — NEW, 1 bloc concurrency pin (bloc_test/mocktail house style)
5. `Code/mine-flow-docs/architecture/04-data-model.md` — §5 contract note + Version Log v0.1.7 (+2 lines) — **docs repo, NOT `mine-flow-app`** (48.25's commit list must not sweep it in)

**Not committed by this substep** (re-run order: 48.24 → 48.25 → 48.26); `run_web_wrapper.dart` is this pass's scratch — **48.25 must not commit it** (delete or leave untracked; note: 48.24's hand-forward list for 48.25 already names this file as CI-loop residue, but on this tree it is *this session's* scratch — same disposition).

## §8 Handoffs

- **48.24:** re-run per the strengthened procedural rule (re-parse gate logs; never dismiss a red as flake when its mechanism is reachable in source). Local full suite on this tree: 508/508 (baseline shifts 505 → 508 with this pass's 3 pins).
- **48.25:** commit the 4 app files of §7 (specific-file staging, `core.autocrlf=false` already set); the bloc file's CRLF worktree artifact is already normalized (raw = payload 9/0); do **not** commit `run_web_wrapper.dart`; the Doc 04 edit lives in the **docs repo** — commit/push it there as the substep's doc lane.
- **48.26:** expect the next gate's web daily-log to pass; if the `:136` actual ever returns, the two-layer contract means the race now has to defeat BOTH the bloc guard AND the never-demote store — treat that as a new defect, not this one re-fired.
- **48.15:** Doc 04 §5 note is written; no other doc reconciliation triggered by this fix.

## §9 Honesty ledger

- Web passes: 2/2 on the fix tree (local Chrome, chromedriver 152.0.7977.64) — CI's runner is not byte-identical hardware; final proof is the next branch-head gate (48.26's lane).
- The full-suite flake failed once and passed twice (isolated + full re-run); recorded, not hidden.
- `.env` values never printed; staging touched only by the two journey runs' own writes.
- Assertion counts: daily-log repo suite 10 → 12; bloc suite 0 → 1; offline-sync journey untouched at 36.
