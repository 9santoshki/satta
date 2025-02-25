from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import requests, logging
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .models import UserProfile
from .serializers import UserSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


logger = logging.getLogger(__name__)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Google token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            google_response = requests.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}")
            if google_response.status_code != 200:
                return Response({"error": "Invalid Google token."}, status=status.HTTP_400_BAD_REQUEST)

            google_user_info = google_response.json()

            required_fields = ['sub', 'email', 'given_name', 'family_name']
            if not all(field in google_user_info for field in required_fields):
                return Response({"error": "Missing required Google user info."}, status=status.HTTP_400_BAD_REQUEST)

            # Create or retrieve user
            user, created = User.objects.get_or_create(
                username=google_user_info['sub'],
                defaults={
                    'email': google_user_info['email'],
                    'first_name': google_user_info['given_name'],
                    'last_name': google_user_info['family_name']
                }
            )

            if created:
                user.set_unusable_password()
                user.save()

            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Error verifying Google token: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DepositMoney(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            amount = float(request.data.get("amount"))
            if amount <= 0:
                return Response({"detail": "Invalid deposit amount."}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({"detail": "Amount must be a valid number."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = get_object_or_404(UserProfile, user=user)
        user_profile.deposit(amount)  
        return Response({"balance": str(user_profile.balance)}, status=status.HTTP_200_OK)

class GetBalance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        return Response({"balance": str(user_profile.balance)}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")
            print(request.data)
            if not username or not email or not password:
                return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = User(username=username, email=email)
            user.set_password(password)  # Secure password storage
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            return Response({"message": "User registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in RegisterView: {e}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user) 

    def perform_create(self, serializer):
        user = serializer.save()
        user.balance = 0  
        user.save()
