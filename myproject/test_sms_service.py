#!/usr/bin/env python3
"""
Test script for SMS service
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from bulkSMS.services.sms_service import send_bulk_sms, validate_phone_number

def test_phone_validation():
    """Test phone number validation"""
    test_numbers = [
        "0712345678",
        "+254712345678", 
        "712345678",
        "+1234567890"
    ]
    
    print("Testing phone number validation:")
    for number in test_numbers:
        formatted = validate_phone_number(number)
        print(f"  {number} -> {formatted}")

def test_sms_sending():
    """Test SMS sending (use sandbox numbers for testing)"""
    # For sandbox testing, use these test numbers
    test_recipients = [
        "+254708374149",  # Sandbox test number
        "+254708374150",  # Sandbox test number
    ]
    
    test_message = "Hello from ReactLife SMS Test! This is a test message."
    
    print(f"\nTesting SMS sending to: {test_recipients}")
    print(f"Message: {test_message}")
    
    result = send_bulk_sms(test_recipients, test_message)
    
    print(f"\nSMS Result: {result}")
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Success: {result.get('message', 'SMS sent')}")
        print(f"   Successful: {result.get('successful', 0)}")
        print(f"   Failed: {result.get('failed', 0)}")

if __name__ == "__main__":
    print("🧪 Testing SMS Service...")
    print("=" * 50)
    
    test_phone_validation()
    test_sms_sending()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

