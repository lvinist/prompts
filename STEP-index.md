# mine-flow — STEP Index

The living roadmap. Every STEP, its status, and a one-line scope. **This is the first
place to look to understand where the project is.** Keep it current as STEPs are planned,
worked, and completed.

> Status values: **Planned** · **In progress** · **Done** (archived to `prompts/`) ·
> **Deferred** (consciously not needed now; keep a revisit trigger) ·
> **Abandoned** (reserved but won't be built — keep the row so the number is never reused).
> Flip a STEP to **In progress** when you start it, so the overlap warning can see it.
> STEP numbers are global and never reset (see `METHOD.md` §1, §8).
> **What to do next** is always derivable from this index — see the next-action resolver in
> `METHOD.md` §10.
>
> **Reserving a number (teams):** adding a STEP row *is* reserving its number, on `prompts/`'s
> shared trunk (not a `step-NNNN` branch). Pull `prompts/`, take `max + 1`, add the row, then
> **commit and push immediately** — before branching or working. If the push is rejected, pull,
> renumber, push again. Before every push, even a clean merge, scan for duplicates
> (`grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md | grep -oE 'STEP-[0-9]+' | sort | uniq -d`)
> — two appended rows merge with no
> conflict into a silent duplicate. See `runbooks/collaboration.md`.
> **Owner** = who's on it; **Repos** = the repos it expects to touch (a *projection* that may
> change — it powers the overlap warning, it doesn't reserve anything). Solo, leave them blank.

## Phase 1 — MVP

| STEP | Title | Owner | Status | Repos (projection) | Scope (one line) |
|------|-------|-------|--------|--------------------|------------------|
| STEP-1 | Architecture | | Done | `mine-flow-docs`, `prompts` | Architecture-first: design docs + ADRs, no code. Substeps = the sessions in `templates/architecture-sessions/`. Branch: `step-0001-architecture`. |
| STEP-2 | Scaffold repos & skeleton | | Planned | `mine-flow-app` | Create the Flutter repository, Clean Architecture structure, apply license, and setup `.env.example` baseline. |
| STEP-3 | Core Data Layer & Authentication | | Planned | `mine-flow-app` | Implement Supabase schema, RLS policies, auth, generate Dart models, and setup offline caching foundation. |
| STEP-4 | Tier 1 - Attendance & Daily Logging | | Planned | `mine-flow-app` | Build UI and offline sync logic for crew attendance and daily structured logs for field operations. |
| STEP-5 | Tier 1 - Equipment Digital Checks | | Planned | `mine-flow-app` | Implement SOP-based pre-work and post-work condition checks for GNSS, Total Station, and Drone/UAV with offline sync. |
| STEP-6 | Mid-Phase Check-in | | Planned | `mine-flow-docs`, `prompts` | Run standard check-in runbook (`runbooks/check-in.md`) to reconcile drift and review risks. |
| STEP-7 | Tier 2 - Field Tracking & Measurement | | Planned | `mine-flow-app` | Build manual entry screens and data flow for cut/fill volume tracking, land clearing area, and inventory. |
| STEP-8 | Tier 2 - Data Bucket Integration | | Planned | `mine-flow-app` | Integrate Google Drive API for uploading heavy geospatial files (.shp, .tiff) and save metadata to Supabase. |
| STEP-9 | Tier 3 - Reporting, Timeline & Polish | | Planned | `mine-flow-app` | Add visual work timeline, PDF report generation, and in-app notifications. |
| STEP-10 | End-to-End Integration & Final Check-in | | Planned | `mine-flow-app`, `mine-flow-docs`, `prompts` | Wire capabilities together to ensure launch criteria are met end-to-end, and run final check-in. |

<!-- STEP-1 is the ONLY row at bootstrap. STEP-2 onward are the implementation STEPs — don't
     add them by hand: after STEP-1's review passes, run the planning session
     (templates/planning-session.md) and it outlines all the Phase-1 implementation STEPs
     here (a couple of sentences each), in dependency order after STEP-1. Each STEP's detailed
     PLAN and substeps are written later, when you start that STEP. Example row shape:
     | STEP-2 | Scaffold repos & skeleton | | Planned | `mine-flow-api` | … | -->


### STEP-1 substeps (architecture sessions)

> Like every STEP, STEP-1 has **one owner**, run on one machine — substeps aren't split
> across people (see `runbooks/collaboration.md` §3). But architecture is a shared
> foundation, so **decide it as a group**: the best setup is the whole team in a room walking
> the sessions together while one person drives the keyboard and commits the docs.

| Substep | Session | Status | Output doc |
|---------|---------|--------|------------|
| 1.1 | System Overview, Requirements & Non-Goals | Done | `architecture/01-system-overview.md` |
| 1.2 | Phasing & Roadmap | Done | `architecture/02-phasing-roadmap.md` |
| 1.3 | Architecture Overview & Component Boundaries | Done | `architecture/03-architecture-overview.md` |
| 1.3a | Native App Architecture | Done | `architecture/15-native-app-architecture.md` |
| 1.4 | Data Model, Ownership & Retention | Done | `architecture/04-data-model.md` |
| 1.5 | Scaling & Performance | Done | `architecture/05-scaling-performance.md` |
| 1.6 | Security & Threat Model | Done | `architecture/06-security-threat-model.md` |
| 1.6a | Identity & Auth | Done | `architecture/16-identity-auth.md` |
| 1.6b | Privacy, Compliance & Data Governance | Done | `architecture/17-privacy-compliance.md` |
| 1.7 | UI / Design System | Done | `architecture/07-ui-design-system.md` |
| 1.8 | Infrastructure & Deployment | Done | `architecture/08-infrastructure-deployment.md` |
| 1.9 | Environments | Done | `architecture/09-environments.md` |
| 1.10 | Observability | Done | `architecture/10-observability.md` |
| 1.11 | Interface Contracts | Done | `architecture/11-interface-contracts.md` |
| 1.12 | Test Strategy | Done | `architecture/12-test-strategy.md` |
| 1.13 | Glossary | Done | `architecture/13-glossary.md` |
| 1.14 | Cross-Cutting Review | Done | review doc |

<!-- Conditional sessions: enumerate every conditional-*.md template and include/defer/skip it
     in the STEP-1 PLAN's "Conditional sessions considered" table. Add an index row only when
     one is included. Slot included conditionals under a LETTERED substep after the related
     owning session, and run them BY NAME, not number (for example, "run the identity-auth
     session" → conditional-identity-auth.md). The output doc takes the next number above the
     core set. EXAMPLE ONLY — do not parse this as a real row; real rows start at the left
     margin above this comment, with the assigned substep and doc number:
       | 1.Xa | Conditional topic | Planned | `architecture/NN-topic.md` |
     If a conditional row is later added and then consciously not needed under the current
     project shape, mark it Deferred with the revisit trigger in the PLAN/risk register. -->

## How to add a STEP
See `prompts/README.md` for the authoring recipe.
