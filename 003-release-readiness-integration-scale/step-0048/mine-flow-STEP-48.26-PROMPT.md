# mine-flow — STEP-48.26: Branch-Head CI Gate Run & Verdict

> **How to run:** tell your agent *"run substep 48.26"*. Self-contained — runnable cold.

**Assigned model: GPT 5.6 Terra.** This substep produces the verdict the whole STEP turns on, and its
failure mode is optimism: reading a green job conclusion as evidence, or rounding "most journeys pass"
up to a passing gate. It must be willing to report red. That is a judgement about whether evidence is
real — but it is bounded by a written rule (all four jobs success **and** non-zero executed counts),
which is why it is Terra rather than Opus. **Escalate to Opus 4.8** if you find yourself wanting to
call the gate passed on anything less than the literal criterion, or if a remaining failure cannot be
classified.

## Why this substep exists

STEP-48's close criterion, written in the PLAN before any of this work began:

> A single CI run on the branch head with `test`, `build-android`, `e2e-web`, `e2e-android` all
> success **and** non-zero executed journey counts; URL and counts quoted in the close.

Run [`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159) failed that
criterion — `14 passed, 10 failed, 2 skipped` on Android, both E2E jobs red — and 48.15 correctly
refused to close. Substeps 48.16–48.24 remediated. You produce the run that decides whether 48.15 may
re-run.

You do **not** close the STEP. You do not touch the index, the archive, or the architecture docs. You
produce a run, an honest reading of it, and a verdict.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, decision **D1** (CI is the
  authoritative gate), the Test plan's final-gate paragraph, and the Definition of done.
- `Upcoming Prompts/mine-flow-STEP-48.15-FINDINGS.md` — what a close needs, and what it refused to do.
- **`Upcoming Prompts/mine-flow-STEP-48.24-FINDINGS.md`** — the local go/no-go and the per-file counts
  it predicted. Your run either confirms them or reveals a CI-vs-local difference; both are useful.
- **Every remediation findings file, `…-48.16-` through `…-48.23-`.** You must know precisely what was
  left **Deferred** and why. A journey that skips for a reason 48.20 or 48.23 recorded is expected; a
  skip nobody predicted is a finding.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-app/.github/workflows/ci.yml` — the four jobs, the `e2e-web` **zero-executed guard**,
  and the one-line Android `script:` constraint.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — the dual-platform gate definition.

## Reading CI without `gh`

There is no `gh` CLI on this host. The GitHub PAT in Git Credential Manager works as a Bearer token:

```bash
TOKEN=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill \
  | grep '^password=' | cut -d= -f2-)

# runs on the STEP branch
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs?branch=step-0048-runtime-evidence&per_page=5"

# jobs for a run
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs/<RUN_ID>/jobs?per_page=50"

# job logs: the endpoint 302s to Azure blob storage, which REJECTS the GitHub
# auth header. Capture the redirect, then fetch it bare.
URL=$(curl -sS -o /dev/null -w '%{redirect_url}' -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/lvinist/mine-flow-app/actions/jobs/<JOB_ID>/logs")
curl -sS "$URL" -o "$LOCALAPPDATA/Temp/job_<JOB_ID>.log"
```

Logs are thousands of lines — filter in code, never print them whole. The Android log groups results
per file with `✅` / `❌` / `⏭️` markers. The web log is a sequential `flutter drive` loop where each
file's outcome appears as `result {"result":"true|false","failureDetails":[…]}`.

**Never print a secret.** CI masks them as `***`; keep it that way in everything you write.

## Your task

### 1. Push the branch head and identify the run

**Precondition (48.25):** the `mine-flow-app` git object store was corrupt through 48.24 and was
repaired by **48.25**, which re-cloned, replayed the wave's changes as honest commits, and pushed a
fast-forward to `origin/step-0048-runtime-evidence`. Before doing anything here, confirm you are in
the **repaired** repository: `git fsck --full` is clean and 48.25's head sha matches
`origin/step-0048-runtime-evidence`. If `fsck` is not clean or the wave commits are missing, **stop**
— 48.25 did not complete; do not attempt repair here, route back to 48.25.

Confirm both repos are clean and every remediation commit is present, then push
`step-0048-runtime-evidence` (48.25 likely already pushed — a no-op push is fine). Record the head
sha. Find the run **triggered by that exact sha** — not the most recent run, not a run from an
earlier commit. 48.15's whole problem was a gate measured against one commit and a close attempted on
another (`469b2bc` after `90a995c`). Quote the sha the run reports and confirm it equals your head.

If a run for that sha already exists and is complete, use it rather than forcing another.

### 2. Wait for all four required jobs

`test`, `build-android`, `e2e-web`, `e2e-android`. `Deploy to Staging` / `Deploy to Production` are
expected to be `skipped` and are not part of the gate. Poll the jobs endpoint; the E2E jobs can take
most of their 60-minute timeout.

### 3. Extract the real counts — per file, per platform

A job conclusion is not the evidence. Build the table:

| Journey file | Android: passed / failed / skipped | Web: pass / fail | Verbatim skip or failure reason | Expected per findings? |
|---|---|---|---|---|

Then the run totals, stated against the baseline:

| | Branch-head run `33327930159` | This run |
|---|---|---|
| Android | 14 passed, 10 failed, 2 skipped | |
| Web | multiple failures | |

**Executed counts must be non-zero.** A job that is green because every test skipped fails the
criterion — that is the exact failure mode STEP-48 was created to fix (STEP-47 closed with
`0 tests passed, 1 skipped` and a green job). Confirm the `e2e-web` zero-executed guard did not fire,
and confirm independently that real tests ran.

### 4. Verify the skips are legitimate

For every skip, quote the verbatim reason and match it to a remediation findings file that predicted
it. Categories that are legitimate:

- Drive-dependent coverage, deferred by **D2** (RISK-0017/0018);
- the crew leg of the RLS matrix, if `TEST_CREW_*` secrets still do not exist (RISK-0021);
- any platform scope 48.23 narrowed under **Q12** (e.g. offline Part A on web);
- anything else a findings file records as Deferred with a revisit trigger.

An unexplained skip is a finding. So is a *pass* that no longer asserts anything — spot-check that no
vacuous `expect(true, isTrue)` has reappeared and that `markTestSkipped` calls are still each followed
by `return;`.

### 5. Classify anything still failing

For each remaining failure: which of 48.16's four classes is it, was it known, and who owns it? Then
choose, per failure:

- **re-run a substep** — the fix was incomplete. Name the substep and the specific defect. Do not fix
  it yourself; that would leave the fix outside the substep record.
- **Deferred with a named reason and a revisit trigger** — genuinely blocked (an absent credential, an
  unsupported platform). Say what would unblock it.

Do **not** silently accept a failure because "most things pass".

### 6. Give the verdict

Two possibilities, stated plainly:

**GO** — all four jobs `success`, executed counts non-zero, every skip explained. Then: 48.15 may
re-run, quoting your run URL, sha, and counts. Say so explicitly, and list exactly what 48.15 still has
to reconcile, gathered from the wave's handoffs:

- Doc 09 §4's "harness only" note and the real E2E shape (Doc 12);
- Doc 04's Version Log if 48.17 changed it (it should have);
- whether the design-review report's coverage claim needs narrowing to web-only or now extends to
  Android (48.22's handoff);
- RISK-0006/0011/0014/0015/0016/0019/0021/0022/0023 close-or-re-justify recommendations produced by the
  wave;
- the STEP-45 rows that can now cite real evidence, and those that cannot.

**NO-GO** — anything short of that. Then: STEP-48 stays `In progress`, Phase 4 stays shut, and you name
the substep(s) to re-run in order. This is a legitimate, valuable outcome. 48.15 set the standard for
saying it.

## Verification

- Head sha pushed; the run's sha quoted and confirmed equal to it.
- All four required jobs' conclusions recorded, with job ids and the run URL.
- Per-file counts extracted from the logs for both platforms; the table is complete.
- Executed counts confirmed non-zero; the zero-executed guard confirmed not fired.
- Every skip's verbatim reason quoted and reconciled with a findings file.
- Every remaining failure classified and assigned.
- Vacuous-pass and `markTestSkipped`-followed-by-`return` spot-checks done.
- The verdict is explicit, and the criterion it was measured against is quoted verbatim.
- No secret value anywhere in your output.

## Scope

**In scope:** pushing the branch head, obtaining and reading the run, extracting counts, classifying
residual failures, and issuing the go/no-go verdict.

**Not in scope:** fixing any defect (route it to its substep), editing application code, migrations,
staging mutation, `risks.yml` status edits, architecture doc edits, `prompts/STEP-index.md` edits,
archiving, and closing STEP-48 (all 48.15's, after your GO).

## Definition of done

- [ ] Branch head pushed; sha recorded and matched to the run.
- [ ] A single CI run identified with `test`, `build-android`, `e2e-web`, `e2e-android` results.
- [ ] Per-file, per-platform counts extracted from job logs; table written.
- [ ] Run totals stated against the `14 passed / 10 failed / 2 skipped` baseline with the delta.
- [ ] Non-zero executed counts confirmed; zero-executed guard confirmed not fired.
- [ ] Every skip explained and matched to a findings file; unexplained skips raised as findings.
- [ ] Every residual failure classified and assigned to a substep or recorded as Deferred with a
      revisit trigger.
- [ ] Explicit GO / NO-GO verdict, with the close criterion quoted.
- [ ] On GO: the reconciliation checklist for 48.15 written out.
- [ ] On NO-GO: the substeps to re-run, in order, with named defects.
- [ ] `mine-flow-STEP-48.25-FINDINGS.md` written; PLAN progress table updated.
- [ ] STEP-48's index row and status untouched.

## Next

On **GO**: tell the user the next action is *"run substep 48.15"* (docs-true sweep, index correction &
close) in a **fresh chat**, and hand it your run URL, sha, and counts.

On **NO-GO**: tell the user which substep to re-run, in a **fresh chat**, and state plainly that
STEP-48 remains `In progress` and Phase 4 remains closed.
