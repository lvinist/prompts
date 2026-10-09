# mine-flow — STEP-55.8 RESIDUAL-2 PROMPT — inventory static defects (verify-then-fix)

**Assigned model:** Gemini 3.1 Pro High (mid tier — bounded fixes pinned by
existing domain tests; schema/policy questions are escalation-triggered, not
inferred).
**Date drafted:** 2026-10-03, by Hermes parent session. Facts re-derived on disk
at head `03180ec`; line numbers are as-of-drafting — re-locate at branch head.
**Branch:** `step-0055-cohesive-ui-rebuild` (app). Serialized with any lane
touching `lib/l10n/` or `tool/check_l10n_baseline.dart`.

## Why this exists

The 2026-09-23 audit and the STEP-index row for 55.8 name three static defects
left open by the 55.8 lane. Two still reproduce in source at head `03180ec`;
one may be stale. Each item below is **verify first** — if already fixed or
superseded at HEAD, record that with file:line evidence instead of re-implementing
(the lane may be verification-only).

## Residual scope (exact — nothing else)

1. **Cold-edit mints a new UUID.**
   `lib/features/tracking/presentation/bloc/inventory/inventory_bloc.dart:82` —
   form init builds `event.existingItem ?? InventoryItem(id: _uuid.v4(), ...)`.
   If any edit entry point launches the form without `existingItem` (cold edit),
   the "edit" persists a brand-new id and orphans the original row. Verify every
   entry point (item sheets/routes from 55.8) passes the existing item; if a cold
   path exists, fix by loading by id, and pin with a RED→GREEN bloc test that
   cold-edits an existing item and asserts the id is preserved.
2. **Client-authored `createdAt` on item form-init.**
   Same file, `:89` — `createdAt: DateTime.now()` on the locally-minted draft
   item. Verify whether `inventory_items.created_at` has a server default and
   whether any ledger path can persist the client value (the
   `inventory_transactions` ledger is server-timestamped via the RPC — do not
   conflate the two). A schema change is NOT authorized here: record the
   disposition honestly (client-value-accepted-with-justification vs
   owner-gated server-default migration) and, if the latter, add it to the
   decision cluster of the 55.11 close lane rather than editing `supabase/**`.
3. **"Mobile history still a bottom sheet" (audit 2026-09-23 claim).**
   At head, `lib/app/router.dart:833` mounts `InventoryHistoryScreen` as a route
   child, and `inventory_history_screen.dart` navigates via
   `context.go`/`pushNamed` — i.e. the surface IS route-backed. Verify what the
   original finding actually named (possibly a second entry point still showing a
   modal sheet on mobile). Either fix the surviving sheet path or record the
   claim as superseded with file:line evidence. Do not "fix" a surface that is
   already route-backed.
4. **Reconcile the records.** Append a dated "Residual (55.8) — statics" section
   to `mine-flow-STEP-55.8-FINDINGS.md` with per-item dispositions; report the
   replacement evidence-cell line for the index row 55.8 (the 55.11 close lane
   applies it — do not flip the row yourself). Keep remote contract (a)–(e)
   **Unverified** (no staging credentials) and do not touch the 55.11 close,
   the capture harness, or STEP-56.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55.8-FINDINGS.md` §8 (remote evidence,
  ordering pin, contract guard, database.ts blockage)
- `Upcoming Prompts/mine-flow-STEP-55.8-RESIDUAL-PROMPT.md` (executed residual)
- Master spec FC-54.8 rows; ADR-0012 semantics if any volume/ledger question arises
- The 2026-09-23 audit's 55.8 section (origin of the three defect names)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5`; pull if the branch moved.
2. Preserve all untracked `.step55.*` scratch and the 55.11 lane files — never
   stash/reset/absorb/commit them.
3. The three dirty `lib/l10n/app_localizations*.dart` files are pure EOL churn
   (`git diff -w` empty at drafting time); leave them for the 55.11 close lane —
   do not commit or "clean" them here.

## Likely files (ownership boundary)

ALLOWED: `lib/features/tracking/presentation/bloc/inventory/**`,
`lib/features/tracking/presentation/pages/inventory_*`,
their tests under `test/`, the 55.8 findings addendum.
FORBIDDEN: `supabase/**`, `.github/workflows/**`, `integration_test/**` (unless a
journey needs a finder update for a changed key — then report, don't fix),
`lib/l10n/**`, other features' files, the 55.11 close artifacts.

## Tests and verification

- RED→GREEN bloc test for item 1 (if a cold path exists).
- Existing inventory/tracking suites:
  `flutter test test/features/tracking/ test/widget/inventory_history_screen_test.dart`
  (re-derive exact paths at HEAD); `flutter analyze`;
  `dart format --set-exit-if-changed` on touched `.dart` only.
- If a route/sheet change lands: the router + inventory widget suites.

## Boundaries and escalation

- No schema/policy/migration edits; no remote mutations; no CI edits; no secrets.
- Escalate: any item whose honest fix requires `supabase/**` or contradicts
  ADR-0012 semantics.

## Definition of done

Each of the three named defects has exactly one disposition (fixed-with-test /
superseded-with-evidence / escalated-to-owner), the findings addendum is
appended, the index-row replacement line is reported, and no other lane's file
was touched.

## Next

Report the three dispositions + test counts; hand the index-row line to the
55.11 close lane (RESIDUAL-3).
