from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoogleLoginView
# UserProfileViewSet
router = DefaultRouter()
# router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('google/', GoogleLoginView.as_view(), name='google-login'),  # Add Google login endpoint
]
