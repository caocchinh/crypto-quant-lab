from itertools import  combinations
import pandas_ta
import talib
import sys
import numpy as np

# all = []
# for i in talib.get_functions():
#     all.append(i)
# for i in pandas_ta.ALL_PATTERNS:
#     all.append(i)

bruh = list(combinations(np.array(talib.get_functions()),3))
print(bruh[0])
# for a,b,c in combination(all,3):
#     count+=1
# for a,b,c,d in combinations(all,4):
#     count+=1
# # for a,b,c,d,e in combinations(all,5):
#     count+=1
