from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, VerifyView, SuccessVerificationView, ErrorVerificationView, \
    GenerateAndSendPasswordView, CustomLoginView, UserBlockedView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/verify_email/', VerifyView.as_view(), name='verify_email'),

    path('verify_success/', SuccessVerificationView.as_view(), name='success_verification'),
    path('verify_error/', ErrorVerificationView.as_view(), name='error_verification'),

    path('password_recovery/', GenerateAndSendPasswordView.as_view(), name='password_recovery'),
    path('blocked_user/', UserBlockedView.as_view(), name='user_blocked'),
]
