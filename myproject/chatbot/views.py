import os
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from openai import OpenAI
from django.utils import timezone
from datetime import timedelta

# Initialize OpenAI client (key from environment, not hardcoded!)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@api_view(["POST"])
@permission_classes([AllowAny])
def chatbot_response(request):
    user_message = request.data.get("message", "")

    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    try:
        print(f"OpenAI API Key present: {bool(os.getenv('OPENAI_API_KEY'))}")  # Debug log
        print(f"User message: {user_message}")  # Debug log
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # small + cheap, works well
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
        )
        answer = response.choices[0].message.content
        print(f"OpenAI response: {answer}")  # Debug log
        return JsonResponse({"response": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chatbot_notification(request):
    """
    API endpoint to get chatbot notification status for the user tab
    Returns data needed for frontend to show blinking notification
    """
    try:
        # You can customize this logic based on your needs
        # For example, show notification only for new users or based on user preferences
        user = request.user
        
        # Check if user has ever used the chatbot
        # This is a simple example - you might want to track this in a database
        show_notification = True  # Always show for now, you can add logic here
        
        notification_data = {
            "show_notification": show_notification,
            "message": "💬 Chat with our AI assistant!",
            "blink": True,
            "chatbot_url": "/api/chatbot/",  # URL to redirect to chatbot
            "icon": "🤖",
            "color": "#007bff"
        }
        
        return JsonResponse(notification_data)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chatbot_page(request):
    """
    API endpoint to get chatbot page data
    Returns welcome message and initial data for the chatbot interface
    """
    try:
        user = request.user
        
        page_data = {
            "welcome_message": f"Hello {user.first_name or user.username}! 👋",
            "subtitle": "I'm your AI assistant. How can I help you today?",
            "placeholder": "Type your message here...",
            "chat_history": [],  # You can implement chat history storage later
            "user_info": {
                "name": user.first_name or user.username,
                "email": user.email
            },
            "features": [
                "Ask me anything!",
                "Get help with your account",
                "Learn about our services",
                "Get technical support"
            ]
        }
        
        return JsonResponse(page_data)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([AllowAny])  # Changed to AllowAny for testing
def track_user_activity(request):
    """
    API endpoint to track user activity and update last activity timestamp
    Call this endpoint whenever user interacts with the app
    """
    try:
        user = getattr(request, 'user', None)
        current_time = timezone.now()
        
        # Store last activity time in user's session or a simple cache
        # For now, we'll use a simple approach - in production you might want to use Redis or database
        request.session['last_activity'] = current_time.isoformat()
        if user and hasattr(user, 'id'):
            request.session['user_id'] = user.id
        else:
            request.session['user_id'] = 'anonymous'
        
        return JsonResponse({
            "success": True,
            "message": "Activity tracked",
            "timestamp": current_time.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])  # Changed to AllowAny for testing
def check_idle_assistance(request):
    """
    API endpoint to check if user needs assistance based on idle time
    Returns notification data if user has been idle for too long
    """
    try:
        user = getattr(request, 'user', None)
        current_time = timezone.now()
        
        # Get last activity time from session
        last_activity_str = request.session.get('last_activity')
        
        if not last_activity_str:
            # If no activity recorded, set current time as last activity
            request.session['last_activity'] = current_time.isoformat()
            return JsonResponse({
                "show_assistance": False,
                "message": "No previous activity recorded"
            })
        
        # Parse last activity time
        last_activity = timezone.datetime.fromisoformat(last_activity_str.replace('Z', '+00:00'))
        
        # Calculate idle time
        idle_duration = current_time - last_activity
        
        # Define idle threshold (1 minute = 60 seconds)
        idle_threshold_minutes = 1
        idle_threshold = timedelta(minutes=idle_threshold_minutes)
        
        # Check if user has been idle for too long
        if idle_duration >= idle_threshold:
            # Get user name for message
            user_name = "User"
            if user and hasattr(user, 'first_name') and user.first_name:
                user_name = user.first_name
            elif user and hasattr(user, 'username'):
                user_name = user.username
            
            assistance_data = {
                "show_assistance": True,
                "idle_minutes": int(idle_duration.total_seconds() / 60),
                "message": f"👋 Hi {user_name}! You've been here for {int(idle_duration.total_seconds() / 60)} minutes. Need any help?",
                "subtitle": "I'm here to assist you with anything you need!",
                "assistance_options": [
                    "Get help with your account",
                    "Learn about our features", 
                    "Technical support",
                    "General questions"
                ],
                "chatbot_url": "/api/chatbot/",
                "icon": "🤖",
                "color": "#FF6B35",  # Orange color to grab attention
                "blink": True,
                "priority": "high"
            }
            return JsonResponse(assistance_data)
        else:
            return JsonResponse({
                "show_assistance": False,
                "idle_minutes": int(idle_duration.total_seconds() / 60),
                "message": f"User active for {int(idle_duration.total_seconds() / 60)} minutes"
            })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([AllowAny])  # Changed to AllowAny for testing
def dismiss_assistance(request):
    """
    API endpoint to dismiss the assistance notification
    Resets the idle timer when user dismisses the notification
    """
    try:
        user = getattr(request, 'user', None)
        current_time = timezone.now()
        
        # Reset last activity time to dismiss the notification
        request.session['last_activity'] = current_time.isoformat()
        
        return JsonResponse({
            "success": True,
            "message": "Assistance notification dismissed",
            "timestamp": current_time.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
