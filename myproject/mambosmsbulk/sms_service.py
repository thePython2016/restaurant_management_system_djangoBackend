import requests
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

class MamboSMSService:
    def __init__(self):
        self.base_url = os.getenv('MAMBO_SMS_BASE_URL', 'https://mambosms.co.tz')
        self.api_key = os.getenv('MAMBO_SMS_API_KEY')
        
        logger.info(f"MamboSMSService initialized with API key: {'***' if self.api_key else 'None'}, base_url: {self.base_url}")
        
    def send_bulk_sms(self, sender_id, message, mobile_numbers):
        """
        Send bulk SMS via Mambo SMS API by sending individual SMS to each number
        Args:
            sender_id: Your sender ID (string)
            message: SMS message content (string)
            mobile_numbers: List of mobile numbers or comma-separated string
        Returns:
            dict: Response with success status and data
        """
        if not self.api_key:
            logger.error("Mambo SMS API key not configured")
            return {
                'success': False,
                'error': 'API key not configured',
                'status_code': None,
                'data': None
            }

        # Use the same endpoint format as single SMS (which is working)
        url = f"{self.base_url}/api/v1/sms/single"
        logger.info(f"Using URL: {url}")
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }

        # Handle mobile numbers - convert to list if needed
        if isinstance(mobile_numbers, str):
            mobile_list = [num.strip() for num in mobile_numbers.split(',') if num.strip()]
        else:
            mobile_list = mobile_numbers

        logger.info(f"Sending SMS to {len(mobile_list)} recipients: {mobile_list}")
        
        # Send SMS to each number individually
        results = []
        successful_sends = 0
        failed_sends = 0
        
        for mobile in mobile_list:
            # Clean and format mobile number
            mobile = str(mobile).strip()
            
            # Convert 255 format to 0 format if needed
            if mobile.startswith('255'):
                mobile = '0' + mobile[3:]
            
            # Validate mobile number format
            if not mobile.startswith('0') or len(mobile) != 10:
                logger.warning(f"Invalid mobile number format: {mobile}")
                failed_sends += 1
                results.append({
                    'mobile': mobile,
                    'success': False,
                    'error': 'Invalid mobile number format'
                })
                continue

            payload = {
                "sender_id": sender_id,
                "message": message,
                "mobile": mobile
            }

            try:
                logger.info(f"Sending SMS to: {mobile}")
                response = requests.post(
                    url, 
                    headers=headers, 
                    json=payload, 
                    timeout=30
                )
                
                # Parse response
                try:
                    response_data = response.json() if response.content else {}
                except ValueError:
                    response_data = {'raw_response': response.text}
                
                logger.info(f"SMS to {mobile} - Status: {response.status_code}")
                
                # Use the same success criteria as single SMS (which is working)
                is_success = response.status_code == 200
                
                if is_success:
                    successful_sends += 1
                    results.append({
                        'mobile': mobile,
                        'success': True,
                        'data': response_data
                    })
                else:
                    failed_sends += 1
                    results.append({
                        'mobile': mobile,
                        'success': False,
                        'error': self._get_error_message(response.status_code, response_data)
                    })
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed for {mobile}: {str(e)}")
                failed_sends += 1
                results.append({
                    'mobile': mobile,
                    'success': False,
                    'error': f'Request failed: {str(e)}'
                })
            except Exception as e:
                logger.error(f"Unexpected error for {mobile}: {str(e)}")
                failed_sends += 1
                results.append({
                    'mobile': mobile,
                    'success': False,
                    'error': f'Unexpected error: {str(e)}'
                })

        # Return summary of all sends
        total_sends = len(mobile_list)
        overall_success = successful_sends > 0 and failed_sends == 0
        
        return {
            'success': overall_success,
            'status_code': 200 if overall_success else 400,
            'data': {
                'total_recipients': total_sends,
                'successful_sends': successful_sends,
                'failed_sends': failed_sends,
                'results': results
            },
            'error': None if overall_success else f"{failed_sends} out of {total_sends} SMS failed to send"
        }
    
    def _get_error_message(self, status_code, response_data):
        """Generate user-friendly error messages based on status code and response"""
        error_messages = {
            400: "Bad request - check your data format",
            401: "Unauthorized - check your API key",
            403: "Forbidden - insufficient permissions",
            404: "Service not found",
            429: "Too many requests - rate limit exceeded",
            500: "Internal server error",
            502: "Bad gateway",
            503: "Service unavailable"
        }
        
        base_error = error_messages.get(status_code, f"HTTP {status_code}")
        
        # Try to get more specific error from response
        if isinstance(response_data, dict):
            api_error = response_data.get('error') or response_data.get('message')
            if api_error:
                return f"{base_error}: {api_error}"
        
        return base_error

    def send_single_sms(self, sender_id, message, mobile_number):
        """
        Send single SMS via Mambo SMS API
        Args:
            sender_id: Your sender ID
            message: SMS message content  
            mobile_number: Single mobile number
        Returns:
            dict: Response with success status and data
        """
        return self.send_bulk_sms(sender_id, message, [mobile_number])


# Utility function for backward compatibility
def send_bulk_sms(mobile_numbers, message, sender_id=None):
    """
    Backward compatible function for sending bulk SMS
    """
    service = MamboSMSService()
    
    # Use default sender ID from settings if not provided
    if not sender_id:
        sender_id = getattr(settings, 'MAMBO_SMS_SENDER_ID', 'MAMBO SMS')
    
    return service.send_bulk_sms(sender_id, message, mobile_numbers)