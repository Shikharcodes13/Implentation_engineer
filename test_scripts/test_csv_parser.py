#!/usr/bin/env python3
"""
Test script for CSV Parser functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'windmill-scripts'))

from csv_parser import main as csv_parser_main

def test_csv_parser():
    """Test the CSV parser with sample data"""
    
    print("🧪 Testing CSV Parser...")
    print("=" * 50)
    
    # Read sample CSV data
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'sample-data', 'customers.csv')
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        csv_content = f.read()
    
    print(f"📁 CSV File: {csv_file_path}")
    print(f"📊 CSV Content Length: {len(csv_content)} characters")
    print(f"📋 First 200 characters:")
    print(csv_content[:200] + "..." if len(csv_content) > 200 else csv_content)
    print()
    
    # Test CSV parsing
    try:
        result = csv_parser_main(csv_content)
        
        print("✅ CSV Parsing Results:")
        print(f"   Success: {result['success']}")
        print(f"   Total Rows: {result['summary']['total_rows']}")
        print(f"   Valid Rows: {result['summary']['valid_rows']}")
        print(f"   Parse Errors: {result['summary']['parse_errors_count']}")
        print(f"   Validation Errors: {result['summary']['validation_errors_count']}")
        print()
        
        # Show parsed data sample
        if result['data']:
            print("📊 Sample Parsed Data (First Row):")
            first_row = result['data'][0]
            for key, value in first_row.items():
                print(f"   {key}: {value}")
            print()
        
        # Show validation results
        if result['validation']:
            validation = result['validation']
            print("✅ Validation Results:")
            print(f"   Valid: {validation['valid']}")
            print(f"   Available Fields: {len(validation['available_fields'])}")
            print(f"   Missing Required: {validation['missing_required']}")
            print(f"   Unexpected Fields: {validation['unexpected_fields']}")
            print()
            
            # Show field coverage
            if validation['field_coverage']:
                print("📈 Field Coverage:")
                for field, coverage in validation['field_coverage'].items():
                    print(f"   {field}: {coverage['coverage_percentage']:.1f}% ({coverage['non_empty_rows']}/{coverage['total_rows']})")
                print()
        
        # Show errors if any
        if result['parse_errors']:
            print("❌ Parse Errors:")
            for error in result['parse_errors']:
                print(f"   Row {error.get('row_number', 'Unknown')}: {error.get('error', 'Unknown error')}")
            print()
        
        if result['validation']['errors']:
            print("❌ Validation Errors:")
            for error in result['validation']['errors']:
                print(f"   {error}")
            print()
        
        return result
        
    except Exception as e:
        print(f"❌ CSV Parser Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_csv_parser()
    
    if result and result['success']:
        print("🎉 CSV Parser Test PASSED!")
    else:
        print("💥 CSV Parser Test FAILED!")
        sys.exit(1)
