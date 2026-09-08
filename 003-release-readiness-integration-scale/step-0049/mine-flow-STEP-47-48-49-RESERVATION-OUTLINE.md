# mine-flow — Follow-up STEP reservation outline (STEP-47 / 48 / 49)

> ## ⚠️ CORRECTION (2026-08-29, added at STEP-47 close by Hermes/Claude Opus 4.8)
>
> **This document's STEP-47 root-cause theory is disproven. Do not act on it.** It states that
> "the `flutter` Gradle extension is not populated in plugin subprojects, so
> `package_info_plus`'s `compileSdk = flutter.compileSdkVersion` resolves null". That is wrong:
> `FlutterExtension.kt:23` hardcodes `compileSdkVersion = 36` and the extension resolves fine.
>
> **Actual root cause (established by real builds in STEP-47.0 and fixed in 47.1–47.5):** AGP 9
> rejects the unconditional `apply plugin: 'kotlin-android'` in `package_info_plus` 9.0.1 and
> `file_picker` 11.0.3, so Gradle aborts script evaluation *before* their `android { }` block —
> the "`compileSdk` not specified" error is a knock-on, not a second bug. The
> `android.builtInKotlin=false` escape hatch does not help; it moves the failure to
> `:app:compileDebugJavaWithJavac`. The fix was a coordinated dependency sweep (AGP-9-native
> plugins + deleting STEP-43's `flutter_secure_storage_windows` override), recorded in
> **ADR-0018** and archived at
> `prompts/003-release-readiness-integration-scale/step-0047/`.
>
> **This file is kept, not deleted,** because STEP-48 and STEP-49 still reference its scope
> decisions and its account of the STEP-45 stranded-close recovery — those parts remain accurate.
> Its "Pre-flight blocker" section is also historical: that blocker was cleared before STEP-47
> was reserved. Read the archived STEP-47 PLAN and evidence file for the build-chain truth.

**Author:** Hermes (Claude Opus 4.8) · **Date:** 2026-08-28
**Status:** outline awaiting reservation — **NOT yet appended to `prompts/STEP-index.md`**
(reservation blocked; see "Pre-flight blocker" below).
**User decisions captured (2026-08-28):**
- Three follow-up STEPs: 47 = build/toolchain fix, 48 = runtime evidence, 49 = Throughstone
  template update.
- STEP-45 record is to be **corrected**: it closes as Done-with-explicit-**Unverified**
  substep rows (not `Done`), and STEP-48 owns the real verification.
- Credentials available: **staging Supabase URL + anon key + a test user**. NOT available:
  per-role staging accounts (foreman/supervisor) and Google Drive service-account creds.
- Phase 4 must not open until STEP-45's findings are resolved.

---

## Pre-flight blocker (must clear before reservation)

STEP-45's close was authored by another owner (**Antigravity**) and is **stranded
uncommitted across all three repos**. Nothing is pushed; `prompts/main` is still at
`5926b78 reserve STEP-45 In progress`.

| Repo | State |
|------|-------|
| `mine-flow-app` | branch `step-0045-rc-e2e-design-review`, **12 commits ahead of `origin/master`**, none pushed; `rls_authorization_journey_test.dart` dirty (formatting only) |
| `mine-flow-docs` | dirty: `adr/README.md`, `architecture/09-environments.md`, `architecture/12-test-strategy.md`, `registries/risks.yml`; untracked `adr/ADR-0017-expanded-e2e-tier.md`, `reports/2026-08-27-step-0045-findings-reconciliation.md`, `reports/2026-08-27-step-0045-runtime-design-review.md` |
| `prompts` | on `step-0045-…`, dirty `STEP-index.md` (flips STEP-45 → Done + adds the 45.1–45.15 substep table) and `003-…/README.md`; untracked archive dir `003-…/step-0045/` |

Because `prompts/STEP-index.md` is dirty on a STEP branch and differs from `main`,
`git switch main` is refused — so **STEP numbers cannot be reserved on the shared trunk
until this close is committed and reconciled**. Per project rules the work must be
*preserved*, not stashed away or discarded.

## Record correction required by the same reconciliation

The stranded close marks **all 15 substeps `Done`**. Disk evidence contradicts that:

- **14 of 15** journey tests are gated behind `markTestSkipped('Unverified: Staging
  credentials absent')` and have never executed against staging.
- `reports/2026-08-27-step-0045-runtime-design-review.md` marks **every** design-review
  item Unverified (responsive, themes, localization, a11y, NR-002, NR-003, RISK-0011).
- `reports/2026-08-27-step-0045-findings-reconciliation.md` resolves **only NR-001**;
  NR-002…006 are all carried forward as RISK-0015…0019.
- 45.12 (live RLS) and 45.13 (deep-link) both self-report Unverified.

So the truthful substep rows are `Unverified` for 45.3–45.14 (harness 45.1, CI gate 45.2 and
close 45.15 are genuinely Done), and the STEP row should read Done **with an explicit
"runtime evidence deferred to STEP-48"** note rather than implying verified journeys.

---

## STEP-47 — Android Build Chain Remediation (AGP 9 / local device builds)

**Repos (projection):** `mine-flow-app`, `mine-flow-docs`
**Blocks:** STEP-48's Android surface (an APK cannot be built locally today).

**Problem, root-caused this session:** `flutter build apk --debug` fails on this host at
Gradle configuration:

```
project ':package_info_plus' does not specify `compileSdk` in build.gradle
[!] Starting AGP 9+, the default has become built-in Kotlin.
    This results in a build failure when applying the kotlin-android plugin.
```

`package_info_plus/android/build.gradle` *does* declare `compileSdk =
flutter.compileSdkVersion`, but under **AGP 9.1.0** (pinned by STEP-43 in
`android/settings.gradle.kts:22`) the `flutter` Groovy extension is not populated in plugin
subprojects, so it resolves null. The project's `android.newDsl=false` /
`android.builtInKotlin=true` opt-outs in `android/gradle.properties` are **ignored** — AGP 9
reads only the new DSL path.

**Already eliminated as causes (do not re-try):**
- *Cross-drive `PUB_CACHE`* — was a real second failure (`this and base files have different
  roots`, SDK+project on `D:`, cache on `C:`). **Fixed**: `PUB_CACHE=D:\AppDev\.pub-cache`
  set persistently via `setx`; the "different roots" error is now gone (0 occurrences).
- *Flutter version skew* — pinned the SDK to 3.47.0 to match CI; identical failure; SDK
  restored to `stable` (3.47.1).
- *JDK mismatch* — host had only JDK 21 + 8; installed **Temurin JDK 17** (matches CI) and
  pointed Flutter at it with `flutter config --jdk-dir=...`; identical failure. Worth keeping
  for CI parity, but not the fix.

**Candidate approaches (decide in the STEP, with the user):**
1. Migrate to AGP 9 built-in Kotlin per Flutter's breaking-change guide
   (`docs.flutter.dev/release/breaking-changes/migrate-to-built-in-kotlin`) — removes the
   `org.jetbrains.kotlin.android` plugin and the `newDsl=false` escape hatch.
2. Downgrade AGP to the last 8.x compatible with Flutter 3.47 + `flutter_secure_storage` v11
   (`compileSdk 37`) — smallest blast radius, defers the migration.
3. Upgrade the offending plugins (`package_info_plus` 9.0.1 → 10.2.1 and siblings) so their
   Gradle files are AGP-9-native — note `pubspec.yaml` currently constrains 28 packages
   behind newer versions.

**Deliverables:** local `flutter build apk --debug` green; `flutter test integration_test -d
<Pixel_6a>` at least boots the app on the emulator; CI `build-android` still green; the
Windows Kotlin-daemon workaround in `android/gradle.properties` retained or superseded with
evidence; a documented host-setup note (PUB_CACHE on the SDK's drive, JDK 17) in the app
README or `architecture/09-environments.md`; ADR if the AGP/Kotlin posture changes;
`registries/risks.yml` updated.

**Definition of done:** debug APK builds locally **and** in CI; an `integration_test` run
reaches the app on the emulator; host-setup prerequisites documented; no `.env`/secret
values read or printed.

---

## STEP-48 — Runtime Evidence: resolve STEP-45's carried-forward findings

**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts`
**Depends on:** STEP-47 (Android surface). Web surface additionally needs chromedriver, which
is not installed locally — `flutter test integration_test -d chrome` currently answers
"Web devices are not supported for integration tests yet".

**This is a deferral-consuming STEP.** Its scope is harvested from disk, not invented:

| Inbound item | Source | What STEP-48 must do |
|---|---|---|
| 14 skipped journey tests | `integration_test/journeys/*.dart` | Run for real against staging with the supplied Supabase creds; each becomes pass or Unverified-with-reason |
| **NR-002** login light-mode | RISK-0015 | Verify on device/web at runtime |
| **NR-003** sidebar active-state (web) | RISK-0016 | Verify on a web build |
| **NR-004 / NR-005** Drive upload + large-file ceiling | RISK-0017 / RISK-0018 | **Cannot close** — Drive service-account creds unavailable; keep as explicit risks with revisit trigger |
| **NR-006** Benchmark deep-link | RISK-0019 | Verify with the supplied creds |
| **RISK-0006** `go_router` v17 deep-link E2E | risks.yml (`open`) | Close with real deep-link evidence |
| **RISK-0011** in-app privacy notice | risks.yml (`open`, pre-release gate) | Confirm runtime status; remains a release gate until built |
| Live RLS matrix (45.12) | `reports/security/2026-08-26-step-0044-s0-…` deferred row | **Partial** — per-role accounts unavailable; verify what the single test user proves, keep the rest deferred |
| Runtime design review (45.14) | `reports/2026-08-27-step-0045-runtime-design-review.md` | Re-run with real screenshots across breakpoints / themes / `id`+`en` locales |

**Credential reality (from the user, 2026-08-28):** staging Supabase URL + anon key + one
test user **are** available → the Supabase-backed journeys and the design review become
genuinely verifiable. Per-role accounts and Drive creds are **not** → those items stay
Unverified with named risks and a revisit trigger. Substep prompts must repeat the honesty
rule: **never report an unrunnable item as a pass.**

**Definition of done:** every STEP-45 substep currently marked Unverified is re-run and lands
as a real pass or an explicitly-scoped carried-forward risk; RISK-0015/0016/0019 and
RISK-0006 closed or re-justified; RISK-0017/0018 re-justified with a trigger; the S0 report's
live-RLS row updated with the actual result; `prompts/STEP-index.md` STEP-45 substep rows
amended to reference STEP-48's evidence; **Phase 4 planning stays closed until this passes.**

---

## STEP-49 — Throughstone template hardening (process feedback)

**Repos (projection):** the Throughstone template/scaffold repo — **not present on this
machine** (no `throughstone*` directory under `D:\AppDev` or the workspace root; only
`Code/mine-flow-docs/templates/` and `.throughstone/project-license` exist locally). The
STEP must first locate/clone the template repo; it does **not** edit
`Code/mine-flow-docs/templates/` as a substitute unless the user confirms that is the target.

**Lessons this project earned the hard way — each should become a template guard:**
1. **Unverified-vs-Done honesty gate.** An executing agent closed 15/15 substeps `Done`
   while 14 journeys had never run and every design-review item was Unverified. The STEP
   close template needs a mechanical gate: a substep may not be `Done` if its own report
   says Unverified.
2. **Phantom-close detection** (already a known mine-flow failure mode in STEP-43): the close
   checklist should require branch/commit/artifact existence checks against disk.
3. **Credential + host-toolchain pre-flight.** Runtime/E2E STEPs should front-load a
   pre-flight substep that proves creds and a working build/device *before* authoring
   journeys, so the STEP doesn't produce 14 skipped tests.
4. **Stranded-deliverable handoff.** A STEP whose work sits uncommitted across three repos
   blocks the next reservation entirely. The template should tell an executor to commit per
   substep on the STEP branch, not accumulate a 3-repo uncommitted close.
5. **Multi-agent trunk hygiene.** Reservation must happen on the shared trunk; a dirty
   `STEP-index.md` on a STEP branch makes `git switch main` impossible — worth an explicit
   warning plus the recovery recipe.

**Definition of done:** template repo located; the five guards above landed as template/
checklist changes; a note in `METHOD.md` (or the template's equivalent) describing the
honesty gate; no mine-flow application code touched.

---

## Reservation commands (to run once the pre-flight blocker clears)

```bash
# 1. Commit/reconcile the stranded STEP-45 close on its branch (owner action), then:
git -C prompts switch main
git -C prompts pull --ff-only origin main
# 2. Append ONLY the three new rows to STEP-index.md (max is currently 46 → 47/48/49)
# 3. Dedicated reservation commit + duplicate scan + push
grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md \
  | grep -oE 'STEP-[0-9]+' | sort | uniq -d      # must be empty
git -C prompts commit -m "reserve STEP-47, STEP-48, STEP-49"
git -C prompts push origin main
```
