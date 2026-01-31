import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

plt.style.use('fivethirtyeight')

ages = [18, 19, 21, 25, 26, 26, 30, 32, 38, 45, 55]


data = pd.read_csv('data3.csv')
ids = data['Responder_id']
ages = data['Age']
median_age = 29
color = '#fc4f30'
plt.hist(ages,bins=np.arange(5,100,step=5),edgecolor="b",log=True)
plt.axvline(median_age,color=color,label="Median Age")
plt.legend()

plt.title('Ages of Respondents')
plt.xlabel('Ages')
plt.ylabel('Total Respondents')

plt.tight_layout()

plt.show()
