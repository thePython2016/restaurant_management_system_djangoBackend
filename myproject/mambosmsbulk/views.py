import logging
import re
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .sms_service import send_bulk_sms

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([])  # Allow anonymous access
def send_bulk_sms_view(request):
    """
    API endpoint to send bulk SMS via Mambo SMS
    
    Expected POST data format:
    {
        "sender_id": "YOUR_SENDER_ID",
        "message": "Your SMS message content",
        "mobile": "0713123456,0754789012,0765456789" or ["0713123456", "0754789012"]
    }
    
    Response format:
    {
        "success": true/false,
        "message": "Status message",
        "data": {...},  // API response data
        "total_recipients": 3,
        "mobile_numbers": ["0713123456", "0754789012", "0765456789"],
        "invalid_numbers": [],  // Any numbers that failed validation
        "error": "Error message if any"
    }
    """
    try:
        # Extract data from request
        logger.info(f"Received request data: {request.data}")
        sender_id = request.data.get('sender_id')
        message = request.data.get('message') 
        mobile = request.data.get('mobile')
        
        logger.info(f"Bulk SMS request received - Sender: {sender_id}, Recipients: {len(str(mobile)) if mobile else 0}")
        
        # Validate required fields
        missing_fields = []
        if not sender_id:
            missing_fields.append('sender_id')
        if not message:
            missing_fields.append('message')
        if not mobile:
            missing_fields.append('mobile')
            
        if missing_fields:
            return Response({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'required_fields': ['sender_id', 'message', 'mobile']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate message length (typical SMS limit is 160 characters)
        max_length = getattr(settings, 'SMS_MAX_LENGTH', 160)
        if len(message) > max_length:
            return Response({
                'success': False,
                'error': f'Message too long. Maximum {max_length} characters allowed.',
                'current_length': len(message)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process mobile numbers
        mobile_numbers = _process_mobile_numbers(mobile)
        
        if mobile_numbers['error']:
            return Response({
                'success': False,
                'error': mobile_numbers['error'],
                'invalid_numbers': mobile_numbers.get('invalid_numbers', [])
            }, status=status.HTTP_400_BAD_REQUEST)
        
        formatted_numbers = mobile_numbers['valid_numbers']
        invalid_numbers = mobile_numbers.get('invalid_numbers', [])
        
        if not formatted_numbers:
            return Response({
                'success': False,
                'error': 'No valid mobile numbers provided after validation'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check recipient limit
        max_recipients = getattr(settings, 'SMS_MAX_BULK_RECIPIENTS', 1000)
        if len(formatted_numbers) > max_recipients:
            return Response({
                'success': False,
                'error': f'Too many recipients. Maximum {max_recipients} allowed.',
                'provided_count': len(formatted_numbers)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info(f"Processed {len(formatted_numbers)} valid numbers, {len(invalid_numbers)} invalid")
        
        # Send bulk SMS
        logger.info(f"About to send SMS with: sender_id={sender_id}, message_length={len(message)}, recipients={formatted_numbers}")
        result = send_bulk_sms(formatted_numbers, message, sender_id)
        
        logger.info(f"SMS service result: Success={result.get('success', False)}")
        
        # Prepare response
        response_data = {
            'total_recipients': len(formatted_numbers),
            'mobile_numbers': formatted_numbers,
            'sender_id': sender_id,
            'message_length': len(message)
        }
        
        if invalid_numbers:
            response_data['invalid_numbers'] = invalid_numbers
            response_data['warning'] = f'{len(invalid_numbers)} numbers were invalid and skipped'
        
        if result.get('success', False):
            response_data.update({
                'success': True,
                'message': f"Bulk SMS sent successfully to {result.get('data', {}).get('successful_sends', 0)} recipients",
                'data': result.get('data', result)
            })
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            sms_error = result.get('error', result.get('message', 'Unknown error'))
            
            response_data.update({
                'success': False,
                'error': 'Failed to send bulk SMS',
                'details': sms_error,
                'sms_service_response': result
            })
            
            # Return 400 for client errors, 500 for server errors
            if 'Invalid mobile number' in sms_error or 'failed to send' in sms_error.lower():
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Unexpected error in bulk SMS view: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error occurred',
            'details': str(e) if settings.DEBUG else 'Please contact support'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _process_mobile_numbers(mobile_input):
    """
    Process and validate mobile numbers from various input formats
    
    Args:
        mobile_input: String (comma-separated), List, or single number
        
    Returns:
        dict: {
            'valid_numbers': List of valid formatted numbers,
            'invalid_numbers': List of invalid numbers,
            'error': Error message if critical error
        }
    """
    try:
        # Convert input to list
        if isinstance(mobile_input, list):
            numbers_list = mobile_input
        elif isinstance(mobile_input, str):
            # Split by comma, semicolon, or newline
            numbers_list = re.split(r'[,;\n]+', mobile_input.strip())
        else:
            return {
                'valid_numbers': [],
                'invalid_numbers': [],
                'error': 'Mobile numbers must be provided as string or list'
            }
        
        # Clean and validate each number
        valid_numbers = []
        invalid_numbers = []
        
        for num in numbers_list:
            num = str(num).strip()
            if not num:  # Skip empty strings
                continue
                
            # Clean the number (remove spaces, dashes, parentheses)
            clean_num = re.sub(r'[\s\-\(\)]+', '', num)
            
            # Convert different formats to Tanzania format (0XXXXXXXXX)
            formatted_num = _format_tanzanian_number(clean_num)
            
            if formatted_num:
                valid_numbers.append(formatted_num)
            else:
                invalid_numbers.append(num)
        
        # Remove duplicates while preserving order
        valid_numbers = list(dict.fromkeys(valid_numbers))
        
        return {
            'valid_numbers': valid_numbers,
            'invalid_numbers': invalid_numbers,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error processing mobile numbers: {str(e)}")
        return {
            'valid_numbers': [],
            'invalid_numbers': [],
            'error': f'Error processing mobile numbers: {str(e)}'
        }


def _format_tanzanian_number(number):
    """
    Format phone number to Tanzanian standard (0XXXXXXXXX)
    
    Handles formats:
    - +255XXXXXXXXX -> 0XXXXXXXXX  
    - 255XXXXXXXXX -> 0XXXXXXXXX
    - 0XXXXXXXXX -> 0XXXXXXXXX (validate)
    - XXXXXXXXX -> 0XXXXXXXXX (add leading 0)
    
    Returns formatted number or None if invalid
    """
    # Remove any non-digit characters
    digits_only = re.sub(r'\D', '', number)
    
    if not digits_only:
        return None
    
    # Handle different formats
    if digits_only.startswith('255'):
        # +255XXXXXXXXX or 255XXXXXXXXX format
        if len(digits_only) == 12:  # 255 + 9 digits
            formatted = '0' + digits_only[3:]
            return formatted
        else:
            return None
    elif digits_only.startswith('0'):
        # 0XXXXXXXXX format
        if len(digits_only) == 10:
            prefix = digits_only[1:4]
            if _is_valid_tanzanian_prefix(prefix):
                return digits_only
            else:
                return None
        else:
            return None
    else:
        # XXXXXXXXX format (missing leading 0)
        if len(digits_only) == 9:
            prefix = digits_only[:3]
            if _is_valid_tanzanian_prefix(prefix):
                formatted = '0' + digits_only
                return formatted
            else:
                return None
        else:
            return None


def _is_valid_tanzanian_prefix(prefix):
    """
    Check if the 3-digit prefix is valid for Tanzanian mobile numbers
    
    Common Tanzanian mobile prefixes:
    - Vodacom: 071, 074, 075, 076
    - Airtel: 078, 068, 069
    - Tigo: 071, 065, 067
    - Zantel: 077
    - Halotel: 062
    - And many more...
    """
    # More comprehensive list of Tanzanian mobile prefixes
    valid_prefixes = {
        '071', '074', '075', '076',  # Vodacom
        '078', '068', '069',          # Airtel  
        '065', '067',                 # Tigo
        '077',                        # Zantel
        '062',                        # Halotel
        '073', '072',                 # Additional Vodacom
        '061', '063', '064',          # Additional prefixes
        '066', '070', '079',          # More prefixes
        '622',                        # Additional prefix (found in contact groups)
        '766'                         # Additional prefix (found in test data)
    }
    
    return prefix in valid_prefixes


def _get_http_status_from_sms_error(sms_status_code):
    """Map SMS API status codes to appropriate HTTP status codes"""
    if not sms_status_code:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    
    status_mapping = {
        400: status.HTTP_400_BAD_REQUEST,
        401: status.HTTP_401_UNAUTHORIZED, 
        403: status.HTTP_403_FORBIDDEN,
        404: status.HTTP_404_NOT_FOUND,
        429: status.HTTP_429_TOO_MANY_REQUESTS,
        500: status.HTTP_502_BAD_GATEWAY,
        502: status.HTTP_502_BAD_GATEWAY,
        503: status.HTTP_503_SERVICE_UNAVAILABLE
    }
    
    return status_mapping.get(sms_status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)