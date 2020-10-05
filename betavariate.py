import time
import random
import pandas as pd

random.seed()

dict_df = dict()
lymbd = 0.4
while lymbd <= 3:
    dict_df[str(lymbd)] = dict()
    for i in range(100):
        b = int(random.expovariate(lymbd))
        try:
            dict_df[str(lymbd)][b] += 1
        except KeyError:
            dict_df[str(lymbd)][b] = 1
    lymbd += 0.3
df = pd.DataFrame(dict_df).sort_index()


print(df)

