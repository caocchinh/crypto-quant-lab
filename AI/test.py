import itertools
import time
from tqdm import tqdm
from itertools import combinations
import numpy as np
import math
# def bruh():
#     for i in tqdm(range(1, 12, 3)):
#         yield
#
# x = bruh()
# try:
#     next(x)
#     time.sleep(2)
#     next(x)
#     time.sleep(0.1)
#     next(x)
#     time.sleep(1)
#     next(x)
#     time.sleep(2)
#     next(x)
# except StopIteration:
#     pass


a =  np.arange(2, 50, step=10)
b = np.arange(2, 50, step=10)
c = np.arange(50, 100, step=10)
bruh =  len(list(itertools.product(a,b,c)))
print(true)
