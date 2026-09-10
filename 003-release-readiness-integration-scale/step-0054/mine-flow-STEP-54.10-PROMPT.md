# mine-flow — STEP-54.10: System Utilities — Dashboard, Notifications, Settings & Auth Critique

> **How to run:** Tell your agent *"run substep 54.10"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric; consolidation at 54.11 catches weak findings.

## Context

STEP-54 critiques each feature as a cohesive lifecycle across Web (desktop) and Android. This substep covers the **system utilities**: the Dashboard (KPI cards — the app's landing surface), the Notification center, Settings (profile, locale, theme), and the Login screen. These are not operational data-entry features, so the List → Form → Detail → Report lifecycle lens applies loosely; the rubric's platform-conformance, states, a11y, and token dimensions apply fully. The login screen additionally carries a compliance obligation: the In-app Privacy Notice (RISK-0011; STEP-48 DR-0003 marked it Needs remediation — absent on the login screen).

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**. Apply it exactly; IDs are `FC-54.10-NNN`.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8; blueprint §54.10 names these surfaces
- `Code/mine-flow-docs/reports/2026-08-30-step-0048-runtime-design-review.md` — prior coverage of login/dashboard (mind the retraction amendment)
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0011 (privacy notice), RISK-0004 (l10n migration)
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md`
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head):
- Dashboard: `lib/app/presentation/pages/dashboard_page.dart` (+ `group_landing_page.dart` if KPIs land there — verify)
- Notifications: `lib/features/notifications/presentation/pages/notification_list_page.dart`
- Settings: `lib/features/settings/presentation/pages/settings_page.dart` (note: another `settings_page.dart` exists under `lib/features/settings/presentation/pages/` — verify which is routed)
- Login: `lib/features/auth/presentation/pages/login_page.dart`
- BLoC states: each feature's `presentation/bloc/`

**Does NOT touch:** application code (read-only), other features, the rubric.

## Your task

Apply every 54.1 rubric dimension, both platforms (Web desktop, Android portrait):

1. **Dashboard KPI cards:** which KPIs, from which features, at what cadence; empty/error states when a source feature has no data; tap-through behavior (does a KPI card navigate to its feature? should it?); card density vs. Doc 07's data-dense principle on each platform.
2. **Notification center:** what generates notifications today (verify from the BLoC/data layer — not assumed); read/unread states; empty state; is the center reachable from both shells (sidebar on Web, where on mobile — the 5-tab bar budget)?
3. **Settings:** profile fields and their edit flow (inline vs. sheet — spec against D1/D2 anyway for consistency), locale switcher (RISK-0004 context: ID default; what does switching actually change today — evidence it), theme toggle (light/dark/system — verify all three), and dark-mode correctness of every settings surface.
4. **Login:** form states (loading/error on bad credentials), keyboard behavior on mobile, and **the privacy-notice compliance check**: is the In-app Privacy Notice present in the first-login flow today? Evidence its presence/absence precisely (RISK-0011 / STEP-48 DR-0003 follow-up — this is a named deliverable of this substep).
5. **Cross-cutting:** l10n posture of these surfaces (hardcoded vs. `AppLocalizations` — spot-check with the l10n guard's perspective), token conformance, anchored-grep residual Material.
6. **D7 verdict:** none expected here (no operational detail views) — state "N/A" explicitly rather than silently omitting.

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.10-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, one-sentence why (Explanatory style).
- Runtime optional and honest: name the command, report artifact byte-size + pixel dimensions; 1×1-placeholder class = harness-defect call-out. Unverifiable → `Unverified` + blocker.
- No code changes: app repo `git status` clean at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.10-FINDINGS.md` — coverage table, findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits (54.11 consolidates). Escalate (and record) on: D1–D8/ADR conflicts, runtime contradicting Doc 07, unevidenced runtime claims, same classification problem twice. **Privacy-notice absence** (if still absent) is a compliance finding — escalate it to the user directly, don't leave it buried in a table row.
- Accepted-risk-shaped discoveries go to findings for 54.11's reconciliation.

## Definition of done

- [ ] All rubric dimensions scored for dashboard, notifications, settings, and login, both platforms.
- [ ] Privacy-notice presence/absence evidenced precisely (RISK-0011 / DR-0003 follow-up).
- [ ] Theme/locale switching behavior evidenced (what actually changes).
- [ ] D7 explicitly N/A (or a justified exception).
- [ ] Coverage/findings/verification/limitations tables present with IDs and citations.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.10 → Done) and tell the user: *"run substep 54.11"* — in a **fresh chat**.
