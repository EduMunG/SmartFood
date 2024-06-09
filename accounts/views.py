from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from . import forms

def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = forms.LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'accounts/home.html', {'user': user})
    else:
        user = None
        return redirect('login')
    
def logout(request):
    auth_logout(request)
    return render(request, 'accounts/logout.html')


def register(request):
    if request.method == 'POST':
        #print('PRINT1')
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            print('PRINT2')
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            login(request, new_user)
            return redirect('takeData')
    else:
        #print('PRINT3')
        user_form = forms.UserRegistrationForm()

    return render(request,'accounts/register.html',{'user_form': user_form})

@login_required
def takeData(request):
    if request.method == 'POST':
        data_form = forms.takeDataUser(request.POST)
        if data_form.is_valid():
            user_profile = data_form.save(commit=False)
            user_profile.user = request.user  # Asocia el perfil al usuario autenticado
            print(user_profile.user.username)
            user_profile.save()
            print('User profile data saved successfully.')
            return render(request, 'accounts/register_done.html', {'data_form': data_form})
    else:
        data_form = forms.takeDataUser()

    return render(request, 'accounts/takeData.html', {'data_form': data_form})
    
