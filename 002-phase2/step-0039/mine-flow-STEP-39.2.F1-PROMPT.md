# 39.2.F1 — Documentation Link Repair, Repository Hygiene & Dependency Constraint Finalization

**Goal:** Repair 16 broken documentation links, finalize the `battery_plus` dependency constraint, revert machine-specific `links.sh` hacks, and sanitize untracked files in the docs repository.

## Steps
1. **Correct ADR-0010 status:** Change status to `Accepted` in the ADR file, index, architecture docs, and PLAN.
2. **Correct `battery_plus` constraint:** Determine the exact intended dependency policy for `battery_plus` and document it.
3. **Revert `links.sh`:** Restore `Code/mine-flow-docs/scripts/links.sh` to use `python3` and run validation using a compatible local method.
4. **Repair 16 broken documentation links:** Fix all broken links reported by the validation script.
5. **Reconcile untracked files:** Move durable files to appropriate tracked locations, and remove or document temporary files.
6. **Verify generated-root files:** Ensure `DESIGN.md` and `PRODUCT.md` are at the workspace root, match the source document, and are not accidentally tracked in `Code/mine-flow-docs`.
7. **Commit and push:** Create a commit on `step-0039-check-in` with these corrections and push it.
