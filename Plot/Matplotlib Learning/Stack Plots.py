from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")

minute = range(1,10)

player1 = [8, 6, 5, 5, 4, 2, 1, 1, 0]
player2 = [0, 1, 2, 2, 2, 4, 4, 4, 4]
player3 = [0, 1, 1, 1, 2, 2, 3, 3, 4]

plt.stackplot(minute,player1,player2,player3 ,labels=["1","2","3"])
plt.legend(loc="lower left")

plt.title("My Stacked Plot")
plt.tight_layout()
plt.show()