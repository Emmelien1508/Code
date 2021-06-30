from math import exp, sqrt
from random import choice, uniform, random
from copy import deepcopy

class ACO():
    def __init__(self, city, nn_value):
        self.algorithm_name = 'aco'
        self.nr_of_scenarios = city.nr_of_scenarios
        self.scenarios = city.scenarios
        self.scooters = city.scooters
        self.nn_value = nn_value
        self.scenario_size = city.scenario_size

        self.tsp_length = 0
        self.scenarios_in_the_tour = {}
        self.length_of_scenarios = {}

        self.ant_count = 10
        self.q0 = 0.98
        self.rho = 0.1
        self.beta = 2
        self.alpha = 0.1
        self.t0 = 1 / (len(self.scooters) * self.nn_value)

        self.reset_scooters()
        self.initialize_distances()
        self.initialize_pheromone()
        self.run()

    def run(self):
        time = 0
        
        best_cost = float('inf')
        best_tour = []
        while time <= len(self.scooters):
            print(f"the time is now {time}")
            for k in range(self.ant_count):
                tour = []
                self.reset_scooters()
                current_point = choice(self.scooters)
                tour.append(current_point)
                current_point.visited = True

                for _ in range(len(self.scooters) - 1):
                    current_point = tour[-1]
                    current_point.visited = True
                    X = uniform(0, 1)
                    unvisited_scooters = [scooter for scooter in self.scooters if scooter not in tour]

                    if X <= self.q0:
                        next_scooter = self.add_scooter(current_point, unvisited_scooters)
                    else:
                        next_scooter = self.choose_scooter_with_probability(current_point, unvisited_scooters)

                    tour.append(next_scooter)
                    self.update_pheromone()

                cost = self.calculate_stsp_length(tour)
                if cost < best_cost:
                    best_tour = deepcopy(tour)
                    best_cost = cost

            self.update_pheromone_trail(best_cost)
            time += 1
        
        self.tour = best_tour
        self.stsp_length = best_cost
        self.calculate_tsp_length()

    def calculate_tsp_length(self):
        """
        Calculates the total length of the TSP tour.
        """
        for i in range(len(self.tour)):
            scooter1, scooter2 = self.get_two_scooters(self.tour, i)
            self.tsp_length += self.get_distance(scooter1, scooter2)  

    def update_pheromone_trail(self, best_cost):
        """
        Updates pheromone levels after all ants choose a tour.
        """
        for i, row in enumerate(self.pheromone):
            for j, col in enumerate(row):
                self.pheromone[i][j] *= (1 - self.alpha)
                self.pheromone[i][j] += self.rho * (1 / best_cost)

    def get_two_scooters(self, tour, i):
        """
        Returns 2 scooters given an index in a tour.
        """
        scooter1 = tour[i]
        
        if i < len(tour) - 1:
            scooter2 = tour[i + 1]
        else:
            scooter2 = tour[0]
        
        return scooter1, scooter2

    def calculate_stsp_length(self, tour):
        """
        Calculates the total length of the sTSP tour.
        """
        stsp_length = 0
        self.sort_scenarios(tour)

        for nr, subtour in self.scenarios_in_the_tour.items():
            print(f"we are now at scenario {nr}")
            self.length_of_scenarios[nr] = 0
            for i in range(len(subtour)):
                scooter1, scooter2 = self.get_two_scooters(subtour, i)
                self.length_of_scenarios[nr] += self.get_distance(scooter1, scooter2)

            stsp_length += (1/self.nr_of_scenarios) * self.length_of_scenarios[nr]

        return stsp_length

    def sort_scenarios(self, tour):
        """
        Sorts the scenarios in the order of the tour. 
        Creates a dictionary where the key is the number of the scenario
        and the value is a list of the scooters in the subtour (with a specific order).
        """
        for k in range(1, self.nr_of_scenarios + 1):
            self.scenarios_in_the_tour[k] = [scooter for scooter in tour if scooter in self.scenarios[k]]

    def reset_scooters(self):
        """
        Resets all cities to unvisited.
        """
        for scooter in self.scooters:
            scooter.visited = False
    
    def add_scooter(self, current_point, unvisited_scooters):
        """
        Adds scooter that maximizes tau_ij * eta_ij^beta.
        """
        scooters_and_pheromones = {}
        for scooter in unvisited_scooters:
            try:
                scooters_and_pheromones[scooter] = self.pheromone[current_point.number][scooter.number] * ((1 / self.distances[current_point.number][scooter.number])**self.beta)
            except:
                scooters_and_pheromones[scooter] = 0

        return max(scooters_and_pheromones, key=scooters_and_pheromones.get)

    def choose_scooter_with_probability(self, current_point, unvisited_scooters):
        """
        Chooses scooter j with a certain probability.
        """
        scooters_and_probabilities = {}
        denominator = 0
        for scooter in unvisited_scooters:
            try:
                denominator += self.pheromone[current_point.number][scooter.number] * ((1 / self.distances[current_point.number][scooter.number])**self.beta)
            except:
                pass
        
        for scooter in unvisited_scooters:
            try:
                numerator = self.pheromone[current_point.number][scooter.number] * ((1 / self.distances[current_point.number][scooter.number])**self.beta)
            except:
                numerator = 0.0
            scooters_and_probabilities[scooter] = numerator / denominator

        rand = random()
        for i, scooter in enumerate(scooters_and_probabilities.keys()):
            rand -= scooters_and_probabilities[scooter]
            if rand <= 0:
                selected = scooter
                break

        return selected

    def get_distance(self, scooter1, scooter2):
        """
        Returns the Euclidian distance between two cities
        """
        return sqrt((scooter1.x - scooter2.x)**2 + (scooter1.y - scooter2.y)**2)  

    def initialize_distances(self):
        """
        Initializes the distance matrix, used for eta.
        """
        self.distances = []
        for i, scooter1 in enumerate(self.scooters):
            self.distances.append([])
            for j, scooter2 in enumerate(self.scooters):
                self.distances[i].append(self.get_distance(scooter1, scooter2))

    def initialize_pheromone(self):
        """
        Initializes the pheromone levels in the ant colony.
        """
        self.pheromone = []
        for i in range(len(self.scooters)):
            self.pheromone.append([])
            for j in range(len(self.scooters)):
                self.pheromone[i].append(1 / ( len(self.scooters) * len(self.scooters)))

    def update_pheromone(self):
        """
        Updates pheromone levels after choosing an edge.
        """
        for i, row in enumerate(self.pheromone):
            for j, col in enumerate(row):
                self.pheromone[i][j] *= (1 - self.rho)
                self.pheromone[i][j] += self.rho * self.t0