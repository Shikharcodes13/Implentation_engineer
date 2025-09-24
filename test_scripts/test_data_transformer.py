#!/usr/bin/env python3
"""
Test script for Data Transformer functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'windmill-scripts'))

from data_transformer import main as transformer_main, CustomerTransformer, create_custom_transformer

def test_data_transformer():
    """Test the data transformer with sample data"""
    
    print("🔄 Testing Data Transformer...")
    print("=" * 50)
    
    # Sample CSV data (from previous test)
    sample_csv_data = [
        {
            "company_name": "Acme Corp",
            "contact_email": "john.doe@acme.com",
            "contact_first_name": "John",
            "contact_last_name": "Doe",
            "phone_number": "+1-555-0100",
            "address": "123 Business St",
            "city": "New York",
            "country": "USA",
            "postal_code": "10001",
            "tax_id": "TAX-123456",
            "company_size": "50-100"
        },
        {
            "company_name": "Beta Inc",
            "contact_email": "jane@beta.co",
            "contact_first_name": "Jane",
            "contact_last_name": "Smith",
            "phone_number": "555.0200",
            "address": "456 Commerce Ave",
            "city": "San Francisco",
            "country": "USA",
            "postal_code": "94105",
            "tax_id": "TAX-789012",
            "company_size": "100-500"
        }
    ]
    
    print(f"📊 Input Data: {len(sample_csv_data)} rows")
    print(f"📋 Sample Input Row:")
    for key, value in sample_csv_data[0].items():
        print(f"   {key}: {value}")
    print()
    
    # Test default transformation
    try:
        print("🧪 Testing Default Transformation...")
        result = transformer_main(sample_csv_data)
        
        print("✅ Transformation Results:")
        print(f"   Successful Transformations: {result['summary']['successful_count']}")
        print(f"   Failed Transformations: {result['summary']['failed_count']}")
        print(f"   Validation Errors: {result['summary']['validation_error_count']}")
        print()
        
        # Show transformed data sample
        if result['successful_transformations']:
            print("📊 Sample Transformed Data (First Row):")
            first_customer = result['successful_transformations'][0]
            for key, value in first_customer.items():
                print(f"   {key}: {value}")
            print()
        
        # Show failed transformations if any
        if result['failed_transformations']:
            print("❌ Failed Transformations:")
            for failed in result['failed_transformations']:
                print(f"   Row {failed['row_index']}: {failed['error']}")
            print()
        
        # Show validation errors if any
        if result['validation_errors']:
            print("❌ Validation Errors:")
            for error in result['validation_errors']:
                print(f"   Row {error['row_index']}: {error['errors']}")
            print()
        
        return result
        
    except Exception as e:
        print(f"❌ Data Transformer Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_custom_transformer():
    """Test custom transformation rules"""
    
    print("🔧 Testing Custom Transformer...")
    print("=" * 50)
    
    # Sample data
    sample_data = [{
        "company_name": "Test Corp",
        "contact_email": "test@example.com",
        "contact_first_name": "Test",
        "contact_last_name": "User",
        "phone_number": "555-1234",
        "company_size": "startup"
    }]
    
    # Custom field mapping
    custom_mapping = {
        "company_name": "name",
        "contact_email": "email",
        "contact_first_name": "firstName",
        "contact_last_name": "lastName"
    }
    
    # Custom validation
    def validate_phone(phone: str) -> bool:
        return len(phone) >= 7  # More lenient validation
    
    # Custom transformation
    def normalize_company_name(name: str) -> str:
        return name.upper()
    
    # Custom business rule
    def add_segment(customer: dict) -> dict:
        size = customer.get("companySize", "").lower()
        if "startup" in size:
            customer["segment"] = "startup"
        else:
            customer["segment"] = "enterprise"
        return customer
    
    try:
        # Create custom transformer
        transformer = create_custom_transformer(
            field_mapping=custom_mapping,
            custom_validations={"phone": validate_phone},
            custom_transformations={"name": normalize_company_name},
            custom_business_rules=[add_segment]
        )
        
        # Test transformation
        result = transformer.transform_batch(sample_data)
        
        print("✅ Custom Transformation Results:")
        print(f"   Successful: {result['summary']['successful_count']}")
        print(f"   Failed: {result['summary']['failed_count']}")
        print()
        
        if result['successful_transformations']:
            print("📊 Custom Transformed Data:")
            customer = result['successful_transformations'][0]
            for key, value in customer.items():
                print(f"   {key}: {value}")
            print()
        
        return result
        
    except Exception as e:
        print(f"❌ Custom Transformer Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test default transformer
    result1 = test_data_transformer()
    
    # Test custom transformer
    result2 = test_custom_transformer()
    
    if result1 and result1['summary']['successful_count'] > 0:
        print("🎉 Data Transformer Test PASSED!")
    else:
        print("💥 Data Transformer Test FAILED!")
        sys.exit(1)
    
    if result2 and result2['summary']['successful_count'] > 0:
        print("🎉 Custom Transformer Test PASSED!")
    else:
        print("💥 Custom Transformer Test FAILED!")
        sys.exit(1)
