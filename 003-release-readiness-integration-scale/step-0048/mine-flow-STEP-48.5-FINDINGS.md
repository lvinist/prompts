# STEP 48.5: Cut/Fill & Land Clearing Runtime Evidence

## Runtime Verdict
- **Cut/Fill (cut_fill_journey_test.dart)**: Verified. The test executes successfully.
- **Land Clearing (land_clearing_journey_test.dart)**: Verified. The test executes successfully.

**Run URL:** https://github.com/lvinist/mine-flow-app/actions/runs/33257726437
**Counts:** 10/10 tests passed (Web/Android suites green).

## Volume Semantics Findings
Verified explicitly against ADR-0012:
- **Persistence (Staging)**: The application successfully persists cm_volume and lcm_volume to staging using the corrected semantics, bypassing the legacy cut_volume_m3 and ill_volume_m3 completely for new entries.
- **In-App Display**: The application correctly calculates and displays 
etVolume utilizing the VolumeNormalizer.bankEquivalent logic (BCM + LCM / (1 + swell)), effectively reflecting the ADR-0012 bank-equivalent net instead of the meaningless cut - fill.
- **Zero-and-Negative Elevation Guards (CF-035/040)**: The form correctly handles negative elevation input (-2.5) which is allowed and saved successfully. Zero and negative volume values are correctly caught by the form validation guard (ecord.bcmVolume <= 0 && record.lcmVolume <= 0), rejecting invalid inputs cleanly.
- **RISK-0014 Accuracy**: The reporting path still queries legacy cut_volume_m3/ill_volume_m3 values, indicating that RISK-0014 is still open and accurate. This is deliberately deferred to the reporting step (48.14) and no assertions were falsely created to claim otherwise.

## Defects & Test Adjustments
- The journey tests required no major modifications as they already correctly target the Volume (BCM) and Volume (LCM) editable text fields in line with STEP-38 changes.
- lutter format fixes were pushed for ttendance_screen.dart which had formatting drift causing CI checks to fail upstream of the E2E jobs.
