from typing import Union

import numpy as np
from numba import njit, prange
from PIL import Image


@njit(parallel=True)
def _gamma_correction_core(arr: np.ndarray, gamma: float) -> np.ndarray:
    h, w, c = arr.shape
    result = np.empty_like(arr)
    for i in prange(h):
        for j in range(w):
            for k in range(c):
                result[i, j, k] = (arr[i, j, k] / 255.0) ** gamma * 255.0
    return result


def gamma_correction(image: Union[str, Image.Image], gamma: float = 2.2) -> Image.Image:
    """
    Applies gamma correction to an image.

    Parameters:
    - image (Union[str, Image.Image]): Either a file path to an image (as a string) or a PIL `Image` object.
      If a string is provided, the image will be loaded using PIL.
    - gamma: The gamma value to apply. Default is 2.2, which is commonly used for screen displays.

    Returns:
    - Image.Image: A PIL `Image` object representing the gamma-corrected image.

    Time complexity: O(n), where n is the number of pixels in the image.

    Space complexity: O(n), where n is the number of pixels in the image.
    """
    if gamma <= 0:
        raise ValueError("Gamma must be greater than 0.")

    if isinstance(image, str):
        image = Image.open(image)

    if gamma == 1:
        return image

    if image.mode != "RGB":
        image = image.convert("RGB")

    arr = np.array(image, dtype=np.float64)
    result = _gamma_correction_core(arr, gamma)
    return Image.fromarray(result.astype(np.uint8))
