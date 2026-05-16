from django.urls import path
from .views import (
    chatbot_response, 
    chatbot_notification, 
    chatbot_page,
    track_user_activity,
    check_idle_assistance,
    dismiss_assistance
)

urlpatterns = [
    path("chat/", chatbot_response, name="chatbot_response"),
    path("notification/", chatbot_notification, name="chatbot_notification"),
    path("page/", chatbot_page, name="chatbot_page"),
    path("track-activity/", track_user_activity, name="track_user_activity"),
    path("idle-assistance/", check_idle_assistance, name="check_idle_assistance"),
    path("dismiss-assistance/", dismiss_assistance, name="dismiss_assistance"),
]
