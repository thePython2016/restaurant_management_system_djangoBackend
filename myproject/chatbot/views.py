import os
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from openai import OpenAI
from django.utils import timezone
from datetime import timedelta

# Safe OpenAI client initialization
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


@api_view(["POST"])
@permission_classes([AllowAny])
def chatbot_response(request):
    user_message = request.data.get("message", "")

    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    # Check if OpenAI API key exists
    if not client:
        return JsonResponse(
            {"error": "OpenAI API key not configured"},
            status=500
        )

    try:
        print(f"OpenAI API Key present: {bool(os.getenv('OPENAI_API_KEY'))}")
        print(f"User message: {user_message}")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
        )

        answer = response.choices[0].message.content

        print(f"OpenAI response: {answer}")

        return JsonResponse({"response": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chatbot_notification(request):
    """
    API endpoint to get chatbot notification status for the user tab
    """

    try:
        user = request.user

        show_notification = True

        notification_data = {
            "show_notification": show_notification,
            "message": "💬 Chat with our AI assistant!",
            "blink": True,
            "chatbot_url": "/api/chatbot/",
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
    """

    try:
        user = request.user

        page_data = {
            "welcome_message": f"Hello {user.first_name or user.username}! 👋",
            "subtitle": "I'm your AI assistant. How can I help you today?",
            "placeholder": "Type your message here...",
            "chat_history": [],
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
@permission_classes([AllowAny])
def track_user_activity(request):
    """
    Track user activity
    """

    try:
        user = getattr(request, 'user', None)
        current_time = timezone.now()

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
@permission_classes([AllowAny])
def check_idle_assistance(request):
    """
    Check if user needs assistance after being idle
    """

    try:
        user = getattr(request, 'user', None)
        current_time = timezone.now()

        last_activity_str = request.session.get('last_activity')

        if not last_activity_str:
            request.session['last_activity'] = current_time.isoformat()

            return JsonResponse({
                "show_assistance": False,
                "message": "No previous activity recorded"
            })

        last_activity = timezone.datetime.fromisoformat(
            last_activity_str.replace('Z', '+00:00')
        )

        idle_duration = current_time - last_activity

        idle_threshold_minutes = 1
        idle_threshold = timedelta(minutes=idle_threshold_minutes)

        if idle_duration >= idle_threshold:

            user_name = "User"

            if user and hasattr(user, 'first_name') and user.first_name:
                user_name = user.first_name
            elif user and hasattr(user, 'username'):
                user_name = user.username

            assistance_data = {
                "show_assistance": True,
                "idle_minutes": int(idle_duration.total_seconds() / 60),
                "message": (
                    f"👋 Hi {user_name}! "
                    f"You've been here for "
                    f"{int(idle_duration.total_seconds() / 60)} minutes. "
                    f"Need any help?"
                ),
                "subtitle": "I'm here to assist you with anything you need!",
                "assistance_options": [
                    "Get help with your account",
                    "Learn about our features",
                    "Technical support",
                    "General questions"
                ],
                "chatbot_url": "/api/chatbot/",
                "icon": "🤖",
                "color": "#FF6B35",
                "blink": True,
                "priority": "high"
            }

            return JsonResponse(assistance_data)

        else:
            return JsonResponse({
                "show_assistance": False,
                "idle_minutes": int(idle_duration.total_seconds() / 60),
                "message": (
                    f"User active for "
                    f"{int(idle_duration.total_seconds() / 60)} minutes"
                )
            })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([AllowAny])
def dismiss_assistance(request):
    """
    Dismiss assistance notification
    """

    try:
        current_time = timezone.now()

        request.session['last_activity'] = current_time.isoformat()

        return JsonResponse({
            "success": True,
            "message": "Assistance notification dismissed",
            "timestamp": current_time.isoformat()
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)