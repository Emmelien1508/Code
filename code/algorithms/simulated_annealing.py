from math import exp, sqrt
from random import random, randint

class SA():
    def __init__(self, algorithm):
        self.algorithm_name = 'sa'
        self.tour = algorithm.tour
        self.tsp_length = algorithm.tsp_length
        self.nr_of_scenarios = algorithm.nr_of_scenarios
        self.scenarios = algorithm.scenarios
        self.scooters = algorithm.scooters
        self.scenario_size = algorithm.scenario_size

        self.stsp_length = 0
        self.all_tours = {}
        self.length_of_scenarios = {}
        self.scenarios_in_the_tour = {}

        self.run()

    def run(self):
        """
        Given a cooling rate and start temperature, 
        the simulated annealing algorithm finds a (global) minimum.
        With each temperature, the simulated annealing heuristic 
        considers a random new state and probabilistically decides 
        whether or not to accept this new state.
        """
        cr = 0.005
        start_temp = 30
        k_max = len(self.scooters)
        current_temp = start_temp
        current_E = self.tsp_length

        i = 0
        while current_temp > 0.001:
            if i % 100 == 0:
                print(f"Iteration {i} with solution {current_E}")

            current_temp = start_temp * (1 - cr)**i

            for k in range(k_max):

                scooter1, scooter2, idx1, idx2 = self.get_random_scooters()
                self.swap(scooter1, scooter2, idx1, idx2)
                new_E = self.calculate_tsp_length()

                if self.acceptance_prob(current_E, new_E, current_temp) >= random():
                    current_E = new_E
                else:
                    self.swap(scooter2, scooter1, idx1, idx2)
                
                self.tsp_length = current_E

            i += 1

        self.calculate_stsp_length()

    def calculate_tsp_length(self):
        """
        Calculates the total length of the TSP tour.
        """
        tsp_length = 0
        for i in range(len(self.tour)):
            scooter1, scooter2 = self.get_two_scooters(self.tour, i)
            tsp_length += self.get_distance(scooter1, scooter2)
        
        return tsp_length

    def get_random_scooters(self):
        """
        Randomly gets two scooters from tour.
        """
        idx1 = randint(0, len(self.tour) - 1)
        idx2 = randint(0, len(self.tour) - 1)

        scooter1 = self.tour[idx1]
        scooter2 = self.tour[idx2]

        return scooter1, scooter2, idx1, idx2

    def swap(self, scooter1, scooter2, idx1, idx2):
        self.tour[idx1] = scooter2
        self.tour[idx2] = scooter1
    
    def sort_scenarios(self):
        """
        Sorts the scenarios in the order of the tour. 
        """
        for k in range(1, self.nr_of_scenarios + 1):
            self.scenarios_in_the_tour[k] = [scooter for scooter in self.tour if scooter in self.scenarios[k]]

    def calculate_stsp_length(self):
        """
        Calculates the total length of the sTSP tour.
        """    
        self.sort_scenarios()

        for nr, subtour in self.scenarios_in_the_tour.items():
            self.length_of_scenarios[nr] = 0
            for i in range(len(subtour)):
                scooter1, scooter2 = self.get_two_scooters(subtour, i)
                self.length_of_scenarios[nr] += self.get_distance(scooter1, scooter2)

        self.stsp_length = (1/self.nr_of_scenarios) * sum(self.length_of_scenarios.values())
    
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
    
    def get_distance(self, scooter1, scooter2): 
        """
        Returns the Euclidian distance between two scooters
        """
        return sqrt((scooter1.x - scooter2.x)**2 + (scooter1.y - scooter2.y)**2)
    
    def acceptance_prob(self, current_E, new_E, temp):
        """
        Returns the probability of making the transition from the current state to the new state.
        """
        if new_E < current_E:
            return 1.0
        return exp((current_E - new_E) / temp)