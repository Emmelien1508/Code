from random import uniform, seed

import pandas as pd

def create_csv_file(n):
    seed(3)
    number, x, y = [], [], []
    half = int(round(n/2, 0))

    for i in range(half):
        number.append(i)
        xcor = (round(6.2 + uniform(-3.5, 3.5), 1))
        ycor = (round(6 + uniform(-3.5, 3.5), 1))

        while xcor > 5.5 and ycor > 7:
            xcor = (round(6.2 + uniform(-3.5, 3.5), 1))
            ycor = (round(6 + uniform(-3.5, 3.5), 1))

        x.append(xcor)
        y.append(ycor)

    for i in range(half, n):
        number.append(i)
        xcor = (round(5.5 + uniform(-5.3, 5.3), 1))
        ycor = (round(5.5 + uniform(-5.3, 5.3), 1))

        while xcor > 5.5 and ycor > 7:  
            xcor = (round(5.5 + uniform(-5.3, 5.3), 1))
            ycor = (round(5.5 + uniform(-5.3, 5.3), 1))

        x.append(xcor)
        y.append(ycor)

    data = {'scooter number': number, 'x coordinates': x, 'y coordinates': y}
    df = pd.DataFrame(data)
    df.to_csv(f"{n}_scooters.csv", index = False, header = False)

if __name__ == "__main__":
    create_csv_file(5)