from typing import Union

import numpy as np
from numba import njit, prange
from PIL import Image


@njit(parallel=True)
def _histogram_equalization_jit(image_array):
	# Calculating histogram
	hist = np.zeros(256, dtype=np.int64)
	flattened = image_array.ravel()
	for i in range(flattened.size):
		hist[flattened[i]] += 1

	# Calculating cumulative sum
	cdf = np.cumsum(hist)

	# Normalizing the cdf
	cdf_min = cdf.min()
	cdf_max = cdf.max()
	if cdf_max != cdf_min:
		cdf_normalized = (cdf - cdf_min) * 255 / (cdf_max - cdf_min)
	else:
		cdf_normalized = cdf.astype(np.float64)

	# Using cdf_normalized as a lookup table to equalize the image
	enhanced_flat = np.zeros_like(flattened)
	for i in prange(flattened.size):
		enhanced_flat[i] = cdf_normalized[flattened[i]]

	return enhanced_flat.reshape(image_array.shape)


def histogram_equalization(image: Union[str, Image.Image]) -> Image.Image:
	"""
	Performs histogram equalization on an input image.

	Histogram equalization is a method in image processing for improving the contrast in images.
	It accomplishes this by effectively spreading out the most frequent pixel values, i.e.,
	stretching out the intensity values it occurs most often.

	Parameters:
	- image (Union[str, Image.Image]): Either a file path to an image (as a string) or a PIL `Image` object.
	  If a string is provided, the image will be loaded using PIL and converted to grayscale.

	Returns:
	- Image.Image: A PIL `Image` object representing the enhanced version of the input image after applying histogram equalization.

	Time complexity: O(n), where n is the number of pixels in the image.

	Space complexity: O(n), where n is the number of pixels in the image.

	Note: This function works by calculating the histogram of the input image,
	computing the cumulative distribution function (CDF), normalizing the CDF
	to map the pixel intensities to the full range of possible values (0-255),
	and then using this mapping to transform the pixel values in the image.
	"""
	if isinstance(image, str):  # If it's a string, then it's treated as a file path
		# Loading the image using PIL
		image = Image.open(image).convert("L")

	image_array = np.array(image)

	# Using JIT for faster processing
	enhanced_image = _histogram_equalization_jit(image_array)

	return Image.fromarray(enhanced_image.astype(np.uint8))
