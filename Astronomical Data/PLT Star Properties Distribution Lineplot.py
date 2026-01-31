import pandas as pd
import matplotlib.pyplot as plt

star_df = pd.read_csv("cleaned_star_data.csv")
plt.figure(figsize=(15, 8))
colors = ['royalblue', 'gold', 'lime', 'magenta']
plt.suptitle('Visualizing the distribution of Numeric Features\n',
             color='tab:pink', fontsize=15, weight='bold')


def line_subplot(i, color, df):
    plt.subplot(4, 1, i + 1)
    plt.plot(df.iloc[:, i], color=color)
    plt.title(df.columns[i], color="red")


for i in range(4):
    line_subplot(i, colors[i], star_df)

plt.tight_layout()
plt.savefig("./star_plots/PLT_lineplot_properties_distribution.png")
plt.show()
