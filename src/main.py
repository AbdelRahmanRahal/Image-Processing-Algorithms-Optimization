import sys
import time  # for timing

from PIL import ImageQt
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QMainWindow

from gui.mainwindow_ui import Ui_MainWindow

# ---------- Import parallel algorithms ----------
from algorithms_parallel.adaptive_gamma_correction import (
	adaptive_gamma_correction as adaptive_gamma_correction_parallel,
)
from algorithms_parallel.gamma_correction import (
	gamma_correction as gamma_correction_parallel,
)
from algorithms_parallel.gaussian_blur import gaussian_blur as gaussian_blur_parallel
from algorithms_parallel.histogram_equalization import (
	histogram_equalization as histogram_equalization_parallel,
)
from algorithms_parallel.mean_blur import mean_blur as mean_blur_parallel
from algorithms_parallel.sepia import sepia as sepia_parallel
from algorithms_parallel.sobel import sobel as sobel_parallel

# ---------- Import serial algorithms ----------
from algorithms_serial.adaptive_gamma_correction import adaptive_gamma_correction
from algorithms_serial.gamma_correction import gamma_correction
from algorithms_serial.gaussian_blur import gaussian_blur as gb
from algorithms_serial.histogram_equalization import histogram_equalization
from algorithms_serial.mean_blur import mean_blur
from algorithms_serial.sepia import sepia
from algorithms_serial.sobel import sobel


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
		self.compareButton.clicked.connect(self.compare_serial_parallel)
		self.algorithmsComboBox.currentTextChanged.connect(self.update_settings_layout)

		# Setup individual algorithm buttons
		self.applyAGCButton.clicked.connect(self.apply_adaptive_gamma_correction)
		self.applyGammaCorrectionButton.clicked.connect(self.apply_gamma_correction)
		self.applyGaussianBlurButton.clicked.connect(self.apply_gaussian_blur)
		self.applyHEButton.clicked.connect(self.apply_histogram_equalization)
		self.applyMeanButton.clicked.connect(self.apply_mean_blur)
		self.applySepiaButton.clicked.connect(self.apply_sepia_filter)
		self.applySobelButton.clicked.connect(self.apply_sobel_edge_detection)

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

	def apply_adaptive_gamma_correction(self):
		try:
			self.image_path
		except AttributeError:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		block_size = self.blockSizeSpinBox.value()
		gamma_min = self.AGCminimumSlider.value() / 100
		gamma_max = self.AGCmaximumSlider.value() / 100

		corrected_image = adaptive_gamma_correction(
			self.image_path, block_size, (gamma_min, gamma_max)
		)
		corrected_image.save("src/processed/adaptive gamma correction.png")

		qimage = ImageQt.toqimage(corrected_image)
		self.processedImageLabel.setPixmap(
			QPixmap.fromImage(qimage).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

	def apply_gamma_correction(self):
		try:
			self.image_path
		except AttributeError:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		gamma = self.gammaSlider.value() / 100

		corrected_image = gamma_correction(self.image_path, gamma)
		corrected_image.save("src/processed/gamma correction.png")

		qimage = ImageQt.toqimage(corrected_image)
		self.processedImageLabel.setPixmap(
			QPixmap.fromImage(qimage).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

	def apply_gaussian_blur(self):
		try:
			self.image_path
		except AttributeError:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		kernel_size = self.gaussianKernelSizeSpinBox.value()
		sigma = self.gaussianRadiusSlider.value() / 10

		blurred_image = gb(self.image_path, kernel_size, sigma)
		blurred_image.save("src/processed/gaussian blur.png")

		qimage = ImageQt.toqimage(blurred_image)
		self.processedImageLabel.setPixmap(
			QPixmap.fromImage(qimage).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

	def apply_histogram_equalization(self):
		try:
			self.image_path
		except AttributeError:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		equalized_image = histogram_equalization(self.image_path)
		equalized_image.save("src/processed/histogram equalization.png")

		qimage = ImageQt.toqimage(equalized_image)
		self.processedImageLabel.setPixmap(
			QPixmap.fromImage(qimage).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

	def apply_mean_blur(self):
		try:
			self.image_path
		except AttributeError:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		kernel_size = self.meanKernelSizeSpinBox.value()

		blurred_image = mean_blur(self.image_path, kernel_size)
		blurred_image.save("src/processed/mean blur.png")

		qimage = ImageQt.toqimage(blurred_image)
		self.processedImageLabel.setPixmap(
			QPixmap.fromImage(qimage).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

	def apply_sepia_filter(self):
		try:
			self.image_path
		except AttributeError:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		gamma = self.sepiaGammaSlider.value() / 100

		sepia_image = sepia(self.image_path, gamma)
		sepia_image.save("src/processed/sepia.png")

		qimage = ImageQt.toqimage(sepia_image)
		self.processedImageLabel.setPixmap(
			QPixmap.fromImage(qimage).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

	def apply_sobel_edge_detection(self):
		try:
			self.image_path
		except AttributeError:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		sobel_image = sobel(self.image_path)
		sobel_image.save("src/processed/sobel.png")

		qimage = ImageQt.toqimage(sobel_image)
		self.processedImageLabel.setPixmap(
			QPixmap.fromImage(qimage).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

	def compare_serial_parallel(self):
		try:
			if self.image_path is None:
				self.image_path
		except AttributeError:
			QMessageBox.critical(None, "Error", "Please select an image first.")
			return

		# Determine selected algorithm
		algo = self.algorithmsComboBox.currentText()

		# Map to serial and parallel functions and their arguments
		# (You'll need to adapt the argument extraction to match each algorithm)
		if algo == "Adaptive Gamma Correction":
			block_size = self.blockSizeSpinBox.value()
			gamma_min = self.AGCminimumSlider.value() / 100
			gamma_max = self.AGCmaximumSlider.value() / 100
			serial_func = adaptive_gamma_correction
			parallel_func = adaptive_gamma_correction_parallel
			args = (self.image_path, block_size, (gamma_min, gamma_max))

		elif algo == "Gamma Correction":
			gamma = self.gammaSlider.value() / 100
			serial_func = gamma_correction
			parallel_func = gamma_correction_parallel
			args = (self.image_path, gamma)

		elif algo == "Gaussian Blur":
			kernel_size = self.gaussianKernelSizeSpinBox.value()
			sigma = self.gaussianRadiusSlider.value() / 10
			serial_func = gb
			parallel_func = gaussian_blur_parallel
			args = (self.image_path, kernel_size, sigma)

		elif algo == "Histogram Equalization":
			serial_func = histogram_equalization
			parallel_func = histogram_equalization_parallel
			args = (self.image_path,)

		elif algo == "Mean Blur":
			kernel_size = self.meanKernelSizeSpinBox.value()
			serial_func = mean_blur
			parallel_func = mean_blur_parallel
			args = (self.image_path, kernel_size)

		elif algo == "Sepia Filter":
			gamma = self.sepiaGammaSlider.value() / 100
			serial_func = sepia
			parallel_func = sepia_parallel
			args = (self.image_path, gamma)

		elif algo == "Sobel Edge Detection":
			serial_func = sobel
			parallel_func = sobel_parallel
			args = (self.image_path,)

		else:
			QMessageBox.warning(None, "Error", "Unknown algorithm selected.")
			return

		# Run serial
		start_serial = time.perf_counter()
		serial_image = serial_func(*args)
		serial_time = time.perf_counter() - start_serial

		# Run parallel
		start_parallel = time.perf_counter()
		parallel_image = parallel_func(*args)
		parallel_time = time.perf_counter() - start_parallel

		# Display serial image (middle)
		qimage_serial = ImageQt.toqimage(serial_image)
		self.processedImageLabel.setPixmap(
			QPixmap.fromImage(qimage_serial).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

		# Display parallel image (right)
		qimage_parallel = ImageQt.toqimage(parallel_image)
		self.parallelImageLabel.setPixmap(
			QPixmap.fromImage(qimage_parallel).scaled(
				487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
			)
		)

		# Update time label
		self.timeLabel.setText(
			f"Serial: {serial_time:.4f}s | Parallel: {parallel_time:.4f}s | "
			f"Speedup: {serial_time / parallel_time:.2f}x"
		)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon("src/gui/icon.png"))
	window = ImageProcessorApp()
	window.show()
	sys.exit(app.exec())
