# mine-flow — STEP-9.2: Report UI Screens & State

> **How to run:** Tell your agent *"run substep 9.2"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is **STEP-9** (Tier 3 - Reporting, Timeline & Polish), substep **9.2**.

**What came before:** Substep 9.1 created the reporting domain, datasources, and `PdfService`. It introduced the `pdf` and `printing` packages. The types `ReportType`, `DateRangeFilter`, `ReportRequest`, and `ReportResult` exist in `lib/features/reporting/domain/entities/`, and `ReportingRepository` exists in `lib/features/reporting/domain/repositories/`.

**This substep** builds the presentation layer: the BLoC/Cubit state management, the reusable widgets, and the report configuration and dashboard screens.

## Read these first
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — Forest & Stone theme, compact density, ID locale.
- `Code/mine-flow-app/lib/app/theme/app_theme.dart` — Colors and typography references.
- `Code/mine-flow-app/lib/features/reporting/domain/entities/report_type.dart`
- `Code/mine-flow-app/lib/features/reporting/domain/entities/date_range_filter.dart`
- `Code/mine-flow-app/lib/features/reporting/domain/entities/report_request.dart`
- `Code/mine-flow-app/lib/features/reporting/domain/entities/report_result.dart`
- `Code/mine-flow-app/lib/features/reporting/domain/repositories/reporting_repository.dart`

## Scope

**This substep owns:**
1. Creating `lib/features/reporting/presentation/bloc/` (State & Cubit).
2. Creating `lib/features/reporting/presentation/widgets/` (ReportTypeCard, DateRangeSelector, ReportSummaryCard).
3. Creating `lib/features/reporting/presentation/pages/` (ReportDashboardPage, ReportConfigPage).

**This substep does NOT touch:**
- GoRouter configuration (that's 9.5).
- Timeline or Notification features (9.3, 9.4).

## Your task

### Task 1: Create Report State & Cubit

**File: `lib/features/reporting/presentation/bloc/report_state.dart`**
```dart
import 'package:equatable/equatable.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_result.dart';

sealed class ReportState extends Equatable {
  const ReportState();

  @override
  List<Object?> get props => [];
}

class ReportInitial extends ReportState {
  const ReportInitial();
}

class ReportLoading extends ReportState {
  const ReportLoading();
}

class ReportSuccess extends ReportState {
  final ReportResult result;

  const ReportSuccess(this.result);

  @override
  List<Object?> get props => [result];
}

class ReportError extends ReportState {
  final String message;

  const ReportError(this.message);

  @override
  List<Object?> get props => [message];
}
```

**File: `lib/features/reporting/presentation/bloc/report_cubit.dart`**
```dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mine_flow/core/error/failures.dart';
import 'package:mine_flow/features/reporting/domain/entities/date_range_filter.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_request.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_type.dart';
import 'package:mine_flow/features/reporting/domain/repositories/reporting_repository.dart';
import 'package:mine_flow/features/reporting/presentation/bloc/report_state.dart';
import 'package:uuid/uuid.dart';

class ReportCubit extends Cubit<ReportState> {
  final ReportingRepository _repository;
  
  ReportType? _selectedType;
  DateRangeFilter _dateRange = DateRangeFilter.currentWeek();
  String? _zoneId;

  ReportCubit({required ReportingRepository repository})
      : _repository = repository,
        super(const ReportInitial());

  void selectReportType(ReportType type) {
    _selectedType = type;
    emit(const ReportInitial());
  }

  void setDateRange(DateRangeFilter range) {
    _dateRange = range;
    if (state is! ReportLoading) emit(const ReportInitial());
  }

  void setZoneFilter(String? zoneId) {
    _zoneId = zoneId;
    if (state is! ReportLoading) emit(const ReportInitial());
  }

  void resetReport() {
    emit(const ReportInitial());
  }

  Future<void> generateReport({required String siteId}) async {
    if (_selectedType == null) {
      emit(const ReportError('Pilih jenis laporan terlebih dahulu.'));
      return;
    }

    emit(const ReportLoading());

    try {
      final request = ReportRequest(
        id: const Uuid().v4(),
        reportType: _selectedType!,
        siteId: siteId,
        dateRange: _dateRange,
        zoneId: _zoneId,
        createdAt: DateTime.now(),
      );

      final result = await _repository.generateReport(request);
      emit(ReportSuccess(result));
    } catch (e) {
      if (e is ValidationFailure) {
        emit(ReportError(e.message));
      } else if (e is ServerFailure) {
        emit(ReportError(e.message));
      } else {
        emit(ReportError('Terjadi kesalahan yang tidak diketahui: $e'));
      }
    }
  }
}
```

### Task 2: Create Report Widgets

**File: `lib/features/reporting/presentation/widgets/report_type_card.dart`**
```dart
import 'package:flutter/material.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_type.dart';

class ReportTypeCard extends StatelessWidget {
  final ReportType type;
  final IconData icon;
  final VoidCallback onTap;

  const ReportTypeCard({
    super.key,
    required this.type,
    required this.icon,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(4),
        side: BorderSide(color: theme.colorScheme.outlineVariant),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(4),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 48, color: theme.colorScheme.primary),
              const SizedBox(height: 16),
              Text(
                type.displayName,
                textAlign: TextAlign.center,
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              const Spacer(),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: onTap,
                  style: OutlinedButton.styleFrom(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(4),
                    ),
                  ),
                  child: const Text('Pilih'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

**File: `lib/features/reporting/presentation/widgets/date_range_selector.dart`**
```dart
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:mine_flow/features/reporting/domain/entities/date_range_filter.dart';

class DateRangeSelector extends StatefulWidget {
  final DateRangeFilter initialRange;
  final ValueChanged<DateRangeFilter> onChanged;

  const DateRangeSelector({
    super.key,
    required this.initialRange,
    required this.onChanged,
  });

  @override
  State<DateRangeSelector> createState() => _DateRangeSelectorState();
}

class _DateRangeSelectorState extends State<DateRangeSelector> {
  late String _selectedOption;
  late DateRangeFilter _currentRange;

  @override
  void initState() {
    super.initState();
    _currentRange = widget.initialRange;
    _selectedOption = 'Minggu Ini';
  }

  void _onOptionChanged(String? newValue) async {
    if (newValue == null) return;
    
    setState(() {
      _selectedOption = newValue;
    });

    if (newValue == 'Minggu Ini') {
      _updateRange(DateRangeFilter.currentWeek());
    } else if (newValue == 'Bulan Ini') {
      _updateRange(DateRangeFilter.currentMonth());
    } else if (newValue == 'Year-to-Date') {
      _updateRange(DateRangeFilter.yearToDate());
    } else if (newValue == 'Project-to-Date') {
      _updateRange(DateRangeFilter.projectToDate());
    } else if (newValue == 'Kustom') {
      final picked = await showDateRangePicker(
        context: context,
        firstDate: DateTime(2020),
        lastDate: DateTime.now(),
        initialDateRange: DateTimeRange(
          start: _currentRange.startDate,
          end: _currentRange.endDate,
        ),
      );
      if (picked != null) {
        _updateRange(DateRangeFilter(
          startDate: picked.start,
          endDate: DateTime(picked.end.year, picked.end.month, picked.end.day, 23, 59, 59),
        ));
      } else {
        // Fallback to previous if canceled
        setState(() {
          _selectedOption = 'Minggu Ini';
          _currentRange = DateRangeFilter.currentWeek();
        });
      }
    }
  }

  void _updateRange(DateRangeFilter newRange) {
    setState(() {
      _currentRange = newRange;
    });
    widget.onChanged(newRange);
  }

  @override
  Widget build(BuildContext context) {
    final dateFormat = DateFormat('dd MMM yyyy', 'id_ID');
    final rangeText = '${dateFormat.format(_currentRange.startDate)} - ${dateFormat.format(_currentRange.endDate)}';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        DropdownButtonFormField<String>(
          value: _selectedOption,
          decoration: const InputDecoration(
            labelText: 'Periode Laporan',
            border: OutlineInputBorder(),
            isDense: true,
          ),
          items: const [
            DropdownMenuItem(value: 'Minggu Ini', child: Text('Minggu Ini')),
            DropdownMenuItem(value: 'Bulan Ini', child: Text('Bulan Ini')),
            DropdownMenuItem(value: 'Year-to-Date', child: Text('Year-to-Date')),
            DropdownMenuItem(value: 'Project-to-Date', child: Text('Project-to-Date')),
            DropdownMenuItem(value: 'Kustom', child: Text('Kustom...')),
          ],
          onChanged: _onOptionChanged,
        ),
        const SizedBox(height: 8),
        Text(
          'Rentang: $rangeText',
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }
}
```

**File: `lib/features/reporting/presentation/widgets/report_summary_card.dart`**
```dart
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_result.dart';

class ReportSummaryCard extends StatelessWidget {
  final ReportResult result;

  const ReportSummaryCard({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final dateFormat = DateFormat('dd MMM yyyy HH:mm', 'id_ID');

    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(4),
        side: BorderSide(color: theme.colorScheme.primary.withOpacity(0.5)),
      ),
      color: theme.colorScheme.primaryContainer.withOpacity(0.2),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.check_circle, color: theme.colorScheme.primary),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'Laporan Berhasil Dibuat',
                    style: theme.textTheme.titleMedium?.copyWith(
                      color: theme.colorScheme.primary,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const Divider(),
            const SizedBox(height: 8),
            _buildRow('Judul:', result.title, theme),
            const SizedBox(height: 4),
            _buildRow('Jumlah Data:', '${result.recordCount} baris', theme),
            const SizedBox(height: 4),
            _buildRow('Waktu Dibuat:', dateFormat.format(result.generatedAt), theme),
            const SizedBox(height: 4),
            _buildRow('Ukuran File:', '${(result.pdfBytes.lengthInBytes / 1024).toStringAsFixed(1)} KB', theme),
          ],
        ),
      ),
    );
  }

  Widget _buildRow(String label, String value, ThemeData theme) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 100,
          child: Text(
            label,
            style: theme.textTheme.bodyMedium?.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
        ),
        Expanded(
          child: Text(
            value,
            style: theme.textTheme.bodyMedium?.copyWith(
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
      ],
    );
  }
}
```

### Task 3: Create Report Dashboard Page

**File: `lib/features/reporting/presentation/pages/report_dashboard_page.dart`**
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_type.dart';
import 'package:mine_flow/features/reporting/presentation/widgets/report_type_card.dart';

class ReportDashboardPage extends StatelessWidget {
  const ReportDashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    // Note: The route '/reports/config' will be wired in substep 9.5
    return Scaffold(
      appBar: AppBar(
        title: const Text('Laporan'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Pilih Jenis Laporan',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Pilih jenis laporan yang ingin Anda buat dan unduh dalam format PDF.',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: GridView.count(
                crossAxisCount: MediaQuery.of(context).size.width > 600 ? 3 : 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 0.85,
                children: [
                  ReportTypeCard(
                    type: ReportType.attendance,
                    icon: Icons.people_outline,
                    onTap: () {
                      context.push('/reports/config', extra: ReportType.attendance);
                    },
                  ),
                  ReportTypeCard(
                    type: ReportType.cutFill,
                    icon: Icons.terrain_outlined,
                    onTap: () {
                      context.push('/reports/config', extra: ReportType.cutFill);
                    },
                  ),
                  ReportTypeCard(
                    type: ReportType.inventory,
                    icon: Icons.inventory_2_outlined,
                    onTap: () {
                      context.push('/reports/config', extra: ReportType.inventory);
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Task 4: Create Report Config Page

**File: `lib/features/reporting/presentation/pages/report_config_page.dart`**
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mine_flow/core/constants/app_constants.dart';
import 'package:mine_flow/features/reporting/domain/entities/report_type.dart';
import 'package:mine_flow/features/reporting/presentation/bloc/report_cubit.dart';
import 'package:mine_flow/features/reporting/presentation/bloc/report_state.dart';
import 'package:mine_flow/features/reporting/presentation/widgets/date_range_selector.dart';
import 'package:mine_flow/features/reporting/presentation/widgets/report_summary_card.dart';
import 'package:printing/printing.dart';

class ReportConfigPage extends StatefulWidget {
  final ReportType reportType;

  const ReportConfigPage({super.key, required this.reportType});

  @override
  State<ReportConfigPage> createState() => _ReportConfigPageState();
}

class _ReportConfigPageState extends State<ReportConfigPage> {
  final TextEditingController _zoneController = TextEditingController();

  @override
  void initState() {
    super.initState();
    context.read<ReportCubit>().selectReportType(widget.reportType);
  }

  @override
  void dispose() {
    _zoneController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('Konfigurasi ${widget.reportType.displayName}'),
      ),
      body: BlocBuilder<ReportCubit, ReportState>(
        builder: (context, state) {
          if (state is ReportSuccess) {
            return _buildSuccessView(context, state, theme);
          }
          return _buildConfigForm(context, state, theme);
        },
      ),
    );
  }

  Widget _buildConfigForm(BuildContext context, ReportState state, ThemeData theme) {
    final cubit = context.read<ReportCubit>();
    final isLoading = state is ReportLoading;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Icon(
            _getIconForType(widget.reportType),
            size: 64,
            color: theme.colorScheme.primary,
          ),
          const SizedBox(height: 16),
          Text(
            widget.reportType.displayName,
            textAlign: TextAlign.center,
            style: theme.textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 32),
          
          DateRangeSelector(
            initialRange: cubit.state is ReportInitial ? (cubit as dynamic)._dateRange : (cubit as dynamic)._dateRange, // Simplified
            onChanged: (range) => cubit.setDateRange(range),
          ),
          const SizedBox(height: 24),
          
          if (widget.reportType == ReportType.cutFill) ...[
            TextFormField(
              controller: _zoneController,
              decoration: const InputDecoration(
                labelText: 'ID Zona (Opsional)',
                hintText: 'Biarkan kosong untuk semua zona',
                border: OutlineInputBorder(),
                isDense: true,
              ),
              onChanged: (value) => cubit.setZoneFilter(value.trim().isEmpty ? null : value.trim()),
            ),
            const SizedBox(height: 24),
          ],

          if (state is ReportError) ...[
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: theme.colorScheme.errorContainer,
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                state.message,
                style: TextStyle(color: theme.colorScheme.onErrorContainer),
              ),
            ),
            const SizedBox(height: 24),
          ],

          ElevatedButton(
            onPressed: isLoading
                ? null
                : () => cubit.generateReport(siteId: AppConstants.defaultSiteId),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
            ),
            child: isLoading
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Buat Laporan', style: TextStyle(fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  Widget _buildSuccessView(BuildContext context, ReportSuccess state, ThemeData theme) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          ReportSummaryCard(result: state.result),
          const SizedBox(height: 24),
          
          ElevatedButton.icon(
            onPressed: () {
              Printing.sharePdf(
                bytes: state.result.pdfBytes,
                filename: state.result.fileName,
              );
            },
            icon: const Icon(Icons.share),
            label: const Text('Bagikan PDF'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
            ),
          ),
          const SizedBox(height: 12),
          
          OutlinedButton.icon(
            onPressed: () {
              Printing.layoutPdf(
                onLayout: (format) async => state.result.pdfBytes,
                name: state.result.title,
              );
            },
            icon: const Icon(Icons.print),
            label: const Text('Cetak'),
            style: OutlinedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
            ),
          ),
          const SizedBox(height: 12),
          
          TextButton.icon(
            onPressed: () => context.read<ReportCubit>().resetReport(),
            icon: const Icon(Icons.refresh),
            label: const Text('Buat Ulang'),
          ),
        ],
      ),
    );
  }

  IconData _getIconForType(ReportType type) {
    switch (type) {
      case ReportType.attendance:
        return Icons.people_outline;
      case ReportType.cutFill:
        return Icons.terrain_outlined;
      case ReportType.inventory:
        return Icons.inventory_2_outlined;
    }
  }
}
```
*(Note: To avoid private field access issues, `DateRangeSelector` initialRange in `_buildConfigForm` can just use `DateRangeFilter.currentWeek()` or we can expose a getter in `ReportCubit`. For simplicity, add a getter in Cubit or just use a default initial).* Let's assume you fix `(cubit as dynamic)._dateRange` to use a public getter if needed, but for MVP it's acceptable to just use `DateRangeFilter.currentWeek()` in the widget.

Wait, add this getter to `ReportCubit`:
```dart
  DateRangeFilter get currentRange => _dateRange;
```
And in `ReportConfigPage`:
```dart
  initialRange: cubit.currentRange,
```

Please apply that small fix to `ReportCubit` when writing the code.

## Verification

Run:
```bash
cd Code/mine-flow-app
flutter analyze lib/features/reporting/presentation/
```
No errors should be found.

## Definition of done
- [ ] `ReportState` and `ReportCubit` created.
- [ ] `ReportTypeCard`, `DateRangeSelector`, and `ReportSummaryCard` widgets created.
- [ ] `ReportDashboardPage` and `ReportConfigPage` created.
- [ ] `flutter analyze` passes.

## Next
Move to substep 9.3: *"run substep 9.3"*.
