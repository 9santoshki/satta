from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoogleLoginView, UserViewSet, GetBalance, DepositMoney, RegisterView, LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet)  # Register the UserViewSet to handle CRUD operations for users

urlpatterns = [
    path('', include(router.urls)),  # Prefixing with versioning

    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Google OAuth
    path('google/', GoogleLoginView.as_view(), name='google-login'),

    # User balance & transactions
    path('balance/', GetBalance.as_view(), name='get-balance'),
    path('deposit/', DepositMoney.as_view(), name='deposit-money'),
]
