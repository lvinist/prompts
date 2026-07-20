# mine-flow — STEP-8.2: Google Drive Integration Service

> **How to run:** Tell your agent _"run substep 8.2"_ (or _"read and run this file"_).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is the second substep of **STEP-8 (Data Bucket Integration)**. It builds the **Google Drive integration service** — a reusable core service that handles service-account-based authentication to the Google Drive API, file upload with progress tracking, file lookup/search, and graceful error handling for Drive outages. This service lives in `lib/core/network/` (shared infrastructure, not feature-specific), so the Data Bucket and any future feature can use it.

Substep 8.1 created the `GeospatialFile` entity and data layer. This substep gives the app the ability to actually upload files to Drive and get back the file ID/link needed to populate a `GeospatialFile` record.

## Read these first

- root `.throughstone/local-user.md` — active user's experience level (Level 2) and communication style (Explanatory); if missing, ask the two local-profile questions from `BOOTSTRAP-PROMPT.md` Stage 0, create it, and calibrate explanations/questions to it
- `Code/mine-flow-docs/architecture/08-infrastructure-deployment.md` — notes that geospatial files are stored on Google Drive via standard Google APIs
- `Code/mine-flow-docs/architecture/11-interface-contracts.md` — App ↔ Google Drive boundary uses the official `googleapis` Dart package
- `Code/mine-flow-docs/architecture/06-security-threat-model.md` — secrets (service account key) must be kept out of the repo; Drive outage is a known risk with graceful degradation
- Existing core services for pattern reference: `lib/core/network/` for network utilities, `lib/core/constants/`, `lib/core/security/` for secrets handling
- `lib/core/offline/` for the `SyncQueueManager` reference (used in the graceful degradation pattern)

## Scope

**Owns:**

- **`lib/core/network/google_drive_service.dart`** — the Drive service client.
**EXTENSIVE REQUIREMENT**:
- Use `googleapis_auth` and `googleapis` correctly for Service Account authentication using `.env` variables or securely loaded keys.
- **Resumable uploads for heavy files**: Heavy geospatial files (.tiff) can be huge. You must chunk or handle uploads reliably using `Media(stream, length)` rather than reading the entire file into memory at once.
- Implement a `Stream` based progress callback or use appropriate `googleapis` parameters if available to track upload progress.
- Strictly implement error handling for network failures. Wrap the Google APIs in a try-catch and throw domain-specific exceptions.
- File upload method with optional progress callback
- File search/lookup by name or folder
- Graceful degradation on Drive API failure (custom exception types, never crash)

**Does NOT touch:**

- The Data Bucket feature's UI or BLoC (substep 8.3)
- The Data Bucket repository or data layer (substep 8.1)
- SyncQueueManager bindings (substep 8.4)
- Any existing features or core modules

## Your task

### 1. Add dependencies

Add the following packages to `pubspec.yaml` (check for existing entries first):

- `googleapis` — Dart client library for Google APIs (specifically the Drive v3 API)
- `googleapis_auth` — Auth helpers for service accounts (client-side)

Run `flutter pub get` after updating `pubspec.yaml`.

### 2. Create the Drive service

Create `lib/core/network/google_drive_service.dart` with:

```dart
import 'package:googleapis/drive/v3.dart' as drive;
import 'package:googleapis_auth/googleapis_auth.dart' as auth;
// ... other imports

/// Service for interacting with Google Drive API using a service account.
///
/// Authenticates via service account credentials (loaded from .env or secure
/// storage), then provides upload, lookup, and search operations.
/// All methods handle failures gracefully — returning null or throwing typed
/// exceptions rather than raw API errors, so callers never crash.
class GoogleDriveService {
  // Configuration
  final String _serviceAccountEmail;   // from .env
  final String _serviceAccountKey;     // from .env (the private key)
  final String _driveFolderId;         // the shared Drive folder to upload into

  drive.DriveApi? _driveApi;

  GoogleDriveService({
    required String serviceAccountEmail,
    required String serviceAccountKey,
    required String driveFolderId,
  }) : _serviceAccountEmail = serviceAccountEmail,
       _serviceAccountKey = serviceAccountKey,
       _driveFolderId = driveFolderId;

  /// Initializes the Drive API client. Must be called before any other method.
  /// Returns true if authentication succeeded, false if it failed (caller can
  /// decide whether to retry or degrade).
  Future<bool> initialize() async { /* ... */ }

  /// Uploads a file to the configured Drive folder.
  ///
  /// [bytes] — the file content.
  /// [fileName] — the display name in Drive (including extension).
  /// [mimeType] — the MIME type (e.g., 'application/zip', 'image/tiff').
  /// [onProgress] — optional callback with (bytesSent, totalBytes).
  ///
  /// Returns the created [DriveFileResult] with fileId and webViewLink,
  /// or throws [DriveUploadException] on failure.
  Future<DriveFileResult> uploadFile({
    required List<int> bytes,
    required String fileName,
    required String mimeType,
    void Function(int sent, int total)? onProgress,
  }) async { /* ... */ }

  /// Looks up a file by its Drive file ID.
  Future<DriveFileResult?> getFile(String fileId) async { /* ... */ }

  /// Searches for files by name (case-insensitive contains) in the configured folder.
  Future<List<DriveFileResult>> searchFiles(String query) async { /* ... */ }

  /// Deletes a file from Drive by its file ID.
  Future<bool> deleteFile(String fileId) async { /* ... */ }

  /// Checks whether the Drive API is reachable (used by features to decide
  /// offline/online mode).
  Future<bool> get isOnline async { /* ... */ }
}

/// Result of a Drive file operation.
class DriveFileResult {
  final String fileId;
  final String name;
  final String webViewLink;
  final int? sizeBytes;
  final String? mimeType;
  final DateTime? createdTime;
}

/// Thrown when a Drive upload fails (network, auth, quota, etc.).
class DriveUploadException implements Exception {
  final String message;
  final String? details;
}
```

**Implementation details:**

- **Auth flow:** Load the service account email and private key from environment config (`.env` → `dotenv` package, which should already be a dependency). Create `ServiceAccountCredentials` using `auth.ServiceAccountCredentials.fromJson()` or constructing it manually from the email/key. Use `auth.clientViaServiceAccount()` to get an authenticated HTTP client, then instantiate `drive.DriveApi(client)`.
- **Upload:** Use `drive.DriveApi.files.create()` with `uploadMedia` parameter for the file bytes. Use `UploadOptions()` with `resumable: true` for large files. Set `parents: [_driveFolderId]` to upload into the configured folder.
- **Progress:** For large file uploads, wrap the bytes in a stream and track chunks sent. The `googleapis` package supports `Media` with a stream for upload progress.
- **Error handling:** Wrap all API calls in try-catch. Catch `DetailedApiRequestError` and rethrow as `DriveUploadException` with a user-friendly message. On auth failure, return `false` from `initialize()`.
- **isOnline:** Try a lightweight Drive API call (e.g., `drive.AboutResource.get()` with `fields: 'user'`) to check connectivity. Return `true` if it succeeds, `false` otherwise.

### 3. Add environment configuration

Update `lib/core/constants/env_config.dart` (or the existing env config class) to include:

- `googleDriveServiceAccountEmail`
- `googleDriveServiceAccountKey`
- `googleDriveFolderId`

Update `.env.example` with these three new keys (with placeholder values and a comment explaining where to get them). **Never commit the actual `.env` file with real credentials.**

### 4. Update barrel exports

Ensure `lib/core/core.dart` or the appropriate core barrel file exports `google_drive_service.dart`.

## Verification

- **Write unit tests** for:
  - Service initialization (mock the auth client, verify `initialize()` returns `true`/`false` appropriately)
  - Upload method (mock `DriveApi`, verify the correct API call is made with expected parameters)
  - Error handling (mock a `DetailedApiRequestError`, verify it's caught and rethrown as `DriveUploadException`)
  - `isOnline` check (mock response from `AboutResource.get()`)
- **Name the test files:** `test/core/network/google_drive_service_test.dart`
- **Run:** `flutter test test/core/network/google_drive_service_test.dart`
- **Run timing:** Tests are collected in substep 8.4 for final verification; run them now to verify your work, but they're officially gated in 8.4.

## Keeping the docs true

- The `google_drive_service.dart` file is a new core component. If its public interface or error model becomes a formal contract, update `architecture/11-interface-contracts.md`.
- The service account authentication pattern is a security-relevant decision. If it departs from what's documented in `architecture/06-security-threat-model.md`, update that doc.
- If the Drive folder ID or service account setup requires a new operational step (beyond what's in `architecture/08-infrastructure-deployment.md`), add it there.

## Definition of done

- [ ] `googleapis` and `googleapis_auth` added to `pubspec.yaml` and `flutter pub get` passes
- [ ] `lib/core/network/google_drive_service.dart` created with full implementation (initialize, uploadFile, getFile, searchFiles, deleteFile, isOnline)
- [ ] `DriveFileResult` and `DriveUploadException` types defined
- [ ] Environment config updated with Drive service account fields; `.env.example` updated
- [ ] Unit tests written for initialization, upload, error handling, and connectivity check
- [ ] Any architecture doc changes reflected

## Next

When this substep is done, update its status in the STEP-8 PLAN, then run **substep 8.3** — _"run substep 8.3"_ — in a fresh chat. (STEP-8 PLAN: `Upcoming Prompts/mine-flow-STEP-8-PLAN.md`)
