# events/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, OutcomeViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'outcomes', OutcomeViewSet)

# The API URLs are now automatically created by the router
urlpatterns = [
    path('', include(router.urls)),  # Include all the router-generated URLs
]
