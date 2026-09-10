# mine-flow — STEP-54.1 Findings: Critique Rubric, Token Vocabulary & Shell/Navigation Foundation

**Date:** 2026-09-11
**Executor:** Hermes/Claude Opus 4.8
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique` at `fe12531`
**Scope:** Read-only critique of the authenticated shell, group landing pages, routing, header, and the nine feature entry points. No application code was modified.

## 1. Scope and evidence boundary

This is a static critique. The mandatory evidence floor is met with branch-head `file:line` citations. No browser, Android emulator, or screenshot capture was run in this substep; therefore visual, touch, screen-reader, contrast, and runtime URL claims are marked `Unverified` rather than inferred from source code. The screenshot placeholder class remains a harness defect, not evidence, per RISK-0015/0016/0023 and the STEP-48 design-review retraction.

The inspected source files were:

- `Code/mine-flow-app/lib/app/presentation/pages/app_shell.dart`
- `Code/mine-flow-app/lib/app/presentation/pages/group_landing_page.dart`
- `Code/mine-flow-app/lib/app/presentation/widgets/global_app_header.dart`
- `Code/mine-flow-app/lib/app/router.dart`
- feature list/form route call sites cited below
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md`

## 2. Reusable critique rubric

Every later STEP-54 critique must apply these dimensions to its feature lifecycle (List → Form sheet → Detail → Report), on both Web/desktop and Android/mobile. A check is only a finding when its source citation is present; otherwise record it as a hypothesis or `Unverified` item.

### 2.1 Lifecycle cohesion

- The list exposes the feature's primary create/edit action and the action opens the intended form surface without a dead end.
- The form can return to the list while preserving the list's filters/position and refreshing saved data deliberately.
- A record can reach its detail/inspection surface where the feature needs one; the detail surface has a clear return path.
- The contextual report action retains the feature context and the list's current filter state instead of routing to an unrelated picker.

### 2.2 Platform conformance

- Web/desktop forms follow D1: a modal right-side sheet, 480–600dp, without obscuring the permanent sidebar.
- Android/mobile forms follow D2: a modal, draggable/scrollable bottom sheet in the thumb zone.
- D5 is satisfied: opening a form changes the GoRouter URL, and refresh/back/forward reconstruct the same form state or an explicit safe fallback.
- Navigation follows Doc 07 §4: collapsible sidebar on Web and exactly five primary bottom-bar items on Android.

### 2.3 Interaction states

- Loading is explicit and does not flash an empty state or stale success state.
- Empty distinguishes first-use/no-data from no-results-after-filter and offers the appropriate next action.
- Error states explain the problem and expose a retry path without losing user-entered or filter state.
- Success and dirty states are explicit: save feedback is visible, and every dismiss path is intercepted when edits are unsaved.

### 2.4 Accessibility

- Foreground/background and status colors meet the Doc 07 WCAG 2.1 AA target in both light and dark themes.
- Mobile interactive controls have a usable target of at least 48dp, including icon-only actions and close/back controls.
- Controls, cards, status changes, errors, and navigation landmarks have meaningful semantics and labels; decorative icons are excluded.
- Layout remains usable under text scaling, keyboard focus, and reduced-motion preferences; keyboard activation works on Web.

### 2.5 Token conformance

- Use ForUI components and `FTheme` semantic colors/typography; no new residual Material component or raw color is introduced.
- Use the Zinc palette, compact spacing, standard ForUI borders/radii, and Geist/default ForUI typography.
- Use Lucide icons consistently and avoid ad-hoc icon families or decorative icon-only controls without labels.
- Motion stays within the Doc 07 150–200ms snappy range and avoids unbounded/bouncy transitions.

### 2.6 D1–D8 conflict scan

- Compare the implementation with every locked decision D1–D8, especially sheet placement, scrim/modality, dirty interception, URL synchronization, contextual reports, and 1:1 substep parity.
- Record a contradiction as a conflict finding; do not silently reinterpret or fix a locked decision inside a critique.
- Distinguish a missing implementation from an unverified runtime claim.
- If the critique would overturn a locked decision or accepted ADR, escalate it to the user/54.11 rather than resolving it locally.

### 2.7 Findings IDs, verdicts, and coverage format

- Findings IDs are `FC-54.<M>-<NNN>`, sequential within substep M and never reused. This file uses `FC-54.1-*`.
- Use exactly these verdicts: **Aligned**, **Needs polish** (token, copy, or local interaction correction), **Needs restructure** (layout/flow correction), and **Unverified** (runtime behavior or visual/a11y claim without evidence).
- Apply a verdict to every finding and provide an overall verdict for each surface/platform pair.
- Coverage tables use: **Surface / Platform / States exercised / Evidence / Result**.

## 3. Shell and navigation model observed

### 3.1 Platform structure

- The shell switches at `_kBreakpoint = 800` in `app_shell.dart:33-35`; `LayoutBuilder` chooses wide at `maxWidth >= 800` and narrow below it in `app_shell.dart:210-218`.
- Wide layout renders a collapsible `FSidebar` and global header in `app_shell.dart:269-318`; the sidebar width animates from 256 to 0 in `app_shell.dart:275-301`.
- Narrow layout renders the `FBottomNavigationBar` with five configured items in `app_shell.dart:47-57` and `app_shell.dart:394-420`.
- The five mobile items are Dashboard, Tools, Operations, Teams, and Settings (`app_shell.dart:47-57`). Their branch mapping is also documented in `router.dart:4-10`.
- Desktop sidebar items are grouped as General, Tools, Operations, Teams, and Other (`app_shell.dart:84-194`). The feature mapping is direct for Data Bucket, Cut/Fill, Land Clearing, Benchmark DB, Attendance, Daily Log, Inventory, Equipment Check, and Timeline.

### 3.2 Group hierarchy and reachability

The group landing routes expose the remaining feature tiles: Tools has Data Bucket (`router.dart:154-170`), Operations has Cut/Fill, Land Clearing, and Benchmark DB (`router.dart:228-255`), and Teams has Attendance, Daily Log, Inventory, Equipment Check, and Timeline (`router.dart:311-350`). Consequently, the nine feature surfaces are reachable in one desktop sidebar activation or two mobile activations (bottom-bar group, then tile), subject to the mobile header/accessibility gaps below.

The hierarchy is defensible for the field: five stable thumb-zone destinations avoid a ten-item bottom bar, while feature tiles provide the second level. It is not yet fully cohesive because group landing pages have no mobile shell header of their own and the current mobile shell hides the global header outside the dashboard (`app_shell.dart:394-400`).

## 4. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.1-001 | Needs restructure | Mobile shell/header | The narrow shell only renders `GlobalAppHeader` when the current path is exactly `/` (`app_shell.dart:397-398`), then renders the notification banner and branch content (`app_shell.dart:399-400`). Feature pages supply their own local `FHeader`, but group landing pages do not. This removes search, theme, notifications, and profile access on Operations/Teams/Tools landings and makes the shell's global controls path-dependent. | `app_shell.dart:383-423`; group landing has only page content and no header (`group_landing_page.dart:23-79`). | STEP-55.10 should provide one consistent mobile shell header strategy: keep the global controls on every authenticated shell route or deliberately replace them with an equivalent local header. Validate at group landings and every feature route. |
| FC-54.1-002 | Needs polish | Desktop sidebar state | Sidebar selection is computed only from exact equality or a child-path prefix (`app_shell.dart:359-365`). The sidebar has child-feature routes such as `/operations/cut-fill`, not the group route `/operations` (`app_shell.dart:109-134`), so the Operations group landing has no selected feature item; the same applies to `/tools` and `/teams`. This contradicts the intended group-route active-state behavior recorded in the earlier DR-0002 review. | `app_shell.dart:359-365`; group landing item routes `app_shell.dart:97-131`, `app_shell.dart:135-173`. | STEP-55.10 should define and test group-route highlighting (section or parent state) without falsely selecting multiple child features. Do not patch it in this critique. |
| FC-54.1-003 | Aligned | Mobile primary navigation | The bottom bar has exactly five items as required by Doc 07: Dashboard, Tools, Operations, Teams, Settings (`app_shell.dart:47-57`). Tools, Operations, and Teams intentionally lead to group landings whose tiles contain the feature routes (`router.dart:154-170`, `router.dart:228-255`, `router.dart:311-350`). | `architecture/07-ui-design-system.md:38-40`; `app_shell.dart:47-57`; `router.dart:154-170`, `228-255`, `311-350`. | Preserve the five-item contract. Polish tile hierarchy and document the two-activation path in STEP-55. |
| FC-54.1-004 | Needs polish | Desktop sidebar collapse | The desktop sidebar animates its width to zero while the vertical divider remains in the row (`app_shell.dart:275-305`). This is structurally functional, but the collapsed state has no compact rail, persistent affordance, or explicit state in the sidebar itself; discoverability depends on the header toggle. The header label does expose “Buka/Tutup sidebar” (`global_app_header.dart:81-89`). | `app_shell.dart:275-305`; `global_app_header.dart:81-89`. | STEP-55.10 should specify the collapsed affordance, focus order, and keyboard behavior. Runtime visual and keyboard behavior is `Unverified` until exercised. |
| FC-54.1-005 | Needs restructure / D5 conflict | Form routing | D5 requires synchronized GoRouter form routes. Only four feature forms are registered in the route tree for Benchmark, Attendance, Daily Log, and Equipment Check (`router.dart:287-299`, `352-375`, `377-410`, `421-446`). Cut/Fill and Land Clearing use root `Navigator` + `MaterialPageRoute` instead of a GoRouter URL (`cut_fill_list_screen.dart:146-168`; `land_clearing_list_screen.dart:145-167`). Inventory also uses `MaterialPageRoute` for both create and edit (`inventory_dashboard_screen.dart:398-417`, `463-482`). Data Bucket has `/upload` and `/:id` routes (`router.dart:182-215`) but the list currently still pushes detail/upload pages with `MaterialPageRoute` (`data_bucket_list_page.dart:320-334`, `367-379`). Timeline has no create/edit form route or form action in its page; it only exposes date-range selection (`timeline_page.dart:64-80`, `238-275`). | Citations in the Finding column. | 54.11 must produce the complete D5 gap list for STEP-55. Migrate each applicable create/edit/detail surface to the route-backed sheet adapter; do not silently treat a `MaterialPageRoute` as URL synchronization. Timeline's missing mutation workflow needs an explicit product decision or a documented read-only boundary. |
| FC-54.1-006 | Needs restructure / D6 conflict | Report navigation | Feature list pages push `report-config` as a standalone route with `ReportType` in `state.extra` (for example `cut_fill_list_screen.dart:133-136`, `attendance_screen.dart:159-163`, `benchmark_list_screen.dart:291-295`). The route itself is outside the authenticated shell (`router.dart:483-508`) and loses the report type on refresh/deep link, falling back to the type picker (`router.dart:492-498`). This contradicts D6's contextual modal `FDialog` retaining list filters/state behind it. | `router.dart:483-508`; `cut_fill_list_screen.dart:133-136`; `attendance_screen.dart:159-163`; `benchmark_list_screen.dart:291-295`. | STEP-55.1 and 55.10 should replace the standalone navigation with a contextual report dialog contract and explicitly preserve filters/list state. Treat the current route as a D6 conflict, not as an acceptable modal implementation. |
| FC-54.1-007 | Needs polish | Token boundary | The shell, header, and group landing deliberately wrap content in Material primitives (`app_shell.dart:20-23`, `269-273`; `global_app_header.dart:8-9`; `group_landing_page.dart:1-4`). The source comments document the interoperability rationale, and ForUI controls/tokens are used around those primitives, so this is not a new anchored-zero Material-family violation. It is nevertheless a boundary that STEP-55 must keep narrow while moving forms into modal surfaces. | `app_shell.dart:20-23`, `269-273`; `global_app_header.dart:8-18`; `group_landing_page.dart:1-4`, `156-202`. | Preserve only justified interoperability primitives, keep the comments, and verify that new sheet/dialog work uses ForUI equivalents. No local code change in 54.1. |
| FC-54.1-008 | Needs polish | Localization | Shell labels, group titles/descriptions, navigation labels, breadcrumb output, search hint, and avatar text are hardcoded Indonesian/English strings (`app_shell.dart:47-57`, `84-194`; `router.dart:158-166`, `232-254`, `315-349`; `global_app_header.dart:81-89`, `196-218`, `269-289`, `312-343`, `415-425`). This is within the known incomplete localization boundary RISK-0004, but it creates inconsistent language behavior when the Settings locale changes. | `registries/risks.yml` RISK-0004; citations in the Finding column. | Record the shell/header migration in the master spec and keep the RISK-0004 boundary visible. STEP-55 should not add more hardcoded user-facing strings. |
| FC-54.1-009 | Unverified | Accessibility and visual states | Source code supplies several semantic labels and a keyboard path for feature tiles (`group_landing_page.dart:113-125`) and labels for shell actions (`global_app_header.dart:195-198`, `269-289`, `312-320`, `336-343`). Static inspection cannot prove WCAG contrast, 48dp hit targets, focus traversal, text scaling, reduced motion, or dark-mode appearance. The current capture artifacts cannot be used as visual evidence because the known screenshot outputs are placeholders. | `group_landing_page.dart:113-125`; `global_app_header.dart:195-198`, `269-289`, `312-320`, `336-343`; STEP-48 retraction in `2026-08-30-step-0048-runtime-design-review.md:14-23`. | Keep verdict `Unverified` until a valid Web/Android runtime artifact and screen-reader/focus evidence exist. STEP-55.11 owns the technical audit; do not infer a pass from analyzer or source semantics. |
| FC-54.1-010 | Unverified | Responsive boundary | The shell and header use the same 800dp comparison (`app_shell.dart:33-35`, `210-218`; `global_app_header.dart:17-47`), so the source has a single explicit boundary and no visible code band where both shell layouts are selected. Actual behavior at exactly 800dp, browser resizing, keyboard insets, and layout overflow is not proven without runtime execution. | `app_shell.dart:33-35`, `210-218`; `global_app_header.dart:17-47`. | STEP-55.11 should exercise widths immediately below, at, and above 800dp, plus large text scale and Android insets. Keep the static result as `Unverified`, not `Aligned`, until those runs produce evidence. |

## 5. D5 route-gap enumeration for all nine features

This table is the authoritative handoff to 54.11/STEP-55. A `Yes` means a route exists in `router.dart`; it does not mean the current caller uses it consistently.

| Feature | Current list surface | URL-backed form/detail route | Current gap / treatment |
|---|---|---|---|
| Cut / Fill | `/operations/cut-fill` | **No form route** | Create uses `Navigator.push(MaterialPageRoute)`; add `/operations/cut-fill/form` and route edit state. `cut_fill_list_screen.dart:146-168`; `router.dart:257-267`. |
| Land Clearing | `/operations/land-clearing` | **No form route** | Create uses `Navigator.push(MaterialPageRoute)`; add `/operations/land-clearing/form` and route edit state. `land_clearing_list_screen.dart:145-167`; `router.dart:268-277`. |
| Benchmark DB | `/operations/benchmark-db` | **Yes:** `/operations/benchmark-db/form` | Route is registered at `router.dart:279-299`; caller uses named route in `benchmark_list_screen.dart:390-448`. Verify the form's modal adapter and edit payload under D1/D2/D4/D5. |
| Crew Attendance | `/teams/attendance` | **Yes:** `/teams/attendance/form` | Route is registered at `router.dart:352-375`; create caller uses `context.push` at `attendance_screen.dart:172-195`. Verify it becomes a responsive sheet and preserves date/filter state. |
| Daily Logging | `/teams/daily-log` | **Yes:** `/teams/daily-log/form` | Route is registered at `router.dart:377-410`; `_openForm` uses the named route at `daily_log_list_screen.dart:82-129`. Verify edit/deep-link state and dirty interception. |
| Equipment Digital Checks | `/teams/equipment-check` | **Yes:** `/teams/equipment-check/form` | Route is registered at `router.dart:421-446`; `_openNewCheck` uses the named route at `equipment_history_screen.dart:102-110`. Detail/inspection view still needs the D7 decision in 54.7. |
| Inventory Management | `/teams/inventory` | **No form route** | Create and edit both use `Navigator.push(MaterialPageRoute)` at `inventory_dashboard_screen.dart:398-417`, `463-482`; add `/teams/inventory/form` and define the stock-adjustment dialog relationship. |
| Data Bucket | `/tools/data-bucket` | **Yes:** `/tools/data-bucket/upload` and `/tools/data-bucket/:id` | Routes exist at `router.dart:182-215`, but current list callers push `FileDetailPage` and `UploadFilePage` through `MaterialPageRoute` (`data_bucket_list_page.dart:320-334`, `367-379`). Route callers must be migrated so D5 is actually exercised; detail is the explicit D7 inspector candidate. |
| Work Timeline | `/teams/timeline` | **No form route** | Current page has date-range selection only (`timeline_page.dart:64-80`, `238-275`) and milestone cards have an optional tap callback but no caller supplies one (`milestone_card.dart:15-37`; `timeline_page.dart:323-350`). Decide whether timeline is read-only for this release or add a milestone form route. |

## 6. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| App shell, sidebar, global header | Web/desktop | Static wide-layout branch, expanded/collapsed code paths, navigation groups, theme/notification/profile controls | `app_shell.dart:210-218`, `269-325`; `global_app_header.dart:39-115`; `app_shell.dart:84-194` | Needs polish; visual/focus behavior `Unverified` (FC-54.1-004, 009, 010) |
| Group landings and feature reachability | Web/desktop | Static route hierarchy and sidebar item mapping | `router.dart:154-170`, `228-255`, `311-350`; `app_shell.dart:84-194` | Aligned for reachability; parent active-state needs polish (FC-54.1-002) |
| Bottom navigation and group landings | Android/mobile | Static narrow branch and five configured items | `app_shell.dart:383-423`; `app_shell.dart:47-57` | Aligned with Doc 07 structure; group/header cohesion needs restructure (FC-54.1-001, 003) |
| Responsive boundary | Web + Android | Static `<800` / `>=800` branches only | `app_shell.dart:33-35`, `210-218`; `global_app_header.dart:17-47` | Unverified at runtime (FC-54.1-010) |
| Feature form navigation | Web + Android | Route declarations and current caller patterns for all nine features | D5 table above; `router.dart:257-446` and cited feature files | Needs restructure against D5 (FC-54.1-005) |
| Contextual reporting entry | Web + Android | Static report button callers and standalone report route | `router.dart:483-508`; cited report callers | Needs restructure against D6 (FC-54.1-006) |
| Theme, localization, tokens, semantics | Web + Android | Static source audit only | `app.dart:40-90`; `app_shell.dart`; `global_app_header.dart`; `group_landing_page.dart`; RISK-0004 | Needs polish for localization/token boundary; visual/a11y runtime `Unverified` (FC-54.1-007–009) |

## 7. D1–D8 conflict and escalation register

- **D1/D2:** Current feature forms are full pushed pages, not the locked responsive sheets. This is recorded as FC-54.1-005 and is implementation scope for STEP-55, not a local critique fix.
- **D3/D4:** No current shell source proves a universal scrim/dirty-dismiss intercept. The absence is carried to the form-focused substeps and marked `Unverified` where runtime behavior would be required; no claim of compliance is made.
- **D5:** The complete nine-feature route-gap list is in §5. Existing route declarations do not prove caller URL synchronization.
- **D6:** Standalone `report-config` navigation with `state.extra` conflicts with the contextual modal decision (FC-54.1-006).
- **D7:** Shell does not decide feature detail treatment. Data Bucket and Equipment Check remain explicit downstream D7 decisions.
- **D8:** The 1:1 critique/implementation substep structure is preserved; this substep does not absorb feature work.

No user escalation was required: the conflicts are already within the locked STEP-54/55 scope and are recorded for 54.11/STEP-55. The static/runtime classification problem did not recur beyond the known screenshot-evidence boundary; this file consistently uses `Unverified` for claims not proven by source.

## 8. Verification record

| Check | Result |
|---|---|
| Rubric has dimensions, concrete checks, IDs, verdicts, and table shape | Pass — §§2 and 2.7 are cold-runnable for 54.2–54.10 |
| Shell critique covers Web and Android | Pass — §§3, 4, and 6 |
| D5 enumeration names all nine features | Pass — §5 lists all nine explicitly |
| Every finding has an ID, verdict, and citation or honest Unverified blocker | Pass — FC-54.1-001 through FC-54.1-010 |
| Application code changed | Pass — no app-repo diff; app branch remains clean |
| Runtime/screenshot evidence | Unverified — not run; placeholder artifacts are excluded as evidence |
| Findings file | Written at `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` |

**Verdict:** The reusable rubric is complete. The shell/navigation foundation is structurally usable and has an aligned five-item mobile hierarchy, but mobile global-control continuity, group active-state feedback, D5 form routing, and D6 report modality are concrete STEP-55 work. Runtime visual/accessibility/responsive claims remain `Unverified`.

**Next action:** Run substep 54.2 in a fresh chat.
