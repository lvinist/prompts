# STEP-48.28 Findings — Registry & documentation truth repair

**Date:** 2026-09-07
**Substep:** 48.28
**Branch:** `step-0048-runtime-evidence`
**Scope:** docs hub registry/check, ADR cross-reference, and `prompts/STEP-index.md` truth corrections. No application code or remote-state mutation.

## Result

**Done.** The committed `registries/risks.yml` corruption was repaired in the working tree and committed with the owned docs changes. RISK-0014 preserves the STEP-48.18 runtime amendment while describing the current, uncommitted 48.27 reporting fix honestly. The new `check.sh` check 10 was observed failing on injected corruption and passing after repair.

## Pre-flight and concurrent work preserved

- `Code/mine-flow-app`: clean before and after; no application files were touched.
- `Code/mine-flow-docs`: `architecture/04-data-model.md` was a concurrent 48.23/48.27 edit and was not staged. The audit report was untracked and is owned by this substep; it was staged with the repair.
- `prompts`: `STEP-index.md` contained the uncommitted STEP-50 `Planned` → `In progress` flip. The flip was preserved and staged together with this substep's 47.8 and STEP-48 row corrections; it was not reverted or silently omitted.
- No `.env`, credentials, tokens, or remote service state were read or changed.

## Corruption re-derivation

Commands were run in `Code/mine-flow-docs` against the exact committed blobs:

```text
HEAD: len=27896 CR=519 FF=1 LF=578
HEAD: yaml.safe_load=FAIL unacceptable character #x000c: special characters are not allowed
origin/main: len=24282 CR=0 FF=0 LF=521
origin/main: yaml.safe_load=OK
91d1dae: len=27896 CR=519 FF=1 LF=578
91d1dae: yaml.safe_load=FAIL unacceptable character #x000c: special characters are not allowed
45457da: len=27280 CR=0 FF=0 LF=576
45457da: yaml.safe_load=OK
```

The committed HEAD blob has the expected 519 CR bytes and one form-feed. The repaired working tree is LF-only. The three restored spans are present at byte offsets 17842, 17959, and 17976:

```text
working risks.yml: len 27512 CR 0 FF 0 LF 581
`reporting_remote_datasource.dart` offset 17842
`fill_volume_m3` offset 17959
`net_volume_m3` offset 17976
```

The normalized diff of `91d1dae` against its parent is confined to the RISK-0014 description plus one trailing blank-line addition. The malformed escape sequences explain why the textual unified diff expands into 11 changed line records: the original `\r`, `\f`, and `\n` were interpreted as a lone CR, form-feed, and newline. The intended runtime amendment is retained in the repaired row.

## Repair verification

```text
yaml.safe_load: 23 risks
unique ids: 23
bytes: 0x0C= 0 CR= 0
spans: True True True
status: mitigated
owner: STEP-48.27
```

RISK-0014 now states that 48.27 reads `bcm_volume`/`lcm_volume`, emits report-facing keys at an explicit presentation-map boundary, and uses `VolumeNormalizer.bankEquivalent` rather than `cut - fill`. It also states that the 48.27 application change is not yet committed/pushed and that PDF regeneration remains open. The 48.18 evidence about the old query falling back to zero is retained as historical evidence, not asserted as current behavior.

## Guard check 10 — both directions observed

A scratch copy was not committed. A form-feed was injected into the `fill_volume_m3` span at offset 17960, then the original repaired file was restored before the passing run.

Corrupt input:

```text
corrupt-check exit=1
10. Registry YAML parses and has no control-byte/CR corruption
contains 0x0c form-feed byte
[FAIL] registries/risks.yml is invalid or has unsafe bytes: contains 0x0c form-feed byte
Summary
  1 fail(s), 1 warning(s)
  RESULT: FAIL
```

Repaired input:

```text
10. Registry YAML parses and has no control-byte/CR corruption
[PASS] all 3 registry YAML file(s) parse and contain no control-byte/CR corruption
Summary
  0 fail(s), 1 warning(s)
  RESULT: OK
```

The one warning is the pre-existing workspace-root scratch-artifact warning; it is not a check failure.

## Other documentation corrections

- `adr/ADR-0018-android-build-chain-posture.md` now links to `[ADR-0017: Expanded Dual-Platform E2E Test Tier](ADR-0017-expanded-e2e-tier.md)`.
- `prompts/STEP-index.md` 47.8 now accurately says Doc 12 §5–§6 records the dual-platform commands and that the harness caveat lives in Doc 09 §4; it no longer claims both E2E gates are boot-smoke-only.
- The STEP-48 row now includes owners through 48.30 and identifies the audit substeps in its scope. The STEP-50 in-progress flip was restored to dirty worktree state after the boundary-correction commit; it is not part of the substep's committed change.

## Final gates

```text
./scripts/check.sh
10. Registry YAML parses and has no control-byte/CR corruption
[PASS] all 3 registry YAML file(s) parse and contain no control-byte/CR corruption
Summary
  0 fail(s), 1 warning(s)
  RESULT: OK

./scripts/links.sh
[PASS] 134 scoped local link(s) resolve
Summary
  0 fail(s)
  RESULT: OK

./doctor.sh status
Where you are:
  Building — STEP-48 (Runtime Evidence — resolve STEP-45's carried-forward findings) is In progress.
Next action:
  → open STEP-48's PLAN in "Upcoming Prompts/" and run its lowest open substep
```

`git diff --check` produced no whitespace errors. The duplicate STEP-number scan returned no lines.

## Commits and remaining dirty files

Docs commit: `754d5e8 fix(STEP-48.28): repair registry and documentation truth`.
Specific-file staging included:

- `adr/ADR-0018-android-build-chain-posture.md`
- `registries/risks.yml`
- `scripts/check.sh`
- `reports/2026-09-05-step-45-47-implementation-audit.md`

The concurrent `architecture/04-data-model.md` edit remains unstaged. The app repo remains clean. The prompts commits are `92e0c6b docs(STEP-48.28): correct roadmap claims` and `a819713 chore(STEP-48.28): restore concurrent STEP-50 status`; the second commit removes the accidental STEP-50 flip from the substep commit, after which the concurrent `In progress` value was reapplied as the sole dirty change in `STEP-index.md`. This findings file remains in `Upcoming Prompts/` as the in-flight substep record.

## Next

Run **48.29** in a fresh chat. STEP-48 remains `In progress`; 48.30 and the final 48.15/close gate remain open.
