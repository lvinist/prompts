# mine-flow — STEP-35.3: Settings Page UI Shell & Integrations

> **How to run:** Tell your agent *"run substep 35.3"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
This is substep 35.3 of STEP-35 (Settings Page Feature). We now have the State Management and App wiring in place. This substep implements the actual `SettingsPage` UI using ForUI components to match the Phase 2 `shadcn-admin` styling, and integrates it into the app's routing system.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-35-PLAN.md` (the STEP PLAN)
- `architecture/07-ui-design-system.md`
- `mine-flow-app/lib/app/router.dart`

## Scope
This substep owns the presentation UI code (`SettingsPage`) and the router updates.

## Your task
1. Create `SettingsPage` in `lib/features/settings/presentation/pages/settings_page.dart`.
2. Build the UI using `forui` widgets (`FScaffold`, `FCard`, `FButton`, etc.) per the `shadcn-admin` design language.
   - **Profile Section:** Display current user's Name and Role (fetched from Auth state).
   - **Preferences Section:** 
     - A combobox or segmented control to select Language (English / Indonesian).
     - A combobox or segmented control to select Theme (Light / Dark / System).
   - **Support Section:** Add buttons linking to `alvin.geomatics@gmail.com` and WhatsApp `wa.me/+6285156042854`. Use `url_launcher` if available, or just scaffold the action.
   - **Logout Section:** A destructive action button triggering the `AuthBloc`'s logout event.
3. Update `lib/app/router.dart`:
   - Add a route for `/settings`.
   - Ensure the user can navigate to the Settings page (e.g., via the app shell's sidebar or bottom nav, or header avatar).
4. Connect the UI controls to call methods on the `SettingsCubit` created in 35.2.

## Verification
- Tests are deferred to the final verification substep (35.4).
- Run `flutter analyze` to ensure there are no syntax or lint errors.

## Definition of done
- [ ] `SettingsPage` UI built using ForUI.
- [ ] Theme, Language, Profile, Support, and Logout sections are fully wired up to their respective logic.
- [ ] Navigation routing updated.
- [ ] Analyzer passes cleanly on the modified files.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 35.4"*, in a **fresh chat**.
