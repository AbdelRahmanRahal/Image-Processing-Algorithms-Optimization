import time
import warnings

import numpy as np
from numba import set_num_threads
from numba.core.errors import NumbaPerformanceWarning
from PIL import Image

from ..algorithms.parallel.gaussian_blur import gaussian_blur

# Suppress Numba warnings
warnings.simplefilter("ignore", category=NumbaPerformanceWarning)

# Set thread count
set_num_threads(20)

# Create test image
img = Image.fromarray(np.random.randint(0, 255, (4000, 4000, 3), dtype=np.uint8))

# Warm-up run (JIT compilation happens here)
gaussian_blur(img, kernel_size=7, sigma=1.5)

# Actual benchmark
start = time.perf_counter()

for _ in range(10):
	gaussian_blur(img, kernel_size=7, sigma=1.5)

end = time.perf_counter()

print(f"Total time: {end - start:.4f}s")
print(f"Average time: {(end - start) / 10:.4f}s")
