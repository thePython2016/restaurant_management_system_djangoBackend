from django.urls import path
from .views import send_bulk_sms_view

urlpatterns = [
    path('v1/sms/bulk-send/', send_bulk_sms_view, name='send_bulk_sms'),
]
# # FOR AIRTIME CONFIG
# from .views import airtime_view

# # urlpatterns += [
# #     path('send-airtime/', airtime_view),
# # ]
