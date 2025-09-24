import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class ErrorSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ErrorCategory(Enum):
    CSV_PARSING = "csv_parsing"
    DATA_VALIDATION = "data_validation"
    TRANSFORMATION = "transformation"
    API_INTEGRATION = "api_integration"
    SYSTEM = "system"

@dataclass
class ErrorRecord:
    """Individual error record with context and metadata."""
    timestamp: str
    severity: ErrorSeverity
    category: ErrorCategory
    message: str
    details: Dict[str, Any]
    row_index: Optional[int] = None
    customer_data: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    recoverable: bool = True

@dataclass
class ProcessingReport:
    """Comprehensive processing report with statistics and errors."""
    processing_id: str
    start_time: str
    end_time: str
    duration_seconds: float
    
    # Input statistics
    total_csv_rows: int
    valid_csv_rows: int
    
    # Processing statistics
    successful_transformations: int
    failed_transformations: int
    validation_errors: int
    
    # API statistics
    successful_api_calls: int
    failed_api_calls: int
    
    # Error tracking
    errors: List[ErrorRecord]
    warnings: List[str]
    
    # Summary
    overall_success: bool
    success_rate: float
    error_rate: float

class ErrorHandler:
    """
    Comprehensive error handling and reporting system.
    Tracks errors across all processing stages and generates detailed reports.
    """
    
    def __init__(self):
        self.errors: List[ErrorRecord] = []
        self.warnings: List[str] = []
        self.start_time = datetime.utcnow()
        self.processing_id = f"proc_{int(self.start_time.timestamp())}"
    
    def add_error(
        self,
        message: str,
        category: ErrorCategory,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        details: Dict[str, Any] = None,
        row_index: Optional[int] = None,
        customer_data: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        recoverable: bool = True
    ):
        """Add an error record to the handler."""
        
        error_record = ErrorRecord(
            timestamp=datetime.utcnow().isoformat(),
            severity=severity,
            category=category,
            message=message,
            details=details or {},
            row_index=row_index,
            customer_data=customer_data,
            error_code=error_code,
            recoverable=recoverable
        )
        
        self.errors.append(error_record)
    
    def add_warning(self, message: str, details: Dict[str, Any] = None):
        """Add a warning to the handler."""
        warning = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "details": details or {}
        }
        self.warnings.append(warning)
    
    def handle_csv_parsing_error(self, error_data: Dict[str, Any], row_number: int):
        """Handle CSV parsing errors."""
        self.add_error(
            message=f"CSV parsing error in row {row_number}",
            category=ErrorCategory.CSV_PARSING,
            severity=ErrorSeverity.HIGH,
            details=error_data,
            row_index=row_number,
            error_code="CSV_PARSE_ERROR"
        )
    
    def handle_validation_error(self, validation_errors: List[str], row_index: int, customer_data: Dict[str, Any]):
        """Handle data validation errors."""
        self.add_error(
            message=f"Validation failed for row {row_index}",
            category=ErrorCategory.DATA_VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            details={"validation_errors": validation_errors},
            row_index=row_index,
            customer_data=customer_data,
            error_code="VALIDATION_ERROR"
        )
    
    def handle_transformation_error(self, error_message: str, row_index: int, csv_data: Dict[str, Any]):
        """Handle transformation errors."""
        self.add_error(
            message=f"Transformation failed for row {row_index}",
            category=ErrorCategory.TRANSFORMATION,
            severity=ErrorSeverity.HIGH,
            details={"transformation_error": error_message},
            row_index=row_index,
            customer_data=csv_data,
            error_code="TRANSFORMATION_ERROR"
        )
    
    def handle_api_error(self, api_error: Dict[str, Any], customer_index: int, customer_data: Dict[str, Any]):
        """Handle API integration errors."""
        severity = ErrorSeverity.HIGH
        if api_error.get("error_type") == "validation_error":
            severity = ErrorSeverity.MEDIUM
        elif api_error.get("error_type") == "rate_limit_error":
            severity = ErrorSeverity.LOW
        
        self.add_error(
            message=f"API call failed for customer {customer_index}",
            category=ErrorCategory.API_INTEGRATION,
            severity=severity,
            details=api_error,
            row_index=customer_index,
            customer_data=customer_data,
            error_code=api_error.get("error_type", "API_ERROR").upper()
        )
    
    def handle_system_error(self, error_message: str, error_details: Dict[str, Any] = None):
        """Handle system-level errors."""
        self.add_error(
            message=error_message,
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            details=error_details or {},
            recoverable=False,
            error_code="SYSTEM_ERROR"
        )
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors by category and severity."""
        summary = {
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "by_category": {},
            "by_severity": {},
            "by_error_code": {}
        }
        
        for error in self.errors:
            # By category
            category = error.category.value
            if category not in summary["by_category"]:
                summary["by_category"][category] = 0
            summary["by_category"][category] += 1
            
            # By severity
            severity = error.severity.value
            if severity not in summary["by_severity"]:
                summary["by_severity"][severity] = 0
            summary["by_severity"][severity] += 1
            
            # By error code
            if error.error_code:
                if error.error_code not in summary["by_error_code"]:
                    summary["by_error_code"][error.error_code] = 0
                summary["by_error_code"][error.error_code] += 1
        
        return summary
    
    def get_failed_rows(self) -> List[Dict[str, Any]]:
        """Get list of rows that failed processing with details."""
        failed_rows = []
        
        for error in self.errors:
            if error.row_index is not None:
                failed_rows.append({
                    "row_index": error.row_index,
                    "error_message": error.message,
                    "error_category": error.category.value,
                    "error_severity": error.severity.value,
                    "customer_data": error.customer_data,
                    "error_details": error.details,
                    "recoverable": error.recoverable
                })
        
        return failed_rows
    
    def generate_report(
        self,
        csv_stats: Dict[str, Any],
        transformation_stats: Dict[str, Any],
        api_stats: Dict[str, Any]
    ) -> ProcessingReport:
        """Generate comprehensive processing report."""
        
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()
        
        total_processed = csv_stats.get("valid_rows", 0)
        successful_count = api_stats.get("successful_count", 0)
        failed_count = api_stats.get("failed_count", 0)
        
        success_rate = (successful_count / total_processed * 100) if total_processed > 0 else 0
        error_rate = (len(self.errors) / total_processed * 100) if total_processed > 0 else 0
        
        overall_success = (
            len(self.errors) == 0 or 
            all(error.severity in [ErrorSeverity.LOW, ErrorSeverity.INFO] for error in self.errors)
        )
        
        return ProcessingReport(
            processing_id=self.processing_id,
            start_time=self.start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_seconds=duration,
            
            total_csv_rows=csv_stats.get("total_rows", 0),
            valid_csv_rows=csv_stats.get("valid_rows", 0),
            
            successful_transformations=transformation_stats.get("successful_count", 0),
            failed_transformations=transformation_stats.get("failed_count", 0),
            validation_errors=transformation_stats.get("validation_error_count", 0),
            
            successful_api_calls=api_stats.get("successful_count", 0),
            failed_api_calls=api_stats.get("failed_count", 0),
            
            errors=self.errors,
            warnings=self.warnings,
            
            overall_success=overall_success,
            success_rate=success_rate,
            error_rate=error_rate
        )
    
    def export_report(self, report: ProcessingReport, format: str = "json") -> str:
        """Export report in specified format."""
        
        if format == "json":
            # Convert to dictionary for JSON serialization
            report_dict = asdict(report)
            
            # Convert enum values to strings
            for error in report_dict["errors"]:
                error["severity"] = error["severity"].value
                error["category"] = error["category"].value
            
            return json.dumps(report_dict, indent=2, default=str)
        
        elif format == "summary":
            return self._generate_text_summary(report)
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _generate_text_summary(self, report: ProcessingReport) -> str:
        """Generate human-readable text summary."""
        
        summary_lines = [
            f"CSV Processing Report - {report.processing_id}",
            f"Processing Time: {report.duration_seconds:.2f} seconds",
            "",
            "=== INPUT STATISTICS ===",
            f"Total CSV Rows: {report.total_csv_rows}",
            f"Valid CSV Rows: {report.valid_csv_rows}",
            "",
            "=== PROCESSING STATISTICS ===",
            f"Successful Transformations: {report.successful_transformations}",
            f"Failed Transformations: {report.failed_transformations}",
            f"Validation Errors: {report.validation_errors}",
            "",
            "=== API STATISTICS ===",
            f"Successful API Calls: {report.successful_api_calls}",
            f"Failed API Calls: {report.failed_api_calls}",
            "",
            "=== OVERALL RESULTS ===",
            f"Success Rate: {report.success_rate:.1f}%",
            f"Error Rate: {report.error_rate:.1f}%",
            f"Overall Success: {'YES' if report.overall_success else 'NO'}",
            ""
        ]
        
        if report.errors:
            error_summary = self.get_error_summary()
            summary_lines.extend([
                "=== ERROR SUMMARY ===",
                f"Total Errors: {error_summary['total_errors']}",
                f"Total Warnings: {error_summary['total_warnings']}",
                ""
            ])
            
            if error_summary["by_category"]:
                summary_lines.append("Errors by Category:")
                for category, count in error_summary["by_category"].items():
                    summary_lines.append(f"  - {category}: {count}")
                summary_lines.append("")
            
            if error_summary["by_severity"]:
                summary_lines.append("Errors by Severity:")
                for severity, count in error_summary["by_severity"].items():
                    summary_lines.append(f"  - {severity}: {count}")
                summary_lines.append("")
        
        if report.warnings:
            summary_lines.extend([
                "=== WARNINGS ===",
                *[f"- {warning['message']}" for warning in report.warnings],
                ""
            ])
        
        return "\n".join(summary_lines)

def main(
    csv_stats: Dict[str, Any],
    transformation_stats: Dict[str, Any],
    api_stats: Dict[str, Any],
    parse_errors: List[Dict[str, Any]] = None,
    transformation_errors: List[Dict[str, Any]] = None,
    api_errors: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Main function for error handling and report generation.
    
    Args:
        csv_stats: CSV processing statistics
        transformation_stats: Transformation processing statistics
        api_stats: API processing statistics
        parse_errors: List of CSV parsing errors
        transformation_errors: List of transformation errors
        api_errors: List of API errors
    
    Returns:
        Comprehensive processing report
    """
    
    handler = ErrorHandler()
    
    # Process CSV parsing errors
    if parse_errors:
        for error in parse_errors:
            handler.handle_csv_parsing_error(error, error.get("row_number", 0))
    
    # Process transformation errors
    if transformation_errors:
        for error in transformation_errors:
            handler.handle_transformation_error(
                error.get("error", "Unknown transformation error"),
                error.get("row_index", 0),
                error.get("data", {})
            )
    
    # Process API errors
    if api_errors:
        for error in api_errors:
            handler.handle_api_error(
                error,
                error.get("customer_index", 0),
                error.get("customer_data", {})
            )
    
    # Generate comprehensive report
    report = handler.generate_report(csv_stats, transformation_stats, api_stats)
    
    return {
        "report": asdict(report),
        "error_summary": handler.get_error_summary(),
        "failed_rows": handler.get_failed_rows(),
        "json_export": handler.export_report(report, "json"),
        "text_summary": handler.export_report(report, "summary")
    }
