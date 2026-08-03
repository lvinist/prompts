# mine-flow — STEP-40.5: Full verification and close

This prompt is self-contained. Execute it directly and independently.

## Context
This is the final verification substep for STEP-40. All 8 test failures from the Phase 2 Tier 2 check-in regression have been fixed in the previous substeps (40.1 through 40.4).

## Implementation Approach
**Fix:** Run the full test suite and static analyzer to ensure zero regressions and zero analyzer issues.
- Run `flutter test` and confirm 100% pass rate.
- Run `flutter analyze` and confirm 0 issues.
- Once verified, archive the STEP by moving the contents of `Upcoming Prompts/` (the PLAN and all PROMPT files) to `prompts/002-phase2/step-0040/`.
- Change the STEP-40 status in `prompts/STEP-index.md` to "Done".

## Files to Touch
- N/A (Verification only, plus file moves and index update)

## Verification Gate
Run these commands to verify the substep is complete:
`flutter test`
`flutter analyze`
