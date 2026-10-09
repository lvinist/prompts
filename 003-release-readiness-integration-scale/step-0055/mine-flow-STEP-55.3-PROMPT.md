# mine-flow — STEP-55.3: Land Clearing Migration and Polish

> **How to run:** Tell your agent “run substep 55.3”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Restorable Plan/Actual state, a read-before-edit inspector, mobile selector behavior, and report integration require bounded design/routing reasoning.

## Context
Migrate Land Clearing to the shared route/sheet/report system while separating inspection from editing. The Plan/Actual state is durable route state; the shared method combobox remains selection-only.

## Read first
STEP-55 PLAN; 55.0–55.2 findings; master spec §§2, 3, 4.2, 5–7; Doc 07; Test Strategy; app README/ARCHITECTURE; `land_clearing_list_screen.dart`, `land_clearing_entry_screen.dart`, widgets/BLoC/domain/repository, router/tests; STEP-54.3 findings.

## Impeccable
Run context once. Use `layout` for Plan/Actual hierarchy and inspector summary, native `adapt` for bottom-sheet/combobox/IME behavior, `harden` for invalid tab/not-found/error states, then bounded `polish` in both themes/platforms.

## Task
- Implement create `/operations/land-clearing/form?tab=plan|actual`, detail `/:id`, and edit `/:id/form?tab=plan|actual`; fetch by ID without `extra`.
- Default invalid/missing tab safely to `actual`; preserve date/zone filters, list state, and focus.
- Use shared responsive sheets and universal dirty guard for create/edit.
- Add route-backed read-only inspector summarizing Plan + Actual; explicit Edit opens edit route. Web right inspector, mobile bottom inspector.
- Keep method selector restricted to enumerated CF-043 options; adapt mobile presentation without arbitrary creation or keyboard occlusion.
- Replace report navigation with bound Land Clearing dialog seeded from date/zone.
- Replace residual Material tabs/date/FAB/fields with shared/ForUI controls while preserving compact density and domain rules.

## Tests and verification
Cover route refresh/back/forward, invalid tab, absent extra, not-found/unauthorized ID, inspector-before-edit, Plan/Actual restoration, all dismissals, selection-only method validation, mobile IME, report context retention, filter/scroll/focus preservation, semantic tabs/summary, 48dp, 2x text, light/dark.

Run focused tracking/router/shared/report tests plus format/analyze/guards. Produce `mine-flow-STEP-55.3-FINDINGS.md` with `FC-54.3-001..007`, artifact metadata, and Unverified blockers.

## Boundaries
Do not make method values creatable, merge Plan and Actual semantics, add a mobile full page, or change data schema. Escalate if existing records cannot reconstruct Plan/Actual safely or two attempts fail.

## Definition of done
Land Clearing list → inspect → edit/create → report is URL-backed, state-preserving, guarded, platform-conformant, tested, and visually polished without domain drift.

## Next
Run substep 55.4 in a fresh chat.
