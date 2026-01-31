import pandas as pd
import matplotlib.pyplot as plt

star_df = pd.read_csv("cleaned_star_data.csv")
temperature = star_df["Temperature (K)"].values
star_type = star_df["Star type"].values
abs_mag = star_df["Absolute magnitude(Mv)"].values

star_types = {
    0: {'label': 'Brown Dwarf', 'color': 'brown', 'size': 30, 'marker': '.'},
    1: {'label': 'Red Dwarf', 'color': 'red', 'size': 35, 'marker': '.'},
    2: {'label': 'White Dwarf', 'color': 'white', 'size': 40, 'marker': '.'},
    3: {'label': 'Main Sequence', 'color': 'cyan', 'size': 30, 'marker': 'o'},
    4: {'label': 'Supergiants', 'color': 'orange', 'size': 100, 'marker': 'o'},
    5: {'label': 'Hypergiants', 'color': 'maroon', 'size': 150, 'marker': 'o'}
}

axes = []
labels = set()
plt.style.use("dark_background")
for i in range(len(star_type)):
    properties = star_types[star_type[i]]
    ax = plt.scatter(temperature[i], abs_mag[i], s=properties["size"],
                     c=properties["color"], marker=properties["marker"],
                     label=properties["label"])
    if properties["label"] not in labels:
        axes.append(ax)
        labels.add(properties["label"])
ax_sun = plt.scatter(5778, 4.83, s=75, c="yellow", marker='o', label="Sun")
axes.append(ax_sun)
plt.title(f"Hertzsprung - Russell Diagram for {len(star_type)} Stars", fontsize=15, color='royalblue')
plt.ylabel("Absolute Magnitude (Mv)", fontsize=13, color='tab:pink')
plt.xlabel("Temperature (K)", fontsize=13, color='tab:pink')
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.legend(handles=axes)
plt.savefig("./star_plots/PLT_Hertzsprung_Russell_Diagram.png")
plt.show()
