from django.contrib.auth import get_user_model

from rest_framework import serializers

from astek_technical_task.api.serializers import ListSerializerSchema

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LoginOutputSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class UserListOutputSchemaSerializer(ListSerializerSchema):
    results = UserOutputSerializer()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RefreshTokenOutputSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()