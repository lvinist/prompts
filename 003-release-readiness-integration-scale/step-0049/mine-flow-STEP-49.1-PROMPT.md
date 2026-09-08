# mine-flow — STEP-49.1: Guards ① + ② — Unverified-vs-Done honesty gate and phantom-close detection

> **How to run:** Tell your agent *"run substep 49.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real authoring work, bounded by written
authorities: the failure modes have documented evidence (STEP-45/48) and the semantic
target is written down in mine-flow's proven status rules. Escalate if your wording would
change what a *status column* means rather than adding a check — see Escalation.

## Context

STEP-49 lands mine-flow's process guards in the Throughstone scaffold (clone at
`D:\AppDev\Throughstone`, branch `step-0049-template-hardening`, cut by 49.0 or by you if
49.0's findings say it wasn't). This substep authors the first two guards:

- **Guard ① — Unverified-vs-Done honesty gate.** In mine-flow STEP-45, an executing agent
  closed 15/15 substeps `Done` while 14 journeys had never run and every design-review
  item was Unverified. The template must make this mechanically rejectable: a substep
  whose own report says Unverified for a required deliverable may not be marked Done.
- **Guard ② — Phantom-close detection.** The close checklist must require
  branch/commit/artifact existence checks against disk before a STEP row flips to Done
  (mine-flow STEP-43 and STEP-45 both phantom-closed or strand-closed).

**The evidence that defines the semantics:**
- `prompts/STEP-index.md` STEP-48 close note (2026-09-08): *"Statuses below are assigned
  from the latest findings and branch-head run 34225431645, not from earlier per-substep
  optimism"* — the proven status-from-latest-evidence rule you are codifying.
- `Code/mine-flow-docs/reports/2026-08-27-step-0045-findings-reconciliation.md` — the
  record-correction that exposed the phantom close.
- `Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` — the
  audit pattern (re-derive claims from disk).
- 49.0's findings (`Upcoming Prompts/mine-flow-STEP-49.0-FINDINGS.md`): the verified
  landing sites and any existing overlap.

## Read these first

- Root `.throughstone/local-user.md` (calibrate to Experience level).
- `Upcoming Prompts/mine-flow-STEP-49-PLAN.md` — the whole PLAN.
- `Upcoming Prompts/mine-flow-STEP-49.0-FINDINGS.md` — landing-site map (authoritative).
- In the **Throughstone clone** (paths from 49.0's map; expected `Code/mine-flow-docs/…`):
  the step-plan template, substep-prompt template, METHOD-equivalent, and
  step-index-seed/template status vocabulary.
- `prompts/STEP-index.md` STEP-48 substep table + close note (the convention being codified).

## Scope

**Owns:** authoring Guards ① and ② in the mapped upstream files; the findings file;
committing this substep's edits on `step-0049-template-hardening`.

**Does NOT touch:** Guards ③–⑤ (substeps 49.2/49.3); `Code/mine-flow-app/`;
`Code/mine-flow-docs/`; `prompts/` (beyond reading); anything outside the clone's
mapped template/process files.

## Your task

1. **Cut the branch** if 49.0 didn't: in `D:\AppDev\Throughstone`,
   `git switch -c step-0049-template-hardening` from the default branch.
2. **Author Guard ① (honesty gate)** per 49.0's landing map — expected shape (adapt to
   upstream's actual file names/structure):
   - In the **step-plan template's** definition-of-done section: a checkable item that the
     substep-status table was reconciled against each substep's own findings/evidence
     file, and that no substep marked `Done` has a required deliverable recorded
     `Unverified` there.
   - In the **substep-prompt template**: a short "Honesty at close" block stating that an
     unrunnable or unrun verification is reported as **Unverified with reason**, never as
     a pass, and that the substep's status inherits the evidence's verdict.
   - In the **METHOD-equivalent's** close rules: status may only be flipped `Done` when
     the evidence file's own wording supports it; the index row's status is derived from
     the latest findings, not from earlier optimism.
   - Respect the template status vocabulary (Planned / In progress / Done / Deferred /
     Abandoned / N/A — or upstream's exact set). **Do not invent a new status value.**
3. **Author Guard ② (phantom-close detection)** — expected shape:
   - In the **step-plan template's** definition-of-done checklist: before a STEP flips to
     Done, verify on disk — for each projected repo — the branch exists (or was merged),
     the commit(s) exist and are pushed where the project pushes, and named artifacts
     (reports, evidence files) exist at their cited paths. A row whose cited evidence
     does not exist on disk cannot close the STEP.
   - In the **METHOD-equivalent close rules**: one clause citing that a claimed commit
     must be verifiable (`git rev-parse`, run URL, or file existence) before it counts.
4. **Keep each guard addition surgical**: the guards must read as additions to the
   existing close rules, not rewrites of the surrounding text. Match upstream's voice,
   heading structure, and comment conventions.
5. **Commit** this substep's edits on the branch (one commit, message naming
   `STEP-49.1 guards 1+2: honesty gate + phantom-close detection`). Do not mix in
   anything belonging to 49.2/49.3.
6. Write `Upcoming Prompts/mine-flow-STEP-49.1-FINDINGS.md`: the exact edits (file →
   section → what was added, with a short diff excerpt per file), wording rationale, any
   existing-guard overlap you had to merge with, escalation log, and an honest
   verification section (what you ran, what you couldn't).

## Verification

No runnable test applies to template prose (this STEP's test plan defers all validation
to 49.4's scratch-init smoke test — confirm that assignment in your findings). Prove
instead:
- `git -C D:/AppDev/Throughstone log --oneline -1` shows your 49.1 commit; `git status`
  clean; `git diff HEAD~1 --stat` touches only the mapped guard-①/② files.
- Every edit site exists in upstream (no invented headings/anchors) — cite the
  surrounding upstream line you appended after.
- Guard text does not introduce a new status value or redefine an existing one.
- Escalation triggers (record if fired): wording that would change status-column
  semantics rather than add a check; upstream's close rules conflict with the
  status-from-latest-evidence principle; landing sites from 49.0 disproven.

## Keeping the docs true

This substep edits the *upstream template*, which is exactly the sanctioned change
(UPDATING-THROUGHSTONE §2 process-docs/templates buckets). mine-flow's local copies are
NOT updated (user decision). If your edits reveal a PLAN assumption is wrong, record it
in findings and flag the PLAN for update — don't edit the PLAN silently.

## Definition of done

- [ ] Guard ① authored at all mapped landing sites.
- [ ] Guard ② authored at all mapped landing sites.
- [ ] Edits committed as one 49.1 commit on `step-0049-template-hardening`; tree clean.
- [ ] Findings file saved with per-file edit record and honest verification section.
- [ ] No status-vocabulary change; no out-of-scope file touched.

## Next

Update the PLAN's substep table (49.1 → Done) and tell the user: *"run substep 49.2"* in
a **fresh chat**.
