# Graeson Brickner
# U1 Lab 1
# Biggest rat project

from rat import Rat
from random import random, triangular, uniform
from copy import deepcopy
from math import ceil
import time

population = [[], []]

GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what

def initial_population():
    '''Create the initial set of rats based on constants'''
    rats = [[],[]]
    mother = Rat("F", INITIAL_MIN_WT)
    father = Rat("M", INITIAL_MAX_WT)

    for r in range(NUM_RATS):
        if r < 10:
            sex = "M"
            ind = 0
        else:
            sex = "F"
            ind = 1

        wt = calculate_weight(sex, mother, father)
        R = Rat(sex, wt)
        rats[ind].append(R)

    return rats

def calculate_weight(sex, mother, father):
    '''Generate the weight of a single rat'''

    if mother.getWeight() > father.getWeight():
        max, min = mother.getWeight(), father.getWeight()

    else:
        min, max = mother.getWeight(), father.getWeight()

    # Use the triangular function from the random library to skew the 
    #baby's weight based on its sex

    if sex == "M":
        wt = int(triangular(min, max, max))
    else:
        wt = int(triangular(min, max, min))

    return wt

def mutate(pups):
    """Check for mutability, modify weight of affected pups"""

    for sex in pups:
        for rat in sex:
            if random() < MUTATE_ODDS:
                rat.setWeight(ceil(rat.getWeight() * uniform(MUTATE_MIN, MUTATE_MAX)))

    return pups  

def breed(rats):
    """Create mating pairs, create LITTER_SIZE children per pair"""
    children = [[], []]

    males, females = rats[0], rats[1]

    if len(males) > len(females):
        iterations = len(males)

    else:
        iterations = len(females)

    for i in range(iterations):
        females[i].incrementLitters()
        males[i].incrementLitters()

        for x in range(LITTER_SIZE):
            if random() < .5:
                children[0].append(Rat('M', calculate_weight('M', females[i], males[i])))

            else:
                children[1].append(Rat('F', calculate_weight('F', females[i], males[i])))

    return children  

def select(rats, pups):
    '''Choose the largest viable rats for the next round of breeding'''
    largest = "bruh"
    smallest = "pluh"

    rats[0] = deepcopy(rats[0]) + deepcopy(pups[0])
    rats[1] = deepcopy(rats[1]) + deepcopy(pups[1])

    rats[0].sort(key=lambda x: x.getWeight(), reverse=True)
    rats[1].sort(key=lambda x: x.getWeight(), reverse=True)
    
    males, females = [], []

    for rat in rats[0]:
        if len(males) < 10 and rat.canBreed():
            males.append(rat)
    
    for rat in rats[1]:
        if len(females) < 10 and rat.canBreed():
            females.append(rat)
    
    rats[0], rats[1] = males, females

    if males[0] > females[0]:
        largest = males[0]

    else:
        largest = females[0]

    if males[-1] < females[-1]:
        smallest = males[-1]

    else:
        smallest = females[-1]

    return rats, largest, smallest

def calculate_mean(rats):
    '''Calculate the mean weight of a population'''
    sumWt = 0
    numRats = 0

    for sex in rats:
        for rat in sex:
            sumWt += rat.getWeight()
            numRats += 1

    return sumWt // numRats

def fitness(rats):
    """Determine if the target average matches the current population's average"""
    mean = calculate_mean(rats)

    return mean >= GOAL, mean

def get_var_name(var):
    for name, value in locals().items():
        if value is var:
            return name

def toTextFile(mean, largest, smallest):
    lists = [[mean, 'mean.txt'], [largest, 'largest.txt'], [smallest, 'smallest.txt']]
    for l in lists:
        with open(f'{l[1]}', 'w') as file:
            toWrite = ""
            for i in l[0]:
                toWrite = toWrite + str(i) + ", "

            file.write(toWrite)

def main():
    start = time.time()
    completed = False
    totalIterations = 0
    allMeans = []
    allLargest = []
    allSmallest = []
    mean = 0
    largest = 0
    population = initial_population()
    while totalIterations < GENERATION_LIMIT and mean < GOAL:
        totalIterations += 1
        babies = breed(population)
        babies = mutate(babies)

        population, newLargest, smallest = select(population, babies)
        newLargest = newLargest.getWeight()
        if newLargest > largest:
            largest = newLargest

        completed, mean = fitness(population)
        allMeans.append(mean)
        allLargest.append(newLargest)
        allSmallest.append(smallest.getWeight())
    
    end = time.time()

    toTextFile(allMeans, allLargest, allSmallest)
    
    print(f"Report!\nTime to Run: {end-start}\nGenerations: {totalIterations}\nYears: {round(totalIterations/GENERATIONS_PER_YEAR)}\nLargest: {largest}")

    for i, x in enumerate(allMeans):
        if i % 10 == 0:
            print()

        print(str(x).rjust(9), end="")

if __name__ == "__main__":
    main()