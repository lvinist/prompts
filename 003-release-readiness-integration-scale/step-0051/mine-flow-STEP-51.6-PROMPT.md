# mine-flow — STEP-51.6: Material-import sweep & residue check

> **How to run:** Tell your agent *"run substep 51.6"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** Mechanical sweep with an unambiguous signal:
**the analyzer and a repeatable grep inventory. Judgement calls are escalation triggers,
not yours to make.**

## Context

STEP-51's final sweep substep for CF-087. After 51.2–51.5 removed the four widget families,
the remaining `package:flutter/material.dart` imports (~71 files at STEP start) must shrink
to only the files that genuinely need Material primitives. **Depends on 51.2, 51.3, 51.4,
51.5 all being Done.** Read the PLAN and **51.1's findings** first.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (decisions D2/D3/D5, ground rules)
- `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` (baseline inventory: 71 files)
- Root `.throughstone/local-user.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (Doc 07 — what counts as
  justified)
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** removing now-unneeded `flutter/material.dart` imports across `lib/`; switching
them to precise imports (`package:forui/forui.dart`, `flutter/widgets.dart`, or the specific
library) as each file actually uses; adding a justification comment on every import that
stays; recording the repeatable inventory command.

**Does NOT touch:** widget behaviour (this is imports only); `test/` and
`integration_test/` files (tests may legitimately use Material testers — out of scope);
any file 51.2–51.5 left flagged as a justified survivor.

## Your task

1. **Inventory the residue:** for each of the files still importing
   `flutter/material.dart` after 51.2–51.5, list what it actually uses from Material
   (`Colors`? `TextEditingController`? nothing?). The analyzer will tell you once the
   import is removed — remove, fix, run `flutter analyze` per file group.
2. **Convert:** no-usage files → drop the import entirely; ForUI-only files →
   `package:forui/forui.dart`; files needing a real Material primitive (document which)
   keep the import **with a one-line justification comment** (e.g. `// Material:
   TextInputConnection — no ForUI equivalent (CF-087 exception)`).
3. **Record the inventory command** so the next audit doesn't re-derive it:
   `grep -rl "package:flutter/material.dart" lib --include='*.dart' | wc -l` plus the
   per-file justification list, saved in your findings and referenced from the register
   appendix's follow-up note (51.10 will finalize).
4. **Residue check:** re-run the four family greps from 51.1 — all must still be zero.

## Verification

- `flutter analyze` → 0 issues (this is your main safety net — unused/undefined imports
  surface here).
- `dart format --set-exit-if-changed` → clean.
- `flutter test` full suite → green, count+delta stated (expect no new cases).
- Inventory command output recorded with the final file count; every remaining import
  justified in a comment.

## Keeping the docs true

If a file needs a Material primitive that is a genuine design exception, that's D5's ADR
condition — **collect the candidates and report them; do not write the ADR yourself**
(escalation). No doc changes otherwise.

## Definition of done

- [ ] Material imports reduced to justified cases only, each with a comment.
- [ ] Repeatable inventory command recorded in findings.
- [ ] `flutter analyze` 0, format clean, full `flutter test` green with count+delta.
- [ ] All four family greps still zero.
- [ ] Findings `Upcoming Prompts/mine-flow-STEP-51.6-FINDINGS.md`; PLAN row updated.

## Escalation (to Opus 4.8 — record in findings if fired)

- More than a handful of files needing genuine Material exceptions (ADR-shaped decision).
- Any analyzer error you cannot resolve by import correction alone.
- Same fix failing twice.

## Next

Tell the user the next open substep (51.7/51.8/51.9 if not yet done, else 51.10). In a
**fresh chat**.
