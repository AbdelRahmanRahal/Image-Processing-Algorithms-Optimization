from typing import Union

import numpy as np
from numba import njit, prange
from PIL import Image

from .convolve import convolve


@njit(parallel=True)
def _gradient_magnitude(edges_x: np.ndarray, edges_y: np.ndarray) -> np.ndarray:
    h, w = edges_x.shape[0], edges_x.shape[1]
    result = np.empty((h, w), dtype=np.float64)
    for i in prange(h):
        for j in range(w):
            result[i, j] = (edges_x[i, j] ** 2 + edges_y[i, j] ** 2) ** 0.5
    return result


def sobel(image: Union[str, Image.Image]) -> Image.Image:
    """
    Applies the Sobel edge detection algorithm to an input image.

    This function computes the gradient of the intensity of the image
    to find edges within the image. It uses the Sobel operator, which
    calculates the derivative of the image intensity at each pixel
    within a small region defined by the kernel. The result is an image
    highlighting the edges.

    Parameters:
    - image (Union[str, Image.Image]): Either a file path to an image (as a string) or a PIL `Image` object.
      If a string is provided, the image will be loaded using PIL and converted to grayscale.

    Returns:
    - Image.Image: A PIL `Image` object representing the edges detected in the original image.

    Time complexity: O(y * x * m * n), where y and x are the dimensions of the input image,
    and m and n are the dimensions of the Sobel kernels.

    Space complexity: O(y * x), where y and x are the dimensions of the input image.
    """
    if isinstance(image, str):
        image = Image.open(image).convert("L")

    image_array = np.array(image)

    # fmt: off
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float64)
    sobel_y = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ], dtype=np.float64)
    # fmt: on

    edges_x = convolve(image_array.astype(np.float64), sobel_x)
    edges_y = convolve(image_array.astype(np.float64), sobel_y)

    edges = _gradient_magnitude(edges_x, edges_y)

    max_value = edges.max()
    if max_value > 0:
        edges = edges / max_value * 255

    return Image.fromarray(edges.astype(np.uint8))
