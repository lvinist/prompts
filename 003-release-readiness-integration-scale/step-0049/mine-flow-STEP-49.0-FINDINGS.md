# mine-flow — STEP-49.0 Findings: Upstream Recon & Landing-Site Map

**Date:** 2026-09-09  
**Executor:** Gemini 3.7 Flash High  
**Substep:** STEP-49.0 (Upstream recon — clone, verify layout, map the five guards to landing sites)  
**Status:** Complete / Clean  

---

## 1. Executive Summary

Upstream repository `https://github.com/mherschberg/Throughstone` was cloned clean to `D:\AppDev\Throughstone` (outside `D:\AppDev\mine_flow`). Its layout matches `Code/mine-flow-docs/UPDATING-THROUGHSTONE.md` §4's `docs-hub` mapping specification, where the template docs hub is `Code/{{PROJECT}}-docs/`.

Recon confirms that **none of the five guards** exist in upstream in full:
- Guards ① (Honesty Gate), ② (Phantom-Close Detection), and ③ (Pre-flight Substep) have **zero existing coverage** (clean greenfield additions).
- Guards ④ (Commit-per-substep) and ⑤ (Trunk-reservation Recovery) have **partial baseline rules** (branch-per-STEP, reservation on trunk) but have a complete gap regarding per-substep commits and the stranded-trunk recovery recipe.

No escalation triggers were tripped. The landing-site map for substeps 49.1–49.3 and the verification harness design for 49.4 are fully specified below.

---

## 2. Clone Verification

| Attribute | Expected | Actual / Verified | Verdict |
|---|---|---|---|
| **Location** | `D:\AppDev\Throughstone` (outside workspace root) | `D:\AppDev\Throughstone` | **PASS** |
| **Origin URL** | `https://github.com/mherschberg/Throughstone` | `https://github.com/mherschberg/Throughstone` | **PASS** |
| **Branch** | Default branch (`main`) | `main` | **PASS** |
| **Resolved HEAD SHA** | `c815347e4d080278667e05459f3241a9db407238` | `c815347e4d080278667e05459f3241a9db407238` | **PASS** |
| **Working Tree Status** | Clean, no untracked files | Clean (`nothing to commit, working tree clean`) | **PASS** |
| **Fork Status** | Deferred to substep 49.5 (Q1 default) | No fork remote configured yet (`origin` only) | **PASS** |

Verification command:
```powershell
git -C D:/AppDev/Throughstone rev-parse HEAD
# Output: c815347e4d080278667e05459f3241a9db407238
git -C D:/AppDev/Throughstone status
# Output: On branch main, Your branch is up to date with 'origin/main', nothing to commit, working tree clean
```

---

## 3. Layout Verification Table

Mapped against `UPDATING-THROUGHSTONE.md` §4:
- In an initialized project (`mine-flow`), the docs hub sits at `Code/mine-flow-docs/`.
- In the uninitialized Throughstone template repo, the docs hub template sits at `Code/{{PROJECT}}-docs/` (where `{{PROJECT}}` is replaced by `init.sh`).
- Workspace root files in Throughstone template: `init.sh`, `doctor.sh`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `CHANGELOG.md`, `prompts/README.md`, `tests/`.

| Expected File / Area (`UPDATING-THROUGHSTONE.md` §4) | Actual Upstream Path | Size / Status | Layout Verdict |
|---|---|---|---|
| `docs-hub/METHOD.md` | `Code/{{PROJECT}}-docs/METHOD.md` | 726 lines (52,661 bytes) | **PASS** |
| `docs-hub/AGENTS.md` | `Code/{{PROJECT}}-docs/AGENTS.md` | 237 lines (19,440 bytes) (also workspace root `AGENTS.md` pointer) | **PASS** |
| `prompts/README.md`-equivalent | `prompts/README.md` | 172 lines (12,322 bytes) | **PASS** |
| `docs-hub/templates/step-plan-template.md` | `Code/{{PROJECT}}-docs/templates/step-plan-template.md` | 134 lines (9,442 bytes) | **PASS** |
| `docs-hub/templates/substep-prompt-template.md` | `Code/{{PROJECT}}-docs/templates/substep-prompt-template.md` | 147 lines (10,028 bytes) | **PASS** |
| `docs-hub/templates/planning-session.md` | `Code/{{PROJECT}}-docs/templates/planning-session.md` | 182 lines (13,968 bytes) | **PASS** |
| `docs-hub/templates/step-index-seed.md` | `Code/{{PROJECT}}-docs/templates/step-index-seed.md` | 86 lines (5,940 bytes) | **PASS** |
| `docs-hub/runbooks/collaboration.md` | `Code/{{PROJECT}}-docs/runbooks/collaboration.md` | 322 lines (22,572 bytes) | **PASS** |
| `docs-hub/scripts/check.sh` | `Code/{{PROJECT}}-docs/scripts/check.sh` | 704 lines (37,809 bytes) | **PASS** |
| `scripts/init.sh`-equivalent | `init.sh` (at repo root) | 1,225 lines (54,480 bytes) | **PASS** (template bootstrap script sits at root) |

**Layout Escalate Trigger:** Not triggered. The upstream structure matches the documented `docs-hub` architecture without deviation.

---

## 4. Target Upstream Version & Release Arc

- **Latest Tagged Release:** `v1.7.1` (tagged 2026-08-10, commit `72f23ea`).
- **Active Development Target:** `## [Unreleased]` section in `CHANGELOG.md` on branch `main`.
- **Planned Target Release:** `v1.8.0`. Active unreleased changes on `main` include repo registration/control conventions, repository splitting runbook, and `apply-project-license.sh --notice-only`.
- **Landing Strategy:** Our changes will target the unreleased state on `main`. In substep 49.4, our CHANGELOG entry will land directly under `## [Unreleased]`, itemizing all five process guards.

---

## 5. Existing Guard Overlap Analysis

| Guard | Upstream Status | Detailed Analysis |
|---|---|---|
| **① Unverified-vs-Done honesty gate** | **None** | `step-plan-template.md` and `substep-prompt-template.md` have no requirement to check for unverified items at close. Substep prompt template outlines test cases but has no rule requiring unrun tests to be flagged `Unverified with reason`. `METHOD.md` §1 and §5 define status transitions without an honesty gate. |
| **② Phantom-close detection** | **None** | `step-plan-template.md` Definition of Done checklist only asks whether the review passed and `prompts/STEP-index.md` was updated. There is no disk verification step (checking branch status, commits pushed, or evidence artifacts on disk). |
| **③ Credential/host-toolchain pre-flight** | **None** | `planning-session.md` item 2 outlines implementation sequences (Scaffold → Core data → Capabilities → Integration) but contains no rule or recommendation to front-load a credential/toolchain pre-flight substep for runtime or E2E STEPs. |
| **④ Commit-per-substep discipline** | **Partial / Gap** | `collaboration.md` §1 specifies branch-per-STEP, and §2 specifies immediate trunk commit for reservations. However, neither `collaboration.md` nor `prompts/README.md` instructs executors to commit after each substep on the STEP branch. `prompts/README.md` step 6 suggests gathering files only upon STEP completion. |
| **⑤ Trunk-reservation recovery** | **Partial / Gap** | `collaboration.md` §2 explicitly says reservation edits belong on trunk and never on a `step-NNNN` branch. However, it provides **zero** diagnostic advice or recovery recipe for what to do when an executor violates this and strands `STEP-index.md` on a branch, blocking `git switch main`. |

---

## 6. Authoritative Per-Guard Landing-Site Map

This map governs the file targets and editing boundaries for substeps 49.1, 49.2, and 49.3:

| Guard | Upstream File(s) to Edit | Section / Line Anchor | Kind | Conflict Risk | Implementation Instructions / Notes |
|---|---|---|---|---|---|
| **① Honesty Gate** | `Code/{{PROJECT}}-docs/templates/step-plan-template.md` | `## Definition of done` (after line 124) | Template | Low | Add checkable DoD item: substep status table reconciled against each substep's evidence file; no substep marked `Done` if a required deliverable is recorded `Unverified`. |
| **① Honesty Gate** | `Code/{{PROJECT}}-docs/templates/substep-prompt-template.md` | `## Verification` (after line 93) & `## Definition of done` (after line 141) | Template | Low | Add "Honesty at close" block: unrun/unrunnable verification must be reported as `Unverified with reason`, never claimed as success; substep status inherits evidence verdict. |
| **① Honesty Gate** | `Code/{{PROJECT}}-docs/METHOD.md` | `## 1. The three tiers of work` (Substep, line 46) & `## 5. The prompt lifecycle` (line 362) | Process doc | Low | Add status-honesty rule: status flips to `Done` only when evidence supports it; status derived from latest findings. Respect existing status enum. |
| **① Honesty Gate** | `Code/{{PROJECT}}-docs/templates/step-index-seed.md` | Status values blockquote (lines 7–16) | Template | Low | Clarify that `Done` requires positive verification; unverified required deliverables cannot close a row as Done. |
| **② Phantom Close** | `Code/{{PROJECT}}-docs/templates/step-plan-template.md` | `## Definition of done` (after line 124) | Template | Low | Add mechanical disk verification checklist: verify projected branches exist/merged, commits exist and pushed where appropriate, and cited artifacts/reports exist at cited paths. |
| **② Phantom Close** | `Code/{{PROJECT}}-docs/METHOD.md` | `## 5. The prompt lifecycle` & `## 10. What to do next` (rule 6, line 713) | Process doc | Low | Add explicit requirement that claimed commits and artifacts must be verified against disk before a STEP or substep is marked `Done`. |
| **③ Pre-flight Substep** | `Code/{{PROJECT}}-docs/templates/planning-session.md` | `## What to work through` §2 (line 124) & `Testing note` (line 150) | Template | Low | Add rule for runtime/E2E STEPs: reserve first substep (substep 0) as pre-flight to verify credentials (by placeholder name) and host toolchain/device/build before authoring journeys. |
| **③ Pre-flight Substep** | `Code/{{PROJECT}}-docs/METHOD.md` | `## 5. The prompt lifecycle` (under Authoring, line 381) | Process doc | Low | Add summary rule pointing to pre-flight requirement for runtime/E2E STEPs. |
| **③ Pre-flight Substep** | `Code/{{PROJECT}}-docs/templates/substep-prompt-template.md` | `## Verification` (line 64) | Template | Low | Add clause: runtime-verifying substeps explicitly state runtime preconditions and fallback to Unverified-with-reason if prerequisites are unmet. |
| **④ Commit Discipline** | `Code/{{PROJECT}}-docs/runbooks/collaboration.md` | `## 1. Branch per STEP` (after line 39) & `## 8. A STEP that spans repos` | Process doc | Low | Require committing per completed substep on the STEP branch; warn that uncommitted multi-repo closes strand trunk and block reservation. |
| **④ Commit Discipline** | `prompts/README.md` | `## Recipe: adding a new STEP` §6 (after line 145) | Process doc | Low | Clarify that commits are created per substep as work proceeds; gathering/archiving in `prompts/` is the final STEP close action. |
| **④ Commit Discipline** | `Code/{{PROJECT}}-docs/templates/substep-prompt-template.md` | `## Next` (line 143) | Template | Low | Explicitly instruct executor to commit completed deliverables on the STEP branch before announcing next action. |
| **⑤ Trunk Recovery** | `Code/{{PROJECT}}-docs/runbooks/collaboration.md` | Under `## 2. Reserving a STEP number` (after line 98) | Process doc | Low | Author subsection "Recovering a stranded close": symptoms (git checkout/switch refused due to local changes in `STEP-index.md`), preservation rule (never stash/discard blindly), reconciliation steps, scan for duplicates, commit on branch, merge/push, switch to trunk, fast-forward, then reserve. |
| **⑤ Trunk Recovery** | `prompts/README.md` | `## Recipe: adding a new STEP` §1 (after line 103) | Process doc | Low | Cross-reference the recovery recipe in `runbooks/collaboration.md` if `prompts/` trunk switch is blocked by uncommitted changes. |

---

## 7. Verify-Loop Design Notes for Substep 49.4

Substep 49.4 will perform smoke validation of the modified Throughstone templates. The validation harness will consist of:

1. **Scratch Project Bootstrap:**
   - Execute `init.sh` in a non-interactive mode targeting a clean temporary directory (`$env:TEMP\throughstone-smoke-494`):
     ```bash
     ./init.sh \
       --non-interactive \
       --slug="smoke-hardening" \
       --desc="Template hardening smoke test" \
       --license=proprietary \
       --layout=multi \
       --collab=solo \
       --remotes=no
     ```
   - Verify `init.sh` exits with code 0.

2. **Template Expansion & Content Inspection:**
   Verify that all five guards are properly expanded in the generated project and that no unresolved placeholders (e.g. `{{PROJECT}}`) remain in the guard clauses:
   - `Code/smoke-hardening-docs/templates/step-plan-template.md`: Check for Guard ① honesty checklist and Guard ② phantom-close checklist.
   - `Code/smoke-hardening-docs/templates/substep-prompt-template.md`: Check for Guard ① honesty wording and Guard ④ commit-per-substep reminder.
   - `Code/smoke-hardening-docs/templates/planning-session.md`: Check for Guard ③ pre-flight substep guidance.
   - `Code/smoke-hardening-docs/runbooks/collaboration.md`: Check for Guard ④ commit-per-substep and Guard ⑤ stranded-close recovery recipe.
   - `Code/smoke-hardening-docs/METHOD.md`: Check for Guards ①, ②, and ③ rules.
   - `prompts/README.md`: Check for Guards ④ and ⑤ guidance.

3. **Integrity Doctor Execution:**
   - Run `./doctor.sh check` (or `Code/smoke-hardening-docs/scripts/check.sh`) inside the generated scratch project.
   - Verify exit code 0 and all checks PASS (no syntax or markdown table errors introduced into `step-index-seed.md` or other files).

4. **Upstream Test Harness Observations (Host / OS Quirks):**
   - We inspected upstream `tests/` (`session-template-contract.sh`, `doctor-dispatcher.sh`, `init-trunk-branch.sh`).
   - `tests/doctor-dispatcher.sh` passes (exit 0).
   - `tests/session-template-contract.sh` fails on clean upstream `main` due to an existing upstream issue (`FAIL: 13-glossary.md release clause differs in wording from the other session templates`). Our changes do not touch `13-glossary.md`. Substep 49.4 should note this pre-existing upstream failure and focus on scratch `init.sh` + `check.sh`.
   - On Windows, `core.autocrlf=true` can affect checksums in bash scripts. The scratch test script should use Git Bash and ensure line endings are handled cleanly.

5. **Upstream CHANGELOG.md Verification:**
   - Confirm that `D:\AppDev\Throughstone\CHANGELOG.md` contains a new entry under `## [Unreleased]` naming all five guards.

---

## 8. Unverified Rule Log

In adherence to the honesty rule:
1. **Upstream GitHub Actions CI status:** **Unverified**. Reason: Remote CI runs cannot be directly observed from a local clone without repository push/workflow access to GitHub.
2. **Upstream maintainer PR turnaround / merge policy:** **Unverified**. Reason: Depends on maintainer external activity; will be addressed at substep 49.5 when the PR is opened.

---

## 9. Escalation Assessment

- **Layout divergence:** None. Upstream layout conforms to `UPDATING-THROUGHSTONE.md`.
- **Existing conflicting guards:** None. All five guards are either greenfield additions or clean extensions of existing baseline rules.
- **Clone reachability:** Success. Cloned cleanly in 3 seconds.
- **Escalations required:** Zero.

---

## 10. Substep 49.0 Definition of Done

- [x] Clone exists at `D:\AppDev\Throughstone` on upstream default branch (`main`), clean, sha recorded (`c815347e4d080278667e05459f3241a9db407238`).
- [x] Layout verified against `UPDATING-THROUGHSTONE.md` §4 mapping.
- [x] Per-guard landing-site map authored with conflict-risk assessment.
- [x] Existing-guard overlap check recorded (none / partial / conflicting, per guard).
- [x] Verify-loop design notes for 49.4 recorded.
- [x] Findings file saved; no out-of-scope file touched.
