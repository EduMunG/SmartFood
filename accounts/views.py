from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
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