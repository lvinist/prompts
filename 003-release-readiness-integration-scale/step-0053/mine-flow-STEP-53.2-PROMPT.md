# mine-flow — STEP-53.2: Flutter #191587 / forui Regression Follow-up

> **How to run:** Tell your agent *"run substep 53.2"* (or *"read and run this file"*).
> A substep is self-contained and must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** This substep needs compatibility judgment across Flutter, forui, semantics, finder patterns, and localization, but the accepted risk and existing code/tests bound the decision. Escalate to Opus on contradictory runtime evidence or a proposed workaround removal that cannot be proven.

## Context

RISK-0009 tracks Flutter issue #191095, where focusing a text field under a `MergeSemantics` subtree triggered an `isMergedIntoParent` assertion. The project mitigated it by pinning `forui ^0.26.0`, using `EditableText`-based finders in affected tests, and retaining a material-localizations scope workaround around the inventory-entry unit dropdown. Flutter fix PR #191587 merged to Flutter master on 2026-09-03, but STEP-50.1 recorded that no stable release containing it had shipped at that time. The local toolchain is Flutter 3.47.1 / Dart 3.13.1.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-53-PLAN.md`
- root `.throughstone/local-user.md`
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-app/pubspec.yaml`
- `Code/mine-flow-app/pubspec.lock`
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0009
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- Relevant affected files found by searching for `RISK-0009`, `EditableText`, `MergeSemantics`, and the localization workaround; re-locate them on the current branch head.
- `https://github.com/flutter/flutter/issues/191095`
- Flutter PR/release evidence for #191587 and the current stable channel

## Scope

Own:

1. Determine whether a stable Flutter release containing #191587 is available and whether the local project uses it.
2. Re-test the current forui/semantics mitigation at the focused test surface without weakening assertions.
3. Decide whether the pin and workarounds must remain, can be narrowed, or can be removed. Removal is allowed only when the stable release and focused regression evidence support it.
4. Record a RISK-0009 recommendation.

Do not upgrade Flutter, change the forui constraint, remove finder/workaround code, or perform broad UI refactoring in this substep unless the PLAN's scope is amended from fresh evidence. Do not turn a driver-level pass or a skipped credential-gated E2E into semantics evidence.

## Your task

- Capture the stable-channel/release evidence and exact current versions in `Upcoming Prompts/mine-flow-STEP-53.2-FINDINGS.md`.
- Search the full app and tests for the mitigation class, not just the file/line named in prior notes.
- Identify the smallest focused tests that exercise text-field focus, forui field semantics, the inventory unit dropdown localization scope, and the relevant finder behavior.
- Run those tests on the current tree. If no test directly exercises one behavior, state that gap rather than claiming coverage.
- Make no source change by default. If a safe compatibility edit is genuinely required and explicitly within the amended scope, add a regression test and document the exact diff and reason; otherwise hand it to 53.3/53.4 as a recommendation.

## Verification

- Run `flutter --version` and `flutter pub deps --style=compact`.
- Run the identified focused tests with `flutter test <exact paths>` and capture the real pass/fail/skip output.
- Run `flutter analyze` only if source changes are made; otherwise record that this substep is code-unchanged.
- Verify the current `forui` resolved version in `pubspec.lock`.
- Check whether the stable release evidence actually includes #191587; an upstream merge alone is insufficient.
- If credentials, Chrome, emulator, or a required host tool is missing, mark that runtime surface Unverified and do not substitute a local static pass.

## Definition of done

- [ ] Stable-release status for #191587 is evidenced or explicitly Unverified.
- [ ] Existing mitigation patterns were swept and focused behavior was tested where possible.
- [ ] Any source change has a regression test and exact verification output; otherwise source remains unchanged.
- [ ] RISK-0009 recommendation is evidence-based and includes a revisit trigger.
- [ ] Findings distinguish test execution, skipped tests, and unavailable runtime evidence.

## Next

Update the STEP-53 PLAN progress row with the findings, then run substep 53.3 in a fresh chat.
