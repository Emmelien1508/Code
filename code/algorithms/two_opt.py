from py2opt.routefinder import RouteFinder
from math import sqrt

class OPT():
  def __init__(self, algorithm):
    self.algorithm_name = '2opt'
    self.tour = algorithm.tour
    self.stsp_length = algorithm.stsp_length
    self.nr_of_scenarios = algorithm.nr_of_scenarios
    self.scenarios = algorithm.scenarios
    self.scooters = algorithm.scooters
    self.scenario_size = algorithm.scenario_size

    self.length_of_scenarios = {}
    self.scenarios_in_the_tour = {}
    self.stsp_length = 0
    
    self.initialize_distance_matrix()
    self.run()

  def run(self):
    for row, scooter1 in enumerate(self.scooters):
      for col, scooter2 in enumerate(self.scooters):
        self.distance_matrix[row][col] = self.get_distance(scooter1, scooter2)
    
    route_finder = RouteFinder(self.distance_matrix, self.scooters, iterations=15)
    best_distance, best_route = route_finder.solve()

    self.tour = best_route
    self.tsp_length = best_distance
    self.calculate_stsp_length()

  def initialize_distance_matrix(self):
    self.distance_matrix = []
    for row in range(len(self.scooters)):
      self.distance_matrix.append([])
      for col in range(len(self.scooters)):
        self.distance_matrix[row].append([])
                      
  def calculate_tsp_length(self, tour):
    tsp_length = 0
    for i in range(len(tour)):
      scooter1, scooter2 = self.get_two_scooters(tour, i)
      tsp_length += self.get_distance(scooter1, scooter2)    

    return tsp_length   
          
  def calculate_stsp_length(self):
    self.sort_scenarios(self.tour)

    for nr, subtour in self.scenarios_in_the_tour.items():
      self.length_of_scenarios[nr] = 0
      for i in range(len(subtour)):
        scooter1, scooter2 = self.get_two_scooters(subtour, i)
        self.length_of_scenarios[nr] += self.get_distance(scooter1, scooter2)

      self.stsp_length += (1/self.nr_of_scenarios) * self.length_of_scenarios[nr]

  def sort_scenarios(self, tour):
    for k in range(1, self.nr_of_scenarios + 1):
      self.scenarios_in_the_tour[k] = [scooter for scooter in tour if scooter in self.scenarios[k]]

  def get_distance(self, scooter1, scooter2): 
    return sqrt((scooter1.x - scooter2.x)**2 + (scooter1.y - scooter2.y)**2)

  def get_two_scooters(self, tour, i):
    scooter1 = tour[i]
    
    if i < len(tour) - 1:
      scooter2 = tour[i + 1]
    else:
      scooter2 = tour[0]
  
    return scooter1, scooter2