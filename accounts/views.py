import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from accounts.models import Food, DailyIntake
from django.db.models import F
from django.contrib import messages
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



@login_required
def agregar_alimento(request):
    selected_foods = request.session.get('selected_foods', [])
    alimentos = Food.objects.filter(name__in=selected_foods)
    
    if request.method == 'POST' and 'save' in request.POST:
        user = request.user
        daily_intake, created = DailyIntake.objects.get_or_create(user=user, date=datetime.date.today(), defaults={'calories': 0, 'proteins': 0, 'fats': 0, 'carbohydrates': 0})
        
        for food in alimentos:
            daily_intake.calories = F('calories') + food.energ_kal
            daily_intake.proteins = F('proteins') + food.proteina
            daily_intake.fats = F('fats') + food.lipid_tot
            daily_intake.carbohydrates = F('carbohydrates') + food.carbohydrt
        daily_intake.save()
        daily_intake.refresh_from_db()

        # Limpiar la selección después de guardar
        request.session['selected_foods'] = []
        messages.success(request, 'Alimentos guardados correctamente.')


    context = {
        'alimentos': selected_foods,
        'selected_foods': alimentos,
    }
    return render(request, 'accounts/search/agregar_alimento.html', context)


@login_required
def buscar_alimento(request):
    query = request.GET.get('query')
    resultados = []

    if query:
        resultados = Food.objects.filter(name__icontains=query)

    if request.method == 'POST':
        food_id = request.POST.get('name')

        if 'selected_foods' not in request.session:
            request.session['selected_foods'] = []
        
        request.session['selected_foods'].append(food_id)
        request.session.modified = True

        return redirect('agregar_alimento')
    

    context = {
        'resultados': resultados,
        'query': query,
    }
    return render(request, 'accounts/search/buscar_alimento.html', context)


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
    
