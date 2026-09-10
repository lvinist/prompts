# mine-flow — STEP-54.0: Pre-flight — STEP-53 Merge Reconciliation & Clean Trunk

> **How to run:** Tell your agent *"run substep 54.0"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Hermes/Claude Opus 4.8.** This substep touches shared-trunk git state a prior STEP left inconsistent (STEP-53 recorded Done with unmerged branches); misclassifying the unmerged ledgers silently corrupts trunk, so it sits in the top tier.

## Context

STEP-53 (Dependency Maintenance) is recorded **Done** in `prompts/STEP-index.md` and archived, but its work was never merged to the trunks. This substep reconciles that, proves the merged trunk is green, then cuts the STEP-54 branch. It is the gate for the entire STEP — nothing else in STEP-54 branches or writes until this is clean.

This is the only substep in STEP-54 that runs the app's test suite (as a merge-regression guard); 54.1–54.11 are read-only critiques and spec-writing.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — the STEP PLAN, especially **Pre-flight** and **Evidence standard**
- `prompts/STEP-index.md` — STEP-53 row (Done) and STEP-54 row (Planned)
- `prompts/003-release-readiness-integration-scale/step-0053/mine-flow-STEP-53.4-FINDINGS.md` — the close findings claiming "ready for closure" (the claim this substep makes true)
- `Code/mine-flow-app/README.md` — build/test prerequisites (PUB_CACHE, JDK 17, Flutter ≥ 3.47.1)
- root `.throughstone/local-user.md` — calibrate any user-facing questions

## Expected state (verified at planning time, 2026-09-10 — re-verify before acting)

- `Code/mine-flow-app`: on branch `step-0053-dependency-maintenance`, HEAD `fe12531` ("chore(STEP-53.3): upgrade direct deps within declared ranges; fix lengthSync"); local `master` = `be44843` (STEP-52 ci wiring) = `origin/master` (0/0 divergence); working tree clean except untracked `.step53-logs/` (evidence logs from 53.x: analyze.log, flutter-doctor.log, results.txt, etc.).
- `Code/mine-flow-docs`: on branch `step-0053-dependency-maintenance`, HEAD `891ce66` ("docs(STEP-53.1-53.3): update RISK-0007, RISK-0009, RISK-0020 from 53.x findings"); `main` = `ce52c77` = `origin/main`; clean tree.
- `prompts`: on `main`, synchronized with `origin/main`, clean.

**Resume note (2026-09-10):** The user chose to merge only the originally recorded STEP-53
heads (`fe12531` app, `891ce66` docs). The later correction commits (`226aa00`, `30b0b06`)
were preserved on local `step-0053-post-close-corrections` backup branches and were not merged.
The `.step53-logs/` directory was archived under
`Code/mine-flow-docs/reports/test-results/2026-09-10-step-0053-evidence/`.

**If the state you find differs materially** (extra unmerged commits, remote divergence, dirty tracked files, the branches already merged), STOP and escalate to the user with the actual state — do not improvise. This is a named escalation trigger in the PLAN.

## Scope

**Owns:** merging `step-0053-dependency-maintenance` → `master` (app) and → `main` (docs); pushing both trunks; deleting the merged local branches; disposition of `.step53-logs/`; the merge-regression verification run; cutting `step-0054-feature-cohesion-critique` in app + docs; flipping the STEP-54 index row to `In progress` and pushing that flip to `prompts/main`.

**Does NOT touch:** `prompts/` history (no rewrites), any file under `Code/mine-flow-app/lib/**`, remote step branches (none exist for step-0053), or anything STEP-54's critique substeps own.

## Your task

1. **Re-verify the expected state above** in all three repos (branch, HEAD sha, trunk position, dirty files). Record actual shas.
2. **Merge** in the app repo: fast-forward `master` to the user-selected recorded head `fe12531`, push `master` to `origin`, and delete the original local `step-0053-dependency-maintenance` branch. Preserve later correction `226aa00` on the explicit backup branch `step-0053-post-close-corrections`.
3. **Merge** in the docs repo: fast-forward `main` to the user-selected recorded head `891ce66`, push `main`, and delete the original local `step-0053-dependency-maintenance` branch. Preserve later correction `30b0b06` on the explicit backup branch `step-0053-post-close-corrections`.
4. **`.step53-logs/` disposition:** The user chose archive. Move the logs into `Code/mine-flow-docs/reports/test-results/2026-09-10-step-0053-evidence/`, commit, push, and record the resulting docs commit.
5. **Merge-regression run** in the app repo on merged `master`: `flutter analyze` (expect 0 issues), `dart format --output=none --set-exit-if-changed .` (expect 0 changed), `flutter test` (expect **550/550** — the count 53.4 verified pre-merge). If the count differs, investigate before proceeding; a different count is not necessarily a failure (the merge could be fine and the count legitimately moved) but must be explained with evidence. Redirect output to files, never read a piped exit code.
6. **Cut the STEP-54 branch** in both `Code/mine-flow-app` and `Code/mine-flow-docs`: `git switch -c step-0054-feature-cohesion-critique` (from the freshly merged trunks). Do not push the step branch unless the project's convention at this moment pushes step branches (check `git branch -r` precedent; historically step branches are local-only here).
7. **Verify the index flip:** the planning session already set the STEP-54 row to `In progress` (with the model-assignment owner string and the 54.0–54.11 substep table) and pushed it to `prompts/main`. Verify `prompts/` is on `main`, clean, and synchronized with `origin/main`, and that the STEP-54 row reads `In progress`. If any of that is false (e.g. the flip commit was never pushed), fix it: statuses are restricted to Planned/In progress/Done/Deferred/Abandoned/N/A — free text breaks `check.sh`. Commit (`docs(STEP-54): flip to In progress`) and push to `origin/main` only if a fix was needed. Before pushing, run the duplicate scan: `grep -oE '^\|[[:space:]]*STEP-[0-9]+' STEP-index.md | grep -oE 'STEP-[0-9]+' | sort | uniq -d` (empty = ok). If the push is rejected, pull, re-check, retry.
8. **Write findings:** `Upcoming Prompts/mine-flow-STEP-54.0-FINDINGS.md` recording: actual pre-merge state (shas), merge results (ff or not), push confirmation, `.step53-logs/` decision, the three verification commands with real output counts, the new branch names/HEADs, and the index-flip commit sha.

## Verification

- Both trunks contain the STEP-53 heads (`git log --oneline -2 master` in app shows `fe12531`; docs `main` shows `891ce66`) and match their remotes (`git rev-list --left-right --count origin/master...master` = `0 0`).
- Step-0053 branches no longer exist locally; `.step53-logs/` disposition executed per user decision.
- `flutter analyze` / format / `flutter test` outputs recorded verbatim (counts, not adjectives) in the findings file.
- STEP-54 row reads `In progress` on `prompts/main` at `origin`.

## Keeping the docs true  (always)

- If any part of STEP-53's recorded state turns out to be inaccurate beyond the unmerged branches (e.g. findings claims that don't match reality), record the discrepancy in your findings and escalate — do not silently "fix" archived history.
- No architecture docs change in this substep. No secrets: never read or print `.env` values; if a command needs `--dart-define` values, use names only.

## Definition of done

- [ ] Both merges landed and pushed; branches deleted; actual shas recorded.
- [ ] `.step53-logs/` disposition decided by the user and executed.
- [ ] Analyze/format/550-test run recorded with real output in the findings file.
- [ ] `step-0054-feature-cohesion-critique` exists in app + docs repos.
- [ ] STEP-54 row `In progress` on pushed `prompts/main`; duplicate scan empty.
- [ ] `Upcoming Prompts/mine-flow-STEP-54.0-FINDINGS.md` written.

## Next

Update the PLAN's substep table (54.0 → Done) and tell the user: *"run substep 54.1"* — in a **fresh chat**.
