# mine-flow — STEP-54.5 Findings: Teams Suite 1 — Crew Attendance Critique

**Date:** 2026-09-11
**Executor:** Gemini 3.1 Pro High
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique`
**Scope:** Read-only critique of Crew Attendance feature (roster list, status badges, check-in sheet, and report navigation) across Web and Android, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric.

## 1. Scope and evidence boundary

This is a static critique. The mandatory evidence floor is met with branch-head `file:line` citations. No runtime capture was performed; therefore visual, touch, screen-reader, contrast, and runtime URL behavior remain `Unverified` rather than inferred from source code. No application code or docs were modified.

The inspected source files were:
- `lib/features/attendance/presentation/pages/attendance_screen.dart`
- `lib/features/attendance/presentation/pages/attendance_form_page.dart`
- `lib/features/attendance/presentation/widgets/crew_roster_item.dart`
- `lib/features/attendance/presentation/widgets/status_toggle_chips.dart`
- `lib/features/attendance/presentation/widgets/attendance_summary_card.dart`
- `lib/features/attendance/presentation/bloc/attendance_bloc.dart`
- `lib/features/attendance/domain/entities/attendance_record.dart`
- `lib/app/router.dart`

## 2. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.5-001 | Needs polish | Lifecycle cohesion | Returning from the check-in form triggers a `LoadAttendanceEvent` which creates a fresh `AttendanceLoaded` state, unintentionally clearing the roster's active search and status filters. | `attendance_screen.dart:185-194`; `attendance_bloc.dart:57-63`. | Preserve the previous `searchQuery` and `statusFilter` from the current state when yielding the refreshed `AttendanceLoaded` state. |
| FC-54.5-002 | Needs polish | Status badges (Form) | While toggle chips use distinct Lucide icons (making them shape-distinguishable), the 'Hadir' (present) and 'Izin' (leave) statuses both share `theme.colors.primary` as their tint color, reducing scannability for color-reliant users. | `status_toggle_chips.dart:50, 74`. | Assign a distinct semantic token or color variant for the 'leave' status so it does not visually blend with 'present'. |
| FC-54.5-003 | Needs polish | Status badges (Summary) | The attendance summary metric tiles rely entirely on color and numeric count without icons, and 'Hadir' and 'Izin' both use `theme.colors.primary`, failing color-blind accessibility guidelines. | `attendance_summary_card.dart:97-147`. | Introduce icons to the summary tiles and differentiate the 'leave' color token. |
| FC-54.5-004 | Needs polish | Ergonomics (Mobile) | The status toggle chips declare only a `40dp` minimum height; the code therefore does not guarantee the rubric's 48dp mobile target, although the actual rendered hit region remains runtime-unverified. | `status_toggle_chips.dart:84-90` | Guarantee a minimum 48x48dp hit region and verify its rendered size on Android. |
| FC-54.5-005 | Aligned | Ergonomics (Mobile) | The primary check-in actions are directly exposed on each roster item in the form via inline toggle chips, enabling efficient single-tap check-in without navigating to a separate detail screen. | `attendance_form_page.dart:219-239`. | Maintain inline status toggles. |
| FC-54.5-006 | Needs restructure | Ergonomics (Mobile) | The check-in form lacks a bulk action (e.g., "Mark All Present"); foremen must individually tap every crew member, causing fatigue on large field rosters. | `attendance_form_page.dart:257-305`. | Implement a bulk-action affordance in the form sheet for marking the remaining un-statused roster members as present. |
| FC-54.5-007 | Needs restructure | Offline state honesty | The `AttendanceRecord` entity carries no local sync status, and the roster item consequently has no record-level state from which to distinguish synced, queued, or failed check-ins; users cannot assess whether a locally saved mark has reached the server. | `attendance_record.dart:5-32`; `crew_roster_item.dart:13-201` | Expose sync metadata through the presentation model and render pending/failed states in `CrewRosterItem`; escalate the missing trust signal to 54.11. |
| FC-54.5-008 | Needs restructure | D1/D2 Form migration | The attendance form is pushed as a full `FScaffold` page via `context.push` rather than using the D1/D2-mandated modal side/bottom sheet adapter. | `attendance_screen.dart:173-184`. | Migrate the form presentation to the universal modal sheet adapter. |
| FC-54.5-009 | Needs restructure | D4 Dirty intercept | The form's header dismisses directly with `context.pop()` and the page has no dirty-intercept wrapper, despite the BLoC exposing `hasUnsavedChanges`; an accidental back action can discard a batch before save. | `attendance_form_page.dart:81-110`; `attendance_state.dart:23-43` | Wrap every dismissal path in the standard dirty-check interceptor. |
| FC-54.5-010 | Needs restructure | D5 Route synchronization | The `/teams/attendance/form` route deep-link receives context entirely through an in-memory `extra` payload rather than URL path/query parameters; a direct link visit defaults to the current date and loses context. | `router.dart:364-372`. | Pass `date` and `siteId` via URL query parameters so deep links reconstruct the exact form state. |
| FC-54.5-011 | Needs restructure | D6 Contextual report | The report action navigates to a standalone `report-config` route instead of presenting a contextual `FDialog` over the roster list, breaking flow context. | `attendance_screen.dart:159-163`. | Replace the standalone push with an `FDialog` that retains the roster's active filters behind it. |
| FC-54.5-012 | Needs polish | Residual Material | The roster item uses `CircleAvatar`, while the screen retains a documented `Material` interoperability wrapper; the avatar is the actionable visual-system holdover and should not be conflated with a justified wrapper boundary. | `crew_roster_item.dart:48`; `attendance_screen.dart:137-143` | Replace `CircleAvatar` with a ForUI avatar or token-styled container; preserve only documented Material interoperability wrappers. |
| FC-54.5-013 | Unverified | Runtime accessibility / responsive behavior | Static source cannot prove rendered hit targets, keyboard/focus order, screen-reader announcements, contrast, text scaling, or list state under actual Web and Android navigation. | `attendance_screen.dart:137-199`; `attendance_form_page.dart:81-110` | Exercise both platforms during STEP-55.11 and retain the blocker until valid runtime evidence exists. |

## 3. D7 Verdict (Detail View)

**Verdict:** No per-member detail view is needed for the Phase 1 MVP.
The current roster list and in-line check-in sheet suffice for this field workflow. Historical editing or deep inspection of a single crew member's attendance across months is not a primary mobile field requirement; it can be handled by reporting.

## 4. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| Roster list & filters | Web + Android | Static inspection of page and bloc interactions | `attendance_screen.dart:137-199`; `attendance_bloc.dart:46-63` | Needs polish (lifecycle filter loss FC-54.5-001); runtime state restoration Unverified |
| Status badges | Web + Android | Static inspection of toggle chips and summary card. | `status_toggle_chips.dart`; `attendance_summary_card.dart` | Needs polish (Color reliance FC-54.5-002, 003). |
| Check-in form | Web + Android | Static layout, declared touch constraints, and bulk action absence | `attendance_form_page.dart:81-110, 219-239, 257-305`; `status_toggle_chips.dart:80-100` | Needs restructure (bulk action and dirty guard); rendered touch size Unverified |
| Offline honesty | Web + Android | Domain model inspection. | `attendance_record.dart`; `crew_roster_item.dart` | Needs restructure (Missing sync indicator FC-54.5-007). |
| Blueprint D1–D6 | Web + Android | Routing, modality, and deep-linking. | `router.dart`; `attendance_screen.dart`; `attendance_form_page.dart` | Needs restructure (Conflicts FC-54.5-008–011). |

## 5. Verification record

| Check | Result |
|---|---|
| Rubric dimensions applied (Android lens) | Pass — Roster/form ergonomics, touch targets, and offline honesty were specifically critiqued. |
| Badge color-independence evidenced | Pass — Checked both `StatusToggleChips` and `AttendanceSummaryCard`. |
| Offline-state honesty evidenced | Pass — Analyzed `AttendanceRecord` and `CrewRosterItem` for missing sync indicators. |
| D4/D5 status and D7 verdict recorded | Pass — Explicitly documented in findings and D7 verdict section. |
| Findings ledger verification | Pass — 13 sequential IDs; every finding has a verdict and branch-head citation. |
| Application code untouched | Pass — app repo clean on `step-0054-feature-cohesion-critique`. |

## 6. Limitations and Escalations

- **Visual / Interactive (Unverified):** No runtime harness was executed; rendered hit targets, contrast, animation, scroll/keyboard behavior, focus order, and screen-reader announcements remain unverified (FC-54.5-013).
- **Escalation:** The lack of a local sync status property on `AttendanceRecord` (FC-54.5-007) is escalated to 54.11 as a critical offline-honesty blocker, since an unsynced check-in that looks identical to a saved one destroys data trust in low-connectivity field environments.
