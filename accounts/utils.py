from .genetic_algorithm import genetic
from .models import Goal, Food, UserProfile
import random






def calculaCalorias(objetivo, caloriasQuemadas):
    if objetivo == "subir":
        superAvit = caloriasQuemadas*0.1
        calorias = caloriasQuemadas+superAvit
    else:
        deficit = caloriasQuemadas*0.1
        calorias = caloriasQuemadas-deficit
    return calorias


def caloriasQuemadas(Kg, FA):
    return Kg*FA*22

def get_vectores_Desayuno_Comida_Colacion_Cena(kg, fa, objetivo):
    caloriasDia = calculaCalorias(objetivo, caloriasQuemadas(kg, fa))
    
    ### Macros ###
    if objetivo == 'subir':
        proteina = 2 * kg
        grasa = 1.5 * kg
        carbos = (caloriasDia - proteina * 4 - grasa * 9) / 4
    else:  # Asumimos que cualquier otro objetivo es bajar de peso
        proteina = 2.5 * kg
        grasa = 0.6 * kg
        carbos = (caloriasDia - proteina * 4 - grasa * 9) / 4
    
    vectorDia = [caloriasDia, grasa, carbos, proteina]
    
    # Usamos una comprensión de listas para multiplicar cada elemento de vectorDia y redondear a dos decimales
    desayuno = [round(0.25 * x, 2) for x in vectorDia]
    colacion = [round(0.15 * x, 2) for x in vectorDia]
    comida = [round(0.40 * x, 2) for x in vectorDia]
    cena = [round(0.20 * x, 2) for x in vectorDia]
    
    return desayuno, colacion, comida, cena




def make_meal(user):
    # Call the genetic algorithm function here
    best_desayuno = []
    best_colacion = []
    best_comida = []
    best_cena = []

    goal=Goal.objects.get(user=user)
    # Retrieve the indexes of the best foods from the algorithm
    # Pass the necessary parameters to the function
    # Retrieve the indexes of the best foods from the algorithm
    desayuno = genetic([goal.daily_calories, goal.fat_percentage, goal.carbohydrate_percentage, goal.protein_percentage], 3, 1000, 0.8, 0.4, 100)
    #for i in desayuno:
    best_desayuno.append(Food.objects.filter(index__in=desayuno).values_list('name', flat=True))
    
    colacion = genetic([goal.daily_calories, goal.fat_percentage, goal.carbohydrate_percentage, goal.protein_percentage], 4, 1000, 0.8, 0.4, 100)
    #for i in colacion:
    best_colacion.append(Food.objects.filter(index__in=colacion).values_list('name', flat=True))
    
    comida = genetic([goal.daily_calories, goal.fat_percentage, goal.carbohydrate_percentage, goal.protein_percentage], 2, 1000, 0.8, 0.4, 100)
    #for i in comida:
    best_comida.append(Food.objects.filter(index__in=comida).values_list('name', flat=True))
    
    cena = genetic([goal.daily_calories, goal.fat_percentage, goal.carbohydrate_percentage, goal.protein_percentage], 3, 1000, 0.8, 0.4, 100)
    #for i in cena:
    best_cena.append(Food.objects.filter(index__in=cena).values_list('name', flat=True))

    return best_desayuno, best_colacion, best_comida, best_cena



def actualizarmeta(user):
    goal = Goal.objects.get(user=user)
    user_profile = user.userprofile

    # Obtener los datos del perfil del usuario
    objetivo = user_profile.objetivo

    daily_calories = 10 * user_profile.kg + 6.25 * user_profile.cm - 5 * user_profile.edad + 5
    # Calcular las calorías quemadas
    if objetivo == "Subir":
        if user_profile.fa == 1.2:
            goal.daily_calories =  daily_calories * 1.2  + 500
        elif user_profile.fa == 1.375:
            goal.daily_calories = daily_calories * 1.375 + 500
        elif user_profile.fa == 1.55:
            goal.daily_calories = daily_calories * 1.55 + 500
        elif user_profile.fa == 1.725:
            goal.daily_calories = daily_calories * 1.725 + 500
        elif user_profile.fa == 1.9:
            goal.daily_calories = daily_calories * 1.9 + 500
        goal.protein_percentage = user_profile.kg * random.uniform(1.2, 2.2)
        goal.fat_percentage = goal.daily_calories * random.uniform(0.2, 0.35)
        goal.carbohydrate_percentage = random.uniform(45, 65)
    elif objetivo == "Bajar":
        if user_profile.fa == 1.2:
            goal.daily_calories = daily_calories * 1.2- 500
        elif user_profile.fa == 1.375:
            goal.daily_calories = daily_calories * 1.375- 500
        elif user_profile.fa == 1.55:
            goal.daily_calories = daily_calories * 1.55- 500
        elif user_profile.fa == 1.725:
            goal.daily_calories = daily_calories * 1.725- 500
        elif user_profile.fa == 1.9:
            goal.daily_calories = daily_calories * 1.9  - 500
        goal.protein_percentage = user_profile.kg * random.uniform(1.2, 2.2)
        goal.fat_percentage = goal.daily_calories * random.uniform(0.2, 0.35)
        goal.carbohydrate_percentage = random.uniform(45, 65)                  

    goal.save()

