from .scooter import Scooter

from random import seed, sample

class City():
    def __init__(self, number, scenario_size, nr_of_scenarios):
        self.city_name = 'Amsterdam'
        self.number = number
        self.scenario_size = scenario_size
        self.nr_of_scenarios = nr_of_scenarios
        self.scooters = []
        self.load_scooters()
        self.load_scenarios()

    def load_scooters(self):
        """
        Reads the scooters csv file and creates Scooter ojbects in the process.
        """
        with open(f'data/{self.number}_scooters.csv', 'r') as file:
            data = file.readlines()
            for i, row in enumerate(data):
                row = row.replace('\n', '').split(',')
                number = int(row[0])
                x = float(row[1])
                y = float(row[2])
                self.scooters.append(Scooter(number, x, y))

    def load_scenarios(self):
        """
        Creates a dictionary called scenarios where the key is the number of 
        the scenario and the value the scooters that are active in the scenario.
        """
        # seed(1)
        chosen_scenarios = []
        for j in range(self.nr_of_scenarios):
            chosen = sample(self.scooters, self.scenario_size)
            chosen_scenarios.append(chosen)
        self.scenarios = {i + 1: list(combs) for i, combs in enumerate(chosen_scenarios)}

    def __str__(self):
        return f"{self.city_name}"