# mine-flow — STEP-46.4 PROMPT
# Remediation Implementation

**STEP:** 46.4 of STEP-46
**Model:** DeepSeek V4 Pro
**Prerequisites:** STEP-46.3 must be complete; `mine-flow-STEP-46.3-FINDINGS.md` must exist
**Branch:** `step-0046-ui-ux-audit` (in `mine-flow-app`)
**Reads from disk:**
  - `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md` — the curated confirmed finding register
  - `Code/mine-flow-docs/architecture/07-ui-design-system.md` — design spec
  - `Code/mine-flow-docs/architecture/12-test-strategy.md` — test strategy
  - `Code/mine-flow-docs/AGENTS.md` and `Code/mine-flow-docs/METHOD.md`
  - Each source file cited in the finding register
**Writes:** Code changes in `Code/mine-flow-app/` on branch `step-0046-ui-ux-audit`

---

## Context

You are the remediation agent for STEP-46. The strong-model (Claude Sonnet 4.6 Thinking) has produced a curated finding register at `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md` containing confirmed P1, P2, and P3 findings — false positives have already been removed. Your job is to implement all of them correctly, add tests for each, and leave the codebase cleaner than you found it.

Read before implementing:
- `Code/mine-flow-docs/AGENTS.md` — project conventions.
- `Code/mine-flow-docs/METHOD.md` §5 — test tier assignment and the rule: every code change has a test or a documented reason.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — design spec (ForUI Zinc tokens, spacing, typography).
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — test tiers (unit, integration, widget, E2E).
- `.throughstone/local-user.md` at workspace root — communication baseline.

---

## Process

### 1. Read the finding register in full before touching any file

Read all confirmed findings (CF-XXX). Group them by file to minimize back-and-forth (if five findings touch `cut_fill_list_screen.dart`, fix them all in one pass before moving to the next file).

### 2. Implement each finding

For each CF-XXX:
- Implement the fix described in the "Fix" field of the finding.
- Keep the fix minimal and targeted — do not refactor unrelated code.
- Preserve all existing comments and docstrings that are unrelated to your change.
- After each file change, run `flutter analyze` to confirm no new analyzer issues are introduced.

### 3. Write a test for each fix

Per the test tier assignment in the finding register and the STEP-46 PLAN test tier table:

| Finding category | Test to write |
|------------------|---------------|
| Hardcoded data / data binding mismatch (P1) | Widget test: pump the widget with a mocked BLoC emitting a state with specific field values; assert the displayed text matches the state field, not the hardcoded literal. |
| Layout overflow / missing Expanded/Flexible (P2) | Widget test: wrap the screen in a `ConstrainedBox(constraints: BoxConstraints.tight(const Size(360, 812)))` for narrow mobile, and `Size(1280, 800)` for desktop. Assert no overflow is rendered (use `expectNoOverflow` or check tester.takeException() is null). |
| Raw color / raw TextStyle (P2–P3) | `flutter analyze` passing is the primary gate. If needed, add a widget test that pumps the widget and asserts the rendered color matches `FTheme.of(context).colorScheme.X`. |
| Navigation dead-end (P1) | Widget test: pump the screen (or a minimal parent that builds the route), tap the trigger button, and assert the correct route/page is pushed (use GoRouter test helpers or a mock observer). |
| i18n hardcoded string (P1–P2) | Widget test: pump the screen with a specific `Locale`, assert the displayed string matches the expected localized value (not the hardcoded literal). Update the l10n ARB files if adding a new key. |

If a test is genuinely infeasible (e.g., a layout fix that only manifests on a physical device with a specific GPU), document the reason in the test file as a `// TODO(STEP-46.4): test not written because ...` comment and flag it in the STEP-45 "needs runtime check" list.

### 4. Preserve the test count baseline

The test baseline entering this STEP is **434 tests** (STEP-43.9 verified). You must not regress any existing test. Every new test you write increases the count. After all fixes are implemented, the final `flutter test` run must show ≥ 434 passing tests.

### 5. Update risks.yml if needed

If any finding reveals a systemic issue that cannot be fully resolved in this STEP (e.g., the l10n migration is a large body of work tracked as RISK-0004), do not try to solve it all — implement the specific instances that are confirmed findings, then verify the existing risk register entry is accurate and up-to-date. Add a new risk row only if this STEP uncovers a risk not already registered.

---

## Verification commands (DoD — run these exactly, in this order)

From `Code/mine-flow-app/`:

```powershell
# 1. Static analysis — must exit 0, zero issues
flutter analyze

# 2. Full test suite — must exit 0, all tests pass, count >= 434
flutter test

# 3. Build check — must compile without error
flutter build web --release
```

Capture the output of steps 1 and 2. If any command fails, fix the failure before proceeding. Do not close the substep with a failing gate.

---

## What to produce

After all fixes and tests pass the verification commands:

1. Commit all changes to `step-0046-ui-ux-audit` in `mine-flow-app`.
   Commit message format: `fix(ui): STEP-46 UI/UX audit remediation — N issues fixed`

2. Update `prompts/STEP-index.md` substep 46.4 to `Done` and the STEP-46 row to `Done`.

3. Create `prompts/003-release-readiness-integration-scale/step-0046/` in `prompts/` if it doesn't exist. Ensure the three finding files from 46.1–46.3 are in that folder.

4. Archive the PLAN and substep prompts from `Upcoming Prompts/` to `prompts/003-release-readiness-integration-scale/step-0046/`. (Leave STEP-42 files in `Upcoming Prompts/` — they belong to the still-in-progress STEP-42.)

5. Tell the user:
   - N findings fixed (P1: X, P2: Y, P3: Z)
   - M tests added
   - `flutter analyze` result: 0 issues
   - `flutter test` result: <count> tests passing
   - W needs-runtime items carried to STEP-45 (list them briefly)
   - "STEP-46 complete. The next action is STEP-42 substep 42.4 (still in progress). Once STEP-42 closes, rebase `step-0046-ui-ux-audit` onto master and merge. Then STEP-44 (security baseline) is next, followed by STEP-45 (runtime E2E + design review, which will now have a concrete list of W runtime checks from STEP-46.3)."

---

## Ground rules for this substep

- **No silent scope expansion.** Fix only the confirmed findings in CF-XXX. If you discover a new issue while implementing, note it as a comment `// STEP-46.4-NOTE: found additional issue — <description>` in the file and add it to a "New findings discovered during remediation" section in the output summary. Do not silently fix it without recording it.
- **No raw colors, no raw TextStyle.** If your fix introduces any UI element, it must use ForUI Zinc theme tokens: `FTheme.of(context).colorScheme.X` or `context.theme.typography.X`.
- **No hardcoded spacing values.** Use the compact scale: 4, 8, 12, 16, 20, 24, 32 dp.
- **Follow Dart coding standards** in `Code/mine-flow-docs/coding-standards/dart.md` — docstrings on every new class and public method; comment the why of non-obvious logic.
- **Windows PowerShell reminder:** drive switch before cd; `.sh` scripts via `& "C:\Program Files\Git\bin\sh.exe"`.
