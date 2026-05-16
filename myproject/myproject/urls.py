"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from custom_password_reset import custom_password_reset
# from bulkSMS import views

# Create router for bulkSMS API
# router = DefaultRouter()
# router.register(r'sms-campaigns', views.SMSCampaignViewSet, basename='smscampaign')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Customer.urls'), name='customers'),
    path('', include('Useraccount.urls'), name='user'),
    
    # Custom and Djoser Authentication URLs
    path('auth/users/reset_password/', custom_password_reset, name='custom_password_reset'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # SMS app URLs
    # path('api/sms/', include('sms.urls')),
    
    # bulkSMS API URLs
    # path('api/', include(router.urls)),
    # path('api/sms/', include('bulkSMS.urls')),
    
    # Direct SMS endpoint for cleaner URL
    # path('', include('bulkSMS.urls')),
]



# urlpatterns += [
#     # path('admin/', admin.site.urls),
#     path("api/", include("mambosms.urls")),

# ]
# project/urls.py


urlpatterns += [
    path("api/", include("mambosmssingle.urls")),
    path("api/", include("mambosmsbulk.urls")),

    path("", include("whatsapplinkin.urls")),  # include the app URLs
    path("api/v1/sms/", include("mambosmsbalance.urls")),
    path("api/", include("chatbot.urls")),
    # path("", include("chatbot.urls")),  # include for REDIS
]


from Items import views as items_views
from Menus import views as menus_views
# from Inventory import views as inventory_views
from OrderItem import views as orderitem_views
from Payment import views as payment_views
from Order import views as order_views
from Staff import views as staff_views
from Customer import views as customer_views
from InventoryItems import views as inventoryitems_views

router = DefaultRouter()
router.register(r'staff', staff_views.StaffViewSet)
router.register(r'customer', customer_views.CustomerViewSet)
router.register(r'item', items_views.ItemViewSet)
router.register(r'menu', menus_views.MenuViewSet)
# router.register(r'inventory', inventory_views.InventoryViewSet)
router.register(r'order', order_views.OrderViewSet)
router.register(r'order-item', orderitem_views.OrderItemViewSet)
router.register(r'payment', payment_views.PaymentViewSet)
# router.register(r'staff-list', staff_views.StaffViewSet, basename="staff-list")
router.register(r'stafflist', staff_views.StaffListViewSet, basename="stafflist")
router.register(r'inventory-items', inventoryitems_views.InventoryItemsViewSet)
router.register(r'inventory-items-list', inventoryitems_views.InventoryItemsListViewSet, basename="inventory-items-list")

urlpatterns += [
    path('api/', include(router.urls)),
    # Dedicated endpoint to view items for Menu Item submenu
    path('api/view-menu-item/', items_views.ItemListCreateView.as_view(), name='view-menu-item'),
]



