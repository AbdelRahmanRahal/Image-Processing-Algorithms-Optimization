import numpy as np
from numba import njit
from PIL import Image


@njit(parallel=True)
def _gamma_correction_jit(image_array, gamma):
	return np.power(image_array / 255.0, gamma) * 255


def gamma_correction(image: Image.Image, gamma: float = 2.2) -> Image.Image:
	"""
	Applies gamma correction to an image.

	Parameters:
	- image (Image.Image): A PIL `Image` object.
	- gamma: The gamma value to apply. Default is 2.2, which is commonly used for screen displays.

	Returns:
	- Image.Image: A PIL `Image` object representing the gamma-corrected image.

	Time complexity: O(n), where n is the number of pixels in the image.

	Space complexity: O(n), where n is the number of pixels in the image.
	"""
	if gamma <= 0:
		# Unexpected behaviour occurs at gamma <= 0
		raise ValueError("Gamma must be greater than 0.")

	if gamma == 1:
		# If gamma is 1, the image remains unchanged
		return image

	# Converting the image to RGB mode if it's not already
	if image.mode != "RGB":
		image = image.convert("RGB")

	image_array = np.array(image)

	# Applying gamma correction
	# gamma correction formula:
	# P_c = (P_uc / P_max) ^ γ * P_max
	corrected_array = _gamma_correction_jit(image_array, gamma)
	corrected_image = Image.fromarray(corrected_array.astype(np.uint8))

	return corrected_image
