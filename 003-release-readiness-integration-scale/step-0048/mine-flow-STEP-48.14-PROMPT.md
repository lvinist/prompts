# mine-flow — STEP-48.14: Risk-Register Reconciliation

> **How to run:** tell your agent *"run substep 48.14"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** Systematic reconciliation against a fixed schema, driven by
evidence the earlier substeps already wrote down — careful bookkeeping rather than open-ended judgement.
**Escalate to Opus 4.8** before reducing RISK-0011's `high` severity or closing any row whose evidence
is a Deferred verdict, and if the RISK-0017/0018 trigger-accuracy problem turns out to be broader than
those two rows (i.e. if other triggers also state reasons that are no longer true).


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then **every** findings file from 48.0 through
48.13. This substep owns `Code/mine-flow-docs/registries/risks.yml` for STEP-48: the journey substeps
deliberately did **not** edit it, each instead writing a close-or-re-justify recommendation with
evidence. Your job is to apply those recommendations coherently, in one pass, so the register tells
the truth after this STEP.

Do not start until 48.3–48.13 are all complete. A partial reconciliation is worse than none: it
creates a register that looks reviewed but is half-stale.

STEP-48's inbound risk rows, and what should decide each:

| Row | Status now | Owning substep | What should decide it |
|---|---|---|---|
| **RISK-0006** | `open` — go_router v18, deep-link E2E unverified | 48.11 | Real deep-link evidence across all routes; note its trigger is *"Before production release, when staging credentials are available"* — that condition is now met |
| **RISK-0011** | `open`, **high**, privacy — in-app privacy notice absent | 48.13 | Runtime observation. If still absent it **stays open as a pre-release gate**; do not downgrade a high-severity privacy gate because a STEP ended |
| **RISK-0015** | `monitoring` — LoginPage light-mode (NR-002) | 48.13 | Screenshot evidence |
| **RISK-0016** | `monitoring` — sidebar active-state on web (NR-003) | 48.13 | Per-group-route web screenshot evidence |
| **RISK-0017** | `monitoring` — Drive upload abandon/cancel (NR-004) | — | **Stays Deferred** per PLAN decision D2. Re-justify with a sharper trigger; do not close |
| **RISK-0018** | `monitoring` — large-file OOM ceiling (NR-005) | — | Same as RISK-0017 |
| **RISK-0019** | `monitoring` — Benchmark deep-link (NR-006) | 48.7 | Web route-registration evidence |

Rows that STEP-48's runs may have produced new information about, even though they are not its
targets: **RISK-0008** (flutter_secure_storage v9→v11 skip — 48.3 was its first live-backend
exercise), **RISK-0014** (reporting path still on the legacy `cut − fill` formula — 48.5 and 48.8
were asked to confirm it still describes reality, **not** to fix it), **RISK-0007** (Hive → `hive_ce`
fork durability — 48.10's queue-persistence evidence is the strongest the project has), **RISK-0003**
and **RISK-0004** (accepted UI-drift and localization deferrals that 48.6/48.9/48.13 checked findings
against), **RISK-0009** (the `EditableText` finder rule the whole suite depends on), **RISK-0010**
(staging provisioned via ClickOps — 48.0 touched staging setup).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the honesty rule and decision D2 (Drive out of scope).
- **Every** `Upcoming Prompts/mine-flow-STEP-48.*-FINDINGS.md` — these are your evidence base.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-docs/registries/risks.yml`** — the whole file. Note its schema: `id`, `status`,
  `title`, `category`, `severity`, `owner`, `opened`, `source`, `description`, `impact`, `mitigation`,
  `revisit_trigger`, `refs`, `closed: {date, reason}`.
- `Code/mine-flow-docs/METHOD.md` §6 and the register's own header comments — how rows are opened,
  closed, and referenced.
- `Code/mine-flow-docs/reports/2026-08-29-step-0048-runtime-design-review.md` (48.13's report) and
  `Code/mine-flow-docs/reports/security/2026-08-26-step-0044-s0-security-baseline-report.md` (whose
  live-RLS row 48.12 updated) — both are `refs` targets.

## Scope

**In scope:** `registries/risks.yml` only. Closing rows whose evidence justifies it, re-justifying
rows that must stay open, raising new rows for deferrals STEP-48 created.

**Not in scope:** architecture docs, the STEP index, phase READMEs, the archive (all 48.15), test or
app code (the journey substeps owned that), rewriting any report.

## Your task

### 1. Build the evidence table first

Before touching the file, tabulate every inbound row against the findings: which substep produced
evidence, what the evidence was (CI run URL, counts, screenshot path, report section), and what that
substep recommended. If a recommendation is missing or ambiguous, **go read the findings file** rather
than inferring. If a substep reported Deferred, the corresponding risk cannot close.

### 2. Apply closures where evidence genuinely supports them

For each row you close: set `status: closed`, fill `closed.date` and `closed.reason`, and add the
evidence to `refs` — the CI run URL, the report path, or the findings path. A closure whose reason is
"verified in STEP-48" without a pointer is not auditable; name the artefact.

The register is an **index**: it references the report or ADR that carries the detail. If a closure's
detail lives only in an `Upcoming Prompts/` findings file, note that 48.15 archives those into
`prompts/003-release-readiness-integration-scale/step-0048/` — reference the **archived** path so the
ref does not break, and confirm with 48.15's plan that the path is right.

### 3. Re-justify rows that stay open — properly

A row that stays open needs more than an unchanged trigger. Update `description` to reflect what
STEP-48 *did* establish, and sharpen `revisit_trigger` so it names a condition someone can actually
check. Two specific cases:

- **RISK-0017 / RISK-0018** stay Deferred by decision D2. Their current triggers read *"When staging
  Google Drive credentials are available"* — but the Drive **service-account secrets already exist in
  CI** (`STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL`, `…_KEY`, `…_FOLDER_ID`, confirmed live during
  planning). So the stated trigger has arguably already fired, and the real reason these stay open is
  that STEP-48 **scoped them out**, not that credentials are missing. Rewrite the triggers to say what
  is true — e.g. deferred by decision to a named future STEP — otherwise the register misrepresents
  why a risk is open. Flag this to the user; it is the kind of quiet inaccuracy that makes a register
  untrustworthy.
- **RISK-0011** — if the privacy notice is still absent, it stays `open`, `high`, and a pre-release
  gate. Add 48.13's runtime confirmation to `refs` and `description`. Do not soften severity.

### 4. Raise new rows for deferrals STEP-48 created

Likely candidates, depending on findings:

- **A partial RLS matrix** (if 48.0 could not create per-role accounts): 48.12 was asked to recommend
  a row. A partial authorization matrix is a *new* deferral — RISK-0015…0019 are STEP-45's
  carry-forwards and none covers it.
- **Any journey that ended Deferred** rather than Verified: it needs a row, an owner, and a trigger,
  or it evaporates the moment the STEP closes. This is precisely how STEP-45's items nearly got lost.
- **Any defect found but deliberately not fixed** in a journey substep.
- **Design-review findings** from 48.13 marked Needs-remediation or Unverified that have no owning
  STEP yet.

Number new rows as `max + 1` (currently RISK-0020 is the maximum, so start at RISK-0021), and check
for duplicates before finishing:

```bash
grep -oE '^[[:space:]]*- id: RISK-[0-9]+' Code/mine-flow-docs/registries/risks.yml \
  | grep -oE 'RISK-[0-9]+' | sort | uniq -d
```

An empty result is the expected success. Note the file has an existing ordering quirk — RISK-0009 sits
between 0007 and 0008 — so **do not re-sort or reflow the file**; the collaboration rules forbid
re-sorting shared table/registry files. Append new rows and edit only the rows you own.

### 5. Update the incidental rows where STEP-48 learned something

RISK-0008 (secure-storage v11 against a live backend), RISK-0007 (Hive fork durability), RISK-0014
(reporting formula still legacy), RISK-0010 (staging provisioning). Add the new evidence to
`description`/`refs` where it materially changes the picture. Do **not** close RISK-0014 — its trigger
names a future reporting STEP and 48.5/48.8 were explicitly forbidden from fixing it.

### 6. Validate the file

```bash
# YAML must still parse
python -c "import yaml,sys; yaml.safe_load(open('Code/mine-flow-docs/registries/risks.yml'))"
# structural gate
./doctor.sh check      # or Code/mine-flow-docs/scripts/check.sh
```

`scripts/check.sh` validates status vocabulary across the project's tables — remember index/PLAN
status cells accept only `Planned` / `In progress` / `Done` / `Deferred` / `Abandoned` / `N/A`. The
risk register has its own `status` vocabulary (`open`, `monitoring`, `closed`); use what the file
already uses and do not invent a value.

### 7. Record it

`Upcoming Prompts/mine-flow-STEP-48.14-FINDINGS.md`: a table of every row touched with before/after
status and the evidence ref; every new row with its rationale; the RISK-0017/0018 trigger-accuracy
issue and how you resolved it; the duplicate-scan result; the `check.sh` result.

## Verification

- Every inbound row (RISK-0006, 0011, 0015, 0016, 0017, 0018, 0019) has an explicit disposition —
  closed with evidence, or re-justified with an accurate description and trigger.
- No row closed without a `refs` pointer to a real artefact.
- Every Deferred journey and unfixed defect from 48.3–48.13 has a row, an owner, and a trigger.
- Duplicate RISK-id scan returns nothing.
- YAML parses; `./doctor.sh check` passes.
- The file is **not** re-sorted or reflowed; only owned rows changed plus appended new ones.
- RISK-0011's severity not reduced without the notice actually existing.
- No secret value anywhere in the register.

## Keeping the docs true

The register is an index, not a narrative — each row points at the report, ADR, or archived findings
file carrying the detail. If a row needs a source that does not exist yet, create the source first or
reference the archived STEP-48 findings path 48.15 will produce. Architecture-doc corrections
identified by the journey substeps belong to **48.15**, not here; if a finding implies a doc edit,
pass it along rather than doing it.

## Definition of done

- [ ] Evidence table built from every 48.x findings file before any edit.
- [ ] RISK-0006, 0011, 0015, 0016, 0019 each closed with evidence refs or re-justified with an
      accurate description and trigger.
- [ ] RISK-0017 / RISK-0018 re-justified as scoped-out-by-decision (D2), with triggers that state the
      real reason rather than the stale "credentials unavailable" one.
- [ ] New rows raised (from RISK-0021 up) for every deferral STEP-48 created: partial RLS matrix, any
      Deferred journey, any unfixed defect, any unowned design-review finding.
- [ ] Incidental rows (RISK-0007/0008/0010/0014) updated where STEP-48 produced new evidence;
      RISK-0014 **not** closed.
- [ ] Duplicate-id scan empty; YAML parses; `./doctor.sh check` passes; file not re-sorted.
- [ ] `Upcoming Prompts/mine-flow-STEP-48.14-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence` in `mine-flow-docs`.

## Next

Tell the user the next action is *"run substep 48.15"* (docs-true sweep, index correction, and STEP
close) in a **fresh chat**, and update 48.14's status in the STEP PLAN.
