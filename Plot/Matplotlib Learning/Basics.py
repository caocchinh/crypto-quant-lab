from matplotlib import pyplot as plt
plt.xkcd()


dev_x = range(25, 36)
dev_y = [38496, 42000, 46762, 49420, 53200
    , 56000, 62316, 64928, 67317, 68748, 73752]

python_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]

js_dev_y = [37810, 43515, 46823, 49293, 53437,
            56373, 62375, 66674, 68745, 68746, 74583]

plt.plot(dev_x, python_dev_y, color="b", label="Python",marker="x",linewidth=2)
plt.plot(dev_x, js_dev_y, color="y", label="Javascript",marker="x")
plt.plot(dev_x, dev_y, color="k", linestyle="--", label="All devs",marker="o")

plt.legend()
plt.ylabel("Age")
plt.title("Ayo")
plt.xlabel("Salary")
plt.grid(True)
plt.tight_layout()
plt.savefig("gg")
plt.show()
