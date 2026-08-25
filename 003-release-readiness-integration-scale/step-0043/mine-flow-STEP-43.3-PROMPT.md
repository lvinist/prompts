# mine-flow — STEP-43.3: CI Workflow Hardening

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.3-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Gemini 3.1 Pro High

## Context

STEP-43.2 upgraded the Android build chain. This substep hardens the CI workflow to pin Flutter 3.47.0 and add explicit JDK 17 setup to both jobs, eliminating the split-SDK and unpinned-JDK root causes.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Section 1, Findings CI-1, CI-2, CI-3.

**Known state:**
- CI `test` job pins `flutter-version: "3.x"` (wildcard).
- CI `build-android` job also uses `flutter-version: "3.x"` (wildcard).
- Neither job has an explicit JDK setup step.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/.github/workflows/ci.yml`
- `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` (Section 1)

## Scope

**Own:** Pin Flutter version and add JDK 17 to both CI jobs.

**Do not:** Add new CI jobs. Change pubspec.yaml. Change any Dart or Gradle files.

## Your task

### 1. Add JDK 17 setup to both jobs

In `.github/workflows/ci.yml`, add this step **before** the "Setup Flutter" step in **both** the `test` and `build-android` jobs:

```yaml
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
```

### 2. Pin Flutter to 3.47.0 in both jobs

In both jobs, change the `flutter-version` value:
- `test` job: `flutter-version: "3.x"` → `flutter-version: "3.47.0"`
- `build-android` job: `flutter-version: "3.x"` → `flutter-version: "3.47.0"`

### 3. Review the final CI file

After changes, both jobs should have this pattern:
```
Checkout → Set up JDK 17 → Setup Flutter (3.47.0) → Get dependencies → ...
```

### 4. Commit and push

This is the first push for the STEP-43 branch:

```powershell
git add .github/workflows/ci.yml
git commit -m "ci(STEP-43.3): pin Flutter 3.47.0, add JDK 17 Temurin to both CI jobs"
git push -u origin step-0043-flutter-upgrade
```

Now the CI will run — it will still fail (we haven't done the Dart migrations yet), but at least the CI infrastructure is correct.

## Verification

- Both CI jobs have `actions/setup-java@v4` with JDK 17 Temurin.
- Both CI jobs pin `flutter-version: "3.47.0"`.
- No `3.x` or `3.32.x` wildcards remain.
- Branch pushed to remote.

## Definition of done

- [ ] JDK 17 Temurin setup added to both CI jobs.
- [ ] Flutter pinned to `3.47.0` in both CI jobs.
- [ ] No wildcard Flutter versions remain.
- [ ] Committed and pushed on `step-0043-flutter-upgrade`.

## Next

After committing, continue in the same chat to **substep 43.4**: `Upcoming Prompts/mine-flow-STEP-43.4-PROMPT.md`.
