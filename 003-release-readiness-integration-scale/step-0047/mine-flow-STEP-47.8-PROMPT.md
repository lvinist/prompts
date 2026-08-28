# mine-flow — STEP-47.8: Documentation — host prerequisites, ADR, risks register

> **How to run:** Tell your agent *"run substep 47.8"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.7 Flash High. The thinking was done in 47.1–47.7; this substep collects their
> notes into durable docs. Escalate only if Q5 (ADR vs Version Log) turns out genuinely contested.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`. Substeps 47.1–47.7 each ended with a
**"notes for 47.8"** block in their status updates. This substep turns those notes into the docs hub's
durable state, so the next agent inherits the reasoning instead of rediscovering it.

Nothing here is optional bookkeeping: the reason STEP-47 exists at all is that the host prerequisites
(PUB_CACHE drive rule, JDK 17) were never written down, so three separate sessions burned time
rediscovering them.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md` — **Q5** is this substep's decision
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — the whole STEP's evidence, including 47.5's
  local build result and 47.7's CI outcome
- Each substep's "notes for 47.8" block (47.1–47.7)
- `Code/mine-flow-app/README.md` — currently has "Android toolchain (Android SDK, accepted licenses)"
  under prerequisites and a troubleshooting row for Android licenses, but **nothing** about the
  PUB_CACHE drive rule or JDK 17
- `Code/mine-flow-docs/architecture/09-environments.md` — **v0.3.0**, last updated 2026-08-27
  (STEP-45.15). Note its structure: numbered sections, a Decision Summary, Open Questions, and a
  **Version Log** table you must append to
- `Code/mine-flow-docs/adr/README.md` — ADR conventions. **Reserve the number like a STEP number**:
  pull, take `max + 1` over the registry, add the row, create the file, commit, and scan for
  duplicates. Current max is **ADR-0017**, so a new ADR is **ADR-0018**
- `Code/mine-flow-docs/templates/adr-template.md`
- `Code/mine-flow-docs/registries/risks.yml` — study an existing entry's exact shape (RISK-0019 is a
  good model: `id`, `status`, `title`, `category`, `severity`, `owner`, `opened`, `source`,
  `description`, `impact`, `mitigation`, `revisit_trigger`, `refs`, `closed:{date,reason}`)
- **RISK-0008** (secure-storage v9→v11 skipped v10 migration) — you are amending its context
- **RISK-0006** (`go_router` v17 deep-link E2E unverified) — wording refresh only; **stays open**
- **ADR-0003** (Google Drive), **ADR-0014** (persist CRS), **ADR-0017** (expanded E2E tier)

## Scope

**Owns:** `Code/mine-flow-app/README.md`, `Code/mine-flow-docs/architecture/09-environments.md`, a new
ADR if Q5 says so, `Code/mine-flow-docs/registries/risks.yml`, `Code/mine-flow-docs/adr/README.md`
(registry row only).

**Does NOT touch:** any `.dart` file, `pubspec.yaml`, `android/**`, `ci.yml`, `prompts/STEP-index.md`
(47.9 owns the index flip and archive). Do not edit an existing ADR's accepted text — ADRs are
immutable; amend with a dated `## Amendment` or write a new one.

## Your task

### 1. Document the host prerequisites in the app README

Add a subsection under the existing prerequisites/setup area covering what actually blocked local
Android builds. Frame it as *requirements with reasons*, because a bare instruction gets skipped:

- **`PUB_CACHE` must be on the same drive as the Flutter SDK and the project.** On this host: SDK at
  `D:\AppDev\flutter`, project at `D:\AppDev\mine_flow`, so `PUB_CACHE=D:\AppDev\.pub-cache` (set
  persistently via `setx`). With the default `C:\Users\<user>\AppData\Local\Pub\Cache`, the Gradle
  build fails with *"this and base files have different roots"* because Gradle cannot compute a
  relative path across Windows drive letters.
- **JDK 17 (Temurin)** wired via `flutter config --jdk-dir=<path>`, matching CI's
  `actions/setup-java` `java-version: '17'`. AGP 9 requires 17;
  `DependencyVersionChecker.kt` errors below it.
- **Android emulator** `Pixel_6a` is the local device used for the boot check; CI uses
  `reactivecircus/android-emulator-runner` at api-level 33 / google_apis / x86_64 / pixel_6a.
- **Web E2E needs chromedriver** — `flutter test integration_test -d chrome` is *not supported*; use
  `flutter drive --driver=test_driver/integration_test.dart --target=<test> -d web-server` with
  chromedriver running on port 4444. (Take the exact command from 47.6's notes so README and CI agree.)
- **Kotlin/Gradle posture** — record Q4's outcome from 47.5: whether
  `kotlin.compiler.execution.strategy=in-process` / `kotlin.incremental=false` are still required on
  Windows, and that `android.builtInKotlin=true` is required under AGP 9 while
  `android.newDsl=false` is Flutter's own compatibility shim (re-added automatically by the tool).

Also add troubleshooting rows next to the existing "Android build fails: license" row: the
different-roots PUB_CACHE error, and the `kotlin-android`/`compileSdk` symptom pair with the pointer
that it means a plugin predating AGP 9 (fixed in STEP-47 by upgrading, not by flags).

### 2. Update `architecture/09-environments.md`

Additions, kept tight — this is a durable architecture doc, not a changelog:

- **§3 Environment Parity** — the local host toolchain requirements that make Local match CI:
  JDK 17, Flutter pin (state the actual CI pin after 47.7; it was `3.47.0` and may have moved to
  `3.47.1`), AGP 9.1.0 / KGP 2.4.0 / Gradle 9.3.1, and the same-drive `PUB_CACHE` rule.
- **§4 Promotion Flow** — if 47.6/47.7 changed how the E2E gates are invoked, reflect it: web E2E runs
  through `flutter drive` + chromedriver, not `flutter test -d chrome`. **State plainly** that a green
  E2E gate currently proves the *harness executes*, and that the 14 staging journeys remain Deferred to
  STEP-48. Without that sentence a reader sees three green checks and concludes the runtime evidence
  exists.
- **Version Log** — append a `v0.4.0` row dated today, STEP-47.8, summarising the parity and gate
  changes. Bump the `**Version:**` header and `**Last updated:**` line to match.

### 3. Answer Q5 and write the ADR if warranted

Q5: does this STEP's outcome warrant a new ADR, or is a Version Log bump enough?

**Recommendation: write the ADR.** Three of the changes reverse or supersede recorded decisions, which
is exactly what ADRs exist for:

- STEP-43 deliberately added `dependency_overrides: flutter_secure_storage_windows: 4.0.0` with a
  documented rationale in `pubspec.yaml`. 47.1 deleted it. A future reader who finds that comment gone
  deserves to know why.
- The Android build posture moved from "AGP 9 + legacy-KGP escape hatches" to "AGP 9 built-in Kotlin
  with AGP-9-native plugins". That is the project's Kotlin-compilation strategy.
- `win32` 5.x → 6.x and `flutter_secure_storage_windows` 4.0.0 → 4.2.2 touch the Windows-desktop
  secure-storage surface, which intersects Doc 06's security posture.

If you write it, it is **ADR-0018** (max is ADR-0017 — re-verify from `adr/README.md`, do not trust
this number blindly). Use `templates/adr-template.md`. Content:

- **Context** — AGP 9 rejects unconditional `apply plugin: 'kotlin-android'`; two plugins
  (`package_info_plus` 9.0.1, `file_picker` 11.0.3) did exactly that; the `win32` coupling made
  partial upgrades unresolvable; the `builtInKotlin=false` escape hatch was tried and fails at
  `:app:compileDebugJavaWithJavac`.
- **Decision** — adopt AGP 9 built-in Kotlin; upgrade to AGP-9-native plugin versions; delete the
  `dependency_overrides` block; sweep the coupled majors; keep `android.newDsl=false` as Flutter's
  shim. Explicitly reject the AGP-8 downgrade path and say why (Flutter 3.47 warns below AGP 9.0.1;
  AGP 10 forces the migration anyway).
- **Consequences** — plugin choices are now constrained to AGP-9-native versions; `win32` 6.x is
  project-wide; `flutter_secure_storage_windows` moved 4.0.0 → 4.2.2 (Windows-desktop surface only,
  not the Android Keystore path ADR-0005/Doc 06 depends on — **verify this claim against 47.1's
  resolution notes before asserting it**); local Android builds require the documented host setup.

Add the registry row in `adr/README.md`, then run the duplicate scan the README prescribes:

```bash
grep -oE '^\|[[:space:]]*ADR-[0-9]+' adr/README.md | grep -oE 'ADR-[0-9]+' | sort | uniq -d
```

Empty output is success.

### 4. Update `registries/risks.yml`

Match the existing entry shape exactly (YAML in this file is load-bearing for `doctor.sh`).

- **RISK-0008** — its `mitigation` says "minSdk = 23 explicit in build.gradle.kts. See RISK-0008."
  Amend to note the `flutter_secure_storage_windows` 4.0.0 → 4.2.2 / `win32` 6.x change from STEP-47.1,
  and state whether the Android Keystore posture is unaffected (it should be — the Windows package is
  a desktop-only implementation — but cite 47.1's notes, don't assert it from intuition). Keep the
  risk `monitoring`; STEP-47 does not resolve it.
- **RISK-0006** — refresh the wording from "go_router v17" to reflect that the app is now on
  `go_router` 18. **Status stays `open`.** Deep-link runtime evidence is STEP-48's; do not close it,
  and do not weaken its `revisit_trigger`.
- **RISK-0017 / RISK-0018** (Drive upload + large-file ceiling) — untouched by this STEP. If 47.4 found
  anything about the Drive surface, add a `refs` line; otherwise leave them alone.
- **New risk, if any** — did the sweep leave accepted debt? Candidates: transitive packages still
  behind because Flutter's SDK pins them (`archive`, `qr`, `package_config`,
  `material_color_utilities`, the analyzer/test family); or a `flutter_lints` 6 rule the team decided
  to live with. Only add a row for something real, with `severity`, `owner`, and a concrete
  `revisit_trigger`. Do not invent risk rows to look thorough.

### 5. Verify and commit

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-docs
python -c "import yaml,sys; d=yaml.safe_load(open('registries/risks.yml',encoding='utf-8')); print('risks.yml parses OK')"
grep -oE '^\|[[:space:]]*ADR-[0-9]+' adr/README.md | grep -oE 'ADR-[0-9]+' | sort | uniq -d
cd /d/AppDev/mine_flow && ./doctor.sh status
```

`doctor.sh status` must still resolve — a malformed risks.yml or a bad status cell breaks it. (On
PowerShell: `& "C:\Program Files\Git\bin\sh.exe" .\doctor.sh status`.)

```bash
git -C Code/mine-flow-docs add architecture/09-environments.md registries/risks.yml adr/
git -C Code/mine-flow-docs commit -m "docs(STEP-47.8): AGP 9 built-in Kotlin posture, host prerequisites, risk updates"
git -C Code/mine-flow-app  add README.md
git -C Code/mine-flow-app  commit -m "docs(STEP-47.8): document Android host prerequisites and web E2E command"
```

## Verification

This substep is documentation, so it has no unit tests — but it does have checkable claims:

- Every prerequisite in the README is one **47.0/47.5 actually proved**, not folklore. If you cannot
  point at evidence for a claim, cut it.
- `risks.yml` parses as YAML and `doctor.sh status` still resolves.
- The ADR duplicate scan is empty; the new ADR appears in the registry.
- `09-environments.md`'s Version Log has a new row and the header Version matches it.
- No existing ADR's accepted text was rewritten.
- Doc 09 states explicitly that green E2E gates ≠ verified journeys, with the STEP-48 pointer.

Cross-check the commands you document by running them. A README instruction nobody executed is how the
PUB_CACHE trap survived three sessions.

## Keeping the docs true (always)

This substep *is* the doc-truth pass, so apply the standard to itself:

- If 47.4 reported a `googleapis` Drive-facing signature change, update
  `architecture/11-interface-contracts.md` and consider an ADR-0003 amendment.
- If 47.4 raised a `flutter_lints` 6 convention question, that belongs in `coding-standards/` — and it
  is a **user decision**, so ask rather than deciding.
- If 47.6 found `architecture/12-test-strategy.md` §6 implies `flutter test` for web E2E, fix that
  wording and bump its Version Log too.

No secrets: name `STAGING_*` secrets only, never values. `.env` stays unread.

## Definition of done

- [ ] App `README.md` documents the PUB_CACHE same-drive rule (with the "different roots" symptom),
      JDK 17 via `flutter config --jdk-dir`, the emulator used, the chromedriver/`flutter drive` web
      E2E command, and the `gradle.properties` flag posture
- [ ] README troubleshooting rows added for the PUB_CACHE error and the `kotlin-android`/`compileSdk`
      symptom pair
- [ ] `architecture/09-environments.md` §3 parity + §4 promotion flow updated; Version Log `v0.4.0`
      appended; header Version and Last updated bumped
- [ ] Doc 09 states plainly that green E2E = harness executes, journeys Deferred to STEP-48
- [ ] Q5 answered; ADR written (expected **ADR-0018**) with context, decision, rejected AGP-8
      alternative, and consequences — or a stated reason none is needed
- [ ] ADR registry row added; duplicate-number scan empty
- [ ] `risks.yml`: RISK-0008 amended, RISK-0006 wording refreshed and **still open**, any genuinely new
      debt recorded with severity/owner/revisit trigger
- [ ] `risks.yml` parses; `doctor.sh status` resolves
- [ ] Doc 11 / coding-standards / Doc 12 follow-ups from 47.4 and 47.6 handled or explicitly raised
- [ ] No `.dart`, `pubspec.*`, `android/**`, `ci.yml`, or `STEP-index.md` change
- [ ] Committed in both `mine-flow-docs` and `mine-flow-app` on `step-0047-android-build-chain`

## Next

Update 47.8's status in the PLAN, then tell the user the next action: **run substep 47.9** (final
verification & STEP close) in a fresh chat.
