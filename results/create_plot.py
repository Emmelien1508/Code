import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_histogram(nr):
    algorithms = ['random', 'nn', 'aco', 'nn+2opt', 'random+2opt', 'sa']
    colors = ['#91f728', '#8a6fdf', '#f8860e', '#c23d81', '#f2d027', '#1e9b8a']
    # algorithms = ['nn', 'aco', 'nn+2opt', 'random+2opt', 'sa']
    # colors = ['#8a6fdf', '#f8860e', '#c23d81', '#f2d027', '#1e9b8a']
    fig = plt.figure()
    for (i, algorithm), color in zip(enumerate(algorithms), colors):
        df = pd.read_excel(f'{algorithm}/output.xlsx', sheet_name=f'scenario size {nr}')
        df = df[df.filter(regex='^(?!Unnamed)').columns]
        df = df.astype(float)
        names = list(df.columns)
        if i == 0:
            ax = df.hist(color=color, alpha=0.7, label=names[0])
        else:
            df.hist(ax=ax, color=color, alpha=0.7, label=names[0])

    plt.legend(ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1.2))
    
    plt.grid(False) 
    plt.yticks([])  
    plt.title("")
    # plt.savefig(f'Histogram_without_random_{nr}.png', bbox_inches="tight")
    plt.savefig(f'Histogram_{nr}.png', bbox_inches="tight")
    plt.close()

def annealing_schedule():
    x = np.array(range(2500)) 
    y = 30 * ((1 - 0.005)**x)
    plt.plot(x, y, color = '#f2d027', label='Temperature', linewidth=4, alpha=0.7)
    a = [0.001 for i in range(2500)]
    plt.plot(x, a, color = '#c23d81', label='Bound', alpha=0.7)
    leg = plt.legend()
    plt.savefig(f'annealing schedule.png', bbox_inches="tight")

if __name__ == "__main__":
    nrs = [25, 50, 75, 100]
    # nrs = [100]
    for nr in nrs:
    # annealing_schedule()
    # show_map_of_ams()
        create_histogram(nr)