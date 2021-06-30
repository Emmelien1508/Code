from itertools import permutations
from math import sqrt

class LowerBound():
    def __init__(self, city):
        self.algorithm_name = 'lb'
        self.scooters = city.scooters
        self.scenarios = city.scenarios
        self.nr_of_scenarios = city.nr_of_scenarios
        self.all_tours = {}
        self.scenario_size = city.scenario_size
    
        self.all_tsp_values = {}

        self.run2()
    
    def run1(self):
        """
        Calculates the lower bound of the sTSP tour.
        This is done by finding the optimal TSP tour per scenario.
        """
        for nr, scenario in self.scenarios.items():
            print(f"We are in scenario {nr}")
            possible_tours = list(permutations(scenario, len(scenario)))
            for tour in possible_tours:
                tsp_value = self.compute_tsp(tour)
                self.all_tsp_values[tour] = tsp_value
            min_tsp = min(self.all_tsp_values, key=self.all_tsp_values.get)
            self.stsp_length += (1/self.nr) * self.all_tsp_values[min_tsp]

    def run2(self):
        """
        Calculates the lower bound of the sTSP tour.
        This is done by finding the optimal sTSP tour per 2 scenarios.
        """
        pairs = {}
        for i in range(1, int(self.nr_of_scenarios) + 1, 2):
            pairs[i] = [self.scenarios[i], self.scenarios[i+1]]

        possible_tours = list(permutations(self.scooters, len(self.scooters)))
        optimal_stsp_length = 0
        for nr, pair in pairs.items():
            self.all_tours = {}
            for possible_tour in possible_tours:
                self.sort_scenarios(list(possible_tour), pair, nr)
                stsp_length = 0
                for subtour in pair:
                    distance = 0
                    for i in range(len(subtour)):
                        scooter1, scooter2 = self.get_two_scooters(subtour, i)
                        distance += self.get_distance(scooter1, scooter2)

                    stsp_length += (1/self.nr_of_scenarios) * distance
            
                self.all_tours[possible_tour] = stsp_length

            self.tour = min(self.all_tours, key=self.all_tours.get)
            optimal_stsp_length += (1/self.nr_of_scenarios) * self.all_tours[self.tour]

    def sort_scenarios(self, tour, subset, nr):
        """
        Sorts the scenarios in the order of the tour.
        """
        s1 = [scooter for scooter in tour if scooter in subset[0]]
        s2 = [scooter for scooter in tour if scooter in subset[1]]
        pairs[nr] = [s1, s2]

    def get_distance(self, scooter1, scooter2):
        """
        Returns the Euclidian distance between two scooters
        """
        return sqrt((scooter1.x - scooter2.x)**2 + (scooter1.y - scooter2.y)**2)

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