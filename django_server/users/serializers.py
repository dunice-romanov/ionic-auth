from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.serializers import raise_errors_on_nested_writes, model_meta

class UserUpdateSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True)

    def create(self, data):
        username = data['username']
        email = data['email']
        password = data['password']
        try:
            user = User.objects.create_user(username, email=email, password=password)
        except: 
            raise TypeError('cant create user')
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')