# mine-flow — STEP-53 PLAN: Dependency Maintenance — hive_ce / forui / Flutter regression follow-ups

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Gemini 3.7 Flash High (53.1) · Gemini 3.1 Pro High (53.2, 53.3) · Hermes/Claude Opus 4.8 (53.4)
*(Executors only — the user remains the accountable owner per `runbooks/collaboration.md`'s one-owner-per-STEP rule; model tiering does not split ownership.)*
**Status:** In progress
**Date:** 2026-09-10
**Branch:** `step-0053-dependency-maintenance`
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts` (merge order: app → docs → prompts)

> Reconcile the dependency risks surfaced by STEP-50.1 without adding product scope: re-check `hive_ce` maintenance and Dart-4 trajectory, revisit the Flutter/forui semantics regression after Flutter PR #191587 merged, and apply only justified compatible dependency updates. The STEP closes with fresh verification and an honest risk-register record.

## Motivation

STEP-47 completed the major Flutter/dependency overhaul, but the follow-up audit in STEP-50.1 left three bounded items open:

- **RISK-0007:** `hive_ce` is the community fork selected for offline storage after the original Hive packages became unmaintained. Its six-month release-gap trigger fired, so current release health and Dart-4 compatibility need a fresh decision against ADR-0006.
- **RISK-0009:** Flutter issue #191095 was mitigated by the `forui ^0.26.0` pin and finder/workaround patterns. Fix PR #191587 merged to Flutter master on 2026-09-03, but the current local stable is Flutter 3.47.1, so the stable-release trigger must be checked before removing any mitigation.
- **RISK-0020:** the lockfile contains minor direct and transitive drift. Current planning evidence from `flutter pub outdated` shows direct updates for `file_picker`, `flutter_secure_storage`, `go_router`, and `lucide_icons_flutter`, a dev update for `build_runner`, and additional transitive updates; some packages remain constrained by the Flutter SDK.

This STEP is maintenance and verification, not a feature or broad migration. A Hive replacement, Flutter channel change, major dependency upgrade, or broad application refactor is outside scope and must become a separately approved STEP if the audit finds it necessary.

## Decisions already locked

- **ADR-0006 / offline storage:** preserve the repository abstraction and do not replace Hive/hive_ce in this STEP. A migration to Isar, Drift, or another engine requires a separate decision and STEP.
- **RISK register:** update RISK-0007, RISK-0009, and RISK-0020 only from fresh evidence. Keep unresolved risks open/monitoring with a concrete trigger; do not close them because a package resolves or a focused test passes.
- **Dependency runbook:** follow `Code/mine-flow-docs/runbooks/dependency-supply-chain.md` Parts 2–3. Review health, provenance, vulnerability posture, license implications, lockfile synchronization, and unused/deferred dependencies.
- **No blind major upgrades:** do not change the Flutter channel/SDK pin, cross a package major version, remove `forui ^0.26.0`, remove the localizations workaround, or remove RISK-0009 finder patterns without written release evidence and regression verification.
- **No dependency overrides:** retain the STEP-47 outcome of zero `dependency_overrides` unless a separately approved emergency decision exists; do not introduce one to force resolution.
- **Test strategy:** `Code/mine-flow-docs/architecture/12-test-strategy.md` requires analyzer/format, contract and localization guards, unit/integration tests, and the applicable dual-platform E2E/build gates before closure.
- **Secrets boundary:** never read, print, copy, or commit `.env`, CI secret values, tokens, or credentials. Use secret names only; credential-gated runtime checks are `Unverified` when unavailable.
- **Branching:** the execution branch is `step-0053-dependency-maintenance` in every touched repository. The shared `prompts/STEP-index.md` row is updated on `prompts/main`, not on the STEP branch.

## Substeps

| # | Title | Model | Produces | Depends on | Open questions |
|---|---|---|---|---|---|
| 53.1 | `hive_ce` maintenance and Dart-4 trajectory audit (Done) | **Gemini 3.7 Flash High** | Release/maintenance/provenance audit; current compatibility evidence; decision to keep/monitor or raise a separate migration STEP; RISK-0007 recommendation | STEP-52 close | None (audited; release gap 219d active; sdk ^3.4.0 bounds <4.0.0; RISK-0007 monitoring recommended) |
| 53.2 | Flutter #191587 / forui regression follow-up | **Gemini 3.1 Pro High** | Stable-channel fix verification; focused regression test of the existing `forui` mitigation and relevant finder/localization patterns; recommendation on retaining or removing mitigations; RISK-0009 recommendation | 53.1 | Has a stable Flutter release containing #191587 shipped? Can the mitigation be changed without reintroducing the assertion or localization regression? |
| 53.3 | Safe dependency and lockfile maintenance | **Gemini 3.1 Pro High** | Audited compatible manifest/lockfile updates, or a documented no-change result; transitive drift disposition; RISK-0020 recommendation | 53.1, 53.2 | Which updates are compatible with Flutter 3.47.1 and the current app, and which are SDK-pinned or require a separate migration? |
| 53.4 | Verification, risk reconciliation, and STEP close | **Hermes/Claude Opus 4.8** | Fresh gates, final findings and risk updates, docs/readme reconciliation where needed, close record, index/phase/archive updates | 53.1–53.3 | Does the evidence support each risk status and the STEP's completion, or must any item remain open/unverified? |

**Substep status:** 53.1 **Done** (2026-09-10) — `hive_ce` 2.19.3 (2026-02-03) and `hive_ce_flutter` 2.3.4 (2026-01-09) verified against `pubspec.lock`, pub cache, and pub.dev outdated JSON; upstream GitHub repo verified active (PR #314 merged 2026-08-26 for Flutter 3.48 beta); release gap 219 days on pub.dev documented; constraint `^3.4.0` bounded `<4.0.0`; zero advisories; 28 hive_ce and 9 hive_ce_flutter import sites Clean-Architecture compliant; RISK-0007 transition to `monitoring` recommended. Findings: `Upcoming Prompts/mine-flow-STEP-53.1-FINDINGS.md`.

53.2 **Done** (2026-09-10) — Flutter PR #191587 merged to master 2026-09-03; latest stable is 3.47.2 (2026-08-27), which predates the fix; Flutter 3.48 is beta-only; stable-release trigger NOT fired. forui resolved 0.26.0 (pin active). Mitigation sweep complete: 30+ EditableText finder call sites in 10 files; GlobalMaterialLocalizations scope wrapper in inventory_item_entry_screen.dart confirmed. Focused tests 16/16 passed (creatable_combobox_test, creatable_combobox_open_test, inventory_item_entry_screen_test). No source changes. MergeSemantics direct-assertion repro gap documented. RISK-0009 transition to `monitoring` recommended (Trigger A: stable ≥3.48 ships with fix; Trigger B: forui removes material_ui shadow; Trigger C: new forui field added to app). Findings: `Upcoming Prompts/mine-flow-STEP-53.2-FINDINGS.md`.

53.3 **Done** (2026-09-10) — `flutter pub outdated` run pre- and post-upgrade. Targeted `flutter pub upgrade file_picker flutter_secure_storage go_router lucide_icons_flutter build_runner` applied: file_picker 12.1.2→12.2.0 (+ android_file_picker 1.0.3→1.1.1, file_picker_darwin 1.0.4→1.1.0, file_picker_linux 1.0.2→1.1.0, file_picker_platform_interface 3.2.0→3.3.0, file_picker_web 3.0.3→3.1.0, windows_file_picker 1.1.0→1.2.0), flutter_secure_storage 11.0.0→11.1.0 (+ flutter_secure_storage_platform_interface 2.0.3→2.1.0), go_router 18.0.0→18.0.1, lucide_icons_flutter 3.1.17→3.1.19, build_runner 2.16.0→2.16.1. `file_picker_platform_interface` 3.3.0 added abstract method `int? lengthSync()` to `PlatformFile`; `FakePlatformFile` in `upload_file_page_test.dart` updated to implement it. pubspec.yaml unchanged (all within declared `^` ranges). Zero dependency_overrides. Lockfile synchronized. All 5 direct and 7 transitive packages within declared ranges; `archive` 4.0.9 (4.2.0 available) and SDK-pinned transitives (`package_config`, `qr`, `material_color_utilities`, `analyzer`/test family, `_fe_analyzer_shared`) confirmed SDK-pinned — RISK-0020 updated. `dart format` clean (330 files, 0 changed). `flutter test` **550/550 passed**. Findings: `Upcoming Prompts/mine-flow-STEP-53.3-FINDINGS.md`. 53.4 **Done** (2026-09-10) — Final local gates executed: `flutter test` passed (550/550), analyzer clean, formats clean, contract and l10n guards clean. `risks.yml` was reconciled and updated by 53.1-53.3 and verified. App README and architecture docs unchanged. Record written to 53.4-FINDINGS.md. Ready for close.


## Model assignment

The user remains the single accountable STEP owner. The named models are executors selected by failure risk:

| Tier | Substeps | Assignment basis |
|---|---|---|
| Fastest / mechanical | 53.1 | Package-health inventory and release-date/provenance checks are bounded by package metadata, changelogs, ADR-0006, and the risk schema. |
| Mid / bounded reasoning | 53.2–53.3 | These substeps require compatibility and regression judgment, but written authorities (RISK-0009, Flutter issue/release evidence, the Test Strategy, pubspec/lockfile, and runbook) bound the decision. |
| Most capable / closure judgment | 53.4 | The closing executor must distinguish a genuinely fixed dependency risk from a merely passing local test, reconcile Unverified runtime evidence, and write the durable risk/STEP verdict without overstating it. |

Only one substep uses the top tier. Escalate any substep to Opus if a result cannot be classified as package metadata versus application defect, if an accepted ADR appears contradicted, if a security/data-integrity issue appears, if evidence does not support a proposed PASS or risk closure, or if the same fix fails twice. Record the escalation in that substep's findings.

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---|---|---|---|---|---|
| Package resolution / lockfile | 53.3 | None unless an upgrade exposes a compatibility regression | Per 53.3 | `flutter pub get`; `flutter pub outdated`; inspect `pubspec.lock`; verify zero overrides | No major upgrades or forced overrides. |
| Focused regression | 53.2 | Update/add only a focused test if the stable-release decision changes behavior; otherwise exercise existing tests and record no source change | Per 53.2 | Relevant focused tests identified from the RISK-0009 sweep; `flutter test <focused paths>` | Test the semantics assertion, editable-text finder behavior, and localization-scope behavior where applicable. |
| Static analysis and formatting | 53.3, 53.4 | No new tests for dependency-only changes; update tests if behavior changes | 53.3 then final | `dart format --output=none --set-exit-if-changed .`; `flutter analyze` | Must be clean. |
| Contract and localization guards | 53.4 | None | Final | `dart run tool/check_supabase_contracts.dart`; `dart run tool/check_l10n_baseline.dart` | Existing release-readiness gates. |
| Unit / integration | 53.3, 53.4 | Update affected tests only if dependency APIs change | Final | `flutter test` | Full suite is the closure bar; capture exact pass/skip/fail output. |
| Build / E2E | 53.4 | No new E2E unless a dependency change affects a tested surface | Final, if prerequisites exist | `flutter build web --release`; `flutter build apk --debug`; applicable CI E2E gate | Credential/device/tool availability limits must be recorded as Unverified, never inferred as green. |
| Security / supply chain | 53.1–53.4 | No application security feature work | Final | Package provenance/advisory/license review; risk-register diff and YAML parse/check | Use package registry/changelog evidence and the dependency runbook. Do not claim a vulnerability scan if the required tool is unavailable. |

## Open questions

- Q1: Does current evidence justify closing or downgrading RISK-0007, or should it remain open with a migration trigger?
- Q2: Does the current stable Flutter channel include the fix for #191587, and is the existing `forui ^0.26.0` mitigation still required?
- Q3: Which outdated packages can be upgraded safely without major-version migration or Flutter SDK changes?
- Q4: Are any requested runtime/build gates unavailable because of missing credentials, devices, or host tools?

Each question is answered in the owning substep's findings and rechecked by 53.4.

## Ground rules

- Review and dependency maintenance only; no feature work, broad refactors, or storage-engine migration.
- Re-locate paths and symbols on the current branch head; line numbers in prior records are not authoritative.
- Preserve concurrent work. Capture the dirty-file set before editing and never absorb unrelated changes into a dependency commit.
- Keep manifest and lockfile changes together and inspect the exact staged diff before any commit.
- Do not normalize line endings in files outside the current substep's ownership.
- Keep accepted risks visible. Every changed risk row names its evidence and revisit trigger.
- Do not edit accepted ADR decisions in place. Write an amendment/new ADR only if the dependency decision genuinely changes.

## Definition of done

- [x] 53.1 records current `hive_ce` health, release cadence, compatibility/provenance evidence, and an honest RISK-0007 disposition.
- [x] 53.2 verifies the stable Flutter/#191587 state and the existing forui workaround surface; RISK-0009 disposition is evidence-based.
- [x] 53.3 either applies only justified compatible updates with a synchronized lockfile or records why updates are deferred; no blind major upgrade and no dependency override.
- [x] RISK-0007, RISK-0009, and RISK-0020 are updated only when supported by the findings and retain concrete revisit triggers where unresolved.
- [x] `pubspec.yaml` and `pubspec.lock` have no unexplained drift; dependency provenance/advisory/license review is recorded to the extent tools permit.
- [x] Format, analyzer, contract guard, localization guard, and full unit/integration suite pass; build/E2E results are recorded with unavailable prerequisites explicitly marked Unverified.
- [x] No secret values, unrelated files, or concurrent work were included.
- [x] 53.4 produces the close findings record and reconciles the PLAN, findings, index, phase README, and archived STEP files.
- [x] STEP review passes; `prompts/STEP-index.md` is updated and the STEP is archived only after all evidence is reconciled.
