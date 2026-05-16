from django.urls import path
from . import views

urlpatterns = [
    path("api/send-whatsapp/", views.send_whatsapp_message, name="send_whatsapp"),
]
