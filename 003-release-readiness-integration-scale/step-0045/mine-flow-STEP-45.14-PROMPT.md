# mine-flow — STEP-45.14: Runtime Impeccable design review (responsive / a11y / localized)

**Recommended model:** Gemini 3.1 Pro (visual/a11y/localization judgment + evidence curation; resolves NR-002/003).

> **How to run:** *"run substep 45.14"*. Self-contained; runnable cold.

## Context

Captures the runtime Impeccable design-review evidence the STEP-46 static+screenshot audit could not
settle, and resolves the two design-only Needs-Runtime items: **NR-002** (login light-mode on device)
and **NR-003** (sidebar active-state on group routes on web). Depends on 45.3. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (canonical UI spec, v0.2.0) and root
  `DESIGN.md` (generated Impeccable bridge — read-only reference, do not edit).
- STEP-46 findings — **NR-002**, **NR-003**, and the systemic P3 items (CF-085 motion durations,
  CF-086 spacing/radii, CF-087 residual Material, CF-088 Material vs Lucide icons) for what to
  visually confirm post-remediation.
- `Code/mine-flow-app/lib/app/presentation/pages/app_shell.dart` (sidebar active-state, line ~264).
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0011** (in-app privacy notice — pre-release gate).

## Scope

Produces `Code/mine-flow-docs/reports/2026-…-step-0045-runtime-design-review.md` + captured
screenshots. May file new findings; small design fixes with a decision are allowed but large
reworks are carried forward, not done here.

## Your task

1. **Responsive:** capture each key screen at mobile / tablet / desktop breakpoints; confirm the
   layouts match Doc 07 and no overflow/adaptive-layout regressions remain.
2. **Themes:** capture light and dark; **resolve NR-002** — confirm the login card follows the theme
   in light mode on a real device (the 46.2 dark screenshot was a capture artifact).
3. **Localization:** capture `id` and `en`; confirm locale switching works end-to-end (STEP-38.3
   wired locale from SettingsCubit) and no untranslated/mixed-language strings remain on key screens.
4. **NR-003:** on the web build, navigate to `/operations`, `/teams`, `/tools` and confirm whether a
   sidebar item highlights and does so correctly; record the outcome (fix if it's a clear bug, else
   carry forward).
5. **Accessibility (runtime):** spot-check semantics/focus order/contrast on key screens (screen
   reader where feasible); note any a11y gaps.
6. **RISK-0011:** confirm at runtime whether the first-login flow shows a privacy notice; record the
   status (still a pre-release gate or now addressed) — do not silently close it.
7. Write the report with embedded/linked screenshots as evidence for every claim. Items that can't be
   run (no device/staging) are **Unverified** with the reason.

## Verification
- Report exists with breakpoint / theme / locale screenshots and per-item outcomes.
- NR-002 and NR-003 each resolved-or-carried-forward with evidence.
- Any code fix has a test; `flutter analyze` 0 / format clean.

## Keeping the docs true (always)
- Design drift vs `architecture/07-ui-design-system.md` → note for 45.15 (Version Log or ADR). New
  findings feed the 45.15 reconciliation.

## Definition of done
- [ ] Runtime design-review report captured across breakpoints, themes, and `id`/`en` locales.
- [ ] NR-002 (login light-mode) and NR-003 (sidebar active-state) resolved or carried forward with evidence.
- [ ] RISK-0011 privacy-notice runtime status recorded.
- [ ] Any code fix tested; analyze 0 / format clean.

## Next
Run substep 45.15 (Findings reconciliation, docs, risks & STEP close) in a fresh chat.
