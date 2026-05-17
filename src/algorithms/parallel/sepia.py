import numpy as np
from numba import njit
from PIL import Image

from .gamma_correction import gamma_correction


@njit(parallel=True)
def _sepia_jit(image_array, sepia_matrix):
	# Accounting for Numba's requirements:
	# 1. np.dot requires matching dtypes (casting uint8 to float64)
	# 2. np.dot only supports 1D or 2D arrays (reshaping 3D to 2D)
	# 3. reshape() requires contiguous arrays (astype on a slice creates one)
	h, w = image_array.shape[:2]
	pixels = image_array[:, :, :3].astype(np.float64).reshape(-1, 3)

	# Parallelized matrix multiplication and clipping
	sepia_flat = np.dot(pixels, sepia_matrix.T)
	return np.clip(sepia_flat, 0, 255).reshape(h, w, 3)


def sepia(image: Image.Image, gamma: float = 1) -> Image.Image:
	"""
	Applies a sepia filter to an input image, enhancing it with a warm brownish tone typical of old photographs.

	The sepia effect is achieved by transforming the color channels of the image according to a predefined matrix,
	followed by clipping the values to ensure they fall within the valid range for displayable colors (0-255).
	Before applying the sepia filter, the image undergoes gamma correction to adjust its brightness and contrast.

	Parameters:
	- image (Image.Image): A PIL `Image` object.
	- gamma (float, optional): The gamma value to apply for gamma correction. Defaults to 1, which means no gamma correction is applied.

	Returns:
	- Image.Image: A PIL `Image` object representing the sepia-enhanced version of the input image.

	Time complexity: O(n), where n is the number of pixels in the image.
	Space complexity: O(n), where n is the number of pixels in the image.
	"""
	image = gamma_correction(image, gamma)

	image_array = np.array(image)

	# fmt: off
	# Sepia filter matrix
	sepia = np.array([
		[0.393, 0.769, 0.189],
		[0.349, 0.686, 0.168],
		[0.272, 0.534, 0.131]
	])
	# fmt: on

	# Using JIT for faster processing
	sepia_image_array = _sepia_jit(image_array, sepia)

	return Image.fromarray(sepia_image_array.astype(np.uint8))
