from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse

def home(request):
    return render(request, 'pages/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(reverse('tracker'))
        else:
            form - UserCreationForm()
        return render(request, 'pages/signup.html', {'form', form})


    
def tracker(request):
    return render(request, 'pages/tracker.html')
    