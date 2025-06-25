from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from astek_technical_task.accounts.constants import AUTHENTICATION_TAG, USER_TAG
from astek_technical_task.accounts.serializers import (
    LoginSerializer,
    LoginOutputSerializer,
    UserOutputSerializer,
    RegisterSerializer,
    RefreshTokenSerializer,
    RefreshTokenOutputSerializer, UserListOutputSchemaSerializer
)
from astek_technical_task.accounts.services import login_user, create_user
from astek_technical_task.accounts.types import LoginInterface, UserInterface, RefreshTokenInterface
from astek_technical_task.api.pagination import get_paginated_response, LimitOffsetPagination
from astek_technical_task.api.serializers import PaginationParamsSerializer

User = get_user_model()


class LoginApiView(APIView):
    """
    Handle user authentication and return JWT access and refresh tokens.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=[AUTHENTICATION_TAG],
        request=LoginSerializer,
        responses=LoginOutputSerializer,
        operation_id="login_user"
    )
    def post(self, request):
        """
        Authenticate a user and return access and refresh tokens.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        interface = LoginInterface(**serializer.validated_data)
        data = login_user(username=interface.username, password=interface.password)

        return Response(LoginOutputSerializer(data).data)


class ListCreateUserApiView(APIView):
    """
    Allows superusers to register new users or view all users.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        tags=[USER_TAG],
        responses=UserListOutputSchemaSerializer,
        operation_id="list_users",
        parameters=[PaginationParamsSerializer]
    )
    def get(self, request):
        """
        List all registered users with pagination.
        """
        users = User.objects.all()
        return get_paginated_response(
            request=request,
            view=self,
            serializer_class=UserOutputSerializer,
            pagination_class=LimitOffsetPagination,
            queryset=users
        )

    @extend_schema(
        tags=[USER_TAG],
        request=RegisterSerializer,
        responses=UserOutputSerializer,
        operation_id="register_user"
    )
    def post(self, request):
        """
        Register a new user with provided credentials.
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            interface = UserInterface(
                username=serializer.validated_data.get("username"),
                password=serializer.validated_data.get("password"),
                email=serializer.validated_data.get("email"),
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
            )
            user = create_user(user_interface=interface)
            return Response(UserOutputSerializer(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(f"Server error: {e}")


class CustomRefreshTokenView(APIView):
    """
    Refresh access token using refresh token.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=[AUTHENTICATION_TAG],
        request=RefreshTokenSerializer,
        responses=RefreshTokenOutputSerializer,
        operation_id="refresh_token"
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            interface = RefreshTokenInterface(**serializer.validated_data)
            refresh_token_str = interface.refresh
            refresh = RefreshToken(refresh_token_str)
            access = refresh.access_token

            return Response({"access": str(access)}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"detail": _("Invalid or expired refresh token")}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutApiView(APIView):
    """
    Blacklist refresh token to logout user.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=[AUTHENTICATION_TAG],
        request=RefreshTokenSerializer,
        responses=None,
        operation_id="logout"
    )
    def post(self, request):
        refresh_token_str = request.data.get("refresh")
        if not refresh_token_str:
            return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token_str)
            token.blacklist()
            return Response({"detail": _("User logged out successfully")}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": _("Invalid or expired token")}, status=status.HTTP_400_BAD_REQUEST)
