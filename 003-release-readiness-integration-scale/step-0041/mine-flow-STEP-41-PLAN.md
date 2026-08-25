# mine-flow — STEP-41 PLAN: Release-Readiness Reconciliation & Contract Baseline

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Antigravity
**Status:** Done
**Date:** 2026-08-06
**Branch:** `step-0041-release-readiness-baseline`
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts` (completion archive only)

> Establish a trustworthy, reproducible release-readiness baseline after Phase 2. This STEP inventories the actual Flutter/Supabase contract and localization state, closes the minimum automation gaps needed to detect future drift, and records evidence plus deferred gaps. It deliberately does **not** provision staging, deploy, change production infrastructure, run a production-data test, or perform the full Indonesian-string migration; those responsibilities remain in STEPs 42–44.

## Motivation

Phase 2 completed the ForUI rebuild and restored a clean automated test baseline (STEP-40). The Phase 2 release notes explicitly leave generated Supabase contract enforcement, full localization implementation, staging, security/privacy baseline work, and runtime E2E/design-review evidence to Phase 3.

The architecture already requires schema changes to regenerate checked-in Dart types and compile in the same change (`architecture/11-interface-contracts.md`), while Doc 07 requires Indonesian user-facing strings to use a localization layer. The repository has:

- **Contract gate (41.2 work is partially done):** `tool/check_supabase_contracts.dart` and a CI step exist and run. The generated type artifact (`lib/core/data/models/generated/database.dart`) does not yet exist — the guard correctly boots with a WARNING + exit(0) until a non-production Supabase project is provisioned. This needs verification and documentation.
- **Localization (41.3 work is zero):** `pubspec.yaml` has `generate: true` and `intl` declared, but `l10n.yaml`, ARB catalogs, and a generated `AppLocalizations` delegate are entirely absent. App delegates are only the Flutter global (`GlobalMaterialLocalizations` etc.). UI strings are hardcoded Indonesian/English.

This STEP converts those known gaps into an evidence-backed baseline that later STEPs can build on.

## Current repository state (as of 2026-08-06)

- **`Code/mine-flow-app`**: on `step-0041-release-readiness-baseline`, clean worktree. Flutter 3.44.5, Dart 3.12.2.
- **`Code/mine-flow-docs`**: on `step-0041-release-readiness-baseline`, clean worktree.
- **`prompts`**: on `main`, STEP-41 row committed and flipped to `In progress`.
- **Supabase CLI**: Not installed locally. Blocks live `supabase gen types dart`. STEP-42 owner must install/configure.
- **Partial report draft**: `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md` exists as a draft from a prior session — it must be completed/finalized by STEP-41.4, not recreated.

## Decisions already locked

- `architecture/11-interface-contracts.md` §§2–4, 9–10 — PostgreSQL migrations are the App↔Supabase source of truth; `supabase gen types dart` is the contract-generation mechanism; schema changes require regenerated types and a successful app compile in the same change.
- `architecture/12-test-strategy.md` §§1, 5–6 — mock external boundaries for unit/integration tests; `flutter analyze`, `flutter test`, formatting, and a successful build are the CI gates.
- `architecture/07-ui-design-system.md` §§4–6 — Indonesian is the MVP default, all user-facing strings must route through a localization layer. Locale selection widget exists; `AppLocalizations` delegate does not.
- `architecture/09-environments.md` — staging is a STEP-42 concern. STEP-41 must not create/configure Supabase projects, secrets, GitHub environments, deployments, or seed real data.
- `architecture/06-security-threat-model.md` — keep secrets out of source control.
- `ADR-0008-impeccable-bridge.md` — `DESIGN.md`/`PRODUCT.md` are generated bridge files; do not edit them directly.
- `registries/risks.yml` — any newly accepted release-readiness gap needs a durable evidence source first, then a concise risk-register row.

## Scope boundaries

### In scope
1. Verify, test, and document the existing `tool/check_supabase_contracts.dart` + CI gate from the prior session.
2. Establish a minimal Flutter `l10n.yaml` + baseline ARB scaffold, a deterministic regression guard, and focused tests — without bulk-translating screens.
3. Fresh `dart format`, `flutter analyze`, `flutter test` results.
4. Finalize the reconciliation report and update docs/risks where justified by evidence.

### Explicitly out of scope
- Live `supabase gen types dart` execution (CLI not installed; deferred to STEP-42).
- Translating all screens, adding languages beyond Indonesian/English, or claiming full localization.
- Editing `DESIGN.md`, `PRODUCT.md`, historical archived STEP artifacts, or unrelated Phase 2 code.
- Staging provisioning, production release, or runtime E2E.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 41.1 | Verify inventory report and repository baseline | Updated/completed draft at `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md` | Clean worktrees (confirmed) | None — state is known |
| 41.2 | Verify and document Supabase contract gate | Verified `tool/check_supabase_contracts.dart`; updated Doc 11 if needed; report rows updated | 41.1 baseline confirmed | Live generation unverified until STEP-42 |
| 41.3 | Localization compliance baseline and regression guard | `lib/l10n/app_id.arb`, `lib/l10n/app_en.arb`, `l10n.yaml`, `tool/check_l10n_baseline.dart`, focused tests | 41.1 identifies localization gap | Whether `generate: true` without `l10n.yaml` causes build issues (check first before creating) |
| 41.4 | Fresh baseline verification and reconciliation close | Updated final report; appropriate doc/version-log and risk changes; verified commands/results | 41.2–41.3 complete | Build smoke gate requires `--dart-define` secrets → record as Unverified |
| 41.5 | Audit Fix — Guard Correctness & CI Hardening | Fixed `tool/check_l10n_baseline.dart` (regex, endsWith, ghost comment), `tool/check_supabase_contracts.dart` (porcelain parser), `ci.yml` (fetch-depth: 2), double-quote fixture test, report closure | 41.4 archived | None — fixes are narrowly scoped to post-impl audit findings |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Tool / script | 41.2 | Dart test or fixture proving guard detects missing artifact and stale artifact | Per substep | `dart run tool/check_supabase_contracts.dart` (passing case); temp fixture for failing case | No network, no secrets |
| Localization / unit | 41.3 | Widget/unit test: app locale config; ARB round-trip; guard pass + intentional-fail fixture | Per substep | Focused: `flutter test test/app/` or new `test/l10n/` suite | Must run without emulator |
| Full regression | 41.4 | All existing tests plus 41.2–41.3 additions | Final | `dart format --output=none --set-exit-if-changed lib/ test/`; `flutter analyze`; `flutter test` | Record actual counts |
| Build smoke | 41.4 | Android debug APK | Final | `flutter build apk --debug --dart-define=SUPABASE_URL=... ...` | **Unverified locally** (secrets required); document exact CI job |
| E2E / staging | N/A | None | Deferred to STEP-42/44 | N/A | Staging does not yet exist |

## Open questions

- **Q1 — Contract source access:** Owner must decide whether to provide a safe non-production Supabase project reference so 41.2 can run live type generation, or confirm STEP-42 is the right moment. STEP-41 records the command/template and marks live generation Unverified.
- **Q2 — l10n.yaml path:** Confirm whether `lib/l10n/` is the correct ARB directory (Flutter convention) or if a project-specific location is preferred. Default to Flutter convention unless an existing contrary convention is found.

## Ground rules

- **Evidence over assertion.** Every report finding must cite a path, command, revision, and actual result. Never synthesize a green build, generated type file, localization coverage, or remote validation.
- **No secret access or leakage.** Do not inspect `.env`, print secret-bearing command lines, or use service-role credentials.
- **Minimal, additive automation.** No new packages unless existing Flutter/Dart tooling cannot meet the need.
- **No false localization completion.** Establish visibility and a migration seam only; broad string replacement is a separately planned future STEP.
- **Calibrate from root `.throughstone/local-user.md`.**

## Definition of done

- [x] The contract gate (`tool/check_supabase_contracts.dart` + CI) is verified, documented, and its Unverified live-generation status is explicitly recorded with STEP-42 as owner.
- [x] A minimal Flutter `l10n.yaml`, baseline ARB files, and a deterministic regression guard are committed, with focused tests proving locale config and guard pass/fail behavior.
- [x] Fresh `dart format`, `flutter analyze`, `flutter test` results are recorded in the reconciliation report with actual counts.
- [x] The reconciliation report is complete: evidence-backed matrix rows, contract/l10n baselines, explicit STEPs 42/43/44 handoffs.
- [x] Architecture docs, CI, README, and `registries/risks.yml` match verified reality.
- [x] **41.5:** l10n guard regex fixed (ISSUE-4), CI fetch-depth hardened (ISSUE-8), guard robustness fixes (ISSUE-1/5/6), double-quote test added, report appended.
- [x] STEP review passed; `prompts/STEP-index.md` updated; STEP archived to `prompts/`.
