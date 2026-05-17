import time

import numpy as np
from PIL import Image

from ..algorithms.serial.gaussian_blur import gaussian_blur

# Create test image
img = Image.fromarray(np.random.randint(0, 255, (4000, 4000, 3), dtype=np.uint8))

start = time.perf_counter()

for _ in range(10):
	gaussian_blur(img, kernel_size=7, sigma=1.5)

end = time.perf_counter()

print(f"Total time: {end - start:.4f}s")
print(f"Average time: {(end - start) / 10:.4f}s")
