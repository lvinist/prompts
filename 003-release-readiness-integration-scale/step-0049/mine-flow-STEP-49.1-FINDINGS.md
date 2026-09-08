# mine-flow — STEP-49.1 Findings: Guards ① + ②

**Date:** 2026-09-09
**Executor:** Gemini 3.1 Pro High
**Substep:** 49.1
**Status:** Complete

## Edits Made

1. **`Code/{{PROJECT}}-docs/templates/step-plan-template.md`**
   - **Section:** `## Definition of done`
   - **Added:** Two checklist items for honesty gate and phantom-close detection.
   - **Excerpt:**
     ```markdown
     +- [ ] Substep status table reconciled against each substep's evidence file; no substep marked `Done` if a required deliverable is recorded `Unverified`.
     +- [ ] Disk verification: for each projected repo, the branch exists (or was merged), commits exist and are pushed, and cited artifacts/reports exist at their cited paths.
     ```

2. **`Code/{{PROJECT}}-docs/templates/substep-prompt-template.md`**
   - **Section:** `## Verification`
   - **Added:** "Honesty at close" instructions for unverified deliverables.
   - **Excerpt:**
     ```markdown
     +- **Honesty at close:** an unrunnable or unrun verification must be reported in the findings/evidence file as **Unverified with reason**, never claimed as a pass. The substep's status inherits the evidence's verdict.
     ```
   - **Section:** `## Definition of done`
   - **Added:** Verification checklist item.
   - **Excerpt:**
     ```markdown
     +- [ ] Findings/evidence file recorded truthfully; substep status inherits the evidence verdict (no `Unverified` items claimed as a pass).
     ```

3. **`Code/{{PROJECT}}-docs/METHOD.md`**
   - **Section:** `## 5. The prompt lifecycle` (New section `### Closing a STEP`)
   - **Added:** Rules that index row status derives from latest findings and commits/artifacts must be verified.
   - **Excerpt:**
     ```markdown
     +### Closing a STEP
     +When closing a STEP or substep, its status may only be flipped to **Done** when the evidence file's own wording supports it. The index row's status must be derived from the latest findings, not from earlier optimism. Furthermore, claimed commits and artifacts must be verified against disk before a STEP or substep is marked `Done` — a claimed commit must be verifiable (e.g., via `git rev-parse`, run URL, or file existence) before it counts.
     ```
   - **Section:** `## 10. What to do next` (Rule 6)
   - **Added:** Disk verification requirement to review instructions.
   - **Excerpt:**
     ```markdown
     -   substep is done, run the STEP's review,
     +   substep is done, run the STEP's review (ensuring commits and cited artifacts are verified against disk),
     ```

4. **`Code/{{PROJECT}}-docs/templates/step-index-seed.md`**
   - **Section:** Status values blockquote
   - **Added:** Honesty check for the `Done` status.
   - **Excerpt:**
     ```markdown
     -> Status values: **Planned** · **In progress** · **Done** (archived to `prompts/`) ·
     +> Status values: **Planned** · **In progress** · **Done** (archived to `prompts/`; requires positive verification, unverified required deliverables cannot close a row as Done) ·
     ```

## Wording Rationale
The additions directly capture the findings from STEP-45/48. The `Unverified` keyword and "inherits the evidence verdict" rule formalizes the behavior without redefining existing status values. The term "phantom-close" maps to verifying commits and artifacts via disk/URL before closing.

## Existing-Guard Overlap
As established in 49.0 findings, there was zero existing coverage for these guards. The additions fit cleanly within the existing sections.

## Escalation Log
None triggered. No new status value was added, and edits align with the target semantics.

## Verification
- **Run:** `git -C D:/AppDev/Throughstone log --oneline -1` correctly shows the 49.1 commit. `git status` is clean. `git diff HEAD~1 --stat` touches exactly the 4 mapped files.
- **Unverified:** No application tests or template smoke tests were run. Validation is deferred to 49.4's scratch-init smoke test, as defined in the test plan.
