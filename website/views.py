from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request): 
    #check to see if someone is logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #authenticate credentials
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged-in")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, Wrong credentials")
            return redirect('home')

    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('home')

def signup_user(request):
    return render(request, 'signup.html', {})