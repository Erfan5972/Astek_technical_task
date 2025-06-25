from django.urls import path

from astek_technical_task.accounts.apis import (
    LoginApiView,
    ListCreateUserApiView,
    CustomRefreshTokenView,
    LogoutApiView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login_user'),
    path('users/', ListCreateUserApiView.as_view(), name='list_create_user'),
    path('token/refresh/', CustomRefreshTokenView.as_view(), name='refresh_token'),
    path('logout/', LogoutApiView.as_view(), name='logout_user')
]
