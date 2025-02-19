from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response  # Import Response
from rest_framework.views import APIView
import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import UserProfile

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for testing
class GoogleLoginView(APIView):
    def options(self, request, *args, **kwargs):
        response = JsonResponse({}, status=200)  # Use JsonResponse
        response["Access-Control-Allow-Origin"] = settings.CORS_ALLOWED_ORIGINS[0]  # Use correct domain
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return JsonResponse({"error": "Google token is required."}, status=400)

        try:
            google_response = requests.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}")
            
            if google_response.status_code != 200:
                return JsonResponse({"error": "Invalid Google token."}, status=400)

            google_user_info = google_response.json()
            
            # Ensure necessary fields exist
            if not all(key in google_user_info for key in ['sub', 'email', 'given_name', 'family_name']):
                return JsonResponse({"error": "Missing required Google user info."}, status=400)

            # Find or create user
            from django.contrib.auth import get_user_model
            user, created = get_user_model().objects.get_or_create(
                username=google_user_info['sub'],
                defaults={'email': google_user_info['email'], 'first_name': google_user_info['given_name'], 'last_name': google_user_info['family_name']}
            )
            if created:
                user.set_unusable_password()
                user.save()

            # Return JSON with explicit CORS headers
            response = JsonResponse({"message": "Login successful", "user": google_user_info}, status=200)
            response["Access-Control-Allow-Origin"] = settings.CORS_ALLOWED_ORIGINS[0]  # Use frontend URL
            response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Error verifying Google token: {str(e)}"}, status=500)



class DepositMoney(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        user = request.user  # Get the authenticated user
        amount = request.data.get("amount")

        if not amount or amount <= 0:
            return Response({"detail": "Invalid deposit amount."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_profile = get_object_or_404(UserProfile, id=user.id)
            user_profile.deposit(amount)  # Add the amount to the user's balance
            return Response({"balance": str(user_profile.balance)}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetBalance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            user_profile = UserProfile.objects.get(id=user.id)
            return Response({"balance": str(user_profile.balance)}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)