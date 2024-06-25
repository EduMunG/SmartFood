from .utility import get_Vector
import random
import math


### Transform the individual into a list of vectors ###
def t(individual):
    meals = [get_Vector(index_db) for index_db in individual]
    vector = [sum(meal) for meal in zip(*meals)]
    return vector 


### Euclidean distance between the objective vector and the best vector ###
def objective_Function(objectiveVector, individual):
    return math.sqrt(sum((ov - iv) ** 2 for ov, iv in zip(objectiveVector, individual)))


### Initialize population ###
def initialize_Population(tamPopulation, num_meals, objectiveVector):
    population = []
    for _ in range(tamPopulation):
        individual = [random.randint(1, 1463) for _ in range(num_meals)]
        vector = t(individual)
        fitness = objective_Function(objectiveVector, vector)
        population.append([individual, fitness])
    return population


##### Selection method ##########
# Tournament selection
def tournament_selection(population, k=3):
    selected = []
    for _ in range(len(population)):
        aspirants = random.sample(population, k)
        selected.append(min(aspirants, key=lambda ind: ind[1]))
    return selected


### Crossover ###
def crossover(father1, father2, objectiveVector):
    n = len(father1)
    point1, point2 = sorted(random.sample(range(1, n), 2))
    son1 = father1[:point1] + father2[point1:point2] + father1[point2:]
    son2 = father2[:point1] + father1[point1:point2] + father2[point2:]
    return [son1, objective_Function(objectiveVector, t(son1))], [son2, objective_Function(objectiveVector, t(son2))]


### Generate sons ###
def recombination(population, probCrossover, objectiveVector):
    random.shuffle(population)
    sons = []
    for i in range(0, len(population) - 1, 2):
        if random.uniform(0, 1) < probCrossover:
            son1, son2 = crossover(population[i][0], population[i + 1][0], objectiveVector)
            sons.extend([son1, son2])
    return sons


### Mutation ###
def mutation(sons, probMutation):
    for son in sons:
        for i in range(len(son[0])):
            if random.uniform(0, 1) < probMutation:
                son[0][i] = random.randint(1, 1463)


### Elitism ###
def elitism(population, tamPopulation):
    return sorted(population, key=lambda x: x[1])[:tamPopulation]


### Genetic Algorithm ###
def genetic(objectiveVector, numMeals, tamPopulation, probCrossover, probMutation, generations):
    population = initialize_Population(tamPopulation, numMeals, objectiveVector)
    for g in range(generations):
        selected = tournament_selection(population)
        sons = recombination(selected, probCrossover, objectiveVector)
        mutation(sons, probMutation)
        population = elitism(population + sons, tamPopulation)
        print(f'Generation {g}: Best fitness: {population[0][1]}, Individual: {population[0][0]}')
        print('-----------')

    return population[0][0]

