# mine-flow — STEP-55.3 RESIDUAL: Land Clearing tab sync, FTabs call, cold-ID validation, findings prefix

> **How to run:** Tell your agent "run 55.3 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Same tier as 55.3 — restorable state + inspector reasoning, bounded.

## Context

Land Clearing is migrated on branch `step-0055-cohesive-ui-rebuild` (same `a74b20a` commit as 55.2 — separate commit for this lane, don't bundle). Inspector-before-edit, contextual `ReportType.landClearing` prefill, selection-only method combobox (CF-043, no `onCreateNew`, BLoC rejects out-of-set), and cold-ID load all exist. The audit (2026-09-19, index row 55.3) left five residuals. Fix only those.

## Residual scope (exact — nothing else)

From the index row 55.3:

1. **Two-way tab↔URL sync.** Today `land_clearing_entry_screen.dart:201-213` builds `currentParams['tab']` but never writes it back ("purely UI state"). Make `tab=plan|actual` survive refresh/back/forward mid-edit: tab change replaces the route query (no new history entry per keystroke), route change drives the tab, invalid/missing still defaults to `actual`. Pin with widget tests (invalid tab, refresh reconstruction, back/forward).
2. **Material `TabBar`/`TabController` call.** The file header claims no ForUI equivalent, but pinned ForUI 0.26 ships `FTabs`. Either migrate Plan/Actual to `FTabs` preserving compact density + semantics, or record a one-paragraph justified-interop note (prove the gap: what FTabs lacks for this two-tab form) and keep Material with the existing justification header intact. Owner-visible either way — no silent third option.
3. **Cold-ID validation.** LC `_onInitializeForm` fetches by raw `event.recordId` with no `validRouteRecordId` check (Cut & Fill has it). Add the same validation + recoverable `AppStatePanel` ("Data Tidak Ditemukan" / "Kembali") behavior, pinned by tests (absent extra, invalid ID, not-found).
4. **`FC-54.3-007` runtime audit stays Unverified at this lane** (same 55.11 deferral as 55.2). Add mechanical coverage only (tab semantics, inspector-before-edit routing, summary hierarchy, 48dp, 2x text, light/dark where harness allows).
5. **Findings hygiene.** Rewrite the `FC-55.3-*` checkboxes in `mine-flow-STEP-55.3-FINDINGS.md` to the correct `FC-54.3-001..007` traceability with command counts (do not delete the original section — supersede with a dated residual section).

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md`
- Master spec §§2.6 (D5 tab-as-query), 4.2 (all 7 items), Doc 07 §§3–4
- `Upcoming Prompts/mine-flow-STEP-55.3-FINDINGS.md` (thin baseline to supersede, not erase)
- `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart` (tab controller ~123-213, validation ~161-184), `land_clearing_list_screen.dart` (inspector entry ~134-146), `land_clearing_inspector_screen.dart`, `lib/features/tracking/presentation/bloc/land_clearing/land_clearing_bloc.dart` (`_onInitializeForm`), `lib/app/router.dart` (land-clearing routes only)
- `test/features/tracking/presentation/land_clearing_entry_screen_test.dart`, `land_clearing_entry_screen_deep_link_test.dart`, `land_clearing_bloc_test.dart` (extend)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app`. Preserve untracked 55.11 files and any CF-lane dirt from a sibling 55.2 run. Never stash/reset/absorb.
2. Run the 55.2 residual lane first OR confirm its files are clean — both lanes touch `router.dart` query conventions; serialize, don't interleave.

## Likely files (ownership boundary)

- ALLOWED: `land_clearing_entry_screen.dart`, `land_clearing_list_screen.dart` (only if inspector entry needs touch), `land_clearing_inspector_screen.dart`, `bloc/land_clearing/*` (validation only), router LC-route hunks only (staged-index proof required), LC tests, `Upcoming Prompts/mine-flow-STEP-55.3-FINDINGS.md` (append dated section).
- FORBIDDEN: `cut_fill_*`, reporting dialog internals, other features, `lib/l10n/**` unless a new visible string proves necessary (ARB workflow + guard).

## Tests and verification

- `flutter test test/features/tracking/presentation/land_clearing_entry_screen_test.dart test/features/tracking/presentation/land_clearing_entry_screen_deep_link_test.dart test/features/tracking/presentation/land_clearing_bloc_test.dart`
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- Plus `tool/check_l10n_baseline.dart` if ARB touched, `tool/check_supabase_contracts.dart` (expect pass).
- Record exact commands + counts. ONE commit `fix(55.3): ...`, LC-owned hunks only.

## Boundaries and escalation

- No creatable method values, no Plan/Actual merge, no mobile full page, no schema change. Escalate if existing records can't reconstruct Plan/Actual safely or two attempts fail. Never print secrets.

## Definition of done

- Tab survives refresh/back/forward with invalid→actual fallback; FTabs migrated or justified; LC cold path validates IDs with recoverable panel; `FC-54.3` traceability correct with counts; runtime honestly deferred; gates green; FINDINGS has a dated "Residual fix (55.3)" section.

## Next

Report the exact replacement evidence-cell line for index row 55.3 — including whether the row is now flippable to Done (do **not** flip it yourself). Tell the user the 55.0–55.3 residual set is complete and to review all four FINDINGS addenda.
