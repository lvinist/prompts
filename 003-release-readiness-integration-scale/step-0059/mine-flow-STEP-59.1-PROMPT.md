# mine-flow — STEP-59.1: Cut/Fill + Land Clearing Draft Restoration

> **How to run:** "run substep 59.1". Cold-runnable.
> **Assigned model tier: mid** (implementation bounded by the 59.0 design + attendance
  reference; silent-failure surface is low — restore bugs fail loudly in tests).

## Context

Implement versioned draft-state snapshot/restore for the cut/fill and land clearing
forms per the 59.0 design, mirroring the attendance reference implementation.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-59-PLAN.md`;
design authority: `Upcoming Prompts/mine-flow-STEP-59.0-FINDINGS.md`.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-59.0-FINDINGS.md` — the design for these two forms.
- Attendance reference (form sheet + restore-requested handler + its 8 roundtrip tests).
- `lib/features/tracking/` (cut/fill + land clearing live here — verify at HEAD).
- Test strategy doc (`architecture/12-test-strategy.md`) for tier choices.

## Scope

**Owns:** draft snapshot model + restore wiring for both tracking forms; restore-requested
reload; version-mismatch fallback; roundtrip + router tests; findings. App branch
`step-0059-os-restoration-forms`.

**Does NOT touch:** other features, route/scope plumbing (already app-wide), sync
queue behavior, migrations.

## Your task

1. Implement per the 59.0 design: versioned draft snapshot (user entry fields only),
   registered with the feature's restoration bucket; restore-requested event reloads
   fresh context BEFORE applying the snapshot (attendance ordering).
2. Tests: (a) snapshot round-trip equality (save → restore → fields equal);
   (b) `restartAndRestore` per form: URL + sheet + unsaved draft survive;
   (c) version-mismatch fallback: old-version snapshot → fresh state, no crash;
   (d) existing feature suites stay green (run them).
3. `dart format` on touched .dart files only; `flutter analyze` 0 new issues.
4. One commit for this substep lane (message carries `59.1`).
5. FINDINGS: files changed, test names + counts, gates run, snapshot field list.

## Verification

- New roundtrip/router tests green; focused feature suites green; analyze clean;
  format clean (touched files).
- `git status` shows only this lane's files; no EOL churn on shared files.
- Restore ordering verified in the roundtrip test (reload-before-apply asserted by
  seeding stale context that the reload must refresh).

## Definition of done

- [ ] Both forms restore drafts across process death, test-proven.
- [ ] Roundtrip + fallback + reload tests green; suites green; analyze clean.
- [ ] Committed on the branch; FINDINGS complete.

## Next

Report to parent. Next: 59.2 (daily log + equipment check) after parent verification.
