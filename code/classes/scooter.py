class Scooter():
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y
        self.visited = False

    def __str__(self):
        return f'{self.number}'