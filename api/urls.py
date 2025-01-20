"""
URL configuration for API.
"""
from django.urls import path, include
from django.contrib import admin
from webshop.views import ProductViewSet
from rest_framework.routers import DefaultRouter, APIRootView


class WebshopAPIRootView(APIRootView):
    pass


class ApiRouter(DefaultRouter):
    APIRootView = WebshopAPIRootView


router = ApiRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
]
