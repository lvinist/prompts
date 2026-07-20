# mine-flow — STEP-3.2: Supabase Auth Edge Function & Flutter Auth Repository

> **How to run:** Tell your agent *"run substep 3.2"* (or *"read and run this file"*).

## Context
This is the second substep of [mine-flow-STEP-3-PLAN.md](file:///d:/AppDev/mine_flow/prompts/001-mvp/step-0003/mine-flow-STEP-3-PLAN.md).
In this substep, we implement the Supabase Edge Function `create-user` (allowing Supervisors to create accounts securely without public signup) and the Flutter Auth repository using `flutter_secure_storage` to persist tokens.

## Read these first
- [16-identity-auth.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/16-identity-auth.md) — Auth specification, Supervisor user creation, session token management
- [15-native-app-architecture.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/15-native-app-architecture.md) — Native app security, secure storage for tokens
- [12-test-strategy.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/12-test-strategy.md) — Testing strategy and mocking rules
- [README.md](file:///d:/AppDev/mine_flow/Code/mine-flow-app/README.md) — App repository structure

## Scope
- **In Scope:**
  - `supabase/functions/create-user/index.ts`: TypeScript Edge Function using Supabase Service Role client to create Auth users and insert profile into `public.users`. Verify request originates from an authenticated Supervisor.
  - `lib/features/auth/domain/repositories/auth_repository.dart`: Interface contract for Auth.
  - `lib/features/auth/data/repositories/auth_repository_impl.dart`: Supabase Auth implementation. Handles email/password sign-in, token storage via `flutter_secure_storage`, session recovery, and logout.
  - `lib/core/security/secure_storage_service.dart`: Encrypted secure storage wrapper for JWT tokens.
  - `test/integration/auth_repository_test.dart`: Unit & integration tests for Auth repository using `mocktail`.
- **Out of Scope:**
  - UI Auth login screens (handled in subsequent feature STEPs).

## Your task
1. Create `supabase/functions/create-user/index.ts`:
   - Validate auth header and check caller role == 'supervisor'.
   - Invoke `supabase.auth.admin.createUser()` with email, password, and user_metadata.
   - Insert corresponding user record into `public.users` table.
2. Implement `SecureStorageService` in `lib/core/security/secure_storage_service.dart` wrapping `FlutterSecureStorage`.
3. Implement `AuthRepository` and `AuthRepositoryImpl` in `lib/features/auth/`:
   - `signInWithEmailAndPassword({required String email, required String password})`
   - `signOut()`
   - `getCurrentUser()`
   - `createUser({required String email, required String password, required String role, required String fullName})` via Edge Function invocation.
4. Write test cases in `test/integration/auth_repository_test.dart` verifying sign-in, token persistence, error handling (invalid credentials), and user creation.

## Verification
- Run test suite: `flutter test test/integration/auth_repository_test.dart` inside `d:/AppDev/mine_flow/Code/mine-flow-app/`.
- Ensure secure storage keys are documented in `.env.example`.

## Keeping the docs true
- Ensure [16-identity-auth.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/16-identity-auth.md) matches implementation details.

## Definition of done
- [x] Supabase Edge Function `create-user/index.ts` created and validated.
- [x] `SecureStorageService` implemented wrapping `flutter_secure_storage`.
- [x] `AuthRepository` and `AuthRepositoryImpl` implemented with error handling.
- [x] Unit/Integration tests passing for `AuthRepository`.

## Next
Update status in STEP-3 PLAN, then tell the user to proceed to *"run substep 3.3"* in a fresh chat.
