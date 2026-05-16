# Add these imports at the top of your existing views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .sms_service import MamboSMSService  # Import from same directory

# Add this function to your existing views.py file
@api_view(['POST'])
# @permission_classes([IsAuthenticated])  # Uncomment if you need authentication
def send_sms_view(request):
    """
    API endpoint to send SMS via Mambo SMS
    """
    try:
        # Get data from request
        sender_id = request.data.get('sender_id')
        message = request.data.get('message')
        mobile = request.data.get('mobile')
        
        print(f"SMS Request - Sender: {sender_id}, Mobile: {mobile}, Message: {message}")
        
        # Validate required fields
        if not all([sender_id, message, mobile]):
            return Response({
                'error': 'Missing required fields: sender_id, message, mobile'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Clean and validate mobile number format
        mobile = str(mobile).strip()
        
        # Convert 255 format to 0 format if needed
        if mobile.startswith('255'):
            mobile = '0' + mobile[3:]
        
        # Validate mobile number format (should start with 0)
        if not mobile.startswith('0') or len(mobile) != 10:
            return Response({
                'error': 'Mobile number should start with 0 and be 10 digits (e.g., 0713123456)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"Formatted mobile number: {mobile}")
        
        # Send SMS
        sms_service = MamboSMSService()
        result = sms_service.send_sms(sender_id, message, mobile)
        
        print(f"SMS Service Result: {result}")
        
        if result['success']:
            return Response({
                'message': 'SMS sent successfully',
                'data': result['data'],
                'mobile': mobile
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to send SMS',
                'details': result.get('error', 'Unknown error'),
                'status_code': result.get('status_code')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        print(f"SMS View Error: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)