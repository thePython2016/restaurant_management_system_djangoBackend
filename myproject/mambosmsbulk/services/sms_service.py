import requests
import logging
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Get Mambo SMS credentials from Django settings
api_key = getattr(settings, 'MAMBOSMS_API_KEY', '')
base_url = "https://mambosms.co.tz" 



def validate_phone_number(phone_number):
    """Validate and format phone number for Africa's Talking"""
    # Remove any non-digit characters except +
    cleaned = ''.join(c for c in phone_number if c.isdigit() or c == '+')
    
    # If number doesn't start with +, assume it's a Kenyan number
    if not cleaned.startswith('+'):
        if cleaned.startswith('0'):
            # Convert 07... to +254...
            cleaned = '+255' + cleaned[1:]
        else:
            # Assume it's already a country code
            cleaned = '+' + cleaned
    
    return cleaned

def send_bulk_sms(recipients, message, sender_id="MAMBO SMS"):
    """
    Send bulk SMS using Mambo SMS API
    
    Args:
        recipients (list): List of phone numbers
        message (str): SMS message content
        sender_id (str): Sender ID (default: "MAMBO SMS")
    
    Returns:
        dict: Response from Mambo SMS API
    """
    try:
        # Check if API key is configured
        if not api_key:
            logger.error("Mambo SMS API key not configured")
            return {
                'success': False,
                'error': "SMS service not properly configured",
                'message': 'Please configure Mambo SMS API key in settings'
            }
        
        # Convert recipients list to comma-separated string
        mobile_numbers = ','.join(recipients)
        
        logger.info(f"Sending SMS to {len(recipients)} recipients: {recipients}")
        logger.info(f"Message: {message}")
        logger.info(f"Sender ID: {sender_id}")
        
        # Prepare the request payload for Mambo SMS API
        payload = {
            "sender_id": sender_id,
            "message": message,
            "mobile": mobile_numbers
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        # Make API request to Mambo SMS
        url = f"{base_url}/api/v1/sms/bulk"
        logger.info(f"Sending request to: {url}")
        logger.info(f"Payload: {payload}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response_data = response.json() if response.content else {}
        
        logger.info(f"Mambo SMS API Response: {response.status_code}, {response_data}")
        
        # Check if the request was successful
        if response.status_code == 200:
            logger.info(f"SMS sent successfully to {len(recipients)} recipients")
            return {
                'success': True,
                'message': f'SMS sent successfully to {len(recipients)} recipients',
                'total_recipients': len(recipients),
                'data': response_data,
                'raw_response': response_data
            }
        else:
            logger.error(f"Mambo SMS API error: {response.status_code}, {response_data}")
            return {
                'success': False,
                'error': f'API request failed with status {response.status_code}',
                'message': response_data.get('message', 'Unknown error'),
                'status_code': response.status_code,
                'raw_response': response_data
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error sending SMS: {str(e)}")
        return {
            'success': False,
            'error': f'Request failed: {str(e)}',
            'message': 'Failed to send SMS due to network error'
        }
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'message': 'Failed to send SMS due to technical error'
        }
