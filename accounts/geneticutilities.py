import pandas as pd
from .models import Food
import math

def get_Vector(index):
    food = Food.objects.get(index=index)
    return [food.energ_kal, food.lipid_tot, food.carbohydrt, food.proteina]
    #df = pd.read_csv('data_base.csv')
    #return list(df.iloc[index][2:-1].values)

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
