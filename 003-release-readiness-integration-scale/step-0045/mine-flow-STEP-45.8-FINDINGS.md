# STEP-45.8 Findings

- **NR-004 (real upload + abandon):** Unverified. Carried-forward risk due to lack of Staging Google Drive credentials (`STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL` absent). Could not test real upload or abandon/cancel behavior on staging.
- **NR-005 (large-file ceiling + guard):** Unverified. Carried-forward risk due to lack of Staging Google Drive credentials. Could not find the practical large-file ceiling on `Pixel_6a`. The existing CF-078 limit of 50MB is retained without empirical tuning.

These outcomes should be reconciled in 45.15 and likely added to `registries/risks.yml`.
