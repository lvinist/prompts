# mine-flow — STEP-48.25: `mine-flow-app` Git Object-Store Repair & Wave Commit

> **How to run:** tell your agent *"run substep 48.25"*. Self-contained — runnable cold.

**Assigned model: Hermes / Claude Opus 4.8.** This substep is destructive-adjacent: it moves a
developer's only local repository through a re-clone and reconstructs lost history from the working
tree. Getting it wrong loses uncommitted work (48.20–48.23) or fabricates a history that does not
match what the files actually say. The deliverable is a **verifiably clean git object store on
`step-0048-runtime-evidence`, containing every remediation change as honest commits, byte-verified
against the working tree** — and the judgement about what is real work vs. line-ending churn. That is
why it is Opus. **Escalate to the user** before any irreversible step (see the safety boundary).

## Why this substep exists

48.23 discovered — and 48.24 confirmed at the gate check — that the `mine-flow-app` **git object
store is corrupt at the filesystem level**, not a code problem:

- `.git/objects/pack/pack-52610b3e4e04e3afef5b79a8bdc41b21371507a7.idx` reports
  `wrong index v2 file size`; the matching `.pack` has a bad object at offset **120923**
  (`inflate returned -5`) and cannot be opened or reindexed.
- `git fsck` finds **~30 corrupt loose objects** (`inflate: data stream error`).
- Refs point into the dead pack: `step-0042-staging-pipeline`, `refs/stash`, several
  `archive/*` tags, and — critically — the **tree objects behind the two unpushed commits**
  48.18 `09e4821` and 48.19 `d143167`.
- Consequence: **every `git add`/`commit` fails** (`error building trees`,
  `invalid object … for 'assets/fonts/Geist-Bold.ttf'`), and the working copy of
  `supabase/types/database.ts` was **deleted from disk** (its blob lives only in the dead pack), so
  the contract-guard test fails until it is restored.

This blocks committing the entire remediation wave (48.18–48.23). It is sequenced here, **after
48.24's local test evidence and before 48.26's CI run**, because CI can only run against a pushed,
committed, healthy tree.

## The situation is recoverable without data loss — this is established, not assumed

48.23 verified all of the following on disk; re-verify them yourself before acting:

- **The working tree is fully intact.** Every 48.18/48.19/48.20/48.22/48.23 change is present as real
  files on disk (e.g. `timeline_remote_datasource.dart` already queries `measured_at`/`cleared_at`;
  `inventory_item_model.dart` writes only `name`; the four 48.23 files exist). The corruption is in
  `.git/objects`, not the working tree.
- **`origin` is healthy.** `origin/step-0048-runtime-evidence` = `469b2bc…` is a good, fetchable tip;
  the repo's default branch is `master`.
- **Only two commits are unpushed** (`09e4821` 48.18, `d143167` 48.19). Their commit objects read but
  their **tree** objects are corrupt — so they cannot be salvaged as commits (`format-patch`,
  `cherry-pick`, `diff-tree` all fail with `unable to read tree`). **Their file content is in the
  working tree**, so re-committing loses only the original SHAs/timestamps, nothing substantive.
- **The "391 dirty files" is mostly noise.** `core.autocrlf=true` with no `.gitattributes` makes git
  report ~388 files as modified for **LF→CRLF line-ending churn only** (binaries like the Geist fonts
  and files nobody edited, like `LICENSE`, show as modified). The real edits are a small subset.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, the honesty rule, and the
  merge order (`app → docs → prompts`).
- **`Upcoming Prompts/mine-flow-STEP-48.24-FINDINGS.md`** — which changes are uncommitted-on-disk,
  whether any real regression was found (a regression must be fixed by its owning substep *before*
  this commit, so the repaired history is right in one pass), and whether
  `supabase/types/database.ts` was present at 48.24 time.
- **`…-48.16-` through `…-48.23-FINDINGS.md`** — the per-substep change inventory. You will reconstruct
  the commit sequence from these, so you must know what each substep touched.
- `Code/mine-flow-app/.env.example` — the shape of the secret-bearing `.env` you must preserve (never
  read or print its values).
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.

## Non-negotiable safety boundary

- **Back up first, and never delete the corrupt repo until the fresh one is proven good.** The corrupt
  folder is the only copy of the uncommitted work; treat it as irreplaceable until byte-verified.
- **Do not `push --force`.** `origin` is healthy; you are fast-forwarding it, not rewriting it.
- **Never read, print, move-by-cat, or commit `.env` / `.secrets/`.** Copy them as opaque files only.
  Reference secrets by name. `.env` must survive the migration (the app needs it locally) but must not
  be staged (it is gitignored — confirm `.gitignore` still ignores it in the fresh clone).
- **Confirm with the user before the irreversible cutover** (repointing the workspace/project at the
  fresh clone and retiring the corrupt one). Everything up to that point is additive and reversible.
- Do **not** attempt in-place repair (`git gc`, `repack`, `index-pack`, `unpack-objects`, deleting the
  pack). 48.23 proved reindex dies on the bad object and fsck cannot rebuild unreadable loose objects;
  fighting it risks losing more. The re-clone path is the recommendation of record.

## Recommended approach — fresh clone + working-tree replay

This is the analysis 48.23 handed forward. Adapt paths to the workspace; do each step, verify, then
proceed.

### 1. Snapshot the corrupt repo (reversible safety net)

Copy `Code/mine-flow-app` to a sibling backup **including `.git`**, e.g.
`Code/mine-flow-app.corrupt-bak-<date>`. This is the rollback if anything downstream goes wrong. Use a
copy that preserves everything (robocopy `/E`, or a plain recursive copy); do not use git for this.

### 2. Inventory what must be preserved from the working tree

Before cloning, enumerate — from disk, not from git — exactly what the fresh clone must receive:

- The real source edits of 48.18–48.23. Derive the candidate list from the findings files, then
  confirm each file exists on disk. Known highlights (verify, do not trust this list blindly):
  - 48.18: `lib/features/timeline/data/datasources/timeline_remote_datasource.dart`,
    `lib/features/reporting/data/datasources/reporting_remote_datasource.dart` (+ its unit test).
  - 48.19: `lib/features/tracking/data/models/inventory_item_model.dart`,
    `lib/features/equipment_check/data/models/equipment_check_dto.dart`,
    `lib/features/tracking/data/models/land_clearing_model.dart` (+ tests).
  - 48.20: `supabase/seed.sql` (and any RLS/fixture files it names).
  - 48.22: `lib/features/timeline/presentation/pages/timeline_page.dart`, the cut/fill dropdown
    file, `upload_file_page.dart`, the Android screenshot-capture guard (+ tests).
  - 48.23: `integration_test/journeys/attendance_journey_test.dart`,
    `integration_test/journeys/offline_sync_journey_test.dart`,
    `test/unit/attendance_repository_test.dart`, `test/unit/daily_log_repository_test.dart`.
- **`.env`** (opaque, do not read).
- Any **untracked** files worth keeping (48.24 counted 2 untracked in the corrupt repo — decide with
  the user whether they belong).
- **Do NOT copy** `.git/`, `build/`, `.dart_tool/`, `.pub-cache`, or generated caches.

### 3. Fresh clone beside the corrupt repo

Clone `https://github.com/lvinist/mine-flow-app.git` to a new folder (e.g. `mine-flow-app-fresh`),
then `git checkout step-0048-runtime-evidence` (lands at the healthy `469b2bc`). Run `git fsck
--full` — it must be **clean**. Confirm `supabase/types/database.ts` is present here (it is committed
at `469b2bc` — this is how the deleted artifact is recovered).

### 4. Kill the CRLF churn before staging

In the fresh clone, set `git config core.autocrlf false` **and/or** add a `.gitattributes` that pins
line endings (`* text=auto eol=lf` is the usual choice for a Flutter repo; confirm against how the
team's existing files are stored — the repo currently has none, which is the root of the 388-file
noise). Do this **before** copying files in, so `git status` shows only real edits, not line-ending
diffs. If you add `.gitattributes`, that is itself a legitimate small commit — call it out.

### 5. Overlay the working-tree changes

Copy the preserved source files (step 2) from the corrupt repo's working tree into the fresh clone,
**excluding `.git`, `build`, `.dart_tool`**. `robocopy <src> <dst> /E /XD .git build .dart_tool
.pub-cache /XF` (list any file to skip) is the safe Windows tool; verify the copy count. Then in the
fresh clone, `git status` must now show a **small, sane** diff — the real edits only.

### 6. Reconstruct the history as honest commits

Recreate the two lost commits and the uncommitted work from the working-tree content, in
substep order, so the history matches the STEP-48 record and each commit is reviewable:

1. 48.18 — datasource column-name reconciliation.
2. 48.19 — write-path dual-key purge.
3. 48.20 — staging fixture & seed alignment (if it had uncommitted disk state).
4. 48.22 — UI/harness defect fixes.
5. 48.23 — persistence/offline-integrity (the four files above) with the message 48.23's findings
   specified:
   `STEP-48.23: persistence/offline-integrity — fix attendance read-back target, scope offline Part A to Android (Doc 15 §1), pin status write paths`.

Stage **specific files**, never `git add .` (that re-imports churn). Preserve author identity; do not
touch `git config` user settings. Do not `--amend` anything on `origin`.

### 7. Byte-verify the reconstruction against the working tree

For every file you committed, prove the committed blob equals the corrupt repo's working-tree file:

```bash
git -C <fresh> show HEAD:<path> | cmp - <corrupt-repo>/<path> && echo "IDENTICAL: <path>"
```

Any mismatch means a copy or line-ending slip — fix before proceeding. Also `git fsck --full` clean,
and `git log --oneline origin/step-0048-runtime-evidence..HEAD` shows exactly your new commits.

### 8. Verify the build, then push

In the fresh clone (`PUB_CACHE=D:/AppDev/.pub-cache`): `flutter pub get`, `flutter analyze` (0),
`dart format --set-exit-if-changed .` (clean), `dart run tool/check_supabase_contracts.dart` (0 — the
restored `database.ts` makes this pass again), and `flutter test` (reconcile against 48.24's count).
Only then `git push origin step-0048-runtime-evidence` — a **fast-forward**, no force. Confirm the
push updated the remote tip.

### 9. Cutover (only after user confirmation)

With the user's explicit go-ahead: repoint the workspace/project at the fresh clone (the Throughstone
`registries/repos.yml` path and any local pointer), and retire the corrupt repo to the backup name.
Keep the backup until 48.26's CI run is green — it is the last rollback.

## Escalation and honesty

- If `git fsck` on the **fresh clone** is not clean, stop — the remote itself is damaged, which is a
  different and larger problem; escalate to the user.
- If a byte-verify mismatch cannot be explained by line endings, stop and diagnose before committing —
  do not commit a file you cannot prove matches the working tree.
- If 48.24 reported a real regression (not a flake, not git), that fix must land **before** step 6 so
  the reconstructed history is correct; name it and route it rather than committing broken code.
- If any step would be irreversible and you are unsure, ask the user rather than proceeding.

## Verification

- Corrupt repo backed up before any change; backup path recorded.
- Fresh clone `git fsck --full` clean; `supabase/types/database.ts` present.
- CRLF churn eliminated (autocrlf off and/or `.gitattributes`); `git status` shows only real edits.
- Every remediation change re-committed in substep order with honest messages; no `git add .`.
- Every committed file byte-verified (`git show HEAD:<path> | cmp -`) against the corrupt repo's
  working tree; results recorded.
- `flutter analyze` 0, `dart format` clean, contract guard 0, `flutter test` reconciled to 48.24.
- Pushed to `origin/step-0048-runtime-evidence` as a fast-forward (no force); new remote tip recorded.
- Cutover done only after explicit user confirmation; backup retained until 48.26 is green.
- No `.env` value read, printed, or committed; `.env` preserved and still gitignored.

## Scope

**In scope:** backing up, re-cloning, eliminating line-ending churn, replaying the working-tree
changes as honest commits, byte-verifying them, running the local gates, pushing the fast-forward, and
(after confirmation) the cutover.

**Not in scope:** fixing application defects (they belong to 48.16–48.23 — a real regression must be
routed and fixed before the commit), running CI (48.26), editing architecture docs / `risks.yml` /
`prompts/STEP-index.md`, and closing STEP-48 (48.15).

## Definition of done

- [ ] Corrupt repo backed up; path recorded; nothing irreversible done before user confirmation.
- [ ] Fresh clone created, `fsck` clean, on `step-0048-runtime-evidence`, `database.ts` present.
- [ ] Line-ending churn eliminated; `git status` shows only genuine edits.
- [ ] 48.18–48.23 changes re-committed in order, specific-file staging, honest messages.
- [ ] Every committed file byte-verified against the working tree; evidence recorded.
- [ ] Local gates pass (analyze 0, format clean, contract guard 0, test count reconciled).
- [ ] Fast-forward push to origin; new tip sha recorded; no force push.
- [ ] Cutover completed after user confirmation; backup retained until 48.26 green.
- [ ] No secret read/printed/committed; `.env` preserved and ignored.
- [ ] `mine-flow-STEP-48.25-FINDINGS.md` written; PLAN progress table updated.

## Next

Tell the user the next action is **"run substep 48.26"** (branch-head CI gate run & verdict) in a
**fresh chat**, and hand it the pushed head sha. STEP-48 remains `In progress`; Phase 4 stays shut
until 48.26 is GO and 48.15 closes.
