import random
from itertools import combinations
import time

myList = random.sample(range(0, 3000001), 3000000)
threshold = 30

start = time.perf_counter()


def twoSum1(nums: list[int], target: int) -> list[int]:
    d = {}
    for i, j in enumerate(nums):
        r = target - j
        if r in d: return [d[r], i]
        d[j] = i


end = time.perf_counter()
print(twoSum1(myList, threshold))
print(f'{start - end:.10f}')

