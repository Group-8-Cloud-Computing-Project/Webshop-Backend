"""
URL configuration for API.
"""
from django.urls import path, include
from django.contrib import admin
from webshop.views import ProductViewSet
from rest_framework.routers import DefaultRouter, APIRootView
from webshop.views import OrderViewSet
from webshop.views import InventoryViewSet
from webshop.views import EmailNotificationViewSet

class WebshopAPIRootView(APIRootView):
    pass


class ApiRouter(DefaultRouter):
    APIRootView = WebshopAPIRootView


router = ApiRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'email-notifications', EmailNotificationViewSet, basename='email-notification')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
]

