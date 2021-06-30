import matplotlib.pyplot as plt 

from math import sqrt

class Graph():
    def __init__(self, algorithm):
        self.name = algorithm.algorithm_name.lower()
        self.tour = algorithm.tour
        self.tsp_length = algorithm.tsp_length
        self.stsp_length = algorithm.stsp_length
        self.scooters = algorithm.scooters 
        self.scenarios_in_the_tour = algorithm.scenarios_in_the_tour
        self.nr_of_scenarios = algorithm.nr_of_scenarios
        self.scenario_size = algorithm.scenario_size

        self.show_stsp()
        # self.show_scenarios()   

    def load_grid(self):
        fig, ax = plt.subplots()
        img = plt.imread("code/visualisation/Map.jpeg")
        ax.imshow(img, extent=[0, 11, 0, 11])

        plt.tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)
        # ax.set(xlim=(0, 11), ylim = (0, 11))

        # c1 = plt.Circle((6.2, 6), 3.5, color='#8a6fdf', alpha=0.15)
        # c2 = plt.Circle((-0.4, 5.7), 3.2, color='#f2d027', alpha=0.1) #west
        # c3 = plt.Circle((10.3, 3.5), 3.5, color='#f8860e', alpha=0.1) #oost
        # c4 = plt.Circle((3.9, -0.5), 3.8, color='#c23d81', alpha=0.1) #zuid
        # c5 = plt.Circle((8.3, 11), 2.4, color='#1e9b8a', alpha=0.1) #noord
        # ax.add_artist(c1)
        # ax.add_artist(c2)
        # ax.add_artist(c3)
        # ax.add_artist(c4)
        # ax.add_artist(c5)
        # ax.set_aspect(1)

        for scooter in self.scooters:
            plt.scatter(scooter.x, scooter.y, c='#c23d81', marker='.')

    def show_stsp(self):
        self.load_grid()

        self.iterate_over_tour(tour = self.tour, scenarios = False)
        
        plt.savefig(f'figures/{self.name}/{self.nr_of_scenarios} scenarios with size {self.scenario_size}/sTSP tour {round(self.stsp_length, 3)} km.png', bbox_inches="tight")

        plt.close()

    def show_scenarios(self):
        for nr, subtour in self.scenarios_in_the_tour.items():
            self.load_grid()

            self.iterate_over_tour(tour = subtour, scenarios = True, nr = nr)
        
            plt.savefig(f'figures/{self.name}/scenarios/Scenario {nr}.png')

            plt.close()

    def get_distance(self, scooter1, scooter2):
        """
        Returns the Euclidian distance between two scooters
        """
        return sqrt((scooter1.x - scooter2.x)**2 + (scooter1.y - scooter2.y)**2)

    def plot_values(self, scooter1, scooter2):
        x_values = [scooter1.x, scooter2.x]
        y_values = [scooter1.y, scooter2.y]
        plt.plot(x_values, y_values, c='#c23d81')

    def iterate_over_tour(self, tour, scenarios, nr=None):
        self.length_of_scenario = {}
        if scenarios:
            self.length_of_scenario[nr] = 0

        for i in range(len(tour)):
            scooter1 = tour[i]
            
            if i < len(tour) - 1:
                scooter2 = tour[i + 1]
            else:
                scooter2 = tour[0]
            
            if scenarios:
                self.length_of_scenario[nr] += self.get_distance(scooter1, scooter2)

            self.plot_values(scooter1, scooter2)
        