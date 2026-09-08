# mine-flow — STEP-48.19: Write-Path Dual-Key Purge (`item_name`, `status`, `vegetation_type`)

> **How to run:** tell your agent *"run substep 48.19"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** Bounded reasoning: the migrations state exactly which
columns exist, and each model's `toJson()` states exactly which keys it sends, so every decision has
a written answer. The reasoning that *is* needed is asymmetry — a **read** may stay tolerant of old
key names while a **write** must not — and that distinction is what this substep is about.
**Escalate to Opus 4.8** if removing a key would drop data the app relies on, or if a key's removal
changes a value a user already sees.

## Why this substep exists

Branch-head CI run [`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159)
failed both E2E jobs. Two of the failures are **writes rejected for naming a column that does not
exist**:

```
PGRST204  Could not find the 'item_name' column of 'inventory_items' in the schema cache
PGRST204  Could not find the 'status' column of 'equipment_checks' in the schema cache
```

Both come from the same anti-pattern: a model's `toJson()` writes **both** the old and the new key
name, hoping one of them lands. Postgres rejects the whole row if any key is unknown, so writing both
guarantees failure rather than compatibility.

| File | Emits | Real column (`20260718000001` / `20260723_step_33_1`) |
|---|---|---|
| `lib/features/tracking/data/models/inventory_item_model.dart:57-58` | `'name'` **and** `'item_name'` | `name` only |
| same file, `:62-63` | `'quantity'` **and** `'quantity_on_hand'` | `quantity` only |
| `lib/features/equipment_check/data/models/equipment_check_dto.dart:99` | `'status'` **and** `'is_operational'` | `is_operational` only |
| `lib/features/tracking/data/models/land_clearing_model.dart:66-68` | `'method'`, `'clearing_method'`, **and** `'vegetation_type'` | `method` only — `vegetation_type` was **dropped** by `20260723_step_33_1` |

The land-clearing row has **not fired yet** — the land-clearing journey died earlier, on a finder
error (48.21's scope). It will fire the moment that finder is fixed. Fix the class, not only the
instances that happened to fail.

Also note what the failing writes do to the queue: each rejection is retried by `SyncQueueManager`
(the logs show `Attempt 1/3`, `2/3`, `3/3`) and then the item is dead. A rejected write is not a
cosmetic error — it is **a mutation that never reaches staging**, which is the same failure class
48.10 was escalated for.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, the honesty rule.
- **`Upcoming Prompts/mine-flow-STEP-48.16-FINDINGS.md`** — your scope. It assigns you specific
  `BH-nnn` rows and, importantly, the **"same class, not yet fired"** sweep: every model `toJson()`
  checked against the real migration columns. Work that list.
- `Upcoming Prompts/mine-flow-STEP-48.17-FINDINGS.md` — **hard dependency.** The new
  `timeline_milestones` and `benchmarks` tables define which keys `timeline_milestone_model.toJson()`
  and `benchmark_model.toJson()` may legally emit; match 48.17's landed column list exactly.
- `Upcoming Prompts/mine-flow-STEP-48.18-FINDINGS.md` if 48.18 has run — it may have touched
  `land_clearing`-adjacent code and its audit table already lists column truth per table.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-app/supabase/migrations/`** — the authority. `20260718000001_core_schema.sql`
  for originals; `20260723_step_33_1_data_model_polish.sql` for what was renamed and **dropped**
  (`cut_volume`/`fill_volume`, `area_cleared_ha`, `vegetation_type`); `20260724_…` for the
  geospatial drops.
- `Code/mine-flow-docs/architecture/04-data-model.md` — entity authority.
- **`Code/mine-flow-docs/adr/ADR-0012-volume-and-land-clearing-metrics.md`** and
  **`ADR-0015-plan-actual-date-zone-separation.md`** — these govern the land-clearing and cut/fill
  field semantics. `plan_area`/`actual_area` and the plan/actual date separation are decisions, not
  incidental names.
- `Code/mine-flow-app/lib/features/*/data/sync/*_sync_registrar.dart` — the drained-queue push path.
  48.10 fixed these to push **direct to the remote datasource** with last-write-wins; the payload they
  send is the `toJson()` you are about to change, so a wrong key here re-breaks 48.10's work.
- `Code/mine-flow-app/tool/check_supabase_contracts.dart` — if you touch no migration you will not
  trip it, but read it so you know why hand-editing `supabase/types/database.ts` is not an option.

## The rule to apply

**Reads stay tolerant. Writes must be exact.**

- A `fromJson` may keep `(json['item_name'] ?? json['name'])` — it parses rows from several sources
  (Supabase, Hive cache written by an older app version, a sync payload) and tolerance there costs
  nothing.
- A `toJson` used for a Supabase write must emit **only** columns that exist. If the same `toJson` is
  also used for the Hive cache or the sync-queue payload, that is the real problem to solve — see
  below.

### The trap: one `toJson` serving two destinations

Several models use a single `toJson()` for both the Supabase write and the local Hive/queue payload.
Removing a key to satisfy Postgres can therefore drop a field the local cache or the queue needs.
Check each model for a separate `toHiveJson()` (`benchmark_model.dart` has one) and follow how
`SyncQueueManager` serialises its payload before deleting anything.

If a key is genuinely needed locally but is not a database column, the fix is **separate
serialisers**, not a key that breaks every write. Prefer the pattern already in the codebase
(`toHiveJson`) over inventing a new one. If you introduce a split, add a docstring saying which
destination each method serves — this is exactly the confusion that created the bug.

## Your task

### 1. Complete the sweep

For every model with a `toJson()` in `lib/`, list each emitted key and mark whether the target table
has that column. Include the two new tables from 48.17.

```bash
grep -rln "Map<String, dynamic> toJson()" lib/
```

Produce a table: model file · target table · key · column exists? · destination(s) of this `toJson`
(Supabase / Hive / queue) · action.

### 2. Purge the phantom keys

- `inventory_item_model.dart` — drop `item_name` and `quantity_on_hand` from `toJson`; keep `name`
  and `quantity`. Keep the tolerant `fromJson`.
- `equipment_check_dto.dart` — drop `status` from `toJson`; keep `is_operational`. The `status` field
  itself stays on the DTO (it is derived in `fromJson`:
  `json['status'] ?? (is_operational ? 'passed' : 'flagged')`) and may still be used in the UI —
  **check before assuming**, and if it is used, make clear in a docstring that it is a derived,
  non-persisted view of `is_operational`.
- `land_clearing_model.dart` — drop `clearing_method` and `vegetation_type`; keep `method`.
- Anything else the sweep or 48.16 turned up, including the two new tables.

For each removal, verify no local consumer depended on the removed key by grepping for it across
`lib/` and `test/`.

### 3. Confirm the queue path still works

The sync registrars push `toJson()` payloads straight at the remote datasource. After your edits:

- re-read each `*_sync_registrar.dart` you affect and confirm the payload it builds is the corrected
  one;
- run `test/…/sync_queue_manager_test.dart` and the per-feature sync tests (`attendance_daily_log_sync_test.dart`,
  `equipment_check_sync_test.dart`) — these are the tests 48.10 relied on. Both are known to flake on
  Hive `setUpAll` in a full-suite run: re-run isolated to confirm, and say so explicitly rather than
  reporting a red suite as green.

### 4. Pin it with tests

Add unit tests asserting the **emitted key set**, not just individual values:

```dart
expect(model.toJson().keys, isNot(contains('item_name')));
```

…or better, assert the full key set equals the expected column set, so a *new* phantom key also
fails. Follow the existing conventions in `test/features/…`. This is the test that would have caught
the bug before a branch-head run, and its absence is why the bug shipped.

### 5. Verify against real staging, not just the analyzer

A key-set unit test proves the payload; only a real write proves the column. Run the inventory,
equipment-check, and land-clearing journeys locally against staging and confirm `PGRST204` is gone
and the rows land. Record the ran-vs-skipped counts. If a journey now fails for a different reason,
confirm 48.16's register routes it elsewhere and name that substep — do not fix out of scope.

## Verification

- Every model `toJson()` in `lib/` audited against the real migration columns; table in findings.
- No `toJson` destined for Supabase emits a non-existent column.
- Every removed key confirmed unused by local consumers (grep evidence in findings).
- Where one `toJson` served two destinations, the split is explicit and documented.
- Key-set unit tests added, run, and passing.
- `sync_queue_manager_test` and the per-feature sync tests green (flake diagnosed, not waved).
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean; `flutter test` green.
- Inventory, equipment-check, and land-clearing journeys run against staging without `PGRST204`;
  counts recorded.
- No assertion deleted or weakened to reach green.

## Scope

**In scope:** write-path serialisation across every model; the Hive/queue split where one `toJson`
serves two destinations; tests pinning the emitted key set; the unfired same-class instances.

**Not in scope:** read-path query column names (48.18), migrations or staging DDL (48.17), seed and
fixture data (48.20), finder repair (48.21), UI defects (48.22), persistence/offline defects (48.23),
`risks.yml` edits, and the reporting net-volume formula (RISK-0014, a later reporting STEP).

## Keeping the docs true

If the sweep shows `architecture/04-data-model.md` naming a field the schema does not have, that is
doc drift — fix the doc and bump its Version Log. If a model's field set contradicts ADR-0012 or
ADR-0015, that is a **bug and a finding**; an ADR is superseded deliberately, never retrofitted to
match drifted code. Every changed method keeps or gains a docstring, and any remaining compatibility
read gets a *why* comment.

## Definition of done

- [ ] Full `toJson()` audit table written.
- [ ] `item_name`, `quantity_on_hand`, `equipment_checks.status`, `clearing_method`,
      `vegetation_type` no longer emitted to Supabase.
- [ ] Every other phantom key found by the sweep removed or explicitly justified.
- [ ] Hive/queue serialisation preserved; any serialiser split documented.
- [ ] Key-set unit tests added and passing.
- [ ] Sync tests green (flake diagnosed isolated).
- [ ] `flutter analyze` 0, `dart format` clean, `flutter test` green.
- [ ] Inventory, equipment-check, land-clearing journeys write successfully against staging; counts
      recorded; `PGRST204` gone.
- [ ] `mine-flow-STEP-48.19-FINDINGS.md` written; PLAN progress table updated.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.20"* (staging fixture & seed alignment) in a
**fresh chat**. Flag any file you changed that 48.20, 48.21, or 48.23 will reopen.
