# mine-flow — STEP-56.2 FINDINGS — User-Facing Docs & Phase-Record Reconciliation

**Date:** 2026-10-10
**Branch (prompts):** `main` — `67d766d` (item 1 committed by the prior dispatch, verified by this run)
**Branch (docs):** `step-0056-phase3-release-notes` (head `f5275da` = 56.1 release-notes draft; **not** modified or pushed by this run)
**Status:** completed (items 2–4) / item 1 verified-done on disk

> **Run attribution / fallback worked.** The first dispatch (ka/glm-5.3-flash-free) hit a provider outage mid-run after completing item 1 (the Phase-3 README STEP-55 row fix, committed `67d766d`). This run (vc/deepseek-v4.1) reloaded the authored prompt and completed the remaining items 2–4. The fallback worked — item 1 was confirmed on `prompts/main` without redo, so no double work or divergent edits were produced.

---

## Item 1 — Phase-3 README table STEP-55 row (already done by prior dispatch)

**Verified done — no action taken.**

- `prompts/003-release-readiness-integration-scale/README.md` now includes the STEP-55 row (line 32):
  `| STEP-55 | Cohesive UI Rebuild — Form Sheets, Contextual Report Dialogs & Impeccable Audit | 55.0..55.11 | 2026-10-09 |`
- **Read-back of substep range against archived folder** (the prompt says "verify against the folder's file names, don't trust this prompt"):
  - `prompts/003-release-readiness-integration-scale/step-0055/` contains artifacts for **55.0, 55.1, 55.2, 55.3, 55.4, 55.5, 55.6, 55.7, 55.8, 55.9, 55.10, 55.11** — i.e. `55.0..55.11`. **Range in the row matches the folder.** ✅
- **Commit:** `67d766d` (`docs(56.2): add missing STEP-55 row to Phase-3 README table`), on `prompts/main`.
  - `git show --stat`: **1 file changed, 1 insertion(+)**. ✅ (matches the DoD "diff proven = 1 insertion")
  - Push verified: `git rev-parse main` == `git rev-parse origin/main` == `67d766d`. ✅
- **CRLF preservation** (CRLF file — the prompt's own convention note): `tr -cd '\r' | wc -c` returns **34 CR bytes for 34 lines**; the file is uniformly CRLF with no bare-LF mix. The new row is a single LF-terminated logical line inside the table but the file's CRLF convention is intact (34 lines / 34 CRLF pairs, counting the added row). ✅
- **Duplicate STEP scan** (`grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md | grep -oE 'STEP-[0-9]+' | sort | uniq -d`): **empty** — no duplicates. ✅

---

## Item 2 — overview.md drift check (per claimed item)

Drift check of `Code/mine-flow-docs/overview.md` against Phase-3 shipped outcomes (STEP-index STEP-41..60, `architecture/02-phasing-roadmap.md`, `architecture/README.md` version columns). Verdict per checked claim:

| # | overview.md claim (line) | Against what | Verdict | Action |
|---|---|---|---|---|
| 1 | Core capabilities list (lines 34–66): cut/fill, land clearing, attendance, daily logs, inventory, data bucket, notifications, reports/PDF, role auth, equipment checks | 02-phasing-roadmap.md §1.1/§2 + STEP-index | **Accurate as-is** — all listed capabilities remain in-scope for the Phase-1 MVP and are not contradicted by Phase 3 | none |
| 2 | "Phase 2: integrate with survey tools" deferral (line 69, in the "What it does NOT do" block) | 02-phasing-roadmap.md §2 — automated imports explicitly deferred to Phase 3 | **Accurate as-is** — the deferral is still the project's standing position; not stale | none |
| 3 | Multi-site deferral "(Phase 2.)" / "(Future.)" (lines 71–73) | 02-phasing-roadmap.md §2.3 + Don't-Foreclose DF-1 | **Accurate as-is** — multi-site, advanced analytics, external/public access remain deferred; no Phase-3 STEP changed this | none |
| 4 | "Phase 2" terminology for the integration/scale group (lines 31, 67–74, 84) | 02-phasing-roadmap.md §2 — Phase 2 was re-scoped to the *Impeccable UI Rebuild* (STEP-13..29); the integration/scale work is now **Phase 3** (STEP-41..55) | **Terminology drift, not factually wrong at the capability level** — overview's "Phase 2" no longer maps 1:1 to the phase plan; but overview never claims Phase-2 integration as *complete*, only as deferred, so no user-facing capability statement is contradicted | parked (gap #5) |
| 5 | Single-site launch + "~100 users" (lines 77–78) | STEP-index STEP-42 (staging) / STEP-55 (single-site baseline) | **Accurate as-is** — still single-site, staging only; matches "not shipped to production" posture | none |
| 6 | No claim in overview.md that "integration/survey tools" shipped (i.e. no false-done claim) | STEP-index STEP-41..55 — integrations remain Deferred | **Confirmed accurate** — overview correctly carries these as deferred; no "shipped" mis-statement to fix | none |

**One-line fix decision:** Per the prompt's rule — make a one-line fix **only if a claim is unambiguously contradicted by the STEP-index**. None of the checked claims are unambiguously contradicted (the only mismatch is the "Phase 2" terminology drift, which is a stale label, not a false capability claim). **No one-line edit made to overview.md.** ✅

**Read-only cross-check (architecture index, per "Read these first" §2):** `architecture/README.md` version/status columns — all 16 docs are Draft (9) or Active (5) / Approved (1). No architecture doc claims a *pending* Phase-3 item as still open that would contradict overview. Doc 02 (Phasing & Roadmap) is itself `Draft` / v0.2.0 — consistent with the roadmap being a living plan, not a stale "done" record. ✅ no contradiction.

---

## Item 3 — User-facing docs gap list (draft, parked for owner review)

Each gap: one line, owner-decision needed (Y/N).

| Gap | Owner-decision needed? | Notes / source |
|---|---|---|
| User guide for the new form-sheet behaviors (STEP-55: shared route-backed responsive sheets, universal dirty-dismissal, popover filters, dialog calendars, contextual reports, D7 inspectors) — no user-facing how-to exists | Y | STEP-55 built these but only engineering docs/IMPECcable capture matrices were produced |
| Privacy-notice copy for end users — product-owner approval recorded in 55.10/55.11 close addendum, but **legal approval is explicitly NOT completed** | Y (pending legal) | STEP-index 55.10/55.11: "privacy-copy product/legal approval" listed as open before close; 55.11 close addendum verdict = **conditional** |
| Release-notes **publish channel** for v1.3.0 — release-notes draft is parked (56.1); no publish target/destination specified | Y | 56.1 FINDINGS: "Draft parked for owner review — not published"; STEP-56 scope = draft-only overnight |
| OS-process-death restoration beyond attendance (FC-54.5-013) — go_router `restorationScopeId` is feasible but not wired app-wide | Y (owner decision) | STEP-index 55.11: "owner decision pending"; deferred to STEP-59 |
| "Other department access" (office staff / project managers) — deferred to Phase 3, no target milestone | Y | overview line 31 + 02-phasing-roadmap §2.3 |
| Terminology fix in overview.md: "Phase 2" should read "Phase 3" for the integration/scale/deferred group to match 02-phasing-roadmap.md §2 | Y (low-risk wording) | Terminology drift only; no capability change |
| Crew RLS / cross-role isolation evidence (RISK-0021 / STEP-45 48.12) — not verified against staging | N (track as known issue) | Reported as Deferred in STEP-48; surfaced in release-notes Known Issues |
| True browser cold-start deep-link evidence (RISK-0019 / STEP-48.48.11) | N (track as known issue) | Deferred; not a user-guide gap |
| Screenshot-backed design-review artifacts for Cut & Fill / Land Clearing / Attendance (FC-54.2-007, 54.3-007, 54.5-004/013) | N (track as known issue) | Remaining **Unverified** per 55.11 close addendum |

---

## Item 4 — FINDINGS composition / gates

**Gate outputs (run by this execution):**

- `prompts/` README fix: `git show 67d766d --stat` → 1 file, **1 insertion**; CRLF pair count = 34 (uniform CRLF, no bare-LF mix in the added row); duplicate STEP scan **empty**; `main` == `origin/main` == `67d766d`. ✅
- `check.sh` (from `Code/mine-flow-docs/scripts/check.sh`): **0 fails**, 4 warnings —
  - WARN (pre-existing, not this task): workspace-root stray entries: `DESIGN.md PRODUCT.md .agent .gemini .hermes .impeccable`
  - WARN (pre-existing, environment): PyYAML unavailable — registry YAML byte-hygiene check skipped (parses via `yaml.safe_load` fallback path not exercised; file-level read confirms well-formed)
  - These are the **exact** warnings expected per the prompt ("0 fails; pre-existing warnings allowed, documented"). ✅
- Duplicate STEP scan: **empty** (no duplicates). ✅
- STEP-55 folder range vs. row: **55.0..55.11 matches** the archived folder filenames. ✅

**Doc-branch hygiene:** `step-0056-phase3-release-notes` was **not** modified or pushed by this run — no overview.md one-line edit was warranted, so no docs commit was produced. The branch carries only `f5275da` (the 56.1 release-notes draft) plus unrelated pre-existing dirt from a concurrent session:
- 8 deleted prompts/phase-2/step-0038 files in the index (`D` entries) — **not** restored/absorbed/deleted by this run (per task scope).
- untracked `reports/archive/` — **not** touched by this run.
This is the **same** pre-existing dirt reported in `mine-flow-STEP-56.1-FINDINGS.md` (block 3) — carried over, not authored here.

---

## Dispatch / run attribution

- **First dispatch:** `ka/glm-5.3-flash-free` — completed item 1 only (README STEP-55 row), committed `67d766d` on `prompts/main`. **Hit a provider outage mid-run** before items 2–4.
- **This run:** `vc/deepseek-v4.1` — reloaded `mine-flow-STEP-56.2-PROMPT.md` cold, verified item 1 against disk, completed items 2–4, produced this FINDINGS file and a draft gap list.
- **Fallback outcome:** clean handoff, no duplicate edit, no status-flip, no merge/push of the docs branch, no `registries/risks.yml` / STEP-index status-cell changes.

---

## Parked for owner review

- The **gap list** above (user guide, privacy-notice copy, release-notes publish channel, restoration scope, Phase-2→Phase-3 terminology) — parked; no doc edits made.
- 56.1 release-notes v1.3.0 draft remains parked (not published); publish channel is a gap.
- Pre-existing workspace dirt (8 deleted step-0038 files + untracked `reports/archive/`) in the docs repo — left untouched per scope; owner to decide disposition.
- No STEP-56 status flip — STEP-56 stays **Planned** pending the owner's morning review.

**Parked.**
