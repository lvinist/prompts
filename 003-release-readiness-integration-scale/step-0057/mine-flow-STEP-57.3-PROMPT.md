# mine-flow — STEP-57.3: E2E Closure — daily_log Journey + CI Gate

> **How to run:** "run substep 57.3". Cold-runnable.
> **Assigned model tier: mid** (mechanical-to-moderate E2E verification bounded by written
> authority; the parent re-verifies the CI verdict from raw logs).

## Context

With the seed (A) and policy (B) in place, close the daily-log zone round-trip loop:
run the daily_log journey web + Android locally, then the full CI gate at the branch
head. This produces the evidence RISK-0030's close criteria demand.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-57-PLAN.md`.

## Read these first

- `integration_test/journeys/daily_log_journey_test.dart` (both the seeded-zone path and
  the inline-create path — the journey's finder shapes are current post-55.x).
- `.github/workflows/*.yml` E2E steps (per-journey isolated `flutter drive` on web;
  Android leg topology) — know the harness before reading results.
- `Upcoming Prompts/mine-flow-STEP-57.2-FINDINGS.md` (role matrix).
- Credential-gated journey rules: daily_log needs `TEST_FOREMAN_*`; creds absent locally
  ⇒ report Unverified skip, never mix with a credentialed run.

## Scope

**Owns:** journey runs (web + Android), full CI gate at branch head, run-log capture,
findings. App branch `step-0057-zone-insert-policy`.

**Does NOT touch:** journey test code unless a finder is provably stale (widget-type
audit first — a "tap not received" is not automatically product work), product code,
CI workflow files.

## Your task

1. Pre-flight: `adb devices` (relaunch emulator if dead — SDK platform-tools adb; it dies
   between sessions), serialize device runs, verify staging creds presence
   (presence/length only, never values).
2. Run daily_log journey web (`flutter drive` per the workflow's invocation;
   `run_web_wrapper.dart` shared-scratch caveat — verify `e2e_executed` marker names
   daily_log, not a leftover journey).
3. Run daily_log journey Android (`.step55.11i-run-android.sh` runner, or the workflow's
   exact command); read the `result:true/false` JSON per journey from the run log.
4. **CI-gate leg — PARKED per owner Q5 (branches stay unpushed):** do NOT push the
   branch. Record the local journey results as the evidence for now; the CI gate at
   the branch head runs AFTER the owner's morning review approves the push. Name
   this explicitly in FINDINGS: "CI verdict pending owner-approved push."
5. Adjudicate honestly: cancelled jobs = evidence holes; infra-failure reds (emulator
   boot) ≠ code reds; flake-vs-regression per the two-consistent-failures rule.
6. FINDINGS: run ids (local), head sha, per-journey verdicts, gate verdict (local
   complete / CI parked), evidence paths.

## Verification

- Web daily_log journey `result:true`; Android daily_log executed+passed in a full-green
  (or honestly-adjudicated) CI run at the branch head.
- `e2e_executed` marker verified as daily_log for every quoted web run.
- No CI-run red left unexplained in FINDINGS.

## Definition of done

- [ ] Both journeys green with cited run ids + head sha.
- [ ] CI gate verdict recorded honestly (green / adjudicated / parked-with-blocker).
- [ ] FINDINGS complete; branch state recorded (pushed or local-only per owner policy).

## Next

Report to parent. Next: 57.4 (registry/docs reconciliation + close bookkeeping) — the
parent verifies 57.3's verdict from raw evidence before that runs.
