from astroquery.skyview import SkyView
import matplotlib.pyplot as plt
import astropy.units as u

data = SkyView.get_images("M31", "DSS2 Blue", pixels=1200, radius=150*u.arcmin)[0][0]
plt.imshow(data.data, cmap="gray", origin="lower")
plt.savefig("./star_plots/ASTROQUERY_M31_DSS2_Blue.png")
plt.show()