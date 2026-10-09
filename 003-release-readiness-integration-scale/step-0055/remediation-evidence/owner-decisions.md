# STEP-55 remediation — owner decisions, 2026-10-04

Source: explicit desktop clarification responses in the current remediation session.

- Privacy: user reviewed the exact `privacyCardBody` in both `lib/l10n/app_id.arb` and `app_en.arb`, with the acknowledge button labels, and **approved both versions as accountable product owner**. This is product-owner copy approval, NOT independent legal validation or verification that retention/deletion mechanisms implement the notice.
- RISK-0025: authorized preparing and locally testing the role-escalation security fix. Live deployment requires separate approval. Unresolved authorization semantics remain owner-gated.
- STEP-56: authorized preparing the staging-only zone-seed follow-up; do not apply it.
- Database: read-only inspection authorized. Ask before ANY database write; no migration apply, seed, remote authorization attack, or destructive test is authorized by this decision.
- Closure: keep STEP-55 **In progress until every required gate is satisfied**. No conditional Done, archive/merge/branch deletion, or release approval inferred.

- E2E environment follow-up: user confirmed project `rpdnonpivoyhghzolyzv` (mine-flow) is **test-only** and explicitly allowed normal E2E synthetic fixture writes. This does NOT authorize schema migration deployment, zone seeding, or live security attack tests.

- RISK-0025 authorization contract: user approved non-supervisor self-update allow-list **name, phone, emergency_contact_name, emergency_contact_phone**. Protect role, site, activation/deletion status, identity fields and other non-allow-listed data; preserve existing supervisor account-management rights. Local regression tests only until separate deployment approval.

## Pre-flight

- App `03180ec3c69d89531fd77fb0e9d77bd8ac59e275`, docs `092b222`, prompts `d106c9e`; fetched origin and all upstream divergence checks were `0 0`.
- App dirty files: `lib/l10n/app_localizations{,_en,_id}.dart` are EOL-only (`git diff -w --stat` empty). Preserve backups before restoring as explicitly scoped in RESIDUAL-3. Untracked scratch runners, JSON, CI captures, and `tool/verify_test_driver_adversarial.dart` excluded.
- Docs untracked historical `reports/design-review/step-0055/` artifacts preserved.
- Prompts pre-existing two-hunk `STEP-index.md` diff is NOT entirely accurate: intro still says awaiting run 139; row claims 0/25 while residual evidence claims 2/25. Preserve baseline; reconcile rather than blindly commit.
- Exact-head GitHub query found CI run 139 / `37003629360`, completed `failure`.
- Capture prompt count is stale: existing matrix derives Web **73** = login + 3 widths × 2 themes × 2 locales × 6 screens; Android **25** = login + 1 width × 2 themes × 2 locales × 6 screens. Do not reduce coverage to make the prompt's 25-Web assertion pass.

## 2026-10-06 timestamp decision gate

- Owner selected **keep client event time separately and make ledger `created_at` server-authored**. Prepare and verify the migration locally first; deployment still requires separate approval. Follow-up: preserve existing ledger `created_at` values and explicitly mark them as legacy client timestamps. Do not null or fabricate historical server times.
- Owner selected **keep client-authored inventory-item creation time and document that contract**. Item `created_at` is intentionally not a server audit timestamp; no item timestamp behavior change is authorized or needed for this choice.

## Execution boundaries

Implementation serialized. Parallel agents are read-only investigators, with no test/device/remote activity. Source fixes require observed regression RED→GREEN. Preserve historical finding bodies and append corrections. No unrelated scratch absorption, EOL normalization, or rollback of dependencies.
