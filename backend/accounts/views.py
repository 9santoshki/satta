import google.auth.transport.requests
import google.oauth2.id_token
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserProfileSerializer
from .models import UserProfile

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({"error": "Google token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the Google ID token
            request_adapter = google.auth.transport.requests.Request()
            google_user_info = google.oauth2.id_token.verify_oauth2_token(
                token, request_adapter
            )

            if not google_user_info:
                return Response({"error": "Invalid Google token."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure required fields exist
            email = google_user_info.get("email")
            first_name = google_user_info.get("given_name", "")
            last_name = google_user_info.get("family_name", "")
            google_id = google_user_info.get("sub")

            if not email or not google_id:
                return Response({"error": "Missing required user info."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user exists or create new one
            user, created = get_user_model().objects.get_or_create(
                username=google_id,
                defaults={"email": email, "first_name": first_name, "last_name": last_name}
            )

            if created:
                user.set_unusable_password()
                user.save()

            # Generate authentication token for the user
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key, "user": UserProfileSerializer(user).data}, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid or expired Google token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
