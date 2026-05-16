import os
from pathlib import Path
import environ
import warnings
from django.utils.translation import gettext_lazy as _
from decouple import config

# -------------------------
# Paths
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# Environment Variables
# -------------------------
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, '.env')

if not os.path.exists(env_file):
    raise FileNotFoundError(f"⚠️ .env file not found at {env_file}")

env.read_env(env_file)

# -------------------------
# Security
# -------------------------
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# -------------------------
# CORS
# -------------------------
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
])
CORS_ALLOW_CREDENTIALS = True

# -------------------------
# Applications
# -------------------------
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Channels
    'channels',
    # Your apps
    'Customer',
    'Items',
    # 'Inventory',
    'Menus',
    'OrderItem',
    'Staff',
    'Order',
    'Useraccount',
    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'djoser',
    'sms',
    'mambosmsbulk',
    
    'mambosmssingle',
    'whatsapplinkin',
    'mambosmsbalance',
    'chatbot',
    'Payment.apps.PaymentConfig',
    'InventoryItems',
    # 'staff',
]
# redis config
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# -------------------------
# URL / WSGI / ASGI
# -------------------------
ROOT_URLCONF = 'myproject.urls'
WSGI_APPLICATION = 'myproject.wsgi.application'
ASGI_APPLICATION = 'myproject.asgi.application'

# -------------------------
# Templates
# -------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------
# Database
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='3306'),
    }
}

# -------------------------
# Password validation
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------
# Localization
# -------------------------
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
    ('sw', _('Swahili')),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -------------------------
# Static files
# -------------------------
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------
# REST Framework
# -------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# -------------------------
# Simple JWT Configuration
# -------------------------
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# -------------------------
# Email Configuration (SendGrid SMTP - Single Sender)
# -------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # This is literally 'apikey'
EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='infonet20th@gmail.com')
SERVER_EMAIL = config('SERVER_EMAIL', default='infonet20th@gmail.com')

# -------------------------

# TWILIO SMS CONFIGURATION
# TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
# TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
# TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')
# # Webhook security
# TWILIO_WEBHOOK_AUTH_TOKEN = config('TWILIO_WEBHOOK_AUTH_TOKEN', default='')
# Site Configuration

# --------------------------------
# AFRICAN TALK SMS CONFIG





# MAMBO SMS



from dotenv import load_dotenv

load_dotenv()
MAMBO_SMS_API_KEY = os.getenv('MAMBO_SMS_SENDER_ID')
MAMBO_SMS_API_KEY = os.getenv('MAMBO_SMS_API_KEY')
MAMBO_SMS_BASE_URL = os.getenv('MAMBO_SMS_BASE_URL', 'https://api.mambo.co.tz')





# ..........
# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# -------------------------
SITE_ID = 1
SITE_NAME = config('SITE_NAME', default='ReactLife')
DOMAIN = config('FRONTEND_DOMAIN', default='localhost:5173')

# -------------------------
# Djoser Configuration
# -------------------------
DJOSER = {
    'DOMAIN': DOMAIN,
    'SITE_NAME': SITE_NAME,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'EMAIL': {
        'activation': 'djoser.email.ActivationEmail',
        'confirmation': 'djoser.email.ConfirmationEmail',
        'password_reset': 'djoser.email.PasswordResetEmail',
        'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
    },
}

# -------------------------
# Sites Framework
# -------------------------
SITE_ID = 1

# -------------------------
# Authentication Backends
# -------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# -------------------------
# Google OAuth
# -------------------------
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}

# -------------------------
# dj-rest-auth config
# -------------------------
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access_token',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_SECURE': False,  # Change to True in production
    'JWT_AUTH_SAMESITE': 'Lax',
    'USER_DETAILS_SERIALIZER': 'dj_rest_auth.serializers.UserDetailsSerializer',
}

# -------------------------
# allauth config
# -------------------------
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]

# -------------------------
# Suppress warnings
# -------------------------
warnings.filterwarnings(
    'ignore',
    message='app_settings.USERNAME_REQUIRED is deprecated',
    category=UserWarning,
    module='dj_rest_auth.registration.serializers'
)
warnings.filterwarnings(
    'ignore',
    message='app_settings.EMAIL_REQUIRED is deprecated',
    category=UserWarning,
    module='dj_rest_auth.registration.serializers'
)

# -------------------------
# Socialaccount config
# -------------------------
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

# -------------------------
# Channels Configuration
# -------------------------
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
# OPEN_AI KEY
from dotenv import load_dotenv
load_dotenv()  # loads .env

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# -------------------------

# Simple JWT Configuration

# -------------------------

from datetime import timedelta



SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),

    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ROTATE_REFRESH_TOKENS': True,

    'BLACKLIST_AFTER_ROTATION': True,

    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',

    'SIGNING_KEY': SECRET_KEY,

    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),

    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    'USER_ID_FIELD': 'id',

    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

    'TOKEN_TYPE_CLAIM': 'token_type',

}



# -------------------------

# Email Configuration (SendGrid SMTP - Single Sender)

# -------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'apikey'  # This is literally 'apikey'

EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY', default='')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='infonet20th@gmail.com')

SERVER_EMAIL = config('SERVER_EMAIL', default='infonet20th@gmail.com')



# -------------------------



# TWILIO SMS CONFIGURATION

# TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')

# TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')

# TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

# # Webhook security

# TWILIO_WEBHOOK_AUTH_TOKEN = config('TWILIO_WEBHOOK_AUTH_TOKEN', default='')

# Site Configuration



# --------------------------------

# AFRICAN TALK SMS CONFIG











# MAMBO SMS







from dotenv import load_dotenv



load_dotenv()

MAMBO_SMS_API_KEY = os.getenv('MAMBO_SMS_SENDER_ID')

MAMBO_SMS_API_KEY = os.getenv('MAMBO_SMS_API_KEY')

MAMBO_SMS_BASE_URL = os.getenv('MAMBO_SMS_BASE_URL', 'https://api.mambo.co.tz')











# ..........

# Celery configuration

CELERY_BROKER_URL = 'redis://localhost:6379'

CELERY_RESULT_BACKEND = 'redis://localhost:6379'

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'UTC'



# -------------------------

SITE_ID = 1

SITE_NAME = config('SITE_NAME', default='ReactLife')

DOMAIN = config('FRONTEND_DOMAIN', default='localhost:5173')



# -------------------------

# Djoser Configuration

# -------------------------

DJOSER = {

    'DOMAIN': DOMAIN,

    'SITE_NAME': SITE_NAME,

    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',

    'ACTIVATION_URL': 'activate/{uid}/{token}',

    'SEND_ACTIVATION_EMAIL': True,

    'SEND_CONFIRMATION_EMAIL': True,

    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,

    'PASSWORD_RESET_CONFIRM_RETYPE': True,

    'EMAIL': {

        'activation': 'djoser.email.ActivationEmail',

        'confirmation': 'djoser.email.ConfirmationEmail',

        'password_reset': 'djoser.email.PasswordResetEmail',

        'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',

    },

}



# -------------------------

# Sites Framework

# -------------------------

SITE_ID = 1



# -------------------------

# Authentication Backends

# -------------------------

AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',

)



# -------------------------

# Google OAuth

# -------------------------

SOCIALACCOUNT_PROVIDERS = {

    'google': {

        'SCOPE': ['profile', 'email'],

        'AUTH_PARAMS': {'access_type': 'online'},

        'OAUTH_PKCE_ENABLED': True,

    }

}



# -------------------------

# dj-rest-auth config

# -------------------------

REST_AUTH = {

    'USE_JWT': True,

    'JWT_AUTH_COOKIE': 'access_token',

    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',

    'JWT_AUTH_HTTPONLY': True,

    'JWT_AUTH_SECURE': False,  # Change to True in production

    'JWT_AUTH_SAMESITE': 'Lax',

    'USER_DETAILS_SERIALIZER': 'dj_rest_auth.serializers.UserDetailsSerializer',

}



# -------------------------

# allauth config

# -------------------------

ACCOUNT_LOGIN_METHODS = {"email"}

ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]



# -------------------------

# Suppress warnings

# -------------------------

warnings.filterwarnings(

    'ignore',

    message='app_settings.USERNAME_REQUIRED is deprecated',

    category=UserWarning,

    module='dj_rest_auth.registration.serializers'

)

warnings.filterwarnings(

    'ignore',

    message='app_settings.EMAIL_REQUIRED is deprecated',

    category=UserWarning,

    module='dj_rest_auth.registration.serializers'

)



# -------------------------

# Socialaccount config

# -------------------------

SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'



# -------------------------

# Channels Configuration

# -------------------------

CHANNEL_LAYERS = {

    'default': {

        'BACKEND': 'channels_redis.core.RedisChannelLayer',

        'CONFIG': {

            "hosts": [('127.0.0.1', 6379)],

        },

    },

}

# OPEN_AI KEY

from dotenv import load_dotenv

load_dotenv()  # loads .env



# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from dotenv import load_dotenv

load_dotenv()  # loads .env



# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")







# -------------------------



# Simple JWT Configuration



# -------------------------



from datetime import timedelta







SIMPLE_JWT = {



    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),



    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),



    'ROTATE_REFRESH_TOKENS': True,



    'BLACKLIST_AFTER_ROTATION': True,



    'UPDATE_LAST_LOGIN': True,



    'ALGORITHM': 'HS256',



    'SIGNING_KEY': SECRET_KEY,



    'VERIFYING_KEY': None,



    'AUTH_HEADER_TYPES': ('Bearer',),



    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',



    'USER_ID_FIELD': 'id',



    'USER_ID_CLAIM': 'user_id',



    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),



    'TOKEN_TYPE_CLAIM': 'token_type',



}







# -------------------------



# Email Configuration (SendGrid SMTP - Single Sender)



# -------------------------



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



EMAIL_HOST = 'smtp.sendgrid.net'



EMAIL_PORT = 587



EMAIL_USE_TLS = True



EMAIL_HOST_USER = 'apikey'  # This is literally 'apikey'



EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY', default='')



DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='infonet20th@gmail.com')



SERVER_EMAIL = config('SERVER_EMAIL', default='infonet20th@gmail.com')







# -------------------------







# TWILIO SMS CONFIGURATION



# TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')



# TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')



# TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')



# # Webhook security



# TWILIO_WEBHOOK_AUTH_TOKEN = config('TWILIO_WEBHOOK_AUTH_TOKEN', default='')



# Site Configuration







# --------------------------------



# AFRICAN TALK SMS CONFIG























# MAMBO SMS















from dotenv import load_dotenv







load_dotenv()



MAMBO_SMS_API_KEY = os.getenv('MAMBO_SMS_SENDER_ID')



MAMBO_SMS_API_KEY = os.getenv('MAMBO_SMS_API_KEY')



MAMBO_SMS_BASE_URL = os.getenv('MAMBO_SMS_BASE_URL', 'https://api.mambo.co.tz')























# ..........



# Celery configuration



CELERY_BROKER_URL = 'redis://localhost:6379'



CELERY_RESULT_BACKEND = 'redis://localhost:6379'



CELERY_ACCEPT_CONTENT = ['json']



CELERY_TASK_SERIALIZER = 'json'



CELERY_RESULT_SERIALIZER = 'json'



CELERY_TIMEZONE = 'UTC'







# -------------------------



SITE_ID = 1



SITE_NAME = config('SITE_NAME', default='ReactLife')



DOMAIN = config('FRONTEND_DOMAIN', default='localhost:5173')







# -------------------------



# Djoser Configuration



# -------------------------



DJOSER = {



    'DOMAIN': DOMAIN,



    'SITE_NAME': SITE_NAME,



    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',



    'ACTIVATION_URL': 'activate/{uid}/{token}',



    'SEND_ACTIVATION_EMAIL': True,



    'SEND_CONFIRMATION_EMAIL': True,



    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,



    'PASSWORD_RESET_CONFIRM_RETYPE': True,



    'EMAIL': {



        'activation': 'djoser.email.ActivationEmail',



        'confirmation': 'djoser.email.ConfirmationEmail',



        'password_reset': 'djoser.email.PasswordResetEmail',



        'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',



    },



}







# -------------------------



# Sites Framework



# -------------------------



SITE_ID = 1







# -------------------------



# Authentication Backends



# -------------------------



AUTHENTICATION_BACKENDS = (



    'django.contrib.auth.backends.ModelBackend',



    'allauth.account.auth_backends.AuthenticationBackend',



)







# -------------------------



# Google OAuth



# -------------------------



SOCIALACCOUNT_PROVIDERS = {



    'google': {



        'SCOPE': ['profile', 'email'],



        'AUTH_PARAMS': {'access_type': 'online'},



        'OAUTH_PKCE_ENABLED': True,



    }



}







# -------------------------



# dj-rest-auth config



# -------------------------



REST_AUTH = {



    'USE_JWT': True,



    'JWT_AUTH_COOKIE': 'access_token',



    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',



    'JWT_AUTH_HTTPONLY': True,



    'JWT_AUTH_SECURE': False,  # Change to True in production



    'JWT_AUTH_SAMESITE': 'Lax',



    'USER_DETAILS_SERIALIZER': 'dj_rest_auth.serializers.UserDetailsSerializer',



}







# -------------------------



# allauth config



# -------------------------



ACCOUNT_LOGIN_METHODS = {"email"}



ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]







# -------------------------



# Suppress warnings



# -------------------------



warnings.filterwarnings(



    'ignore',



    message='app_settings.USERNAME_REQUIRED is deprecated',



    category=UserWarning,



    module='dj_rest_auth.registration.serializers'



)



warnings.filterwarnings(



    'ignore',



    message='app_settings.EMAIL_REQUIRED is deprecated',



    category=UserWarning,



    module='dj_rest_auth.registration.serializers'



)







# -------------------------



# Socialaccount config



# -------------------------



SOCIALACCOUNT_AUTO_SIGNUP = True



SOCIALACCOUNT_EMAIL_REQUIRED = True



SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'







# -------------------------



# Channels Configuration



# -------------------------



CHANNEL_LAYERS = {



    'default': {



        'BACKEND': 'channels_redis.core.RedisChannelLayer',



        'CONFIG': {



            "hosts": [('127.0.0.1', 6379)],



        },



    },



}



# OPEN_AI KEY



from dotenv import load_dotenv



load_dotenv()  # loads .env







# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


