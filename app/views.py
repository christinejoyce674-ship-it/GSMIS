from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.EmailBackEnd import EmailBackEnd
from app.models import CustomUser



def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect('admin_dashboard')
        elif request.user.user_type == '2':
          return redirect('teacher_home')
    elif request.user.user_type == '3':
         return redirect('parent_dashboard')
        

def doLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = EmailBackEnd.authenticate(
            request,
            username=email,
            password=password
        )
        
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_dashboard')
            elif user_type == '2':
                return redirect('teacher_home')
            elif user_type == '3':
                return redirect('parent_dashboard')
        else:
            messages.error(request, 'Invalid Email or Password!')
            return redirect('login')
            
    return redirect('login')

def doLogout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')



def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)