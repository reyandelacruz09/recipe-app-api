"""
Views for the user API
"""
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from core.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import (
    viewsets,
)
from core import core_functions


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


@api_view(['POST'])
def login(request):

    user = get_object_or_404(
        User,
        Q(username=request.data['username']) |
        Q(email=request.data['username'])
    )

    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


class UserView(
    viewsets.ModelViewSet,
    core_functions.Core
):
    pass
