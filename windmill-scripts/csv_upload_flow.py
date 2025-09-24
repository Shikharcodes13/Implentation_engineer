import json
from typing import Dict, Any, List, Optional
from datetime import datetime

def main(
    csv_content: str,
    api_base_url: str,
    api_key: Optional[str] = None,
    transformation_config: Dict[str, Any] = None,
    encoding: Optional[str] = None,
    delimiter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main orchestrator for CSV upload and processing flow.
    
    This function coordinates all processing stages:
    1. CSV parsing and validation
    2. Data transformation
    3. API integration
    4. Error handling and reporting
    
    Args:
        csv_content: Raw CSV content as string
        api_base_url: Base URL for MockAPI.io endpoint
        api_key: Optional API key for authentication
        transformation_config: Optional configuration for custom transformations
        encoding: Character encoding (auto-detected if None)
        delimiter: CSV delimiter (auto-detected if None)
    
    Returns:
        Complete processing results with detailed report
    """
    
    flow_start_time = datetime.utcnow()
    
    try:
        # Stage 1: CSV Parsing
        print("Starting CSV parsing...")
        csv_result = parse_csv_content(
            csv_content=csv_content,
            encoding=encoding,
            delimiter=delimiter
        )
        
        if not csv_result["success"]:
            return {
                "success": False,
                "error": "CSV parsing failed",
                "stage": "csv_parsing",
                "details": csv_result,
                "timestamp": flow_start_time.isoformat()
            }
        
        print(f"CSV parsing completed: {csv_result['summary']['valid_rows']} valid rows")
        
        # Stage 2: Data Transformation
        print("Starting data transformation...")
        transformation_result = transform_data(
            csv_data=csv_result["data"],
            transformation_config=transformation_config
        )
        
        print(f"Data transformation completed: {transformation_result['summary']['successful_count']} successful transformations")
        
        # Stage 3: API Integration
        print("Starting API integration...")
        api_result = create_customers_via_api(
            customers=transformation_result["successful_transformations"],
            api_base_url=api_base_url,
            api_key=api_key
        )
        
        print(f"API integration completed: {api_result['summary']['successful_count']} successful API calls")
        
        # Stage 4: Error Handling and Reporting
        print("Generating comprehensive report...")
        report_result = generate_processing_report(
            csv_stats=csv_result["summary"],
            transformation_stats=transformation_result["summary"],
            api_stats=api_result["summary"],
            parse_errors=csv_result["parse_errors"],
            transformation_errors=transformation_result["failed_transformations"],
            api_errors=api_result["failed_creations"]
        )
        
        flow_end_time = datetime.utcnow()
        flow_duration = (flow_end_time - flow_start_time).total_seconds()
        
        # Compile final results
        final_result = {
            "success": True,
            "flow_duration_seconds": flow_duration,
            "timestamp": flow_start_time.isoformat(),
            
            # Stage results
            "csv_parsing": {
                "success": csv_result["success"],
                "summary": csv_result["summary"],
                "validation": csv_result["validation"]
            },
            
            "data_transformation": {
                "summary": transformation_result["summary"],
                "successful_transformations": transformation_result["successful_transformations"],
                "failed_transformations": transformation_result["failed_transformations"]
            },
            
            "api_integration": {
                "summary": api_result["summary"],
                "successful_creations": api_result["successful_creations"],
                "failed_creations": api_result["failed_creations"]
            },
            
            # Comprehensive report
            "processing_report": report_result,
            
            # Quick summary for easy access
            "quick_summary": {
                "total_csv_rows": csv_result["summary"]["total_rows"],
                "successfully_processed": api_result["summary"]["successful_count"],
                "failed_processing": api_result["summary"]["failed_count"],
                "success_rate": (api_result["summary"]["successful_count"] / csv_result["summary"]["total_rows"] * 100) if csv_result["summary"]["total_rows"] > 0 else 0,
                "overall_success": report_result["report"]["overall_success"]
            }
        }
        
        print(f"Flow completed successfully in {flow_duration:.2f} seconds")
        print(f"Success rate: {final_result['quick_summary']['success_rate']:.1f}%")
        
        return final_result
        
    except Exception as e:
        flow_end_time = datetime.utcnow()
        flow_duration = (flow_end_time - flow_start_time).total_seconds()
        
        return {
            "success": False,
            "error": f"Flow execution failed: {str(e)}",
            "flow_duration_seconds": flow_duration,
            "timestamp": flow_start_time.isoformat(),
            "stage": "flow_orchestration"
        }

def parse_csv_content(csv_content: str, encoding: str = None, delimiter: str = None) -> Dict[str, Any]:
    """
    Parse CSV content using the CSV parser module.
    This is a wrapper around the csv_parser.main function.
    """
    # Import and call the CSV parser
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from csv_parser import main as csv_parser_main
    return csv_parser_main(csv_content, encoding, delimiter)

def transform_data(csv_data: List[Dict[str, Any]], transformation_config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Transform CSV data using the data transformer module.
    This is a wrapper around the data_transformer.main function.
    """
    # Import and call the data transformer
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from data_transformer import main as transformer_main
    return transformer_main(csv_data, transformation_config)

def create_customers_via_api(customers: List[Dict[str, Any]], api_base_url: str, api_key: str = None) -> Dict[str, Any]:
    """
    Create customers via API using the API client module.
    This is a wrapper around the api_client.main function.
    """
    # Import and call the API client
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from api_client import main as api_client_main
    return api_client_main(customers, api_base_url, api_key)

def generate_processing_report(
    csv_stats: Dict[str, Any],
    transformation_stats: Dict[str, Any],
    api_stats: Dict[str, Any],
    parse_errors: List[Dict[str, Any]] = None,
    transformation_errors: List[Dict[str, Any]] = None,
    api_errors: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate comprehensive processing report using the error handler module.
    This is a wrapper around the error_handler.main function.
    """
    # Import and call the error handler
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from error_handler import main as error_handler_main
    return error_handler_main(
        csv_stats=csv_stats,
        transformation_stats=transformation_stats,
        api_stats=api_stats,
        parse_errors=parse_errors,
        transformation_errors=transformation_errors,
        api_errors=api_errors
    )

def validate_flow_inputs(
    csv_content: str,
    api_base_url: str,
    api_key: str = None
) -> Dict[str, Any]:
    """
    Validate inputs before starting the flow.
    
    Args:
        csv_content: Raw CSV content
        api_base_url: API base URL
        api_key: Optional API key
    
    Returns:
        Validation result
    """
    errors = []
    warnings = []
    
    # Validate CSV content
    if not csv_content or not csv_content.strip():
        errors.append("CSV content is empty or missing")
    elif len(csv_content.strip()) < 50:
        warnings.append("CSV content seems too short - please verify the data")
    
    # Validate API URL
    if not api_base_url or not api_base_url.strip():
        errors.append("API base URL is required")
    elif not api_base_url.startswith(('http://', 'https://')):
        errors.append("API base URL must start with http:// or https://")
    
    # Check for common CSV patterns
    if csv_content:
        lines = csv_content.strip().split('\n')
        if len(lines) < 2:
            errors.append("CSV must have at least a header row and one data row")
        
        # Check for basic CSV structure
        if len(lines) > 0:
            first_line = lines[0]
            if ',' not in first_line and '\t' not in first_line:
                warnings.append("CSV doesn't appear to have standard delimiters (comma or tab)")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

# Convenience function for testing with sample data
def test_with_sample_data(api_base_url: str, api_key: str = None) -> Dict[str, Any]:
    """
    Test the flow with built-in sample data.
    
    Args:
        api_base_url: MockAPI.io base URL
        api_key: Optional API key
    
    Returns:
        Test results
    """
    
    # Sample CSV content
    sample_csv = """company_name,contact_email,contact_first_name,contact_last_name,phone_number,address,city,country,postal_code,tax_id,company_size
Acme Corp,john.doe@acme.com,John,Doe,+1-555-0100,123 Business St,New York,USA,10001,TAX-123456,50-100
Beta Inc,jane@beta.co,Jane,Smith,555.0200,456 Commerce Ave,San Francisco,USA,94105,TAX-789012,100-500
Gamma LLC,bob@gamma.io,Bob,Johnson,(555) 0300,789 Innovation Blvd,Austin,USA,73301,TAX-345678,10-50"""
    
    print("Running test with sample data...")
    
    # Validate inputs first
    validation = validate_flow_inputs(sample_csv, api_base_url, api_key)
    if not validation["valid"]:
        return {
            "success": False,
            "error": "Input validation failed",
            "validation_errors": validation["errors"]
        }
    
    # Run the main flow
    return main(
        csv_content=sample_csv,
        api_base_url=api_base_url,
        api_key=api_key
    )
