# from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from .views import change_password


# urlpatterns = [
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('change-password/', change_password, name='change_password'),
# ]


from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import change_password, test_google_auth, GoogleLogin, custom_password_reset, custom_registration

urlpatterns = [
    # JWT Authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Password management
    path('change-password/', change_password, name='change_password'),
    path('change-password', change_password, name='change_password_no_slash'),
    
    # dj-rest-auth endpoints (only for login/logout, not registration)
    path('auth/', include('dj_rest_auth.urls')),
    
    # Social authentication
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/test/', test_google_auth, name='test_google_auth'),
    
    # Custom password reset
    path('auth/custom-password-reset/', custom_password_reset, name='custom_password_reset'),
    
    # Custom registration
    path('auth/registration/', custom_registration, name='custom_registration'),
]