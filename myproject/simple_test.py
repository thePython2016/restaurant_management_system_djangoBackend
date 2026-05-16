import requests
import json

# Test registration
url = "http://127.0.0.1:8000/auth/registration/"
data = {
    "username": "testuser456",
    "email": "testuser456@example.com",
    "password1": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "1234567890"
}

print("Testing registration...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        print("✅ Registration successful!")
    else:
        print("❌ Registration failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")

