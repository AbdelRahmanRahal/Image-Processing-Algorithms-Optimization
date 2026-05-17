import sys
import time  # for timing

from PIL import Image, ImageQt
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

# ---------- Import parallel algorithms ----------
from algorithms.parallel.adaptive_gamma_correction import (
	adaptive_gamma_correction as adaptive_gamma_correction_parallel,
)
from algorithms.parallel.gamma_correction import (
	gamma_correction as gamma_correction_parallel,
)
from algorithms.parallel.gaussian_blur import gaussian_blur as gaussian_blur_parallel
from algorithms.parallel.histogram_equalization import (
	histogram_equalization as histogram_equalization_parallel,
)
from algorithms.parallel.mean_blur import mean_blur as mean_blur_parallel
from algorithms.parallel.sepia import sepia as sepia_parallel
from algorithms.parallel.sobel import sobel as sobel_parallel

# ---------- Import serial algorithms ----------
from algorithms.serial.adaptive_gamma_correction import adaptive_gamma_correction
from algorithms.serial.gamma_correction import gamma_correction
from algorithms.serial.gaussian_blur import gaussian_blur as gb
from algorithms.serial.histogram_equalization import histogram_equalization
from algorithms.serial.mean_blur import mean_blur
from algorithms.serial.sepia import sepia
from algorithms.serial.sobel import sobel
from gui.mainwindow_ui import Ui_MainWindow


def warm_up_parallel_algorithms():
	"""Pre-compiles Numba JIT functions to avoid first-run latency."""
	# Create a tiny 8x8 dummy image to trigger compilation
	dummy_img = Image.new("RGB", (8, 8), color="red")
	try:
		# Each call triggers the JIT compilation for the underlying Numba functions
		histogram_equalization_parallel(dummy_img)
		gamma_correction_parallel(dummy_img, 1.2)
		sepia_parallel(dummy_img, 1.0)
		adaptive_gamma_correction_parallel(dummy_img, 8, (0.5, 1.5))
		sobel_parallel(dummy_img)
		mean_blur_parallel(dummy_img, 3)
		gaussian_blur_parallel(dummy_img, 3, 1.0)
	except Exception:
		pass


def _to_pixmap(pil_image: Image.Image, w: int = 487, h: int = 360) -> QPixmap:
	qimage = ImageQt.toqimage(pil_image)
	return QPixmap.fromImage(qimage).scaled(
		w, h, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
	)


class ImageProcessorApp(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.image_path = None
		self._connect_signals()
		self.update_settings_layout()

	def _connect_signals(self):
		"""Initialize signal-slot connections."""
		self.loadImageButton.clicked.connect(self.open_image_dialog)
		self.algorithmsComboBox.currentTextChanged.connect(self.update_settings_layout)

		# Every per-algorithm button now triggers compare_serial_parallel
		self.applyAGCButton.clicked.connect(self.compare_serial_parallel)
		self.applyGammaCorrectionButton.clicked.connect(self.compare_serial_parallel)
		self.applyGaussianBlurButton.clicked.connect(self.compare_serial_parallel)
		self.applyHEButton.clicked.connect(self.compare_serial_parallel)
		self.applyMeanButton.clicked.connect(self.compare_serial_parallel)
		self.applySepiaButton.clicked.connect(self.compare_serial_parallel)
		self.applySobelButton.clicked.connect(self.compare_serial_parallel)

		# Setup dynamic value labels
		self.AGCminimumSlider.valueChanged.connect(self.set_AGC_minimum_range_value)
		self.AGCmaximumSlider.valueChanged.connect(self.set_AGC_maximimum_range_value)
		self.gammaSlider.valueChanged.connect(self.set_gamma_value)
		self.gaussianRadiusSlider.valueChanged.connect(self.set_gaussian_radius_value)
		self.sepiaGammaSlider.valueChanged.connect(self.set_sepia_gamma_value)

		# Ensure UI labels match initial slider positions
		self.set_AGC_minimum_range_value()
		self.set_AGC_maximimum_range_value()
		self.set_gamma_value()
		self.set_gaussian_radius_value()
		self.set_sepia_gamma_value()

	def set_AGC_minimum_range_value(self):
		self.AGCminimumRangeValue.setText(str(self.AGCminimumSlider.value() / 100))

	def set_AGC_maximimum_range_value(self):
		self.AGCmaximumRangeValue.setText(str(self.AGCmaximumSlider.value() / 100))

	def set_gamma_value(self):
		self.gammaValue.setText(str(self.gammaSlider.value() / 100))

	def set_gaussian_radius_value(self):
		self.gaussianRadiusValue.setText(str(self.gaussianRadiusSlider.value() / 10))

	def set_sepia_gamma_value(self):
		self.sepiaGammaValue.setText(str(self.sepiaGammaSlider.value() / 100))

	def update_settings_layout(self):
		self.AGCGroupBox.hide()
		self.gammaCorrectionGroupBox.hide()
		self.gaussianGroupBox.hide()
		self.HEGroupBox.hide()
		self.meanGroupBox.hide()
		self.sepiaGroupBox.hide()
		self.sobelGroupBox.hide()

		match self.algorithmsComboBox.currentText():
			case "Adaptive Gamma Correction":
				self.AGCGroupBox.show()
			case "Gamma Correction":
				self.gammaCorrectionGroupBox.show()
			case "Gaussian Blur":
				self.gaussianGroupBox.show()
			case "Histogram Equalization":
				self.HEGroupBox.show()
			case "Mean Blur":
				self.meanGroupBox.show()
			case "Sepia Filter":
				self.sepiaGroupBox.show()
			case "Sobel Edge Detection":
				self.sobelGroupBox.show()
			case _:
				pass

	def open_image_dialog(self):
		fileName, _ = QFileDialog.getOpenFileName(
			None,
			"Select Image",
			"",
			"Images (*.png *.xpm *.jpg)",
			options=QFileDialog.Option.DontUseNativeDialog,
		)
		self.image_path = fileName

		if fileName:
			pixmap = QPixmap(self.image_path).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
			self.originalImageLabel.setPixmap(pixmap)
			self.processedImageLabel.clear()
			self.parallelImageLabel.clear()
			self.timeLabel.setText("")

	def compare_serial_parallel(self):
		if not self.image_path:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		# Load the image once here to exclude I/O from timing comparisons
		input_image = Image.open(self.image_path)
		algo = self.algorithmsComboBox.currentText()

		if algo == "Adaptive Gamma Correction":
			block_size = self.blockSizeSpinBox.value()
			gamma_min = self.AGCminimumSlider.value() / 100
			gamma_max = self.AGCmaximumSlider.value() / 100
			serial_func = adaptive_gamma_correction
			parallel_func = adaptive_gamma_correction_parallel
			args = (input_image, block_size, (gamma_min, gamma_max))

		elif algo == "Gamma Correction":
			gamma = self.gammaSlider.value() / 100
			serial_func = gamma_correction
			parallel_func = gamma_correction_parallel
			args = (input_image, gamma)

		elif algo == "Gaussian Blur":
			kernel_size = self.gaussianKernelSizeSpinBox.value()
			sigma = self.gaussianRadiusSlider.value() / 10
			serial_func = gb
			parallel_func = gaussian_blur_parallel
			args = (input_image, kernel_size, sigma)

		elif algo == "Histogram Equalization":
			serial_func = histogram_equalization
			parallel_func = histogram_equalization_parallel
			args = (input_image,)

		elif algo == "Mean Blur":
			kernel_size = self.meanKernelSizeSpinBox.value()
			serial_func = mean_blur
			parallel_func = mean_blur_parallel
			args = (input_image, kernel_size)

		elif algo == "Sepia Filter":
			gamma = self.sepiaGammaSlider.value() / 100
			serial_func = sepia
			parallel_func = sepia_parallel
			args = (input_image, gamma)

		elif algo == "Sobel Edge Detection":
			serial_func = sobel
			parallel_func = sobel_parallel
			args = (input_image,)

		else:
			QMessageBox.warning(None, "Error", "Unknown algorithm selected.")
			return

		# --- Serial run ---
		self.processedImageLabel.clear()
		self.parallelImageLabel.clear()
		self.timeLabel.setText("Running serial…")
		QtWidgets.QApplication.processEvents()  # flush: show "Running serial…" + cleared panels

		start_serial = time.perf_counter()
		serial_image = serial_func(*args)
		serial_time = time.perf_counter() - start_serial

		# Show serial result immediately and flush to screen before parallel starts
		self.processedImageLabel.setPixmap(_to_pixmap(serial_image))
		self.timeLabel.setText(f"Serial: {serial_time:.4f}s  |  Running parallel…")
		QtWidgets.QApplication.processEvents()  # flush: paint serial image now

		# --- Parallel run ---
		start_parallel = time.perf_counter()
		parallel_image = parallel_func(*args)
		parallel_time = time.perf_counter() - start_parallel

		# Show parallel result
		self.parallelImageLabel.setPixmap(_to_pixmap(parallel_image))

		speedup = serial_time / parallel_time if parallel_time > 0 else float("inf")
		self.timeLabel.setText(
			f"Serial: {serial_time:.4f}s  |  Parallel: {parallel_time:.4f}s  |  "
			f"Speedup: {speedup:.2f}x"
		)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon("src/gui/icon.png"))
	warm_up_parallel_algorithms()
	window = ImageProcessorApp()
	window.show()
	sys.exit(app.exec())
