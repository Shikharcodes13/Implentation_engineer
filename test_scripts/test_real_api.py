#!/usr/bin/env python3
"""
Test script for Real MockAPI.io Integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'windmill-scripts'))

from csv_upload_flow import main as flow_main
import requests
import json

def test_mockapi_endpoint():
    """Test the MockAPI.io endpoint directly"""
    
    print("🌐 Testing MockAPI.io Endpoint...")
    print("=" * 50)
    
    api_url = "https://68d39755214be68f8c6666a0.mockapi.io/customers"
    
    try:
        # Test GET request to see current state
        print("📡 Testing GET request...")
        response = requests.get(api_url, timeout=10)
        
        print(f"✅ GET Response:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        print()
        
        # Test POST request with sample customer
        print("📤 Testing POST request...")
        sample_customer = {
            "name": "Test Company",
            "email": "test@example.com",
            "firstName": "Test",
            "lastName": "User",
            "phone": "+1-555-9999",
            "address": "123 Test St",
            "city": "Test City",
            "country": "USA",
            "postalCode": "12345",
            "taxId": "TAX-TEST-123",
            "companySize": "10-50"
        }
        
        response = requests.post(api_url, json=sample_customer, timeout=10)
        
        print(f"✅ POST Response:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        print()
        
        if response.status_code in [200, 201]:
            print("🎉 MockAPI.io endpoint is working correctly!")
            return True
        else:
            print(f"❌ POST request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ MockAPI.io test failed: {str(e)}")
        return False

def test_complete_flow_with_real_api():
    """Test the complete flow with real MockAPI.io endpoint"""
    
    print("🚀 Testing Complete Flow with Real API...")
    print("=" * 50)
    
    # Read sample CSV data
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'sample-data', 'customers.csv')
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        csv_content = f.read()
    
    # Use real MockAPI.io endpoint
    api_url = "https://68d39755214be68f8c6666a0.mockapi.io/api/v1"
    
    try:
        print(f"📁 CSV File: {csv_file_path}")
        print(f"🌐 API Endpoint: {api_url}")
        print(f"📊 CSV Content Length: {len(csv_content)} characters")
        print()
        
        # Test complete flow
        result = flow_main(
            csv_content=csv_content,
            api_base_url=api_url,
            api_key=None,
            transformation_config=None,
            encoding=None,
            delimiter=None
        )
        
        print("✅ Complete Flow Results with Real API:")
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
            
            # Data Transformation
            transform_stage = result['data_transformation']
            print(f"   Data Transformation:")
            print(f"     Successful: {transform_stage['summary']['successful_count']}")
            print(f"     Failed: {transform_stage['summary']['failed_count']}")
            
            # API Integration
            api_stage = result['api_integration']
            print(f"   API Integration:")
            print(f"     Successful: {api_stage['summary']['successful_count']}")
            print(f"     Failed: {api_stage['summary']['failed_count']}")
            print()
            
            # Show successful API creations
            if api_stage['successful_creations']:
                print("🎉 Successfully Created Customers:")
                for i, creation in enumerate(api_stage['successful_creations'][:3]):  # Show first 3
                    customer = creation['customer_data']
                    api_response = creation['api_response']
                    print(f"   {i+1}. {customer['name']} (ID: {api_response.get('id', 'N/A')})")
                    print(f"      Email: {customer['email']}")
                    print(f"      Retry Count: {creation['retry_count']}")
                print()
            
            # Show failed API calls
            if api_stage['failed_creations']:
                print("❌ Failed API Calls:")
                for i, failed in enumerate(api_stage['failed_creations'][:3]):  # Show first 3
                    customer = failed['customer_data']
                    print(f"   {i+1}. {customer['name']}: {failed['error']}")
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
        
        else:
            print(f"❌ Flow Failed: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Complete Flow Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def verify_customers_created():
    """Verify that customers were actually created in MockAPI.io"""
    
    print("🔍 Verifying Created Customers...")
    print("=" * 50)
    
    api_url = "https://68d39755214be68f8c6666a0.mockapi.io/customers"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            customers = response.json()
            
            print(f"✅ Verification Results:")
            print(f"   Total Customers in API: {len(customers)}")
            print()
            
            if customers:
                print("📊 Sample Created Customers:")
                for i, customer in enumerate(customers[:5]):  # Show first 5
                    print(f"   {i+1}. ID: {customer.get('id', 'N/A')}")
                    print(f"      Name: {customer.get('name', 'N/A')}")
                    print(f"      Email: {customer.get('email', 'N/A')}")
                    print(f"      Created: {customer.get('createdAt', 'N/A')}")
                    print()
            else:
                print("⚠️ No customers found in API")
            
            return len(customers)
        else:
            print(f"❌ Verification failed: Status {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return 0

if __name__ == "__main__":
    # Test MockAPI.io endpoint directly
    api_working = test_mockapi_endpoint()
    
    if api_working:
        # Test complete flow with real API
        result = test_complete_flow_with_real_api()
        
        if result and result['success']:
            # Verify customers were created
            customer_count = verify_customers_created()
            
            print("🎯 Final Results:")
            print(f"   MockAPI.io Working: ✅")
            print(f"   Complete Flow Success: ✅")
            print(f"   Customers Created: {customer_count}")
            print(f"   Success Rate: {result['quick_summary']['success_rate']:.1f}%")
            
            if result['quick_summary']['success_rate'] > 0:
                print("\n🎉 REAL API INTEGRATION TEST PASSED!")
                print("Your CSV upload system is working with the real MockAPI.io endpoint!")
            else:
                print("\n⚠️ API Integration Test Completed but No Customers Created")
                print("Check the API endpoint configuration and try again.")
        else:
            print("\n💥 Complete Flow Test Failed")
    else:
        print("\n💥 MockAPI.io Endpoint Test Failed")
        print("Please check your MockAPI.io configuration.")
