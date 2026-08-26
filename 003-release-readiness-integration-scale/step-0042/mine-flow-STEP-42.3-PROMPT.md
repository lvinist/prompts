# mine-flow — STEP-42.3: Staging GCP Service Account & GitHub Secrets

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-42.3-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-42.2 committed the generated Dart types and hardened the contract guard. This substep creates a fully separate GCP service account for staging (decision locked: separate account, not shared with production), configures it with Drive API access, and sets all `STAGING_*` GitHub Secrets so the CI test job and future deploy jobs can run authenticated.

**Known state (as of completion of 42.2):**
- `lib/core/data/models/generated/database.dart` committed.
- Contract guard hardened — exits 0 on full enforcement pass.
- GitHub Secrets `STAGING_SUPABASE_URL`, `STAGING_SUPABASE_ANON_KEY`, and the Google Drive staging secrets are **not yet set**.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/.env.example` ← for the full list of required keys
- `Code/mine-flow-docs/architecture/08-infrastructure-deployment.md`
- `Code/mine-flow-docs/architecture/09-environments.md`

## Scope

**Own:** Create staging GCP service account; download JSON key; create staging Drive folder; set all `STAGING_*` GitHub Secrets; update `.env.example`; confirm CI `test` job passes green.

**Do not:** Create or touch any production secrets. Change application code or CI job definitions (those are substeps 42.4/42.5). Share the staging service account key file in any committed file.

## Your task

This substep is **primarily ClickOps**. Document each step clearly as you go — these exact steps will be transcribed into `runbooks/staging-provision.md` in substep 42.7.

### 1. Create a staging Google Drive folder

In Google Drive, create a new folder named `mine-flow-staging` (or similar). Note its **folder ID** from the URL:
`https://drive.google.com/drive/folders/<FOLDER_ID>`

### 2. Create the staging GCP service account

In [Google Cloud Console](https://console.cloud.google.com/):
1. Select your GCP project (the same project that hosts production Drive access, or a new one — your choice).
2. Navigate to **IAM & Admin → Service Accounts → Create Service Account**.
3. Name: `mine-flow-staging` (display name). ID: `mine-flow-staging`.
4. Skip optional role grant (access is granted via Drive folder sharing, not IAM roles).
5. Click **Done**.
6. Click on the new service account → **Keys** tab → **Add Key → Create new key → JSON**. Download the JSON file to a **local, non-repo location** (never commit it).

### 3. Enable the Google Drive API (if not already)

In **APIs & Services → Enabled APIs**, confirm `Google Drive API` is enabled. Enable it if not.

### 4. Grant the service account access to the staging Drive folder

In Google Drive:
- Right-click the `mine-flow-staging` folder → **Share**.
- Add the service account email (from the JSON key file: `client_email` field) as **Editor**.
- Click **Send / Done**.

### 5. Extract credentials from the JSON key file

From the downloaded JSON key file, extract:
- `client_email` → this is `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL`
- `private_key` → this is `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY` (the full multi-line PEM key)

Do not paste these values into any file visible to the agent. Handle them only via the GitHub Secrets UI.

### 6. Set GitHub Secrets

In the GitHub repository → **Settings → Secrets and variables → Actions → New repository secret**, add:

| Secret name | Value |
|-------------|-------|
| `STAGING_SUPABASE_URL` | Staging project URL (Supabase Dashboard → Project Settings → API → Project URL) |
| `STAGING_SUPABASE_ANON_KEY` | Staging anon key (Supabase Dashboard → Project Settings → API → anon public) |
| `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL` | `client_email` from the staging JSON key |
| `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY` | `private_key` from the staging JSON key (full PEM block) |
| `STAGING_GOOGLE_DRIVE_FOLDER_ID` | The folder ID from step 1 |

### 7. Update `.env.example`

Add the following to `Code/mine-flow-app/.env.example` in a new section:

```
# Supabase CLI project reference (used by `supabase link`)
# Find it: Supabase Dashboard -> Project Settings -> General -> Reference ID
SUPABASE_PROJECT_REF=

# ---------------------------------------------------------------------------
# Staging CI secrets (set in GitHub repo Settings -> Secrets and variables -> Actions)
# These are injected by the deploy-staging GitHub Actions job -- not used locally.
# ---------------------------------------------------------------------------
# STAGING_SUPABASE_URL=
# STAGING_SUPABASE_ANON_KEY=
# STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL=
# STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY=
# STAGING_GOOGLE_DRIVE_FOLDER_ID=
```

### 8. Trigger CI and confirm the test job passes

Push the `.env.example` change to `step-0042-staging-pipeline`:

```bash
# From Code/mine-flow-app/:
git add .env.example
git commit -m "docs(STEP-42.3): add SUPABASE_PROJECT_REF and STAGING_* keys to .env.example"
git push
```

In GitHub Actions, observe the `ci` workflow run triggered by this push. Confirm the `test` job passes green (the `STAGING_SUPABASE_URL` and `STAGING_SUPABASE_ANON_KEY` secrets are now populated so Supabase-touching tests can resolve).

Record the run URL and pass/fail status.

## Verification

- GitHub Secrets UI shows all 5 `STAGING_*` secrets set (you can see the names, not the values).
- CI `test` job passes green on the pushed commit.
- `.env.example` documents `SUPABASE_PROJECT_REF` and the `STAGING_*` comment block; no real values committed.
- Staging Drive folder exists; service account email has Editor access.
- No JSON key file or private key value appears in any committed file.

## Definition of done

- [ ] Staging GCP service account created with Drive API access.
- [ ] Staging Drive folder created; service account email granted Editor access.
- [ ] All 5 `STAGING_*` GitHub Secrets set.
- [ ] `.env.example` updated with `SUPABASE_PROJECT_REF` and `STAGING_*` comment block; committed.
- [ ] CI `test` job confirmed green on push; run URL recorded.

## Next

After confirming CI green, start a fresh chat and run **substep 42.4**: `Upcoming Prompts/mine-flow-STEP-42.4-PROMPT.md`.
