# mine-flow — STEP-39.6: Full verification, check-in report, review, and archival

> **How to run:** Tell your agent *"run substep 39.6"* (or *"read and run this file"*).

## Context
This is the final substep. It runs all validation gates, writes the durable check-in report, and archives the STEP.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-39-PLAN.md`
- `Code/mine-flow-docs/runbooks/check-in.md`

## Scope
Verification and reporting only.

## Your task
1. Execute the full verification gate defined in the PLAN. Ensure all steps pass cleanly.
2. Verify that all DoD items in the PLAN are complete and evidenced.
3. Write the durable check-in report to `Code/mine-flow-docs/reports/2026-07-28-phase2-tier2-check-in-report.md`.
4. Perform the final STEP review.
5. Update `prompts/STEP-index.md` to mark STEP-39 as Done.
6. Archive the STEP by moving all loose files from `Upcoming Prompts/` to `prompts/002-phase2/step-0039/`.
7. Commit and push the final branch state.

## Verification
- **Run these commands:**
  - `cd Code/mine-flow-app`
  - `flutter pub get`
  - `flutter analyze`
  - `flutter test` (must discover and run every test, no skipped files)
  - `flutter build apk --debug`
  - `cd ../.. && ./Code/mine-flow-docs/scripts/doctor.sh status`
  - `./Code/mine-flow-docs/scripts/doctor.sh check`
  - `git status` (for every repo touched)
- Check for duplicate STEP/ADR numbers in `STEP-index.md` and `adr/README.md`.
- Verify the generated bridge files contain only the expected changes.
- Review `risks.yml` one last time.

## Keeping the docs true
N/A

## Definition of done
- [ ] Verification gates passed.
- [ ] Durable check-in report saved.
- [ ] STEP reviewed.
- [ ] STEP archived.
- [ ] `prompts/STEP-index.md` updated to Done.

## Next
Tell the user that STEP-39 is fully complete, archived, and ready for merging.
