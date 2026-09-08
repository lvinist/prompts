# mine-flow — STEP-49.2 Findings: Guard ③ (Runtime pre-flight substep guidance)

**Date:** 2026-09-09
**Executor:** Gemini 3.1 Pro High
**Substep:** STEP-49.2 (Guard ③ — credential/host-toolchain pre-flight substep for runtime STEPs)
**Status:** Complete / Clean

---

## 1. Edit Record & Rationale

### `Code/{{PROJECT}}-docs/templates/planning-session.md`
**Rationale:** The planning session is where STEPs are outlined. To prevent runtime/E2E STEPs from assuming missing prerequisites, we added a rule to explicitly reserve the first substep (substep 0) as a pre-flight before authoring any functional journeys.
**Excerpt:**
```diff
@@ -136,6 +136,7 @@ STEP's PLAN with its owner rather than silently replacing its index row.
    from what's built and plan the STEPs that **extend** it, rather than re-scaffolding or
    rebuilding what's already there. Adjust to the actual project. Each STEP gets a
    global STEP number (continuing from STEP-1).
+   **Runtime pre-flight rule:** Any STEP whose substeps must *execute* against a runtime (E2E, integration against staging, device/emulator, deployment) must reserve its **first substep as a pre-flight** (substep 0). This pre-flight proves, with recorded evidence, that required credentials exist (name them by placeholder, never value), the host toolchain can build/run the target, and the baseline gates pass. The STEP's remaining substeps are authored *after* the pre-flight verdict, and any unprovable surface is scoped as Unverified-with-reason rather than assumed.
 3. **Interleave check-in STEPs.** About **every 20 STEPs** (the project's cadence, adjustable), add a **Check-in STEP**
```

### `Code/{{PROJECT}}-docs/METHOD.md`
**Rationale:** `METHOD.md` defines the overarching prompt lifecycle. We added a summary rule in the Authoring section pointing to the strict pre-flight requirement for runtime/E2E STEPs.
**Excerpt:**
```diff
@@ -385,6 +385,8 @@ and make the STEP's final test command or CI gate explicit. Tests may run per su
 dedicated final verification substep; choose deliberately in the PLAN. A code-changing substep
 without tests needs a stated reason, not silence.
 
+**Runtime pre-flight rule:** For any STEP executing against a runtime (e.g. E2E, integration against staging, device/emulator, deployment), the STEP's first substep (substep 0) must be reserved as a **pre-flight**. This pre-flight proves required credentials (by placeholder name) and host toolchain readiness with evidence before any remaining substeps are authored. See the planning-session template for details.
+
 ### Closing a STEP
```

### `Code/{{PROJECT}}-docs/templates/substep-prompt-template.md`
**Rationale:** Added a specific check in the Verification section. Runtime-verifying substeps explicitly state runtime preconditions and fallback to Unverified-with-reason if they are unmet.
**Excerpt:**
```diff
@@ -92,6 +92,7 @@
   that the STEP PLAN assigns them to a later final verification substep. Tests that are deferred
   this way still must pass before the STEP is Done.
 - **Honesty at close:** an unrunnable or unrun verification must be reported in the findings/evidence file as **Unverified with reason**, never claimed as a pass. The substep's status inherits the evidence's verdict.
+- **Runtime pre-flight:** if this substep executes against a runtime (e.g. E2E, staging, device/emulator, deployment), it must explicitly state its runtime preconditions. If those prerequisites are unmet (e.g. credentials missing, toolchain broken), the execution must be skipped and reported as **Unverified with reason**.
```

---

## 2. Overlap Notes
No conflicts with existing upstream rules. The Guard cleanly extends the "Authoring" and "Verification" frameworks without redefining existing status values or STEP structures.

---

## 3. Escalation Log
- No escalation triggers were met.
- The upstream planning flow naturally accommodated the guidance for substep 0.
- All mapped files from 49.0 were correctly identified and used.

---

## 4. Verification Record
- **Commit:** A single commit (`STEP-49.2 guard 3: runtime pre-flight substep guidance`) has been recorded.
- **Tree Status:** Working directory is clean (`git status` confirms).
- **Diff:** `git diff HEAD~1` confirms that only the three mapped files were touched, with exactly the content described above.
- **Secret Scan:** Grepped local diff. No credential values or secrets were recorded, only placeholders and plain text guidance.

## 5. Untested Edge Cases & Next Step
- Verification by running an actual initialization script is deferred to `substep 49.4`, which serves as the smoke test.
