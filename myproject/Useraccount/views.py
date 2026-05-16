from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

class CustomRegisterView(RegisterView):
    """
    Custom registration view that provides clear success response
    for frontend form clearing
    """
    serializer_class = CustomRegisterSerializer
    permission_classes = []  # Allow unauthenticated access
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save(request)
            
            # Return a clear success response
            return Response({
                'success': True,
                'message': 'Account created successfully! Please check your email for verification.',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'clear_form': True  # This flag tells frontend to clear the form
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Registration error: {e}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not current_password or not new_password or not confirm_password:
            return Response({
                'error': 'All fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({
                'error': 'New password and confirm password do not match'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        if not check_password(current_password, user.password):
            return Response({
                'error': 'Current password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.password = make_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# GOOGLE AUTH
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken
import requests

# Test endpoint for debugging
@api_view(['POST'])
def test_google_auth(request):
    """Test endpoint to debug Google auth issues"""
    return Response({
        'message': 'Test endpoint working',
        'received_data': request.data,
        'headers': dict(request.headers)
    })

User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    
    def post(self, request, *args, **kwargs):
        # Debug: Print request data
        print("Request data:", request.data)
        print("Request headers:", request.headers)
        
        access_token = request.data.get('access_token')
        
        if not access_token:
            print("No access token provided")
            return Response(
                {'error': 'Access token is required', 'received_data': request.data}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            print(f"Making request to Google with token: {access_token[:20]}...")
            
            # Get user info from Google
            google_response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            print(f"Google response status: {google_response.status_code}")
            print(f"Google response: {google_response.text}")
            
            google_user_info = google_response.json()
            
            if 'error' in google_user_info:
                print(f"Google API error: {google_user_info}")
                return Response(
                    {'error': 'Invalid access token', 'google_error': google_user_info}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            email = google_user_info.get('email')
            if not email:
                print("No email in Google response")
                return Response(
                    {'error': 'Email not provided by Google', 'google_data': google_user_info}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            print(f"Processing user with email: {email}")
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
                print(f"Existing user found: {user.username}")
            except User.DoesNotExist:
                # Create new user
                username = email.split('@')[0]  # Use email prefix as username
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=google_user_info.get('given_name', ''),
                    last_name=google_user_info.get('family_name', ''),
                    password=None  # No password for social login
                )
                user.set_unusable_password()
                user.save()
                print(f"New user created: {user.username}")
            
            # Create or get social account
            social_account, created = SocialAccount.objects.get_or_create(
                user=user,
                provider='google',
                defaults={
                    'uid': google_user_info.get('id'),
                    'extra_data': google_user_info
                }
            )
            
            if created:
                print(f"Social account created for user: {user.username}")
            else:
                print(f"Social account already exists for user: {user.username}")
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }
            
            print(f"Successfully generated tokens for user: {user.username}")
            return Response(response_data)
            
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_registration(request):
    """
    Custom registration view that handles the frontend data format
    """
    try:
        data = request.data
        
        # Extract data from request
        username = data.get('username', '')
        email = data.get('email', '')
        password1 = data.get('password1', '')
        password2 = data.get('password2', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        phone_number = data.get('phone_number', '')
        
        # Validate required fields
        if not username:
            return Response({
                'username': ['Username is required.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not email:
            return Response({
                'email': ['Email is required.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not password1:
            return Response({
                'password1': ['Password is required.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if password1 != password2:
            return Response({
                'password2': ['Passwords do not match.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response({
                'username': ['A user with this username already exists.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({
                'email': ['A user with this email already exists.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        # Store phone number if provided (you might want to create a separate profile model)
        if phone_number:
            print(f"Phone number for user {username}: {phone_number}")
            # You can store this in a separate model or user profile
        
        return Response({
            'success': True,
            'message': 'Account created successfully!',
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Registration error: {e}")
        return Response({
            'error': 'Registration failed. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_password_reset(request):
    """
    Custom password reset view that sends reset email
    """
    try:
        email = request.data.get('email')
        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return specific error when email doesn't exist
            return Response({
                'error': 'No account found with this email address. Please check your email or create a new account.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Generate token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset URL
        reset_url = f"http://localhost:5173/password-reset-confirm?uid={uid}&token={token}"
        
        # Send email
        subject = 'Password Reset Request'
        message = f"""
        Hello {user.username},
        
        You requested a password reset for your account.
        
        Please click the following link to reset your password:
        {reset_url}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Your Site Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            print(f"Password reset email sent to {email}")
            print(f"Reset URL: {reset_url}")
            
            return Response({
                'message': 'Password reset email sent successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Email sending error: {e}")
            return Response({
                'error': 'Failed to send email. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        print(f"Password reset error: {e}")
        return Response({
            'error': 'An error occurred. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        