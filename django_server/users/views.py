from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer, UserUpdateSerializer

class UsersViewSet(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return  UserSerializer
    
    def create_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(username=serializer.data['username'])
        token = self.create_token(user)
        context = { 'token': token }
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        if 'password' in self.request.data:
            print('in if')  
            password_ = serializer.validated_data['password']
            password = make_password(password_)
            serializer.validated_data['password'] = password
        return super().perform_update(serializer)