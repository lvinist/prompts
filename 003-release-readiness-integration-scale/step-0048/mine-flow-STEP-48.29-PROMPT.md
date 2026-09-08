# mine-flow — STEP-48.29: Evidence-guard hardening (zero-executed CI guards, l10n multi-line blind spot)

> **How to run:** tell your agent *"run substep 48.29"*. Self-contained — runnable cold in a fresh chat.
>
> Inside STEP-48. Does **not** close the STEP, archive it, or authorize Phase 4.

## Context

STEP-48 exists because STEP-45 shipped fifteen journeys that never ran while CI reported green. The
mechanism was a job that exits 0 on `0 tests passed, 1 skipped`. Substep 48.2 added a "zero-executed"
guard to both E2E jobs to make that impossible.

**The guard does not work.** Its regex is:

```bash
grep -qE "\+[1-9]|\-[1-9]|All tests passed|Some tests failed"
```

Two demonstrated holes:

1. **Android.** `flutter test` prints a final progress line of the form `+<passed> ~<skipped>:`. A run
   where every test skipped prints e.g. `00:05 +0 ~17: All tests passed!` — which the guard accepts
   twice over (`All tests passed` matches literally; `+0` correctly fails `\+[1-9]` but nothing else
   needs to). Verified this session by piping that exact line into the guard: it passes.
2. **Web.** The `e2e-web` job loops per file and appends each `flutter drive` run to `all_web.log`.
   `flutter drive` prints `All tests passed.` **once per file**, including files where every test
   skipped, and prints `result {"result":"true","failureDetails":[]}` alongside it.
   `step4824_e2e_web_all.log` contains 15 of each. So a 16-file web run in which all 16 skipped
   satisfies the aggregate guard.

The same *shape* of hole exists in the localization guard, and it is worth fixing in the same substep
because the lesson is identical — a guard whose matcher is narrower than the thing it guards:

`tool/check_l10n_baseline.dart` splits each file into lines and tests `_hardcodedTextPattern` per line
(`:172–180`). The pattern requires `Text(` and the literal on **one** line, so the extremely common

```dart
Text(
  'Pilih Jenis Laporan',
)
```

is invisible. Of the 33 non-exempt presentation files, **21 contain 36 such literals** — including
`report_type_picker_page.dart`, a file **created by STEP-46.4 itself** while the guard was already in
place, plus both `app_shell.dart` copies, `global_app_header.dart`, `zone_picker.dart`, and nine
tracking/timeline cards. The guard currently reports `[OK] No new hardcoded strings detected`.

Note the asymmetry to preserve: the guard's *contract* is not "no hardcoded strings anywhere" — 29
legacy files are deliberately exempt pending RISK-0004. The contract is "a **new** presentation file
uses AppLocalizations from day one". Widening the exemption list to 50 files would make it green and
worthless. **Q16** in the PLAN is the decision you must apply.

## Read these first

- `Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` — §G-2, §G-3, and the
  §8 recipes (they contain the exact commands that demonstrate both holes).
- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the audit-substep block, **Q16**, the honesty rule,
  and D1 (CI is the authoritative gate).
- `Upcoming Prompts/mine-flow-STEP-48.2-FINDINGS.md` — what the original guard intended, and the
  `android-emulator-runner` newline constraint that shaped it (the `script:` block must stay a single
  line; do not reformat it into a multi-line block).
- `Code/mine-flow-app/.github/workflows/ci.yml` — `e2e-web` (~`:160–200`) and `e2e-android`
  (~`:260–285`). Read both guards and the artifact-upload steps.
- `Code/mine-flow-app/tool/check_l10n_baseline.dart` — the whole file, including
  `_legacyExemptFiles`, `_hardcodedTextPattern`, `_routerLabelPattern`, `_legacyRouterLabels`, and
  `findRouterLabelViolations` (already unit-tested, so there is a precedent for testable helpers).
- `Code/mine-flow-app/test/tool/check_l10n_baseline_test.dart` and
  `test/tool/check_supabase_contracts_test.dart` — the existing guard-test pattern.
- `Code/mine-flow-app/integration_test/helpers/staging_config.dart` — `isStagingConfigured`,
  `hasPerRoleAccounts`, `hasCrewAccount`, `isDriveConfigured`: the four legitimate skip reasons. Your
  guard must still tolerate **honest, expected** skips (Drive/D2 → RISK-0017/0018, crew → RISK-0021)
  while rejecting a wholesale skip.
- Captured real logs at the workspace root — your test fixtures, do not fabricate substitutes:
  `step4824_e2e_web_all.log` (16-file web loop, 15 pass / 1 fail),
  `step4824_r4_android_full.log` (`21:26 +23 ~3: All tests passed!`),
  `step4824_e2e_web_probe.log` (single-file web run).
- `Code/mine-flow-docs/architecture/12-test-strategy.md` §6 — the documented CI-gate list.

## Pre-flight and concurrency boundary

- `Code/mine-flow-app` has ~26 modified files + 1 untracked test from 48.23/48.27 awaiting 48.25's
  commit lane. **Preserve all of them.** Your changes are confined to `.github/workflows/ci.yml`,
  `tool/check_l10n_baseline.dart`, `test/tool/`, and whichever presentation files Q16 says to fix.
- `Code/mine-flow-docs` has `architecture/04-data-model.md` modified (48.23/48.27). Do not touch it.
- `prompts/STEP-index.md` carries STEP-50's edit and the STEP-51 reservation. Do not modify
  `prompts/` in this substep.
- Do not read or print `.env` values or secrets. `ci.yml` references secrets **by name** only — keep
  it that way; never echo a secret into a log line, and do not add a debug step that prints one.
- Do not mutate staging. Do not run the E2E jobs against staging from here: your guard evidence comes
  from the captured logs plus synthetic fixtures.

## Scope

### In scope

1. **Make both zero-executed guards honest.**
   - The guard must assert **executed count > 0**, not "some string appeared". For Android that means
     parsing the final `+N ~M` progress line (or the framework's `(passed, failed, skipped)` summary)
     and failing when `N + failed == 0`. For web it means counting per-file outcomes across the
     aggregate log rather than accepting one `All tests passed.`
   - Web needs a per-file signal because the aggregate is a concatenation: a run of 16 files where 15
     genuinely executed and 1 skipped is fine; 16 skipped is not. Decide and document the rule
     (recommended: require executed > 0 **in aggregate**, and additionally report the per-file
     ran/skipped table so a reader can see composition — 48.24 and 48.26 both had to reconstruct this
     by hand from raw logs, which is why it keeps being mis-read).
   - Keep tolerating the *named* expected skips. An honest skip has a reason string
     (`Unverified: Staging credentials absent`, Drive/D2, crew/RISK-0021); a wholesale skip does not.
   - Respect the `android-emulator-runner` constraint: the Android `script:` stays one line. If the
     logic no longer fits, factor it into a committed helper script (e.g.
     `tool/ci/check_executed.sh` or a `dart run` entry) invoked from that single line — that is
     preferable anyway, because it becomes testable.
2. **Prove the guards.** Run them against captured logs and synthetic fixtures, and show:
   - **fail** on an all-skipped Android line (`+0 ~17: All tests passed!`);
   - **fail** on a synthetic web aggregate of N all-skipped file blocks;
   - **pass** on `step4824_r4_android_full.log` (23 passed / 3 skipped) and on
     `step4824_e2e_web_all.log` (15 pass / 1 fail);
   - unchanged verdicts for the real logs the previous guard already handled correctly.
   If the helper is a script or Dart entry point, add unit tests under `test/tool/`.
3. **Make the l10n guard multi-line-aware.**
   - Detect a `Text(` whose literal argument begins on a following line. Do not regress the existing
     single-line and double-quote coverage (STEP-41.5's ISSUE-4 fixed the double-quote hole; there are
     tests for it).
   - Keep skipping comments and empty/1-char literals as documented. Beware the obvious false
     positives: `Text(` inside a doc comment, and interpolated-only literals like `'$percent%'` —
     decide whether an interpolation-only string counts as user-facing copy and **write the rule
     down** in the file's doc comment either way.
   - Extract the detection into a testable function (mirror `findRouterLabelViolations`) and cover it:
     single-line, multi-line, double-quoted multi-line, comment, empty, interpolation-only.
4. **Apply Q16's split to the 21-file backlog.** For each of the 21 non-exempt files with multi-line
   literals, decide **fix** or **exempt-with-reason**, and record the decision and count. The rule:
   a file the guard was supposed to catch — created or substantially rewritten after the guard landed,
   `report_type_picker_page.dart` first among them — gets fixed. A file that predates the guard joins
   `_legacyExemptFiles` with the same RISK-0004 TODO the existing 29 carry. Do not blanket-exempt; do
   not blanket-rewrite 36 literals into ARB keys either, which would balloon this substep into an
   l10n migration. If the fix list is large, name the boundary you drew and why.
5. **Keep Doc 12 in step only if you change what the gate *is*.** Adding rigour to an existing gate
   needs no doc change. If you add or rename a CI gate, update `architecture/12-test-strategy.md` §6
   and bump its Version Log — but coordinate with 48.15, which owns Doc 12's E2E-shape rewrite.

### Out of scope

- Migrating the 29 already-exempt legacy files to AppLocalizations (RISK-0004's own STEP).
- Doc 12's substantive E2E-shape rewrite (48.15).
- `registries/risks.yml`, RISK-0014, ADR-0018 (48.28).
- `CreatableCombobox`, shadow files (48.30). CF-087 Material remainder (STEP-51).
- Running the branch-head CI gate or judging it (48.26). Pushing (48.25).
- Weakening any journey assertion, or "fixing" a red journey by relaxing the guard.

## Your task

1. Reproduce both holes first and quote the output — including the one-line proof that the current
   Android guard accepts `+0 ~17`. A guard fix nobody watched fail is what produced this finding.
2. Design the executed-count rule for each platform against the **real log grammars** (they differ;
   web's per-file `result {…}` JSON is not the same signal as Android's progress line). Write the rule
   into the workflow/helper as a comment so the next reader does not have to re-derive it.
3. Implement, then run the full fail/pass matrix from item 2 above.
4. Fix the l10n pattern, add the helper + tests, then run the guard and read its output before
   deciding Q16's split. Apply the split. Re-run until `[OK]` is honest — meaning the exemption list
   grew only by files you can justify in one sentence each.
5. Run the local gates. Do not commit anyone else's files.
6. Write `Upcoming Prompts/mine-flow-STEP-48.29-FINDINGS.md`: the two holes with evidence, the new
   rules, the fail/pass matrix, the Q16 split with per-file reasons, counts before/after, and an
   explicit statement of what a green E2E job now proves that it did not before.

## Verification

```bash
cd Code/mine-flow-app
# l10n guard, before and after
dart run tool/check_l10n_baseline.dart

# guard unit tests + full suite
flutter test test/tool/
flutter test

flutter analyze
dart format --output=none --set-exit-if-changed lib/ test/ tool/
dart run tool/check_supabase_contracts.dart

# executed-count guard, both directions (adapt to your helper's interface)
printf '00:05 +0 ~17: All tests passed!\n'      > /tmp/skiponly.log   # must FAIL
tail -40 ../../step4824_r4_android_full.log     > /tmp/android_ok.log # must PASS
```

Also confirm the workflow still parses: `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml',encoding='utf-8'))"`.

Required evidence:

- The old guard's acceptance of `+0 ~17` quoted, and the new guard's rejection of it quoted.
- The new guards passing on both captured real logs, with the counts they derived.
- A synthetic all-skipped **web** aggregate rejected.
- `dart run tool/check_l10n_baseline.dart` output before (`[OK]`, falsely) and after.
- The Q16 split: N fixed, M exempted, each exemption one line of justification.
- `flutter test` green (state the count; the current baseline is 513 locally with 48.23/48.27's
  uncommitted pins present) and `flutter analyze` 0.
- `git status --short` for all three repos showing the concurrent files untouched.
- No secret value printed; `ci.yml` still references secrets by name only.

## Keeping the docs true

If a guard's contract changes in a way a future reader would need to know — e.g. "a green `e2e-web`
now means at least one file executed and the per-file table is in the log" — say so in the workflow
comment and in your findings, and coordinate the Doc 12 wording with 48.15 rather than writing a
competing version. The l10n guard's own doc comment is part of the contract: update its MAINTENANCE
note if the exemption rules change.

## Definition of done

- [ ] Neither E2E guard can pass on an all-skipped run; both proven failing on a synthetic all-skipped
      input and passing on captured real logs.
- [ ] The Android `script:` remains a single line (or the logic moved into a committed, tested helper).
- [ ] Web guard reports per-file ran/skipped composition, not just an aggregate boolean.
- [ ] Honest named skips (Drive/D2, crew/RISK-0021, credentials) still tolerated.
- [ ] `_hardcodedTextPattern` detection is multi-line-aware, extracted into a tested function, with
      single-line/double-quote coverage unregressed and the interpolation rule documented.
- [ ] All 21 backlog files dispositioned per Q16 with counts and one-line reasons; no blanket exemption.
- [ ] `flutter analyze` 0, formatter clean, contract guard OK, `flutter test` green, `test/tool/` green.
- [ ] `ci.yml` still valid YAML; no secret value read or printed.
- [ ] Concurrent 48.23/48.27 app files, the Doc 04 edit, and `prompts/STEP-index.md` untouched.
- [ ] `mine-flow-STEP-48.29-FINDINGS.md` written with real output, including a plain statement of what
      a green E2E job now proves.

## Next

Then **48.30** (dead affordance + shadow files) in a fresh chat, after which the code-touching wave
re-enters the gate sequence: 48.24 local gate → 48.25 commit/push → 48.26 branch-head verdict.
STEP-48 stays `In progress`.
