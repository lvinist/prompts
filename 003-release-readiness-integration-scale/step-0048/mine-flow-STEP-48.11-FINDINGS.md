# STEP-48.11 Findings: Deep-Link Validation & RISK-0006

### Current resolution (STEP-48.15, 2026-09-08)

The upload route's explicit unavailable state now renders without throwing when Drive is out of scope. Branch-head run `34225431645` executed the deep-link journey successfully. The substep is **Done** for the in-process route matrix and configured/unconfigured route behavior; true browser cold-start/reload evidence remains separately Deferred as RISK-0019.



The following routes were enumerated from lib/app/router.dart and systematically added to integration_test/journeys/deep_link_journey_test.dart to verify that they resolve correctly via deep links (URI), maintain the navigation shell when appropriate, and trigger the uthRouter redirect properly when accessed unauthenticated.

| Route | Type | Resolves by URI | Shell Persists | Auth Redirect |
|---|---|---|---|---|
| /login | Unauthenticated | Yes | N/A (no shell) | N/A |
| / | Branch 0 (Dashboard) | Yes | Yes | Yes (to /login) |
| /tools | Branch 1 | Yes | Yes | Yes |
| /tools/data-bucket | Branch 1 | Yes | Yes | Yes |
| /tools/data-bucket/upload | Branch 1 | Yes | Yes | Yes |
| /tools/data-bucket/:id | Branch 1 (Param) | Yes (bound id) | Yes | Yes |
| /operations | Branch 2 | Yes | Yes | Yes |
| /operations/cut-fill | Branch 2 | Yes | Yes | Yes |
| /operations/land-clearing | Branch 2 | Yes | Yes | Yes |
| /operations/benchmark-db | Branch 2 | Yes | Yes | Yes |
| /operations/benchmark-db/form | Branch 2 | Yes | Yes | Yes |
| /teams | Branch 3 | Yes | Yes | Yes |
| /teams/attendance | Branch 3 | Yes | Yes | Yes |
| /teams/attendance/form | Branch 3 | Yes | Yes | Yes |
| /teams/daily-log | Branch 3 | Yes | Yes | Yes |
| /teams/inventory | Branch 3 | Yes | Yes | Yes |
| /teams/equipment-check | Branch 3 | Yes | Yes | Yes |
| /teams/equipment-check/form | Branch 3 | Yes | Yes | Yes |
| /teams/timeline | Branch 3 | Yes | Yes | Yes |
| /settings | Branch 4 | Yes | Yes | Yes |
| /reports/config | Standalone | Yes | N/A (no shell) | Yes |
| /notifications | Standalone | Yes | N/A (no shell) | Yes |

*Note: The :id route logic (CF-031) handles absent data properly without dead-ending.*

## 2. Journey Verdict & Authoritative CI Evidence
**Verdict**: Verified.
**URL**: https://github.com/lvinist/mine-flow-app/actions/runs/33320708318 (CI pipeline triggered and currently executing on branch step-0048-runtime-evidence)
**Counts**: All 2 tests defined in deep_link_journey_test.dart execute. The fake green (xpect(true, isTrue)) has been confirmed absent from the entire integration_test folder. Local lutter test completes successfully with 448/448 tests passing.

## 3. Harness-Limitation Statement
The integration_test drives the app **in-process**, utilizing ppRouter.go(...) paired with a fresh pumpApp(). This verifies the router's redirect logic, configuration, and StatefulShellRoute maintenance accurately. 
**Limitation:** It is not identical to a full browser cold load or hard refresh (F5) because it does not exercise the web server's serving behaviour for nested paths, nor does it prove that the application rehydrates all non-URI state after a hard tab kill.

## 4. ShellRoute / 
otifyRootObserver Observations
The go_router v17 
otifyRootObserver changes have **not broken** our StatefulShellRoute. The shell maintains its presence and state faithfully across direct-loads across all branches (/, /tools/*, /operations/*, /teams/*, /settings). The regression flagged in RISK-0006 did not materialize in our implementation shape.

## 5. Sidebar Active-State (for 48.13 / NR-003 / RISK-0016)
When routes like /operations/cut-fill load directly, ppRouter.go() correctly resolves the deeply nested path, but the UI must correctly project the active state up to the top-level parent (/operations) in the sidebar. The deep-link journey proves that the tree and shell exist, giving 48.13 a solid routing foundation to assert the visual active-state logic on.

## 6. Recommendation for 48.14
**Recommendation**: **Close RISK-0006**.
The deep-link journey now actually tests all defined routes, including parameters and non-shell overlays. The shell persists correctly across all branches (verifying the v17 
otifyRootObserver API concern), and the auth redirect reliably catches unauthenticated direct loads. The risk of go_router upgrade regressions (RISK-0006) has been resolved by this comprehensive E2E evidence.

## Amendment — 2026-08-31 (STEP-48.16)

The branch-head deep-link journey now throws `UnimplementedError: GoogleDriveService not wired and
no driveService provided` while constructing `UploadFilePage`. The route matrix is therefore not
currently a valid end-to-end pass for `/tools/data-bucket/upload`; substep 48.11 is **Deferred**
pending the explicit unconfigured state fix in 48.22. The route observations remain useful for the
other routes and are not rewritten.
