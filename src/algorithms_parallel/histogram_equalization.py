from typing import Union

import numpy as np
from numba import njit, prange
from PIL import Image


@njit
def _build_histogram_and_lut(flat: np.ndarray) -> np.ndarray:
    hist = np.zeros(256, dtype=np.int64)
    for i in range(flat.size):
        hist[flat[i]] += 1

    cdf = np.zeros(256, dtype=np.int64)
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + hist[i]

    cdf_min = cdf[0]
    cdf_max = cdf[255]
    lut = np.zeros(256, dtype=np.uint8)
    if cdf_max != cdf_min:
        for i in range(256):
            lut[i] = np.uint8((cdf[i] - cdf_min) * 255 / (cdf_max - cdf_min))
    else:
        for i in range(256):
            lut[i] = np.uint8(i)
    return lut


@njit(parallel=True)
def _apply_lut(flat: np.ndarray, lut: np.ndarray) -> np.ndarray:
    result = np.empty_like(flat)
    for i in prange(flat.size):
        result[i] = lut[flat[i]]
    return result


def histogram_equalization(image: Union[str, Image.Image]) -> Image.Image:
    """
    Performs histogram equalization on an input image.

    Histogram equalization improves the contrast in images by effectively
    spreading out the most frequent pixel values.

    Parameters:
    - image (Union[str, Image.Image]): Either a file path to an image (as a string) or a PIL `Image` object.
      If a string is provided, the image will be loaded using PIL and converted to grayscale.

    Returns:
    - Image.Image: A PIL `Image` object representing the enhanced version of the input image.

    Time complexity: O(n), where n is the number of pixels in the image.

    Space complexity: O(n), where n is the number of pixels in the image.
    """
    if isinstance(image, str):
        image = Image.open(image).convert("L")

    image_array = np.array(image)
    flat = image_array.flatten().astype(np.uint8)

    lut = _build_histogram_and_lut(flat)
    result_flat = _apply_lut(flat, lut)

    return Image.fromarray(result_flat.reshape(image_array.shape))
