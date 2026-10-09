# mine-flow — STEP-55.0 RESIDUAL-2: localize the drag-handle semantic label

> **How to run:** Tell your agent "run 55.0 residual-2 fix only". Execute cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** Same lane and tier as 55.0 — this edits the shared dismissal primitive file where a bad edit compounds across every feature, even though the fix itself is one l10n key.

## Context

The 2026-09-21 residual review re-verified the 55.0 residual lane against disk: all three dismiss triggers (`drag`, `browserNavigation`, `parentNavigation`) are wired through the one `AppDismissController` path, the one-shot latch and busy/dirty contracts hold, focused 23/23, format/analyze clean, CR bytes 0. That work is complete but was left **uncommitted** — see Pre-flight.

One deviation from the docs was found:

- `_DragHandle` carries a hardcoded user-facing semantic label `'Seret ke bawah untuk menutup'` at `lib/core/presentation/widgets/app_interaction_primitives.dart:549`. The PLAN's ground rules say "New user-facing strings go through localization." The 55.0 residual prompt said "no l10n change expected — if one proves necessary, stop and escalate instead of inventing it." The lane instead invented an Indonesian fallback (its comment: "no sheetDragHandle key exists yet"). The `tool/check_l10n_baseline.dart` guard does **not** scan `lib/core/presentation/`, so the string escaped mechanically — that blind spot is a detection limitation, not authorization.

## Residual scope (exact — nothing else)

1. Add a `sheetDragHandle` key to `lib/l10n/app_id.arb` (`"Seret ke bawah untuk menutup"`) and `lib/l10n/app_en.arb` (`"Drag down to close"`).
2. Regenerate the localization output using the project's gen-l10n workflow (the documented `flutter gen-l10n`/build step; the generated `app_localizations*.dart` files are committed-CRLF **by convention** — new CRLF hunks there are correct, do not normalize them to LF).
3. Swap the hardcoded fallback in `_DragHandle` to the file's existing semantic-fallback pattern: `Localizations.of<AppLocalizations>(context, AppLocalizations)?.sheetDragHandle ?? 'Seret ke bawah untuk menutup'` — identical in shape to the `sheetBarrierLabel`/`sheetClose` fallbacks already in the same file.
4. Optionally pin it: one test case in `test/core/presentation/widgets/app_interaction_primitives_test.dart` asserting the drag handle's `Semantics` label resolves (extend, don't rewrite).

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md` (ground rules: localization, evidence contract)
- `Upcoming Prompts/mine-flow-STEP-55.0-FINDINGS.md` (baseline + residual fix 2026-09-19)
- `lib/core/presentation/widgets/app_interaction_primitives.dart` (the `_DragHandle` build, `sheetBarrierLabel` fallback pattern)
- `lib/l10n/app_id.arb`, `lib/l10n/app_en.arb` (key conventions: camelCase, Indonesian-first)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app` (expect `step-0055-cohesive-ui-rebuild`). Confirm `prompts/` is on `main`.
2. **As of the 2026-09-21 review, the tree carried uncommitted 55.0/55.1 residual lanes** (`app_interaction_primitives.dart` + its test; `router.dart` report-config hunks + `report_config_page.dart` + `app_contextual_report_dialog.dart` + their tests). That work is verified complete (review 2026-09-21). If it is still dirty, commit it FIRST, one commit per owning substep (`fix(55.0): ...`, `fix(55.1): ...`), staged to only each lane's files — or obtain the owner's decision to leave it dirty. Never stash, reset, absorb, or bundle lanes. Start this lane from the cleanest tree you can reach.
3. Preserve the 55.11 untracked files (`.step55.11h-run-web.sh`, `.step55.11i-run-android.sh`, `run_web_wrapper.dart`, `test/widget/m2_challenger_stress_test.dart`, `tool/verify_test_driver_adversarial.dart`). Never commit them.

## Likely files (ownership boundary)

- ALLOWED: `lib/core/presentation/widgets/app_interaction_primitives.dart` (one fallback swap), `lib/l10n/app_id.arb`, `lib/l10n/app_en.arb`, regenerated `app_localizations*.dart`, `test/core/presentation/widgets/app_interaction_primitives_test.dart` (one optional case), `Upcoming Prompts/mine-flow-STEP-55.0-FINDINGS.md` (append only).
- FORBIDDEN: `lib/features/**`, `lib/app/router.dart`, `tool/check_l10n_baseline.dart` (do NOT extend its scan scope in this lane — widening it is a separate owner decision), docs, index.

## Tests and verification

- `flutter test test/core/presentation/widgets/app_interaction_primitives_test.dart`
- `dart format --output=none --set-exit-if-changed <touched files>` (exclude generated l10n files from the changed-count claim if the formatter reflows their CRLF convention — classify per the repo's HEAD convention first)
- `flutter analyze`
- `dart run tool/check_l10n_baseline.dart` (expect pass; note it does not scan `lib/core/` — the proof that the string is localized is the ARB key itself)
- Record exact commands + counts. CR-byte audit both owned non-generated files (expect 0 churn vs HEAD).

## Boundaries and escalation

- No feature migration, no router edit, no visual restyle, no new package, no guard-scope change.
- Stop if gen-l10n is unavailable in this environment (record Unverified, do not hand-edit generated files), or if the same fix fails twice. Never print `.env` or secret values.

## Definition of done

- `sheetDragHandle` key present in both ARBs, generated output regenerated, `_DragHandle` uses the localized fallback with the file's existing pattern; focused + static gates pass; FINDINGS has a dated "Residual fix 2 (55.0)" section with commands/counts and the l10n-escape lesson recorded.

## Next

Report the exact replacement evidence-cell line for index row 55.0 (do **not** edit the index or flip any status yourself). Tell the user to run the 55.1 residual-2 in a fresh chat.
