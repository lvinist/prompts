# mine-flow — STEP-48.28: Registry & doc truth repair (risks.yml corruption, RISK-0014, ADR-0018 xref, 47.8 index claim)

> **How to run:** tell your agent *"run substep 48.28"*. Self-contained — runnable cold in a fresh chat.
>
> This is a docs-hub substep inside STEP-48. It does **not** close STEP-48, does not archive the
> STEP, does not authorize Phase 4, and touches no application code.

## Context

A read-only implementation audit of the STEP-45 / 46 / 47 closes
(`Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md`) found that
`Code/mine-flow-docs/registries/risks.yml` — the accepted-risk register the whole method treats as
authoritative — is **committed in an unparseable state**:

```
ReaderError: unacceptable character #x000c: special characters are not allowed
  in "<byte string>", position 18357
```

Three bytes inside RISK-0014's `description` are wrong, and all three sit exactly where the source
text had a backtick followed by a letter that a string escape consumes:

| Offset | Byte on disk | What the text should say |
|---|---|---|
| 18291 | `0x0D` (lone CR) | `` `reporting_remote_datasource.dart` `` — became `\r` + `eporting…` |
| 18371 | `0x0C` (form feed) | `` `fill_volume_m3` `` — became `\f` + `ill_volume_m3` |
| — | a real newline | `` `net_volume_m3` `` — became `\n` + `et_volume_m3` |

Provenance is settled, do not re-derive it: `91d1dae` ("STEP-48.18: Amend RISK-0014 status") is the
only commit in the file's history carrying a `0x0C`, and the same commit rewrote the file to CRLF
(0 → 519 CR bytes), which is why a one-sentence status amendment reports
`522 insertions(+), 520 deletions(-)`. Ignoring CR, its semantic diff is **four changed lines, all in
RISK-0014**: the intended amendment plus the three mangled escapes. The workspace-root scripts
`edit_risks.py` / `edit_risks.js` are the likely instruments.

This matters beyond one row. STEP-47.9 explicitly repaired this file (removing a duplicate
RISK-0012..0019 paste) and recorded "20 unique ids and `yaml.safe_load` clean" as a health property.
Four substeps later it was broken again and **nothing noticed**, because `scripts/check.sh` has nine
checks and none of them parses YAML.

Two smaller truth defects ride along, both cheap and both in the same repo:

- **RISK-0014's row is stale in the opposite direction.** It says the reporting datasource "still
  queries the legacy `cut_volume_m3`/`fill_volume_m3` columns and computes `net_volume_m3 = cut −
  fill`". At the committed tip `c73a00e` that was true. On the current working tree **48.27 fixed
  it**: `reporting_remote_datasource.dart` now reads `bcm_volume`/`lcm_volume` and emits
  `VolumeNormalizer.bankEquivalent(...)`, with the report-facing key names documented as an explicit
  presentation-map boundary.
- **ADR-0018 cites an ADR that does not exist.** Its "Related documents" lists
  `ADR-0017-release-readiness-evidence`; the real file is `ADR-0017-expanded-e2e-tier.md`
  ("Expanded Dual-Platform E2E Test Tier"). It is not a markdown link, so `links.sh` passes it — the
  same blind spot as the YAML one.

And one index claim to correct in `prompts/`:

- **STEP-47.8's substep row misdescribes its own deliverable.** It claims
  `architecture/12-test-strategy.md` §6 was "clarified that both E2E gates are boot-smoke-only".
  Commit `b48df96` is the entire Doc 12 change and contains no such caveat: it bumped v1.1 → v1.2,
  added `flutter drive`/chromedriver to §5, and reworded §6 to
  `- Dual-Platform E2E Tests (Chrome via flutter drive and Pixel 6a via flutter test).`
  The honest note lives in Doc 09 §4 instead. **You correct the claim, not the doc** — Doc 12's
  substantive rewrite belongs to 48.15, which already owns it, and the caveat itself is now obsolete
  (gate `33953949570` reports `e2e-android` `24 tests passed, 2 skipped`).

## Read these first

- `Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` — §G-1, §G-5, §G-7, §F-1
  and the §8 reproduction recipes. This is your source register.
- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the audit-substep block, **Q15**, the honesty rule,
  the status vocabulary, and the concurrency boundary.
- `Code/mine-flow-docs/registries/risks.yml` — the target. Read it as bytes, not only as text.
- `Code/mine-flow-docs/AGENTS.md` "Keep accepted risks visible" + `METHOD.md` §6 — what a register
  row is for.
- `Code/mine-flow-docs/scripts/check.sh` — the nine existing checks and their `hdr`/`pass`/`fail`/
  `warn`/`hint` conventions. Your new check must match them exactly.
- `Code/mine-flow-docs/adr/ADR-0018-android-build-chain-posture.md` and
  `Code/mine-flow-docs/adr/ADR-0017-expanded-e2e-tier.md`.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` §5–§6 and its Version Log — **read only**,
  to confirm what `b48df96` did and did not say.
- `prompts/STEP-index.md` — the STEP-47 substep table (row 47.8).
- `Code/mine-flow-app/lib/features/reporting/data/datasources/reporting_remote_datasource.dart` —
  **read only**, to see what RISK-0014's row should now say.

## Pre-flight and concurrency boundary

Inspect all three repos before editing. Expect concurrent work that is **not yours**:

- `Code/mine-flow-app`: ~26 modified files + 1 untracked test — 48.23's and 48.27's fixes, awaiting
  48.25's commit lane. **Do not stage, commit, revert, reformat, or touch any of them.** This substep
  changes no application code at all.
- `Code/mine-flow-docs`: `architecture/04-data-model.md` is modified (48.23/48.27's Doc 04
  amendment), and `reports/2026-09-05-step-45-47-implementation-audit.md` is **untracked** — it is
  this substep's source register and yours to commit alongside your fixes. Preserve the Doc 04 edit;
  commit only your own files with specific-file staging.
- `prompts`: `STEP-index.md` carries an uncommitted STEP-50 edit (STEP-48 and STEP-50 flipped to
  `In progress`) that belongs to STEP-50. STEP-51's reservation row is already **committed and pushed**
  to `origin/main` (`e2d2087`) and local `main` is fast-forwarded to it — do not re-reserve it. Your
  47.8 correction and the STEP-48-row reconciliation are edits to that same dirty file: if you cannot
  stage your lines without absorbing STEP-50's flip, leave them uncommitted and say so in your findings.

Do not read or print `.env` values, tokens, or passwords. Do not mutate staging or any remote
service. `registries/risks.yml` is a **committed** file — your repair is a normal commit on
`step-0048-runtime-evidence`, never a force-push or history rewrite.

## Scope

### In scope

1. **Repair `registries/risks.yml`.**
   - Rebuild RISK-0014's `description` so the three destroyed backtick spans read correctly again.
     Per **Q15**, repair in place: `45457da`'s block is the pre-corruption text but predates 48.18's
     amendment, so restoring it wholesale would revert real evidence. Combine `45457da`'s wording
     with `91d1dae`'s intended sentence.
   - Normalize the file to LF. It was LF before `91d1dae`; the 519 CR bytes are churn.
   - Prove no other row moved: after the repair, a CR-insensitive diff against `HEAD` must show
     changes confined to RISK-0014 (plus whatever you deliberately update per item 2).
   - Do **not** renumber, re-sort, reflow, or "tidy" any other row. 23 ids in, 23 ids out
     (RISK-0001..0023; 0021–0023 were added legitimately by 48.14's `45457da`, so 47.9's "20 ids"
     figure is merely outdated).

2. **Re-state RISK-0014 against reality.** The code defect is fixed on disk by 48.27 but the fix is
   uncommitted, so choose the status honestly and say which tree you checked. Whatever you choose,
   the row must (a) stop asserting a formula the code no longer computes, (b) name 48.27 and this
   audit report as evidence refs, and (c) keep a revisit trigger if anything is still open —
   e.g. the fix is not yet committed/pushed, and no PDF report has been regenerated against it. If
   you conclude it should be `closed`, fill `closed.date` and `closed.reason`; if not, keep it `open`
   with an accurate description. Do not invent a verification you did not run.

3. **Add `check.sh` check 10 — registry YAML parses.** Iterate `registries/*.yml`, parse each, and
   `fail` with the file name and the parser's first error line when one does not. Constraints:
   - match the existing style — `hdr "10. …"`, `pass`/`fail`/`hint`, no early `exit`, so one run
     still reports all drift;
   - the script is `set -uo pipefail` `bash` and must stay runnable via
     `& "C:\Program Files\Git\bin\sh.exe" .\doctor.sh check` on this host;
   - prefer a Python `yaml.safe_load` one-liner (the host has `python` 3.11 and PyYAML; `links.sh`
     already precedents "hand python a here-doc"), and if no YAML parser is available, `warn` with a
     hint rather than silently passing — a skipped check must be visible;
   - also reject the specific bytes that caused this incident (`0x0C`, lone `CR`) even if a future
     parser tolerates them, since the point is byte hygiene in a hand-edited registry.
   - Update the header comment block's numbered check list and `METHOD.md`/`runbooks` references only
     if they enumerate the checks.

4. **Fix ADR-0018's related-documents xref** to `ADR-0017-expanded-e2e-tier` (or the exact filename
   convention used by neighbouring ADRs — check two others before choosing). Consider making it a
   real markdown link so `links.sh` can see it in future; if you do, verify `links.sh` still passes.

5. **Correct STEP-47.8's index row** in `prompts/STEP-index.md`: replace the false "§6 clarified that
   both E2E gates are boot-smoke-only" clause with what `b48df96` actually did, and note that the
   honest harness caveat lives in Doc 09 §4. Keep the row's other content intact.

6. **Reconcile the STEP-48 row's substep-keyed fields** in `prompts/STEP-index.md`. That row is a
   separate authority from the PLAN and has been lagging since 48.27 was added: its owner list stops
   at 48.26 (`Hermes/Claude Opus 4.8 (48.1, 48.10, 48.15, 48.23, 48.25)` — no 48.27, no 48.28–48.30),
   its prose says "Remediation wave 48.16–48.26", and its terminal-gate sentence says "48.15 re-runs
   only on a GO verdict from 48.26". Update all of them together — owner-by-substep list, wave range,
   and any inline substep references — and add a clause for the audit substeps. **Constraint:** the
   STEP-48 row is *also* part of the uncommitted STEP-50 edit described in the pre-flight (it was
   flipped `Planned` → `In progress` there). If you cannot change your fields without staging that
   flip, leave the edit in the working tree, say so explicitly in your findings, and name it as
   bookkeeping owed by whoever commits STEP-50's flip. Do not stage someone else's status change to
   land your own.

### Out of scope

- Doc 12's substantive rewrite (what the E2E gate proves today) — **48.15 owns it**; its DoD already
  says "Doc 12 updated if the E2E tier's real shape differs from v1.2".
- Any application code, test, or CI change — those are 48.29 and 48.30.
- CF-087's Material remainder and 46.4's test debt — **STEP-51**.
- Committing or pushing anyone else's dirty files; closing STEP-48; changing STEP-48's own status.
- Re-auditing the risk register row by row. That is STEP-50's check-in remit; you fix only RISK-0014
  and whatever your YAML repair mechanically touches.

## Your task

1. Re-derive the corruption before fixing it: print the byte offsets, confirm `yaml.safe_load` fails,
   confirm `HEAD` and `origin/main` both differ in CR count, and confirm the semantic (CR-insensitive)
   diff of `91d1dae` is confined to RISK-0014. Quote real output.
2. Repair the file. Re-parse. Print the id count and the CR/`0x0C` counts before and after.
3. Re-state RISK-0014 per item 2, reading the actual datasource to describe the current behaviour.
4. Add check 10, then **prove it works in both directions**: it must fail on the pre-repair file
   (re-introduce the byte in a scratch copy, or `git stash` the fix) and pass on the repaired one.
   A guard you did not watch fail is not a guard — this is the exact lesson 48.29 is also applying.
5. Fix the ADR xref; re-run `links.sh`.
6. Correct the 47.8 row.
7. Commit with specific-file staging, one commit per repo, preserving every concurrent file listed
   above. Report exactly what you staged and what you deliberately left dirty.
8. Write `Upcoming Prompts/mine-flow-STEP-48.28-FINDINGS.md`.

## Verification

```bash
cd Code/mine-flow-docs
python -c "import yaml; d=yaml.safe_load(open('registries/risks.yml',encoding='utf-8')); print(len(d['risks']),'risks')"
python -c "b=open('registries/risks.yml','rb').read(); print('0x0C',b.count(b'\x0c'),'CR',b.count(b'\r'))"
git diff --stat -- registries/risks.yml
git diff -- registries/risks.yml | tr -d '\r' | grep -cE '^[+-][^+-]'   # expect a small number

cd ../..
"C:/Program Files/Git/bin/sh.exe" ./doctor.sh check       # 0 fail; check 10 present and PASS
"C:/Program Files/Git/bin/sh.exe" ./doctor.sh links       # 0 fail
"C:/Program Files/Git/bin/sh.exe" ./doctor.sh status      # STEP-48 still In progress
```

Required evidence:

- `yaml.safe_load` succeeds; 23 ids; `0x0C` = 0; CR = 0.
- The repaired RISK-0014 `description` contains the three backtick spans intact.
- A CR-insensitive diff proves no other register row's content changed.
- check.sh check 10 observed **failing** on a corrupt input and **passing** on the repaired file, with
  both outputs quoted.
- `links.sh` 0 fail after the ADR edit.
- The concurrent app/docs/prompts files listed in the pre-flight are still dirty and unmodified by you
  (quote `git status --short` for all three repos).
- No secret value read or printed.

## Keeping the docs true

This substep is *itself* a docs-true action, so hold the same bar you are enforcing: if you change
what a register row asserts, the row must cite the evidence that justifies it (48.27's findings, this
audit report). If you touch a `Version:`-bearing architecture doc, bump its Version Log — but you
should not need to; nothing here requires an architecture-doc edit. Never rewrite an archived findings
file; append if something must be corrected. `DESIGN.md` / `PRODUCT.md` are generated — leave them.

## Definition of done

- [ ] `registries/risks.yml` parses under `yaml.safe_load`, 23 ids, 0 `0x0C`, 0 CR.
- [ ] RISK-0014's three destroyed backtick spans restored; 48.18's amendment preserved, not reverted.
- [ ] RISK-0014's status/description/mitigation match what the code does now, with 48.27 + this audit
      cited and an accurate revisit trigger (or an honest `closed` block).
- [ ] No other register row's content changed (CR-insensitive diff quoted).
- [ ] `check.sh` check 10 parses every `registries/*.yml`, rejects `0x0C`/lone CR, matches the script's
      existing conventions, and was observed failing on a corrupt input.
- [ ] ADR-0018's related-documents xref names the real ADR-0017 file; `links.sh` passes.
- [ ] STEP-47.8's index row no longer claims a Doc 12 caveat that does not exist.
- [ ] The STEP-48 index row's substep-keyed fields reconciled (owner list through 48.30, wave range,
      terminal-gate reference) — or the blocker named if STEP-50's uncommitted flip prevents staging.
- [ ] The audit report `reports/2026-09-05-step-45-47-implementation-audit.md` is committed.
- [ ] `./doctor.sh check` 0 fail, `./doctor.sh links` 0 fail.
- [ ] Concurrent 48.23/48.27 app files, the Doc 04 edit, and STEP-50's index edit all preserved and
      listed by name.
- [ ] No secrets read, printed, or committed. No force-push, no history rewrite.
- [ ] `mine-flow-STEP-48.28-FINDINGS.md` written with real command output.

## Next

After this substep, run **48.29** (evidence-guard hardening) in a fresh chat, then **48.30**. The gate
sequence is unchanged: any code-touching substep is followed by 48.24 (local gate) → 48.25
(commit/push) → 48.26 (branch-head CI verdict). STEP-48 remains `In progress`.
