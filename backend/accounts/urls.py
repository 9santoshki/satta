from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoogleLoginView, GetBalance, DepositMoney, UserProfileViewSet
# UserProfileViewSet (if you're using a ViewSet, you can register it with the router)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)  # Uncomment if you have a UserProfileViewSet

urlpatterns = [
    path('', include(router.urls)),
    path('profiles/<str:user_id>/', UserProfileViewSet.as_view({'get': 'retrieve'})),
    path('google/', GoogleLoginView.as_view(), name='google-login'),  # Add Google login endpoint
    path('balance/', GetBalance.as_view(), name='get-balance'),  # Endpoint for getting balance
    path('deposit/', DepositMoney.as_view(), name='deposit-money'),  # Endpoint for depositing money
]
