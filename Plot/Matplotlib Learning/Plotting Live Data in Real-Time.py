import random
from itertools import count
import pandas as pd
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []
index = count()

def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(-6,8))
    plt.cla()
    plt.plot(x_vals,y_vals)

ani = FuncAnimation(plt.gcf(),animate,interval=1000)

plt.tight_layout()
plt.show()


# data = pd.read_csv('data.csv')
# x = data['x_value']
# y1 = data['total_1']
# y2 = data['total_2']