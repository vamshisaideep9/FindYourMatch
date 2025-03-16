from django.urls import path
from .views import SignupView, LoginView
from .views import (
    EmailVerificationView, VerifyEmailView,
    PasswordResetView, PasswordResetConfirmView,
    UsernameResetView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]


urlpatterns += [
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='email-verify'),
    path('reset-password/', PasswordResetView.as_view(), name='password-reset'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset-username/', UsernameResetView.as_view(), name='username-reset'),
]
