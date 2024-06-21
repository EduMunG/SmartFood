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
from .models import UserProfile
from .forms import UserProfileForm
from django.db.models import Sum
from .import test,entradaGenetico,utility






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
    if request.user.is_authenticated:
        user = request.user
        # Obtener el perfil del usuario
        user_profile = get_object_or_404(UserProfile, user=user)
        # Pasar los datos del perfil al contexto
        meals = make_meal(user_profile)

        context = {
            'user': user,
            'fa': user_profile.fa,
            'kg': user_profile.kg,
            'edad': user_profile.edad,
            'objetivo': user_profile.objetivo,
            'desayuno': meals[0],
            'colacion':meals[1],
            'comida': meals[2],
            'cena': meals[3],

        }
        return render(request, 'accounts/home.html', context)
    else:
        return redirect('login')


 

@login_required
def agregar_alimento(request):
    if request.method == 'POST' and 'save' in request.POST:
        selected_foods = request.session.get('selected_foods', [])

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

        return redirect('consumo')  # Redirigir a la página de consumo después de guardar

    else:
        messages.error(request, 'No se pudo guardar los alimentos.')

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
            return render(request, 'accounts/register_done.html', {'data_form': data_form})
    else:
        data_form = forms.takeDataUser()

    return render(request, 'accounts/takeData.html', {'data_form': data_form})
    

def cambiar_inf(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la URL con nombre 'home'
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

    context = {
        'selected_foods': alimentos,
        'total_calorias': total_calorias,
        'total_proteinas': total_proteinas,
        'total_grasas': total_grasas,
        'total_carbohidratos': total_carbohidratos,
    }
    return render(request, 'accounts/search/consumo.html', context)

def info(request):
    return render(request, 'accounts/info.html')


def make_meal(user):
    bets_foods = []

    desayuno, colacion, comida ,cena = entradaGenetico.get_vectores_Desayuno_Comida_Colacion_Cena(user.kg,user.fa, user.objetivo)

    vectores = [desayuno, colacion, comida, cena]
    num_meals = [4,3,3,3]

    for comidas,num_meal in zip(vectores, num_meals):

        indexes = test.genetic(comidas,num_meal,100,0.9,0.5,100)
        print("Indezzz",indexes)
        # Convertir la lista de índices a un QuerySet

        foods_info = Food.objects.filter(index__in=indexes).values('name', 'energ_kal', 'carbohydrt', 'lipid_tot','proteina')

         # Iterar sobre cada diccionario para imprimir la proteina
        for food in foods_info:
            print("Proteina:", food['proteina'])

        bets_foods.append(foods_info)

        #bets_foods.append(Food.objects.filter(index__in=indexes))
    

    return bets_foods

