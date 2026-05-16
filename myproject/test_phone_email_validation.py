#!/usr/bin/env python
"""
Test script to verify email and phone number validation
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_existing_email_validation():
    """Test registration with existing email"""
    print("Testing existing email validation...")
    
    # First, create a user with email
    test_email = f"testemail{int(time.time())}@example.com"
    test_username = f"testuser{int(time.time())}"
    
    first_user_data = {
        "username": test_username,
        "email": test_email,
        "password1": "password123",
        "password2": "password123",
        "first_name": "First",
        "last_name": "User",
        "phone_number": "1111111111"
    }
    
    try:
        # Create first user
        response1 = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=first_user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response1.status_code != 201:
            print(f"❌ Failed to create first user: {response1.text}")
            return False
        
        print("✅ First user created successfully")
        
        # Try to create second user with same email
        second_user_data = {
            "username": f"seconduser{int(time.time())}",
            "email": test_email,  # Same email
            "password1": "password123",
            "password2": "password123",
            "first_name": "Second",
            "last_name": "User",
            "phone_number": "2222222222"
        }
        
        response2 = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=second_user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.text}")
        
        if response2.status_code == 400:
            data = response2.json()
            if 'email' in str(data) and 'field_errors' in data:
                print("✅ Existing email error handled correctly!")
                return True
            else:
                print("❌ Existing email not detected properly")
                return False
        else:
            print("❌ Expected 400 error for existing email")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_existing_phone_validation():
    """Test registration with existing phone number"""
    print("\nTesting existing phone number validation...")
    
    # First, create a user with phone number
    test_phone = f"123456789{int(time.time()) % 1000}"
    test_username = f"testuser{int(time.time())}"
    
    first_user_data = {
        "username": test_username,
        "email": f"user1{int(time.time())}@example.com",
        "password1": "password123",
        "password2": "password123",
        "first_name": "First",
        "last_name": "User",
        "phone_number": test_phone
    }
    
    try:
        # Create first user
        response1 = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=first_user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response1.status_code != 201:
            print(f"❌ Failed to create first user: {response1.text}")
            return False
        
        print("✅ First user created successfully")
        
        # Try to create second user with same phone number
        second_user_data = {
            "username": f"seconduser{int(time.time())}",
            "email": f"user2{int(time.time())}@example.com",
            "password1": "password123",
            "password2": "password123",
            "first_name": "Second",
            "last_name": "User",
            "phone_number": test_phone  # Same phone number
        }
        
        response2 = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=second_user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.text}")
        
        if response2.status_code == 400:
            data = response2.json()
            if 'phone_number' in str(data) and 'field_errors' in data:
                print("✅ Existing phone number error handled correctly!")
                return True
            else:
                print("❌ Existing phone number not detected properly")
                return False
        else:
            print("❌ Expected 400 error for existing phone number")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_field_error_structure():
    """Test that field errors are properly structured"""
    print("\nTesting field error structure...")
    
    # Test with invalid data to trigger field errors
    test_data = {
        "username": "",  # Empty username
        "email": "invalid-email",  # Invalid email
        "password1": "short",  # Short password
        "password2": "different",  # Mismatched password
        "first_name": "",
        "last_name": "",
        "phone_number": ""
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            data = response.json()
            if 'field_errors' in data and isinstance(data['field_errors'], dict):
                print("✅ Field errors structure is correct!")
                print(f"Field errors: {data['field_errors']}")
                return True
            else:
                print("❌ Field errors structure is incorrect")
                return False
        else:
            print("❌ Expected 400 error for invalid data")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Email and Phone Validation Test ===")
    
    # Test all scenarios
    email_test = test_existing_email_validation()
    phone_test = test_existing_phone_validation()
    structure_test = test_field_error_structure()
    
    print("\n=== Test Results ===")
    print(f"Email Validation: {'✅ PASS' if email_test else '❌ FAIL'}")
    print(f"Phone Validation: {'✅ PASS' if phone_test else '❌ FAIL'}")
    print(f"Error Structure: {'✅ PASS' if structure_test else '❌ FAIL'}")
    
    all_passed = email_test and phone_test and structure_test
    
    if all_passed:
        print("\n🎉 All validation tests passed! Email and phone number errors are working correctly.")
    else:
        print("\n⚠️  Some validation tests failed. Please check the configuration.")
