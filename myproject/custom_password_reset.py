from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
import json

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_password_reset(request):
    """
    Custom password reset endpoint that sends real emails
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        if not email:
            return Response(
                {'email': ['This field is required.']}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user exists (but don't reveal this for security)
        try:
            user = User.objects.get(email=email)
            
            # Generate reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # Create reset URL
            reset_url = f"http://localhost:5173/password/reset/confirm?uid={uid}&token={token}"
            
            # Send email
            subject = 'Password Reset Request - ReactLife'
            message = f"""
Hello,

You requested a password reset for your account.

Please click the following link to reset your password:

{reset_url}

If you didn't request this password reset, please ignore this email.

This link will expire in 24 hours.

Best regards,
ReactLife Team
            """
            
            # Send the email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            # Also print to console for development
            print(f"\n" + "="*60)
            print(f"PASSWORD RESET EMAIL SENT TO: {email}")
            print(f"Reset URL: {reset_url}")
            print(f"UID: {uid}")
            print(f"Token: {token}")
            print(f"="*60 + "\n")
            
        except User.DoesNotExist:
            # Don't reveal if user doesn't exist for security
            pass
        except Exception as email_error:
            print(f"Email sending failed: {email_error}")
            # Still return success to prevent email enumeration
        
        # Always return success to prevent email enumeration
        return Response(
            {'detail': 'Password reset email sent.'}, 
            status=status.HTTP_204_NO_CONTENT
        )
        
    except json.JSONDecodeError:
        return Response(
            {'detail': 'Invalid JSON'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        print(f"Password reset error: {e}")
        return Response(
            {'detail': 'An error occurred'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

