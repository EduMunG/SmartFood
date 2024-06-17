import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from accounts.models import Food, DailyIntake
from django.db.models import F
from django.contrib import messages
from . import forms
from .models import Goal, UserProfile
from .forms import UserProfileForm
from django.db.models import Sum
from .genetic_algorithm import *
from .utils import make_meal, actualizarmeta
from django.views.decorators.csrf import csrf_protect





@csrf_protect
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

@login_required
def home(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'GET':
        desayuno, colacion, comida, cena = make_meal(user)
        # Pasar los datos del perfil al contexto
        context = {
            'user': user,
            'fa': user_profile.fa,
            'kg': user_profile.kg,
            'edad': user_profile.edad,
            'Estatura': user_profile.cm,
            'objetivo': user_profile.objetivo,
            'desayuno': desayuno,
            'colacion': colacion,
            'comida': comida,
            'cena': cena,
        }

    return render(request, 'accounts/home.html', context)


@login_required
def agregar_alimento(request):
    return render(request, 'accounts/search/agregar_alimento.html')

@login_required
def buscar_alimento(request):
    query = request.GET.get('query')
    meal_type = request.GET.get('meal', '')
    resultados = []
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

        return redirect('consumo')


    context = {
        'resultados': resultados,
        'query': query,
        'meal_type': meal_type,
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
            actualizarmeta(request)  # Call the actualizarmeta function
            return render(request, 'accounts/register_done.html', {'data_form': data_form})
    else:
        data_form = forms.takeDataUser()

    return render(request, 'accounts/takeData.html', {'data_form': data_form})




@login_required
def cambiar_inf(request):
    user_profile = request.user.userprofile
    _ = Goal.objects.get_or_create(
        user=request.user,
        defaults={'daily_calories': 0, 'protein_percentage': 0, 'carbohydrate_percentage': 0, 'fat_percentage': 0})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            actualizarmeta(request.user)  # Call the actualizarmeta function with the user instance
            return redirect('home')  # Redirect to the URL with name 'home'
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'accounts/cambiar_inf.html', {'form': form})






    
@login_required
def consumo(request):
    selected_foods = request.session.get('selected_foods', [])
    alimentos = Food.objects.filter(name__in=selected_foods)

    # Calcular el total de nutrientes consumidos
    total_calorias = alimentos.aggregate(Sum('energ_kal'))['energ_kal__sum'] or 0
    total_proteinas = alimentos.aggregate(Sum('proteina'))['proteina__sum'] or 0
    total_grasas = alimentos.aggregate(Sum('lipid_tot'))['lipid_tot__sum'] or 0
    total_carbohidratos = alimentos.aggregate(Sum('carbohydrt'))['carbohydrt__sum'] or 0

    # Limpiar la selección de alimentos
    if request.method == 'POST' and 'clear' in request.POST:
        if 'clear' in request.POST:
            request.session['selected_foods'] = []
            request.session.modified = True
            messages.success(request, 'Selección de alimentos eliminada.')
            return redirect('consumo')
        
    # Guardar el consumo diario
    if request.method == 'POST' and 'save' in request.POST:
        user = request.user
        # Obtener o crear el registro de consumo diario para el usuario y la fecha actual
        daily_intake, created = DailyIntake.objects.get_or_create(
            user=user,
            date=datetime.date.today(),
            defaults={'calories': 0, 'proteins': 0, 'fats': 0, 'carbohydrates': 0}
        )
        
        # Filtrar los alimentos seleccionados desde la base de datos
        alimentos = Food.objects.filter(name__in=selected_foods)

        # Actualizar el consumo diario con los nutrientes de los alimentos seleccionados
        for food in alimentos:
            daily_intake.calories = F('calories') + food.energ_kal
            daily_intake.proteins = F('proteins') + food.proteina
            daily_intake.fats = F('fats') + food.lipid_tot
            daily_intake.carbohydrates = F('carbohydrates') + food.carbohydrt
        
        # Guardar los cambios en el registro de consumo diario
        daily_intake.save()
        daily_intake.refresh_from_db()

        # Limpiar la selección después de guardar
        request.session['selected_foods'] = []
        messages.success(request, 'Alimentos guardados correctamente.')

        return redirect('consumo')
         

    context = {
        'selected_foods': alimentos,
        'total_calorias': total_calorias,
        'total_proteinas': total_proteinas,
        'total_grasas': total_grasas,
        'total_carbohidratos': total_carbohidratos,
    }
    return render(request, 'accounts/search/consumo.html', context)




