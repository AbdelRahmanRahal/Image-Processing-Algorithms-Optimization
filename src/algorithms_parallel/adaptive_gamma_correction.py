from typing import Union

import numpy as np
from numba import njit, prange
from PIL import Image


@njit(parallel=True)
def _agc_core(
    arr: np.ndarray, block_size: int, gamma_min: float, gamma_max: float
) -> np.ndarray:
    h, w, c = arr.shape
    result = arr.copy().astype(np.float64)
    n_blocks_y = (h + block_size - 1) // block_size
    n_blocks_x = (w + block_size - 1) // block_size

    for by in prange(n_blocks_y):
        y0 = by * block_size
        y1 = min(y0 + block_size, h)
        for bx in range(n_blocks_x):
            x0 = bx * block_size
            x1 = min(x0 + block_size, w)
            total = 0.0
            count = 0
            for i in range(y0, y1):
                for j in range(x0, x1):
                    for k in range(c):
                        total += arr[i, j, k]
                        count += 1
            avg = total / count
            gamma = gamma_min + (gamma_max - gamma_min) * avg / 255.0
            for i in range(y0, y1):
                for j in range(x0, x1):
                    for k in range(c):
                        result[i, j, k] = (arr[i, j, k] / 255.0) ** gamma * 255.0

    return result


def adaptive_gamma_correction(
    image: Union[str, Image.Image],
    block_size: int = 16,
    gamma_range: tuple = (0.5, 2.0),
) -> Image.Image:
    """
    Applies adaptive gamma correction to an input image.

    This function improves the visibility of details in both dark and bright
    regions of an image by adjusting the gamma value adaptively based on the
    local brightness of different blocks within the image.

    Parameters:
    - image (Union[str, Image.Image]): Either a file path to an image (as a string) or a PIL `Image` object.
      If a string is provided, the image will be loaded using PIL.
    - block_size (int, optional): The size of the blocks over which gamma correction is applied. Defaults to 16.
    - gamma_range (tuple, optional): The minimum and maximum gamma values to use for correction. Defaults to (0.5, 2.0).

    Returns:
    - Image.Image: A PIL `Image` object representing the corrected version of the input image.

    Time complexity: O(n), where n is the number of pixels in the image.

    Space complexity: O(n), where n is the number of pixels in the image.
    """
    if isinstance(image, str):
        image = Image.open(image)

    arr = np.array(image, dtype=np.float64)
    result = _agc_core(arr, block_size, float(gamma_range[0]), float(gamma_range[1]))
    return Image.fromarray(result.astype(np.uint8))
