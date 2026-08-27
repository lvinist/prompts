# mine-flow — STEP-46.2 PROMPT
# Pass 1b: Screenshot Visual Review — All 24 Screens

**STEP:** 46.2 of STEP-46
**Model:** Pro-tier with vision (Gemini Pro High or equivalent)
**Independent of 46.1** — can run before, after, or concurrently with 46.1
**Reads from disk:** `Code/mine-flow-docs/architecture/07-ui-design-system.md`, `Code/mine-flow-docs/overview.md`
**Writes:** `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.2-FINDINGS.md` + screenshot files

---

## Context

You are running Pass 1b of the STEP-46 UI/UX audit. This is a **visual / rendered** pass. You will start the app in a browser, navigate to every screen, capture a screenshot of each, and review each screenshot with an open-ended "what looks wrong here" framing — **not a fixed checklist**. Your goal is to surface things that are only visible at render time: overflow at actual pixel densities, token drift visible as a color that looks subtly wrong, navigation that leads nowhere, labels that don't match adjacent data.

Read before starting:
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the design spec (Zinc palette, Geist font, compact spacing, sidebar/tab nav patterns).
- `Code/mine-flow-docs/overview.md` — what this app does and who uses it.
- `.throughstone/local-user.md` at workspace root — communication baseline.

---

## Step 1: Start the app

From `Code/mine-flow-app/`:

```powershell
flutter run -d chrome --web-port 3001
```

Wait for the app to launch in Chrome. If `flutter run` fails because Chrome is already in use, try `--web-port 3002`.

Log in with a test account (use the staging seed credentials or a local Supabase dev account). If no real credentials are available, note which screens you cannot reach due to auth and capture the login screen at minimum. The goal is to reach every screen — if some require specific data (e.g., FileDetailPage needs an existing file record), use the earliest available state that shows non-empty content.

---

## Step 2: For each screen, navigate + capture

Navigate to each screen in the order below. For every screen:

1. Navigate to the screen (use the sidebar/tab nav or the browser address bar with the route).
2. **Capture a screenshot** of the full browser window. Save it to `prompts/003-release-readiness-integration-scale/step-0046/screenshots/S<NN>-<screen-name>.png`.
3. If the screen has a distinct **empty state** (no data), also capture `S<NN>-<screen-name>-empty.png`.
4. If there is a **form** pushed from the list screen, capture the form too as `S<NN>-<screen-name>-form.png`.
5. Toggle **dark mode** (via Settings or the theme toggle in the AppBar) and capture `S<NN>-<screen-name>-dark.png` for any screen where dark mode looks noticeably different.

| Screen | Route to navigate to | Notes |
|--------|----------------------|-------|
| S01 LoginPage | `/login` | Capture before logging in |
| S02 DashboardPage | `/` | Dashboard stats |
| S03 GroupLandingPage | `/operations` (and `/teams`, `/tools`) | Capture all three group variants |
| S04 SettingsPage | `/settings` | Full settings list |
| S05 AttendanceScreen | `/teams/attendance` | |
| S06 AttendanceFormPage | `/teams/attendance/form` | Push from S05 via the add-attendance button |
| S07 DailyLogListScreen | `/teams/daily-log` | |
| S08 DailyLogFormScreen | Push from S07 | |
| S09 CutFillListScreen | `/operations/cut-fill` | |
| S10 CutFillFormScreen | Push from S09 | |
| S11 LandClearingListScreen | `/operations/land-clearing` | |
| S12 LandClearingEntryScreen | Push from S11 | |
| S13 InventoryDashboardScreen | `/teams/inventory` | |
| S14 InventoryItemEntryScreen | Push from S13 | |
| S15 EquipmentHistoryScreen | `/teams/equipment-check` | |
| S16 EquipmentCheckFormScreen | Push from S15 via the FAB | |
| S17 BenchmarkListScreen | `/operations/benchmark-db` | |
| S18 BenchmarkFormScreen | Push from S17 | |
| S19 TimelinePage | `/teams/timeline` | |
| S20 DataBucketListPage | `/tools/data-bucket` | |
| S21 UploadFilePage | Push from S20 via upload button | |
| S22 FileDetailPage | Push from S20 by tapping a file | Requires an existing file record |
| S23 ReportConfigPage | `/reports/config` — Note: this route requires a ReportType passed via extra. Try pushing it from a Laporan button on one of the feature screens. | |
| S24 NotificationListPage | `/notifications` — Note: this is a standalone route pushed on top of the shell. Navigate directly via address bar or tap the notification icon. | |

---

## Step 3: Review each screenshot

For each screenshot, write a visual finding note using the following framing:

> **Imagine you are a [supervisor / foreman / crew member] using mine-flow for the first time.**
> What on this screen looks off, confusing, inconsistent with the other screens, or broken?
> Compare against the design spec (DESIGN.md §1–5). Do not limit yourself to a checklist.

Specifically look for (but do not limit to):
- **Layout at this browser width:** Elements clipping, overflowing, not filling available space, or misaligning. The web layout should use the collapsible left sidebar (DESIGN.md §4). Is the sidebar present and correct?
- **Dark mode vs light mode:** Does the screen look correct in both? Any element that stays light-colored in dark mode (un-themed hardcoded color)?
- **Typography:** Is Geist being used? Does the heading hierarchy match the other screens? Are numbers in tables using a monospace/tabular font?
- **Color token correctness:** Does anything look like the wrong shade — a button that's slightly off the Zinc palette, a badge that uses a legacy Forest/Stone color?
- **Navigation:** Every button, FAB, and link — does it lead somewhere? Does the back/breadcrumb navigation take you to the right parent? Is the current screen highlighted in the sidebar/tab bar?
- **States:** Does the screen show a sensible state? If data is missing, is there a proper empty state with a helpful message, or just a blank white area?
- **Terminology consistency:** Does the label on this screen match the label for the same concept on other screens? (e.g., "Zona" vs "Area", "Simpan" vs "Submit", "Foreman" vs "Mandor")
- **Information that doesn't match its stated source:** A field labelled "Nama Kru" showing what looks like an ID string; a date field showing today's date when it should show the record's date.
- **Role visibility:** If you are a crew member, are there controls visible that you shouldn't be able to use?

---

## Output format

Create `prompts/003-release-readiness-integration-scale/step-0046/screenshots/` folder for screenshots.

Write findings to `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.2-FINDINGS.md`:

```markdown
# STEP-46.2 — Screenshot Visual Review Findings

Generated: <date>
Screens reviewed: 24
Screenshots saved to: prompts/003-release-readiness-integration-scale/step-0046/screenshots/
Total visual candidates: <N>

## Findings

### V-001 | P2 | S09 CutFillListScreen
**Screenshot:** `screenshots/S09-cut-fill-list.png`
**Category:** Layout — table columns clip on 1280px web width
**Observation:** The rightmost column ("Aksi") is clipped behind the scrollbar at the default 1280px width. The layout does not use Expanded/Flexible to distribute column widths proportionally.
**Severity:** P2

---

### V-002 | P1 | S03 GroupLandingPage (/teams variant)
...
```

Rules:
- Prefix findings with `V-` (to distinguish from 46.1's `F-` code findings).
- Every finding must include: severity tier, screen ID, screenshot filename, category, and a plain-English observation of what you saw.
- If a screen looks correct and has no findings, write "S0N: No visual findings."
- If you could not navigate to a screen (e.g., auth blocked, missing extra), write "S0N: Could not reach — [reason]. Recommend 46.3 flag."

---

## After writing the findings file

1. Verify all screenshot files are saved in `prompts/003-release-readiness-integration-scale/step-0046/screenshots/`.
2. Commit findings file + screenshots to the `step-0046-ui-ux-audit` branch in `prompts/`.
3. Update `prompts/STEP-index.md` substep 46.2 to `Done`.
4. Tell the user: "46.2 complete — N visual findings across M screens. Ready for 46.3 once 46.1 is also done."
