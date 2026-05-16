#!/usr/bin/env python
"""
Script to set up Google OAuth app in Django admin
Run this script to create the necessary Social Application for Google OAuth
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_google_oauth():
    """Set up Google OAuth app in Django admin"""
    
    # Get or create the default site
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Local Development'
        }
    )
    
    if created:
        print(f"Created site: {site.domain}")
    else:
        print(f"Using existing site: {site.domain}")
    
    # Check if Google OAuth app already exists
    try:
        google_app = SocialApp.objects.get(provider='google')
        print(f"Google OAuth app already exists: {google_app.name}")
        print(f"Client ID: {google_app.client_id}")
        print(f"Secret Key: {'*' * len(google_app.secret) if google_app.secret else 'Not set'}")
        
        # Check if site is associated
        if site in google_app.sites.all():
            print("Site is already associated with Google OAuth app")
        else:
            google_app.sites.add(site)
            print("Added site to Google OAuth app")
            
    except SocialApp.DoesNotExist:
        print("Google OAuth app not found!")
        print("\nTo create it manually:")
        print("1. Go to http://127.0.0.1:8000/admin/")
        print("2. Navigate to Sites > Social Applications")
        print("3. Add a new Social Application with:")
        print("   - Provider: Google")
        print("   - Name: Google OAuth")
        print("   - Client ID: [Your Google OAuth Client ID]")
        print("   - Secret Key: [Your Google OAuth Client Secret]")
        print("   - Sites: Add the site (127.0.0.1:8000)")
        print("\nOr run this script with your credentials:")
        print("python setup_google_oauth.py --client-id YOUR_CLIENT_ID --secret YOUR_SECRET")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and '--client-id' in sys.argv:
        # Parse command line arguments
        client_id = None
        secret = None
        
        for i, arg in enumerate(sys.argv):
            if arg == '--client-id' and i + 1 < len(sys.argv):
                client_id = sys.argv[i + 1]
            elif arg == '--secret' and i + 1 < len(sys.argv):
                secret = sys.argv[i + 1]
        
        if client_id and secret:
            # Create the Google OAuth app
            site = Site.objects.get(id=1)
            google_app = SocialApp.objects.create(
                provider='google',
                name='Google OAuth',
                client_id=client_id,
                secret=secret
            )
            google_app.sites.add(site)
            print(f"Created Google OAuth app: {google_app.name}")
            print(f"Client ID: {google_app.client_id}")
        else:
            print("Please provide both --client-id and --secret")
    else:
        setup_google_oauth() 