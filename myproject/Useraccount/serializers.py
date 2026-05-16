from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that includes user data in the login response
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        
        return data

class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom registration serializer that supports both email and phone number registration.
    """
    
    # Override email field to make it optional and remove label
    email = serializers.EmailField(required=False, allow_blank=True, label='')
    phone_number = serializers.CharField(required=False, allow_blank=True, label='')
    phone = serializers.CharField(required=False, allow_blank=True, label='')
    
    def validate(self, data):
        # Check if either email or phone_number is provided
        email = data.get('email', '')
        phone_number = data.get('phone_number', '')
        phone = data.get('phone', '')
        password2 = data.get('password2', '')
        password1 = data.get('password1', '')
        
        # Validate confirm password
        if password2 != password1:
            raise serializers.ValidationError({
                'password2': 'Passwords do not match.'
            })
        
        # If phone number is provided but email is empty, create a placeholder email
        if phone_number and not email:
            data['email'] = f"{phone_number}@phone.local"
            email = data['email']
        
        # Now check if we have either email or phone_number
        if not email and not phone_number:
            raise serializers.ValidationError({
                'email': 'Either email or phone number is required.',
                'phone_number': 'Either email or phone number is required.'
            })
        
        # If email is provided, validate it
        if email:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({
                    'email': 'A user with this email already exists.'
                })
        
        # Call parent validation after our custom validation
        return super().validate(data)
    
    def validate_email(self, value):
        # Allow empty email if phone number is provided
        if not value and self.initial_data.get('phone_number'):
            return value
        return super().validate_email(value)
    
    def save(self, request):
        user = super().save(request)
        return user
    
    def get_cleaned_data(self):
        email = self.validated_data.get('email', '')
        phone_number = self.validated_data.get('phone_number', '')
        phone = self.validated_data.get('phone', '')
        
        # If phone number is provided but email is empty, create a placeholder email
        if phone_number and not email:
            email = f"{phone_number}@phone.local"
        
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': email,
            'phone_number': phone_number,
            'phone': phone,
        }
    
    def custom_signup(self, request, user):
        # Store phone number in user profile or custom field if needed
        phone_number = self.validated_data.get('phone_number', '')
        phone = self.validated_data.get('phone', '')
        
        # You can extend this to store in a separate profile model
        # For now, we'll just log it
        if phone_number or phone:
            print(f"Phone number for user {user.username}: {phone_number or phone}")
    
    def _has_phone_field(self):
        """
        Add this method to prevent the AttributeError
        """
        return True
