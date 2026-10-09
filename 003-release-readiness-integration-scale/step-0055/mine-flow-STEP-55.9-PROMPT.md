# mine-flow — STEP-55.9: Data Bucket and Timeline Cohesion

> **How to run:** Tell your agent “run substep 55.9”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** Existing upload/detail routes and explicit preservation decisions make this a mechanical migration with clear retry/cancel and no-report boundaries.

## Context
Make Data Bucket’s existing GoRouter routes authoritative, migrate upload/detail to shared platform surfaces, and preserve Work Timeline as read-only. Neither feature gains reporting.

## Read first
STEP-55 PLAN; prior findings; master spec §§2, 4.8, 5–7; Doc 07; Docs 11/12/15; Data Bucket and Timeline presentation/BLoC/domain/data files, Drive service, router/tests; STEP-54.9 findings and Drive risks.

## Impeccable
Run context once. Use `harden` for retry/cancel/Drive-unavailable/large-file/partial-upload states, native `adapt` for upload sheet and inspector, `layout` for file metadata/timeline density, then bounded `polish`.

## Task
- Replace Data Bucket `MaterialPageRoute` callers with authoritative `/tools/data-bucket/upload` and `/tools/data-bucket/:id`; cold detail fetches by ID and preserves list filter/scroll/refresh.
- Migrate upload to responsive sheet; selected file/date/metadata create dirty state; all dismissals use D4.
- While busy, provide labelled `Batalkan Unggahan`, define confirmation/partial-transfer cleanup/retry truth, and do not misuse dirty dialog.
- Preserve selected bytes on retry and existing 50MB/human-readable size behavior.
- Convert detail to Web right inspector and Android bottom inspector; explicit Open in Drive/Delete actions.
- Keep Work Timeline read-only, without create/detail routes or fake report action. Keep both features report-free.
- Replace Data Bucket FAB/date decorator and Timeline `InkWell` with shared/ForUI controls where actionable.

## Tests and verification
Cover caller URL use, cold detail without extra, not-found/unauthorized, list state/focus; upload dirty state, cancel before/during/after partial transfer, cleanup failure, retry bytes, 50MB boundaries, double submit, Drive unavailable; detail platform shape/actions/delete guard; Timeline read-only/no routes/no reports; keyboard/semantics/48dp/themes. Mock Drive externally; never transmit real files in unit tests.

Run focused Data Bucket/Timeline/router/shared suites, format/analyze/guards, and bounded Web/Pixel_6a checks where safe. Produce `mine-flow-STEP-55.9-FINDINGS.md` tracing `FC-54.9-001..010` and Drive residuals.

## Boundaries
No milestone creation, Timeline/Data Bucket report, arbitrary Drive production request, or false cancellation/cleanup claim. Escalate if API cannot cancel honestly, partial upload semantics are unknown, or repeated failure occurs.

## Definition of done
Data Bucket routes/sheet/inspector/cancel/retry are truthful and tested; Timeline remains intentionally read-only/report-free; platform polish evidence is recorded.

## Next
Run substep 55.10 in a fresh chat.
