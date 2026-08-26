# mine-flow — STEP-42.4: deploy-staging CI Job

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-42.4-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-42.3 set all `STAGING_*` GitHub Secrets and confirmed the CI test job passes. This substep adds a `deploy-staging` job to `.github/workflows/ci.yml` that builds Flutter Web with staging credentials and deploys it to GitHub Pages on every push to `master`. It also creates the GitHub Actions `staging` environment.

**Known state (as of completion of 42.3):**
- All `STAGING_*` GitHub Secrets are set.
- CI `test` and `build-android` jobs pass green.
- No `deploy-staging` or `deploy-production` jobs exist yet.
- `lib/core/data/models/generated/database.dart` committed.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/.github/workflows/ci.yml` ← you will extend this
- `Code/mine-flow-docs/architecture/08-infrastructure-deployment.md`
- `Code/mine-flow-docs/architecture/09-environments.md`

## Scope

**Own:** Create the `staging` GitHub Actions environment (ClickOps); add the `deploy-staging` job to `ci.yml`; verify the staging URL is reachable in a browser after a successful deploy run.

**Do not:** Add `deploy-production` (substep 42.5). Change any application code. Modify any secrets already set.

## Your task

### 1. Create the `staging` GitHub Actions environment (ClickOps)

In GitHub repo → **Settings → Environments → New environment**:
- Name: `staging`
- No required reviewers (staging deploys automatically).
- No wait timer.
- Save.

Record that you created it.

### 2. Add the `deploy-staging` job to `ci.yml`

Append the following job to `Code/mine-flow-app/.github/workflows/ci.yml` after the `build-android` job:

```yaml
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-android
    if: github.ref == 'refs/heads/master'
    environment:
      name: staging
      url: ${{ steps.deploy.outputs.page_url }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: "3.47.0"
          channel: stable
          cache: true

      - name: Get dependencies
        run: flutter pub get

      - name: Build Flutter Web (staging)
        run: |
          flutter build web --release \
            --dart-define=SUPABASE_URL=${{ secrets.STAGING_SUPABASE_URL }} \
            --dart-define=SUPABASE_ANON_KEY=${{ secrets.STAGING_SUPABASE_ANON_KEY }} \
            --dart-define=GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL=${{ secrets.STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL }} \
            --dart-define=GOOGLE_DRIVE_FOLDER_ID=${{ secrets.STAGING_GOOGLE_DRIVE_FOLDER_ID }} \
            --dart-define=APP_ENV=staging

      - name: Deploy to GitHub Pages (staging)
        id: deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: build/web
          destination_dir: staging
          publish_branch: gh-pages-staging

      - name: Upload staging APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: staging-apk-${{ github.sha }}
          path: build/app/outputs/flutter-apk/app-debug.apk
          retention-days: 14
```

### 3. Enable GitHub Pages for the staging branch (ClickOps)

After the first deploy run creates the `gh-pages-staging` branch:
- GitHub repo → **Settings → Pages → Source**: set to `Deploy from a branch` → branch `gh-pages-staging` → `/` (root).
- Note the published URL (format: `https://<org>.github.io/<repo>/staging/`).

If GitHub Pages is already configured for a different branch, create a second Pages site using the GitHub Actions Pages action (`actions/deploy-pages`) instead — check if the `peaceiris/actions-gh-pages` action supports this without needing a separate Pages config.

### 4. Commit and push to trigger the deploy

```bash
# From Code/mine-flow-app/:
git add .github/workflows/ci.yml
git commit -m "ci(STEP-42.4): add deploy-staging job for automatic staging deployment on master"
git push
```

Wait for the GitHub Actions run to complete. Record the run URL and all job statuses.

### 5. Verify the staging URL

Open the staging Pages URL in a browser:
- The mine-flow web app loads (login page appears).
- Log in with `supervisor@mineflow.dev` (password from seed data — check `supabase/seed.sql` or Supabase dashboard for the test password).
- Confirm the app reaches the dashboard without errors.

Record: staging URL, login result, and any console errors observed.

### 6. Verify the staging APK artifact

In GitHub Actions → the completed `deploy-staging` run → **Artifacts**:
- Confirm `staging-apk-<sha>` artifact is attached.
- Download it and confirm the file is a valid `.apk` (non-zero size, extension correct).

## Verification

- `deploy-staging` job appears in GitHub Actions and passes green on push to `master`.
- Staging GitHub Pages URL is reachable in browser; login page loads.
- Login with `supervisor@mineflow.dev` succeeds and dashboard renders.
- `staging-apk-<sha>` artifact is attached to the workflow run (14-day retention).
- `flutter analyze` still clean; no regressions to `flutter test`.

## Definition of done

- [ ] `staging` GitHub Actions environment created (no required reviewers).
- [ ] `deploy-staging` job added to `ci.yml` and committed.
- [ ] CI run passes: `test` → `build-android` → `deploy-staging` all green.
- [ ] Staging web URL confirmed reachable; login with `supervisor@mineflow.dev` succeeds.
- [ ] Staging APK artifact attached to the CI run; file confirmed non-zero.
- [ ] Staging URL recorded for runbook (substep 42.7).

## Next

After confirming the staging URL is live, start a fresh chat and run **substep 42.5**: `Upcoming Prompts/mine-flow-STEP-42.5-PROMPT.md`.
