# mine-flow — STEP-55.0: Shared Responsive Interaction Foundation

> **How to run:** Tell your agent “run substep 55.0”. Execute cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** This substep defines the route and dismissal invariants inherited by every feature; a quiet mistake can lose user input or create systemic navigation drift.

## Context
STEP-55 implements the approved STEP-54 master polish specification. This substep owns pre-flight/branch setup and the shared D1–D5 interaction foundation. It does not migrate individual feature pages beyond the minimum fixtures needed to prove the shared contract.

## Read first
- root `AGENTS.md`, `.throughstone/local-user.md`
- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md`
- `Code/mine-flow-docs/reports/2026-09-11-step-54-master-polish-spec.md` §§1–2, 6–7, 9
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` v0.5.0
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/architecture/11-interface-contracts.md`
- `Code/mine-flow-app/README.md`, `ARCHITECTURE.md`
- `Code/mine-flow-app/lib/app/router.dart`
- existing shared widgets under `lib/core/presentation/widgets/`
- archived `prompts/.../step-0054/mine-flow-STEP-54.1-FINDINGS.md` and `54.10a-FINDINGS.md`

## Impeccable
Run `impeccable context` once from the app root. Treat `NO_PRODUCT_MD`/CanvasKit no-signal as known. Do not run `init`, `document`, or `extract`. Apply the `layout`, native `adapt`, and `harden` playbooks to the shared components. Finish with one bounded `polish` pass over the fixture path. Mechanical detection is supplemental only.

## Scope
1. Reconcile clean/upstream-synchronized app/docs/prompts trunks, duplicate STEP scan, overlap check, and baseline gates. Cut `step-0055-cohesive-ui-rebuild` in app/docs and flip STEP-55 to In progress on `prompts/main` only after the gate is clean.
2. Implement canonical shared widgets (names may vary only if one documented equivalent exists):
   - `AppResponsiveSheet<T>` with form/read-only/selection modes;
   - `AppDirtyDismissDialog` and one `requestDismiss(reason)` state path;
   - `AppDetailInspector` with approved mobile-full-page override;
   - `AppFilterPopover` and `AppCalendarDialog`;
   - `AppStatusBadge`, `AppSyncStatusBadge`, `AppAccessibleIconButton`, `AppStatePanel`, and `AppPlatformSelect` where not already supplied by ForUI.
3. Add route-host/adapter support so URL state owns open sheet/detail state; `extra` is optional cache only.
4. Implement Web >=800 right-sheet and Android/narrow <800 bottom-sheet geometry, focus, barrier, scroll, IME, safe-area, back, reduced-motion, and 48dp behavior exactly as master spec §2.
5. Add localized exact dirty-dialog copy and modal semantics.
6. Create a minimal test fixture route/screen; do not migrate production features here.

## Likely files
- Create under `lib/core/presentation/widgets/` and `test/core/presentation/widgets/`
- Modify `lib/app/router.dart` only for reusable hosting/fixture support
- Modify ARB/generated localization via the project workflow
- Update app README/architecture only if reusable component conventions or commands become newly true

## Tests and verification
Write failing tests before behavior, then implement. Cover every dismissal reason in clean/dirty/busy states; one pending pop only; discard/continue focus; direct route reconstruction; invalid/unauthorized/not-found fallback contract; 799/800/801 and 1024/1280 geometry; modal barrier/inert background; body-only scroll; Android back/drag/IME; filter apply/reset/cancel; calendar bounds/range/cancel; 48dp and semantic labels; light/dark and text scaling.

Run focused shared/router tests, `dart format --output=none --set-exit-if-changed .`, `flutter analyze`, and relevant localization/contract guards. Record actual commands/counts in `mine-flow-STEP-55.0-FINDINGS.md`. Capture representative Web and Pixel_6a evidence when credentials are not needed; report blockers as Unverified.

## Boundaries and escalation
- No feature migration, schema work, generic design refresh, or new package.
- Stop if baseline/branches differ, dirty work exists, ForUI cannot meet a locked interaction without a material workaround, or route-pop behavior fails twice.
- Never print `.env` or secret values.

## Definition of done
- Shared components meet master spec §2 and are testable independently.
- All close paths use one guard and exactly one route pop.
- URL reconstruction and list-state preservation contracts are pinned by tests.
- Focused/static gates pass; findings and PLAN row are updated.

## Next
Tell the user to run substep 55.1 in a fresh chat.
