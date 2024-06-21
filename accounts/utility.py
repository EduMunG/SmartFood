import pandas as pd 
import math
from .models import Food

def get_Vector(index):
    if index == 1813:
        print(f"Detenido en el índice: {index}")
        return [254.28, 42.85, 6.66, 5.71]
    
    try:
        food = Food.objects.get(index=index)
        # print(f'{food.energ_kal}, {food.lipid_tot}, {food.carbohydrt}, {food.proteina}')
        return [food.energ_kal, food.lipid_tot, food.carbohydrt, food.proteina]
    except Food.DoesNotExist:
        print(f"No se encontró ningún Food con el índice: {index}")
        return [254.28, 42.85, 6.66, 5.71]


'''
def t(individual):
    meals = []
    for i in range(len(individual)):
        index_db = individual[i]
        meals.append(get_Vector(index_db))
    vector = [0 for _ in meals[0]] # Initialize a vector of zeros
    for m in meals:
        for j in range(len(m)):
            vector[j] += m[j]
    return vector 

def objective_Function(objectiveVector, individual):
    return math.sqrt(sum((ov - iv) ** 2 for ov, iv in zip(objectiveVector, individual)))


indiviudal = t([1639, 1368, 1460, 479])

print(objective_Function([463, 56, 15, 22], indiviudal))
'''
