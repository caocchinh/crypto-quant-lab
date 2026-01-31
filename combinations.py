from itertools import combinations

param_names = ["fast", "slow", "signal", "ema_length"]
print(len(list(combinations(param_names,))))
