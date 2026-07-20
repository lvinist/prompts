# mine-flow — STEP-1 PLAN: Architecture

**Phase:** Phase 1 — MVP
**Owner:** (solo)
**Status:** Planned
**Date:** 2026-07-17
**Branch:** `step-0001-architecture`
**Repos (projection):** `mine-flow-docs`, `prompts`

> Design the full architecture for mine-flow — a mining operations dashboard built with
> Flutter + BLoC on Supabase — before writing any application code. This STEP produces
> architecture docs and ADRs only. It covers every aspect of the system: requirements,
> component boundaries, data model, security, UI design system, infrastructure, testing,
> and more. Each substep is an interactive session that interviews the user and writes one
> architecture doc.

## Motivation
mine-flow is a greenfield project with significant breadth (11 features, 3 user roles,
cross-platform Flutter app, Supabase backend, Google Drive integration, geospatial
metadata, SOP-based equipment checks). Building without an architecture plan would lead to
rework, especially around the data model (which must accommodate future multi-site), the
security model (personal data: national IDs, DOB), and the UI system (shadcn-admin-inspired
design translated to Flutter). STEP-1 locks the shape of the system so implementation
STEPs can be executed confidently.

## Decisions already locked
- root `.throughstone/local-user.md` — read **Experience level** (Level 2) before
  user-facing questions or explanations, and read **Communication style** (Explanatory)
  before planning discussions; keep that file as the personal local source of truth for
  both values.
- `registries/risks.yml` — review relevant accepted risks/debt before planning work that
  touches their area.
- **Tech stack** — Flutter + BLoC (non-negotiable), Supabase (non-negotiable), Google Drive
  for geospatial file storage.
- **Single-site MVP, multi-site-ready architecture** — don't hardcode single-site
  assumptions into the data model.
- **Design language** — shadcn-admin (collapsible sidebar, card dashboard, data tables,
  dark/light mode, clean professional aesthetics) translated to Flutter widgets.
- **Equipment check SOP forms** — GNSS RTK, Total Station, Drone/UAV with start-of-work
  and end-of-work checks only.
- **Sensitive data** — personal data (DOB, national ID), passwords (Supabase Auth),
  cut/fill volumes, land clearing areas must be protected.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 1.1 | System Overview, Requirements & Non-Goals | `architecture/01-system-overview.md` | — | — |
| 1.2 | Phasing & Roadmap | `architecture/02-phasing-roadmap.md` | 1.1 | — |
| 1.3 | Architecture Overview & Component Boundaries | `architecture/03-architecture-overview.md` | 1.1, 1.2 | Mono-repo vs multi-repo for Flutter app + shared packages |
| 1.3a | Native App Architecture | `architecture/15-native-app.md` | 1.3 | Platform-specific features (camera for daily logs, offline?) |
| 1.4 | Data Model, Ownership & Retention | `architecture/04-data-model.md` | 1.3 | Zone/area structure for cut/fill; equipment check schema |
| 1.5 | Scaling & Performance | `architecture/05-scaling-performance.md` | 1.3, 1.4 | — |
| 1.6 | Security & Threat Model | `architecture/06-security-threat-model.md` | 1.3, 1.4 | RLS policy granularity for roles |
| 1.6a | Identity & Auth | `architecture/16-identity-auth.md` | 1.6 | Auth flow (email/password, SSO?), role assignment mechanism |
| 1.6b | Privacy, Compliance & Data Governance | `architecture/17-privacy-compliance.md` | 1.4, 1.6 | Retention policies for personal data; national ID encryption |
| 1.7 | UI / Design System | `architecture/07-ui-design-system.md` | 1.3 | Flutter package selection for shadcn-like components |
| 1.8 | Infrastructure & Deployment | `architecture/08-infrastructure-deployment.md` | 1.3 | Flutter web hosting (Supabase Storage, Firebase Hosting, or other) |
| 1.9 | Environments | `architecture/09-environments.md` | 1.8 | Number of Supabase projects (dev/staging/prod?) |
| 1.10 | Observability | `architecture/10-observability.md` | 1.8 | Error tracking service (Sentry, Crashlytics?) |
| 1.11 | Interface Contracts | `architecture/11-interface-contracts.md` | 1.3, 1.4 | Supabase RPC vs direct table access patterns |
| 1.12 | Test Strategy | `architecture/12-test-strategy.md` | 1.3 | Flutter test tooling (widget tests, integration tests) |
| 1.13 | Glossary | `architecture/13-glossary.md` | all above | — |
| 1.14 | Cross-Cutting Review | review doc | all above | — |

## Test plan
<!-- Architecture STEP — no code is written, so no tests. -->
N/A — STEP-1 produces architecture docs and ADRs only; no application code is written.

## Conditional sessions considered

| Conditional session | Owning session | Decision | Substep / reason / revisit trigger |
|---------------------|----------------|----------|------------------------------------|
| Native app (mobile / desktop) | 1.3 Architecture Overview | **Include** | **1.3a** — Flutter targets mobile (Android/iOS) and desktop natively; need to decide platform-specific capabilities (camera, file access, offline), build/distribution strategy, and responsive breakpoints. |
| Identity & auth | 1.6 Security & Threat Model | **Include** | **1.6a** — The app requires login with three roles (supervisor, foreman, crew) and role-based data visibility. Supabase Auth is the provider; this session designs the auth flow, role assignment, token handling, and session management. |
| Privacy, compliance & data governance | 1.4 Data Model / 1.6 Security | **Include** | **1.6b** — The app stores personal data (date of birth, national identification numbers) and commercially sensitive operational data (cut/fill volumes, land clearing areas). Need to define encryption-at-rest, access controls, retention policies, and any applicable regulatory requirements. |

## Open questions
- **Q1** — Mono-repo vs multi-repo for the Flutter app code? (One repo for the whole app, or separate repos for shared packages, the app shell, etc.) — Resolved in 1.3.
- **Q2** — Google Drive integration approach: Google Drive API with service account, or simple URL linking with manual uploads? — Resolved in 1.3/1.11.
- **Q3** — Notification delivery: in-app only, or also push notifications (FCM) and/or email? — Resolved in 1.3.
- **Q4** — Offline capability: do field users need to work without connectivity? — Resolved in 1.3a.
- **Q5** — Report templates: what data goes into each report type? — Resolved in 1.4/1.11.

## Ground rules
- **No application code in this STEP.** Output is Markdown architecture docs + ADRs only.
- **Calibrate communication from root `.throughstone/local-user.md`.** The user is Level 2
  (basic coding experience) with Explanatory communication style — explain each question's
  *what* and *why* in plain language, lead with a recommended default, and avoid unexplained
  jargon. Tell the user they can ask for clarification at any time.
- **One decision/question cluster at a time.** Don't dump a wall of questions. Recommend
  sensible defaults; explain what they foreclose.
- **Plan interactively.** Before this PLAN is finalized, confirm scope with the user and ask
  clarifying questions for ambiguous requirements, sequencing, dependencies, ownership, or
  repo boundaries. When a planning decision is needed, offer appropriate options with brief
  pros and cons. Respect the saved communication style while still asking the questions
  needed to make the STEP coherent.
- **Sessions are self-contained.** Each session reads `overview.md` and earlier architecture
  docs from disk. The user can clear the chat between sessions — state lives in files.
- **Significant decisions become ADRs.** Use `Code/mine-flow-docs/templates/adr-template.md`.
  Never rewrite an accepted ADR — supersede or amend.
- **Accepted risks stay visible.** If this STEP accepts a risk or defers tech debt, add or
  update `registries/risks.yml` with severity, owner, and revisit trigger.

## Definition of done
- [ ] All 14 core architecture sessions completed and docs written.
- [x] All 3 conditional sessions (native-app, identity-auth, privacy-compliance) completed.
- [ ] All significant decisions recorded as ADRs.
- [ ] `prompts/STEP-index.md` substep table fully updated (all rows show `Done`).
- [ ] Cross-Cutting Review (1.14) passed — no gaps, no missing conditionals, docs are
      internally consistent.
- [ ] STEP review passed; `prompts/STEP-index.md` updated; STEP archived to `prompts/`.
