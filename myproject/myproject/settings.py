import os
import warnings
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
import dj_database_url
from decouple import config
import pymysql

# Force PyMySQL to act as MySQLdb
pymysql.install_as_MySQLdb()

# -------------------------
# Base Directory
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# Security
# -------------------------
DEBUG = os.environ.get("DEBUG", "False") == "True"

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "change-me-set-SECRET_KEY-in-render-env"
)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".vercel.app",
    ".onrender.com",
    # ".onrender.com",
    'restaurant-management-system-9p47.onrender.com',
    'restaurant-management-system-pi-one.vercel.app',
     'restaurant-management-system-9p47.onrender.com',
    'restaurant-management-system-pi-one.vercel.app',
    'restaurant-management-system-one-pink.vercel.app',
    'restaurant-management-system-dun-kappa.vercel.app',
   
    
]

# Add Render hostname dynamically
if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(
        os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    )

# -------------------------
# CORS
# -------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "https://restaurant-management-system-pi-one.vercel.app",
    "https://restaurant-management-system-one-pink.vercel.app",
    "https://restaurant-management-system-dun-kappa.vercel.app",
    
]

FRONTEND_URL = os.environ.get("FRONTEND_URL")

if FRONTEND_URL:
    CORS_ALLOWED_ORIGINS.append(FRONTEND_URL)

CORS_ALLOW_CREDENTIALS = True

# -------------------------
# Installed Apps
# -------------------------
INSTALLED_APPS = [
    "corsheaders",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "whitenoise.runserver_nostatic",
    "channels",

    # Local Apps
    "Customer",
    "Items",
    "Menus",
    "OrderItem",
    "Staff",
    "Order",
    "Useraccount",
    "InventoryItems",
    "chatbot",
    "Payment.apps.PaymentConfig",
    "sms",
    "mambosmsbulk",
    "mambosmssingle",
    "mambosmsbalance",
    "whatsapplinkin",

    # Third Party
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.sites",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    "dj_rest_auth",
    "dj_rest_auth.registration",

    "djoser",
]

# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "allauth.account.middleware.AccountMiddleware",
]

# -------------------------
# URL Configuration
# -------------------------
ROOT_URLCONF = "myproject.urls"

WSGI_APPLICATION = "myproject.wsgi.application"
ASGI_APPLICATION = "myproject.asgi.application"

# -------------------------
# Templates
# -------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -------------------------
# Database Configuration
# -------------------------

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Production PostgreSQL (Render)
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
        )
    }

else:
    # Local MySQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "resta_",
            "USER": "root",
            "PASSWORD": "passcode2000",
            "HOST": "localhost",
            "PORT": "3307",
        }
    }

# -------------------------
# Default Auto Field
# -------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------
# Password Validators
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator"
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

# -------------------------
# Internationalization
# -------------------------
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
    ("sw", _("Swahili")),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True
USE_TZ = True

# -------------------------
# Static Files
# -------------------------
STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

# -------------------------
# DRF
# -------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",

        "rest_framework.authentication.SessionAuthentication",
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# -------------------------
# JWT
# -------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),

    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": True,

    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": "HS256",

    "SIGNING_KEY": SECRET_KEY,

    "VERIFYING_KEY": None,

    "AUTH_HEADER_TYPES": ("Bearer",),

    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    "USER_ID_FIELD": "id",

    "USER_ID_CLAIM": "user_id",

    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),

    "TOKEN_TYPE_CLAIM": "token_type",
}

# -------------------------
# Email
# -------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.sendgrid.net"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = "apikey"

EMAIL_HOST_PASSWORD = config(
    "SENDGRID_API_KEY",
    default=""
)

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="infonet20th@gmail.com"
)

SERVER_EMAIL = config(
    "SERVER_EMAIL",
    default="infonet20th@gmail.com"
)

# -------------------------
# SMS
# -------------------------
MAMBO_SMS_SENDER_ID = os.getenv("MAMBO_SMS_SENDER_ID")

MAMBO_SMS_API_KEY = os.getenv("MAMBO_SMS_API_KEY")

MAMBO_SMS_BASE_URL = os.getenv(
    "MAMBO_SMS_BASE_URL",
    "https://api.mambo.co.tz"
)

# -------------------------
# Celery
# -------------------------
CELERY_BROKER_URL = os.environ.get(
    "REDIS_URL",
    "redis://localhost:6379"
)

CELERY_RESULT_BACKEND = os.environ.get(
    "REDIS_URL",
    "redis://localhost:6379"
)

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "UTC"

# -------------------------
# Sites
# -------------------------
SITE_ID = 1

SITE_NAME = config(
    "SITE_NAME",
    default="ReactLife"
)

DOMAIN = os.environ.get(
    "FRONTEND_DOMAIN",
    config(
        "FRONTEND_DOMAIN",
        default="localhost:5173"
    )
)

# -------------------------
# Djoser
# -------------------------
DJOSER = {
    "DOMAIN": DOMAIN,

    "SITE_NAME": SITE_NAME,

    "PASSWORD_RESET_CONFIRM_URL":
    "password/reset/confirm/{uid}/{token}",

    "ACTIVATION_URL":
    "activate/{uid}/{token}",

    "SEND_ACTIVATION_EMAIL": True,

    "SEND_CONFIRMATION_EMAIL": True,

    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,

    "PASSWORD_RESET_CONFIRM_RETYPE": True,

    "EMAIL": {
        "activation":
        "djoser.email.ActivationEmail",

        "confirmation":
        "djoser.email.ConfirmationEmail",

        "password_reset":
        "djoser.email.PasswordResetEmail",

        "password_changed_confirmation":
        "djoser.email.PasswordChangedConfirmationEmail",
    },
}

# -------------------------
# Authentication Backends
# -------------------------
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",

    "allauth.account.auth_backends.AuthenticationBackend",
)

# -------------------------
# Google OAuth
# -------------------------
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email"
        ],

        "AUTH_PARAMS": {
            "access_type": "online"
        },

        "OAUTH_PKCE_ENABLED": True,
    }
}

# -------------------------
# REST AUTH
# -------------------------
REST_AUTH = {
    "USE_JWT": True,

    "JWT_AUTH_COOKIE": "access_token",

    "JWT_AUTH_REFRESH_COOKIE": "refresh_token",

    "JWT_AUTH_HTTPONLY": True,

    "JWT_AUTH_SECURE": not DEBUG,

    "JWT_AUTH_SAMESITE": "Lax",

    "USER_DETAILS_SERIALIZER":
    "dj_rest_auth.serializers.UserDetailsSerializer",
}

ACCOUNT_LOGIN_METHODS = {"email"}

ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "username*",
    "password1*",
    "password2*"
]

# -------------------------
# Ignore Warnings
# -------------------------
warnings.filterwarnings(
    "ignore",
    message="app_settings.USERNAME_REQUIRED is deprecated",
    category=UserWarning,
    module="dj_rest_auth.registration.serializers"
)

warnings.filterwarnings(
    "ignore",
    message="app_settings.EMAIL_REQUIRED is deprecated",
    category=UserWarning,
    module="dj_rest_auth.registration.serializers"
)

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

# -------------------------
# Channels
# -------------------------
REDIS_HOST_URL = os.environ.get(
    "REDIS_URL",
    "redis://127.0.0.1:6379"
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND":
        "channels_redis.core.RedisChannelLayer",

        "CONFIG": {
            "hosts": [REDIS_HOST_URL],
        },
    },
}

# -------------------------
# OpenAI
# -------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")