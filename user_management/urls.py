from django.urls import path

from user_management.views import SignUpView, LoginView, EmailVerifyView

urlpatterns = [
    path("signUp/", SignUpView.as_view(), name="user_sign_up"),
    path("login/", LoginView.as_view(), name="user_login"),
    path("emailVerification/", EmailVerifyView.as_view(), name="email_verification")
]
