# mine-flow — STEP-48.1 Findings: Journey-Integrity Repair Audit (no fake greens)

**Date:** 2026-08-29
**Executor:** Hermes / Claude Opus 4.8
**Branch:** `step-0048-runtime-evidence`
**Prerequisite:** `mine-flow-STEP-48.0-FINDINGS.md` — **GATE: PASSED** (confirmed before starting)
**Scope:** repair only. **No journey was run for evidence** — 48.3–48.12 own that (PLAN decision D1: CI on the branch head is authoritative).

---

## 1. Verdict

All 16 test files under `integration_test/` and all 4 helpers were read and audited. Three
dishonest files and one stubbed helper were repaired; eleven journeys were swept and four
expectation-vs-app conflicts were fixed mechanically; **one conflict is a genuine app-vs-doc
defect and is handed forward, not silently rewritten**.

**No file under `integration_test/` can now report a pass without asserting something real.**
Verified mechanically, not by eye — see §7.

---

## 2. Per-file audit table (16 tests + 4 helpers)

Assertion counts are `expect(` / `fail(` / `expectRlsRefusal(` / `expectReadPermitted(`
occurrences, counted on code lines only (comments excluded), `git show HEAD:<file>` vs. the
working tree. "before → after" is the count change.

| # | File | Asserts (before → after) | Verdict | What changed |
|---|---|---|---|---|
| 1 | `app_boots_test.dart` | 1 → 1 | **clean** | Nothing. Honest gated skip + `return`; asserts `find.byType(EditableText)` (RISK-0009-compliant). |
| 2 | `journeys/auth_journey_test.dart` | 16 → 16 | **clean** | Nothing. The strongest file in the suite: asserts the real `'Masuk'` label, that no token is stored on a failed login, and that `user.email == testUserEmail` (so a hardcoded stub cannot pass). |
| 3 | `journeys/deep_link_journey_test.dart` | 2 → 16 | **repaired (fake green removed)** | `expect(true, isTrue)` **deleted**; whole file rewritten with a real gated body. See §3. |
| 4 | `journeys/data_bucket_journey_test.dart` | 0 → 9 | **repaired (stub removed) + honest-skip** | Dead post-guard code deleted; split Part A (Drive-gated, cites RISK-0017/0018) + Part B (real staging metadata evidence). See §4. |
| 5 | `journeys/rls_authorization_journey_test.dart` | 2 → 21 | **repaired (stub + silent-pass removed)** | Restructured into gated Part A (per-role) + unconditional Part B; the silent `try/catch` denial check now asserts positively. Its two "before" assertions were both `fail()` inside `catch` blocks — **zero `expect()`**. See §5. |
| 6 | `journeys/benchmark_journey_test.dart` | 13 → 15 | **repaired (broken finders)** | Four non-existent field labels and two order-dependent dropdown finders fixed. See §6.1. |
| 7 | `journeys/cut_fill_journey_test.dart` | 10 → 10 | **repaired (wrong siteId)** | `siteId: 'site-1'` → `defaultSiteId`. See §6.2. |
| 8 | `journeys/land_clearing_journey_test.dart` | 8 → 9 | **repaired (RISK-0009 + wrong siteId)** | The suite's only `find.byType(TextField)` removed; `siteId: 'site-1'` → `defaultSiteId`. See §6.2, §6.3. |
| 9 | `journeys/equipment_check_journey_test.dart` | 30 → 31 | **repaired (weak + wrong assertions)** | Three `TextField` finders migrated to `EditableText`; the `'4/5 Lolos'` badge assertion replaced with the badge's real strings. See §6.4. |
| 10 | `journeys/notifications_journey_test.dart` | 12 → 12 | **needs-runtime-decision** | Assertion **kept unchanged** and documented in-file: `NotificationBanner` is never mounted in `lib/`, which contradicts Doc 01/Doc 02. Handed to **48.9**. See §6.5. |
| 11 | `journeys/attendance_journey_test.dart` | 19 → 19 | **clean** | Nothing. Every literal verified against `lib/`; `'Izin sakit shift pagi'` is test-authored input, correctly asserted back out of the UI. |
| 12 | `journeys/daily_log_journey_test.dart` | 20 → 20 | **clean** | Nothing. `'Tambah "Pit Alpha"'` matches `CreatableCombobox`'s interpolated `'Tambah "$query"'` tile; both `maxLines` predicates match the form. |
| 13 | `journeys/inventory_journey_test.dart` | 21 → 21 | **clean** | Nothing. Already anchors text entry on `FTextField`→`EditableText`; uses `ValueKey`s; the `isSupervisor` branch asserts on both sides. |
| 14 | `journeys/reporting_journey_test.dart` | 7 → 7 | **clean** | Nothing. NR-001's control lock is asserted on the real widget properties (`dateSelector.enabled`, `zonePicker.enabled`), which is genuine evidence. |
| 15 | `journeys/timeline_journey_test.dart` | 16 → 16 | **clean** | Nothing. All 11 text finders verified present in `lib/`; the milestone `switch` asserts per status. |
| 16 | `journeys/offline_sync_journey_test.dart` | 26 → 26 | **clean** | Nothing. Already correctly split Part A (gated, named reason) / Part B (unconditional, real Hive + controllable network). The model for what 48.1 applied elsewhere. |
| 17 | `helpers/app_harness.dart` | n/a | **clean** | Nothing. `pumpApp` mirrors `main.dart` init and guards `Supabase.initialize` on `isStagingConfigured`. |
| 18 | `helpers/offline_helper.dart` | n/a | **clean** | Nothing. Honest about its scope (mocks `checkConnectivity` only) — `offline_sync_journey_test.dart` compensates with its own `NetworkInfo`. |
| 19 | `helpers/staging_config.dart` | n/a | **repaired (extended)** | Added `hasCrewAccount`, `isDriveConfigured`, and the Drive service-account defines so journeys can skip on a *specific* named reason instead of an inline `String.fromEnvironment`. |
| 20 | `helpers/login_helper.dart` | 0 → 4 | **repaired (stub completed + silent-pass removed)** | "currently stubbed" docstring gone; role wiring completed; silent `return` replaced with `fail()`; login success now proven. See §5.4. |

---

## 3. Fake green removed — `deep_link_journey_test.dart`

**The defect.** Its second test printed `'Unverified: Auth-guarded routes need a session…'`
and then asserted `expect(true, isTrue)` under the comment *"We pass the test gracefully to
allow CI to proceed"*. The moment 48.2 points CI at this file it reports a pass for work
never done. **Deleted.**

**Also broken, in the first test.** It asserted `find.text('Login')`. A repo-wide grep proves
no `'Login'` string exists anywhere in `lib/` — the login screen's submit button is
`FButton` → `Text('Masuk')` (`login_page.dart:165`). That assertion would have failed for the
wrong reason. Fixed to the real label; a `matchedLocation == /login` assertion was added so
the redirect itself — not just a rendered string — is what is proven.

**What the file now proves** (two tests, both gated on `isStagingConfigured` with a named
reason and `return`):

1. an unauthenticated direct-load of a guarded route redirects to `/login`, and no `AppShell` mounts;
2. all **17** shell-hosted routes resolve by URI *and* keep `AppShell` mounted — the actual RISK-0006 surface (go_router 17→18 shell handling);
3. `/tools/data-bucket/:id` binds its path parameter with `extra == null` and renders `FileDetailRoute`, reaching CF-031's explicit *"File tidak ditemukan."* state rather than a dead end;
4. a standalone non-shell route (`/notifications`) resolves;
5. `signOut()` re-triggers the redirect back to `/login`.

**Stated limitation (deliberately in the file, not hidden):** a genuine *browser* reload
cannot be triggered from inside `integration_test` — the harness owns the page. What is
exercised is the direct-load shape a reload produces (`appRouter.go(uri)` with no `extra`,
after a fresh `pumpApp()`). 48.11 owns the runtime verdict and RISK-0006.

---

## 4. Stub made honest — `data_bucket_journey_test.dart`

**Before:** 0 assertions. A gated skip, then *unreachable* `pumpApp` + `loginAsStagingUser`
calls under `// Stub for the rest of the journey` — dead code that reads like coverage.

**After (D2 respected — Drive stays out of scope):**

- **Part A (Drive-gated).** Skip reason now names `GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL` /
  `GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY`, cites **RISK-0017** (NR-004 upload + abandon/cancel) and
  **RISK-0018** (NR-005 large-file ceiling), and states that STEP-48 defers them deliberately.
  The unreachable code is gone. If Drive credentials are ever injected without the body being
  written, the test **fails** with an explanation rather than passing empty — a credentialed
  run cannot silently report a pass for absent coverage.
- **Part B (staging-gated, no Drive) — new real evidence.** Asserts the `/tools/data-bucket`
  route resolves inside `AppShell`, performs a live RLS-permitted `geospatial_files` metadata
  read against staging Postgres, and asserts the **rendered state agrees with the queried
  data**: rows → `FileCard`s and no empty state; no rows → the documented
  *"Belum ada file yang diunggah"* and no cards. Every rendered row is checked to belong to
  `defaultSiteId`.

**Why Part B stops where it does (recorded, not glossed):** the prompt suggested also covering
the file-picker validation path and the 50 MB ceiling. Both live inside `UploadFilePage`,
which resolves `GoogleDriveService` from `appServices.driveService`; `AppInitializer` leaves
that **null** unless the Drive service-account defines are present (CF-018 — it refuses to
fabricate an empty-credential client) and the page then throws `UnimplementedError`.
Navigating there without Drive credentials would fail for an environment reason, not a product
one. Those two paths are therefore unreachable in STEP-48's configuration and belong to
RISK-0017/0018.

---

## 5. Stub + silent-pass removed — `rls_authorization_journey_test.dart`

**Before:** 0 assertions, and worse than empty. Two distinct defects:

1. the single-user path — the only path that could run — did nothing but `developer.log` + `markTestSkipped`;
2. the per-role path's foreman-delete check was `try { delete } on PostgrestException catch { if (…) log }` — it did **nothing at all** when no exception was thrown, so an RLS hole would have passed silently.

**After — 22 assertions across three tests.**

### 5.1 Positive denial assertions

New `expectRlsRefusal(operation, reason:, cleanup:)` helper: if the operation *completes*, the
test **fails** with a message that says this is a security finding and points at the PLAN's
escalation rule. It also requires the exception to be a `PostgrestException` carrying SQLSTATE
`42501` or a policy message, and runs `cleanup` in the unexpected-success case so a probe row
that should never have been written does not pollute staging.

### 5.2 Denial semantics, read off the migration

Postgres RLS denies a `SELECT` by **filtering rows** and denies writes by **raising 42501**.
Only writes throw. So every "must be refused" assertion is a write, and every read-side
restriction (e.g. `crew_daily_logs_select` limiting crew to `status = 'approved'`) is asserted
as a property of the returned rows. `expectReadPermitted` exists because
`expect(rows, isA<List>())` is a tautology — the real evidence is the absence of a throw, so
the helper makes that explicit with a failure message naming the table and policy.

### 5.3 Structure

- **Part A / supervisor + foreman** — gated on `hasPerRoleAccounts`. Each leg first resolves
  the session's role from `public.users` and **asserts it is the expected role**, so a
  mis-mapped secret cannot make the leg test the wrong policy set. Foreman denial: `INSERT`
  into `zones` (foremen hold only `zones_read_active`).
- **Part A / crew** — gated separately on the new `hasCrewAccount`. **48.0 created
  `crew@mineflow.dev` in staging but published no `TEST_CREW_*` repository secrets**, so this
  leg skips with that exact reason. No other role is substituted.
- **Part B / single user** — unconditional when staging is configured. Proves the role
  resolves through the same `public.users` row `public.current_user_role()` reads (without
  which every policy is inert), that entitled reads succeed, and that an unpermitted write is
  refused. For foreman/crew that is the `zones` INSERT. **For supervisor there is no
  table-level denial** (it holds `FOR ALL` on all nine tables), so the unambiguous denial is
  the unauthenticated path: every policy is `TO authenticated`, so an anon INSERT must be
  refused — which is what distinguishes "RLS is enforced" from "the tables happen to be open".

### 5.4 `login_helper.dart` — role wiring completed, silent pass removed

The prompt asked whether the early `if (!isStagingConfigured) return;` could let a caller
think a login succeeded. It could: a silent return left the test sitting on the login screen,
where a later "screen renders" assertion could pass for the wrong reason — the same class of
defect as a placeholder assertion. All four failure modes now `fail()` loudly:

- missing staging credentials → `fail` telling the caller to guard with `markTestSkipped`;
- **missing credentials for the requested role → `fail`**, never a downgrade. STEP-45's version silently fell back to `TEST_USER_*` for a `role: 'foreman'` call, so a caller could mistake shared-user coverage for role-specific coverage. `supervisor` still falls back to `TEST_USER_*`, which is truthful because 48.0 assigned the shared account the supervisor role;
- not on the login screen when called → `fail`;
- **login not accepted → `fail`**. The helper now asserts the `'Masuk'` button is *gone* afterwards. Previously a rejected sign-in returned normally.

The "Roles are wired in 45.12; currently stubbed" docstring is gone; the docstring now states
the real resolution order and the reason for each `fail`.

---

## 6. Sweep of the remaining eleven journeys

Method: grep alone is insufficient, so every text-ish finder literal
(`find.text`, `textContaining`, `widgetWithText`, `bySemanticsLabel`, `byTooltip`) was
extracted and checked against every string literal in `lib/`, then each miss was read in
context to classify it. 4 mechanical fixes, 1 finding handed forward, 7 explained non-issues.

### 6.1 `benchmark_journey_test.dart` — six broken finders (mechanical)

| STEP-45 finder | Reality in `lib/` | Fix |
|---|---|---|
| `widgetWithText(Column, 'Northing (Y)')` | label is `'Northing (m)'` | corrected |
| `widgetWithText(Column, 'Easting (X)')` | label is `'Easting (m)'` | corrected |
| `widgetWithText(Column, 'Ortho Height')` | label is `'Ortho Height (m)'` | corrected |
| `widgetWithText(Column, 'Ellips Height')` | label is `'Ellips Height (m)'` | corrected |
| `byType(DropdownButtonFormField<String>).first` for **CRS** | the form builds three: Status (l.214) → CRS (l.250) → Orde (l.396), so `.first` was **Status**, which has no `'UTM Zone 51S'` item | anchored to its own `'CRS'` label |
| `…).last` for **Status** | `.last` was **Orde** | anchored to its own `'Status'` label |

Field anchors also moved from `Column` (which matched several nested ancestors) to the
`FTextField` that owns each label. Two `findsOneWidget` guards added so an ambiguous finder
fails loudly instead of silently picking `.first`.

Q4 applied: these are stale *test* expectations against a UI the docs never specified
label-by-label — test defects, fixed here. `'BM-TEST-01'` is test-authored input, correctly
asserted back out of the list.

### 6.2 `cut_fill_` + `land_clearing_journey_test.dart` — wrong `siteId` (mechanical)

Both verified persistence with `getCutFillRecords(siteId: 'site-1')` /
`getLandClearingRecords(siteId: 'site-1')`. `'site-1'` exists nowhere in `lib/` or the
migrations — the app's `defaultSiteId` is `f47ac10b-58cc-4372-a567-0e02b2c3d479`
(`app_constants.dart:55`), which is what the forms save with. The repositories filter
`siteId` client-side, so the filtered list would have been **empty** and the following
`firstWhere` would have thrown `StateError` before any assertion ran. Both now use
`defaultSiteId`.

> **Note handed to 48.4/48.5 (not fixed here — needs a runtime decision):** the app's
> `defaultSiteId` (`f47ac10b-…`) does **not** match the `site_id` in the migrations' column
> default or `supabase/seed.sql` (`00000000-0000-0000-0000-000000000001`). Records the app
> writes and records the seed wrote therefore carry different site ids. This does not break
> the repaired assertions (they query what the app writes), but any journey asserting on
> *seeded* list contents may see an empty list for this reason rather than a code defect.
> There is no `sites` table and no doc pins either value, so which one is canonical is a
> judgement call for the substeps holding real output.

### 6.3 `land_clearing_journey_test.dart` — RISK-0009 violation (mechanical)

The suite's only `find.byType(TextField)`: the notes field was located as
`descendant(of: byType(TextField), matching: byType(EditableText)).last`. Two problems — it
violates the RISK-0009 finder rule, and `.last` depended on widget order across two tabs.
Re-anchored on the notes field's own unique hint
(`'Kondisi lahan, vegetasi, hambatan, dll...'`) with a `findsOneWidget` guard.
`grep -rn "byType(TextField)" integration_test/` now returns no code hits.

### 6.4 `equipment_check_journey_test.dart` — RISK-0009 + a weak assertion

Three `find.widgetWithText(TextField, …)` finders migrated to a
`textFieldLabelled()` helper resolving to `EditableText`. These are plain Material
`TextField`s not currently under a forui `MergeSemantics` subtree, so #191095 does not bite
today — the change enforces one finder style and survives a future migration of these fields
to `FTextField`.

The substantive fix: `expect(find.textContaining('4/5 Lolos'), findsWidgets)` claimed to check
the condition badge but was satisfied by the **submit button** alone
(`'Simpan Inspeksi SOP (4/5 Lolos)'`) — it proved nothing about the badge. The badge actually
renders `'$passedCount dari $totalCount Item SOP Lolos Check'` (with *"dari"*, not a slash)
plus a title. Now asserts the badge's real strings (`'PERLU MAINTENANCE / FLAGGED'`,
`'4 dari 5 Item SOP Lolos Check'`) and the button separately — three real assertions where
there was one weak one.

### 6.5 `notifications_journey_test.dart` — app-vs-doc conflict, handed to 48.9

**Not fixed here, and deliberately not deleted.** `NotificationBanner` is defined at
`lib/features/notifications/presentation/widgets/notification_banner.dart` but a repo-wide
grep finds **only its own declaration and a widget test** — it is never mounted anywhere in
`lib/`. Doc 01 §Notifications and Doc 02 both specify *"in-app only, with persistent banner
for critical items"*.

Per Q4 the app contradicts the architecture docs, so this is a **bug**, not doc drift.
Deleting the assertion to get green is exactly the laundering STEP-48 exists to prevent.
The assertion stays, now with a `reason:` naming the finding, plus an in-file comment
recording two further facts 48.9 will need: the block is only reached when staging actually
holds a critical unread notification, and the widget requires a `NotificationCubit` ancestor
that the router supplies only on `/notifications` — after the point this check runs.

### 6.6 Explained non-issues (no change; recorded so 48.x does not re-litigate)

| Literal | Why it is correct |
|---|---|
| `'Izin sakit shift pagi'` (attendance) | test-authored remark, entered then asserted back out of `CrewRosterItem`. |
| `'Simpan Absensi'` (attendance) | `textContaining` against the interpolated `'Simpan Absensi (${n} Kru)'`. |
| `'Tambah "Pit Alpha"'` (daily log) | matches `CreatableCombobox`'s `'Tambah "$query"'` tile. |
| `'140.0 m³'` (cut/fill) | matches `'${netVolume.toStringAsFixed(1)} m³'`; 100 BCM + 50 LCM ÷ 1.25 = 140.0 confirmed against `VolumeNormalizer` (default swell 0.25, no per-material override). |
| `'0.1500'` / `'0.1600'` (land clearing) | match `(planArea / 10000.0).toStringAsFixed(4)`; 1500 m² → 0.1500 Ha. |
| `'4/5 Lolos'` remnant | now only inside the submit-button assertion, which is where it genuinely renders. |
| `'notifikasi'` | `textContaining` against `'${n} notifikasi'`. |
| STEP-38 `AttendanceFormPage` extraction | already reflected: `attendance_journey_test.dart` imports and asserts `AttendanceFormPage` and drives the real `'Input Absensi'` FAB. No stale screen references found. |

---

## 7. Verification (mechanical, on this branch)

| Gate | Result |
|---|---|
| `grep -rn "expect(true" integration_test/` | **no code hits** (one prose mention in the `deep_link` header explaining what was removed) |
| `grep -rn "byType(TextField)" integration_test/` | **no code hits** (one prose mention in the `land_clearing` fix comment) |
| `grep -rn "Stub\|we would:" integration_test/` | **no code hits** (one prose mention in the `data_bucket` header) |
| Every `markTestSkipped(` followed by `return;` | **22 calls checked, 0 problems** (parenthesis-balanced scan, not a line grep) |
| Every `testWidgets` body has an assertion or skip+return | **25 blocks checked, 0 without an assertion** |
| Every finder literal exists in `lib/` | all remaining misses classified in §6.6 |
| `flutter analyze` | **No issues found!** |
| `dart format --set-exit-if-changed .` | clean (326 files, 0 changed) |
| `flutter test` | **448 passed, 0 failed** on re-run — see §7.1 |

Assertion totals across the 16 test files: **203 → 249** (code lines only). Three files went
from placeholder/near-zero assertions to 46 real ones.

### 7.1 Flake diagnosis — not waved through

The **first** full-suite run ended `+447 -1`, failing
`test/integration/equipment_check_sync_test.dart` ("offline creation enqueues mutation and
flushes when online", `expect(syncedPayloads.length, 1)` got `0`). Diagnosed with the three
independent checks before proceeding:

1. **Untouched by this substep** — `git diff --stat -- test/` is empty; the file is byte-identical to `master` (`git diff --quiet master..step-0048-runtime-evidence -- <file>` → identical). 48.1 changed only `integration_test/` and cannot affect it.
2. **Green in isolation** — `flutter test test/integration/equipment_check_sync_test.dart` passed **twice** (3/3); the whole `test/integration/` directory passed (21/21).
3. **Green on a clean full re-run** — `flutter test` → **448 passed, 0 failed, exit 0**.

Verdict: an order-dependent shared-state flake in the Hive-backed sync integration tests
(the timing-sensitive `Future.delayed(100ms)` drain), the same family as the known
`attendance_daily_log_sync_test.dart` flake recorded in the STEP-47 index row — a
**sibling** of it, not the same file, so it is worth noting as a second instance. Not a
regression, and not hidden.

---

## 8. Handed forward

| Finding | Type | Owner |
|---|---|---|
| `NotificationBanner` never mounted, contradicting Doc 01/Doc 02 | **app defect** (Q4: app contradicts doc) | **48.9**; if confirmed at runtime, 48.14 raises the RISK row and 48.15 records the doc position |
| `defaultSiteId` (`f47ac10b-…`) ≠ migration/seed `site_id` (`00000000-…0001`) | data/config mismatch; may make seeded-list assertions look like code defects | **48.4 / 48.5**, with real output in hand |
| Crew leg of the RLS matrix unrunnable — account exists, `TEST_CREW_*` secrets do not | credential gap | **48.12** (either add the two secrets or record the matrix as partial with this trigger) |
| Data-bucket file-picker validation + 50 MB ceiling unreachable without Drive (CF-018 leaves `driveService` null) | deferred scope (D2) | **48.14** — fold into RISK-0017/0018's re-justification |
| Second Hive sync-integration flake (`equipment_check_sync_test.dart`), sibling of the known `attendance_daily_log_sync_test.dart` one | test-infra flake | **48.15** at the final gate; consider one RISK row for the family |

No architecture doc was edited in this substep (correct per the prompt: repairs must not
change an architecture decision; 48.15 owns doc edits, 48.14 owns `registries/risks.yml`).

---

## 9. Next

Next action: **"run substep 48.2"** (CI gate expansion + evidence artifacts) in a **fresh chat**.
