from scipy.signal import convolve2d
from astroquery.skyview import SkyView
from astropy.visualization import ZScaleInterval
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.filters import meijering, sato
from skimage.feature import corner_foerstner
from skimage.feature import multiscale_basic_features

def log_normalization(pixel_array):
    return np.log(pixel_array)

def plot_pixels(pixel_array, title, color):
    plt.imshow(pixel_array, cmap='gray', origin='lower')
    plt.title(title, color=color, weight='bold')
    plt.axis('off')

data = SkyView.get_images("M31", "SDSSg")[0][0].data
log_array = log_normalization(data)
z = ZScaleInterval()
z1, z2 = z.get_limits(log_array)
img = plt.imshow(log_array, vmin=z1, vmax=z2, cmap="gray", origin="lower")

image_array = img.make_image(renderer=None, unsampled=True)[0]
gray_array = cv2.cvtColor(image_array, cv2.COLOR_BGRA2GRAY)


kernel = np.ones((3, 3))/9
gaussian_kernel = np.array([[1/16, 1/8,1/16],
                             [1/8,1/4,1/8],
                             [1/16, 1/8,1/16]])

convolved_image = convolve2d(gray_array, kernel, mode='same')
gaussian_convolved_image = convolve2d(gray_array, gaussian_kernel, mode='same')
# plot_pixels(convolved_image, title='Normal Kernel Convolution', color='maroon')
# plot_pixels(gaussian_convolved_image, title='Gaussian Kernel Convolution', color='maroon')
SPECTRAL_LIST = ["gray","jet","hot","prism","nipy_spectral"]
meijering_output = meijering(gaussian_convolved_image)
sato_output = sato(gaussian_convolved_image)
feature_output = corner_foerstner(gaussian_convolved_image)
featured_image = multiscale_basic_features(gaussian_convolved_image)
P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P23,P24 = cv2.split(featured_image)
Pixels = [P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P23,P24]

for i, feature in enumerate(Pixels):
    fig = plt.figure()
    plt.imshow(feature, cmap='nipy_spectral', origin='lower')
    plt.title(f'Feature {i+1}')
    plt.axis('off')
    plt.savefig(f"./star_plots/multiscale_basic_features_{i}_M31_SDSSg.png")
    plt.show()

# for colormap in SPECTRAL_LIST:
#     fig = plt.figure()
#     plt.subplot(1, 2, 1)
#     plt.imshow(feature_output[0], cmap=colormap, origin='lower')
#     plt.title(f'Error Image + {colormap}')
#     plt.axis('off')
#
#     plt.subplot(1, 2, 2)
#     plt.imshow(feature_output[1], cmap=colormap, origin='lower')
#     plt.title(f'Roundness of Error Image + {colormap}')
#     plt.axis('off')
#     plt.tight_layout()
#
#     plt.savefig(f"./star_plots/Corner_Foerstner_{colormap}_M31_SDSSg.png")
#     plt.show()
