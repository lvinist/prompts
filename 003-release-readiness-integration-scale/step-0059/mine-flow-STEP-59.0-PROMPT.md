# mine-flow — STEP-59.0: Restoration Inventory & Per-Feature Draft-State Design

> **How to run:** "run substep 59.0". Cold-runnable.
> **Assigned model tier: mid** (bounded design work mirroring a landed reference
  implementation; ambiguity parks per Q1 rule).

## Context

STEP-59 extends OS process-death restoration from attendance (landed `27e5c5c`) to all
form features. This substep inventories every form surface and designs its draft-state
snapshot per the attendance precedent, BEFORE any implementation substep runs.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-59-PLAN.md`.

## Read these first

- `lib/features/attendance/presentation/pages/attendance_form_sheet.dart` + its
  restore-requested handler — THE reference implementation (don't reinvent).
- `lib/app/router.dart` (17 `restorationId` pages, 5 branch scope ids) — verify all
  present at HEAD before designing (re-derive; don't trust this prompt's counts).
- Each feature's form entry point: `cut_fill_form_screen.dart`,
  `land_clearing_entry_screen.dart`, daily log form/sheet, equipment check sheet,
  `benchmark_form_screen.dart`, inventory form, data-bucket metadata form
  (re-locate paths at HEAD — names may have moved).
- `lib/features/attendance/` restore tests (2 router + 8 roundtrip) — the test shape.
- `architecture/15-native-app-architecture.md` (restoration section, if any) + Doc 03.

## Scope

**Owns:** (a) inventory table: feature → form surface → draft fields worth snapshotting
(user entry: text, selections, entity ids) vs reload-fresh (reference data, rosters,
auth); (b) per-feature restore design (snapshot version, restore-requested reload
event, version-mismatch fallback); (c) findings parked for the implementer substeps.
Docs repo branch `step-0059-os-restoration-forms`; no code changes.

**Does NOT touch:** app code (design only), migrations, ADRs (unless a design decision
warrants one — park instead), registries.

## Your task

1. Verify the three-layer scope state at HEAD (shell/branch/pages) — record counts.
2. Walk each feature's form: enumerate state-holding widgets/blocs; classify each field
   draft-vs-fresh per the attendance precedent (snapshot the user's entry, reload the
   context). For each feature produce a compact design block: snapshot shape (fields +
   version), restore trigger (mirror `AttendanceFormRestoreRequested`), reload-before-
   apply semantics, version-mismatch fallback (discard → fresh state, never crash).
3. Flag ambiguities per Q1 rule: e.g. data-bucket metadata with a half-completed Drive
   upload, equipment check's SOP checklist state mid-signoff. Ambiguous → parked with
   options; NOT ambiguous → firm design the implementer executes.
4. Write `Upcoming Prompts/mine-flow-STEP-59.0-FINDINGS.md`: inventory + designs +
   parked list. The three implementer substeps (59.1–59.3) build directly on this.

## Verification

Design-only (no code): every feature named in the PLAN appears in the inventory with a
verdict (designed / parked-ambiguous); reference implementation correctly mirrored (no
invented new patterns); router counts verified at HEAD, not quoted.

## Definition of done

- [ ] Inventory covers all 7 form surfaces with draft/fresh classification.
- [ ] Per-feature designs written; parked ambiguities explicit with options.
- [ ] FINDINGS complete on the scratch folder; no code changed.

## Next

Report to parent. Next: 59.1 (cut/fill + land clearing) implements from this design.
