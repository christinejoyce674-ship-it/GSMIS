from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib import messages


def home(request):
    return render(request, "home.html")

def landing(request):
    return render(request, "landing.html")

def login_page(request):
    if request.user.is_authenticated:
        u_type = str(request.user.user_type)
        if u_type == '1' or u_type == '4':
            return redirect('app:hod_home')
        elif u_type == '2':
            return redirect('app:teacher_home')
        elif u_type == '3':
            return redirect('app:parent_dashboard')
    return render(request, 'login.html')

def doLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Login the user - Django will create a new session
            login(request, user)
            
            # Get user type and redirect accordingly
            u_type = str(user.user_type)
            if u_type == '1' or u_type == '4':
                return redirect('app:hod_home')
            elif u_type == '2':
                return redirect('app:teacher_home')
            elif u_type == '3':
                return redirect('app:parent_dashboard')
            else:
                messages.error(request, 'Invalid user type!')
                return redirect('app:login')
        else:
            messages.error(request, 'Invalid Email or Password!')
            return redirect('app:login')
            
    return redirect('app:login')

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('app:login')