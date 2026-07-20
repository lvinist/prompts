# mine-flow — STEP-9.1: Reporting Domain, Data Layer & PDF Service

> **How to run:** Tell your agent *"run substep 9.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is **STEP-9** (Tier 3 - Reporting, Timeline & Polish), substep **9.1** — the first substep.

**STEP-9 PLAN:** `Upcoming Prompts/mine-flow-STEP-9-PLAN.md`

**What came before:** STEPs 3–8 built all Tier 1 (daily ops) and Tier 2 (tracking & measurement) features. The data sources for reports — `AttendanceRecord`, `CutFillRecord`, `LandClearingRecord`, `InventoryItem`, `EquipmentCheck`, `DailyLog` — already exist in the codebase with full domain entities, data models, repositories, and Supabase datasources.

**This substep** builds the **reporting feature's domain and data layers**, plus a **PDF generation service** that can produce formatted PDF documents from aggregated data. The `lib/features/reporting/` directory currently exists but is **empty** (only a `.gitkeep` file). No PDF generation package exists in `pubspec.yaml` yet.

## Read these first

Read these files before starting work. They define the patterns, entities, and constraints this substep must follow:

- `Code/mine-flow-docs/overview.md` — project brief
- `Code/mine-flow-docs/architecture/01-system-overview.md` — Tier 3 scope definition (§4: Reports/PDF export: crew attendance & overtime, cut/fill weekly/monthly/YTD/PTD, inventory tracking)
- `Code/mine-flow-docs/architecture/02-phasing-roadmap.md` — Launch criterion LC-3: at least one report type exportable to PDF
- `Code/mine-flow-docs/architecture/03-architecture-overview.md` — Clean Architecture modular monolith
- `Code/mine-flow-docs/architecture/04-data-model.md` — Core entities and relationships
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — Forest & Stone palette, Inter typography
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — Test pyramid, mocking strategy
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md` — BLoC state management, offline-first
- `Code/mine-flow-docs/coding-standards/dart.md` — Dart coding standards
- `Code/mine-flow-app/README.md` — App setup and run instructions
- `.throughstone/local-user.md` — Experience level: Level 2 - Basic; Communication style: Explanatory

**Existing entity examples to follow as patterns:**
- `Code/mine-flow-app/lib/features/tracking/domain/entities/cut_fill_record.dart` — Equatable entity with `copyWith()`, `props`
- `Code/mine-flow-app/lib/features/tracking/domain/repositories/tracking_repository.dart` — Repository interface pattern
- `Code/mine-flow-app/lib/features/tracking/data/repositories/tracking_repository_impl.dart` — Repository implementation pattern
- `Code/mine-flow-app/lib/features/data_bucket/data/datasources/data_bucket_remote_datasource.dart` — Supabase datasource pattern

**Existing dependency references:**
- `Code/mine-flow-app/pubspec.yaml` — Current dependencies (NO pdf or printing package yet)
- `Code/mine-flow-app/lib/core/data/models/` — All existing Hive data models
- `Code/mine-flow-app/lib/core/domain/entities/` — All existing core domain entities
- `Code/mine-flow-app/lib/core/error/failures.dart` — Failure hierarchy

## Scope

**This substep owns:**
1. Adding `pdf: ^3.11.1` and `printing: ^5.13.4` packages to `pubspec.yaml`
2. Creating `lib/features/reporting/domain/` — entities and repository interface
3. Creating `lib/features/reporting/data/` — datasources (querying existing Supabase tables), repository implementation
4. Creating `lib/core/services/pdf_service.dart` — PDF generation engine
5. Deleting the empty `.gitkeep` file from `lib/features/reporting/`

**This substep does NOT touch:**
- Presentation layer (BLoC, pages, widgets) — that's 9.2
- Timeline feature — that's 9.3
- Notification system — that's 9.4
- Route wiring or tests — that's 9.5

## Your task

### Task 1: Add PDF dependencies to `pubspec.yaml`

Add the following under `dependencies:` in `Code/mine-flow-app/pubspec.yaml`, after the `url_launcher` entry:

```yaml
  # --- PDF generation (STEP-9: Report export) ---
  pdf: ^3.11.1
  printing: ^5.13.4
```

Then run `flutter pub get` in the `Code/mine-flow-app/` directory to install them.

### Task 2: Create reporting domain entities

**File: `lib/features/reporting/domain/entities/report_type.dart`**

Create an enum defining the 3 supported report types:

```dart
/// Enumeration of supported report types in the reporting feature.
///
/// Each report type maps to a specific data source and PDF layout.
enum ReportType {
  /// Crew attendance & overtime report.
  /// Data source: attendance_records table.
  attendance('Laporan Kehadiran', 'attendance'),

  /// Cut/fill volume report (weekly, monthly, YTD, PTD).
  /// Data source: cut_fill_records table.
  cutFill('Laporan Volume Cut/Fill', 'cut_fill'),

  /// Inventory tracking report.
  /// Data source: inventory_items table.
  inventory('Laporan Inventaris', 'inventory');

  const ReportType(this.displayName, this.tableName);

  /// Indonesian display name for UI.
  final String displayName;

  /// Supabase table name for data queries.
  final String tableName;
}
```

**File: `lib/features/reporting/domain/entities/date_range_filter.dart`**

Create a value object for date range filtering:

```dart
import 'package:equatable/equatable.dart';

/// Value object representing a date range filter for reports.
///
/// Used to specify the time window for data aggregation in report generation.
class DateRangeFilter extends Equatable {
  /// Start date of the range (inclusive).
  final DateTime startDate;

  /// End date of the range (inclusive).
  final DateTime endDate;

  const DateRangeFilter({
    required this.startDate,
    required this.endDate,
  });

  /// Duration of the date range.
  Duration get duration => endDate.difference(startDate);

  /// Number of days in the range (inclusive).
  int get dayCount => duration.inDays + 1;

  /// Whether this is a valid range (start <= end).
  bool get isValid => !startDate.isAfter(endDate);

  /// Creates a filter for the current week (Monday to Sunday).
  factory DateRangeFilter.currentWeek() {
    final now = DateTime.now();
    final monday = now.subtract(Duration(days: now.weekday - 1));
    final sunday = monday.add(const Duration(days: 6));
    return DateRangeFilter(
      startDate: DateTime(monday.year, monday.month, monday.day),
      endDate: DateTime(sunday.year, sunday.month, sunday.day, 23, 59, 59),
    );
  }

  /// Creates a filter for the current month.
  factory DateRangeFilter.currentMonth() {
    final now = DateTime.now();
    final firstDay = DateTime(now.year, now.month, 1);
    final lastDay = DateTime(now.year, now.month + 1, 0, 23, 59, 59);
    return DateRangeFilter(startDate: firstDay, endDate: lastDay);
  }

  /// Creates a filter for Year-To-Date.
  factory DateRangeFilter.yearToDate() {
    final now = DateTime.now();
    return DateRangeFilter(
      startDate: DateTime(now.year, 1, 1),
      endDate: DateTime(now.year, now.month, now.day, 23, 59, 59),
    );
  }

  /// Creates a filter for Project-To-Date (from project start to now).
  /// Uses a fixed project start date for the MVP.
  factory DateRangeFilter.projectToDate() {
    final now = DateTime.now();
    return DateRangeFilter(
      startDate: DateTime(2026, 1, 1), // Project start — adjust as needed
      endDate: DateTime(now.year, now.month, now.day, 23, 59, 59),
    );
  }

  DateRangeFilter copyWith({
    DateTime? startDate,
    DateTime? endDate,
  }) {
    return DateRangeFilter(
      startDate: startDate ?? this.startDate,
      endDate: endDate ?? this.endDate,
    );
  }

  @override
  List<Object?> get props => [startDate, endDate];
}
```

**File: `lib/features/reporting/domain/entities/report_request.dart`**

```dart
import 'package:equatable/equatable.dart';
import 'package:mine_flow/features/reporting/domain/entities/date_range_filter.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_type.dart';

/// Domain entity representing a request to generate a report.
///
/// Encapsulates all parameters needed to query data and produce a report.
class ReportRequest extends Equatable {
  /// Unique identifier for this request.
  final String id;

  /// Type of report to generate.
  final ReportType reportType;

  /// Site ID to filter data for (Phase 1: single site).
  final String siteId;

  /// Date range for the report data.
  final DateRangeFilter dateRange;

  /// Optional zone ID filter. If null, includes all zones.
  final String? zoneId;

  /// Timestamp when this request was created.
  final DateTime createdAt;

  const ReportRequest({
    required this.id,
    required this.reportType,
    required this.siteId,
    required this.dateRange,
    this.zoneId,
    required this.createdAt,
  });

  ReportRequest copyWith({
    String? id,
    ReportType? reportType,
    String? siteId,
    DateRangeFilter? dateRange,
    String? zoneId,
    DateTime? createdAt,
  }) {
    return ReportRequest(
      id: id ?? this.id,
      reportType: reportType ?? this.reportType,
      siteId: siteId ?? this.siteId,
      dateRange: dateRange ?? this.dateRange,
      zoneId: zoneId ?? this.zoneId,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  List<Object?> get props => [id, reportType, siteId, dateRange, zoneId, createdAt];
}
```

**File: `lib/features/reporting/domain/entities/report_result.dart`**

```dart
import 'dart:typed_data';
import 'package:equatable/equatable.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_request.dart';

/// Domain entity representing the result of a generated report.
///
/// Contains the PDF bytes and metadata about the generated report.
class ReportResult extends Equatable {
  /// The original request that produced this result.
  final ReportRequest request;

  /// Generated PDF as raw bytes. Can be shared, printed, or saved.
  final Uint8List pdfBytes;

  /// Human-readable title for the report (used in PDF header and sharing).
  final String title;

  /// Number of data rows included in the report.
  final int recordCount;

  /// Timestamp when the report was generated.
  final DateTime generatedAt;

  const ReportResult({
    required this.request,
    required this.pdfBytes,
    required this.title,
    required this.recordCount,
    required this.generatedAt,
  });

  /// File name for saving/sharing the PDF.
  String get fileName =>
      '${request.reportType.tableName}_report_${generatedAt.toIso8601String().substring(0, 10)}.pdf';

  @override
  List<Object?> get props => [request, pdfBytes, title, recordCount, generatedAt];
}
```

### Task 3: Create reporting repository interface

**File: `lib/features/reporting/domain/repositories/reporting_repository.dart`**

```dart
import 'package:mine_flow/features/reporting/domain/entities/report_request.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_result.dart';

/// Repository interface for the reporting feature.
///
/// Defines the contract for fetching aggregated data and generating reports.
/// The implementation queries existing Supabase tables (attendance_records,
/// cut_fill_records, inventory_items) and delegates PDF generation to PdfService.
abstract class ReportingRepository {
  /// Generates a complete report (data fetch + PDF generation) for the given request.
  ///
  /// Returns a [ReportResult] containing the PDF bytes and metadata.
  /// Throws [ServerFailure] if the Supabase query fails.
  /// Throws [ValidationFailure] if the request parameters are invalid.
  Future<ReportResult> generateReport(ReportRequest request);

  /// Fetches raw attendance data for the given site, date range, and optional zone.
  ///
  /// Returns a list of maps with keys: user_name, date, status, check_in, check_out, overtime_hours.
  Future<List<Map<String, dynamic>>> fetchAttendanceData({
    required String siteId,
    required DateTime startDate,
    required DateTime endDate,
    String? zoneId,
  });

  /// Fetches raw cut/fill volume data for the given site, date range, and optional zone.
  ///
  /// Returns a list of maps with keys: zone_name, measurement_date, cut_volume_m3,
  /// fill_volume_m3, net_volume_m3, measured_by.
  Future<List<Map<String, dynamic>>> fetchCutFillData({
    required String siteId,
    required DateTime startDate,
    required DateTime endDate,
    String? zoneId,
  });

  /// Fetches raw inventory data for the given site.
  ///
  /// Returns a list of maps with keys: item_name, category, quantity, unit,
  /// minimum_stock, last_updated.
  Future<List<Map<String, dynamic>>> fetchInventoryData({
    required String siteId,
  });
}
```

### Task 4: Create reporting data layer

**File: `lib/features/reporting/data/datasources/reporting_remote_datasource.dart`**

This datasource queries existing Supabase tables to aggregate report data. It does NOT create new tables — it reads from existing ones.

```dart
import 'package:logging/logging.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

/// Remote datasource for fetching aggregated report data from Supabase.
///
/// Queries existing tables (attendance_records, cut_fill_records, inventory_items)
/// with date range and zone filters. Does not create new database tables.
class ReportingRemoteDataSource {
  final SupabaseClient _supabaseClient;
  static final Logger _logger = Logger('ReportingRemoteDataSource');

  ReportingRemoteDataSource({required SupabaseClient supabaseClient})
      : _supabaseClient = supabaseClient;

  /// Fetches attendance records joined with user names for the given filters.
  ///
  /// Queries the `attendance_records` table with a join to `users` for names.
  /// Returns raw JSON maps with: user_name, date, status, check_in, check_out, overtime_hours.
  Future<List<Map<String, dynamic>>> fetchAttendanceData({
    required String siteId,
    required DateTime startDate,
    required DateTime endDate,
    String? zoneId,
  }) async {
    _logger.info(
      'Fetching attendance data for site=$siteId, '
      'range=${startDate.toIso8601String()} to ${endDate.toIso8601String()}',
    );

    try {
      var query = _supabaseClient
          .from('attendance_records')
          .select('*, users!inner(full_name)')
          .eq('site_id', siteId)
          .gte('date', startDate.toIso8601String())
          .lte('date', endDate.toIso8601String())
          .isFilter('deleted_at', null)
          .order('date', ascending: true);

      final response = await query;
      _logger.info('Fetched ${response.length} attendance records.');

      return response.map<Map<String, dynamic>>((row) {
        return {
          'user_name': row['users']?['full_name'] ?? 'Tidak Diketahui',
          'date': row['date'],
          'status': row['status'] ?? 'unknown',
          'check_in': row['check_in_time'],
          'check_out': row['check_out_time'],
          'overtime_hours': row['overtime_hours'] ?? 0.0,
        };
      }).toList();
    } catch (e, stack) {
      _logger.severe('Failed to fetch attendance data', e, stack);
      rethrow;
    }
  }

  /// Fetches cut/fill volume records joined with zone names for the given filters.
  ///
  /// Queries the `cut_fill_records` table with a join to `zones` for zone names.
  /// Returns raw JSON maps with: zone_name, measurement_date, cut_volume_m3,
  /// fill_volume_m3, net_volume_m3, measured_by.
  Future<List<Map<String, dynamic>>> fetchCutFillData({
    required String siteId,
    required DateTime startDate,
    required DateTime endDate,
    String? zoneId,
  }) async {
    _logger.info(
      'Fetching cut/fill data for site=$siteId, '
      'range=${startDate.toIso8601String()} to ${endDate.toIso8601String()}',
    );

    try {
      var query = _supabaseClient
          .from('cut_fill_records')
          .select('*, zones!inner(name, category)')
          .eq('site_id', siteId)
          .gte('measurement_date', startDate.toIso8601String())
          .lte('measurement_date', endDate.toIso8601String())
          .isFilter('deleted_at', null)
          .order('measurement_date', ascending: true);

      if (zoneId != null) {
        query = _supabaseClient
            .from('cut_fill_records')
            .select('*, zones!inner(name, category)')
            .eq('site_id', siteId)
            .eq('zone_id', zoneId)
            .gte('measurement_date', startDate.toIso8601String())
            .lte('measurement_date', endDate.toIso8601String())
            .isFilter('deleted_at', null)
            .order('measurement_date', ascending: true);
      }

      final response = await query;
      _logger.info('Fetched ${response.length} cut/fill records.');

      return response.map<Map<String, dynamic>>((row) {
        final cutVol = (row['cut_volume_m3'] as num?)?.toDouble() ?? 0.0;
        final fillVol = (row['fill_volume_m3'] as num?)?.toDouble() ?? 0.0;
        return {
          'zone_name': '${row['zones']?['category'] ?? ''} - ${row['zones']?['name'] ?? ''}',
          'measurement_date': row['measurement_date'],
          'cut_volume_m3': cutVol,
          'fill_volume_m3': fillVol,
          'net_volume_m3': cutVol - fillVol,
          'measured_by': row['measured_by'],
        };
      }).toList();
    } catch (e, stack) {
      _logger.severe('Failed to fetch cut/fill data', e, stack);
      rethrow;
    }
  }

  /// Fetches current inventory items for the given site.
  ///
  /// Queries the `inventory_items` table.
  /// Returns raw JSON maps with: item_name, category, quantity, unit,
  /// minimum_stock, last_updated.
  Future<List<Map<String, dynamic>>> fetchInventoryData({
    required String siteId,
  }) async {
    _logger.info('Fetching inventory data for site=$siteId');

    try {
      final response = await _supabaseClient
          .from('inventory_items')
          .select()
          .eq('site_id', siteId)
          .isFilter('deleted_at', null)
          .order('name', ascending: true);

      _logger.info('Fetched ${response.length} inventory items.');

      return response.map<Map<String, dynamic>>((row) {
        return {
          'item_name': row['name'] ?? 'Tidak Diketahui',
          'category': row['category'] ?? '-',
          'quantity': (row['quantity'] as num?)?.toDouble() ?? 0.0,
          'unit': row['unit'] ?? '-',
          'minimum_stock': (row['minimum_stock'] as num?)?.toDouble() ?? 0.0,
          'last_updated': row['updated_at'],
        };
      }).toList();
    } catch (e, stack) {
      _logger.severe('Failed to fetch inventory data', e, stack);
      rethrow;
    }
  }
}
```

**File: `lib/features/reporting/data/repositories/reporting_repository_impl.dart`**

```dart
import 'package:logging/logging.dart';
import 'package:mine_flow/core/error/failures.dart';
import 'package:mine_flow/core/services/pdf_service.dart';
import 'package:mine_flow/features/reporting/data/datasources/reporting_remote_datasource.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_request.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_result.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_type.dart';
import 'package:mine_flow/features/reporting/domain/repositories/reporting_repository.dart';

/// Implementation of [ReportingRepository] that fetches data from Supabase
/// via [ReportingRemoteDataSource] and generates PDFs via [PdfService].
class ReportingRepositoryImpl implements ReportingRepository {
  final ReportingRemoteDataSource _remoteDataSource;
  final PdfService _pdfService;
  static final Logger _logger = Logger('ReportingRepositoryImpl');

  ReportingRepositoryImpl({
    required ReportingRemoteDataSource remoteDataSource,
    required PdfService pdfService,
  })  : _remoteDataSource = remoteDataSource,
        _pdfService = pdfService;

  @override
  Future<ReportResult> generateReport(ReportRequest request) async {
    _logger.info('Generating report: ${request.reportType.displayName}');

    if (!request.dateRange.isValid) {
      throw const ValidationFailure('Rentang tanggal tidak valid.');
    }

    try {
      List<Map<String, dynamic>> data;
      String title;

      switch (request.reportType) {
        case ReportType.attendance:
          data = await fetchAttendanceData(
            siteId: request.siteId,
            startDate: request.dateRange.startDate,
            endDate: request.dateRange.endDate,
            zoneId: request.zoneId,
          );
          title = 'Laporan Kehadiran';
          break;
        case ReportType.cutFill:
          data = await fetchCutFillData(
            siteId: request.siteId,
            startDate: request.dateRange.startDate,
            endDate: request.dateRange.endDate,
            zoneId: request.zoneId,
          );
          title = 'Laporan Volume Cut/Fill';
          break;
        case ReportType.inventory:
          data = await fetchInventoryData(siteId: request.siteId);
          title = 'Laporan Inventaris';
          break;
      }

      final pdfBytes = await _pdfService.generatePdf(
        reportType: request.reportType,
        title: title,
        data: data,
        startDate: request.dateRange.startDate,
        endDate: request.dateRange.endDate,
      );

      return ReportResult(
        request: request,
        pdfBytes: pdfBytes,
        title: title,
        recordCount: data.length,
        generatedAt: DateTime.now(),
      );
    } catch (e) {
      if (e is Failure) rethrow;
      _logger.severe('Report generation failed', e);
      throw ServerFailure('Gagal membuat laporan: ${e.toString()}');
    }
  }

  @override
  Future<List<Map<String, dynamic>>> fetchAttendanceData({
    required String siteId,
    required DateTime startDate,
    required DateTime endDate,
    String? zoneId,
  }) {
    return _remoteDataSource.fetchAttendanceData(
      siteId: siteId,
      startDate: startDate,
      endDate: endDate,
      zoneId: zoneId,
    );
  }

  @override
  Future<List<Map<String, dynamic>>> fetchCutFillData({
    required String siteId,
    required DateTime startDate,
    required DateTime endDate,
    String? zoneId,
  }) {
    return _remoteDataSource.fetchCutFillData(
      siteId: siteId,
      startDate: startDate,
      endDate: endDate,
      zoneId: zoneId,
    );
  }

  @override
  Future<List<Map<String, dynamic>>> fetchInventoryData({
    required String siteId,
  }) {
    return _remoteDataSource.fetchInventoryData(siteId: siteId);
  }
}
```

### Task 5: Create PDF Service

**File: `lib/core/services/pdf_service.dart`**

This is the core PDF generation engine. It uses the `pdf` package to create formatted PDF documents.

```dart
import 'dart:typed_data';

import 'package:intl/intl.dart';
import 'package:logging/logging.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;

import 'package:mine_flow/features/reporting/domain/entities/report_type.dart';

/// Service responsible for generating PDF documents from report data.
///
/// Uses the `pdf` package to create formatted PDF pages with headers,
/// data tables, and summary statistics. Follows the Forest & Stone design
/// system colors where applicable.
class PdfService {
  static final Logger _logger = Logger('PdfService');

  /// Forest & Stone primary color for PDF headers.
  static const PdfColor _primaryColor = PdfColor.fromInt(0xFF166534);

  /// Stone gray for secondary text.
  static const PdfColor _stoneGray = PdfColor.fromInt(0xFF78716C);

  /// Generates a PDF document for the given report type and data.
  ///
  /// Returns the PDF as raw [Uint8List] bytes suitable for sharing/saving.
  /// [reportType] determines the table column layout.
  /// [title] is the report title shown in the header.
  /// [data] is a list of maps where keys are column identifiers.
  /// [startDate] and [endDate] define the report period.
  Future<Uint8List> generatePdf({
    required ReportType reportType,
    required String title,
    required List<Map<String, dynamic>> data,
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    _logger.info('Generating PDF for $title (${data.length} records)');

    final pdf = pw.Document(
      title: title,
      author: 'mine-flow',
      creator: 'mine-flow Reporting System',
    );

    final dateFormat = DateFormat('dd MMM yyyy', 'id_ID');
    final periodText = '${dateFormat.format(startDate)} — ${dateFormat.format(endDate)}';

    pdf.addPage(
      pw.MultiPage(
        pageFormat: PdfPageFormat.a4,
        margin: const pw.EdgeInsets.all(40),
        header: (context) => _buildHeader(title, periodText, context),
        footer: (context) => _buildFooter(context),
        build: (context) => [
          pw.SizedBox(height: 20),
          _buildSummarySection(reportType, data),
          pw.SizedBox(height: 16),
          _buildDataTable(reportType, data),
        ],
      ),
    );

    final bytes = await pdf.save();
    _logger.info('PDF generated successfully: ${bytes.length} bytes');
    return Uint8List.fromList(bytes);
  }

  /// Builds the page header with title, period, and a colored divider.
  pw.Widget _buildHeader(String title, String periodText, pw.Context context) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        pw.Row(
          mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
          children: [
            pw.Text(
              title,
              style: pw.TextStyle(
                fontSize: 18,
                fontWeight: pw.FontWeight.bold,
                color: _primaryColor,
              ),
            ),
            pw.Text(
              'mine-flow',
              style: pw.TextStyle(fontSize: 10, color: _stoneGray),
            ),
          ],
        ),
        pw.SizedBox(height: 4),
        pw.Text(
          'Periode: $periodText',
          style: pw.TextStyle(fontSize: 10, color: _stoneGray),
        ),
        pw.SizedBox(height: 4),
        pw.Text(
          'Dibuat: ${DateFormat('dd MMM yyyy HH:mm', 'id_ID').format(DateTime.now())}',
          style: pw.TextStyle(fontSize: 9, color: _stoneGray),
        ),
        pw.Divider(color: _primaryColor, thickness: 1.5),
      ],
    );
  }

  /// Builds the page footer with page numbers.
  pw.Widget _buildFooter(pw.Context context) {
    return pw.Container(
      alignment: pw.Alignment.centerRight,
      child: pw.Text(
        'Halaman ${context.pageNumber} / ${context.pagesCount}',
        style: pw.TextStyle(fontSize: 9, color: _stoneGray),
      ),
    );
  }

  /// Builds a summary statistics section based on report type.
  pw.Widget _buildSummarySection(
    ReportType reportType,
    List<Map<String, dynamic>> data,
  ) {
    switch (reportType) {
      case ReportType.attendance:
        return _buildAttendanceSummary(data);
      case ReportType.cutFill:
        return _buildCutFillSummary(data);
      case ReportType.inventory:
        return _buildInventorySummary(data);
    }
  }

  pw.Widget _buildAttendanceSummary(List<Map<String, dynamic>> data) {
    final total = data.length;
    final present = data.where((d) => d['status'] == 'present').length;
    final absent = data.where((d) => d['status'] == 'absent').length;
    final sick = data.where((d) => d['status'] == 'sick').length;
    final leave = data.where((d) => d['status'] == 'leave').length;
    final totalOvertime = data.fold<double>(
      0.0,
      (sum, d) => sum + ((d['overtime_hours'] as num?)?.toDouble() ?? 0.0),
    );

    return pw.Container(
      padding: const pw.EdgeInsets.all(12),
      decoration: pw.BoxDecoration(
        border: pw.Border.all(color: PdfColors.grey300),
        borderRadius: pw.BorderRadius.circular(4),
      ),
      child: pw.Row(
        mainAxisAlignment: pw.MainAxisAlignment.spaceAround,
        children: [
          _summaryItem('Total', '$total'),
          _summaryItem('Hadir', '$present'),
          _summaryItem('Absen', '$absent'),
          _summaryItem('Sakit', '$sick'),
          _summaryItem('Cuti', '$leave'),
          _summaryItem('Lembur (jam)', totalOvertime.toStringAsFixed(1)),
        ],
      ),
    );
  }

  pw.Widget _buildCutFillSummary(List<Map<String, dynamic>> data) {
    final totalCut = data.fold<double>(
      0.0,
      (sum, d) => sum + ((d['cut_volume_m3'] as num?)?.toDouble() ?? 0.0),
    );
    final totalFill = data.fold<double>(
      0.0,
      (sum, d) => sum + ((d['fill_volume_m3'] as num?)?.toDouble() ?? 0.0),
    );

    return pw.Container(
      padding: const pw.EdgeInsets.all(12),
      decoration: pw.BoxDecoration(
        border: pw.Border.all(color: PdfColors.grey300),
        borderRadius: pw.BorderRadius.circular(4),
      ),
      child: pw.Row(
        mainAxisAlignment: pw.MainAxisAlignment.spaceAround,
        children: [
          _summaryItem('Total Pengukuran', '${data.length}'),
          _summaryItem('Total Cut (m³)', totalCut.toStringAsFixed(2)),
          _summaryItem('Total Fill (m³)', totalFill.toStringAsFixed(2)),
          _summaryItem('Netto (m³)', (totalCut - totalFill).toStringAsFixed(2)),
        ],
      ),
    );
  }

  pw.Widget _buildInventorySummary(List<Map<String, dynamic>> data) {
    final totalItems = data.length;
    final lowStock = data.where((d) {
      final qty = (d['quantity'] as num?)?.toDouble() ?? 0.0;
      final minStock = (d['minimum_stock'] as num?)?.toDouble() ?? 0.0;
      return qty <= minStock && minStock > 0;
    }).length;

    return pw.Container(
      padding: const pw.EdgeInsets.all(12),
      decoration: pw.BoxDecoration(
        border: pw.Border.all(color: PdfColors.grey300),
        borderRadius: pw.BorderRadius.circular(4),
      ),
      child: pw.Row(
        mainAxisAlignment: pw.MainAxisAlignment.spaceAround,
        children: [
          _summaryItem('Total Item', '$totalItems'),
          _summaryItem('Stok Rendah', '$lowStock'),
        ],
      ),
    );
  }

  pw.Widget _summaryItem(String label, String value) {
    return pw.Column(
      children: [
        pw.Text(
          value,
          style: pw.TextStyle(
            fontSize: 16,
            fontWeight: pw.FontWeight.bold,
            color: _primaryColor,
          ),
        ),
        pw.SizedBox(height: 2),
        pw.Text(
          label,
          style: pw.TextStyle(fontSize: 9, color: _stoneGray),
        ),
      ],
    );
  }

  /// Builds the data table based on report type.
  pw.Widget _buildDataTable(
    ReportType reportType,
    List<Map<String, dynamic>> data,
  ) {
    switch (reportType) {
      case ReportType.attendance:
        return _buildAttendanceTable(data);
      case ReportType.cutFill:
        return _buildCutFillTable(data);
      case ReportType.inventory:
        return _buildInventoryTable(data);
    }
  }

  pw.Widget _buildAttendanceTable(List<Map<String, dynamic>> data) {
    final dateFormat = DateFormat('dd/MM/yyyy');
    return pw.TableHelper.fromTextArray(
      headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 9),
      cellStyle: const pw.TextStyle(fontSize: 8),
      headerDecoration: const pw.BoxDecoration(color: PdfColors.grey200),
      cellAlignments: {
        0: pw.Alignment.centerLeft,
        1: pw.Alignment.center,
        2: pw.Alignment.center,
        3: pw.Alignment.center,
        4: pw.Alignment.center,
        5: pw.Alignment.centerRight,
      },
      headers: ['Nama', 'Tanggal', 'Status', 'Masuk', 'Keluar', 'Lembur (jam)'],
      data: data.map((row) {
        final date = row['date'] != null
            ? dateFormat.format(DateTime.parse(row['date'] as String))
            : '-';
        return [
          row['user_name']?.toString() ?? '-',
          date,
          _translateStatus(row['status']?.toString() ?? ''),
          row['check_in']?.toString() ?? '-',
          row['check_out']?.toString() ?? '-',
          (row['overtime_hours'] as num?)?.toStringAsFixed(1) ?? '0.0',
        ];
      }).toList(),
    );
  }

  pw.Widget _buildCutFillTable(List<Map<String, dynamic>> data) {
    final dateFormat = DateFormat('dd/MM/yyyy');
    return pw.TableHelper.fromTextArray(
      headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 9),
      cellStyle: const pw.TextStyle(fontSize: 8),
      headerDecoration: const pw.BoxDecoration(color: PdfColors.grey200),
      cellAlignments: {
        0: pw.Alignment.centerLeft,
        1: pw.Alignment.center,
        2: pw.Alignment.centerRight,
        3: pw.Alignment.centerRight,
        4: pw.Alignment.centerRight,
        5: pw.Alignment.centerLeft,
      },
      headers: ['Zona', 'Tanggal', 'Cut (m³)', 'Fill (m³)', 'Netto (m³)', 'Diukur oleh'],
      data: data.map((row) {
        final date = row['measurement_date'] != null
            ? dateFormat.format(DateTime.parse(row['measurement_date'] as String))
            : '-';
        return [
          row['zone_name']?.toString() ?? '-',
          date,
          (row['cut_volume_m3'] as num?)?.toStringAsFixed(2) ?? '0.00',
          (row['fill_volume_m3'] as num?)?.toStringAsFixed(2) ?? '0.00',
          (row['net_volume_m3'] as num?)?.toStringAsFixed(2) ?? '0.00',
          row['measured_by']?.toString() ?? '-',
        ];
      }).toList(),
    );
  }

  pw.Widget _buildInventoryTable(List<Map<String, dynamic>> data) {
    return pw.TableHelper.fromTextArray(
      headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 9),
      cellStyle: const pw.TextStyle(fontSize: 8),
      headerDecoration: const pw.BoxDecoration(color: PdfColors.grey200),
      cellAlignments: {
        0: pw.Alignment.centerLeft,
        1: pw.Alignment.center,
        2: pw.Alignment.centerRight,
        3: pw.Alignment.center,
        4: pw.Alignment.centerRight,
      },
      headers: ['Nama Item', 'Kategori', 'Jumlah', 'Satuan', 'Stok Minimum'],
      data: data.map((row) {
        return [
          row['item_name']?.toString() ?? '-',
          row['category']?.toString() ?? '-',
          (row['quantity'] as num?)?.toStringAsFixed(1) ?? '0.0',
          row['unit']?.toString() ?? '-',
          (row['minimum_stock'] as num?)?.toStringAsFixed(1) ?? '0.0',
        ];
      }).toList(),
    );
  }

  /// Translates attendance status to Indonesian display text.
  String _translateStatus(String status) {
    switch (status.toLowerCase()) {
      case 'present':
        return 'Hadir';
      case 'absent':
        return 'Absen';
      case 'sick':
        return 'Sakit';
      case 'leave':
        return 'Cuti';
      default:
        return status;
    }
  }
}
```

### Task 6: Delete the empty `.gitkeep` file

Delete the file `lib/features/reporting/.gitkeep` since the directory now has real content.

### Task 7: Run `flutter pub get`

After all files are created, run:
```bash
cd Code/mine-flow-app
flutter pub get
```

Verify there are no import errors by running:
```bash
flutter analyze lib/features/reporting/ lib/core/services/pdf_service.dart
```

## Verification

- **Tests are deferred to substep 9.5** (dedicated final verification substep per STEP PLAN).
- After completing the tasks above, verify:
  1. `flutter pub get` succeeds without errors
  2. `flutter analyze lib/features/reporting/ lib/core/services/pdf_service.dart` shows no errors (warnings are acceptable)
  3. The following files exist with non-zero size:
     - `lib/features/reporting/domain/entities/report_type.dart`
     - `lib/features/reporting/domain/entities/date_range_filter.dart`
     - `lib/features/reporting/domain/entities/report_request.dart`
     - `lib/features/reporting/domain/entities/report_result.dart`
     - `lib/features/reporting/domain/repositories/reporting_repository.dart`
     - `lib/features/reporting/data/datasources/reporting_remote_datasource.dart`
     - `lib/features/reporting/data/repositories/reporting_repository_impl.dart`
     - `lib/core/services/pdf_service.dart`
  4. The `.gitkeep` file in `lib/features/reporting/` has been removed

## Keeping the docs true (always)

This substep does not change any architecture decisions. The reporting feature was already specified in the architecture docs (Doc 01 §4, Doc 02 §1). No doc updates are needed unless you deviate from the prescribed patterns.

If you find that the Supabase table names or column names in the datasource don't match what exists in the database, **adapt the datasource queries** to match the actual schema — the architecture doc's entity names are canonical, but Supabase column naming may differ. Document any adaptations in comments.

## Definition of done
- [ ] `pdf` and `printing` packages added to `pubspec.yaml` and `flutter pub get` succeeds.
- [ ] Reporting domain entities created: `ReportType`, `DateRangeFilter`, `ReportRequest`, `ReportResult`.
- [ ] Reporting repository interface created with `generateReport()`, `fetchAttendanceData()`, `fetchCutFillData()`, `fetchInventoryData()`.
- [ ] Reporting remote datasource created, querying existing Supabase tables.
- [ ] Reporting repository implementation created, delegating to datasource and PdfService.
- [ ] `PdfService` created with PDF generation for all 3 report types (attendance, cut/fill, inventory).
- [ ] `flutter analyze` passes without errors on the new files.
- [ ] Code this substep wrote or changed is covered by the relevant tests named above, and those tests are assigned to the STEP's final verification substep (9.5).
- [ ] New/changed classes, functions, and methods carry docstrings.
- [ ] `.gitkeep` deleted from `lib/features/reporting/`.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 9.2"*, in a **fresh chat**.
