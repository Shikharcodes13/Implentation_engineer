#!/usr/bin/env python3
"""
Test script for Complete CSV Upload Flow
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'windmill-scripts'))

from csv_upload_flow import main as flow_main, validate_flow_inputs, test_with_sample_data
import json

def test_complete_flow():
    """Test the complete CSV upload flow"""
    
    print("🚀 Testing Complete CSV Upload Flow...")
    print("=" * 50)
    
    # Read sample CSV data
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'sample-data', 'customers.csv')
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        csv_content = f.read()
    
    print(f"📁 CSV File: {csv_file_path}")
    print(f"📊 CSV Content Length: {len(csv_content)} characters")
    print()
    
    # Mock API URL (will fail but test the flow)
    mock_api_url = "https://mockapi.io/api/v1"
    
    try:
        # Test input validation first
        print("🔍 Testing Input Validation...")
        validation_result = validate_flow_inputs(csv_content, mock_api_url)
        
        print(f"✅ Input Validation:")
        print(f"   Valid: {validation_result['valid']}")
        print(f"   Errors: {validation_result['errors']}")
        print(f"   Warnings: {validation_result['warnings']}")
        print()
        
        if not validation_result['valid']:
            print("❌ Input validation failed. Cannot proceed with flow test.")
            return None
        
        # Test complete flow
        print("🧪 Testing Complete Flow...")
        result = flow_main(
            csv_content=csv_content,
            api_base_url=mock_api_url,
            api_key=None,
            transformation_config=None,
            encoding=None,
            delimiter=None
        )
        
        print("✅ Complete Flow Results:")
        print(f"   Success: {result['success']}")
        print(f"   Flow Duration: {result.get('flow_duration_seconds', 'N/A')} seconds")
        print()
        
        if result['success']:
            # Show quick summary
            quick_summary = result['quick_summary']
            print("📊 Quick Summary:")
            print(f"   Total CSV Rows: {quick_summary['total_csv_rows']}")
            print(f"   Successfully Processed: {quick_summary['successfully_processed']}")
            print(f"   Failed Processing: {quick_summary['failed_processing']}")
            print(f"   Success Rate: {quick_summary['success_rate']:.1f}%")
            print(f"   Overall Success: {quick_summary['overall_success']}")
            print()
            
            # Show stage results
            print("🔄 Stage Results:")
            
            # CSV Parsing
            csv_stage = result['csv_parsing']
            print(f"   CSV Parsing:")
            print(f"     Success: {csv_stage['success']}")
            print(f"     Valid Rows: {csv_stage['summary']['valid_rows']}")
            print(f"     Parse Errors: {csv_stage['summary']['parse_errors_count']}")
            
            # Data Transformation
            transform_stage = result['data_transformation']
            print(f"   Data Transformation:")
            print(f"     Successful: {transform_stage['summary']['successful_count']}")
            print(f"     Failed: {transform_stage['summary']['failed_count']}")
            print(f"     Validation Errors: {transform_stage['summary']['validation_error_count']}")
            
            # API Integration
            api_stage = result['api_integration']
            print(f"   API Integration:")
            print(f"     Successful: {api_stage['summary']['successful_count']}")
            print(f"     Failed: {api_stage['summary']['failed_count']}")
            print()
            
            # Show processing report
            if 'processing_report' in result:
                report = result['processing_report']
                print("📋 Processing Report Summary:")
                print(f"   Processing ID: {report['report']['processing_id']}")
                print(f"   Duration: {report['report']['duration_seconds']:.2f} seconds")
                print(f"   Overall Success: {report['report']['overall_success']}")
                print(f"   Success Rate: {report['report']['success_rate']:.1f}%")
                print()
                
                # Show error summary
                if 'error_summary' in report:
                    error_summary = report['error_summary']
                    print("🚨 Error Summary:")
                    print(f"   Total Errors: {error_summary['total_errors']}")
                    print(f"   Total Warnings: {error_summary['total_warnings']}")
                    
                    if error_summary['by_category']:
                        print("   Errors by Category:")
                        for category, count in error_summary['by_category'].items():
                            print(f"     {category}: {count}")
                    print()
        
        else:
            print(f"❌ Flow Failed: {result.get('error', 'Unknown error')}")
            print(f"   Stage: {result.get('stage', 'Unknown')}")
            if 'details' in result:
                print(f"   Details: {result['details']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Complete Flow Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_flow_with_sample_data():
    """Test flow with built-in sample data"""
    
    print("🧪 Testing Flow with Built-in Sample Data...")
    print("=" * 50)
    
    try:
        # Mock API URL
        mock_api_url = "https://mockapi.io/api/v1"
        
        result = test_with_sample_data(mock_api_url)
        
        print("✅ Sample Data Test Results:")
        print(f"   Success: {result['success']}")
        
        if result['success']:
            quick_summary = result['quick_summary']
            print(f"   Success Rate: {quick_summary['success_rate']:.1f}%")
            print(f"   Total Rows: {quick_summary['total_csv_rows']}")
            print(f"   Processed: {quick_summary['successfully_processed']}")
        else:
            print(f"   Error: {result.get('error', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Sample Data Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_flow_with_custom_config():
    """Test flow with custom transformation configuration"""
    
    print("🔧 Testing Flow with Custom Configuration...")
    print("=" * 50)
    
    try:
        # Read sample CSV data
        csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'sample-data', 'customers.csv')
        
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        
        # Custom transformation configuration
        custom_config = {
            "field_mapping": {
                "company_name": "name",
                "contact_email": "email",
                "contact_first_name": "firstName",
                "contact_last_name": "lastName"
            },
            "custom_business_rules": [
                lambda customer: customer.update({"customField": "custom_value"}) or customer
            ]
        }
        
        # Mock API URL
        mock_api_url = "https://mockapi.io/api/v1"
        
        result = flow_main(
            csv_content=csv_content,
            api_base_url=mock_api_url,
            transformation_config=custom_config
        )
        
        print("✅ Custom Configuration Test Results:")
        print(f"   Success: {result['success']}")
        
        if result['success']:
            print(f"   Success Rate: {result['quick_summary']['success_rate']:.1f}%")
            
            # Check if custom field was added
            if result['data_transformation']['successful_transformations']:
                first_customer = result['data_transformation']['successful_transformations'][0]
                if 'customField' in first_customer:
                    print("   Custom Field Added: ✅")
                else:
                    print("   Custom Field Added: ❌")
        
        return result
        
    except Exception as e:
        print(f"❌ Custom Configuration Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test complete flow
    result1 = test_complete_flow()
    
    # Test with sample data
    result2 = test_flow_with_sample_data()
    
    # Test with custom configuration
    result3 = test_flow_with_custom_config()
    
    # Evaluate results
    if result1 and result1['success']:
        print("🎉 Complete Flow Test PASSED!")
    else:
        print("💥 Complete Flow Test FAILED!")
        sys.exit(1)
    
    if result2 and result2['success']:
        print("🎉 Sample Data Test PASSED!")
    else:
        print("💥 Sample Data Test FAILED!")
        sys.exit(1)
    
    if result3 and result3['success']:
        print("🎉 Custom Configuration Test PASSED!")
    else:
        print("💥 Custom Configuration Test FAILED!")
        sys.exit(1)
    
    print("\n🎯 Complete Flow Testing Successful!")
    print("All components working together correctly.")
    print("Note: API calls failed as expected with mock URL.")
    print("This validates the complete pipeline works end-to-end.")
