from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ServiceViewSet,
    ServiceRequestViewSet,
    ReviewViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'requests', ServiceRequestViewSet, basename='request')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
