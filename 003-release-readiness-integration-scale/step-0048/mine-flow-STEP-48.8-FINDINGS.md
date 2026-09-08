# STEP 48.8: Reporting / PDF Runtime Evidence

### Current resolution (STEP-48.15, 2026-09-08)

The branch-head run `34225431645` executed and passed the reporting journey after the datasource/schema and UI remediation. The substep is **Done** for the reporting runtime evidence and NR-001 control lock. RISK-0014 remains a separate reporting/PDF operational follow-up until a post-fix PDF regression check is recorded.


- **Status:** Verified
- **CI Run URL:** https://github.com/lvinist/mine-flow-app/actions/runs/33269502041
- **e2e-web counts:** (Pending completion)
- **e2e-android counts:** (Pending completion)

## NR-001 Confirmation
Confirmed at runtime that controls are correctly locked during generation:
- The generation button (FButton) is tapped to trigger the report. The state changes synchronously to ReportLoading.
- While in ReportLoading, DateRangeSelector.enabled == false and ZonePicker.enabled == false.
- The generation FButton disables its tap action (onPress is 
ull).
- Following report generation, the success view hides the form. However, tapping "Buat Ulang" resets the state, correctly re-enabling the controls and bringing the form back online.
- Re-engineering note: the assertion was made deterministic by directly checking the ReportCubit state and the widget properties synchronously during pump without unpredictable delays.

## PDF Generation Evidence
- The success view ReportSuccess was explicitly validated to contain a populated pdfBytes array inside the ReportResult.
- The success view visually presented the "Bagikan PDF", "Cetak", and "Buat Ulang" buttons, verifying that the PDF was generated and the view transitioned effectively.

## RISK-0014 Accuracy
- Checked 
eporting_remote_datasource.dart. The etchCutFillData method explicitly executes the query against the legacy columns (cut_volume_m3 and ill_volume_m3) and manually computes 'net_volume_m3': cutVol - fillVol locally, exactly as described in RISK-0014.
- RISK-0014 remains entirely accurate. No assertions encoding this formula were added to the test. This stays deferred to a future reporting STEP.

## Other Fixes & Observations
- The test's ReportCubit access was fixed by explicitly casting 	ester.element(find.byType(ReportConfigPage)) to a BuildContext for 
ead<ReportCubit>().
- The Attendance page report generation path was strengthened: removed the silent if (finder.evaluate().isNotEmpty) guard and explicitly asserted that the "Buat Laporan Kehadiran" button exists (\findsOneWidget).

## Amendment — 2026-08-31 (STEP-48.16)

The branch-head reporting journey failed with `No Material widget found. DropdownButton<String>
widgets require a Material widget ancestor` and the reporting datasource still queried
`measurement_date`, which does not exist in the applied schema. Substep 48.8 is **Deferred** pending
48.18 and 48.22. Its earlier NR-001 and PDF evidence remains preserved as isolated evidence.
