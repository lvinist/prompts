# mine-flow — STEP-49.3 Findings: Guards ④ + ⑤

**Date:** 2026-09-09
**Executor:** Gemini 3.1 Pro High
**Substep:** 49.3 (Guards ④+⑤ — commit-per-substep discipline + stranded-trunk recovery recipe)
**Status:** Complete / Clean

---

## 1. Executive Summary

Guards ④ (commit-per-substep discipline) and ⑤ (stranded-trunk recovery recipe) were successfully authored in the Throughstone clone at `D:\AppDev\Throughstone`. The changes enforce committing each completed substep's deliverables immediately on the STEP branch, preventing uncommitted multi-repo closes that strand the shared trunk. The recovery recipe provides a structured escape hatch for when this discipline is violated.

---

## 2. Per-File Edit Record

### `Code/{{PROJECT}}-docs/runbooks/collaboration.md`

**Guard 4:** Added explicit bullets under `## 1. Branch per STEP` and `## 8. A STEP that spans repos` warning against accumulating uncommitted work across repos.
**Guard 5:** Added a new subsection `### Recovering a stranded close` before `## 3. The shared coordination surface is the index row`.

**Diff Excerpt:**
```diff
@@ -37,6 +37,7 @@
   one logical STEP stays recognizable across repos.
 - This holds **even when you're solo.** It costs nothing alone and means the workflow is
   identical the day a second contributor arrives — no mode switch.
+- **Commit per completed substep.** As you complete each substep, commit its deliverables on the STEP branch with a message naming the substep (e.g., "STEP-42.1: ..."). Do not save up the whole STEP's work for one multi-repo close — an uncommitted close spanning multiple repos will strand your shared trunk and block the next STEP reservation entirely.
 - Branch lifetime, PR gates, and how the branch merges are **standard practice** — the method
   only fixes the name and the cross-repo consistency.
 
@@ -102,6 +103,14 @@
 > after STEP-1. The reserve-then-push dance only matters for **ad-hoc STEPs** added later
 > (bugs, inserted work) — which is exactly when two people might grab a number at once.
 
+### Recovering a stranded close
+If you violate the commit-per-substep discipline and leave `prompts/STEP-index.md` dirty on a `step-NNNN` branch, `git switch main` will refuse to switch branches, blocking the next STEP reservation entirely. (For a worked example, see mine-flow's STEP-45, where an uncommitted close stranded the trunk and was successfully recovered this way before reserving STEPs 47-49.) Do not blindly stash or discard. To recover safely:
+1. **Preserve and reconcile:** Keep the uncommitted files. Re-truth the index row and substep summary against actual evidence (apply the Unverified honesty gate — if a deliverable failed, mark it Unverified, never Done).
+2. **Review:** Run `git diff --check` to catch whitespace or format damage, and run the duplicate STEP-number scan to ensure no collisions were introduced.
+3. **Commit locally:** Commit the reconciled changes on your current `step-NNNN` branch.
+4. **Merge and switch:** Push the branch, merge it, then `git switch main` and fast-forward your local trunk.
+5. **Reserve:** Now you can safely allocate the next STEP number on the shared trunk.
+
 ## 3. The shared coordination surface is the index row
 
@@ -259,6 +268,7 @@
 - Its **PLAN lists the repos it touches and the order they merge in** (cross-repo
   sequencing). Reference commits / PRs / tags where ordering matters.
 - It uses the **same `step-NNNN` branch name in each repo** (§1).
+- **It must not accumulate an uncommitted close across repos.** Commit each completed substep's deliverables immediately on the STEP branches. If you leave a final cross-repo close uncommitted, your dirty `prompts/STEP-index.md` on the STEP branch will prevent switching to trunk, completely blocking the next STEP reservation.
 - If it creates a new repo, **register it** (`register-repo.md`) — your row only (§5).
```

### `Code/{{PROJECT}}-docs/templates/substep-prompt-template.md`

**Guard 4:** Updated the `## Next` section to instruct the executor to commit deliverables before announcing the next action.

**Diff Excerpt:**
```diff
@@ -144,6 +144,6 @@
 - [ ] Findings/evidence file recorded truthfully; substep status inherits the evidence verdict (no `Unverified` items claimed as a pass).
 
 ## Next
-When this substep is done, update its status in the STEP PLAN, then tell the user the next
+When this substep is done, commit its deliverables on the STEP branch (with a message naming the substep), update its status in the STEP PLAN, then tell the user the next
 action: the next open substep — *"run substep N.M"*, in a **fresh chat** — or, if this was
 the last substep, the STEP's review. (`METHOD.md` §10.)
```

### `prompts/README.md`

**Guard 4:** Adjusted step 7 under `## Recipe: adding a new STEP` to clarify that commits happen as work proceeds.
**Guard 5:** Added a reference under step 1 pointing to the recovery recipe in `collaboration.md`.

**Diff Excerpt:**
```diff
@@ -111,7 +111,7 @@
    pull, renumber, push again. Before every push, even on a clean merge, scan for a duplicate
    (`grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md | grep -oE 'STEP-[0-9]+' | sort | uniq -d`); two appended rows merge
    with no conflict into a silent duplicate. (Solo with no remote, this is just a local edit.)
-   See `Code/{{PROJECT}}-docs/runbooks/collaboration.md`.
+   If your `prompts/` trunk switch is blocked by uncommitted changes (a stranded close), see the recovery recipe in `Code/{{PROJECT}}-docs/runbooks/collaboration.md`.
 2. **Confirm scope** with the user before writing anything — a STEP is a real commitment.
@@ -155,7 +155,7 @@
    present the PLAN and substep list to the user and **stop for approval** before running any
    substep. Do not continue from planning into execution unless the user explicitly asks for a
    specific substep, e.g. `run substep N.1`.
-7. **On completion:** run the STEP's review — your team's standard **PR / code review** (the
+7. **On completion:** (Note that commits are created per substep on the STEP branch as work proceeds; archiving is the final bookkeeping.) Run the STEP's review — your team's standard **PR / code review** (the
    method doesn't redefine it), plus the doc-drift check — then **gather the STEP's files
```

---

## 3. Rationale & Overlap Notes

**Rationale:** By ensuring each substep's deliverables are committed immediately, we prevent large, multi-repo changes from piling up uncommitted, which caused the STEP-45 stranded close. The recovery recipe provides a standardized, tested method to escape a stranded state without losing work.
**Overlap:** Upstream's `collaboration.md` already defined branch-per-STEP and reservation protocols, but lacked the specific requirement to commit *per substep*. The changes merged seamlessly into the existing sections without duplicating rules.

---

## 4. Escalation Log

**None.** Upstream's collaboration model matched the shared-trunk assumption and the recovery recipe applied cleanly. No contradictions were found in the existing text.

---

## 5. Honest Verification

- **Command Run:** `git -C D:\AppDev\Throughstone log --oneline -1` and `git -C D:\AppDev\Throughstone diff HEAD~1 HEAD`.
- **Verdict:** PASS. The single commit `STEP-49.3 guards 4+5: commit-per-substep + stranded-trunk recovery` is present on the branch. The diff shows modifications only in the mapped template/process files (`collaboration.md`, `substep-prompt-template.md`, `prompts/README.md`). No out-of-scope files were touched.
- **Recovery Recipe Integrity:** The recovery command sequence aligns with upstream's reservation rules and correctly emphasizes preserving and reconciling evidence.
