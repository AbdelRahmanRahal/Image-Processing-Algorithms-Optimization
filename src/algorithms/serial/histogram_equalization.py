import numpy as np
from PIL import Image


def histogram_equalization(image: Image.Image) -> Image.Image:
	"""
	Performs histogram equalization on an input image.

	Histogram equalization is a method in image processing for improving the contrast in images.
	It accomplishes this by effectively spreading out the most frequent pixel values, i.e.,
	stretching out the intensity values it occurs most often.

	Parameters:
	- image (Image.Image): A PIL `Image` object.

	Returns:
	- Image.Image: A PIL `Image` object representing the enhanced version of the input image after applying histogram equalization.

	Time complexity: O(n), where n is the number of pixels in the image.

	Space complexity: O(n), where n is the number of pixels in the image.

	Note: This function works by calculating the histogram of the input image,
	computing the cumulative distribution function (CDF), normalizing the CDF
	to map the pixel intensities to the full range of possible values (0-255),
	and then using this mapping to transform the pixel values in the image.
	"""
	# Ensure the image is in grayscale for histogram calculation
	image_array = np.array(image.convert("L"))

	# Calculating histogram
	hist = [0] * 256
	for pixel in image_array.flatten():
		hist[pixel] += 1

	# Calculating cumulative sum
	cdf = [0] * 256
	cdf[0] = hist[0]
	for i in range(1, len(hist)):
		cdf[i] = cdf[i - 1] + hist[i]

	# Normalizing the cdf
	cdf_min = min(cdf)
	cdf_max = max(cdf)
	if cdf_max != cdf_min:
		# Normalizing the cdf
		cdf_normalized = [
			(value - cdf_min) * 255 / (cdf_max - cdf_min) for value in cdf
		]
	else:
		# If cdf_max equals cdf_min, skip normalization and keep the original image
		cdf_normalized = cdf

	# Using cdf_normalized as a lookup table to equalize the image
	flattened_enhanced_image = [
		cdf_normalized[pixel] for pixel in image_array.flatten()
	]
	enhanced_image = np.array(flattened_enhanced_image, dtype="uint8").reshape(
		image_array.shape
	)

	return Image.fromarray(enhanced_image)
