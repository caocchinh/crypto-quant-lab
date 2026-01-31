from astroquery.skyview import SkyView
from astropy.visualization import ZScaleInterval
import matplotlib.pyplot as plt
import numpy as np
import cv2

def sqrt_scaling(pixel_array):
    return np.sqrt(pixel_array)

def minmax_scaling(pixel_array):
    num = pixel_array - np.min(pixel_array)
    den = np.max(pixel_array) - np.min(pixel_array)
    return num / den


def zscale(pixel_array):
    num = pixel_array - np.mean(pixel_array)
    den = np.std(pixel_array)
    return num / den


def log_normalization(pixel_array):
    return np.log(pixel_array)


def plot_pixels(pixel_array, title, color):
    plt.imshow(pixel_array, cmap='gray', origin='lower')
    plt.title(title, color=color, weight='bold')
    plt.axis('off')


def compare_pixels(original_array, scaled_array, title):
    plt.subplot(1, 2, 1)
    plot_pixels(original_array, title='Original Image', color='black')
    plt.subplot(1, 2, 2)
    plot_pixels(scaled_array, title=title, color='royalblue')
    plt.tight_layout()
    plt.show()


data = SkyView.get_images("M31", "SDSSg")[0][0].data
# minmax_array = minmax_scaling(data)
# compare_pixels(data, minmax_array, title="MinMax Scaled Image")
# zscale_array = zscale(data)
# compare_pixels(data, zscale_array, title="Z Scaled Image")
log_array = log_normalization(data)
# compare_pixels(data, log_array, title="Log Normalized Image")
# sqrt_array = sqrt_scaling(data)
# compare_pixels(data, sqrt_array, title="Square Root Image")
# plt.hist(log_array.flat, bins=1000)
z = ZScaleInterval()
z1, z2 = z.get_limits(log_array)
img = plt.imshow(log_array, vmin=z1, vmax=z2, cmap="gray", origin="lower")
image_array = img.make_image(renderer=None, unsampled=True)[0]
gray_array = cv2.cvtColor(image_array, cv2.COLOR_BGRA2GRAY)
# plot_pixels(gray_array, title='ZScaleInterval GrayScale', color='royalblue')
plt.figure().clear()
plt.hist(gray_array.flat, bins=1000)
plt.show()
