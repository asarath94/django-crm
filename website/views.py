from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import signupform, AddRecordForm
from .models import record

# Create your views here.
def home(request): 
    records = record.objects.all()


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
        return render(request, 'home.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('home')

def signup_user(request):
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully signed up.")
            return redirect('home')
        
    else:
        form = signupform()
        return render(request, 'signup.html', {'form': form})
        
    return render(request, 'signup.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        #look up records
        customer_record = record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})

    else:
        messages.success(request, "You have to be logged-in to view this page.")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "You have successfully deleted the customer record.")
        return redirect('home')
    else:
        messages.success(request, "You have to be logged-in to delete the record.")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added..")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in..")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated..")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in..")
        return redirect('home')






