import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth.models import User
from django.core.mail import send_mail

def check_users():
    print("🔍 Checking users in database...")
    users = User.objects.all()
    
    if users.exists():
        print(f"✅ Found {users.count()} user(s):")
        for user in users:
            print(f"  - {user.email} ({user.username})")
    else:
        print("❌ No users found in database!")
        print("💡 You need to create a user first for password reset to work.")
        return False
    
    return True

def test_email():
    print("\n🧪 Testing email configuration...")
    try:
        send_mail(
            subject='Password Reset Test - Django App',
            message='This is a test email from your Django application. If you receive this, your email configuration is working correctly!',
            from_email='infonet20th@gmail.com',
            recipient_list=['infonet20th@gmail.com'],
            fail_silently=False,
        )
        print("✅ Email test successful! Check your email inbox.")
        return True
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Django Email Configuration Check")
    print("=" * 40)
    
    # Check users
    has_users = check_users()
    
    # Test email
    if has_users:
        test_email()
    
    print("\n📋 Next Steps:")
    if not has_users:
        print("1. Create a user first: python manage.py createsuperuser")
        print("2. Or register a user through your app")
    print("3. Try password reset again from your React app")
    print("4. Check your email for the reset link")
