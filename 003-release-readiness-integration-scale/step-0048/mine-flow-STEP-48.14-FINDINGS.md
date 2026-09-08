# STEP-48.14 Findings: Risk-Register Reconciliation

## Evidence Table

| Row | Status Before | Owning Substep | Evidence / Result | Recommendation / Action |
|---|---|---|---|---|
| RISK-0006 | `open` | 48.11 | `mine-flow-STEP-48.11-FINDINGS.md`: go_router v18 deep-link routing verified across all 21 routes, shell persists correctly. | Close with evidence. |
| RISK-0011 | `open`, high | 48.13 | `reports/2026-08-30-step-0048-runtime-design-review.md` (DR-0003): Privacy Notice still absent at runtime. | Re-justify, keep open as pre-release gate. |
| RISK-0015 | `monitoring` | 48.13 | `reports/2026-08-30-step-0048-runtime-design-review.md` (DR-0001): Verified light-mode login respects theme via visual evidence. | Close with evidence. |
| RISK-0016 | `monitoring` | 48.13 | `reports/2026-08-30-step-0048-runtime-design-review.md` (DR-0002): Verified correct routes highlight sidebar via visual evidence. | Close with evidence. |
| RISK-0017 | `monitoring` | (D2) | `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`: Drive out of scope by decision D2. | Re-justify as Deferred by D2; update trigger. |
| RISK-0018 | `monitoring` | (D2) | Same as RISK-0017. | Re-justify as Deferred by D2; update trigger. |
| RISK-0019 | `monitoring` | 48.7 | `mine-flow-STEP-48.7-FINDINGS.md`: Harness does not prove true cold-start deep-link. | Re-justify and keep open/monitoring. |

## Incidental Rows Updated

| Row | Update | Source |
|---|---|---|
| RISK-0007 | Added positive durability evidence from Part A of offline sync test. | `mine-flow-STEP-48.10-FINDINGS.md` |
| RISK-0008 | Added positive session restore evidence against live backend. | `mine-flow-STEP-48.3-FINDINGS.md` |
| RISK-0010 | Noted ClickOps provisioning confirmed intact via pre-flight gate. | `mine-flow-STEP-48.0-FINDINGS.md` |
| RISK-0014 | Added confirmation that reporting formula still queries legacy columns. | `mine-flow-STEP-48.5-FINDINGS.md`, `48.8-FINDINGS.md` |

## New Deferral Rows Raised

- **RISK-0021**: Partial RLS matrix and cross-role isolation unverified (crew leg unrunnable due to missing `TEST_CREW_*` staging credentials). (From 48.12)
- **RISK-0022**: Benchmark journey deferred against staging because the `benchmarks` table does not exist in the staging database. (From 48.7)
- **RISK-0023**: Accessibility (screen-reader) unverified. Design review marked it Unverified because screenshots cannot prove screen-reader behavior. (From 48.13)

## RISK-0017/0018 Resolution
Their triggers stated "When staging Google Drive credentials are available". However, since the service account secrets already exist in CI and this was explicitly scoped out by decision D2 in STEP-48 planning, keeping the old trigger is dishonest. The triggers have been rewritten to state "Deferred by decision D2 to a future STEP focusing on Drive integration" to accurately reflect that it's a deliberate scope deferral.

## Duplicate Scan
```bash
grep -oE '^[[:space:]]*- id: RISK-[0-9]+' Code/mine-flow-docs/registries/risks.yml | grep -oE 'RISK-[0-9]+' | sort | uniq -d
```
Returns empty.

## YAML / check.sh Result
Both YAML parsing and `./doctor.sh check` pass.

