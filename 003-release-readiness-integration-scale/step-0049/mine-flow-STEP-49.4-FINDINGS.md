# mine-flow — STEP-49.4 Findings: Scaffold Smoke Validation & CHANGELOG Entry

**Date:** 2026-09-09  
**Executor:** Gemini 3.7 Flash High  
**Substep:** STEP-49.4 (Scaffold smoke validation + CHANGELOG entry)  
**Status:** Complete / Clean  

---

## 1. Executive Summary

Substep 49.4 served as the verification gate for the Throughstone template hardening work (Guards ①–⑤ authored across substeps 49.1–49.3).

All validation gates passed cleanly:
1. **Scratch Bootstrap (Multi-repo & Mono-repo):** `init.sh` ran against the modified template exported from branch `step-0049-template-hardening` in non-interactive mode for both `--layout=multi` and `--layout=mono`. Both runs exited **code 0**, properly detached from template history, substituted project slug tokens, and initialized Git repositories cleanly.
2. **Generated Project Integrity:** `./doctor.sh check` (`check.sh`) inside both generated projects completed with **exit code 0** (0 failures, 0 warnings, RESULT: OK across all 13 structural checks in both layouts).
3. **Guard Marker Integrity:** All five guards were verified present across all 7 mapped template and process files in both generated projects with 16 exact positive substring matches (1:1 hit count for each marker).
4. **Placeholder Substitution:** No dangling `{{PROJECT}}`, `{{PROJECT_DESCRIPTION}}`, or `{{TRUNK_BRANCH}}` tokens remain in either generated project (0 hits across all files).
5. **Upstream CHANGELOG Entry:** An entry documenting all five process guards and their one-line effects was added under `## [Unreleased] -> ### Added` in `D:\AppDev\Throughstone\CHANGELOG.md` and committed on `step-0049-template-hardening` (commit `f5b7980`).

No escalation triggers were met. The Throughstone clone tree is clean.

---

## 2. Scratch Smoke Run Details

- **Scratch Directories Tested:**
  - Multi-repo: `C:\Users\Alpxalpha\AppData\Local\Temp\throughstone-smoke-494` (and re-verified in `test-smoke-multi`; cleanly removed after verification).
  - Mono-repo: `C:\Users\Alpxalpha\AppData\Local\Temp\test-smoke-mono` (cleanly removed after verification).
- **Template Preparation Method:** `git -C D:/AppDev/Throughstone archive HEAD | tar -x -C "$DEST"` (clean export of the hardened template on branch `step-0049-template-hardening`).
- **Initialization Command Lines:**
  - Multi-repo:
    ```bash
    ./init.sh \
      --non-interactive \
      --slug="smoke49" \
      --desc="Template hardening smoke test" \
      --license=private \
      --layout=multi \
      --collab=solo \
      --remotes=no
    ```
  - Mono-repo:
    ```bash
    ./init.sh \
      --non-interactive \
      --slug="smokemono49" \
      --desc="Mono-repo smoke test" \
      --license=private \
      --layout=mono \
      --collab=solo \
      --remotes=no
    ```
- **Exit Codes:** Both exited `0`.
- **Evidence Log Path:** `step49_smoke_init.log` (preserved at workspace root `d:/AppDev/mine_flow/step49_smoke_init.log`).

### Summary of `step49_smoke_init.log`:
```text
Throughstone — setup
Detaching from the template's git history...
Renaming {{PROJECT}} -> smoke49 ...
  created Code/smoke49-docs/overview.md (fill it in)
  created prompts/STEP-index.md (seeded from template)
Initialising git...
  git repo: Code/smoke49-docs
  git repo: prompts
Done.
```

---

## 3. Generated Project Doctor Verification

- **Command Line:**
  ```bash
  cd "C:/Users/Alpxalpha/AppData/Local/Temp/throughstone-smoke-494"
  ./doctor.sh check
  ```
- **Exit Code:** `0`
- **Evidence Log Path:** `step49_smoke_check.log` (preserved at workspace root `d:/AppDev/mine_flow/step49_smoke_check.log`).

### Doctor Output Summary:
- 1. Duplicate STEP numbers: **[PASS]**
- 2. Duplicate ADR numbers: **[PASS]**
- 3. Statuses valid: **[PASS]**
- 4. Architecture docs carry Version/Status/Log: **[PASS]**
- 5. ADR registry matches disk: **[PASS]**
- 6. Legacy local user profile fields: **[PASS]**
- 7. Workspace-root hygiene: **[PASS]**
- 8. Architecture-session template numbering: **[PASS]**
- 9. Conditional-session template contract: **[PASS]**
- 10. Check-in cadence marker: **[PASS]**
- 11. Repo registry record consistency: **[PASS]**
- 12. Repo registry control record: **[PASS]**
- 13. Repo registry file shape: **[PASS]**
- **Result:** `0 fail(s), 0 warning(s) — RESULT: OK`

---

## 4. Per-Guard Marker Verification Table

Grep verification executed against the generated project files (`Code/smoke49-docs/` and `prompts/`):

| Guard | Target File in Generated Project | Marker Phrase / Snippet Tested | Hits | Verdict |
|---|---|---|---|---|
| **① Honesty Gate** | `Code/smoke49-docs/templates/step-plan-template.md` | `Substep status table reconciled against each substep's evidence file; no substep marked \`Done\` if a required deliverable is recorded \`Unverified\`.` | 1 | **PASS** |
| **① Honesty Gate** | `Code/smoke49-docs/templates/substep-prompt-template.md` | `**Honesty at close:** an unrunnable or unrun verification must be reported in the findings/evidence file as **Unverified with reason**` | 1 | **PASS** |
| **① Honesty Gate** | `Code/smoke49-docs/templates/substep-prompt-template.md` | `Findings/evidence file recorded truthfully; substep status inherits the evidence verdict` | 1 | **PASS** |
| **① Honesty Gate** | `Code/smoke49-docs/METHOD.md` | `When closing a STEP or substep, its status may only be flipped to **Done** when the evidence file's own wording supports it.` | 1 | **PASS** |
| **① Honesty Gate** | `Code/smoke49-docs/templates/step-index-seed.md` | `requires positive verification, unverified required deliverables cannot close a row as Done` | 1 | **PASS** |
| **② Phantom Close** | `Code/smoke49-docs/templates/step-plan-template.md` | `Disk verification: for each projected repo, the branch exists (or was merged), commits exist and are pushed, and cited artifacts/reports exist at their cited paths.` | 1 | **PASS** |
| **② Phantom Close** | `Code/smoke49-docs/METHOD.md` | `claimed commits and artifacts must be verified against disk before a STEP or substep is marked \`Done\`` | 1 | **PASS** |
| **③ Pre-flight Substep** | `Code/smoke49-docs/templates/planning-session.md` | `**Runtime pre-flight rule:** Any STEP whose substeps must *execute* against a runtime` | 1 | **PASS** |
| **③ Pre-flight Substep** | `Code/smoke49-docs/METHOD.md` | `**Runtime pre-flight rule:** For any STEP executing against a runtime` | 1 | **PASS** |
| **③ Pre-flight Substep** | `Code/smoke49-docs/templates/substep-prompt-template.md` | `**Runtime pre-flight:** if this substep executes against a runtime` | 1 | **PASS** |
| **④ Commit Discipline** | `Code/smoke49-docs/runbooks/collaboration.md` | `**Commit per completed substep.**` | 1 | **PASS** |
| **④ Commit Discipline** | `Code/smoke49-docs/runbooks/collaboration.md` | `**It must not accumulate an uncommitted close across repos.**` | 1 | **PASS** |
| **④ Commit Discipline** | `Code/smoke49-docs/templates/substep-prompt-template.md` | `commit its deliverables on the STEP branch (with a message naming the substep)` | 1 | **PASS** |
| **④ Commit Discipline** | `prompts/README.md` | `commits are created per substep on the STEP branch as work proceeds` | 1 | **PASS** |
| **⑤ Trunk Recovery** | `Code/smoke49-docs/runbooks/collaboration.md` | `### Recovering a stranded close` | 1 | **PASS** |
| **⑤ Trunk Recovery** | `prompts/README.md` | `If your \`prompts/\` trunk switch is blocked by uncommitted changes (a stranded close), see the recovery recipe in \`Code/smoke49-docs/runbooks/collaboration.md\`` | 1 | **PASS** |

### Placeholder Token Checks:
- `grep -rnF "{{PROJECT}}" .` -> **0 hits (PASS)**
- `grep -rnF "{{PROJECT_DESCRIPTION}}" .` -> **0 hits (PASS)**
- `grep -rnF "{{TRUNK_BRANCH}}" .` -> **0 hits (PASS)**

---

## 5. Upstream CHANGELOG Diff & Commit

- **Target File:** `D:\AppDev\Throughstone\CHANGELOG.md`
- **Branch:** `step-0049-template-hardening`
- **Commit SHA:** `f5b79807d85c9a7c4b18057a4b4d62ffef030500`
- **Commit Message:** `STEP-49.4 smoke validation + CHANGELOG entry`

### Git Diff:
```diff
diff --git a/CHANGELOG.md b/CHANGELOG.md
index 745407e..4d49d56 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -18,6 +18,28 @@ any project built with it.
 > remains v1.7.1.
 
 ### Added
+- **Five process failure guards against phantom closes, stranded trunks, and unverified work.**
+  Scaffold templates, runbooks, and method documentation now enforce five durable process disciplines
+  earned from field failure modes:
+  - **Guard ① (Honesty gate):** A STEP or substep cannot close as `Done` if any required deliverable
+    or test is recorded as `Unverified`; row status must derive from the latest findings and inherit
+    the evidence verdict (`templates/step-plan-template.md`, `templates/substep-prompt-template.md`,
+    `templates/step-index-seed.md`, `METHOD.md` §1, §5).
+  - **Guard ② (Phantom-close detection):** Claimed branches, commits, and cited artifacts must be
+    verified against disk before a STEP or substep is marked `Done` (`templates/step-plan-template.md`,
+    `METHOD.md` §5, §10).
+  - **Guard ③ (Runtime pre-flight substep):** STEPs executing against an active runtime (E2E, staging,
+    device/emulator, deployment) must reserve substep 0 as a pre-flight to prove credentials (by
+    placeholder name) and host toolchain readiness before authoring functional journeys
+    (`templates/planning-session.md`, `templates/substep-prompt-template.md`, `METHOD.md` §5).
+  - **Guard ④ (Commit-per-substep discipline):** Executors must commit each completed substep's
+    deliverables immediately on the STEP branch instead of accumulating uncommitted work across repos
+    that strands the shared trunk (`runbooks/collaboration.md` §1, §8, `templates/substep-prompt-template.md`,
+    `prompts/README.md`).
+  - **Guard ⑤ (Stranded-trunk recovery recipe):** A structured recovery procedure for safely reconciling,
+    committing, merging, and switching when a dirty `STEP-index.md` on a STEP branch blocks `git switch main`
+    and halts reservation on the shared trunk (`runbooks/collaboration.md` §2, `prompts/README.md`).
+
 - **A runbook for splitting a repository** — `runbooks/splitting-repos.md`. The method used to say
   splitting was "standard git," which is not something you can act on: the recipe you find
   elsewhere makes the extracted repo *new*, with its history rewritten by `git filter-repo`, a
```

---

## 6. Escalation Log

**None.**
- `init.sh` ran to completion without encountering missing tooling, unexpected prompt blocks, or credential requirements.
- Generated project structure completely matched expectation.
- All guard clauses survived templating expansion intact.
- Upstream CHANGELOG entry followed established conventions and committed cleanly.

---

## 7. Verification Record

- **Deep Verification (Ran Actual Tests):**
  - Ran `init.sh` for multi-repo layout in scratch directory (`throughstone-smoke-494` and re-tested in `test-smoke-multi`) -> exited 0, log saved to `step49_smoke_init.log`.
  - Ran `init.sh` for mono-repo layout (`--layout=mono`) in scratch directory `test-smoke-mono` -> exited 0.
  - Ran `./doctor.sh check` in generated multi-repo project -> exited 0 (0 failures, 0 warnings), log saved to `step49_smoke_check.log`.
  - Ran `./doctor.sh check` in generated mono-repo project -> exited 0 (0 failures, 0 warnings).
  - Verified all 16 guard markers across 7 files with automated `grep -cF` in both layouts -> All returned 1 hit (100% presence).
  - Verified 0 hits for all placeholder patterns (`{{PROJECT}}`, `{{PROJECT_DESCRIPTION}}`, `{{TRUNK_BRANCH}}`) across both generated projects.
  - Verified `git -C D:/AppDev/Throughstone status` -> clean working tree on `step-0049-template-hardening`.
- **Shallow Verification:**
  - Eyeballed `CHANGELOG.md` placement and markdown rendering under `## [Unreleased] -> ### Added`.
- **Unverified Aspects:**
  - Upstream GitHub remote push and pull request creation (intentionally assigned to substep 49.5 on Hermes top tier).
  - Upstream GitHub Actions CI workflows on the fork branch (unverified until push).

---

## 8. Substep 49.4 Definition of Done

- [x] Scratch `init.sh` run: exit 0, log preserved and cited (`step49_smoke_init.log`).
- [x] Generated project `check.sh`: exit 0, cited (`step49_smoke_check.log`).
- [x] All five guards' markers verified present in the generated output (table in findings).
- [x] No un-replaced placeholder tokens in the generated project.
- [x] Upstream CHANGELOG entry committed (`f5b7980`); clone tree clean.
- [x] Findings file saved; scratch directory cleaned up (`C:\Users\Alpxalpha\AppData\Local\Temp\throughstone-smoke-494`).
