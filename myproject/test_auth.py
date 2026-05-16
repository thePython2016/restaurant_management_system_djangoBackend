#!/usr/bin/env python
"""
Simple test script to verify registration and login functionality
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    """Test user registration"""
    print("Testing registration...")
    
    registration_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password1": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890",
        "phone": "1234567890"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Registration Status: {response.status_code}")
        print(f"Registration Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\nTesting login...")
    
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            data = response.json()
            if 'access' in data:
                print(f"✅ Access token received: {data['access'][:20]}...")
            return True
        else:
            print("❌ Login failed!")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def test_google_auth():
    """Test Google auth endpoint (without actual token)"""
    print("\nTesting Google auth endpoint...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/google/",
            json={"access_token": "test_token"},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Google Auth Status: {response.status_code}")
        print(f"Google Auth Response: {response.text}")
        
        # Should return 400 for invalid token, which is expected
        if response.status_code in [400, 401]:
            print("✅ Google auth endpoint responding correctly!")
            return True
        else:
            print("❌ Google auth endpoint not working as expected!")
            return False
            
    except Exception as e:
        print(f"❌ Google auth error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Authentication Endpoints")
    print("=" * 40)
    
    # Test registration
    reg_success = test_registration()
    
    # Test login
    login_success = test_login()
    
    # Test Google auth endpoint
    google_success = test_google_auth()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"Registration: {'✅ PASS' if reg_success else '❌ FAIL'}")
    print(f"Login: {'✅ PASS' if login_success else '❌ FAIL'}")
    print(f"Google Auth: {'✅ PASS' if google_success else '❌ FAIL'}")
    
    if reg_success and login_success:
        print("\n🎉 Authentication system is working correctly!")
    else:
        print("\n⚠️  Some authentication tests failed. Check the server logs.")

