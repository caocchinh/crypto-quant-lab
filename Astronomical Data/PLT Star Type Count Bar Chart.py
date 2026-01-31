import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("dark_background")
star_df = pd.read_csv("cleaned_star_data.csv")
ax = star_df["Star type"].value_counts().plot(kind="bar", color=["brown", "red", "white", "yellow", "lightblue", "orange"])
ax.bar_label(ax.containers[0], color="red")
plt.title("Visualize star count per star type", color="royalblue", weight="bold")
plt.yticks(color="tab:pink")
plt.ylabel("# of Stars", color="white", fontsize=13)
plt.xticks(ticks=[0,1,2,3,4,5],
           labels=["Brown\nDwarf", "Red\nDwarf", "White\nDwarf", "Main\nSequence", "Supergiants", "Hypergiants"],
           rotation=45, color="lime")
plt.savefig("./star_plots/PLT_barplot_star_count.png")
plt.show()





