# mine-flow — STEP-42.5: deploy-production Job & Manual Gate

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-42.5-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-42.4 deployed staging automatically on every `master` push. This substep wires the `deploy-production` job — triggered only on GitHub Release publish — and gates it behind a required reviewer so no production release can happen without human approval.

**Known state (as of completion of 42.4):**
- `deploy-staging` job deployed and confirmed working.
- Staging URL live and login confirmed.
- No `deploy-production` job exists yet.
- `PROD_*` GitHub Secrets do **not** exist yet (production provisioning is out of scope for STEP-42; the job will reference them so they can be added before the first real release).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/.github/workflows/ci.yml` ← you will extend this
- `Code/mine-flow-docs/architecture/08-infrastructure-deployment.md`
- `Code/mine-flow-docs/architecture/09-environments.md`

## Scope

**Own:** Create `production` GitHub Actions environment with required reviewer (ClickOps); add `deploy-production` job to `ci.yml`; dry-run with a test pre-release tag to confirm the gate blocks without approval; clean up the test tag.

**Do not:** Set `PROD_*` secrets (production project not yet provisioned — STEP-43+ concern). Actually approve and execute a production deploy. Change any application code or existing CI jobs.

## Your task

### 1. Create the `production` GitHub Actions environment (ClickOps)

In GitHub repo → **Settings → Environments → New environment**:
- Name: `production`
- **Required reviewers**: add yourself (or a designated approver).
- No wait timer.
- Save.

This is the gate: no job targeting `production` can run without an explicit approval in the GitHub Actions UI.

### 2. Add the `deploy-production` job to `ci.yml`

Append after the `deploy-staging` job in `Code/mine-flow-app/.github/workflows/ci.yml`:

```yaml
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    if: github.event_name == 'release' && github.event.action == 'published'
    environment:
      name: production
      url: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/

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

      - name: Build Flutter Web (production)
        run: |
          flutter build web --release \
            --dart-define=SUPABASE_URL=${{ secrets.PROD_SUPABASE_URL }} \
            --dart-define=SUPABASE_ANON_KEY=${{ secrets.PROD_SUPABASE_ANON_KEY }} \
            --dart-define=GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL=${{ secrets.PROD_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL }} \
            --dart-define=GOOGLE_DRIVE_FOLDER_ID=${{ secrets.PROD_GOOGLE_DRIVE_FOLDER_ID }} \
            --dart-define=APP_ENV=production

      - name: Deploy to GitHub Pages (production)
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: build/web
          publish_branch: gh-pages

      - name: Build Android release APK
        run: |
          flutter build apk --release \
            --dart-define=SUPABASE_URL=${{ secrets.PROD_SUPABASE_URL }} \
            --dart-define=SUPABASE_ANON_KEY=${{ secrets.PROD_SUPABASE_ANON_KEY }} \
            --dart-define=GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL=${{ secrets.PROD_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL }} \
            --dart-define=GOOGLE_DRIVE_FOLDER_ID=${{ secrets.PROD_GOOGLE_DRIVE_FOLDER_ID }} \
            --dart-define=APP_ENV=production

      - name: Attach APK to GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: build/app/outputs/flutter-apk/app-release.apk
```

### 3. Commit and push

```bash
# From Code/mine-flow-app/:
git add .github/workflows/ci.yml
git commit -m "ci(STEP-42.5): add deploy-production job with manual approval gate"
git push
```

### 4. Dry-run the production gate

Create a GitHub Release as a **pre-release** (important: use pre-release so it is clearly test-only) with tag `v0.0.0-test`:
- GitHub repo → **Releases → Draft a new release**.
- Tag: `v0.0.0-test` (create new tag on `master`).
- Title: `STEP-42.5 gate dry-run — DO NOT USE`.
- Check **Set as a pre-release**.
- Click **Publish release**.

In GitHub Actions → observe the triggered workflow:
- `deploy-production` should appear with status **Waiting for approval**.
- Record a screenshot description or the exact status text shown.
- **Do NOT approve.** Click **Cancel** on the waiting job.

### 5. Clean up the test tag and release

In GitHub repo → **Releases** → find `v0.0.0-test` → **Delete release**.
Then delete the tag:
```bash
# From Code/mine-flow-app/:
git push origin --delete v0.0.0-test
git tag -d v0.0.0-test  # if it was created locally
```

Record that cleanup was done.

## Verification

- `production` GitHub Actions environment exists with at least 1 required reviewer.
- `deploy-production` job appears in `ci.yml` and is committed.
- Dry-run release triggered the job; job showed "Waiting for approval" status.
- Job was cancelled (not approved); no actual production deploy ran.
- Test tag `v0.0.0-test` and release deleted cleanly.
- `flutter analyze` still clean; `flutter test` still 434+ tests, 0 failures.

## Definition of done

- [ ] `production` GitHub Actions environment created with required reviewer gate.
- [ ] `deploy-production` job added to `ci.yml` and committed.
- [ ] Dry-run with `v0.0.0-test` pre-release confirmed gate blocks at "Waiting for approval".
- [ ] Test release and tag cleaned up.
- [ ] No actual production deploy ran.
- [ ] CI suite still green (no regressions).

## Next

After confirming the gate, start a fresh chat and run **substep 42.6**: `Upcoming Prompts/mine-flow-STEP-42.6-PROMPT.md`.
