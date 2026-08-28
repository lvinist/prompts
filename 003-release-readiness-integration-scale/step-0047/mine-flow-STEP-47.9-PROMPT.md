# mine-flow — STEP-47.9: Final verification & STEP close

> **How to run:** Tell your agent *"run substep 47.9"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.1 Pro High. The close is where this project has historically gone wrong —
> STEP-43 phantom-closed, STEP-45 closed 15/15 Done for work that never ran. Treat it as a real
> verification pass, not paperwork.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`; all evidence is in
`Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md`. Substeps 47.0–47.8 are done.

This substep re-runs the full gate, merges three repos in order, flips the index row, and archives the
STEP. It is also the honesty gate: **a substep may not be recorded `Done` if its own evidence says
Unverified.** That rule exists because STEP-45's close claimed 15/15 Done while 14 journeys had never
executed, and correcting the record cost a whole session.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md` — the Definition of done is your checklist
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — every substep's evidence
- `prompts/README.md` — the close recipe (step 6: gather files into `step-NNNN/`, mark Done)
- `prompts/STEP-index.md` — the STEP-47 row, and the **STEP-45 substep table** as the model for how a
  substep table records Deferred/Unverified honestly
- `Code/mine-flow-docs/METHOD.md` §10 — the next-action resolver
- `Code/mine-flow-docs/runbooks/collaboration.md` — shared-trunk rules
- `Code/mine-flow-docs/architecture/12-test-strategy.md` §6 — the gate set you must prove

**Status vocabulary — mechanical, enforced by `scripts/check.sh`:** index status cells accept only
`Planned` / `In progress` / `Done` / `Deferred` / `Abandoned` / `N/A`. Free text like "Unverified"
breaks `doctor.sh`. Use **`Deferred`** in the status cell and put the Unverified detail in the Output
column — that is exactly how STEP-45's corrected table does it.

## Scope

**Owns:** the full verification run, the three-repo merge, `prompts/STEP-index.md`'s STEP-47 row and
substep table, the phase README row, and the archive into
`prompts/003-release-readiness-integration-scale/step-0047/`.

**Does NOT touch:** application code (all substeps are complete — if something needs fixing, reopen the
owning substep rather than patching at close), STEP-48's or STEP-49's rows beyond a cross-reference.

## Your task

### 1. Run the full gate — every command, on the STEP branch

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
git status --short                 # must be clean
flutter clean && flutter pub get
flutter analyze                                                    # 0 issues
dart format --output=none --set-exit-if-changed lib/ test/          # clean
flutter test 2>&1 | tail -20                                        # >=442 passing
dart run tool/check_supabase_contracts.dart
dart run tool/check_l10n_baseline.dart
flutter build apk --debug 2>&1 | tail -10                           # exit 0
flutter build web --release 2>&1 | tail -10                         # exit 0
flutter pub outdated 2>&1 | tail -20                                # direct+dev up to date
grep -n "dependency_overrides" pubspec.yaml || echo "no dependency_overrides — correct"
```

Also confirm the emulator boot check still passes (47.5's headline claim):

```bash
flutter emulators --launch Pixel_6a
flutter devices
flutter test integration_test/app_boots_test.dart -d <device-id>
```

**Every number goes in the close record.** If any gate is red, the STEP is not done — reopen the
owning substep. Do not close with a red gate and a note promising a follow-up.

### 2. Verify CI on the branch tip

```bash
git -C /d/AppDev/mine_flow/Code/mine-flow-app push
curl -s "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs?per_page=3&branch=step-0047-android-build-chain" \
  | python -c "import json,sys; [print(r['id'], r['head_sha'][:8], r['conclusion'], r['html_url']) for r in json.load(sys.stdin)['workflow_runs']]"
curl -s "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs/<RUN_ID>/jobs" \
  | python -c "import json,sys; [print(j['name'], j['conclusion']) for j in json.load(sys.stdin)['jobs']]"
```

Required: `test`, `build-android`, `e2e-web`, `e2e-android` all **success** on the *final* branch
commit. A green run on an older commit does not close this STEP — the user's scope decision was all
three Android/web jobs green.

Record the run URL and the per-job table.

### 3. Phantom-close check — verify claims against disk

STEP-43 phantom-closed; do not repeat it. For every deliverable the PLAN promises, prove it exists:

```bash
cd /d/AppDev/mine_flow
ls -la Code/mine-flow-app/build/app/outputs/flutter-apk/app-debug.apk
git -C Code/mine-flow-app log --oneline master..step-0047-android-build-chain
git -C Code/mine-flow-docs log --oneline main..step-0047-android-build-chain
git -C prompts             log --oneline main..step-0047-android-build-chain
grep -rn "FilePickerResult\|withData\|allowMultiple" Code/mine-flow-app/lib Code/mine-flow-app/test   # expect nothing
grep -n "ADR-0018" Code/mine-flow-docs/adr/README.md         # if 47.8 wrote one
ls Code/mine-flow-docs/adr/ | tail -3
ls "Upcoming Prompts/"
```

Each substep must have at least one commit in the repo it claimed to change, or an explicit
"verified, no change required" note in the evidence file. A substep with neither did not happen.

### 4. Apply the honesty gate to the substep table

Read each substep's evidence and assign a status **from its own evidence**, not from its optimism.

Truthful expectations, to be confirmed against reality:

| # | Expected status | Notes for the Output column |
|---|---|---|
| 47.0 | Done | evidence file exists; CI root cause Confirmed or explicitly Unverified |
| 47.1 | Done | zero `dependency_overrides`; KGP audit table; version list |
| 47.2 | Done | file_picker 12 migration + tests; single-pick CF-078 behaviour change noted |
| 47.3 | Done | bloc 9 migration; 11 suites green; any mounted-listener test change noted |
| 47.4 | Done | Q3 answered; lints 6 at 0 issues; CRS tolerances unchanged |
| 47.5 | Done **only if** the APK built and boot ran | otherwise Deferred with the Unverified reason |
| 47.6 | Done **only if** `e2e-web` is green | otherwise Deferred; quote the error |
| 47.7 | Done **only if** both Android jobs are green | must state the ran-vs-skipped split |
| 47.8 | Done | README + Doc 09 v0.4.0 + ADR/Q5 + risks rows |
| 47.9 | Done | this close |

**The one sentence that must appear** in the STEP-47 row: CI E2E green proves the **harness executes**;
the 14 staging journeys authored in STEP-45 remain **Deferred to STEP-48**. Three green checks without
that sentence will be misread as runtime evidence, and STEP-48 will look redundant when it is not.

### 5. Merge in order: app → docs → prompts

```bash
cd /d/AppDev/mine_flow

# 1) app (trunk is master)
git -C Code/mine-flow-app switch master
git -C Code/mine-flow-app pull --ff-only origin master
git -C Code/mine-flow-app merge --no-ff step-0047-android-build-chain \
  -m "merge(STEP-47): Android build chain remediation — AGP 9 built-in Kotlin, dependency sweep, CI E2E gates"
git -C Code/mine-flow-app push origin master

# 2) docs (trunk is main)
git -C Code/mine-flow-docs switch main
git -C Code/mine-flow-docs pull --ff-only origin main
git -C Code/mine-flow-docs merge --no-ff step-0047-android-build-chain -m "merge(STEP-47): docs — build posture, host prerequisites, risks"
git -C Code/mine-flow-docs push origin main

# 3) prompts (trunk is main) — after §6 writes the index + archive
```

**Before pushing to `master`:** the project's git rules say don't push to a trunk without permission.
Confirm with the user before the app-repo push, and note that merging to `master` will trigger
`deploy-staging` (Doc 09 §4 — it fires on `refs/heads/master` when `build-android`, `e2e-web`, and
`e2e-android` all pass). That is a real deployment to the staging GitHub Pages slot. Flag it and get
an explicit go-ahead; do not surprise the user with a deploy.

If a merge conflicts, resolve it in favour of the STEP branch **only** for files this STEP owns.
Anything else, stop and report.

### 6. Index, substep table, archive

In `prompts/STEP-index.md`:

- Flip STEP-47's status cell to `Done` (exact vocabulary only).
- Fill the Owner cell with the models that actually ran the substeps.
- Extend the Scope cell with a **Delivered:** summary — APK green locally and in CI, dependency sweep
  outcome, zero overrides, test count, ADR number — and the harness-vs-journeys sentence from §4.
- Add a `### STEP-47 substeps` table after the main table, in the same shape as STEP-45's and
  STEP-46's, with one row per substep: `| # | Title | Status | Output |`.
- **Edit only STEP-47's rows.** Never re-sort or reflow the shared table (`prompts/README.md`).

Archive per `prompts/README.md` step 6:

```bash
cd /d/AppDev/mine_flow
mkdir -p prompts/003-release-readiness-integration-scale/step-0047
mv "Upcoming Prompts/mine-flow-STEP-47-PLAN.md" \
   "Upcoming Prompts/mine-flow-STEP-47.0-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.1-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.2-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.3-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.4-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.5-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.6-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.7-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.8-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.9-PROMPT.md" \
   "Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md" \
   prompts/003-release-readiness-integration-scale/step-0047/
```

Also handle the stale reservation outline: `Upcoming Prompts/mine-flow-STEP-47-48-49-RESERVATION-OUTLINE.md`
still contains the **disproven** "flutter extension not populated in plugin subprojects" root-cause
theory. STEP-48 and STEP-49 still reference its content, so **keep it**, but add a dated correction
note at its top pointing at STEP-47's actual root cause and this archive. A stale document that
contradicts the evidence is worse than no document.

Update the phase README (`prompts/003-release-readiness-integration-scale/README.md`) with a STEP-47 row
from `templates/phase-readme-template.md`'s shape.

Then:

```bash
cd /d/AppDev/mine_flow/prompts
git add STEP-index.md 003-release-readiness-integration-scale/
git commit -m "close(STEP-47): Android build chain green locally and in CI; PLAN+prompts archived to step-0047"
grep -oE '^\|[[:space:]]*STEP-[0-9]+' STEP-index.md | grep -oE 'STEP-[0-9]+' | sort | uniq -d   # must be empty
git diff --check
git switch main && git pull --ff-only origin main
git merge --no-ff step-0047-android-build-chain -m "merge(STEP-47): close and archive"
git push origin main
```

### 7. Confirm the resolver and hand off

```bash
cd /d/AppDev/mine_flow && ./doctor.sh status
```

Expected: STEP-47 no longer next; **STEP-48** (Runtime Evidence) resolves as the next action. If the
resolver still points at 47, the index edit is wrong — fix it before finishing.

A check-in STEP was last run at STEP-40. Per `prompts/README.md` (every ~10–20 STEPs), a check-in is
now **7 STEPs** overdue in the sense that it is due within the remaining headroom. Mention it to the
user when handing off — it is their call whether STEP-48 or a check-in comes first.

Also tell the user what STEP-47 unblocked for STEP-48, concretely: an installable debug APK, a working
emulator boot path, and a web E2E invocation that can actually run journeys once credentials are wired.

## Verification

- Every gate in §1 green, with real numbers recorded (not "all passing").
- CI: all four jobs green on the **final** branch commit, run URL recorded.
- Phantom-close checks in §3 all pass; every substep maps to a commit or an explicit no-change note.
- No substep marked `Done` whose own evidence says otherwise; anything short is `Deferred` with the
  reason in the Output column.
- Duplicate STEP-number scan empty; `git diff --check` clean.
- All three repos merged to their trunks and pushed, with user consent for the `master` push and its
  `deploy-staging` consequence.
- `doctor.sh status` resolves STEP-48 as next.
- The archive folder contains the PLAN, all ten substep prompts, and the evidence file.

## Keeping the docs true (always)

47.8 owns doc content; this substep only verifies it landed:

- `architecture/09-environments.md` is at v0.4.0 with a matching Version Log row.
- The ADR (if written) is in the registry with no duplicate number.
- `registries/risks.yml` parses; RISK-0006 is still `open`; RISK-0008's amendment is present.
- The app `README.md` host-prerequisites section exists.

If any is missing, reopen 47.8 rather than writing it here — otherwise the archived prompt and the
delivered work disagree.

No secrets: no `.env` read, no secret value printed, no remote Supabase state mutated. Note explicitly
that `deploy-staging` may publish to the staging Pages slot as a *consequence of the merge*, which is
the one remote effect of this close and requires the user's go-ahead.

## Definition of done

- [ ] Full gate re-run on the branch: analyze 0, format clean, `flutter test` ≥442, both contract
      guards, debug APK exit 0, web release exit 0, `pub outdated` clean, no `dependency_overrides`
- [ ] Emulator boot check re-confirmed
- [ ] CI `test` + `build-android` + `e2e-web` + `e2e-android` green on the final commit; run URL recorded
- [ ] Phantom-close checks pass; every substep traced to a commit or a stated no-change
- [ ] Substep statuses assigned from evidence; `Deferred` used (never free-text "Unverified") in status cells
- [ ] STEP-47 row flipped to `Done` with a Delivered summary **and** the harness-vs-journeys sentence
- [ ] `### STEP-47 substeps` table added; only STEP-47's rows touched; no re-sorting
- [ ] Reservation outline annotated with the dated root-cause correction
- [ ] Phase README row added
- [ ] PLAN + 10 substep prompts + evidence archived to `prompts/003-…/step-0047/`
- [ ] Duplicate-number scan empty; `git diff --check` clean
- [ ] All three repos merged and pushed; `master` push explicitly authorised by the user, with the
      `deploy-staging` consequence stated beforehand
- [ ] `doctor.sh status` resolves STEP-48 as the next action
- [ ] Check-in cadence mentioned to the user

## Next

STEP-47 is closed. Tell the user the next action per `METHOD.md` §10: **STEP-48 — Runtime Evidence
(resolve STEP-45's carried-forward findings)** — planned in a fresh chat, noting that a Check-in STEP
is also due and they may prefer it first. STEP-48 now has what it was blocked on: a buildable APK, a
working emulator path, and a web E2E invocation that runs.
