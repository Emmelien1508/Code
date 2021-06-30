from random import uniform
import numpy as np
import pandas as pd

data = {'SA100': []}
mean = 178.3775290
std = 8.030196788

s = np.random.normal(mean, std, 80)
for item in s:
    data['SA100'].append(item)

df = pd.DataFrame.from_dict(data)
df.to_excel(f'SA_100_fake_values.xlsx', index=False)