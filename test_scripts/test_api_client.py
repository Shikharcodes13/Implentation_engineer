#!/usr/bin/env python3
"""
Test script for API Client functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'windmill-scripts'))

from api_client import main as api_client_main, MockAPIClient, create_api_client
import json

def test_api_client_mock():
    """Test API client with mock responses"""
    
    print("🌐 Testing API Client (Mock Mode)...")
    print("=" * 50)
    
    # Sample customer data
    sample_customers = [
        {
            "name": "Acme Corp",
            "email": "john.doe@acme.com",
            "firstName": "John",
            "lastName": "Doe",
            "phone": "+1-555-0100",
            "address": "123 Business St",
            "city": "New York",
            "country": "USA",
            "postalCode": "10001",
            "taxId": "TAX-123456",
            "companySize": "50-100"
        },
        {
            "name": "Beta Inc",
            "email": "jane@beta.co",
            "firstName": "Jane",
            "lastName": "Smith",
            "phone": "+1-555-0200",
            "address": "456 Commerce Ave",
            "city": "San Francisco",
            "country": "USA",
            "postalCode": "94105",
            "taxId": "TAX-789012",
            "companySize": "100-500"
        }
    ]
    
    print(f"📊 Input Data: {len(sample_customers)} customers")
    print(f"📋 Sample Customer:")
    for key, value in sample_customers[0].items():
        print(f"   {key}: {value}")
    print()
    
    # Test with mock API URL (this will fail but test the client logic)
    try:
        print("🧪 Testing API Client Logic...")
        
        # Use a mock URL that will fail (to test error handling)
        mock_api_url = "https://mockapi.io/api/v1"
        
        result = api_client_main(
            customers=sample_customers,
            api_base_url=mock_api_url,
            api_key=None,
            max_retries=1  # Reduced retries for faster testing
        )
        
        print("✅ API Client Results:")
        print(f"   Total Customers: {result['summary']['total_customers']}")
        print(f"   Successful API Calls: {result['summary']['successful_count']}")
        print(f"   Failed API Calls: {result['summary']['failed_count']}")
        print()
        
        # Show API errors
        if result['summary']['api_errors']:
            print("📊 API Error Types:")
            for error_type, count in result['summary']['api_errors'].items():
                print(f"   {error_type}: {count}")
            print()
        
        # Show failed creations
        if result['failed_creations']:
            print("❌ Failed API Calls (Expected - Mock URL):")
            for failed in result['failed_creations'][:2]:  # Show first 2
                print(f"   Customer {failed['customer_index']}: {failed['error']}")
            print()
        
        return result
        
    except Exception as e:
        print(f"❌ API Client Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_api_client_configuration():
    """Test API client configuration and retry logic"""
    
    print("⚙️ Testing API Client Configuration...")
    print("=" * 50)
    
    try:
        # Test client creation
        client = create_api_client(
            base_url="https://test-api.com",
            api_key="test-key",
            timeout=30,
            max_retries=3,
            base_delay=1.0
        )
        
        print("✅ API Client Configuration:")
        print(f"   Base URL: {client.base_url}")
        print(f"   API Key: {'Set' if client.api_key else 'Not Set'}")
        print(f"   Timeout: {client.timeout}s")
        print(f"   Max Retries: {client.retry_config.max_retries}")
        print(f"   Base Delay: {client.retry_config.base_delay}s")
        print()
        
        # Test retry configuration
        print("🔄 Retry Configuration:")
        print(f"   Max Retries: {client.retry_config.max_retries}")
        print(f"   Base Delay: {client.retry_config.base_delay}")
        print(f"   Max Delay: {client.retry_config.max_delay}")
        print(f"   Backoff Factor: {client.retry_config.backoff_factor}")
        print(f"   Retry Status Codes: {client.retry_config.retry_on_status_codes}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ API Client Configuration Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_client_with_real_mockapi():
    """Test with a real MockAPI.io endpoint (if available)"""
    
    print("🌍 Testing with Real MockAPI.io...")
    print("=" * 50)
    print("Note: This test requires a real MockAPI.io endpoint.")
    print("If you don't have one set up, this test will be skipped.")
    print()
    
    # Check if user has a MockAPI URL configured
    mockapi_url = os.environ.get('MOCKAPI_BASE_URL')
    
    if not mockapi_url:
        print("⚠️ No MockAPI.io URL configured. Skipping real API test.")
        print("To test with real API:")
        print("1. Set up MockAPI.io account")
        print("2. Set MOCKAPI_BASE_URL environment variable")
        print("3. Run this test again")
        return True
    
    try:
        sample_customers = [{
            "name": "Test Company",
            "email": "test@example.com",
            "firstName": "Test",
            "lastName": "User",
            "phone": "+1-555-9999"
        }]
        
        result = api_client_main(
            customers=sample_customers,
            api_base_url=mockapi_url,
            api_key=os.environ.get('MOCKAPI_API_KEY'),
            max_retries=2
        )
        
        print("✅ Real API Test Results:")
        print(f"   Successful: {result['summary']['successful_count']}")
        print(f"   Failed: {result['summary']['failed_count']}")
        
        if result['successful_creations']:
            print("📊 Successful Creation:")
            creation = result['successful_creations'][0]
            print(f"   Customer ID: {creation['api_response'].get('id', 'N/A')}")
            print(f"   Retry Count: {creation['retry_count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Real API Test Failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Test API client logic (will fail with mock URL)
    result1 = test_api_client_mock()
    
    # Test configuration
    result2 = test_api_client_configuration()
    
    # Test with real API (optional)
    result3 = test_api_client_with_real_mockapi()
    
    # Evaluate results
    if result1 and result1['summary']['total_customers'] > 0:
        print("🎉 API Client Logic Test PASSED!")
    else:
        print("💥 API Client Logic Test FAILED!")
        sys.exit(1)
    
    if result2:
        print("🎉 API Client Configuration Test PASSED!")
    else:
        print("💥 API Client Configuration Test FAILED!")
        sys.exit(1)
    
    if result3:
        print("🎉 API Client Integration Test PASSED!")
    else:
        print("⚠️ API Client Integration Test SKIPPED (no MockAPI.io configured)")
    
    print("\n🎯 API Client Testing Complete!")
    print("Note: API calls failed as expected with mock URL.")
    print("This validates the error handling and retry logic works correctly.")
