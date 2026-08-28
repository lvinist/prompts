# mine-flow — STEP-45.8: Data Bucket E2E + real Drive upload + large-file behavior (NR-004 / NR-005)

**Recommended model:** Gemini 3.1 Pro (real Drive auth, abandon/cancel behavior, size-guard tuning — code + product decisions).

> **How to run:** *"run substep 45.8"*. Self-contained; runnable cold.

## Context

Data Bucket journey plus resolution of **NR-004** (real authenticated Google Drive upload + abandon/
cancel behavior) and **NR-005** (large-file OOM threshold on a mid-range device). Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md` (Q4 — Drive service-account creds). Runtime findings
here may add a cancel affordance and tune the file-size guard — surface options to the user first.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md` — Q4.
- `Code/mine-flow-app/lib/features/data_bucket/` and `lib/core/network/google_drive_service.dart`.
- `Code/mine-flow-app/lib/features/data_bucket/presentation/pages/upload_file_page.dart`.
- STEP-46 findings — **NR-004** (real Drive upload + abandon), **NR-005** (large-file OOM),
  CF-018 (empty-credential Drive fallback — fixed statically in 46.4), CF-078 (no file-size limit;
  retry re-uploads), CF-045 (zone required but never validated) — confirm at runtime.

## Scope

Owns `integration_test/journeys/data_bucket_journey_test.dart` and any `upload_file_page`/service
change that NR-004/005 warrant (cancel affordance, size-guard tuning).

## Your task

1. **Drive wiring (NR-004):** confirm the upload path resolves a real `driveService` from
   `appServices` (CF-018 fix) rather than empty creds. With staging Drive creds (Q4), upload a real
   file on **Android** and **web**; assert the record + Drive state after a successful upload.
2. **Abandon/cancel (NR-004):** trigger back/close mid-upload; confirm the record/Drive state and
   decide whether a cancel affordance (PopScope + CancelToken) is warranted. If yes, implement it
   (present to user first) with a test.
3. **Large-file ceiling (NR-005):** on `Pixel_6a`, attempt uploads of increasing size to find the
   practical `withData: true` ceiling; set the CF-078 size guard accordingly (present the chosen
   limit to the user).
4. If Drive creds are unavailable (Q4), mark NR-004/005 **Unverified** with the reason — do not
   fabricate an upload result.

## Verification
- Data-bucket journey passes on Chrome + `Pixel_6a` (or Unverified w/ reason).
- Any cancel/size-guard change has a test.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch.

## Keeping the docs true (always)
- Record NR-004/005 outcome (resolved w/ code + limit, or carried-forward risk) for 45.15. A size
  guard limit chosen from measurement may warrant a risk-register note.

## Definition of done
- [ ] Data-bucket journey passes (or Unverified w/ reason) on both platforms.
- [ ] NR-004 (real upload + abandon) and NR-005 (large-file ceiling + guard) resolved or carried forward.
- [ ] analyze 0 / format clean; files documented.

## Next
Run substep 45.9 (Reporting / PDF E2E over a real dataset) in a fresh chat.
