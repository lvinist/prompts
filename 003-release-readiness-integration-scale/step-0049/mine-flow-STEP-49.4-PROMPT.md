# mine-flow — STEP-49.4: Scaffold smoke validation + CHANGELOG entry

> **How to run:** Tell your agent *"run substep 49.4"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.7 Flash High.** Mechanical run-and-report with clear exit
codes: the STEP's final verification substep. Escalate any failure you cannot trivially
attribute — see Escalation.

## Context

STEP-49's guards ①–⑤ are authored on `step-0049-template-hardening` in the Throughstone
clone (`D:\AppDev\Throughstone`) by substeps 49.1–49.3. This substep is the STEP's test
gate (the PLAN's test plan assigns all validation here): prove the modified scaffold
still **bootstraps a working project**, record the evidence, and write the upstream
CHANGELOG entry.

The scratch-project run must never touch the real mine_flow workspace — it happens in a
temp directory and is deleted or left as temp debris only.

## Read these first

- Root `.throughstone/local-user.md`.
- `Upcoming Prompts/mine-flow-STEP-49-PLAN.md` — especially the Test plan and Definition of done.
- `Upcoming Prompts/mine-flow-STEP-49.0-FINDINGS.md` — the verify-loop design notes
  (authoritative for *what to check in the generated project*) and the smoke-test plan.
- Findings from 49.1, 49.2, 49.3 — which files carry which guards (so you can grep for
  each guard's marker text in the generated output).
- In the **Throughstone clone**: `init.sh` usage/help (`bash init.sh --help` or the
  header comment) for the required arguments (slug/provider etc.), and `CHANGELOG.md`.

## Scope

**Owns:** the scratch-init smoke run, its captured log, the guard-marker checks, the
CHANGELOG entry, the findings file, one 49.4 commit.

**Does NOT touch:** `D:\AppDev\mine_flow` (the real workspace) beyond `Upcoming
Prompts/` bookkeeping; the guard content itself (if validation fails, report —
the fix belongs to the owning substep, not you).

## Your task

1. **Prepare the scratch run.** Read 49.0's verify-loop notes and `init.sh`'s own
   preflights. Create a scratch directory under `$LOCALAPPDATA/Temp` (NOT `/tmp` —
   MSYS path translation is disabled on this host; NOT inside `D:\AppDev\mine_flow`).
   Copy the clone's contents (or use `git -C D:/AppDev/Throughstone worktree add` —
   your call, record which) so `init.sh` runs against the modified template on the
   branch, cleanly separated.
2. **Run the smoke test:** `bash init.sh` with a throwaway slug (e.g. `smoke49`) and
   whatever provider/owner flags make it non-interactive (49.0's notes should say
   which; `--provider=manual` or equivalent local mode if available). Capture the full
   output to a log file. Expected: **exit 0**.
3. **Verify the generated project:**
   - The generated docs hub's `check.sh` (or `doctor.sh check`) runs **exit 0**.
   - Each guard's marker text appears where the landing map says it should: the
     generated step-plan template / substep-prompt template / METHOD / planning-session
     / collaboration runbook / prompts-README carry the new guard clauses. Grep for a
     distinctive phrase per guard (pick one from each guard's authored text; record the
     phrase + hit count per file in your findings).
   - No placeholder regression: the project slug replaced correctly (grep for the
     un-replaced project-placeholder token — zero hits expected).
4. **Failure triage:** if any check fails, classify against the owning substep (which
     guard's edit is implicated) and **escalate rather than fix** — you are the gate,
     not the author. A failure that is trivially environmental (e.g. missing `perl`)
     you may resolve and re-run, recording both runs.
5. **Write the upstream CHANGELOG entry** (in the clone, on the branch): one entry
     naming all five guards and their one-line effect, under the repo's existing
     changelog conventions (Unreleased section if present; else create the entry shape
     the file's history uses).
6. **Commit** (`STEP-49.4 smoke validation + CHANGELOG entry`) — CHANGELOG and any
   validation artifacts the repo's conventions expect; the run log itself stays in
   `Upcoming Prompts/` evidence, not the upstream repo.
7. Write `Upcoming Prompts/mine-flow-STEP-49.4-FINDINGS.md`: the smoke-run command
   lines + exit codes, the log file path (workspace-root evidence log per house style,
   e.g. `step49_smoke_init.log`), the per-guard marker table, the check.sh result, the
   CHANGELOG diff, escalation log, honest verification section. Clean up the scratch
   directory (or record its path if left for inspection).

## Verification

This *is* the verification substep. Acceptance:
- `init.sh` on the modified template → exit 0, log captured and cited.
- Generated project's `check.sh` → exit 0, cited.
- Per-guard marker table complete: 5 guards × their mapped files, each with a grep hit.
- Upstream `CHANGELOG.md` diff names all five guards.
- One 49.4 commit on `step-0049-template-hardening`; clone tree clean afterwards.
- Escalation triggers (record if fired): any smoke failure not trivially environmental;
  a guard missing from the generated project (fix belongs to 49.1–49.3); `init.sh`
  requires interactivity/credentials you don't have (report Unverified, don't fake it).

## Keeping the docs true

Validation artifacts live in the findings file and evidence logs. If validation disproves
a guard's landing, record it — the owning substep (or the close substep 49.5) handles the
repair; do not silently edit other substeps' content.

## Definition of done

- [ ] Scratch `init.sh` run: exit 0, log preserved and cited in findings.
- [ ] Generated project `check.sh`: exit 0, cited.
- [ ] All five guards' markers verified present in the generated output (table in findings).
- [ ] No un-replaced placeholder tokens in the generated project.
- [ ] Upstream CHANGELOG entry committed; clone tree clean.
- [ ] Findings file saved; scratch directory cleaned up or its path recorded.

## Next

Update the PLAN's substep table (49.4 → Done) and tell the user: *"run substep 49.5"* in
a **fresh chat** — the close substep (fork, PR, STEP close).
