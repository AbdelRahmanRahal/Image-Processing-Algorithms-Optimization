from typing import Union

import numpy as np
from numba import njit, prange
from PIL import Image

from .gamma_correction import gamma_correction


@njit(parallel=True)
def _sepia_core(arr: np.ndarray) -> np.ndarray:
    h, w = arr.shape[0], arr.shape[1]
    result = np.empty((h, w, 3), dtype=np.float64)
    for i in prange(h):
        for j in range(w):
            r = float(arr[i, j, 0])
            g = float(arr[i, j, 1])
            b = float(arr[i, j, 2])
            out_r = 0.393 * r + 0.769 * g + 0.189 * b
            out_g = 0.349 * r + 0.686 * g + 0.168 * b
            out_b = 0.272 * r + 0.534 * g + 0.131 * b
            result[i, j, 0] = out_r if out_r < 255.0 else 255.0
            result[i, j, 1] = out_g if out_g < 255.0 else 255.0
            result[i, j, 2] = out_b if out_b < 255.0 else 255.0
    return result


def sepia(image: Union[str, Image.Image], gamma: float = 1) -> Image.Image:
    """
    Applies a sepia filter to an input image, enhancing it with a warm brownish tone typical of old photographs.

    The sepia effect is achieved by transforming the color channels of the image according to a predefined matrix,
    followed by clipping the values to ensure they fall within the valid range for displayable colors (0-255).
    Before applying the sepia filter, the image undergoes gamma correction to adjust its brightness and contrast.

    Parameters:
    - image (Union[str, Image.Image]): Either a file path to an image (as a string) or a PIL `Image` object.
      If a string is provided, the image will be loaded using PIL.
    - gamma (float, optional): The gamma value to apply for gamma correction. Defaults to 1, which means no gamma correction is applied.

    Returns:
    - Image.Image: A PIL `Image` object representing the sepia-enhanced version of the input image.

    Time complexity: O(n), where n is the number of pixels in the image.
    Space complexity: O(n), where n is the number of pixels in the image.
    """
    image = gamma_correction(image, gamma)
    arr = np.array(image)
    result = _sepia_core(arr)
    return Image.fromarray(result.astype(np.uint8))
