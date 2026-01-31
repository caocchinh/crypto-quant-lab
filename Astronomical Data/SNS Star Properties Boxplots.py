import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("default")
plt.figure(figsize=(25,8))
star_df = pd.read_csv("cleaned_star_data.csv")
plt.suptitle('Visualizing the outliers in Numeric features of Star Type',
             color='black', weight='bold', fontsize=15)
for i in range(4):
    plt.subplot(1,4,i+1)
    sns.boxplot(x=star_df["Star type"], y=star_df.iloc[:, i], palette="Spectral")
    plt.ylabel("")
    plt.title(star_df.columns[i], color="red")
plt.savefig("./star_plots/SNS_boxplot_star_properties.png")
plt.show()
