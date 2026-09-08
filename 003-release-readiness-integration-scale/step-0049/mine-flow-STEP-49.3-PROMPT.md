# mine-flow — STEP-49.3: Guards ④ + ⑤ — commit-per-substep discipline and trunk-reservation recovery

> **How to run:** Tell your agent *"run substep 49.3"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Authoring work bounded by a written authority:
the recovery recipes already proven in mine-flow (STEP-45 stranded close; the trunk
reservation rules). Escalate only if upstream's collaboration model differs materially
from the shared-trunk assumption.

## Context

STEP-49 lands mine-flow's process guards in the Throughstone scaffold. This substep
authors the last two guards:

- **Guard ④ — no multi-repo uncommitted closes.** A STEP whose work sits uncommitted
  across three repos blocks the next reservation entirely (mine-flow STEP-45: `prompts/main`
  stuck at `reserve STEP-45 In progress` because a dirty `STEP-index.md` on the STEP branch
  made `git switch main` impossible). The scaffold must tell an executor to **commit per
  substep on the STEP branch** — not accumulate a 3-repo uncommitted close.
- **Guard ⑤ — dirty-index/trunk-reservation recovery recipe.** When the stranded state
  has already happened: preserve the archived files, reconcile the index row and substep
  summary against actual completion evidence, update the archived PLAN's status/checklist,
  run `git diff --check` + the duplicate-STEP-number scan, commit the reconciliation,
  then push. Then (and only then) switch to `main`, fast-forward, and reserve the next
  STEP number. Reservation itself always happens **on the shared trunk**, never a
  `step-NNNN` branch.

**The proven recipes:** `Upcoming Prompts/mine-flow-STEP-47-48-49-RESERVATION-OUTLINE.md`
(§ "Pre-flight blocker" — the real stranded state; § "Reservation commands" — the
recovery sequence actually executed), and `Code/mine-flow-docs/runbooks/collaboration.md`
(the reservation/trunk rules mine-flow already lives by; the guard makes the scaffold
carry them too). Note the recovery was *real*: STEP-45's close was preserved, corrected
(`Done` rows re-truthed to Unverified), committed on its branch, merged, and only then
were STEP-47/48/49 reserved — cite that arc as the worked example.

## Read these first

- Root `.throughstone/local-user.md`.
- `Upcoming Prompts/mine-flow-STEP-49-PLAN.md`.
- `Upcoming Prompts/mine-flow-STEP-49.0-FINDINGS.md` — landing-site map (authoritative).
- `Upcoming Prompts/mine-flow-STEP-47-48-49-RESERVATION-OUTLINE.md` — § "Pre-flight
  blocker" and § "Reservation commands".
- `Code/mine-flow-docs/runbooks/collaboration.md` — the existing multi-contributor rules.
- In the **Throughstone clone**: the collaboration runbook and prompts-README-equivalent
  per 49.0's map.

## Scope

**Owns:** authoring Guards ④ and ⑤ at the mapped sites; findings file; one 49.3 commit.

**Does NOT touch:** Guards ①②③ or their files; mine-flow repos; anything outside the
clone's mapped template/process files. Do **not** renumber or rewrite upstream's
existing collaboration rules — add to them.

## Your task

1. Confirm `step-0049-template-hardening` is checked out in `D:\AppDev\Throughstone`.
2. **Author Guard ④ (commit-per-substep)** per 49.0's map — expected shape:
   - In the **collaboration runbook**: a rule that each substep's deliverables are
     committed on the STEP branch when the substep completes (not saved up for one
     end-of-STEP multi-repo close), with the worked consequence: an uncommitted close
     strands the shared trunk and blocks every later reservation. One commit per owning
     substep, message carrying the substep ID.
   - In the **prompts-README-equivalent**: fold the same expectation into the STEP
     execution recipe (the equivalent of "On completion, gather the STEP's files…"):
     committing happens along the way, gathering/archiving is the final bookkeeping.
3. **Author Guard ⑤ (stranded-trunk recovery)** — expected shape:
   - In the **collaboration runbook**: a short "Recovering a stranded close" subsection:
     preconditions (dirty `STEP-index.md` on a STEP branch; `git switch main` refused),
     the preservation rule (never stash/discard; preserve and reconcile), the
     reconciliation steps (re-truth the index row + substep summary against actual
     evidence — same honesty semantics as Guard ①), `git diff --check`, the duplicate
     STEP-number scan, commit, push, then `switch main` + fast-forward, *then* reserve.
   - Keep the existing reservation-on-trunk rule intact; the recovery subsection is the
     "what to do when it went wrong anyway" companion.
4. **Match upstream conventions**; additions not rewrites; the worked example cites
   mine-flow's STEP-45 arc in one or two sentences max (the scaffold speaks generally,
   the example grounds it).
5. **Commit** as one commit (`STEP-49.3 guards 4+5: commit-per-substep + stranded-trunk recovery`).
6. Write `Upcoming Prompts/mine-flow-STEP-49.3-FINDINGS.md`: per-file edit record with
   diff excerpts, rationale, overlap notes (especially: does upstream's collaboration
   runbook already partially cover this? merge, don't duplicate), escalation log,
   honest verification section.

## Verification

Template prose — validated by 49.4's smoke test (confirm the assignment). Prove:
- `git -C D:/AppDev/Throughstone log --oneline -1` shows the 49.3 commit; tree clean;
  `git diff HEAD~1 --stat` touches only this guard's mapped files.
- The recovery recipe's command sequence is consistent with upstream's own reservation
  rules (no contradiction between the new subsection and the existing rule text).
- Escalation triggers (record if fired): upstream's collaboration model has no shared
  trunk / different reservation flow (the recipe's premise fails); 49.0's landing sites
  disproven; upstream already carries a conflicting recovery recipe.

## Keeping the docs true

Upstream template edits are the sanctioned change; mine-flow's local copies stay
untouched. Flag any disproven PLAN assumption in findings rather than silently editing.

## Definition of done

- [ ] Guard ④ authored at all mapped landing sites.
- [ ] Guard ⑤ authored at all mapped landing sites.
- [ ] One 49.3 commit on the branch; tree clean; diff scoped to these guards.
- [ ] Findings file saved with per-file edit record and honest verification.
- [ ] No out-of-scope files; no rewrites of upstream's existing rules.

## Next

Update the PLAN's substep table (49.3 → Done) and tell the user: *"run substep 49.4"* in
a **fresh chat**.
