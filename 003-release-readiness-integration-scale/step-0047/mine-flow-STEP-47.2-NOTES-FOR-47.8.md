# Notes for 47.8 from 47.2

- **CF-078 behaviour change (user-visible):** the Data Bucket upload screen now asks the user to
  pick a file **once** instead of twice. STEP-46's CF-078 remediation enforced the 50 MB cap by
  calling `FilePicker.pickFiles(withData: false)` for metadata and then a *second* time with
  `withData: true` for the bytes — a `file_picker` 11 workaround for having no lazy size read.
  `file_picker` 12 supplies `PlatformFile.length()` and `readAsBytes()`, so one `pickFile()` call
  now covers both. **CF-078's intent is preserved** (an oversized file is never read into memory)
  and the cap value, the Indonesian message *"File terlalu besar (maks 50 MB)."*, and the
  destructive-colour toast are byte-identical. Record this in the STEP record so the single pick is
  not later mistaken for a regression against the audit.
- **Internal contract narrowed:** `_UploadFileFormState._fileBytes` was tightened from
  `List<int>?` to `Uint8List?` (what `readAsBytes()` returns). `DataBucketUploadCubit.uploadFile`
  and `GoogleDriveService.uploadFile` still take `required List<int> bytes` — **their signatures
  were not changed**; `Uint8List` satisfies them. New state field `_selectedFileSize` (`int?`)
  holds the size captured at pick time, because `PlatformFile.size` no longer exists and `build`
  cannot `await length()`.
- **No architecture/ADR impact.** Implementation-level dependency migration only; no
  `architecture/*` doc edit and no ADR from this substep.
- **Test-mocking note worth carrying into Doc 12 if it documents mocking boundaries:** the picker
  is mocked at `FilePickerPlatform.instance`, but with a *hand-rolled* `FilePickerPlatform`
  subclass rather than a `mocktail` mock. A `mocktail` mock needs
  `MockPlatformInterfaceMixin` from `plugin_platform_interface`, and a `PlatformFile` fake's
  `xFile` override needs `cross_file` — both are transitive-only packages here, so importing them
  trips `depend_on_referenced_packages` under `flutter_lints` 6. Extending the real
  `FilePickerPlatform` passes `PlatformInterface.verifyToken` through its own constructor and keeps
  the test dependency-clean. (`xFile` is unused by the screen, so the fake's override throws.)
