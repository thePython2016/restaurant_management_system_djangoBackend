from django.urls import path
from . import views  # Import from same directory

urlpatterns = [
    # ... your existing URLs ...
    path('api/v1/sms/single/', views.send_sms_view, name='send_sms'),
]