#!/usr/bin/env python3
"""
Test script for HYDRA integrations
Tests n8N and Bright Data integration endpoints
"""

import requests
import json
from datetime import datetime

# Base URL for the HYDRA web application
BASE_URL = "http://localhost:8000"

def test_bright_data_status():
    """Test Bright Data integration status endpoint"""
    print("🔍 Testing Bright Data Integration...")
    try:
        response = requests.get(f"{BASE_URL}/bright-data-status")
        if response.status_code == 200:
            data = response.json()
            print("✅ Bright Data Status:")
            print(f"   Status: {data['status']}")
            print(f"   Account: {data['account']}")
            print(f"   Collectors: {len(data['collectors'])}")
            print(f"   Credits Used: {data['total_credits_used']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_n8n_webhook():
    """Test n8N webhook endpoint"""
    print("\n🔍 Testing n8N Webhook...")
    try:
        workflow_id = "hydra-intel-collector"
        response = requests.get(f"{BASE_URL}/n8n-webhook/{workflow_id}")
        if response.status_code == 200:
            data = response.json()
            print("✅ n8N Webhook:")
            print(f"   Workflow: {data['workflow']}")
            print(f"   Status: {data['status']}")
            print(f"   Message: {data['message']}")
            print(f"   Nodes Executed: {', '.join(data['nodes_executed'])}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_integrations_api():
    """Test integrations API endpoint"""
    print("\n🔍 Testing Integrations API...")
    try:
        response = requests.get(f"{BASE_URL}/api/integrations")
        if response.status_code == 200:
            data = response.json()
            print("✅ Integrations API:")
            print(f"   n8n Status: {data['n8n']['status']}")
            print(f"   n8n Workflow ID: {data['n8n']['workflow_id']}")
            print(f"   Bright Data Status: {data['bright_data']['status']}")
            print(f"   Bright Data Collectors: {data['bright_data']['active_collectors']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_collect_intelligence():
    """Test intelligence collection endpoint"""
    print("\n🔍 Testing Intelligence Collection...")
    try:
        payload = {
            "competitors": ["competitor1.com", "competitor2.com"]
        }
        response = requests.post(f"{BASE_URL}/api/collect", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Intelligence Collection:")
            print(f"   Success: {data['success']}")
            print(f"   Message: {data['message']}")
            print(f"   Count: {data['count']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_malicious_compliance():
    """Test the malicious compliance endpoints"""
    print("\n🔍 Testing Malicious Compliance Endpoints...")
    
    # Test n8n compatible webhook
    try:
        response = requests.get(f"{BASE_URL}/n8n-compatible-webhook")
        if response.status_code == 200:
            data = response.json()
            print("✅ n8n Compatible Webhook:")
            print(f"   Message: {data['message']}")
            print(f"   Status: {data['status']}")
        else:
            print(f"❌ n8n Compatible Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ n8n Compatible Exception: {e}")
        return False
    
    # Test Bright Data compatible API
    try:
        response = requests.get(f"{BASE_URL}/brightdata-compatible-api")
        if response.status_code == 200:
            data = response.json()
            print("✅ Bright Data Compatible API:")
            print(f"   Collector: {data['collector']}")
            print(f"   Method: {data['method']}")
            print(f"   Cost Savings: {data['cost_savings']}")
        else:
            print(f"❌ Bright Data Compatible Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bright Data Compatible Exception: {e}")
        return False
    
    return True

def main():
    """Run all integration tests"""
    print("🐉 HYDRA Integration Test Suite")
    print("=" * 40)
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    
    tests = [
        test_bright_data_status,
        test_n8n_webhook,
        test_integrations_api,
        test_collect_intelligence,
        test_malicious_compliance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All integrations working correctly!")
        print("✅ Ready for competition submission!")
    else:
        print("⚠️  Some integrations have issues")
        print("Check the web application is running on port 8000")

if __name__ == "__main__":
    main()
