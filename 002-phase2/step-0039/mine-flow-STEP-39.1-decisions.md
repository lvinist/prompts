# Phase 2 Tier 2 Check-in (STEP-39.1) Locked Decisions and Inventory

## 1. Locked Owner Decisions
The following architectural decisions have been explicitly approved by the owner and are locked for implementation:
- **Typography**: The usage of the `Geist` font is approved.
- **Mobile Navigation**: The 5 permanently visible items (without a kebab menu) are approved.
- **Low-Battery Operating Rule**: The "Hybrid" approach is approved. The app will pause automatic background sync if OS Battery Saver is ON **OR** raw battery is `<= 20%`.

## 2. Affected-Document and Dependency Inventory for Substep 39.2
The following files and dependencies will be modified in Substep 39.2 to reconcile the architecture with the implementation and explicitly approved decisions:

### Architecture Documents
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`: Must be updated to reflect the `Geist` font and 5-item mobile navigation decisions. Needs a Version Log bump.
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`: Must be updated to explicitly define the "Hybrid" low-battery sync rule (Battery Saver OR <= 20%). Needs a Version Log bump.

### ADRs
- `Code/mine-flow-docs/adr/ADR-0009-ui-design-system-drift.md`: A new Accepted ADR must be created detailing the approval of the `Geist` font and 5-item mobile nav drift. *(Note: ADR-0009 reservation and creation belongs to Substep 39.2 and has not yet occurred.)*

### Registries
- `Code/mine-flow-docs/registries/risks.yml`: Needs review and potential update regarding the accepted drift or battery sync changes.

### Dependencies
- `Code/mine-flow-app/pubspec.yaml`: The `battery_plus` package will be added (after supply-chain review) to support the low-battery rule.

### Generated Bridge Files
- `DESIGN.md`: Must be regenerated to reflect updates to `07-ui-design-system.md`.
- `PRODUCT.md`: Must be regenerated if applicable.

## 3. Baseline Status & Test Evidence

### Invalid Interrupted Run
An initial combined test run `flutter test test/features/tracking/presentation/inventory_dashboard_screen_test.dart test/features/data_bucket/presentation/pages/data_bucket_list_page_test.dart test/widget/equipment_check_form_test.dart` was executed but hung due to a known semantics issue. It was manually terminated without producing a reliable final exit code or result count. Combining the semantics-crashing test with the stale-expectation tests was an invalid isolation strategy.

### Isolated Test Results

#### 1. Inventory Dashboard Screen
**Command**: `flutter test test/features/tracking/presentation/inventory_dashboard_screen_test.dart --reporter expanded`
- **Working Directory**: `Code/mine-flow-app`
- **Exit Code**: 1
- **Passed/Failed/Crashed**: 1 Failed (0 Passed, 0 Crashed)
- **First Relevant Failure**: `Expected: exactly one matching candidate. Actual: _KeyWidgetFinder:<Found 0 widgets with key [<'create_new_inventory_appbar_button'>]: []>`
- **Terminated Normally**: Yes
- **Elapsed Time**: ~2s

#### 2. Data Bucket List Page
**Command**: `flutter test test/features/data_bucket/presentation/pages/data_bucket_list_page_test.dart --reporter expanded`
- **Working Directory**: `Code/mine-flow-app`
- **Exit Code**: 1
- **Passed/Failed/Crashed**: 1 Failed (0 Passed, 0 Crashed)
- **First Relevant Failure**: `Expected: exactly one matching candidate. Actual: _KeyWidgetFinder:<Found 0 widgets with key [<'upload_file_appbar_button'>]: []>`
- **Terminated Normally**: Yes
- **Elapsed Time**: ~2s

#### 3. Equipment Check Form
**Command**: `flutter test test/widget/equipment_check_form_test.dart --reporter expanded`
- **Working Directory**: `Code/mine-flow-app`
- **Exit Code**: N/A (Manually Terminated)
- **Passed/Failed/Crashed**: Hung/Crashed
- **First Relevant Failure**: The test hung at `EquipmentCheckFormScreen Widget Tests should render equipment tabs, check type toggle, summary badge, and SOP cards` and was manually terminated.
- **Terminated Normally**: No
- **Elapsed Time**: N/A
- **Stack Trace** (from prior run):
  ```
  _RenderObjectSemantics.debugCheckForParentData.debugCheckParentDataNotDirty (package:flutter/src/rendering/object.dart:5706:42)
  List.forEach (dart:core-patch/growable_array.dart:428:8)
  _RenderObjectSemantics.debugCheckForParentData.debugCheckParentDataNotDirty (package:flutter/src/rendering/object.dart:5706:42)
  List.forEach (dart:core-patch/growable_array.dart:428:8)
  ...
  _RenderObjectSemantics.debugCheckForParentData (package:flutter/src/rendering/object.dart:5709:5)
  PipelineOwner.flushSemantics.<anonymous closure> (package:flutter/src/rendering/object.dart:1498:34)
  PipelineOwner.flushSemantics (package:flutter/src/rendering/object.dart:1501:8)
  PipelineOwner.flushSemantics (package:flutter/src/rendering/object.dart:1653:15)
  AutomatedTestWidgetsFlutterBinding.drawFrame (package:flutter_test/src/binding.dart:2444:35)
  RendererBinding._handlePersistentFrameCallback (package:flutter/src/rendering/binding.dart:509:5)
  SchedulerBinding._invokeFrameCallback (package:flutter/src/scheduler/binding.dart:1430:15)
  SchedulerBinding.handleDrawFrame (package:flutter/src/scheduler/binding.dart:1345:9)
  ```
*(Diagnosis is deferred to Substep 39.4).*

## 4. Branch & Reservation Verification
- **STEP-39 Reservation Commit**: Verified (Commit `e7b97c4... reserve STEP-39`).
- **Push Status**: Verified (Pushed to origin, `prompts` is up to date).
- **Branch Status**: Verified as `step-0039-check-in` in `Code/mine-flow-docs`, `Code/mine-flow-app`, and `prompts`.
- **STEP-index Status**: Verified (`| 39 | Phase 2 Tier 2 Check-in... | In progress |`).
- **ADR-0009 Reservation Status**: Reservation belongs to Substep 39.2 and has not yet occurred.
