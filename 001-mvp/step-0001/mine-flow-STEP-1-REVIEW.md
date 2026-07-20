# mine-flow — Cross-Cutting Review (Session 1.14)

**Date:** 2026-07-18
**STEP:** 1.14 (Cross-Cutting Review)

## 1. Scope Checked
- Read local-user profile (`.throughstone/local-user.md`).
- Read `overview.md`.
- Read all 16 architecture docs and 5 ADRs.
- Read all 3 conditional session templates (`conditional-identity-auth.md`, `conditional-native-app.md`, `conditional-privacy-compliance.md`).
- Checked STEP-1 PLAN and `prompts/STEP-index.md`.

## 2. Conditional-Session Gate
- **Native App Architecture (1.3a):** Complete.
- **Identity & Auth (1.6a):** Complete.
- **Privacy, Compliance & Data Governance (1.6b):** Complete.
All applicable conditional sessions were properly scoped in the PLAN, executed, and their outputs verified.

## 3. Findings & Fixes Applied
1. **Supervisor User Creation Gap (High):**
   - *Finding:* Client SDK cannot securely create users in Supabase Auth without the `service_role` key.
   - *Fix Applied:* Updated `16-identity-auth.md` and `08-infrastructure-deployment.md` to explicitly state that an Edge Function is required for Supervisor account creation.
2. **Missing `site_id` in Data Model (Medium):**
   - *Finding:* Phase 2 requirements (and `02-phasing-roadmap.md`) mandate multi-site readiness, but `04-data-model.md` omitted the `site_id` field.
   - *Fix Applied:* Added `site_id` as a required dimension for all operational entities in `04-data-model.md` and bumped the version.
3. **Missing ADRs (Medium):**
   - *Finding:* Foundational decisions had not been documented as formal Architecture Decision Records.
   - *Fix Applied:* Drafted and registered 5 ADRs: Flutter/Clean Architecture (0001), Supabase (0002), Google Drive (0003), Offline-First Sync (0004), and Supabase RLS (0005).
4. **Index Missing (Low):**
   - *Finding:* `architecture/README.md` was not populated.
   - *Fix Applied:* Populated the architecture index table.

## 4. Open Questions Carried Forward
- **OQ-1:** What is the detailed internal folder structure for Clean Architecture in Flutter? (Carried forward to implementation planning).

## 5. Next Steps
- STEP-1 (Architecture) is now fully complete and ready to be archived.
- Start a fresh chat and run the **implementation planning session** (`templates/planning-session.md`, *"Run planning session: Phase-1 implementation roadmap"*) to outline the Phase-1 implementation STEPs.
