from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from .models import SMSMessage

@csrf_exempt
@require_http_methods(["POST"])
def twilio_webhook(request):
    """
    Webhook endpoint for receiving SMS messages from Twilio
    """
    # Validate the request is from Twilio (optional but recommended)
    if hasattr(settings, 'TWILIO_WEBHOOK_AUTH_TOKEN') and settings.TWILIO_WEBHOOK_AUTH_TOKEN:
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
        url = request.build_absolute_uri()
        signature = request.META.get('HTTP_X_TWILIO_SIGNATURE', '')
        
        if not validator.validate(url, request.POST, signature):
            return HttpResponseForbidden('Invalid signature')

    # Extract SMS data from Twilio webhook
    from_phone = request.POST.get('From', '')
    to_phone = request.POST.get('To', '')
    message_body = request.POST.get('Body', '')
    message_sid = request.POST.get('MessageSid', '')

    try:
        # Save SMS to database
        sms_message = SMSMessage.objects.create(
            from_phone=from_phone,
            to_phone=to_phone,
            message_body=message_body,
            message_sid=message_sid
        )
        
        print(f"SMS saved: {sms_message}")  # For debugging
        
    except Exception as e:
        print(f"Error saving SMS: {e}")  # For debugging
        return HttpResponse("Error processing SMS", status=500)

    # Optional: Send auto-reply
    response = MessagingResponse()
    response.message("Thank you for your message! We'll get back to you soon.")
    
    return HttpResponse(str(response), content_type='text/xml')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sms_messages(request):
    """
    API endpoint to get SMS messages for authenticated user
    """
    try:
        messages = SMSMessage.objects.all()[:20]  # Get latest 20 messages
        data = []
        
        for msg in messages:
            data.append({
                'id': msg.id,
                'from_phone': msg.from_phone,
                'to_phone': msg.to_phone,
                'message_body': msg.message_body,
                'received_at': msg.received_at.isoformat(),
                'is_read': msg.is_read
            })
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch messages'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_sms_read(request, sms_id):
    """
    Mark SMS as read
    """
    try:
        sms = SMSMessage.objects.get(id=sms_id)
        sms.is_read = True
        sms.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    except SMSMessage.DoesNotExist:
        return Response(
            {'error': 'SMS not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': 'Failed to update SMS'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_count(request):
    """
    Get count of unread SMS messages
    """
    try:
        count = SMSMessage.objects.filter(is_read=False).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to get unread count'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )