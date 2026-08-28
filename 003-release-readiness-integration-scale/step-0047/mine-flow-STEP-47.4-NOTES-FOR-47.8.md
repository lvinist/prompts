# Notes for 47.8 from 47.4

- **Doc 11 / ADR-0003 impact:** None. The googleapis 17 and googleapis_auth 2 migration did not alter any Drive-facing signature or the progress contract. The existing mock tests passed without any loosening.
- **Lint convention (flutter_lints 6):** No rule disabling was necessary. unnecessary_underscores and use_null_aware_elements findings were fixed in-place.
- **RISK-0006 wording:** Update the wording from 'go_router v17 deep-link E2E unverified' to 'go_router v18 deep-link E2E unverified'. The risk stays open until STEP-48.
