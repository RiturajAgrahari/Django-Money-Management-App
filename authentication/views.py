from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth

# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Invalid Email'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email is use, choose another one'}, status=409)
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contains alphanumeric characters'},
                                status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username is use, choose another one'}, status=409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # CREATE A USER ACCOUNT

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]


        context = {
            'fieldValue': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, "Password length must be greater than 5!")
                    return render(request, 'register.html', context=context)
                else:
                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)
                    user.is_active = True
                    user.save()
                    return redirect('login')

        # messages.success(request, "Success Whatsapp success")
        # messages.warning(request, "Success Whatsapp warning")
        # messages.info(request, "Success Whatsapp info")
        # messages.error(request, "Success Whatsapp error")

        return render(request, 'register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome, {user.username} you are now logged in")
                    return redirect('add_expense')

                messages.error(request, "account is not active, please check your email")
                return render(request, 'login.html')

            messages.error(request, "Invalid Credentials, try again!")
            return render(request, 'login.html')

        messages.error(request, "Please fill all fields")
        return render(request, "login.html")


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out!")
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'reset_password.html')

    def post(self, request):
        email = request.POST['email']
        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, "Please supply a valid email")
            return render(request, 'reset_password.html', context)

        return render(request, 'reset_password.html')
