import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sms_balance(request):
    """
    Get SMS balance from Mambo SMS service or return mock data
    Requires user to be logged in
    """
    try:
        # First try to get real data from Mambo SMS API
        try:
            url = f"{settings.MAMBO_SMS_BASE_URL}/api/v1/sms/balance"
            headers = {
                "Authorization": f"Bearer {settings.MAMBO_SMS_API_KEY}",
                "Content-Type": "application/json",
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Return formatted response matching the expected structure
            return Response({
                'success': True,
                'balance': data,
                'message': 'Balance retrieved successfully from Mambo SMS',
                'raw_data': data
            })
            
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            # If external API fails, return mock data with the structure you provided
            print(f"External API failed: {e}. Returning mock data.")
            
            # Mock data matching your exact structure
            mock_balance_data = {
                "id": 24,
                "company_id": "24",
                "initial_balance": "1000",
                "available_balance": "940",
                "created_at": "2025-08-25T09:37:33.000000Z",
                "updated_at": "2025-09-01T11:45:50.000000Z"
            }
            
            return Response({
                'success': True,
                'balance': mock_balance_data,
                'message': 'Balance retrieved from mock data (external API unavailable)',
                'raw_data': mock_balance_data
            })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'An unexpected error occurred',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_sms_balance_test(request):
    """
    Test endpoint for SMS balance - no authentication required
    Returns mock data for testing
    """
    # Mock data matching your exact structure with updated values
    mock_balance_data = {
        "id": 24,
        "company_id": "24",
        "initial_balance": "1000",
        "available_balance": "934",
        "created_at": "2025-08-25T09:37:33.000000Z",
        "updated_at": "2025-09-01T13:14:27.000000Z"
    }
    
    return Response({
        'success': True,
        'balance': mock_balance_data,
        'message': 'Test balance data retrieved successfully',
        'raw_data': mock_balance_data
    })
