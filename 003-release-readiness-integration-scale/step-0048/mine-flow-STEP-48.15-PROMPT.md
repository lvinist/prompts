# mine-flow — STEP-48.15: Docs-True Sweep, Index Correction & STEP Close

> **How to run:** tell your agent *"run substep 48.15"*. Self-contained — runnable cold.

**Assigned model: Claude Opus 4.8.** The third and last substep that justifies the heaviest tier,
because it writes the durable record: it rewrites `architecture/09-environments.md` §4, amends STEP-45's
rows, judges every substep's status against the honesty gate, and delivers the **Phase 4 gate verdict**.
It must be willing to close the STEP with `Deferred` rows and an explicit "not delivered" statement —
the STEP-47 index row is the model for that candour. Optimism here re-creates the exact defect STEP-48
was created to fix. STEP-47 followed the same pattern: 47.9, its close, was Opus.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then **every** findings file from 48.0 through
48.14. This is the closing substep: it makes the durable record match what STEP-48 actually proved,
then archives the STEP.

**Do not start until 48.0–48.14 are all complete.** And do not close on chat history — verify each
substep's state from disk. Phantom closes are a documented mine-flow failure mode (STEP-43), and
STEP-45's stranded close is the reason this whole STEP exists.

Three things make this substep unusually consequential:

1. **`architecture/09-environments.md` §4 currently contains a sentence STEP-48 was created to make
   false.** It reads: *"a green E2E gate currently proves only that the test harness executes — the
   emulator boots, the APK installs, and the harness runs. The actual 14 staging journeys remain
   Deferred to STEP-48 and are skipped on CI due to missing credentials."* Rewrite it against the real
   evidence, and bump the Version Log (it is at v0.4.0). If some journeys are still Deferred, the new
   text must say **which** — do not replace an honest limitation with a vague success.

2. **STEP-45's substep rows carry an evidence note that must be updated, not deleted.**
   `prompts/STEP-index.md` has a blockquote above the STEP-45 table explaining that `Deferred` there
   means *"the deliverable exists and is committed but has never been executed against a real
   backend/device — the runtime evidence is deferred to STEP-48."* For each 45.x row STEP-48 settled,
   amend the row to cite STEP-48's evidence. The note itself stays (it is the historical record of the
   correction) but should gain a line pointing at STEP-48's outcome.

3. **Phase 4 is gated on this STEP.** The STEP-48 index row says *"Phase 4 must not open until this
   passes."* If material items ended Deferred, say so plainly in the close and state whether the gate
   is satisfied. That judgement belongs to the user — present the evidence and a recommendation.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the definition of done you are checking against.
- **Every** `Upcoming Prompts/mine-flow-STEP-48.*-FINDINGS.md`.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/METHOD.md` §6 (keeping docs true), §10 (next-action resolver).
- **`prompts/README.md`** — the authoring/archiving recipe, especially step 6 (gather
  `Upcoming Prompts/` files into `step-NNNN/`).
- `Code/mine-flow-docs/runbooks/collaboration.md` — edit only your own rows in shared tables; never
  re-sort or reflow.
- **`Code/mine-flow-docs/architecture/09-environments.md`** v0.4.0 — §4 and the Version Log.
- **`Code/mine-flow-docs/architecture/12-test-strategy.md`** v1.2 — its E2E framing, the dual-platform
  gate, and its Version Log. Its v1.1 row notes ADR-0017 expanded the E2E tier; if STEP-48 changed the
  real shape (e.g. an aggregating entrypoint, a zero-executed guard, screenshot capture as a tier),
  reflect it.
- `prompts/STEP-index.md` — STEP-45's rows and note, STEP-48's row, and the substep-table convention.
- `prompts/003-release-readiness-integration-scale/README.md` — the phase summary table you append to.
- `Code/mine-flow-docs/architecture/README.md` — the doc index with per-doc version/status columns.
  STEP-50 reconciled it; keep it accurate if you bump any doc's version.

## Scope

**In scope:** architecture-doc corrections identified across 48.1–48.13 (with Version Log bumps or an
ADR), the STEP-45 row amendments, STEP-48's own index row and substep table, the phase README row, and
the archive.

**Not in scope:** `registries/risks.yml` (48.14 finished it — do not re-edit), test or app code,
rewriting any report (48.13's design review and 48.12's S0-row update are done), root `DESIGN.md` /
`PRODUCT.md` (**generated — never hand-edit**), reserving or planning STEP-51+.

## Your task

### 1. Verify every substep from disk

For 48.0 through 48.14, confirm on disk: the findings file exists, the commits exist on
`step-0048-runtime-evidence` in each repo it claimed to touch, and the artefacts it claimed
(screenshots, report, CI runs) are real. A substep that claims a CI pass must have a run URL you can
fetch.

**The honesty gate applies to the close itself:** a substep may not be recorded `Done` if its own
findings say Unverified/Deferred. Use `Deferred` in the status cell with the detail in the Output
column — free text like "Unverified" breaks `scripts/check.sh`.

### 2. Apply the docs-true corrections

Collect every doc correction handed forward by 48.1–48.13 and apply them:

- **`architecture/09-environments.md`** — rewrite the §4 "harness only" passage; bump the Version Log
  (v0.4.0 → v0.5.0 for a substantive change).
- **`architecture/12-test-strategy.md`** — update if the real E2E shape differs from v1.2; bump its
  Version Log.
- Any other doc named in the findings (04-data-model, 03-architecture-overview, 06-security-threat-model,
  15-native-app-architecture, 16-identity-auth, 07-ui-design-system).

Apply the two-directional rule strictly: **stale doc → fix it and bump the Version Log; app drifted
from a still-correct doc → that is a bug**, and if it was not fixed during the journey substeps it
needs a follow-up STEP row, not a doc edit that blesses the drift. If a correction overturns a settled
decision, write an **ADR** (`templates/adr-template.md`) rather than quietly editing the doc — and
reserve the ADR number the same way as a STEP number: pull, take `max + 1`, add the `adr/README.md`
row, commit, and scan for duplicates:

```bash
grep -oE '^\|[[:space:]]*ADR-[0-9]+' Code/mine-flow-docs/adr/README.md \
  | grep -oE 'ADR-[0-9]+' | sort | uniq -d
```

If you bump any doc's version, keep `architecture/README.md`'s index table in step.

### 3. Amend STEP-45's substep rows

For each of 45.3–45.14 that STEP-48 settled, amend the row's Output column to cite the evidence —
e.g. *"**Verified in STEP-48.4** — CI run \<url\>, N passed"* — while leaving the row's historical
framing intact. Rows STEP-48 could **not** settle stay `Deferred` with an updated pointer to whatever
now owns them (a new risk row from 48.14, or a follow-up STEP). Add a line to the existing blockquote
note recording STEP-48's outcome.

Do not touch other STEPs' rows and do not re-sort the table.

### 4. Write STEP-48's own record

- Flip the STEP-48 row to `Done`, fill in the Owner, and write a scope/outcome summary in the style of
  the STEP-47 row: what was delivered, **with real counts and the CI run URL**, and — critically —
  what was **not** delivered and where it went. STEP-47's row is the model: it states plainly that
  both E2E jobs self-skipped and that no journey was runtime-verified. Match that candour.
- Add a `### STEP-48 substeps` table with rows 48.0–48.15, each with a status from the permitted
  vocabulary and an Output column naming the real deliverable.
- Append the phase README row to `prompts/003-release-readiness-integration-scale/README.md`
  (format: `| STEP-48 | Runtime Evidence — … | 48.0..48.15 | <date> |`).

### 5. Final verification run

Before archiving, run the full gate and record actual output:

```bash
cd Code/mine-flow-app
flutter analyze
dart format --set-exit-if-changed .
flutter test
```

Then confirm a **CI run on the branch head** where `test`, `build-android`, `e2e-web`, and
`e2e-android` all succeed **with non-zero executed journey counts**. A green job reporting only skips
is not a pass — that is the exact failure mode STEP-48 exists to end. Quote the run URL and the
per-job counts in the close.

The `test/integration/attendance_daily_log_sync_test.dart` Hive `setUpAll` flake is known
(intermittent full-suite, green isolated): if it fails, re-run isolated and record which it was.

Also run the project's structural gate from the workspace root:

```bash
./doctor.sh check
```

### 6. Archive

Per `prompts/README.md` step 6, gather from `Upcoming Prompts/` into
`prompts/003-release-readiness-integration-scale/step-0048/`:

- `mine-flow-STEP-48-PLAN.md` (status flipped to `Done`, its definition-of-done checkboxes
  reflecting reality — an unmet box stays unchecked with a note, not silently ticked);
- all sixteen substep prompts `mine-flow-STEP-48.0-PROMPT.md` … `-48.15-PROMPT.md`;
- all findings files `mine-flow-STEP-48.*-FINDINGS.md`.

The design-review **report** stays under `Code/mine-flow-docs/reports/` (state, not history) — only
the PLAN, prompts, and findings move into the archive. Leave `Upcoming Prompts/` holding only
`.gitkeep` and any genuinely-future files (note that
`mine-flow-STEP-47-48-49-RESERVATION-OUTLINE.md` is still there and is still referenced by STEP-49 —
decide with the user whether it archives with this STEP or waits for 49; do not delete it).

If 48.14 referenced archived findings paths in `risks.yml`, verify those paths resolve **after** the
move. A broken ref in the register is a silent failure.

### 7. Merge and push

Merge order per the PLAN: `mine-flow-app` → `mine-flow-docs` → `prompts`. Check each repo's branch
topology before merging (`git -C <repo> log --oneline --left-right --graph origin/master...HEAD`), and
push. For `prompts`, confirm the shared trunk is clean and the STEP-number duplicate scan is empty
before pushing:

```bash
grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md \
  | grep -oE 'STEP-[0-9]+' | sort | uniq -d
git -C prompts diff --check
```

**Do not force-push, reset, or rewrite history.** If a push is rejected, pull and reconcile.

### 8. Tell the user what is next

Run `./doctor.sh status` and report what it resolves. The remaining `Planned` row is **STEP-49**
(Throughstone template hardening) — and note that STEP-49's whole subject is the failure modes STEP-48
just lived through, so this STEP's findings are direct input to it.

State explicitly whether the **Phase 4 gate** is satisfied, with the evidence, and recommend either
opening Phase 4 planning or resolving named residual items first. That is the user's call; give them
the facts and a recommendation.

## Verification

- Every substep 48.0–48.14 verified from disk, not from chat history.
- No substep marked `Done` whose findings say Unverified/Deferred.
- `architecture/09-environments.md` §4 rewritten truthfully with a Version Log bump; any other
  corrected doc likewise; `architecture/README.md` index consistent.
- STEP-45's settled rows cite STEP-48 evidence; unsettled rows point at their new owner.
- STEP-48 row `Done` with real counts and a CI run URL, and an explicit statement of what was not
  delivered.
- `### STEP-48 substeps` table present with all sixteen rows and permitted status values.
- Phase README row appended.
- `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- A CI run on the branch head with all four jobs green **and non-zero executed journey counts**.
- `./doctor.sh check` passes; STEP-id duplicate scan empty; `git diff --check` clean.
- Archive folder contains the PLAN + 16 prompts + all findings; `Upcoming Prompts/` cleared of this
  STEP's files; any `risks.yml` refs to archived paths still resolve.
- All three repos merged in order and pushed; no history rewritten.
- No secret value anywhere in the docs, index, or archive.

## Keeping the docs true

This substep *is* the docs-true pass. Two rules to hold: never edit a doc to bless drift the app
introduced (file a follow-up STEP instead), and never amend an accepted ADR to match code (supersede
or append an amendment). Generated files — root `DESIGN.md`, `PRODUCT.md` — are never hand-edited; if
48.13 reported bridge drift, route it as a separately authorised regeneration task rather than editing
them here.

## Definition of done

- [ ] All substeps verified from disk; statuses honest and from the permitted vocabulary.
- [ ] All doc corrections applied with Version Log bumps, or an ADR written and its number reserved
      with a duplicate scan.
- [ ] `architecture/09-environments.md` §4's "harness only" passage rewritten against real evidence.
- [ ] STEP-45's substep rows amended to cite STEP-48's evidence; its note updated; unsettled rows
      re-pointed.
- [ ] STEP-48 row `Done` with counts, CI URL, and an explicit not-delivered statement; substep table
      written; phase README row appended.
- [ ] Full local gate green and a branch-head CI run with non-zero executed journey counts, quoted.
- [ ] `./doctor.sh check` passes; duplicate scans empty; `git diff --check` clean.
- [ ] PLAN + 16 prompts + findings archived to
      `prompts/003-release-readiness-integration-scale/step-0048/`; `Upcoming Prompts/` cleared of
      this STEP's files; archived refs in `risks.yml` verified to resolve.
- [ ] All three repos merged (app → docs → prompts) and pushed; nothing force-pushed.
- [ ] The user is told the next action (`./doctor.sh status`), given the Phase 4 gate verdict with
      evidence and a recommendation, and told to start a **fresh chat**.

## Next

STEP-49 (Throughstone Template Hardening) is the remaining `Planned` row, and STEP-48's findings —
especially every fake-green and stub 48.1 removed — are its raw material. Tell the user to start a
fresh chat for it, or to open Phase 4 planning if they judge the gate satisfied.
