from astroquery.skyview import SkyView
import matplotlib.pyplot as plt

data = SkyView.get_images("M31", "SDSSg")[0][0]
plt.imshow(data.data, cmap="gray", origin="lower")
plt.savefig("./star_plots/ASTROQUERY_M31_SDSSg.png")
plt.show()