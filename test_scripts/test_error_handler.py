#!/usr/bin/env python3
"""
Test script for Error Handler functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'windmill-scripts'))

from error_handler import main as error_handler_main, ErrorHandler, ErrorCategory, ErrorSeverity
import json

def test_error_handler():
    """Test the error handler with various error scenarios"""
    
    print("🚨 Testing Error Handler...")
    print("=" * 50)
    
    # Sample statistics from previous stages
    csv_stats = {
        "total_rows": 10,
        "valid_rows": 8,
        "parse_errors_count": 2,
        "validation_errors_count": 0
    }
    
    transformation_stats = {
        "successful_count": 7,
        "failed_count": 1,
        "validation_error_count": 2
    }
    
    api_stats = {
        "successful_count": 6,
        "failed_count": 4,
        "api_errors": {
            "network_error": 2,
            "validation_error": 1,
            "server_error": 1
        }
    }
    
    # Sample errors from different stages
    parse_errors = [
        {
            "row_number": 3,
            "error": "Invalid CSV format",
            "row_data": {"company_name": "Bad,Corp", "email": "bad@corp"},
            "error_type": "parsing"
        },
        {
            "row_number": 7,
            "error": "Missing required field",
            "row_data": {"company_name": "Incomplete Corp"},
            "error_type": "parsing"
        }
    ]
    
    transformation_errors = [
        {
            "row_index": 5,
            "error": "Transformation failed: Invalid email format",
            "data": {
                "company_name": "Bad Email Corp",
                "contact_email": "invalid-email"
            }
        }
    ]
    
    api_errors = [
        {
            "customer_index": 2,
            "customer_data": {
                "name": "Network Error Corp",
                "email": "network@error.com"
            },
            "error": "Network connection timeout",
            "error_type": "network_error",
            "status_code": 0,
            "retry_count": 3
        },
        {
            "customer_index": 4,
            "customer_data": {
                "name": "Server Error Corp",
                "email": "server@error.com"
            },
            "error": "Internal server error",
            "error_type": "server_error",
            "status_code": 500,
            "retry_count": 2
        }
    ]
    
    print(f"📊 Test Data:")
    print(f"   CSV Stats: {csv_stats}")
    print(f"   Transformation Stats: {transformation_stats}")
    print(f"   API Stats: {api_stats}")
    print(f"   Parse Errors: {len(parse_errors)}")
    print(f"   Transformation Errors: {len(transformation_errors)}")
    print(f"   API Errors: {len(api_errors)}")
    print()
    
    try:
        # Test error handler
        result = error_handler_main(
            csv_stats=csv_stats,
            transformation_stats=transformation_stats,
            api_stats=api_stats,
            parse_errors=parse_errors,
            transformation_errors=transformation_errors,
            api_errors=api_errors
        )
        
        print("✅ Error Handler Results:")
        report = result['report']
        print(f"   Processing ID: {report['processing_id']}")
        print(f"   Duration: {report['duration_seconds']:.2f} seconds")
        print(f"   Overall Success: {report['overall_success']}")
        print(f"   Success Rate: {report['success_rate']:.1f}%")
        print(f"   Error Rate: {report['error_rate']:.1f}%")
        print()
        
        # Show error summary
        error_summary = result['error_summary']
        print("📊 Error Summary:")
        print(f"   Total Errors: {error_summary['total_errors']}")
        print(f"   Total Warnings: {error_summary['total_warnings']}")
        
        if error_summary['by_category']:
            print("   Errors by Category:")
            for category, count in error_summary['by_category'].items():
                print(f"     {category}: {count}")
        
        if error_summary['by_severity']:
            print("   Errors by Severity:")
            for severity, count in error_summary['by_severity'].items():
                print(f"     {severity}: {count}")
        
        if error_summary['by_error_code']:
            print("   Errors by Code:")
            for code, count in error_summary['by_error_code'].items():
                print(f"     {code}: {count}")
        print()
        
        # Show failed rows
        failed_rows = result['failed_rows']
        if failed_rows:
            print("❌ Failed Rows:")
            for row in failed_rows[:3]:  # Show first 3
                print(f"   Row {row['row_index']}: {row['error_message']}")
                print(f"     Category: {row['error_category']}")
                print(f"     Severity: {row['error_severity']}")
                print(f"     Recoverable: {row['recoverable']}")
            print()
        
        # Show text summary
        text_summary = result['text_summary']
        print("📋 Text Summary:")
        print(text_summary)
        
        return result
        
    except Exception as e:
        print(f"❌ Error Handler Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_error_handler_individual():
    """Test individual error handler methods"""
    
    print("🔧 Testing Individual Error Handler Methods...")
    print("=" * 50)
    
    try:
        handler = ErrorHandler()
        
        # Test adding different types of errors
        handler.handle_csv_parsing_error(
            {"error": "Invalid format", "details": "test"},
            1
        )
        
        handler.handle_validation_error(
            ["Invalid email", "Missing phone"],
            2,
            {"email": "bad@email", "name": "Test Corp"}
        )
        
        handler.handle_transformation_error(
            "Transformation failed",
            3,
            {"company_name": "Bad Corp"}
        )
        
        handler.handle_api_error(
            {"error": "API timeout", "error_type": "network_error"},
            4,
            {"name": "API Error Corp"}
        )
        
        handler.handle_system_error(
            "System configuration error",
            {"config": "database"}
        )
        
        handler.add_warning("This is a test warning", {"test": True})
        
        # Get error summary
        summary = handler.get_error_summary()
        
        print("✅ Individual Error Handler Results:")
        print(f"   Total Errors: {summary['total_errors']}")
        print(f"   Total Warnings: {summary['total_warnings']}")
        
        if summary['by_category']:
            print("   Categories:")
            for category, count in summary['by_category'].items():
                print(f"     {category}: {count}")
        
        if summary['by_severity']:
            print("   Severities:")
            for severity, count in summary['by_severity'].items():
                print(f"     {severity}: {count}")
        
        # Get failed rows
        failed_rows = handler.get_failed_rows()
        print(f"   Failed Rows: {len(failed_rows)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Individual Error Handler Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handler_export():
    """Test error handler export functionality"""
    
    print("📤 Testing Error Handler Export...")
    print("=" * 50)
    
    try:
        handler = ErrorHandler()
        
        # Add some test errors
        handler.handle_csv_parsing_error({"error": "test"}, 1)
        handler.add_warning("test warning")
        
        # Create a mock report
        from error_handler import ProcessingReport
        report = ProcessingReport(
            processing_id="test_123",
            start_time="2024-01-15T10:00:00Z",
            end_time="2024-01-15T10:01:00Z",
            duration_seconds=60.0,
            total_csv_rows=10,
            valid_csv_rows=8,
            successful_transformations=7,
            failed_transformations=1,
            validation_errors=2,
            successful_api_calls=6,
            failed_api_calls=4,
            errors=handler.errors,
            warnings=handler.warnings,
            overall_success=False,
            success_rate=60.0,
            error_rate=40.0
        )
        
        # Test JSON export
        json_export = handler.export_report(report, "json")
        json_data = json.loads(json_export)
        
        print("✅ JSON Export Test:")
        print(f"   Export Length: {len(json_export)} characters")
        print(f"   Processing ID: {json_data['processing_id']}")
        print(f"   Success Rate: {json_data['success_rate']}%")
        print()
        
        # Test text export
        text_export = handler.export_report(report, "summary")
        
        print("✅ Text Export Test:")
        print(f"   Export Length: {len(text_export)} characters")
        print(f"   Contains Summary: {'CSV Processing Report' in text_export}")
        print(f"   Contains Statistics: {'Total CSV Rows' in text_export}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error Handler Export Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test main error handler
    result1 = test_error_handler()
    
    # Test individual methods
    result2 = test_error_handler_individual()
    
    # Test export functionality
    result3 = test_error_handler_export()
    
    # Evaluate results
    if result1 and result1['report']['overall_success'] == False:  # Expected to fail due to test errors
        print("🎉 Error Handler Test PASSED!")
    else:
        print("💥 Error Handler Test FAILED!")
        sys.exit(1)
    
    if result2:
        print("🎉 Individual Error Handler Test PASSED!")
    else:
        print("💥 Individual Error Handler Test FAILED!")
        sys.exit(1)
    
    if result3:
        print("🎉 Error Handler Export Test PASSED!")
    else:
        print("💥 Error Handler Export Test FAILED!")
        sys.exit(1)
    
    print("\n🎯 Error Handler Testing Complete!")
    print("Note: Expected failures validate error handling works correctly.")
