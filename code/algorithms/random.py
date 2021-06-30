from random import shuffle
from math import sqrt
from itertools import zip_longest

class Random():

    def __init__(self, city):
        self.algorithm_name = 'random'
        self.scooters = city.scooters
        self.scenarios = city.scenarios
        self.nr_of_scenarios = city.nr_of_scenarios
        self.scenario_size = city.scenario_size
        self.tsp_length = 0
        self.stsp_length = 0

        self.length_of_scenarios = {}
        self.scenarios_in_the_tour = {}

        self.run()

    def run(self):
        """
        Randomly creates a tour and computes the length of the TSP and sTSP tour.
        """
        shuffle(self.scooters)
        self.tour = [scooter for scooter in self.scooters]
        self.calculate_stsp_length()
        self.calculate_tsp_length()

    def calculate_tsp_length(self):
        """
        Calculates the total length of the TSP tour.
        """
        self.tsp_length = 0

        for i in range(len(self.tour)):
            scooter1, scooter2 = self.get_two_scooters(self.tour, i)
            self.tsp_length += self.get_distance(scooter1, scooter2)

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
            self.stsp_length += (1/self.nr_of_scenarios) * self.length_of_scenarios[nr]

    def sort_scenarios(self):
        """
        Sorts the scenarios in the order of the tour.
        """
        for k in range(1, self.nr_of_scenarios + 1):
            self.scenarios_in_the_tour[k] = [scooter for scooter in self.tour if scooter in self.scenarios[k]]

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

