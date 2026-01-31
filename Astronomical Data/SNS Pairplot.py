import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

star_df = pd.read_csv("cleaned_star_data.csv")
sns.pairplot(star_df)
plt.tight_layout()
plt.savefig("./star_plots/SNS_pairplot.png")
plt.show()