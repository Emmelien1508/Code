import pandas as pd

from time import time

from code.classes.city import City
from code.visualisation.visualise import Graph
from code.algorithms import random, nearest_neighbor, simulated_annealing, bruteforce, ant_colony, two_opt, lb, ilp

def randomm(scenario_size):
    city = City(number=350, scenario_size=scenario_size, nr_of_scenarios=100)
    algorithm1 = random.Random(city)
    # Graph(algorithm1)
    return algorithm1

def nnnn(scenario_size):
    city = City(number=350, scenario_size=scenario_size, nr_of_scenarios=100)
    algorithm1 = nearest_neighbor.NN(city)
    # print(f"The TSP tour is {round(algorithm1.tsp_length, 3)} km long.")
    # print(f"The sTSP tour is {round(algorithm1.stsp_length, 3)} km long.")
    # Graph(algorithm1)
    return algorithm1

def lowab(scenario_size):
    city = City(number=350, scenario_size=scenario_size, nr_of_scenarios=100)
    algorithm1 = lb.LowerBound(city)
    print(f"The lower bound of the sTSP is {round(algorithm1.stsp_length, 3)} km long.")

    return algorithm1.stsp_length

def main(scenario_size):
    print("In the city Amsterdam there are 20 e-scooters on the street.")
    print("Some of them need to be provided with a full battery at the end of the day.")
    print("What is the optimal route to charge these scooters?")
    print("Let's use algorithms to solve this optimization problem!")
    
    print()

    city = City(number=350, scenario_size=scenario_size, nr_of_scenarios=100)

    baseline = input("What baseline algorithm would you like to apply? Type 'r' for Random, 'nn' for Nearest Neighbor, and 'aco' for Ant Colony Optimization. ")
    while baseline.lower()[0] != 'r' and baseline.lower()[0] != 'n' and baseline.lower()[0] != 'a':
        baseline = input("What baseline algorithm would you like to apply? ")

    start1 = time()
    if 'r' in baseline:
        algorithm1 = random.Random(city)
    elif 'n' in baseline:
        algorithm1 = nearest_neighbor.NN(city)
    else:
        nn_obj = nearest_neighbor.NN(city)
        nn_value = nn_obj.stsp_length
        algorithm1 = ant_colony.ACO(city, nn_value)
    end1 = time()

    print(f"The baseline algorithm found a solution in {round(end1 - start1, 3)} seconds.")
    print(f"The TSP tour is {round(algorithm1.tsp_length, 3)} km long.")
    print(f"The sTSP tour is {round(algorithm1.stsp_length, 3)} km long.")

    Graph(algorithm1)

    print()

    print("Now we're going to improve this result!")
    improvement = input("Do you want to apply Simulated Annealing or 2-Opt? Type 'sa' for Simulated Annealing and '2' for 2-Opt. ")
    while improvement.lower()[0] != 's' and improvement.lower()[0] != '2':
        improvement = input("What improvement algorithm would you like to apply? ")
    
    start2 = time()
    if 'sa' in improvement:
        algorithm2 = simulated_annealing.SA(algorithm1)
    else:
        algorithm2 = two_opt.OPT(algorithm1)
    end2 = time()
    Graph(algorithm2)

    print()

    print(f"\nThe second algorithm found a solution in {round(end2 - start2, 3)} seconds.")
    print(f"The TSP tour is {round(algorithm2.tsp_length, 3)} km long.")
    print(f"The sTSP tour is {round(algorithm2.stsp_length, 3)} km long.")

def random_and_2opt(scenario_size):
    city = City(number=350, scenario_size=scenario_size, nr_of_scenarios=100)
    algorithm1 = random.Random(city)
    algorithm2= two_opt.OPT(algorithm1)
    Graph(algorithm2)

    return algorithm1, algorithm2

def nn_and_2opt(scenario_size):
    city = City(number=350, scenario_size=scenario_size, nr_of_scenarios=100)
    algorithm1 = nearest_neighbor.NN(city)
    algorithm2 = two_opt.OPT(algorithm1)
    Graph(algorithm1)
    Graph(algorithm2)

    return algorithm1, algorithm2

if __name__ == "__main__":
    # nrs = [25, 50, 75, 100]
    # for nr in nrs:
    nr = 50
    # data = {'2-Opt': []}
    # start = time()
    # for i in range(100):
    _, _ = nn_and_2opt(nr)
        # data['2-Opt'].append(opt.stsp_length)
    # end = time()
    # print(f"It was finished in {end - start} seconds")
    # df = pd.DataFrame.from_dict(data)
    # df.to_excel(f'2OPT+RANDOM_{nr}.xlsx', index=False)
