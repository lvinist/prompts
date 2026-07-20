# mine-flow — STEP-11.5: Workspace Hygiene (Archive Prompts)

> **How to run:** Tell your agent *"run substep 11.5"* (or *"read and run this file"*).

## Context
As part of the STEP-10 audit, it was discovered that the prompt files for STEP-7, STEP-8, and STEP-9 were left in `Upcoming Prompts/` instead of being archived to their respective folders in `prompts/001-mvp/`.

## Read these first
- `prompts/README.md` (for archive convention rules)

## Scope
Move the loose prompt files.

## Your task
1. Create `prompts/001-mvp/step-0007/`, `prompts/001-mvp/step-0008/`, and `prompts/001-mvp/step-0009/`.
2. Move all `mine-flow-STEP-7*` files from `Upcoming Prompts/` to `prompts/001-mvp/step-0007/`.
3. Move all `mine-flow-STEP-8*` files from `Upcoming Prompts/` to `prompts/001-mvp/step-0008/`.
4. Move all `mine-flow-STEP-9*` files from `Upcoming Prompts/` to `prompts/001-mvp/step-0009/`.
5. Verify `Upcoming Prompts/` is clean of old files (only STEP-11 files should remain).

## Verification
- List the directories to confirm the files were moved correctly.

## Keeping the docs true  (always)
- Ensure the file structure matches `METHOD.md` §8 conventions.

## Definition of done
- [ ] Old prompt files are archived.
- [ ] `Upcoming Prompts/` only contains `mine-flow-STEP-11*`.

## Next
When this substep is done, update its status in the STEP PLAN, then run the STEP review. Since this is the final Phase 1 polish step, after archiving STEP-11 itself, you will be ready to plan Phase 2.
