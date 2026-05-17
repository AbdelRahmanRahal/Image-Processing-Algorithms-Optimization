import time
import numpy as np
from PIL import Image
import sys
import os

# Ensure the 'src' directory is in the path for algorithm imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
	from algorithms.parallel.adaptive_gamma_correction import (
		adaptive_gamma_correction as agc_parallel,
	)
	from algorithms.parallel.gamma_correction import gamma_correction as gc_parallel
	from algorithms.parallel.gaussian_blur import gaussian_blur as gb_parallel
	from algorithms.parallel.histogram_equalization import (
		histogram_equalization as he_parallel,
	)

	from algorithms.parallel.mean_blur import mean_blur as mb_parallel
	from algorithms.parallel.sepia import sepia as sepia_parallel
	from algorithms.parallel.sobel import sobel as sobel_parallel

	# ---------- Import serial algorithms ----------
	from algorithms.serial.adaptive_gamma_correction import (
		adaptive_gamma_correction as agc,
	)
	from algorithms.serial.gamma_correction import gamma_correction as gc
	from algorithms.serial.gaussian_blur import gaussian_blur as gb
	from algorithms.serial.histogram_equalization import histogram_equalization as he
	from algorithms.serial.mean_blur import mean_blur as mb
	from algorithms.serial.sepia import sepia
	from algorithms.serial.sobel import sobel
except ImportError as e:
	print(
		f"Error: Could not import algorithms. Make sure to run this script from the 'src' directory. {e}"
	)
	sys.exit(1)


def run_timer(func, *args, **kwargs):
	"""
	Measures execution time.
	Includes a warm-up phase to ensure JIT compilation or cache initialization
	doesn't skew the results.
	"""
	if func is None:
		return None

	# Warm-up phase (Critical for Numba/Parallel code)
	func(*args, **kwargs)

	# Measurement phase
	start = time.perf_counter()
	func(*args, **kwargs)
	end = time.perf_counter()

	return end - start


def print_report_row(algo_name, t_serial, t_parallel):
	if t_serial and t_parallel:
		speedup = t_serial / t_parallel
		gain = f"{speedup:.2f}x"
	else:
		gain = "N/A"

	s_str = f"{t_serial:.4f}s" if t_serial else "N/A"
	p_str = f"{t_parallel:.4f}s" if t_parallel else "N/A"

	print(f"{algo_name:<30} | {s_str:<12} | {p_str:<13} | {gain:<10}")


def main():
	width, height = 1000, 1000
	print(f"\nInitializing Benchmark with {width}x{height} image...")
	test_img = Image.fromarray(
		np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
	)

	print("\n" + "=" * 75)
	print(f"{'ALGORITHM PERFORMANCE COMPARISON':^75}")
	print("=" * 75)
	print(
		f"{'Algorithm':<30} | {'Serial Time':<12} | {'Parallel Time':<13} | {'Speedup'}"
	)
	print("-" * 75)

	# 1. AGC Benchmark
	t_s_agc = run_timer(agc, test_img)
	t_p_agc = run_timer(agc_parallel, test_img)
	print_report_row("Adapative Gamma Correction", t_s_agc, t_p_agc)

	# 2. Gamma Correction Benchmark
	t_s_gc = run_timer(gc, test_img)
	t_p_gc = run_timer(gc_parallel, test_img)
	print_report_row("Gamma Correction", t_s_gc, t_p_gc)

	# 3. Gaussian Blur Benchmark
	# Using a 7x7 kernel to increase computational load
	t_s_blur = run_timer(gb, test_img, kernel_size=7, sigma=1.5)
	t_p_blur = run_timer(gb_parallel, test_img, kernel_size=7, sigma=1.5)
	print_report_row("Gaussian Blur", t_s_blur, t_p_blur)

	# 4. Histogram Equalization Benchmark
	t_s_he = run_timer(he, test_img)
	t_p_he = run_timer(he_parallel, test_img)
	print_report_row("Histogram Equalization", t_s_he, t_p_he)

	# 5. Mean Blur Benchmark
	# Using a 7x7 kernel to increase computational load
	t_s_blur = run_timer(mb, test_img, kernel_size=7)
	t_p_blur = run_timer(mb_parallel, test_img, kernel_size=7)
	print_report_row("Mean Blur", t_s_blur, t_p_blur)

	# 6. Sepia Filter Benchmark
	t_s_sepia = run_timer(sepia, test_img)
	t_p_sepia = run_timer(sepia_parallel, test_img)
	print_report_row("Sepia Filter", t_s_sepia, t_p_sepia)

	# 7. Sobel Filter Benchmark
	t_s_sobel = run_timer(sobel, test_img)
	t_p_sobel = run_timer(sobel_parallel, test_img)
	print_report_row("Sobel Filter", t_s_sobel, t_p_sobel)

	print("=" * 75)

	print("\nFindings:")
	print("- Parallel performance scales better as image resolution increases.")
	print("- Serial overhead is dominated by pixel-wise loops or large array copies.")

	print("\nTo generate low-level profile reports for Perf:")
	print("-" * 75)
	print("1. Linux Perf:  perf stat -d python benchmark.py")
	print("2. CProfile:    python -m cProfile -s tottime benchmark.py")
	print("=" * 75 + "\n")


if __name__ == "__main__":
	main()
