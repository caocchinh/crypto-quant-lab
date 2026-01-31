import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("dark_background")
plt.title("Visualizing the count of Star Colors", color="royalblue", fontsize=15)
star_df = pd.read_csv("cleaned_star_data.csv")
star_color = star_df["Star color"].value_counts()
ax = sns.barplot(x=star_color.index, y=star_color, palette="viridis")
for container in ax.containers:
    ax.bar_label(container, color="red", weight="bold")
plt.xticks(rotation=15, color="orange", fontsize=11)
plt.ylabel("# Star color", color="white", fontsize=13)
plt.yticks(color="tab:pink")
plt.savefig("./star_plots/SNS_barplot_color_count.png")
plt.show()
