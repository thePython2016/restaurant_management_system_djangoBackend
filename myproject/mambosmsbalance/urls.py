from django.urls import path
from . import views

app_name = 'mambosmsbalance'

urlpatterns = [
    path("balance/", views.get_sms_balance, name="sms-balance"),
    path("balance/test/", views.get_sms_balance_test, name="sms-balance-test"),
]
