# mine-flow — STEP-55.10: Shell, Dashboard, Notifications, Settings, and Auth

> **How to run:** Tell your agent “run substep 55.10”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** This broad utilities pass is tightly specified but combines runtime accessibility, auth/privacy, logging hygiene, routing, localization, and shell behavior.

## Context
Complete STEP-55’s system surfaces after all feature migrations. This substep owns master spec §4.9, including P0 desktop semantics, privacy acknowledgement, and sensitive-header redaction. It must preserve the five-tab mobile contract and existing auth/session safety.

## Read first
- STEP-55 PLAN and 55.0–55.9 findings
- master spec §§2.8–2.9, 4.9, 6–7, 8.3, 9
- Doc 07 v0.5.0; Docs 06, 11, 12, 16, 17; relevant ADRs/risks (especially RISK-0004, 0011, 0019, 0026–0029)
- app README/ARCHITECTURE
- `lib/app/{app.dart,router.dart}`; `app/presentation/pages/{app_shell,dashboard_page}.dart`; `global_app_header.dart`
- notifications, settings, auth presentation/domain/data files; logger/network code
- existing shell/router/dashboard/login/settings/notification tests
- STEP-54.1, 54.10, 54.10a findings

## Impeccable
Run context once; no init/document/extract. Use `layout` for shell/dashboard/breadcrumb hierarchy, native `adapt` for every mobile route, `harden` for auth/loading/error/privacy states, `clarify` only for approved localized copy, and one bounded `polish` cycle. The CanvasKit detector cannot establish quality.

## Task
1. Expose desktop sidebar navigation and global header controls as real runtime accessibility nodes with roles, names, selected/state, focus, and keyboard activation.
2. Keep five mobile tabs; provide stable notification/global-control reachability on every authenticated mobile shell route.
3. Repair group active state, collapsed-sidebar reopen affordance, traversal, and keyboard behavior.
4. Make all four KPI cards semantic actions to declared destinations; add compact workflow shortcuts for the remaining five features without inventing KPIs.
5. Separate loading, failure/retry, first-use CTA, filtered empty, and valid zero states; preserve content during refresh.
6. Preserve notification states/actions and move activation to shared/ForUI tappable behavior.
7. Add `/settings/profile/form` responsive profile edit; display name editable, role visibly server-managed.
8. Preserve Light/Dark/System and locale wiring; make live System brightness changes rebuild.
9. Bind header identity to authenticated user name/localized role with Settings parity; remove hardcoded identity. Simplify logout to plain `FDialog`; await sign-out; configure support contacts.
10. Implement versioned first-login privacy acknowledgement before dashboard access using **approved** Terms/Privacy copy. Permit sign-out. Do not invent or label copy as legally approved.
11. Fix login Done-submit, dismissible/clearing errors, heading, explicit field names, Indonesian Web language, and all sampled 48dp targets.
12. Redact/suppress `Authorization`, `apikey`, cookies, tokens, and similar sensitive headers before any runtime capture. Add regression tests proving raw values never appear.
13. Replace breadcrumbs with centralized canonical navigable ancestors, current-page semantics, query preservation, dirty-sheet interception, and constrained-width overflow.
14. Localize all new copy and preserve narrow justified Material boundaries only.

## Tests
Add/update shell/router/dashboard/notification/settings/auth/logger tests for: AX semantics and keyboard; group/collapse states; 799/800/801; five tabs; notification reachability; KPI/shortcut routes; dashboard state distinctions; notification actions; profile route/authorization; live system theme; locale/document language; header identity parity; logout; privacy version/ack/sign-out/error/re-entry; login keyboard/error/names; breadcrumb mapping/dynamic IDs/query/dirty guard/overflow; sensitive-header redaction including failure logs.

Run focused suites, format, analyze, l10n and contract guards. Perform one Web + Pixel_6a runtime batch in light/dark/system and representative roles, only after redaction tests pass. Produce `mine-flow-STEP-55.10-FINDINGS.md` tracing all §4.9 IDs and user-review requirements.

## Boundaries
No sixth tab, new KPI definitions, legal copy invention, editable role, auth weakening, secret logging, generic localization rewrite, or detector-as-PASS. If approved privacy copy is unavailable, implement/test the versioned gate infrastructure but mark release acceptance blocked/Unverified—never fabricate copy.

Escalate on any raw secret in output, authorization bypass, privacy authority ambiguity, shell semantics absent despite verified source wiring, or repeated failure.

## Definition of done
P0 shell/privacy/logging obligations and §4.9 behavior are implemented/tested; runtime semantics are real; identity/breadcrumbs/routes are truthful; focused/static gates pass; evidence is safe and recorded.

## Next
Run substep 55.11 in a fresh chat.
