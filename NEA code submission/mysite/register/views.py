from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def aplog(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('apchome')  # Redirect to your home page
        else: 
          messages.warning(request, 'email or password or member code not correct')
    return render(request, 'main/aplog.html')


def adlog(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
         member_code = request.POST.get('member_code')  # get the member code
         if member_code == "8853":
            login(request, user)
            return redirect('home')  # Redirect to your home page
        else: 
          messages.warning(request, 'email or password or member code not correct')
          
    return render(request, 'main/adlog.html')


def sign(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('aplog')  # Named URL instead of hardcoding path
    else:
        form = UserCreationForm()
    return render(request, 'main/signup1.html', {'form': form})
    


# Example alternative signup view (commented out)
# def signup(request):
#     form = UserCreationForm()
#     return render(request, 'register/signup1.html', {'form': form})  