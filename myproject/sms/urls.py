from django.urls import path
from . import views

app_name = 'sms'

urlpatterns = [
    path('webhook/', views.twilio_webhook, name='twilio-webhook'),
    path('messages/', views.get_sms_messages, name='get-messages'),
    path('messages/<int:sms_id>/read/', views.mark_sms_read, name='mark-read'),
    path('unread-count/', views.get_unread_count, name='unread-count'),
]