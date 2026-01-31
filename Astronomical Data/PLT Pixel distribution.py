from astroquery.skyview import SkyView
import matplotlib.pyplot as plt

data = SkyView.get_images("M31", "SDSSg")[0][0]
plt.hist(data.data.flat, bins=1000)
plt.savefig("./star_plots/PLT_Pixel_Distribution_M31_SDSSg.png")
plt.show()