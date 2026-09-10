# mine-flow — STEP-53.3: Safe Dependency and Lockfile Maintenance

> **How to run:** Tell your agent *"run substep 53.3"* (or *"read and run this file"*).
> A substep is self-contained and must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** This is a bounded dependency upgrade with compatibility and lockfile reasoning. Escalate to Opus for a major upgrade, a security/provenance concern, an unexpected application behavior change, or a conflict with ADR-0006/RISK-0009.

## Context

STEP-50.1 and the current `flutter pub outdated` output identify minor dependency drift after the STEP-47 major sweep. At planning time, the app resolves direct updates for `file_picker`, `flutter_secure_storage`, `go_router`, and `lucide_icons_flutter`, a dev update for `build_runner`, and multiple transitive updates; `archive`, `package_config`, `qr`, material/analyzer/test families, and related packages remain constrained in part by Flutter SDK requirements. The app is on Flutter 3.47.1 / Dart 3.13.1 and must retain zero dependency overrides.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-53-PLAN.md`
- root `.throughstone/local-user.md`
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-app/pubspec.yaml`
- `Code/mine-flow-app/pubspec.lock`
- `Code/mine-flow-docs/runbooks/dependency-supply-chain.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/architecture/06-security-threat-model.md`
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0007, RISK-0009, RISK-0020
- `Code/mine-flow-app/tool/check_supabase_contracts.dart`
- `Code/mine-flow-app/tool/check_l10n_baseline.dart`
- The completed 53.1 and 53.2 findings files, if present

## Scope

Own only justified compatible dependency maintenance in `mine-flow-app`:

1. Re-check `flutter pub outdated`, package changelogs/provenance, current SDK constraints, and the 53.1/53.2 recommendations.
2. Apply safe patch/minor updates that remain within the existing declared major ranges and do not require a Flutter SDK/channel change.
3. Keep `pubspec.yaml` and `pubspec.lock` synchronized and preserve zero `dependency_overrides`.
4. Update affected tests only when an actual dependency API or behavior change requires it.
5. Produce `Upcoming Prompts/mine-flow-STEP-53.3-FINDINGS.md` with the exact package changes, deferred updates, and RISK-0020 recommendation.

Do not perform a Hive-to-another-engine migration, major package migration, Flutter SDK upgrade, broad application refactor, or workaround removal merely to make resolution succeed. If an update needs one of those actions, leave it deferred and escalate.

## Your task

- Capture the pre-edit branch, HEAD, status, and dirty-file set. Preserve unrelated work byte-for-byte.
- Run `flutter pub outdated` and inspect the manifest/lockfile before editing.
- Vet each candidate under the dependency runbook: canonical package, maintenance signal, license/provenance, advisories where tooling is available, SDK compatibility, and transitive impact.
- Apply only the smallest compatible set. Prefer targeted `flutter pub upgrade <packages>` or an equivalent reproducible command over an unconstrained graph rewrite.
- Review the lockfile diff for unexpected packages, major-version changes, source changes, or dependency overrides.
- If any update changes app behavior, add/update the narrow regression test before handing off. Do not silently absorb source fixes into a dependency-only commit.

## Verification

Run and capture:

- `flutter pub get` (or the targeted upgrade command used)
- `flutter pub outdated`
- `flutter pub deps --style=compact`
- `git diff -- pubspec.yaml pubspec.lock`
- `dart format --output=none --set-exit-if-changed .`
- Focused tests for any changed surface
- `flutter analyze` if source or generated files changed

Do not claim vulnerability scanning, license scanning, or runtime E2E coverage unless the relevant tool/gate actually ran. Never read or print `.env` values. If dependency resolution fails twice for the same reason, stop and escalate.

## Definition of done

- [ ] Every manifest/lockfile change has a recorded reason and package-source evidence.
- [ ] No unapproved major upgrade, Flutter SDK change, or dependency override was introduced.
- [ ] Lockfile is synchronized and unexpected transitive churn is explained or reverted.
- [ ] Affected tests and static checks pass, or the exact failure is recorded and escalated.
- [ ] RISK-0020 recommendation distinguishes resolved drift from SDK-pinned residuals.
- [ ] Unrelated/concurrent files were not staged or modified.

## Next

Update the STEP-53 PLAN progress row with the findings, then run substep 53.4 in a fresh chat.
