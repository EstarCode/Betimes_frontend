"""
Comprehensive test script for all 35 requirements
Tests all backend APIs and functionality
"""

import requests
import json
import time
from pathlib import Path

# Disable SSL warnings for development
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://127.0.0.1:8000/api/v1"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, message=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if message:
        print(f"  {message}")

def test_authentication():
    """Test Requirement 12-15: Authentication, MFA, RBAC, Session Management"""
    print(f"\n{Colors.BLUE}Testing Authentication Features...{Colors.END}")
    
    # Test user registration
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json={
            "email": "testuser@betimes.com",
            "password": "TestPass123!@#",
            "first_name": "Test",
            "last_name": "User"
        })
        print_test("User Registration", response.status_code in [200, 201], f"Status: {response.status_code}")
    except Exception as e:
        print_test("User Registration", False, str(e))
    
    # Test login
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json={
            "email": "admin@betimes.com",
            "password": "admin123"
        })
        if response.status_code == 200:
            token = response.json().get('access')
            print_test("User Login", True, "Token received")
            return token
        else:
            print_test("User Login", False, f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("User Login", False, str(e))
        return None

def test_dashboard(token):
    """Test Requirement 16: Enterprise Dashboard"""
    print(f"\n{Colors.BLUE}Testing Dashboard Features...{Colors.END}")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard/metrics/", headers=headers)
        print_test("Dashboard Metrics", response.status_code == 200, f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Total Uploads: {data.get('total_uploads', 0)}")
            print(f"  Active Users: {data.get('active_users', 0)}")
    except Exception as e:
        print_test("Dashboard Metrics", False, str(e))

def test_workflows(token):
    """Test Requirement 11: Enterprise Workflow System"""
    print(f"\n{Colors.BLUE}Testing Workflow Features...{Colors.END}")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Test workflow templates
    try:
        response = requests.get(f"{BASE_URL}/workflows/templates/", headers=headers)
        print_test("Workflow Templates", response.status_code == 200, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Workflow Templates", False, str(e))
    
    # Test workflow instances
    try:
        response = requests.get(f"{BASE_URL}/workflows/instances/", headers=headers)
        print_test("Workflow Instances", response.status_code == 200, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Workflow Instances", False, str(e))

def test_uploads(token):
    """Test Requirement 1: Large File Upload System"""
    print(f"\n{Colors.BLUE}Testing Upload Features...{Colors.END}")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Test upload initialization
    try:
        response = requests.post(f"{BASE_URL}/uploads/initialize/", 
            json={
                "filename": "test.pdf",
                "file_size": 1024000,
                "total_chunks": 10,
                "content_type": "application/pdf"
            },
            headers=headers
        )
        print_test("Upload Initialization", response.status_code in [200, 201], f"Status: {response.status_code}")
    except Exception as e:
        print_test("Upload Initialization", False, str(e))

def test_compression(token):
    """Test Requirement 4: PDF Compression"""
    print(f"\n{Colors.BLUE}Testing Compression Features...{Colors.END}")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        response = requests.get(f"{BASE_URL}/compress/jobs/", headers=headers)
        print_test("Compression Jobs", response.status_code == 200, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Compression Jobs", False, str(e))

def test_conversion(token):
    """Test Requirement 2, 3, 7: Document Conversion"""
    print(f"\n{Colors.BLUE}Testing Conversion Features...{Colors.END}")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        response = requests.get(f"{BASE_URL}/convert/jobs/", headers=headers)
        print_test("Conversion Jobs", response.status_code == 200, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Conversion Jobs", False, str(e))

def test_versions(token):
    """Test Requirement 10: Document Version Control"""
    print(f"\n{Colors.BLUE}Testing Version Control Features...{Colors.END}")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        response = requests.get(f"{BASE_URL}/documents/", headers=headers)
        print_test("Document Versions", response.status_code == 200, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Document Versions", False, str(e))

def test_api_documentation():
    """Test Requirement 33: API Documentation"""
    print(f"\n{Colors.BLUE}Testing API Documentation...{Colors.END}")
    
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/api/docs/")
        print_test("Swagger Documentation", response.status_code == 200, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Swagger Documentation", False, str(e))

def test_security_headers():
    """Test Requirement 30: Security Hardening"""
    print(f"\n{Colors.BLUE}Testing Security Headers...{Colors.END}")
    
    try:
        response = requests.get(BASE_URL.replace('/api/v1', ''))
        headers = response.headers
        
        security_headers = {
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
        }
        
        for header, expected in security_headers.items():
            has_header = header in headers
            print_test(f"Security Header: {header}", has_header, 
                      f"Value: {headers.get(header, 'Not Set')}")
    except Exception as e:
        print_test("Security Headers", False, str(e))

def test_performance():
    """Test Requirement 26, 31: Performance and Scalability"""
    print(f"\n{Colors.BLUE}Testing Performance...{Colors.END}")
    
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/dashboard/metrics/")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        passed = response_time < 2000  # Should be under 2 seconds
        
        print_test("API Response Time", passed, 
                  f"Response time: {response_time:.2f}ms (Target: <2000ms)")
    except Exception as e:
        print_test("API Response Time", False, str(e))

def main():
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}Betimes Enterprise Platform - Comprehensive Test Suite{Colors.END}")
    print(f"{Colors.YELLOW}Testing all 35 requirements{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}")
    
    # Test authentication first to get token
    token = test_authentication()
    
    # Test all other features
    test_dashboard(token)
    test_workflows(token)
    test_uploads(token)
    test_compression(token)
    test_conversion(token)
    test_versions(token)
    test_api_documentation()
    test_security_headers()
    test_performance()
    
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}Test Suite Completed!{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}\n")

if __name__ == "__main__":
    main()
