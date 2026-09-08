# mine-flow — STEP-49.2: Guard ③ — credential/host-toolchain pre-flight substep for runtime STEPs

> **How to run:** Tell your agent *"run substep 49.2"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Authoring work fully bounded by a written
authority: STEP-47.0's documented pre-flight pattern. Escalate only if upstream's
planning flow cannot host the guidance without structural change.

## Context

STEP-49 lands mine-flow's process guards in the Throughstone scaffold. This substep
authors **Guard ③**: runtime/E2E STEPs must front-load a pre-flight substep that proves
credentials and a working build/device/toolchain *before* the STEP authors journeys or
tests — so a STEP cannot produce 14 skipped tests (mine-flow STEP-45's exact failure:
journeys authored before anyone proved `TEST_USER_EMAIL`/`TEST_USER_PASSWORD` existed,
discovered only at STEP-47.0).

**The proven pattern to codify** (STEP-47.0, `prompts/003-release-readiness-integration-scale/step-0047/`):
- A substep 0 that runs before any implementation work, whose deliverable is *evidence*,
  not code: verbatim failure output, host toolchain inventory (SDK/VM/JDK/PATH/env
  versions), baseline gate results, and an explicit credentials-available-or-not verdict.
- Each pre-flight fact is recorded with its own verification; anything uncheckable is
  **Unverified with reason**, and the STEP's later substeps are re-scoped (or the STEP is
  re-sequenced) on that basis — e.g. STEP-48 was only plannable because STEP-47.0 proved
  which credentials existed.
- Expected landing sites (verify against 49.0's map): the **planning-session template**
  (STEP-planning recipe) and the **METHOD-equivalent's** STEP-planning rules; possibly
  the substep-prompt template's Verification section.

## Read these first

- Root `.throughstone/local-user.md`.
- `Upcoming Prompts/mine-flow-STEP-49-PLAN.md`.
- `Upcoming Prompts/mine-flow-STEP-49.0-FINDINGS.md` — landing-site map (authoritative).
- `prompts/003-release-readiness-integration-scale/step-0047/mine-flow-STEP-47.0-EVIDENCE.md` (or the archived 47.0 prompt/findings — the pre-flight pattern in practice).
- `prompts/STEP-index.md` STEP-47 row + 47.0/47.5 substep rows — what the pattern delivered.
- In the **Throughstone clone**: the planning-session template and METHOD-equivalent
  planning rules per 49.0's map.

## Scope

**Owns:** authoring Guard ③ at the mapped sites; findings file; one 49.2 commit.

**Does NOT touch:** Guards ①②④⑤ or their files beyond what 49.0 mapped to this guard;
mine-flow repos; anything outside the clone's mapped template/process files.

## Your task

1. Confirm branch `step-0049-template-hardening` exists and is checked out in
   `D:\AppDev\Throughstone` (49.1 created it; if you are somehow first, cut it from the
   default branch per 49.0's recorded sha).
2. **Author Guard ③** per 49.0's map — expected shape:
   - In the **planning-session template**: guidance that any STEP whose substeps must
     *execute* against a runtime (E2E, integration against staging, device/emulator,
     deployment) reserves its **first substep as a pre-flight** that proves, with
     recorded evidence: required credentials exist (name them by placeholder, never
     value), the host toolchain can build/run the target, and the baseline gates pass.
     The STEP's remaining substeps are authored *after* the pre-flight verdict, and any
     unprovable surface is scoped as Unverified-with-reason rather than assumed.
   - In the **METHOD-equivalent's STEP-planning rules**: the same rule in summary form
     (one or two sentences pointing at the planning-session guidance).
   - If 49.0's map adds the substep-prompt template's Verification section, add one
     clause there: runtime-verifying substeps name their runtime precondition and what
     happens when it is absent (skip with recorded reason, never a silent pass).
3. **Match upstream conventions** (voice, headings, comment style). Additions, not
   rewrites. Never print credential *values* anywhere — placeholders/names only.
4. **Commit** as one commit (`STEP-49.2 guard 3: runtime pre-flight substep guidance`);
   the diff must contain only this guard's edits.
5. Write `Upcoming Prompts/mine-flow-STEP-49.2-FINDINGS.md`: per-file edit record with
   diff excerpts, rationale, overlap notes, escalation log, honest verification section.

## Verification

Template prose — validated by 49.4's smoke test (confirm the assignment). Prove:
- `git -C D:/AppDev/Throughstone log --oneline -1` shows the 49.2 commit; tree clean;
  `git diff HEAD~1 --stat` touches only this guard's mapped files.
- No credential value or secret appears in any edit (grep your own diff for `=`, tokens
  longer than 20 chars near words like key/token/password — placeholders only).
- Escalation triggers (record if fired): upstream's planning flow structurally cannot
  host the guidance; 49.0's landing sites for this guard disproven; conflict with an
  upstream rule that already governs runtime STEPs.

## Keeping the docs true

Upstream template edits are the sanctioned change; mine-flow's local copies stay
untouched. Flag any disproven PLAN assumption in findings rather than silently editing.

## Definition of done

- [ ] Guard ③ authored at all mapped landing sites.
- [ ] One 49.2 commit on the branch; tree clean; diff scoped to this guard.
- [ ] Findings file saved with per-file edit record and honest verification.
- [ ] No secrets, no out-of-scope files.

## Next

Update the PLAN's substep table (49.2 → Done) and tell the user: *"run substep 49.3"* in
a **fresh chat**.
