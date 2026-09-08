# mine-flow — STEP-48.16: Branch-Head Failure Triage & Classification Gate

> **How to run:** tell your agent *"run substep 48.16"*. Self-contained — runnable cold.

**Assigned model: GPT 5.6 Terra.** This substep decides *what each failure is*, and every substep
after it inherits that decision. Misfiling one application defect as a test defect launders a
regression into a green suite — the exact failure mode STEP-48 was created to correct. The work is
bounded (the logs are fixed, the classification rule is written below), which is why it is Terra and
not Opus, but the cost of a wrong call here is silent. **Escalate to Opus 4.8** if a failure cannot
be classified from the available evidence, or if classifying it honestly would mean contradicting a
substep already marked `Done`.

## Why this substep exists

STEP-48 ran fifteen `integration_test` journeys against real staging and marked ten substeps `Done`.
Then 48.15 tried to close the STEP and found the required **branch-head** CI gate red: run
[`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159) on commit
`90a995c31a3a` reports

| Job | Result |
|---|---|
| Lint, analyze & test | success |
| Build Android APK | success |
| E2E Tests (Android) | **failure** — `14 tests passed, 10 failed, 2 skipped` |
| E2E Tests (Web) | **failure** |

48.15 refused to convert that into a close and recorded itself `Deferred`. That was correct. The
remediation is substeps 48.16–48.25, and you are first.

The per-substep greens and the branch-head red are **both true**. Each journey substep verified its
own file, mostly on a locally booted emulator, at a point in the branch's history. The branch-head
run is the first time all fifteen files ran together against the *current* staging schema. Your job
is to explain every failure and route it, not to relitigate whether the earlier substeps lied.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — especially the **2026-08-31 amendment**, which
  carries a verified failure inventory read from the job logs, decisions **D6** and **D7**, the
  remediation substep table, and questions **Q7–Q12**.
- `Upcoming Prompts/mine-flow-STEP-48.15-FINDINGS.md` — the honest blocked close.
- The findings files for the substeps that own the failing journeys: `…-48.4-`, `…-48.5-`,
  `…-48.6-`, `…-48.7-`, `…-48.8-`, `…-48.9-`, `…-48.10-`, `…-48.11-`, `…-48.13-FINDINGS.md`.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory. Calibrate accordingly.
- `Code/mine-flow-docs/architecture/04-data-model.md` — the entity/column authority.
- `Code/mine-flow-app/supabase/migrations/` — all five migration files. This is what staging
  actually has.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the UI contract, for any
  visual/widget failure.
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md` §1–§2 — platform scope and
  offline-first/last-write-wins, for the offline failures.

## Reading the CI logs yourself

Do not work from the PLAN's inventory alone — confirm it. There is no `gh` CLI on this host, but the
GitHub PAT in Git Credential Manager works as a Bearer token:

```bash
TOKEN=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill \
  | grep '^password=' | cut -d= -f2-)

# jobs for the run
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs/33327930159/jobs?per_page=50"

# logs: the endpoint 302s to Azure blob storage, which REJECTS the GitHub auth
# header. Capture the redirect, then fetch it bare.
for JID in 99301582624 99301582641; do
  URL=$(curl -sS -o /dev/null -w '%{redirect_url}' -H "Authorization: Bearer $TOKEN" \
    "https://api.github.com/repos/lvinist/mine-flow-app/actions/jobs/$JID/logs")
  curl -sS "$URL" -o "$LOCALAPPDATA/Temp/job_$JID.log"
done
```

`99301582624` is Android, `99301582641` is web. The Android log is ~5400 lines and the web log
~1800; filter in code, do not print them whole. The Android log groups results per file with
`✅` / `❌` / `⏭️` markers — that is the fastest route to the per-journey verdict. The web log is a
sequential `flutter drive` loop where each file's outcome appears as
`result {"result":"true|false","failureDetails":[…]}`.

**Never print a secret.** The logs already mask secrets as `***`; keep it that way in anything you
write.

## Your task

### 1. Build the per-failure register

One row per **distinct failure**, not per failing file — a file can fail for two reasons, and two
files can fail for the same reason. For each:

| Field | Content |
|---|---|
| ID | `BH-001`, `BH-002`, … (branch-head) |
| Platform | Android / Web / both |
| Journey file + line | e.g. `cut_fill_journey_test.dart:90` |
| Verbatim error | the exact message, quoted — `42703 column cut_fill_records.measurement_date does not exist`, not "a column error" |
| Classification | one of the four below |
| Root cause | one or two sentences, naming the file:line that is wrong |
| Owning substep | exactly one of 48.17–48.23 |
| Superseded-by note | which earlier substep believed this was settled, if any |

### 2. Classify with this rule, not by convenience

- **schema-gap** — the app queries a table or column that no migration creates. The *database* is
  wrong (or the query is; decide which, and say so). Errors of shape `PGRST205`, `PGRST204`,
  `42703`. → 48.17 for missing tables, 48.18 for wrong column names in queries, 48.19 for wrong
  column names in writes.
- **fixture-drift** — the schema is fine, the data is not: empty-string UUIDs (`22P02`), non-UUID
  identifiers like `KRU-001`, a `site_id` that no seeded row uses, an FK to a row that does not
  exist (`23503`). → 48.20.
- **app-defect** — the application misbehaves at runtime: an unhandled exception building a page, a
  layout overflow, a value that does not persist, a route that does not resolve. → 48.22 for
  UI/harness, 48.23 for persistence/data-integrity.
- **test-defect** — the journey is wrong about the app: an ambiguous finder, a semantics label that
  no widget carries, a wait that is too short. → 48.21.

**The rule that decides ties (PLAN Q4, still binding):** if the app contradicts
`architecture/07-ui-design-system.md` or another accepted doc/ADR, it is an **app-defect** and gets a
finding — do **not** edit the test to match whatever the app currently does. If the doc is stale,
that is doc drift needing a Version Log bump. A `42501` RLS refusal deserves particular care: a
policy correctly refusing an operation is a **test-defect** (the test assumed the wrong role); a
policy refusing something a role should be allowed is a **security-shaped app-defect** — escalate
that one.

### 3. Answer Q7 — audit the ten `Done` substeps

For each substep marked `Done` whose journey failed at branch head, decide:

- **stays `Done`** — its own evidence is still true and the failure is new information (a schema gap
  another feature exposed, a cross-journey interaction). Add a note in the PLAN's progress table
  pointing at the remediation substep.
- **downgraded to `Deferred`** — its evidence is now known false: it asserted a behaviour the
  branch-head run disproves. Amend the PLAN row and **append** an amendment to its findings file.

**Archived findings are immutable — append, never rewrite.** Use a dated
`## Amendment — 2026-08-31 (STEP-48.16)` block.

Say plainly how many of the ten you downgraded and why. If you downgrade none, justify that; if you
downgrade most, say what the earlier substeps had in common.

### 4. Verify the PLAN's inventory

The PLAN's amendment table was written during planning from the same logs. Confirm each row, and
call out anything it got wrong or missed. It already records one correction you should not redo:
the `adb: device offline` lines are `android-emulator-runner`'s normal boot poll and it recovered
(`Emulator booted.` five lines later) — the Android job failed on **tests**, not infrastructure.

It also flags failures that have **not fired yet** but are the same class as ones that did — e.g.
`land_clearing_model.dart:67-68` writes `clearing_method` and `vegetation_type`, and
`20260723_step_33_1` dropped `vegetation_type`. Sweep for that class deliberately: grep every
model's `toJson()` against the actual migration columns and list every mismatch, fired or not. A
class fixed only where it happened to fail will fail again in the next run.

### 5. Sequence the fixes

Produce the dependency order the wave should run in, and name anything two substeps would both
touch (a file both 48.19 and 48.22 must edit, for instance) so they do not collide. 48.17 is a hard
dependency for 48.18–48.20; beyond that, say what can run in parallel.

## Verification

- Every `❌` in the Android log and every `"result":"false"` in the web log appears in your register.
  Count them and state the count: the run reports **10 failed** on Android.
- Every register row has exactly one owning substep. No row is unassigned, none has two.
- Every classification quotes the evidence line it rests on.
- Q7 answered for all ten `Done` substeps.
- The "same class, not yet fired" sweep is complete — every model `toJson()` checked against the
  migrations.
- No secret value appears anywhere in your output.

## Scope

**In scope:** reading logs, classifying, routing, auditing the `Done` statuses, sweeping for
unfired instances of the same classes, sequencing.

**Not in scope:** fixing anything. No application code, no migrations, no test edits, no staging
mutation. If you find yourself editing a `.dart` file, you have left the substep. The only files you
write are `Upcoming Prompts/mine-flow-STEP-48.16-FINDINGS.md`, the PLAN's progress table and Q7
notes, and appended amendments to earlier findings files.

## Definition of done

- [ ] `mine-flow-STEP-48.16-FINDINGS.md` written with the full `BH-nnn` register.
- [ ] All 10 Android failures and all web failures accounted for; counts stated.
- [ ] Each failure classified by the four-way rule with its evidence quoted.
- [ ] Each failure assigned to exactly one of 48.17–48.23.
- [ ] Q7 answered: each `Done` substep confirmed or downgraded, findings amended by appending.
- [ ] Unfired same-class defects listed (model `toJson()` vs migrations sweep).
- [ ] Fix sequence and file-collision warnings recorded.
- [ ] PLAN progress table updated for 48.16 and any downgraded rows.
- [ ] Nothing else modified — `git status` in `mine-flow-app` shows no changes.

## Next

Tell the user the next action is *"run substep 48.17"* (staging schema completion) in a **fresh
chat**, and that 48.17 needs a scoped Supabase access token (`sbp_…`) to hand to the agent when it
asks. Note which substeps 48.18–48.23 actually have work assigned to them — if your triage assigned
nothing to one of them, say so, and it should be marked `N/A` rather than run for form's sake.
