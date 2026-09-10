# mine-flow — STEP-53.4: Verification, Risk Reconciliation, and STEP Close

> **How to run:** Tell your agent *"run substep 53.4"* (or *"read and run this file"*).
> A substep is self-contained and must be executable cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** This is the only top-tier assignment: it must decide whether dependency risks are genuinely resolved, separate code completion from evidence completion, and write the durable close record without overstating unavailable gates.

## Context

Substeps 53.1–53.3 audit and, where justified, maintain the dependency graph. This closing substep re-derives their claims from disk, runs the final verification gate, updates durable risk/docs records, and closes STEP-53 only if the evidence supports it.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-53-PLAN.md`
- `Upcoming Prompts/mine-flow-STEP-53.1-FINDINGS.md`
- `Upcoming Prompts/mine-flow-STEP-53.2-FINDINGS.md`
- `Upcoming Prompts/mine-flow-STEP-53.3-FINDINGS.md`
- root `.throughstone/local-user.md`
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-app/pubspec.yaml`
- `Code/mine-flow-app/pubspec.lock`
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0007, RISK-0009, RISK-0020
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/architecture/06-security-threat-model.md`
- `Code/mine-flow-docs/runbooks/dependency-supply-chain.md`
- `Code/mine-flow-docs/runbooks/collaboration.md`
- `prompts/STEP-index.md`
- `003-release-readiness-integration-scale/README.md` or the current phase README path

## Scope

Own the final verification and documentation/branch close for STEP-53:

1. Reconcile the findings against the current worktrees, HEADs, staged diff, manifest, and lockfile.
2. Run the final local gates and record exact results.
3. Update `Code/mine-flow-docs/registries/risks.yml` for RISK-0007, RISK-0009, and RISK-0020 only where evidence supports the change.
4. Update the app README or architecture docs only if dependency behavior, setup, or a documented decision actually changed; bump version logs for architecture changes and do not rewrite accepted ADR decisions.
5. Write `Upcoming Prompts/mine-flow-STEP-53.4-FINDINGS.md` as the close record, then update the PLAN progress/DoD, `prompts/STEP-index.md`, and the phase README. Archive PLAN, prompts, and findings under `prompts/003-release-readiness-integration-scale/step-0053/` only after review and evidence reconciliation.
6. Follow the repo merge order and branch rules; do not commit unrelated work or secrets.

Do not invent CI, E2E, package advisory, license, or runtime results. Do not close a risk because a command passed if its trigger concerns release health, stable-channel inclusion, or unavailable external state.

## Verification

Run from the app repository as applicable:

- `git status --short --branch`, `git diff --check`, and exact staged-diff inspection
- `flutter pub get` / `flutter pub outdated`
- `dart format --output=none --set-exit-if-changed .`
- `dart run tool/check_supabase_contracts.dart`
- `dart run tool/check_l10n_baseline.dart`
- `flutter analyze`
- `flutter test`
- `flutter build web --release`
- `flutter build apk --debug` when the Android toolchain and same-drive `PUB_CACHE` prerequisites are available
- applicable CI/E2E gate only when its credentials, browser/driver, emulator, and remote evidence exist

For full-suite failures, re-run the exact failing file in isolation, then repeat the full suite once before classifying an order-dependent failure as a flake. Report the full-suite and isolated results separately. A focused pass is not a full-gate pass. If a runtime gate is unavailable, write `Unverified` with the missing prerequisite and handoff; never substitute static evidence.

Before any external push or close claim, verify repository topology, branch heads, the intended staged file set, and that `prompts/main` has no duplicate STEP numbers. Read back the exact target state after state-changing writes.

## Definition of done

- [ ] Final gate results are fresh, exact, and tied to the current commit; unavailable surfaces are explicitly Unverified.
- [ ] RISK-0007, RISK-0009, and RISK-0020 records agree with the findings and retain triggers for unresolved work.
- [ ] Manifest/lockfile, README/architecture docs, PLAN, findings, index, and phase README are mutually consistent.
- [ ] No secret values, unrelated files, or concurrent work were included.
- [ ] STEP review and `git diff --check` pass; archive contains the complete STEP record.
- [ ] Branches and shared `prompts/main` are synchronized according to the collaboration rules.
- [ ] The final response names the next action and tells the user to start a fresh chat.

## Next

After a verified close, run `doctor.sh status` and tell the user the next planned STEP in a fresh chat. If closure is blocked, record the exact blocker and keep STEP-53 In progress.
