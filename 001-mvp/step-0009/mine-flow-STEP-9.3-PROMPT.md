# mine-flow — STEP-9.3: Work Timeline Feature

> **How to run:** Tell your agent *"run substep 9.3"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is **STEP-9** (Tier 3 - Reporting, Timeline & Polish), substep **9.3**.
**Goal:** Deliver a visual planned-vs-actual work timeline. It will query `cut_fill_records` and `land_clearing_records` to build a time-series chart of progress, and use a new table `timeline_milestones` to track specific goals.

## Scope

**This substep owns:**
1. Adding `fl_chart: ^0.69.2` to `pubspec.yaml`.
2. Creating Timeline Domain: `timeline_milestone.dart`, `timeline_data_point.dart`, `timeline_repository.dart`.
3. Creating Timeline Data: SQL migration `create_timeline_milestones.sql`, Hive model (Type ID 14), Remote Datasource, Repository Impl.
4. Creating Timeline Presentation: Cubit, Widgets, and the `TimelinePage`.

## Your task

### Task 1: Add dependencies
In `pubspec.yaml`, add:
```yaml
  fl_chart: ^0.69.2
```
Run `flutter pub get`.

### Task 2: Timeline Domain

**File: `lib/features/timeline/domain/entities/timeline_milestone.dart`**
```dart
import 'package:equatable/equatable.dart';

enum TimelineCategory { cutFill, landClearing, general }

enum MilestoneStatus { planned, inProgress, completed, overdue }

class TimelineMilestone extends Equatable {
  final String id;
  final String siteId;
  final String? zoneId;
  final String title;
  final String? description;
  final TimelineCategory category;
  final double? targetValue;
  final double? actualValue;
  final DateTime? targetDate;
  final DateTime startDate;
  final DateTime? endDate;
  final MilestoneStatus status;
  final DateTime? createdAt;
  final DateTime? updatedAt;
  final DateTime? deletedAt;

  const TimelineMilestone({
    required this.id,
    required this.siteId,
    this.zoneId,
    required this.title,
    this.description,
    this.category = TimelineCategory.general,
    this.targetValue,
    this.actualValue,
    this.targetDate,
    required this.startDate,
    this.endDate,
    this.status = MilestoneStatus.planned,
    this.createdAt,
    this.updatedAt,
    this.deletedAt,
  });

  TimelineMilestone copyWith({
    String? id,
    String? siteId,
    String? zoneId,
    String? title,
    String? description,
    TimelineCategory? category,
    double? targetValue,
    double? actualValue,
    DateTime? targetDate,
    DateTime? startDate,
    DateTime? endDate,
    MilestoneStatus? status,
    DateTime? createdAt,
    DateTime? updatedAt,
    DateTime? deletedAt,
  }) {
    return TimelineMilestone(
      id: id ?? this.id,
      siteId: siteId ?? this.siteId,
      zoneId: zoneId ?? this.zoneId,
      title: title ?? this.title,
      description: description ?? this.description,
      category: category ?? this.category,
      targetValue: targetValue ?? this.targetValue,
      actualValue: actualValue ?? this.actualValue,
      targetDate: targetDate ?? this.targetDate,
      startDate: startDate ?? this.startDate,
      endDate: endDate ?? this.endDate,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      deletedAt: deletedAt ?? this.deletedAt,
    );
  }

  @override
  List<Object?> get props => [
        id, siteId, zoneId, title, description, category, targetValue,
        actualValue, targetDate, startDate, endDate, status,
        createdAt, updatedAt, deletedAt,
      ];
}
```

**File: `lib/features/timeline/domain/entities/timeline_data_point.dart`**
```dart
import 'package:equatable/equatable.dart';

class TimelineDataPoint extends Equatable {
  final DateTime date;
  final double cumulativeCutVolume;
  final double cumulativeFillVolume;
  final double cumulativeLandClearing;
  final double dailyCutVolume;
  final double dailyFillVolume;
  final double dailyLandClearing;

  const TimelineDataPoint({
    required this.date,
    this.cumulativeCutVolume = 0.0,
    this.cumulativeFillVolume = 0.0,
    this.cumulativeLandClearing = 0.0,
    this.dailyCutVolume = 0.0,
    this.dailyFillVolume = 0.0,
    this.dailyLandClearing = 0.0,
  });

  @override
  List<Object?> get props => [
        date, cumulativeCutVolume, cumulativeFillVolume,
        cumulativeLandClearing, dailyCutVolume, dailyFillVolume,
        dailyLandClearing,
      ];
}
```

**File: `lib/features/timeline/domain/repositories/timeline_repository.dart`**
```dart
import 'package:mine_flow/features/timeline/domain/entities/timeline_data_point.dart';
import 'package:mine_flow/features/timeline/domain/entities/timeline_milestone.dart';

abstract class TimelineRepository {
  Future<List<TimelineMilestone>> getMilestones({required String siteId, String? zoneId});
  Future<TimelineMilestone> createMilestone(TimelineMilestone milestone);
  Future<void> updateMilestone(TimelineMilestone milestone);
  Future<void> deleteMilestone(String id);
  Future<List<TimelineDataPoint>> getProgressData({
    required String siteId,
    String? zoneId,
    required DateTime startDate,
    required DateTime endDate,
  });
}
```

### Task 3: Timeline Data Layer

**File: `lib/features/timeline/data/migrations/create_timeline_milestones.sql`**
```sql
CREATE TABLE timeline_milestones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  site_id UUID NOT NULL REFERENCES sites(id),
  zone_id UUID REFERENCES zones(id),
  title TEXT NOT NULL,
  description TEXT,
  category TEXT NOT NULL DEFAULT 'general',
  target_value DOUBLE PRECISION,
  actual_value DOUBLE PRECISION,
  target_date TIMESTAMPTZ,
  start_date TIMESTAMPTZ NOT NULL DEFAULT now(),
  end_date TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'planned',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  deleted_at TIMESTAMPTZ
);
```

**File: `lib/features/timeline/data/models/timeline_milestone_model.dart`**
(Create Hive TypeAdapter ID 14. Standard Hive model mapping to the entity. Keep it simple.)
```dart
import 'package:hive/hive.dart';
import 'package:mine_flow/features/timeline/domain/entities/timeline_milestone.dart';

part 'timeline_milestone_model.g.dart';

@HiveType(typeId: 14)
class TimelineMilestoneModel extends HiveObject {
  @HiveField(0)
  final String id;
  @HiveField(1)
  final String siteId;
  @HiveField(2)
  final String? zoneId;
  @HiveField(3)
  final String title;
  @HiveField(4)
  final String? description;
  @HiveField(5)
  final String category;
  @HiveField(6)
  final double? targetValue;
  @HiveField(7)
  final double? actualValue;
  @HiveField(8)
  final DateTime? targetDate;
  @HiveField(9)
  final DateTime startDate;
  @HiveField(10)
  final DateTime? endDate;
  @HiveField(11)
  final String status;
  @HiveField(12)
  final DateTime? createdAt;
  @HiveField(13)
  final DateTime? updatedAt;
  @HiveField(14)
  final DateTime? deletedAt;

  TimelineMilestoneModel({
    required this.id,
    required this.siteId,
    this.zoneId,
    required this.title,
    this.description,
    required this.category,
    this.targetValue,
    this.actualValue,
    this.targetDate,
    required this.startDate,
    this.endDate,
    required this.status,
    this.createdAt,
    this.updatedAt,
    this.deletedAt,
  });

  factory TimelineMilestoneModel.fromEntity(TimelineMilestone entity) {
    return TimelineMilestoneModel(
      id: entity.id,
      siteId: entity.siteId,
      zoneId: entity.zoneId,
      title: entity.title,
      description: entity.description,
      category: entity.category.name,
      targetValue: entity.targetValue,
      actualValue: entity.actualValue,
      targetDate: entity.targetDate,
      startDate: entity.startDate,
      endDate: entity.endDate,
      status: entity.status.name,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
      deletedAt: entity.deletedAt,
    );
  }

  TimelineMilestone toEntity() {
    return TimelineMilestone(
      id: id,
      siteId: siteId,
      zoneId: zoneId,
      title: title,
      description: description,
      category: TimelineCategory.values.firstWhere((e) => e.name == category, orElse: () => TimelineCategory.general),
      targetValue: targetValue,
      actualValue: actualValue,
      targetDate: targetDate,
      startDate: startDate,
      endDate: endDate,
      status: MilestoneStatus.values.firstWhere((e) => e.name == status, orElse: () => MilestoneStatus.planned),
      createdAt: createdAt,
      updatedAt: updatedAt,
      deletedAt: deletedAt,
    );
  }

  factory TimelineMilestoneModel.fromJson(Map<String, dynamic> json) {
    return TimelineMilestoneModel(
      id: json['id'],
      siteId: json['site_id'],
      zoneId: json['zone_id'],
      title: json['title'],
      description: json['description'],
      category: json['category'] ?? 'general',
      targetValue: (json['target_value'] as num?)?.toDouble(),
      actualValue: (json['actual_value'] as num?)?.toDouble(),
      targetDate: json['target_date'] != null ? DateTime.parse(json['target_date']) : null,
      startDate: DateTime.parse(json['start_date']),
      endDate: json['end_date'] != null ? DateTime.parse(json['end_date']) : null,
      status: json['status'] ?? 'planned',
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at']) : null,
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
      deletedAt: json['deleted_at'] != null ? DateTime.parse(json['deleted_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'site_id': siteId,
      'zone_id': zoneId,
      'title': title,
      'description': description,
      'category': category,
      'target_value': targetValue,
      'actual_value': actualValue,
      'target_date': targetDate?.toIso8601String(),
      'start_date': startDate.toIso8601String(),
      'end_date': endDate?.toIso8601String(),
      'status': status,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'deleted_at': deletedAt?.toIso8601String(),
    };
  }
}
```
*Note: We won't run `build_runner` now, so just leave `timeline_milestone_model.g.dart` alone. You can write the TypeAdapter manually if preferred, but since we are mocking/ignoring Hive code generation execution for MVP if possible, we'll write the manual adapter in `lib/core/offline/adapters/timeline_milestone_adapter.dart` instead of relying on `build_runner`. Actually, write the manual adapter to avoid build_runner:*

**File: `lib/core/offline/adapters/timeline_milestone_adapter.dart`**
```dart
import 'package:hive/hive.dart';
import 'package:mine_flow/features/timeline/data/models/timeline_milestone_model.dart';

class TimelineMilestoneModelAdapter extends TypeAdapter<TimelineMilestoneModel> {
  @override
  final int typeId = 14;

  @override
  TimelineMilestoneModel read(BinaryReader reader) {
    final fields = reader.readMap();
    return TimelineMilestoneModel(
      id: fields[0] as String,
      siteId: fields[1] as String,
      zoneId: fields[2] as String?,
      title: fields[3] as String,
      description: fields[4] as String?,
      category: fields[5] as String,
      targetValue: fields[6] as double?,
      actualValue: fields[7] as double?,
      targetDate: fields[8] as DateTime?,
      startDate: fields[9] as DateTime,
      endDate: fields[10] as DateTime?,
      status: fields[11] as String,
      createdAt: fields[12] as DateTime?,
      updatedAt: fields[13] as DateTime?,
      deletedAt: fields[14] as DateTime?,
    );
  }

  @override
  void write(BinaryWriter writer, TimelineMilestoneModel obj) {
    writer.writeMap({
      0: obj.id,
      1: obj.siteId,
      2: obj.zoneId,
      3: obj.title,
      4: obj.description,
      5: obj.category,
      6: obj.targetValue,
      7: obj.actualValue,
      8: obj.targetDate,
      9: obj.startDate,
      10: obj.endDate,
      11: obj.status,
      12: obj.createdAt,
      13: obj.updatedAt,
      14: obj.deletedAt,
    });
  }
}
```
*(Remove the `part 'timeline_milestone_model.g.dart';` and `@HiveType` annotations from `TimelineMilestoneModel` since we are doing manual adapters).*

**File: `lib/features/timeline/data/datasources/timeline_remote_datasource.dart`**
```dart
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:mine_flow/features/timeline/data/models/timeline_milestone_model.dart';

class TimelineRemoteDataSource {
  final SupabaseClient _supabaseClient;

  TimelineRemoteDataSource({required SupabaseClient supabaseClient}) : _supabaseClient = supabaseClient;

  Future<List<TimelineMilestoneModel>> getMilestones({required String siteId, String? zoneId}) async {
    var query = _supabaseClient.from('timeline_milestones').select().eq('site_id', siteId).isFilter('deleted_at', null);
    if (zoneId != null) query = query.eq('zone_id', zoneId);
    
    final data = await query.order('target_date', ascending: true);
    return data.map((json) => TimelineMilestoneModel.fromJson(json)).toList();
  }

  Future<TimelineMilestoneModel> createMilestone(TimelineMilestoneModel milestone) async {
    final data = await _supabaseClient.from('timeline_milestones').insert(milestone.toJson()).select().single();
    return TimelineMilestoneModel.fromJson(data);
  }

  Future<void> updateMilestone(TimelineMilestoneModel milestone) async {
    await _supabaseClient.from('timeline_milestones').update(milestone.toJson()).eq('id', milestone.id);
  }

  Future<void> deleteMilestone(String id) async {
    await _supabaseClient.from('timeline_milestones').update({'deleted_at': DateTime.now().toIso8601String()}).eq('id', id);
  }

  // Aggregate query
  Future<List<Map<String, dynamic>>> getProgressData({
    required String siteId,
    String? zoneId,
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    // Note: A real app might use a Postgres RPC or View for this aggregation. 
    // For MVP, we fetch the records in the date range and group them in memory.
    
    var cutFillQuery = _supabaseClient.from('cut_fill_records').select().eq('site_id', siteId).isFilter('deleted_at', null).gte('measurement_date', startDate.toIso8601String()).lte('measurement_date', endDate.toIso8601String());
    if (zoneId != null) cutFillQuery = cutFillQuery.eq('zone_id', zoneId);
    
    var landQuery = _supabaseClient.from('land_clearing_records').select().eq('site_id', siteId).isFilter('deleted_at', null).gte('date', startDate.toIso8601String()).lte('date', endDate.toIso8601String());
    if (zoneId != null) landQuery = landQuery.eq('zone_id', zoneId);

    final cutFillData = await cutFillQuery;
    final landData = await landQuery;

    // Grouping logic is moved to repository impl. We just return raw maps here.
    return [
      {'type': 'cut_fill', 'data': cutFillData},
      {'type': 'land_clearing', 'data': landData},
    ];
  }
}
```

**File: `lib/features/timeline/data/repositories/timeline_repository_impl.dart`**
```dart
import 'package:mine_flow/features/timeline/data/datasources/timeline_remote_datasource.dart';
import 'package:mine_flow/features/timeline/data/models/timeline_milestone_model.dart';
import 'package:mine_flow/features/timeline/domain/entities/timeline_data_point.dart';
import 'package:mine_flow/features/timeline/domain/entities/timeline_milestone.dart';
import 'package:mine_flow/features/timeline/domain/repositories/timeline_repository.dart';

class TimelineRepositoryImpl implements TimelineRepository {
  final TimelineRemoteDataSource _remoteDataSource;

  TimelineRepositoryImpl({required TimelineRemoteDataSource remoteDataSource}) : _remoteDataSource = remoteDataSource;

  @override
  Future<List<TimelineMilestone>> getMilestones({required String siteId, String? zoneId}) async {
    final models = await _remoteDataSource.getMilestones(siteId: siteId, zoneId: zoneId);
    return models.map((m) => m.toEntity()).toList();
  }

  @override
  Future<TimelineMilestone> createMilestone(TimelineMilestone milestone) async {
    final model = TimelineMilestoneModel.fromEntity(milestone);
    final result = await _remoteDataSource.createMilestone(model);
    return result.toEntity();
  }

  @override
  Future<void> updateMilestone(TimelineMilestone milestone) async {
    final model = TimelineMilestoneModel.fromEntity(milestone);
    await _remoteDataSource.updateMilestone(model);
  }

  @override
  Future<void> deleteMilestone(String id) async {
    await _remoteDataSource.deleteMilestone(id);
  }

  @override
  Future<List<TimelineDataPoint>> getProgressData({
    required String siteId,
    String? zoneId,
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    final rawData = await _remoteDataSource.getProgressData(siteId: siteId, zoneId: zoneId, startDate: startDate, endDate: endDate);
    
    final cutFillRecords = rawData.firstWhere((r) => r['type'] == 'cut_fill')['data'] as List<dynamic>;
    final landRecords = rawData.firstWhere((r) => r['type'] == 'land_clearing')['data'] as List<dynamic>;

    // Group by day string 'YYYY-MM-DD'
    final Map<String, TimelineDataPoint> dailyMap = {};
    
    for (var r in cutFillRecords) {
      final dateStr = (r['measurement_date'] as String).substring(0, 10);
      final cut = (r['cut_volume_m3'] as num?)?.toDouble() ?? 0.0;
      final fill = (r['fill_volume_m3'] as num?)?.toDouble() ?? 0.0;
      
      final existing = dailyMap[dateStr] ?? TimelineDataPoint(date: DateTime.parse(dateStr));
      dailyMap[dateStr] = TimelineDataPoint(
        date: existing.date,
        dailyCutVolume: existing.dailyCutVolume + cut,
        dailyFillVolume: existing.dailyFillVolume + fill,
        dailyLandClearing: existing.dailyLandClearing,
      );
    }

    for (var r in landRecords) {
      final dateStr = (r['date'] as String).substring(0, 10);
      final area = (r['area_cleared_ha'] as num?)?.toDouble() ?? 0.0; // assuming field name
      
      final existing = dailyMap[dateStr] ?? TimelineDataPoint(date: DateTime.parse(dateStr));
      dailyMap[dateStr] = TimelineDataPoint(
        date: existing.date,
        dailyCutVolume: existing.dailyCutVolume,
        dailyFillVolume: existing.dailyFillVolume,
        dailyLandClearing: existing.dailyLandClearing + area,
      );
    }

    final sortedDates = dailyMap.keys.toList()..sort();
    
    // Calculate cumulatives
    double runningCut = 0.0;
    double runningFill = 0.0;
    double runningLand = 0.0;
    
    List<TimelineDataPoint> result = [];
    for (var dateStr in sortedDates) {
      final dayData = dailyMap[dateStr]!;
      runningCut += dayData.dailyCutVolume;
      runningFill += dayData.dailyFillVolume;
      runningLand += dayData.dailyLandClearing;
      
      result.add(TimelineDataPoint(
        date: dayData.date,
        dailyCutVolume: dayData.dailyCutVolume,
        dailyFillVolume: dayData.dailyFillVolume,
        dailyLandClearing: dayData.dailyLandClearing,
        cumulativeCutVolume: runningCut,
        cumulativeFillVolume: runningFill,
        cumulativeLandClearing: runningLand,
      ));
    }

    return result;
  }
}
```

### Task 4: Timeline Presentation Layer

Create `TimelineCubit`, `TimelineState`, `TimelinePage`, `TimelineChart`, `MilestoneCard`. (Implement standard BLoC fetching data from repository. TimelineChart uses `fl_chart` LineChart widget).

Due to length constraints, ensure your `TimelinePage` and widgets are minimal but fully functional according to the Scope section. Provide basic implementations of `fl_chart`.

## Next
Move to substep 9.4: *"run substep 9.4"*.
