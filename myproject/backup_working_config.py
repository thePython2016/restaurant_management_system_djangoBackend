#!/usr/bin/env python
"""
Backup the current working SendGrid configuration
"""

import os
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.conf import settings

def backup_current_config():
    """Backup current working configuration"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_content = f"""
# WORKING SENDGRID CONFIGURATION - BACKUP {timestamp}
# This configuration was working for email delivery

# Email Configuration (SendGrid SMTP - Single Sender)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # This is literally 'apikey'
EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='infonet20th@gmail.com')
SERVER_EMAIL = config('SERVER_EMAIL', default='infonet20th@gmail.com')

# Site Configuration
SITE_ID = 1
SITE_NAME = config('SITE_NAME', default='ReactLife')
DOMAIN = config('FRONTEND_DOMAIN', default='localhost:5173')

# Djoser Configuration
DJOSER = {{
    'DOMAIN': DOMAIN,
    'SITE_NAME': SITE_NAME,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{{uid}}/{{token}}',
    'ACTIVATION_URL': 'activate/{{uid}}/{{token}}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'EMAIL': {{
        'activation': 'djoser.email.ActivationEmail',
        'confirmation': 'djoser.email.ConfirmationEmail',
        'password_reset': 'djoser.email.PasswordResetEmail',
        'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
    }},
}}

# Current working settings:
EMAIL_BACKEND = '{settings.EMAIL_BACKEND}'
EMAIL_HOST = '{getattr(settings, 'EMAIL_HOST', 'NOT SET')}'
EMAIL_PORT = {getattr(settings, 'EMAIL_PORT', 'NOT SET')}
EMAIL_USE_TLS = {getattr(settings, 'EMAIL_USE_TLS', 'NOT SET')}
DEFAULT_FROM_EMAIL = '{settings.DEFAULT_FROM_EMAIL}'
SITE_NAME = '{getattr(settings, 'SITE_NAME', 'NOT SET')}'
DOMAIN = '{getattr(settings, 'DOMAIN', 'NOT SET')}'
"""
    
    with open(f'working_sendgrid_config_backup_{timestamp}.txt', 'w') as f:
        f.write(backup_content)
    
    print(f"✅ Backed up working configuration to: working_sendgrid_config_backup_{timestamp}.txt")
    print("💡 You can use this to restore the working email setup later")

if __name__ == "__main__":
    backup_current_config()
