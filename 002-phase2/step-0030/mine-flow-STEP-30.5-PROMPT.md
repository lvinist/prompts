# Substep 30.5: Analyzer Clean-up

**Scope:** Global workspace.

## 1. Audit
- Run `flutter analyze` and enumerate all 32 issues by file and category (error/warning/info), not just the errors.

## 2. Fix
- Fix each issue found in the audit. 
- Where a fix would touch code outside STEP-30's scope (e.g. a pre-existing issue STEP-30 didn't introduce, surfaced incidentally), flag it explicitly in the PLAN rather than silently fixing or silently skipping it — so I can decide whether it's in scope.

## 3. Verify
- Re-run `flutter analyze` and confirm 0 issues before this substep is considered done.
- Re-run the full test suite (`flutter test`) to confirm the clean-up didn't regress anything STEP-30's earlier substeps already verified.
