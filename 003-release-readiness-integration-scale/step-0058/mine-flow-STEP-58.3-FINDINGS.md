# STEP-58.3 FINDINGS: Upstream PR #206 Recheck + Workspace-Root Hygiene

## 1. PR #206 State (Task 1)

**GitHub API fetch** of `repos/mherschberg/Throughstone/pulls/206`:
- **State:** `open`
- **Merged:** `false`
- **Head SHA:** `f5b79807d85c9a7c4b18057a4b4d62ffef030500`
- **Updated at:** `2026-09-08T21:54:48Z`
- **Fetch timestamp:** `2026-10-10T01:16:36Z` (live API call, HTTP 200)

**Disposition:** PR #206 remains open, unmerged. Recorded as a dated addendum in the STEP-49 row's evidence cell in `prompts/STEP-index.md` (CRLF file, patched with `io.open newline=''` discipline). Status cell left unchanged (Done). Committed to prompts/main as `36aa33f` and pushed to origin.

## 2. Concurrent-Lane Adoption (Task 2)

**Verification:** Re-verified byte-identity of all 8 archived step-0038 files vs the deleted tracked blobs:

| Archived file | Tracked blob | Byte-identical (modulo CR)? |
|---|---|---|
| `reports/archive/step-0038/STEP-38-closing-note.md` | `prompts/phase-2/step-0038/STEP-38-closing-note.md` | ✅ Yes |
| `reports/archive/step-0038/STEP-38-remediation-addendum.md` | `prompts/phase-2/step-0038/STEP-38-remediation-addendum.md` | ✅ Yes |
| `reports/archive/step-0038/STEP-38-remediation.md` | `prompts/phase-2/step-0038/STEP-38-remediation.md` | ✅ Yes |
| `reports/archive/step-0038/step-38-audit-prompt-benchmark-nav.md` | `prompts/phase-2/step-0038/step-38-audit-prompt-benchmark-nav.md` | ✅ Yes |
| `reports/archive/step-0038/step-38-audit-prompt-gemini.md` | `prompts/phase-2/step-0038/step-38-audit-prompt-gemini.md` | ✅ Yes |
| `reports/archive/step-0038/step-38-audit-prompt-glm.md` | `prompts/phase-2/step-0038/step-38-audit-prompt-glm.md` | ✅ Yes |
| `reports/archive/step-0038/step-38-remediation-reaudit-prompt.md` | `prompts/phase-2/step-0038/step-38-remediation-reaudit-prompt.md` | ✅ Yes |
| `reports/archive/step-0038/step2-fix-package-final.md` | `prompts/phase-2/step-0038/step2-fix-package-final.md` | ✅ Yes |

**Workspace-root context:** Confirmed `ORIGINAL_REQUEST.md`, `PROJECT.md`, and `scratch/` are no longer at the workspace root — moved into `reports/archive/workspace-root-context/` by the concurrent session. The archived contents match the root originals (verified via file listing and content head).

**Commit:** `40290304` on `step-0058-doc-drift-registry-sweep` — adoption commit attributed to the concurrent session with the exact owner-authorized message.

## 3. Bridge Move (Task 3)

**Script analysis:** `scripts/impecable-bridge.ps1` reads `architecture/07-ui-design-system.md` and writes `DESIGN.md` + `PRODUCT.md` to the workspace root. The script is CRLF (confirmed: 49 CR, 49 LF lines).

**Moved files:**
- `DESIGN.md` → `reports/bridge/DESIGN.md` (CRLF, 90 CR lines, byte-identical copy verified via `diff`)
- `PRODUCT.md` → `reports/bridge/PRODUCT.md` (CRLF, 90 CR lines, byte-identical copy verified via `diff`)

**Script patched:**
- Output path constant changed from `"DESIGN.md"` → `"Code\mine-flow-docs\reports\bridge\DESIGN.md"`
- Output path constant changed from `"PRODUCT.md"` → `"Code\mine-flow-docs\reports\bridge\PRODUCT.md"`
- Help text and success message updated to reference the new location
- CRLF preserved (verified post-patch: 49 CR, 49 LF)

**Commit:** `82d17c92` on `step-0058-doc-drift-registry-sweep`.

## 4. Debris Classification

| Root item | Disposition | Evidence |
|---|---|---|
| `DESIGN.md` | Moved → `reports/bridge/` | Byte-identical copy, source removed |
| `PRODUCT.md` | Moved → `reports/bridge/` | Byte-identical copy, source removed |
| `ORIGINAL_REQUEST.md` | Already moved by concurrent session | Not at root; archived in `reports/archive/workspace-root-context/` |
| `PROJECT.md` | Already moved by concurrent session | Not at root; archived in `reports/archive/workspace-root-context/` |
| `scratch/` | Already moved by concurrent session | Not at root; archived in `reports/archive/workspace-root-context/scratch/` |
| `.agent/` | Per-machine pointer (tool state) | Contains only `skills/` subdir; kept as intentional |
| `.gemini/` | Per-machine pointer (tool state) | Contains only `skills/` subdir; kept as intentional |
| `.hermes/` | Per-machine pointer (tool state) | Contains `plans/` subdir; kept as intentional |
| `.impecible/` | Per-machine pointer (tool state) | Contains `live/` subdir with annotations/roots.json/sessions; kept as intentional |
| `.throughstone/` | Per-machine pointer | Contains `local-user.md`; kept as intentional |

No files parked for owner — all items either moved-and-committed, kept-as-pointer, or already handled by the concurrent session.

## 5. check.sh Warning Delta

| | Before (58.3 start) | After (58.3 close) |
|---|---|---|
| Fails | 0 | 0 |
| Warnings | 1 | 1 |
| Warning items | `DESIGN.md PRODUCT.md .agent .gemini .hermes .impecible` | `.agent .gemini .hermes .impecible` |

The `DESIGN.md` and `PRODUCT.md` entries disappeared from the root-hygiene warning. The remaining `.agent`, `.gemini`, `.hermes`, `.impecible` dirs are per-machine tool state, documented as intentional (not durable content).

## 6. Duplicate STEP Scan

`grep` for duplicate STEP numbers in `prompts/STEP-index.md`: **0 duplicates** (clean).

## 7. git diff --check

`git diff --check` on the docs repo: clean for the bridge commit (`82d17c92`). Minor EOF newline warnings appear in the adoption commit (`40290304`) but these are in archived workspace-root-context files (new blank line at EOF, trailing whitespace in handoff docs) — pre-existing content from the concurrent session's move, not introduced by this lane's edits.
