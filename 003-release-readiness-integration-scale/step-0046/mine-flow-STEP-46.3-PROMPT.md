# mine-flow — STEP-46.3 PROMPT
# Pass 2: Strong-Model Confirmation & Finding Register

**STEP:** 46.3 of STEP-46
**Model:** Claude Sonnet 4.6 Thinking (the strong model — spend is proportional to candidate count, not screen count)
**Prerequisites:** Both 46.1 AND 46.2 must be complete
**Reads from disk:**
  - `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.1-FINDINGS.md`
  - `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.2-FINDINGS.md`
  - `prompts/003-release-readiness-integration-scale/step-0046/screenshots/*.png` (all captured screenshots)
  - The actual source file and surrounding context for every candidate finding (look up the file+line from the finding entry)
  - `Code/mine-flow-docs/architecture/07-ui-design-system.md`
  - `Code/mine-flow-docs/overview.md`
  - `lib/app/router.dart`
**Writes:** `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`

---

## Context

You are running Pass 2 of the STEP-46 UI/UX audit. Pass 1a (code scan) and Pass 1b (screenshot review) have produced two raw finding lists. Your job is to **independently confirm or reject every candidate finding** against the actual source file and screenshot. You are the gate that separates real bugs from false positives before the remediation agent spends time on them.

Read before starting:
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the design spec.
- `Code/mine-flow-docs/overview.md` — stated capabilities and user roles.
- `lib/app/router.dart` — the full routing setup (important for navigation findings).

---

## Process

### 1. Load all candidate findings

Read `mine-flow-STEP-46.1-FINDINGS.md` and `mine-flow-STEP-46.2-FINDINGS.md`. Merge them into a single working list. Deduplicate: if F-007 and V-003 describe the same issue on the same screen, merge them into one confirmed entry noting both sources.

Total working list = all F-XXX + all V-XXX entries.

### 2. For each candidate finding, independently verify

For each entry in the merged list:

1. **Read the actual source.** Open the file + line range cited in the finding. Read enough surrounding context to understand what the code actually does.
2. **Look at the screenshot.** Open the corresponding screenshot(s) from `screenshots/`.
3. **Make a verdict:**

   - **CONFIRMED** — the issue is real. The code or screenshot demonstrates the problem as described (or worse). Write the exact fix needed.
   - **REJECTED** — the issue is not real. Explain in one sentence why the code/rendering is correct and the Pass 1 model was wrong.
   - **NEEDS-RUNTIME** — cannot be confirmed or rejected from static code + screenshot alone (e.g., whether a Supabase query actually filters by the right field at runtime, or whether a layout that looks correct at 1280px breaks on a physical 360px device). These go to STEP-45 for runtime verification.

**Do not accept a finding uncritically just because Pass 1 flagged it.** Your job is to be the skeptic. A false positive wastes DeepSeek's remediation time. A false negative ships a bug.

### 3. Rate confirmed findings

For every CONFIRMED finding, assign:
- **Severity:** P1 (functional/data correctness), P2 (layout/visual), or P3 (token/cosmetic — still fixed in 46.4 per PLAN decisions)
- **Fix description:** One clear paragraph describing exactly what needs to change in the code to fix this. Be specific enough that a fresh agent can implement it without re-reading the finding's analysis.
- **Test tier:** Which test tier from the STEP-46 PLAN covers this fix? (Widget test, integration test, static guard, or "no test feasible — reason: X")

---

## Output format

Write the curated register to `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`:

```markdown
# STEP-46.3 — Confirmed Finding Register

Generated: <date>
Source findings: <N> from 46.1 (F-XXX), <M> from 46.2 (V-XXX)
Total working list: <N+M> candidates
Deduplicated working list: <X> unique issues
Confirmed: <Y> | Rejected: <Z> | Needs-Runtime: <W>

---

## Confirmed Findings (fix in 46.4)

### CF-001 | P1 | S09 CutFillListScreen — foremanId always empty string
**Sources:** F-001 (46.1), V-009 (46.2)
**File:** `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
**Lines:** 42–44; also `lib/app/router.dart` lines 241–246
**Severity:** P1
**Confirmed:** Yes. `router.dart` passes `foremanId: ''` unconditionally. `CutFillListScreen` passes this to the BLoC which passes it to the repository filter. A crew member and a foreman both see the same unfiltered dataset. This violates the role-based data visibility stated in `overview.md`.
**Fix:** Read the authenticated user's ID from the auth state (SupabaseAuth current user UID) in the router builder (or in the BLoC's initial load) and pass it as `foremanId`. If the current user is a supervisor, pass null or an empty string only if "see all" is the correct supervisor behavior — verify against `overview.md` ("Supervisors review all data").
**Test tier:** Widget test — mount CutFillListScreen with a mocked BLoC; assert that the bloc receives a non-empty foremanId when the simulated user is a foreman.

---

### CF-002 | P2 | S03 GroupLandingPage — ...

---

## Rejected Findings

### REJECTED: F-014 | S19 TimelinePage — spacing 10dp
**Verdict:** NOT a violation. The 10dp value is padding inside a ForUI card component (not project code) — it comes from the ForUI package's internal layout. Project code uses 8dp and 16dp correctly at the boundary. Pass 1 model was reading into package internals. No action.

---

## Needs-Runtime Findings (carry to STEP-45)

### NR-001 | S23 ReportConfigPage — state.extra null fallback bare Scaffold
**Sources:** F-022 (46.1)
**Observation:** The router has a null fallback that renders a bare Scaffold with a hardcoded Indonesian string `'Jenis laporan tidak ditemukan.'`. Cannot confirm from static code whether any in-app navigation path reaches this route without `extra` — needs runtime tracing on device/staging.
**STEP-45 action:** Navigate to `/reports/config` via every Laporan button in the app and confirm none reach the null fallback path.

---

## Summary Table

| ID     | Severity | Screen | Short description                     | Status    |
|--------|----------|--------|---------------------------------------|-----------|
| CF-001 | P1       | S09    | foremanId always empty string         | Confirmed |
| CF-002 | P2       | S03    | GroupLandingPage feature tile overflow | Confirmed |
| ...    |          |        |                                       |           |
| REJECTED: F-014 | — | S19  | Spacing 10dp in ForUI internals       | Rejected  |
| NR-001 | P1       | S23    | ReportConfigPage null-extra fallback  | Needs-Runtime |
```

---

## After writing the register

1. Count the totals and fill in the header.
2. Commit `mine-flow-STEP-46.3-FINDINGS.md` to the `step-0046-ui-ux-audit` branch in `prompts/`.
3. Update `prompts/STEP-index.md` substep 46.3 to `Done`.
4. Tell the user:
   - Total confirmed findings by severity (P1: N, P2: M, P3: K)
   - Total rejected (false positives)
   - Total needs-runtime (going to STEP-45)
   - "Ready to run 46.4 (remediation)?"
