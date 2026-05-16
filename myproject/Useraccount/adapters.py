from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to handle compatibility issues
    """
    
    def save_user(self, request, user, form, commit=True):
        """
        Override save_user to handle the serializer instead of form
        """
        if hasattr(form, 'get_cleaned_data'):
            # Handle serializer case
            cleaned_data = form.get_cleaned_data()
            user.username = cleaned_data.get('username', '')
            user.email = cleaned_data.get('email', '')
            if cleaned_data.get('password1'):
                user.set_password(cleaned_data['password1'])
        else:
            # Handle form case (fallback)
            user = super().save_user(request, user, form, commit=False)
        
        if commit:
            user.save()
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter
    """
    pass

