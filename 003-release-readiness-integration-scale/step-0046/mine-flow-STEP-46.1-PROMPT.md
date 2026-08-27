# mine-flow — STEP-46.1 PROMPT
# Pass 1a: Code-Level Static Scan — All 24 Screens

**STEP:** 46.1 of STEP-46
**Model:** Flash-tier (Gemini Flash or equivalent lightweight model)
**Reads from disk:** `Code/mine-flow-docs/architecture/07-ui-design-system.md`, `Code/mine-flow-docs/overview.md`, all 24 screen files + their primary BLoC/Cubit/state files and key widget files
**Writes:** `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.1-FINDINGS.md`

---

## Context

You are running Pass 1a of the STEP-46 UI/UX audit. This is a **code-reading-only** pass — no fixes, no screenshots. Your job is discovery: flag anything in the code that looks functionally wrong, visually broken, or inconsistent with the design spec, so a stronger model can later confirm or reject each finding.

Read these before scanning:
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (v0.3.0) — the canonical design spec (ForUI Zinc tokens, Geist font, compact spacing, WCAG 2.1 AA, l10n scaffold).
- `Code/mine-flow-docs/overview.md` — the three user roles (supervisor, foreman, crew) and stated capabilities.
- `lib/app/router.dart` — route definitions and how each screen receives its dependencies.
- `.throughstone/local-user.md` at workspace root — your communication baseline.

---

## Screens to scan (24 total)

For each screen below, read:
1. The screen file itself.
2. Its primary BLoC or Cubit file (look under `bloc/` or `cubit/` in the same `presentation/` tree).
3. Its primary state class.
4. Any key widget files it delegates to (look in the same feature's `presentation/widgets/` folder).

| ID  | Screen file (relative to `lib/`)                                                    |
|-----|-------------------------------------------------------------------------------------|
| S01 | `features/auth/presentation/pages/login_page.dart`                                  |
| S02 | `app/presentation/pages/dashboard_page.dart`                                         |
| S03 | `app/presentation/pages/group_landing_page.dart`                                     |
| S04 | `features/settings/presentation/pages/settings_page.dart`                           |
| S05 | `features/attendance/presentation/pages/attendance_screen.dart`                      |
| S06 | `features/attendance/presentation/pages/attendance_form_page.dart`                  |
| S07 | `features/daily_log/presentation/pages/daily_log_list_screen.dart`                  |
| S08 | `features/daily_log/presentation/pages/daily_log_form_screen.dart`                  |
| S09 | `features/tracking/presentation/pages/cut_fill_list_screen.dart`                    |
| S10 | `features/tracking/presentation/pages/cut_fill_form_screen.dart`                    |
| S11 | `features/tracking/presentation/pages/land_clearing_list_screen.dart`               |
| S12 | `features/tracking/presentation/pages/land_clearing_entry_screen.dart`              |
| S13 | `features/tracking/presentation/pages/inventory_dashboard_screen.dart`              |
| S14 | `features/tracking/presentation/pages/inventory_item_entry_screen.dart`             |
| S15 | `features/equipment_check/presentation/pages/equipment_history_screen.dart`         |
| S16 | `features/equipment_check/presentation/pages/equipment_check_form_screen.dart`      |
| S17 | `features/benchmark/presentation/pages/benchmark_list_screen.dart`                  |
| S18 | `features/benchmark/presentation/pages/benchmark_form_screen.dart`                  |
| S19 | `features/timeline/presentation/pages/timeline_page.dart`                           |
| S20 | `features/data_bucket/presentation/pages/data_bucket_list_page.dart`               |
| S21 | `features/data_bucket/presentation/pages/upload_file_page.dart`                    |
| S22 | `features/data_bucket/presentation/pages/file_detail_page.dart`                    |
| S23 | `features/reporting/presentation/pages/report_config_page.dart`                     |
| S24 | `features/notifications/presentation/pages/notification_list_page.dart`            |

---

## What to flag (not an exhaustive checklist — look for anything suspicious)

These categories define the *class* of issue. Look for all of them, but also flag anything outside this list that a first-time user (supervisor, foreman, or crew member) would notice as wrong or confusing:

### P1 — Functional / data correctness (breaks the app's purpose)
- **Hardcoded data submitted as real:** literal strings or values that look like placeholder data but are actually submitted to the backend or shown as real (e.g., `foremanId: ''` in a route builder, `siteId: 'default-site'`, a hardcoded timestamp, a fixed employee name).
- **Data binding mismatch:** a widget reads from state field X but its label or a nearby widget says Y (e.g., a card shows `entry.createdAt` but the label says "Tanggal Pekerjaan", when those fields differ in the data model).
- **Navigation dead-end:** a screen has a button or FAB that navigates to a route that requires `state.extra` but the caller doesn't pass it, resulting in the fallback bare-Scaffold path (already spotted: `report_config_page.dart` at `/reports/config` requires `ReportType?` via `state.extra`; any screen pushing this route without extra is a P1).
- **Missing empty / error / loading state:** a BLoC emits `Loading`, `Success`, and `Failure` states but the screen only handles one or two of them — the unhandled state shows nothing or the wrong UI.
- **Role-gated action not gated:** a screen shows a "delete" or "edit" action that should only be visible to supervisors but has no role check visible in the widget or BLoC.

### P2 — Layout / visual correctness (broken at some viewport)
- **Missing `Expanded` or `Flexible` in `Row`/`Column`:** a `Text` or `Widget` child of a `Row` that is not wrapped in `Expanded`/`Flexible` and has no explicit width — will overflow on narrow screens.
- **Unconstrained `ListView` inside `Column`:** a `ListView` (or `GridView`) inside a `Column` without `shrinkWrap: true` or an `Expanded` wrapper — causes unbounded height errors.
- **`Text` without overflow handling in a constrained context:** a `Text` widget displaying a user-supplied string (name, zone, remark) with no `overflow: TextOverflow.ellipsis` or `softWrap` in a fixed-width card.
- **Form fields that clip on narrow screens:** form rows with two side-by-side inputs (e.g., BCM/LCM columns) that will overflow on a 360dp phone width.

### P2–P3 — Token / cosmetic inconsistency (DESIGN.md violation)
- **Raw `Color(...)` or `Colors.X` not from `FTheme`:** any direct use of `Color(0xFF...)`, `Colors.red`, `Colors.grey`, etc. in a widget that should be using ForUI Zinc theme tokens via `context.theme.colorScheme` or `FTheme.of(context)`.
- **Raw `TextStyle(...)` not from theme:** inline `TextStyle(fontSize: ..., color: ...)` rather than `context.theme.typography.X`.
- **Spacing values off the compact scale:** padding or margin values that are not on the 4/8/12/16/20/24/32 dp scale (e.g., `EdgeInsets.all(10)`, `EdgeInsets.symmetric(vertical: 6)`).
- **Button type inconsistency:** a destructive action using a primary-style `FButton` instead of the destructive variant; a secondary action using the wrong ForUI button type.

### P1–P2 — i18n
- **Hardcoded Indonesian string not routed through `AppLocalizations`:** any string literal in a widget that is a user-visible label, button text, or message (e.g., `Text('Simpan')`, `'Berhasil disimpan'`) and is not retrieved via `AppLocalizations.of(context)` or equivalent. Cross-reference with `lib/l10n/` to see what is and isn't covered (RISK-0004).

---

## Output format

Write findings to `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.1-FINDINGS.md`.

Create the folder `prompts/003-release-readiness-integration-scale/step-0046/` if it does not exist.

Use this structure exactly (so the STEP-46.3 model can parse it mechanically):

```markdown
# STEP-46.1 — Code-Level Static Scan Findings

Generated: <date>
Screens scanned: 24
Total candidates: <N>

## Findings

### F-001 | P1 | S09 CutFillListScreen
**File:** `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
**Lines:** 42–44
**Category:** Hardcoded data — foremanId is always empty string
**Evidence:** `CutFillListScreen(repository: ..., siteId: defaultSiteId, foremanId: '')` — the router always passes `foremanId: ''`. If the filtering logic uses this field, all users see all crew's data regardless of role.
**Severity:** P1

---

### F-002 | P2 | S11 LandClearingListScreen
...
```

Rules for the findings list:
- One finding per numbered entry. Do not group multiple issues into one entry.
- Every finding MUST include: severity tier, screen ID, file path, line range, category, and a one-paragraph explanation of WHY it is wrong (not just what it is).
- Do not speculate beyond what the code shows. If you are uncertain, write "Uncertain — recommend 46.3 confirmation."
- Do not include findings for third-party package internals (ForUI, go_router, etc.) — only project code.
- If a screen has no findings, include a one-line "S0N: No findings." entry so the record is complete.

---

## After writing the findings file

1. Run `flutter analyze` from `Code/mine-flow-app/` and append any new analyzer warnings (not already in a finding) as P2/P3 entries at the end of the findings list.
2. Commit `mine-flow-STEP-46.1-FINDINGS.md` to the `step-0046-ui-ux-audit` branch in `prompts/`.
3. Update `prompts/STEP-index.md` substep 46.1 to `Done`.
4. Tell the user: "46.1 complete — N findings. Ready to run 46.2 (screenshot review) and/or proceed to 46.3 once both passes are done."
