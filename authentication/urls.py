from .views import UsernameValidationView, EmailValidationView, RegistrationView, LoginView, LogoutView, RequestPasswordResetEmail
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate_username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validate_email"),
    path('request_reset_link', RequestPasswordResetEmail.as_view(), name="request_password"),
]