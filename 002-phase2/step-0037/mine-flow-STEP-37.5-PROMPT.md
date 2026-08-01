# mine-flow — STEP-37.5: Final Verification & Analyzer Gate

> **How to run:** Tell your agent *"run substep 37.5"* (or *"read and run this file"*).
> Run this **only after substeps 37.1, 37.2, 37.3, and 37.4 are all Done.**

## Context

Substep 37.5 of STEP-37 (Residual Impeccable Material Purge). Final gate: confirm the
analyzer is clean, the full test suite has no new failures, run the Impeccable grep,
and archive the STEP.

## Read these first (silently)

- `Upcoming Prompts/mine-flow-STEP-37-PLAN.md` — full context, DoD list, and substep statuses

## Your task

### Step 1 — Analyzer

Run `flutter analyze` from the `mine-flow-app` repo root.
Expected: **No issues found.**
If any new issues exist: fix them before proceeding. Do not mark the STEP done with
analyzer failures.

### Step 2 — Full test suite

Run `flutter test` from the `mine-flow-app` repo root.
Record the total pass/fail counts in your execution notes.
Compare against the pre-STEP-37 baseline (document the last known baseline from
`prompts/STEP-index.md` or the PLAN file).
**Zero new failures permitted.** Pre-existing failures may remain if they match the
documented baseline.

### Step 3 — Manual spot-check (7 widgets)

Open the app in debug mode and visually verify each changed widget:

| Widget | What to check |
|---|---|
| Equipment Check form submit button | Renders as FButton (primary), loading spinner shows on submit, uses `primaryForeground` colour |
| SOP Checklist Item Card | Renders with correct conditional border (pass = subtle, fail = destructive tint) |
| Equipment Check Card delete button | "Hapus Record" ghost button renders, destructive colour correct |
| Milestone Card | Border renders, background correct, tap triggers callback |
| Notification list dismiss-all | "Tutup Semua" ghost button renders, triggers dismiss-all |
| Notification banner | Appears for critical notifications at correct position, destructive background, "Tutup" FButton works |
| File detail delete dialog | Dialog opens with FButton actions; cancel = ghost, delete = destructive; confirm triggers deletion |

Record pass/fail for each widget in your execution notes.

### Step 4 — Final grep (Impeccable clean check)

Run this PowerShell command from the `mine-flow-app` root:

```powershell
Get-ChildItem -Path lib -Recurse -Filter "*.dart" |
  Select-String -Pattern "\bElevatedButton\b|\bTextButton\b|\bCard\b\s*\(|\bMaterialBanner\b" |
  Select-Object Filename, LineNumber, Line |
  Format-Table -AutoSize
```

Expected: **empty output** (zero matches), OR matches that are:
- In comment lines only (not code), **and**
- Documented here as known/pre-existing non-blocking hits.

If any un-documented code-level match appears: fix it before marking done.

### Step 5 — Update the PLAN and index

1. Open `Upcoming Prompts/mine-flow-STEP-37-PLAN.md` and check all remaining unchecked
   `[ ]` DoD boxes that are now verified. Add evidence citations next to each (file + line
   or command output).
2. Open `prompts/STEP-index.md` and flip:
   - STEP-37 row: `Planned` → `Done`
   - All 5 substep rows (37.1–37.5): `Planned` → `Done`

### Step 6 — Archive

Copy the completed `Upcoming Prompts/mine-flow-STEP-37-PLAN.md` and all
`mine-flow-STEP-37.N-PROMPT.md` files into `prompts/002-phase2/step-0037/`
(replacing the PLAN file already there). Clear `Upcoming Prompts/` of STEP-37 files
(restore `.gitkeep` if needed).

## Definition of done

- [ ] `flutter analyze` clean — no issues.
- [ ] `flutter test` zero new failures vs. pre-STEP baseline (baseline documented).
- [ ] Manual spot-check: all 7 widgets pass visual verification (recorded in execution notes).
- [ ] Final grep: empty output or only documented non-blocking comment hits.
- [ ] All DoD boxes in `mine-flow-STEP-37-PLAN.md` checked with evidence citations.
- [ ] `prompts/STEP-index.md` STEP-37 row and all substep rows → **Done**.
- [ ] STEP-37 files archived to `prompts/002-phase2/step-0037/`.
- [ ] `Upcoming Prompts/` cleared of STEP-37 files.

## Next

When STEP-37 is done and archived, tell the user:

*"STEP-37 complete and archived. Phase 2 Tier 2 is now Impeccable-clean — zero Blocking
Material widget violations remain in lib/. Next action: run `./doctor.sh status` to
determine the next planned STEP."*

Then start a fresh chat.
