# accounts/views.py
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth import get_user_model

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        data = request.data
        user = UserProfile.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
