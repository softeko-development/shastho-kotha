from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from user.decorators import *
from user.models import CustomUser

@login_required(login_url='login_page')
@user_passes_test(lambda user: is_staff_or_has_role(user, "doctor", "staff", "pharmacy", roles=['Manager']))
def dashboard(request):
    context = {
        'heading': "Dashboard"
    }
    return render(request, 'dashboard.html', context)

def home_page(request):
    return render(request, 'index.html')
def privacy_policy(request):
    return render(request, 'privacy-policy.html')
def delete_account(request):
    return render(request, 'delete-account.html')

def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.status == CustomUser.Status.ACTIVE:  # Check if the user status is ACTIVE
                login(request, user)
                return redirect('dashboard')  # Redirect to your dashboard after login
            else:
                messages.error(request, 'Your account is not active. Please contact support.')
                return redirect('login_page')  # Redirect to the login page with an error message
        else:
            messages.error(request, 'Invalid Username or Password!')
            return redirect('login_page')  # Redirect to the login page with an error message

    context = {
        'heading': 'Login'
    }
    return render(request, 'login.html', context)

@login_required(login_url='login_page')
def logoutPage(request):
    logout(request)
    return redirect('login_page') 