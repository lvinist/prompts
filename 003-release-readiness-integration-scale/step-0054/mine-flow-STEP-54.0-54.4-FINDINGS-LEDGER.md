# mine-flow — STEP-54.0–54.4 Findings Ledger Slice

**Built:** 2026-09-11
**Scope:** STEP-54.0 pre-flight plus every `FC-54.*` finding in STEP-54.1–54.4
**Inspected app branch/head:** `step-0054-feature-cohesion-critique` at `fe12531931eed861518b20f7323c6cf6bd0ccb8b`
**Purpose:** Verified input slice for STEP-54.11 consolidation; this is not the final master spec or STEP close.

## 1. Slice accounting

| Substep | Source | FC IDs | Ledger result |
|---|---|---:|---|
| 54.0 | `mine-flow-STEP-54.0-FINDINGS.md` | 0 | Pre-flight record accounted for separately below; it intentionally defines no critique IDs. |
| 54.1 | `mine-flow-STEP-54.1-FINDINGS.md` | 10 | `FC-54.1-001`–`FC-54.1-010`, all present and unique. |
| 54.2 | `mine-flow-STEP-54.2-FINDINGS.md` | 7 | `FC-54.2-001`–`FC-54.2-007`, all present and unique. |
| 54.3 | `mine-flow-STEP-54.3-FINDINGS.md` | 7 | `FC-54.3-001`–`FC-54.3-007`, all present and unique. |
| 54.4 | `mine-flow-STEP-54.4-FINDINGS.md` | 9 | `FC-54.4-001`–`FC-54.4-009`, all present and unique. |
| **Total** |  | **33** | **33/33 findings accounted for; no duplicate or missing sequence number.** |

### 54.0 pre-flight account

STEP-54.0 contains no `FC-54.*` findings because it is the merge/branch gate rather than a feature critique. Its ledger contribution is the verified baseline: app `master` was fast-forwarded to `fe12531`, docs `main` to `891ce66`, the STEP-53 evidence was archived by docs commit `bc77632`, the app regression run recorded analyze 0, format 0 changed, and 550 passed/5 skipped, and both STEP-54 branches were cut. The app branch inspected for this slice still resolves to the recorded app head `fe12531` and is clean.

## 2. Consolidated ledger

Verdicts below are normalized to the exact 54.1 vocabulary. D1–D8 labels remain in the area or adjudication rather than being appended to the verdict.

| ID | Verdict | Area | One-line finding | Evidence status | Candidate STEP-55 account |
|---|---|---|---|---|---|
| FC-54.1-001 | Needs restructure | Mobile shell/header | The mobile shell renders the global header only on `/`, leaving group landings without the global controls available on the dashboard. | Re-resolved: `app_shell.dart:383-423`; `group_landing_page.dart:23-79`. | 55.10 shell/header implementation. |
| FC-54.1-002 | Needs polish | Desktop sidebar state | Exact/prefix route matching does not provide a selected parent state on `/tools`, `/operations`, or `/teams`. | Source citation retained from finding; no restructure re-check required. | 55.10 parent/group active-state acceptance criterion. |
| FC-54.1-003 | Aligned | Mobile primary navigation | The bottom bar exposes exactly the five Doc 07 destinations and delegates feature reachability to group landings. | Source citation retained from finding. | Preserve and regression-test in 55.10/55.11. |
| FC-54.1-004 | Needs polish | Desktop sidebar collapse | The sidebar can animate to zero width, but the collapsed state depends on the header toggle and lacks a persistent rail affordance. | Source citation retained; runtime keyboard/visual behavior remains unverified. | 55.10 interaction polish; 55.11 runtime keyboard/focus check. |
| FC-54.1-005 | Needs restructure | D5 form routing | Several features either lack form routes or bypass existing GoRouter routes with `MaterialPageRoute`, so URL-backed form/detail reconstruction is incomplete. | Re-resolved from the finding body and §5 route table; the original evidence cell says only “Citations in the Finding column.” | 55.0 route adapter plus the applicable feature substeps 55.2–55.9. |
| FC-54.1-006 | Needs restructure | D6 report navigation | Report actions push a standalone route with `ReportType` in `state.extra`, and refresh can fall back to the type picker instead of preserving feature context. | Re-resolved: `router.dart:483-508`; representative callers still resolve. | 55.1 shared report dialog plus feature integrations. |
| FC-54.1-007 | Needs polish | Token boundary | Shell surfaces intentionally retain a narrow documented Material interoperability boundary that new sheet/dialog work must not expand. | Source citation retained from finding. | 55.0/55.10 constraint; verify in 55.11 token sweep. |
| FC-54.1-008 | Needs polish | Localization | Shell, navigation, group, and header strings remain hardcoded and therefore do not follow locale changes consistently. | Source citation retained from finding; already within RISK-0004. | 55.10; reconcile with RISK-0004 rather than opening a duplicate risk. |
| FC-54.1-009 | Unverified | Accessibility/visual states | Static semantics do not prove contrast, target size, focus order, text scaling, reduced motion, or dark-mode quality. | Blocker retained: no valid runtime artifact in 54.1. | 55.11 runtime/a11y evidence debt. |
| FC-54.1-010 | Unverified | Responsive boundary | Source uses a consistent 800dp branch, but behavior at and around the breakpoint is not proven at runtime. | Blocker retained: no runtime width sweep in 54.1. | 55.11 test immediately below/at/above 800dp. |
| FC-54.2-001 | Needs restructure | Cut/fill report / D6 | The cut/fill report action opens the standalone report route and does not carry the active date/zone filters. | Re-resolved: `cut_fill_list_screen.dart:133-136`; `report_config_page.dart:40-48`. | 55.1 and 55.2. |
| FC-54.2-002 | Needs restructure | Cut/fill form / D1–D2 | Create and edit open a full `MaterialPageRoute` form rather than the responsive sheet contract. | Re-resolved: `cut_fill_list_screen.dart:146-168,407-417`. | 55.0 and 55.2. |
| FC-54.2-003 | Needs restructure | Cut/fill route / D5 | The router has `/operations/cut-fill` but no create/edit form child route. | Re-resolved: `router.dart:257-267`. | 55.0 route contract and 55.2 implementation. |
| FC-54.2-004 | Needs restructure | Cut/fill dirty guard / D4 | The BLoC tracks unsaved changes, but visible dismiss controls pop directly and the form has no `PopScope`/`WillPopScope` guard. | Re-resolved: `cut_fill_bloc.dart:94-103,211-220`; `cut_fill_form_screen.dart:180-185,253-259`; whole-file guard scan returned none. | 55.0 universal guard and 55.2 wiring. |
| FC-54.2-005 | Needs polish | Cut/fill tokens | The cut/fill list/form retain Material FAB, date picker, and text-field primitives outside the target ForUI vocabulary. | Source citation retained from finding. | 55.2 token cleanup. |
| FC-54.2-006 | Aligned | Cut/fill D7 | Scalar cut/fill records can continue opening edit directly; a separate read-only inspector is not justified. | Source citation retained from finding. | Preserve as the D7 “no inspector” decision in 55.2. |
| FC-54.2-007 | Unverified | Cut/fill accessibility | Static labels do not prove touch targets, contrast, or focus behavior. | Blocker retained: no runtime artifact in 54.2. | 55.11 runtime/a11y evidence debt. |
| FC-54.3-001 | Needs restructure | Land-clearing form / D1–D5 | Create/edit use `MaterialPageRoute` and the form has no URL-backed sheet or dirty-dismiss guard. | Re-resolved: `land_clearing_list_screen.dart:145-168,404-427`; `land_clearing_entry_screen.dart:247-268`; whole-file guard scan returned none. | 55.0 and 55.3. |
| FC-54.3-002 | Needs polish | Plan/Actual tab state | `DefaultTabController`/`TabBar` state is local, so form reconstruction does not retain the selected Plan/Actual tab. | Source citation retained. Treat as form-state preservation, not as a substitute for the missing form route in FC-54.3-001. | 55.3; choose a stable route/query or explicit restoration contract. |
| FC-54.3-003 | Needs polish | Shared method combobox | The selection-only CF-043 contract is preserved, but the shared combobox always renders an inline list rather than adapting to mobile. | Static structure resolves at `creatable_combobox.dart:319-362`; keyboard-occlusion impact remains unverified. | 55.3 platform adaptation; verify occlusion in 55.11 before claiming a runtime defect. |
| FC-54.3-004 | Needs restructure | Land-clearing report / D6 | The report action pushes the standalone report route and does not preserve list filters. | Re-resolved: `land_clearing_list_screen.dart:128-135`. | 55.1 and 55.3. |
| FC-54.3-005 | Needs polish | Land-clearing tokens | Form/list surfaces retain Material tabs, date pickers, FABs, and text fields outside the target component vocabulary. | Source citation retained from finding. | 55.3 token cleanup. |
| FC-54.3-006 | Needs restructure | Land-clearing D7 | A record tap opens the mixed Plan/Actual edit form directly, so the critique selects a read-only inspector before edit. | Re-resolved: `land_clearing_list_screen.dart:400-427`. The original role-specific rationale (“field workers only…”) is not established by this citation and must not be carried forward as fact. | 55.3 inspector-sheet implementation, justified by inspection/edit separation and accidental-edit risk. |
| FC-54.3-007 | Unverified | Land-clearing accessibility | Tabs, summary cards, contrast, targets, and dark mode were not exercised at runtime. | Blocker retained: no runtime artifact in 54.3. | 55.11 runtime/a11y evidence debt. |
| FC-54.4-001 | Needs restructure | Benchmark spatial validation | Failed coordinate projection can reach submit and is persisted as latitude/longitude `0.0, 0.0`, creating a data-integrity defect. | Re-resolved: `benchmark_form_screen.dart:501-518`; `benchmark_bloc.dart:540-546`. | 55.4 priority-zero validation fix and targeted tests. |
| FC-54.4-002 | Needs restructure | Benchmark form / D1–D2 | The benchmark form is a full routed `FScaffold`, not the required Web right sheet/mobile bottom sheet. | Re-resolved: `benchmark_form_screen.dart:165-195`. **Qualification:** the original claim that this necessarily obscures the shell/sidebar is not supported; the route is nested under the shell. | 55.0 and 55.4; carry only the sheet-contract mismatch, not the obscured-shell claim. |
| FC-54.4-003 | Needs polish | Benchmark tokens | Benchmark surfaces retain Material FAB, refresh, and dropdown primitives. | Source citation retained from finding. | 55.4 token cleanup. |
| FC-54.4-004 | Needs polish | Benchmark dirty guard / D4 | Back/cancel paths dismiss without consulting dirty state, and the form has no universal pop guard. | Source citation retained: `benchmark_form_screen.dart:165-188`; whole-file guard scan returned none. | 55.0 guard and 55.4 wiring. |
| FC-54.4-005 | Needs polish | Benchmark touch target | The delete control is a 20dp icon in a bare gesture detector without a demonstrated 48dp target. | Source citation rechecked at `benchmark_list_screen.dart:504-517`. | 55.4; verify target geometry in 55.11. |
| FC-54.4-006 | Needs restructure | Benchmark report / D6 | Benchmark reporting pushes the standalone route instead of opening a contextual dialog. | Re-resolved: `benchmark_list_screen.dart:291-294`. | 55.1 and 55.4. |
| FC-54.4-007 | Needs restructure | Benchmark edit route / D5 | The form route exists, but edit identity is supplied only through `state.extra`, so refresh/deep-link reconstruction cannot recover the selected benchmark. | Re-resolved: `benchmark_list_screen.dart:390-393`; `router.dart:287-297`. | 55.0 route semantics and 55.4 ID-based loading. |
| FC-54.4-008 | Needs polish | Benchmark CRS UX | CRS labels omit datum context and projection failure copy does not explain how to recover. | Source citation retained from finding. | 55.4 copy/selector/error-state polish. |
| FC-54.4-009 | Unverified | Benchmark runtime states | Empty/error visuals, keyboard insets, target geometry, and dark-mode contrast were not exercised at runtime. | Blocker retained: no runtime artifact in 54.4. | 55.11 runtime/a11y evidence debt. |

## 3. `Needs restructure` citation re-resolution

All 14 restructure findings were checked against app branch head `fe12531`. None was dropped. Ten resolve without a claim change; four require the qualification recorded below.

| ID | Result | Re-resolution / adjudication |
|---|---|---|
| FC-54.1-001 | Pass | Mobile header condition and header-less group landing still resolve at the cited ranges. |
| FC-54.1-005 | Pass — evidence-cell qualification | The route gaps resolve, but the original evidence cell is not self-contained; use the citations in the finding text and §5 route table when writing the master spec. |
| FC-54.1-006 | Pass | Standalone report route, `state.extra`, and fallback picker remain present. |
| FC-54.2-001 | Pass | Cut/fill report caller and report-type selection remain present; active list filters are not passed. |
| FC-54.2-002 | Pass | Both create and edit still use `MaterialPageRoute`. |
| FC-54.2-003 | Pass | The cut/fill route still has no form child. |
| FC-54.2-004 | Pass | Dirty state is tracked, direct pops remain, and no pop guard exists in the form file. |
| FC-54.3-001 | Pass | Create/edit remain pushed pages; the route has no form child and the form has no pop guard. |
| FC-54.3-004 | Pass | The standalone report caller remains at the cited lines. |
| FC-54.3-006 | Pass — rationale qualification | Direct-to-edit behavior resolves. Do not carry the uncited assertion about planner/field-worker role exclusivity into the spec. |
| FC-54.4-001 | Pass | Validation omits projection success and the BLoC still falls back to `0.0, 0.0`. |
| FC-54.4-002 | Pass — claim qualification | Full `FScaffold` versus responsive sheet resolves. Strike the unsupported “obscures the shell/sidebar” clause. |
| FC-54.4-006 | Pass | Benchmark report still pushes the standalone route. |
| FC-54.4-007 | Pass | Edit still passes the benchmark through `extra`; the form route consumes `state.extra`. |

## 4. Cross-finding reconciliation for this slice

1. **FC-54.1-005 is the umbrella D5 finding.** FC-54.2-003, FC-54.3-001, and FC-54.4-007 are feature-specific implementations of that gap, not duplicates to discard. The spec should trace shared route-adapter work to FC-54.1-005 and each feature route to its local ID.
2. **FC-54.1-006 is the umbrella D6 finding.** FC-54.2-001, FC-54.3-004, and FC-54.4-006 retain local traceability for each feature integration.
3. **Dirty-state evidence differs by feature.** Cut/fill already tracks `hasUnsavedChanges` but does not intercept dismissal; land clearing and benchmark still need their feature wiring assessed while adopting the universal 55.0 guard. Do not infer one shared state implementation from the common D4 outcome.
4. **Benchmark report presence is verified.** The 54.4 prompt allowed a deliberate absence, but branch-head source has a Benchmark report action and `ReportType.benchmark`; the master report inventory must list it as present and needing D6 migration.
5. **D7 decisions in this slice are complete:** Cut/fill — no separate inspector; Land clearing — inspector sheet; Benchmark — inspector sheet. STEP-54.0/54.1 do not own feature-level D7 verdicts.
6. **Unverified remains unverified.** Static source confirms structure, not contrast, target geometry, keyboard occlusion, breakpoint visuals, screen-reader output, or dark-mode quality. These items stay assigned to 55.11 unless later STEP-54 runtime evidence explicitly closes them.

## 5. Verification record

| Check | Result |
|---|---|
| Parsed source findings | Pass — 33 rows: 54.1 = 10, 54.2 = 7, 54.3 = 7, 54.4 = 9. |
| ID uniqueness and continuity | Pass — no duplicates; every sequence starts at 001 and has no gap. |
| Verdict vocabulary | Pass in this ledger — normalized to `Aligned`, `Needs polish`, `Needs restructure`, or `Unverified`. |
| Restructure citation re-resolution | Pass with recorded qualifications — 14/14 checked, 0 struck. |
| 54.0 accounted for | Pass — no FC IDs expected; pre-flight baseline recorded separately. |
| D7 slice | Pass — cut/fill no inspector; land clearing inspector; benchmark inspector. |
| Application code modified | Pass — none. App repo remained clean on `step-0054-feature-cohesion-critique`. |
| Final STEP-54 accounting | Not claimed — this artifact covers only 54.0–54.4; STEP-54.5–54.10a remain outside this slice. |

## 6. Limitations

- This is a consolidation work product for the requested slice, not the final 54.11 master polish specification, Doc 07 v0.5.0 bump, risk reconciliation, user review gate, or STEP close.
- Source was checked at app head `fe12531`; later app changes require citation re-resolution again.
- Runtime evidence was not added. All original visual/accessibility/runtime blockers remain explicit.
