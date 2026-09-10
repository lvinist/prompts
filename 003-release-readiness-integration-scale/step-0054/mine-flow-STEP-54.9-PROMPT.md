# mine-flow — STEP-54.9: Tools & Timeline — Data Bucket & Work Timeline Critique

> **How to run:** Tell your agent *"run substep 54.9"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric; consolidation at 54.11 catches weak findings.

## Context

STEP-54 critiques each feature as a cohesive lifecycle (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android. This substep covers the **Tools group: Data Bucket** (geospatial file repository — list, upload, file detail) **and Work Timeline** (milestones). Blueprint D7 explicitly names Data Bucket's "file inspection" as an open detail-view question, so the file-detail D7 verdict here is a first-class deliverable. Data Bucket is also the only feature whose payload is binary files (`.shp`, `.tiff` via Google Drive) rather than structured rows — upload progress, failure recovery, and file-size honesty are its distinctive critique concerns.

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**. Apply it exactly; IDs are `FC-54.9-NNN`.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8, especially **D7's explicit mention of Data Bucket file inspection**
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `Code/mine-flow-docs/architecture/04-data-model.md` — file metadata and milestone semantics
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md` — Google Drive backend boundary
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head):
- Data Bucket list: `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`
- Upload: `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
- File detail: `lib/features/data_bucket/presentation/pages/file_detail_page.dart` + `file_detail_route.dart` (note: the router shows `tools/data-bucket/:id` — a real detail route exists; this is the D7 exemplar)
- Work Timeline: `lib/features/timeline/presentation/pages/timeline_page.dart` (+ locate the milestone entry surface — form/dialog; verify)
- Report path: verify whether either feature has a ReportType (blueprint doesn't name one here — record presence/absence as a deliberate decision)
- BLoC states: `lib/features/data_bucket/presentation/bloc/`, `lib/features/timeline/presentation/bloc/`

**Does NOT touch:** application code (read-only), other features, the rubric.

## Your task

Apply every 54.1 rubric dimension, both platforms (Web desktop, Android portrait):

1. **Data Bucket lifecycle:** list → upload → back (does the new file appear? optimistic update or refresh?); list → file detail → back. Trace both loops.
2. **Upload UX (the distinctive concern):** progress indication for large geospatial files, cancellation, failure recovery (retry without re-selecting the file?), file-size/type feedback before commit, and mobile file-picker ergonomics. An upload that dies silently on connectivity loss is a data-trust defect — evidence its current behavior precisely.
3. **D7 verdict (first-class deliverable):** file detail as side-sheet inspector vs. full page. Note a detail *route* already exists (`:id`) — weigh deep-linkability (a URL you can share) against the inspector pattern; consider whether Web and Mobile should differ. Verdict + rationale for 54.11.
4. **Upload → sheet migration spec:** D1/D2 changes for the upload form; D4 status (a multi-field upload with picked files is high dirty-loss risk); D5 gap (router shows `tools/data-bucket/upload` exists — verify semantics).
5. **Work Timeline:** milestone list/entry — critique against the rubric; spec the milestone entry sheet (D1/D2/D4/D5); is timeline a *viewing* feature (read-mostly) and does its UI respect that (no fake CRUD affordances, or missing ones that should exist)?
6. **Interaction states, a11y, tokens:** all rubric dimensions; anchored-grep residual Material.
7. **Report path:** presence/absence for both features, recorded as deliberate decisions.

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.9-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, one-sentence why (Explanatory style).
- Runtime optional and honest: name the command, report artifact byte-size + pixel dimensions; 1×1-placeholder class = harness-defect call-out. Unverifiable → `Unverified` + blocker.
- No code changes: app repo `git status` clean at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.9-FINDINGS.md` — coverage table, findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits (54.11 consolidates). Escalate (and record) on: D1–D8/ADR conflicts, runtime contradicting Doc 07, unevidenced runtime claims, same classification problem twice. **Upload-integrity findings** (silent failure, lost file reference) are data-integrity class — escalate prominently.
- Accepted-risk-shaped discoveries go to findings for 54.11's reconciliation.

## Definition of done

- [ ] All rubric dimensions scored, both platforms, for both Data Bucket and Work Timeline.
- [ ] **D7 verdict for file detail recorded with full rationale** (a 54.11 consolidation input).
- [ ] Upload progress/failure-recovery behavior explicitly evidenced.
- [ ] D4/D5 status recorded for upload and milestone entry.
- [ ] Report-path presence/absence recorded as deliberate decisions.
- [ ] Coverage/findings/verification/limitations tables present with IDs and citations.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.9 → Done) and tell the user: *"run substep 54.10"* — in a **fresh chat**.
