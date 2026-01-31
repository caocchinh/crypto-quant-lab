from matplotlib import pyplot as plt
# import numpy as np
# import pandas as pd
# plt.style.use("fivethirtyeight")
#
#
# dev_x = range(25, 36)
#
# x_indexes = np.arange(len(dev_x))
# width = 0.25
#
# dev_y = [38496, 42000, 46762, 49420, 53200
#     , 56000, 62316, 64928, 67317, 68748, 73752]
#
# python_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]
#
# js_dev_y = [37810, 43515, 46823, 49293, 53437,
#             56373, 62375, 66674, 68745, 68746, 74583]
#
# plt.bar(x_indexes-width, python_dev_y, color="b", label="Python",linewidth=2,width=width)
# plt.bar(x_indexes, js_dev_y, color="y", label="Javascript",width=width)
# plt.bar(x_indexes+width, dev_y, color="k", linestyle="--", label="All devs",width=width)
#
# plt.xticks(ticks=x_indexes,labels=dev_x)
#
# plt.legend()
# plt.ylabel("Age")
# plt.title("Ayo")
# plt.xlabel("Salary")
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("gg")
# plt.show()
import pprint

import pandas as pd
from collections import Counter

file = pd.read_csv("data.csv",index_col=0)
launguageCounter = Counter()
for i in  file["LanguagesWorkedWith"].str.split(";"):
    launguageCounter.update(i)

x_language = list(reversed([i[0] for i in launguageCounter.most_common(5)]))
y_count = list(reversed([i[1] for i in launguageCounter.most_common(5)]))

print(x_language)
print(y_count)

plt.xkcd()


plt.xlabel("Count")
plt.ylabel("Languages")
plt.title("Most Popular Languages")
plt.tight_layout()
plt.barh(x_language,y_count)

plt.show()