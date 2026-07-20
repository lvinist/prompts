# mine-flow — STEP-9.4: In-App Notification System

> **How to run:** Tell your agent *"run substep 9.4"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is **STEP-9** (Tier 3 - Reporting, Timeline & Polish), substep **9.4**.
**Goal:** Deliver a rule-based in-app notification system (no push/FCM). This fulfills Launch Criterion LC-4 ("In-app notifications functional for at least equipment check reminders").

## Scope

**This substep owns:**
1. Creating Notification Domain: `app_notification.dart`, `notification_repository.dart`.
2. Creating Notification Data: `notification_rule_engine.dart`, Hive models (Type IDs 15, 16, 17), `notification_local_datasource.dart`, `notification_repository_impl.dart`.
3. Creating Notification Presentation: Cubit, `notification_list_page.dart`, `notification_banner.dart` (critical alerts), `notification_badge.dart`.

## Your task

### Task 1: Notification Domain

**File: `lib/features/notifications/domain/entities/app_notification.dart`**
```dart
import 'package:equatable/equatable.dart';

enum NotificationType { equipmentCheckReminder, lowInventory, missingAttendance, overdueMilestone }
enum NotificationSeverity { info, warning, critical }

class AppNotification extends Equatable {
  final String id;
  final String title;
  final String message;
  final NotificationType type;
  final NotificationSeverity severity;
  final bool isRead;
  final bool isDismissed;
  final DateTime createdAt;
  final DateTime? expiresAt;
  final Map<String, dynamic>? metadata;

  const AppNotification({
    required this.id,
    required this.title,
    required this.message,
    required this.type,
    required this.severity,
    this.isRead = false,
    this.isDismissed = false,
    required this.createdAt,
    this.expiresAt,
    this.metadata,
  });

  AppNotification copyWith({
    String? id,
    String? title,
    String? message,
    NotificationType? type,
    NotificationSeverity? severity,
    bool? isRead,
    bool? isDismissed,
    DateTime? createdAt,
    DateTime? expiresAt,
    Map<String, dynamic>? metadata,
  }) {
    return AppNotification(
      id: id ?? this.id,
      title: title ?? this.title,
      message: message ?? this.message,
      type: type ?? this.type,
      severity: severity ?? this.severity,
      isRead: isRead ?? this.isRead,
      isDismissed: isDismissed ?? this.isDismissed,
      createdAt: createdAt ?? this.createdAt,
      expiresAt: expiresAt ?? this.expiresAt,
      metadata: metadata ?? this.metadata,
    );
  }

  @override
  List<Object?> get props => [
        id, title, message, type, severity, isRead,
        isDismissed, createdAt, expiresAt, metadata,
      ];
}
```

**File: `lib/features/notifications/domain/repositories/notification_repository.dart`**
```dart
import 'package:mine_flow/features/notifications/domain/entities/app_notification.dart';

abstract class NotificationRepository {
  Future<List<AppNotification>> getActiveNotifications();
  Future<void> markAsRead(String id);
  Future<void> dismiss(String id);
  Future<void> dismissAll();
  Future<int> getUnreadCount();
  Future<List<AppNotification>> checkAndGenerateNotifications({required String siteId});
}
```

### Task 2: Notification Data Layer & Rule Engine

**File: `lib/features/notifications/data/models/app_notification_model.dart`**
Create a manual Hive adapter (Type ID 15) for the model, mapping properties identically to `AppNotification`. (Keep it simple).

**File: `lib/features/notifications/data/services/notification_rule_engine.dart`**
```dart
import 'package:mine_flow/features/notifications/domain/entities/app_notification.dart';
import 'package:uuid/uuid.dart';

class NotificationRuleEngine {
  // In a real implementation, inject repositories (e.g. EquipmentCheckRepository) here.
  // For this step prompt, implement the checking logic based on local mock or provided repo queries.
  
  Future<List<AppNotification>> evaluateRules({required String siteId}) async {
    List<AppNotification> notifications = [];
    final now = DateTime.now();
    
    // Rule 1: Equipment Check Reminder (CRITICAL)
    // If after 3 PM and no post-work check today
    if (now.hour >= 15) {
      notifications.add(AppNotification(
        id: const Uuid().v4(),
        title: 'Peringatan Alat',
        message: 'Pemeriksaan peralatan selesai kerja belum dilakukan hari ini',
        type: NotificationType.equipmentCheckReminder,
        severity: NotificationSeverity.critical,
        createdAt: now,
        expiresAt: DateTime(now.year, now.month, now.day + 1, 6), // Expires next morning
      ));
    }

    // Rule 2, 3, 4 can be implemented similarly using actual data if available.
    return notifications;
  }
}
```

**File: `lib/features/notifications/data/datasources/notification_local_datasource.dart`**
Create a simple Hive-backed storage that saves these generated notifications and updates their `isRead`/`isDismissed` flags. 

**File: `lib/features/notifications/data/repositories/notification_repository_impl.dart`**
Implement the repository methods, delegating generation to `NotificationRuleEngine` and storage to `NotificationLocalDataSource`. Ensure `checkAndGenerateNotifications` deduplicates based on type and day (so we don't spam 100 equipment check reminders).

### Task 3: Notification Presentation

**Cubit:** `NotificationCubit` fetching notifications and emitting loaded states.
**Pages & Widgets:** 
Create `notification_list_page.dart` (showing cards).
Create `notification_banner.dart` (a `MaterialBanner` checking `context.read<NotificationCubit>().state` for critical notifications).

## Critical requirements
- In-app only.
- Strict Forest & Stone theme implementation.
- Deduplicate notifications (don't generate the same warning multiple times in one session).

## Next
Move to substep 9.5: *"run substep 9.5"*.
