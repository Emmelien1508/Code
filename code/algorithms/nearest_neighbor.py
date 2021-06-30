from math import sqrt
from random import choice

class NN():
    """
    Make the tour go from a city to its nearest neighbor. Repeat.
    """
    def __init__(self, city):
        self.algorithm_name = 'nn'
        self.scooters = city.scooters
        self.scenarios = city.scenarios
        self.nr_of_scenarios = city.nr_of_scenarios
        self.scenario_size = city.scenario_size
        
        self.reset()
        self.run()

    def run(self):
        """
        Start the tour at the first city; at each step extend the tour 
        by moving from the previous city to its nearest neighbor 
        that has not yet been visited.
        """
        start = choice(self.scooters)
        start.visited = True
        self.tour.append(start)
        unvisited_scooters = [scooter for scooter in self.scooters if scooter.visited == False]
        while unvisited_scooters:
            closest_scooter = self.nearest_neighbor(self.tour[-1], unvisited_scooters)
            self.tour.append(closest_scooter)
            unvisited_scooters.remove(closest_scooter)
        
        self.calculate_tsp_length()
        self.calculate_stsp_length()

    def get_distance(self, scooter1, scooter2):
        """
        Returns the Euclidian distance between two scooters
        """
        return sqrt((scooter1.x - scooter2.x)**2 + (scooter1.y - scooter2.y)**2)

    def nearest_neighbor(self, scooter1, scooters):
        """
        Find the scooter in all scooters that is nearest to scooter1.
        """
        return min(scooters, key=lambda c: self.get_distance(c, scooter1))

    def calculate_tsp_length(self):
        """
        Calculates the total length of the TSP tour.
        """
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
        Creates a dictionary where the key is the number of the scenario
        and the value is a list of the scooters in the subtour (with a specific order).
        """
        for k in range(1, self.nr_of_scenarios + 1):
            self.scenarios_in_the_tour[k] = [scooter for scooter in self.tour if scooter in self.scenarios[k]]

    def reset(self):
        """
        Resets all values of attributes and scooter objects.
        """
        self.tour = []
        self.tsp_length = 0
        self.stsp_length = 0
        self.length_of_scenarios = {}
        self.scenarios_in_the_tour = {}

        for scooter in self.scooters:
            scooter.visited = False

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