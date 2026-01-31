import pandas as pd
from matplotlib import pyplot as plt

plt.style.use('seaborn')

# x = [5, 7, 8, 5, 6, 7, 9, 2, 3, 4, 4, 4, 2, 6, 3, 6, 8, 6, 4, 1]
# y = [75, 4, 3, 9, 1, 3, 2, 5, 2, 4, 8, 7, 1, 6, 4, 9, 7, 7, 5, 1]
#
#
# colors = [21,2,3, 7, 5, 7, 2, 5, 3, 7, 1, 2, 8, 1, 9, 2, 5, 6, 7, 5]
# sizes = [209, 486, 381, 255, 191, 315, 185, 228, 174,
#          538, 239, 394, 399, 153, 273, 293, 436, 501, 397, 539]
# plt.scatter(x,y ,c=colors,marker="o",edgecolors="b",alpha=.75,cmap="Greens",s=sizes)
# cbar = plt.colorbar()
# cbar.set_label("Sastisfaction level")


data = pd.read_csv('2019-05-31-data.csv')
view_count = data['view_count']
likes = data['likes']
ratio = data['ratio']
plt.xscale("log")
plt.yscale("log")

plt.scatter(view_count,likes,c=ratio,edgecolors="b",alpha=0.75,linewidth=1,cmap="summer")

cbar = plt.colorbar()
cbar.set_label("Like/Dislike Ratio")
plt.title('Trending YouTube Videos')
plt.xlabel('View Count')
plt.ylabel('Total Likes')

plt.tight_layout()

plt.show()