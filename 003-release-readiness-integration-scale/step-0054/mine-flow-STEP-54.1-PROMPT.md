# mine-flow — STEP-54.1: Critique Rubric, Token Vocabulary & Shell/Navigation Foundation Critique

> **How to run:** Tell your agent *"run substep 54.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Hermes/Claude Opus 4.8.** The rubric and findings-ID scheme this substep produces are inherited unchanged by all ten critique substeps (54.2–54.10) and consolidated by 54.11 — a wrong or ambiguous rubric silently corrupts every downstream critique, which is the definition of a silent, compounding failure.

## Context

STEP-54 critiques all 9 features and the app shell as cohesive lifecycles (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android, then consolidates into the master polish spec STEP-55 implements. This substep defines **how** every critique is performed and scored (the rubric), then performs the first critique itself: the app shell and navigation foundation that every feature renders inside.

Preconditions: 54.0 completed (trunks merged, `step-0054-feature-cohesion-critique` branch exists in app + docs, index row `In progress`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — the STEP PLAN (evidence standard, D1–D8, ground rules)
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — locked decisions D1–D8 and the substep roadmap
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — v0.4.0 UI canon (ForUI Zinc, compact density, Geist, Lucide, sidebar Web + 5-tab bar Android, WCAG 2.1 AA, ID locale, 150–200ms motion)
- `Code/mine-flow-docs/reports/2026-08-30-step-0048-runtime-design-review.md` — the findings-table format precedent (and its placeholder-PNG retraction amendment: the honesty lesson)
- `Code/mine-flow-app/README.md` and `Code/mine-flow-app/ARCHITECTURE.md`
- `Code/mine-flow-docs/registries/risks.yml` — rows RISK-0004 (l10n migration), RISK-0015/0016/0023 (screenshot placeholders)
- root `.throughstone/local-user.md`

## Scope

**Owns:** (1) the reusable critique rubric + findings-ID scheme + verdict vocabulary, published inside this substep's findings file; (2) the shell/navigation critique itself.

**Does NOT touch:** any application code (read-only — `lib/**` is frozen for all of STEP-54), feature-screen critiques (54.2–54.10), the master spec (54.11).

**Shell critique surfaces** (paths as of 2026-09-10; re-locate on the branch head):
- `lib/app/presentation/pages/app_shell.dart` — `FSidebar` (desktop), `FBottomNavigationBar` (mobile), global header
- `lib/app/presentation/pages/group_landing_page.dart` — Operations/Teams/Tools group landings
- `lib/app/router.dart` — route tree, deep-link structure (D5), `AppRoutes`
- Responsive breakpoint logic (the ~800dp switch) — locate in `app_shell.dart` or `lib/core/`
- Theme toggles (light/dark/system) in settings + shell wiring

## Your task

### Part A — The rubric (the deliverable later substeps inherit)

Define, in a dedicated **Rubric** section of your findings file:

1. **Critique dimensions** (each with 2–4 concrete checks a cold-running agent can apply):
   - **Lifecycle cohesion** — List → Form → Detail → Report connectedness; can a user complete the loop without dead ends; does state survive round-trips.
   - **Platform conformance** — D1 (right side-sheet Web), D2 (bottom sheet Mobile), D5 (URL sync), Doc 07 navigation canon (sidebar / 5-tab bar).
   - **Interaction states** — loading, empty, error, success, dirty; each state present and designed, not accidental.
   - **Accessibility** — WCAG 2.1 AA contrast (ForUI Zinc baseline), touch targets ≥ 48dp on mobile, semantics/labels, text scaling.
   - **Token conformance** — ForUI widgets only (no residual Material — cf. STEP-51's anchored-zero sweeps), Zinc palette, compact spacing, Lucide icons, Geist.
   - **D1–D8 conflict scan** — does the current implementation contradict a locked decision (record as a conflict finding, never fix locally).
2. **Findings-ID scheme:** `FC-54.<M>-<NNN>` (e.g. `FC-54.3-002`), sequential per substep, never reused.
3. **Verdict vocabulary:** `Aligned` / `Needs polish` (token-or-copy level) / `Needs restructure` (layout/flow level) / `Unverified` (runtime claim without evidence) — applied per finding, plus an overall per-surface summary.
4. **Coverage table shape** (from the STEP-48 review): Surface / Platform / States exercised / Evidence / Result.

### Part B — Shell & navigation critique

Apply the rubric to the shell surfaces above, both platforms. Specific questions to answer with file:line evidence:

- Does the responsive breakpoint switch cleanly between sidebar and bottom bar? Any width band where neither/both render?
- Sidebar: collapsible per Doc 07? Active-state on group routes (cf. STEP-48 DR-0002)? Are all 9 features reachable in ≤ 2 taps/clicks from the shell on *each* platform?
- Bottom bar: exactly 5 items per Doc 07 — what are they, and where do the remaining features live (group landing?)? Is that hierarchy defensible on mobile?
- Route tree vs. D5: which features already have `/form` sub-routes (router shows `cut-fill`? check `benchmark-db/form`, `attendance/form`, `daily-log/form`, `equipment-check/form`) and which forms are currently pushed without URL change? Enumerate the D5 gap list — STEP-55 needs it.
- Header, theme toggle, locale switcher: consistent placement, token conformance, dark-mode correctness of every shell surface.

### Evidence standard (from the PLAN — mandatory)

- **Static floor:** every finding cites `file:line` on the branch head you inspect. No citation → hypothesis, not finding.
- **Runtime where the harness works:** you may run the app (web recipe: `flutter run -d chrome` or the drive harness) to check a specific claim; any screenshot must be reported with **byte size and pixel dimensions** — the 68-byte/1×1 placeholder class (RISK-0015/0016/0023) must be called out as harness-defect, not evidence.
- **Unverified:** anything you cannot evidence is marked `Unverified` with the blocker named. Do not fix the harness (STEP-55.11 territory).

## Verification

- The rubric section is complete enough that a cold agent can run 54.2–54.10 from it alone (dimensions, checks, ID scheme, verdicts, table shape).
- Every shell finding carries a verdict, an ID, and a file:line citation (or is marked Unverified with blocker).
- The D5 route-gap enumeration covers all 9 features explicitly.
- No code was modified: `git status` in the app repo shows a clean tree (aside from anything 54.0 flagged).

## Keeping the docs true  (always)

- This substep writes findings only — no architecture doc changes. If the critique finds Doc 07 itself is wrong or stale (e.g. the 5-tab claim doesn't match reality), record it as a finding for 54.11 to reconcile via the Doc 07 bump — do not edit Doc 07 in this substep.
- Escalate (and record the escalation) if: a finding conflicts with locked D1–D8 or an accepted ADR; runtime behavior contradicts Doc 07; you are tempted to record a runtime claim you cannot evidence; the same classification problem recurs twice.

## Definition of done

- [ ] Rubric (dimensions, checks, ID scheme, verdict vocabulary, table shape) published in the findings file.
- [ ] Shell critique complete: both platforms, all rubric dimensions, coverage table filled.
- [ ] D5 route-gap enumeration for all 9 features recorded.
- [ ] All findings have IDs, verdicts, and citations (or honest Unverified markers).
- [ ] `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` written; no application code touched.

## Next

Update the PLAN's substep table (54.1 → Done) and tell the user: *"run substep 54.2"* — in a **fresh chat**.
