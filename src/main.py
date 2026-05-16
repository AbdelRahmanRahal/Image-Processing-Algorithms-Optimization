import time  # for timing

from PIL import ImageQt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox

# ---------- Import parallel algorithms (to be created) ----------
# Replace with your actual parallel implementations
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

# ---------- Import serial algorithms (your existing ones) ----------
from algorithms_serial.adaptive_gamma_correction import adaptive_gamma_correction
from algorithms_serial.gamma_correction import gamma_correction
from algorithms_serial.gaussian_blur import gaussian_blur as gb
from algorithms_serial.histogram_equalization import histogram_equalization
from algorithms_serial.mean_blur import mean_blur
from algorithms_serial.sepia import sepia
from algorithms_serial.sobel import sobel


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setEnabled(True)
		MainWindow.resize(1600, 900)
		MainWindow.setMinimumSize(QtCore.QSize(1600, 900))
		MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
		self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(58, 36, 1482, 789))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.previewGroupBox = QtWidgets.QGroupBox(parent=self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(6)
		sizePolicy.setHeightForWidth(
			self.previewGroupBox.sizePolicy().hasHeightForWidth()
		)
		self.previewGroupBox.setSizePolicy(sizePolicy)
		self.previewGroupBox.setObjectName("previewGroupBox")
		self.gridLayout_3 = QtWidgets.QGridLayout(self.previewGroupBox)
		self.gridLayout_3.setObjectName("gridLayout_3")

		# Original image label (left)
		self.originalImageLabel = QtWidgets.QLabel(parent=self.previewGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.originalImageLabel.sizePolicy().hasHeightForWidth()
		)
		self.originalImageLabel.setSizePolicy(sizePolicy)
		self.originalImageLabel.setText("")
		self.originalImageLabel.setObjectName("originalImageLabel")
		self.gridLayout_3.addWidget(self.originalImageLabel, 2, 0, 1, 1)

		# Processed image label (serial, middle)
		self.processedImageLabel = QtWidgets.QLabel(parent=self.previewGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.processedImageLabel.sizePolicy().hasHeightForWidth()
		)
		self.processedImageLabel.setSizePolicy(sizePolicy)
		self.processedImageLabel.setText("")
		self.processedImageLabel.setObjectName("processedImageLabel")
		self.gridLayout_3.addWidget(
			self.processedImageLabel, 2, 1, 1, 1
		)  # now spans only col 1

		# NEW: Parallel image label (right)
		self.parallelImageLabel = QtWidgets.QLabel(parent=self.previewGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.parallelImageLabel.sizePolicy().hasHeightForWidth()
		)
		self.parallelImageLabel.setSizePolicy(sizePolicy)
		self.parallelImageLabel.setText("")
		self.parallelImageLabel.setObjectName("parallelImageLabel")
		self.gridLayout_3.addWidget(self.parallelImageLabel, 2, 2, 1, 1)

		# Row 3: labels for column headings (optional)
		# Row 4: existing controls (loadImageButton, selectAlgorithmLabel, algorithmsComboBox)

		self.loadImageButton = QtWidgets.QPushButton(parent=self.previewGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
		)
		sizePolicy.setHorizontalStretch(4)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.loadImageButton.sizePolicy().hasHeightForWidth()
		)
		self.loadImageButton.setSizePolicy(sizePolicy)
		self.loadImageButton.setObjectName("loadImageButton")
		self.gridLayout_3.addWidget(self.loadImageButton, 4, 0, 1, 1)

		self.selectAlgorithmLabel = QtWidgets.QLabel(parent=self.previewGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.selectAlgorithmLabel.sizePolicy().hasHeightForWidth()
		)
		self.selectAlgorithmLabel.setSizePolicy(sizePolicy)
		self.selectAlgorithmLabel.setObjectName("selectAlgorithmLabel")
		self.gridLayout_3.addWidget(self.selectAlgorithmLabel, 4, 1, 1, 1)

		self.algorithmsComboBox = QtWidgets.QComboBox(parent=self.previewGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
		)
		sizePolicy.setHorizontalStretch(3)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.algorithmsComboBox.sizePolicy().hasHeightForWidth()
		)
		self.algorithmsComboBox.setSizePolicy(sizePolicy)
		self.algorithmsComboBox.setContextMenuPolicy(
			QtCore.Qt.ContextMenuPolicy.NoContextMenu
		)
		self.algorithmsComboBox.setWhatsThis("")
		self.algorithmsComboBox.setObjectName("algorithmsComboBox")
		self.algorithmsComboBox.addItem("")
		self.algorithmsComboBox.addItem("")
		self.algorithmsComboBox.addItem("")
		self.algorithmsComboBox.addItem("")
		self.algorithmsComboBox.addItem("")
		self.algorithmsComboBox.addItem("")
		self.algorithmsComboBox.addItem("")
		self.gridLayout_3.addWidget(self.algorithmsComboBox, 4, 2, 1, 1)

		# NEW: Compare button (row 5, span all columns)
		self.compareButton = QtWidgets.QPushButton(parent=self.previewGroupBox)
		self.compareButton.setObjectName("compareButton")
		self.gridLayout_3.addWidget(self.compareButton, 5, 0, 1, 3)

		# NEW: Time label at the bottom (row 6)
		self.timeLabel = QtWidgets.QLabel(parent=self.previewGroupBox)
		self.timeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.timeLabel.setObjectName("timeLabel")
		self.gridLayout_3.addWidget(self.timeLabel, 6, 0, 1, 3)

		self.processedImageLabel = QtWidgets.QLabel(parent=self.previewGroupBox)
		# self.processedImageLabel.setEnabled(False)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.processedImageLabel.sizePolicy().hasHeightForWidth()
		)
		self.processedImageLabel.setSizePolicy(sizePolicy)
		self.processedImageLabel.setContextMenuPolicy(
			QtCore.Qt.ContextMenuPolicy.DefaultContextMenu
		)
		self.processedImageLabel.setStatusTip("")
		self.processedImageLabel.setText("")
		self.processedImageLabel.setObjectName("processedImageLabel")
		self.gridLayout_3.addWidget(self.processedImageLabel, 2, 1, 1, 2)
		self.gridLayout.addWidget(self.previewGroupBox, 0, 0, 1, 2)
		self.AGCGroupBox = QtWidgets.QGroupBox(parent=self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.AGCGroupBox.sizePolicy().hasHeightForWidth())
		self.AGCGroupBox.setSizePolicy(sizePolicy)
		self.AGCGroupBox.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
		self.AGCGroupBox.setObjectName("AGCGroupBox")
		self.AGCLayout = QtWidgets.QHBoxLayout(self.AGCGroupBox)
		self.AGCLayout.setObjectName("AGCLayout")
		spacerItem = QtWidgets.QSpacerItem(
			150,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.AGCLayout.addItem(spacerItem)
		self.AGCSettingsLayout = QtWidgets.QWidget(parent=self.AGCGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(2)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.AGCSettingsLayout.sizePolicy().hasHeightForWidth()
		)
		self.AGCSettingsLayout.setSizePolicy(sizePolicy)
		self.AGCSettingsLayout.setObjectName("AGCSettingsLayout")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.AGCSettingsLayout)
		self.verticalLayout.setObjectName("verticalLayout")
		self.blockSizeLayout = QtWidgets.QHBoxLayout()
		self.blockSizeLayout.setObjectName("blockSizeLayout")
		self.blockSizeLabel = QtWidgets.QLabel(parent=self.AGCSettingsLayout)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.blockSizeLabel.sizePolicy().hasHeightForWidth()
		)
		self.blockSizeLabel.setSizePolicy(sizePolicy)
		self.blockSizeLabel.setObjectName("blockSizeLabel")
		self.blockSizeLayout.addWidget(self.blockSizeLabel)
		self.blockSizeSpinBox = QtWidgets.QSpinBox(parent=self.AGCSettingsLayout)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
		)
		sizePolicy.setHorizontalStretch(3)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.blockSizeSpinBox.sizePolicy().hasHeightForWidth()
		)
		self.blockSizeSpinBox.setSizePolicy(sizePolicy)
		self.blockSizeSpinBox.setContextMenuPolicy(
			QtCore.Qt.ContextMenuPolicy.DefaultContextMenu
		)
		self.blockSizeSpinBox.setMinimum(4)
		self.blockSizeSpinBox.setMaximum(32)
		self.blockSizeSpinBox.setSingleStep(4)
		self.blockSizeSpinBox.setProperty("value", 16)
		self.blockSizeSpinBox.setObjectName("blockSizeSpinBox")
		self.blockSizeLayout.addWidget(self.blockSizeSpinBox)
		spacerItem1 = QtWidgets.QSpacerItem(
			300,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.blockSizeLayout.addItem(spacerItem1)
		self.verticalLayout.addLayout(self.blockSizeLayout)
		self.AGCgammaRangeLayout = QtWidgets.QHBoxLayout()
		self.AGCgammaRangeLayout.setObjectName("AGCgammaRangeLayout")
		self.AGCsliderLabelsLayout = QtWidgets.QVBoxLayout()
		self.AGCsliderLabelsLayout.setObjectName("AGCsliderLabelsLayout")
		self.AGCminimumLabel = QtWidgets.QLabel(parent=self.AGCSettingsLayout)
		self.AGCminimumLabel.setObjectName("AGCminimumLabel")
		self.AGCsliderLabelsLayout.addWidget(self.AGCminimumLabel)
		self.AGCmaximumLabel = QtWidgets.QLabel(parent=self.AGCSettingsLayout)
		self.AGCmaximumLabel.setObjectName("AGCmaximumLabel")
		self.AGCsliderLabelsLayout.addWidget(self.AGCmaximumLabel)
		spacerItem2 = QtWidgets.QSpacerItem(
			20,
			20,
			QtWidgets.QSizePolicy.Policy.Ignored,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.AGCsliderLabelsLayout.addItem(spacerItem2)
		self.AGCgammaRangeLayout.addLayout(self.AGCsliderLabelsLayout)
		self.AGCgammaSlidersLayout = QtWidgets.QVBoxLayout()
		self.AGCgammaSlidersLayout.setObjectName("AGCgammaSlidersLayout")
		self.AGCminimumSlider = QtWidgets.QSlider(parent=self.AGCSettingsLayout)
		self.AGCminimumSlider.setEnabled(True)
		self.AGCminimumSlider.setMinimum(5)
		self.AGCminimumSlider.setMaximum(100)
		self.AGCminimumSlider.setPageStep(10)
		self.AGCminimumSlider.setProperty("value", 50)
		self.AGCminimumSlider.setTracking(True)
		self.AGCminimumSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
		self.AGCminimumSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
		self.AGCminimumSlider.setObjectName("AGCminimumSlider")
		self.AGCgammaSlidersLayout.addWidget(self.AGCminimumSlider)
		self.AGCmaximumSlider = QtWidgets.QSlider(parent=self.AGCSettingsLayout)
		self.AGCmaximumSlider.setMinimum(101)
		self.AGCmaximumSlider.setMaximum(300)
		self.AGCmaximumSlider.setProperty("value", 200)
		self.AGCmaximumSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
		self.AGCmaximumSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
		self.AGCmaximumSlider.setObjectName("AGCmaximumSlider")
		self.AGCgammaSlidersLayout.addWidget(self.AGCmaximumSlider)
		self.AGCgammaRangeLabel = QtWidgets.QLabel(parent=self.AGCSettingsLayout)
		self.AGCgammaRangeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.AGCgammaRangeLabel.setObjectName("AGCgammaRangeLabel")
		self.AGCgammaSlidersLayout.addWidget(self.AGCgammaRangeLabel)
		self.AGCgammaRangeLayout.addLayout(self.AGCgammaSlidersLayout)
		self.AGCrangeValuesLayout = QtWidgets.QVBoxLayout()
		self.AGCrangeValuesLayout.setObjectName("AGCrangeValuesLayout")
		self.AGCminimumRangeValue = QtWidgets.QLabel(parent=self.AGCSettingsLayout)
		self.AGCminimumRangeValue.setObjectName("AGCminimumRangeValue")
		self.AGCrangeValuesLayout.addWidget(self.AGCminimumRangeValue)
		self.AGCmaximumRangeValue = QtWidgets.QLabel(parent=self.AGCSettingsLayout)
		self.AGCmaximumRangeValue.setObjectName("AGCmaximumRangeValue")
		self.AGCrangeValuesLayout.addWidget(self.AGCmaximumRangeValue)
		spacerItem3 = QtWidgets.QSpacerItem(
			40,
			20,
			QtWidgets.QSizePolicy.Policy.Ignored,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.AGCrangeValuesLayout.addItem(spacerItem3)
		self.AGCgammaRangeLayout.addLayout(self.AGCrangeValuesLayout)
		self.verticalLayout.addLayout(self.AGCgammaRangeLayout)
		self.AGCLayout.addWidget(self.AGCSettingsLayout)
		self.applyAGCButton = QtWidgets.QPushButton(parent=self.AGCGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
		)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.applyAGCButton.sizePolicy().hasHeightForWidth()
		)
		self.applyAGCButton.setSizePolicy(sizePolicy)
		self.applyAGCButton.setObjectName("applyAGCButton")
		self.AGCLayout.addWidget(self.applyAGCButton)
		spacerItem4 = QtWidgets.QSpacerItem(
			150,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.AGCLayout.addItem(spacerItem4)
		self.gridLayout.addWidget(self.AGCGroupBox, 1, 0, 1, 2)
		self.gaussianGroupBox = QtWidgets.QGroupBox(parent=self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(
			self.gaussianGroupBox.sizePolicy().hasHeightForWidth()
		)
		self.gaussianGroupBox.setSizePolicy(sizePolicy)
		self.gaussianGroupBox.setObjectName("gaussianGroupBox")
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.gaussianGroupBox)
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		spacerItem5 = QtWidgets.QSpacerItem(
			250,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_3.addItem(spacerItem5)
		self.gaussianSettingsLayout = QtWidgets.QWidget(parent=self.gaussianGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(2)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.gaussianSettingsLayout.sizePolicy().hasHeightForWidth()
		)
		self.gaussianSettingsLayout.setSizePolicy(sizePolicy)
		self.gaussianSettingsLayout.setObjectName("gaussianSettingsLayout")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gaussianSettingsLayout)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.gaussianKernelSizeLayout = QtWidgets.QHBoxLayout()
		self.gaussianKernelSizeLayout.setObjectName("gaussianKernelSizeLayout")
		self.gaussianKernelSizeLabel = QtWidgets.QLabel(
			parent=self.gaussianSettingsLayout
		)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.gaussianKernelSizeLabel.sizePolicy().hasHeightForWidth()
		)
		self.gaussianKernelSizeLabel.setSizePolicy(sizePolicy)
		self.gaussianKernelSizeLabel.setObjectName("gaussianKernelSizeLabel")
		self.gaussianKernelSizeLayout.addWidget(self.gaussianKernelSizeLabel)
		self.gaussianKernelSizeSpinBox = QtWidgets.QSpinBox(
			parent=self.gaussianSettingsLayout
		)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
		)
		sizePolicy.setHorizontalStretch(3)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.gaussianKernelSizeSpinBox.sizePolicy().hasHeightForWidth()
		)
		self.gaussianKernelSizeSpinBox.setSizePolicy(sizePolicy)
		self.gaussianKernelSizeSpinBox.setContextMenuPolicy(
			QtCore.Qt.ContextMenuPolicy.DefaultContextMenu
		)
		self.gaussianKernelSizeSpinBox.setMinimum(3)
		self.gaussianKernelSizeSpinBox.setMaximum(15)
		self.gaussianKernelSizeSpinBox.setSingleStep(2)
		self.gaussianKernelSizeSpinBox.setProperty("value", 5)
		self.gaussianKernelSizeSpinBox.setObjectName("gaussianKernelSizeSpinBox")
		self.gaussianKernelSizeLayout.addWidget(self.gaussianKernelSizeSpinBox)
		spacerItem6 = QtWidgets.QSpacerItem(
			220,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.gaussianKernelSizeLayout.addItem(spacerItem6)
		self.verticalLayout_2.addLayout(self.gaussianKernelSizeLayout)
		self.gaussianRadiusLayout = QtWidgets.QHBoxLayout()
		self.gaussianRadiusLayout.setObjectName("gaussianRadiusLayout")
		self.gaussianRadiusLabel = QtWidgets.QLabel(parent=self.gaussianSettingsLayout)
		self.gaussianRadiusLabel.setObjectName("gaussianRadiusLabel")
		self.gaussianRadiusLayout.addWidget(self.gaussianRadiusLabel)
		self.gaussianRadiusSlider = QtWidgets.QSlider(
			parent=self.gaussianSettingsLayout
		)
		self.gaussianRadiusSlider.setMinimum(10)
		self.gaussianRadiusSlider.setMaximum(100)
		self.gaussianRadiusSlider.setProperty("value", 10)
		self.gaussianRadiusSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
		self.gaussianRadiusSlider.setTickPosition(
			QtWidgets.QSlider.TickPosition.TicksAbove
		)
		self.gaussianRadiusSlider.setObjectName("gaussianRadiusSlider")
		self.gaussianRadiusLayout.addWidget(self.gaussianRadiusSlider)
		self.gaussianRadiusValue = QtWidgets.QLabel(parent=self.gaussianSettingsLayout)
		self.gaussianRadiusValue.setObjectName("gaussianRadiusValue")
		self.gaussianRadiusLayout.addWidget(self.gaussianRadiusValue)
		self.verticalLayout_2.addLayout(self.gaussianRadiusLayout)
		self.horizontalLayout_3.addWidget(self.gaussianSettingsLayout)
		self.applyGaussianBlurButton = QtWidgets.QPushButton(
			parent=self.gaussianGroupBox
		)
		self.applyGaussianBlurButton.setObjectName("applyGaussianBlurButton")
		self.horizontalLayout_3.addWidget(self.applyGaussianBlurButton)
		spacerItem7 = QtWidgets.QSpacerItem(
			250,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_3.addItem(spacerItem7)
		self.gridLayout.addWidget(self.gaussianGroupBox, 3, 0, 1, 2)
		self.gammaCorrectionGroupBox = QtWidgets.QGroupBox(parent=self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(
			self.gammaCorrectionGroupBox.sizePolicy().hasHeightForWidth()
		)
		self.gammaCorrectionGroupBox.setSizePolicy(sizePolicy)
		self.gammaCorrectionGroupBox.setObjectName("gammaCorrectionGroupBox")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.gammaCorrectionGroupBox)
		self.horizontalLayout.setObjectName("horizontalLayout")
		spacerItem8 = QtWidgets.QSpacerItem(
			150,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout.addItem(spacerItem8)
		self.gammaLabel = QtWidgets.QLabel(parent=self.gammaCorrectionGroupBox)
		self.gammaLabel.setObjectName("gammaLabel")
		self.horizontalLayout.addWidget(self.gammaLabel)
		self.gammaSlider = QtWidgets.QSlider(parent=self.gammaCorrectionGroupBox)
		self.gammaSlider.setMinimum(5)
		self.gammaSlider.setMaximum(300)
		self.gammaSlider.setPageStep(25)
		self.gammaSlider.setProperty("value", 220)
		self.gammaSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
		self.gammaSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
		self.gammaSlider.setObjectName("gammaSlider")
		self.horizontalLayout.addWidget(self.gammaSlider)
		self.gammaValue = QtWidgets.QLabel(parent=self.gammaCorrectionGroupBox)
		self.gammaValue.setObjectName("gammaValue")
		self.horizontalLayout.addWidget(self.gammaValue)
		self.applyGammaCorrectionButton = QtWidgets.QPushButton(
			parent=self.gammaCorrectionGroupBox
		)
		self.applyGammaCorrectionButton.setObjectName("applyGammaCorrectionButton")
		self.horizontalLayout.addWidget(self.applyGammaCorrectionButton)
		spacerItem9 = QtWidgets.QSpacerItem(
			150,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout.addItem(spacerItem9)
		self.gridLayout.addWidget(self.gammaCorrectionGroupBox, 2, 0, 1, 2)
		self.meanGroupBox = QtWidgets.QGroupBox(parent=self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.meanGroupBox.sizePolicy().hasHeightForWidth())
		self.meanGroupBox.setSizePolicy(sizePolicy)
		self.meanGroupBox.setObjectName("meanGroupBox")
		self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.meanGroupBox)
		self.horizontalLayout_6.setObjectName("horizontalLayout_6")
		spacerItem10 = QtWidgets.QSpacerItem(
			375,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_6.addItem(spacerItem10)
		self.meanKernelSizeLabel = QtWidgets.QLabel(parent=self.meanGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.meanKernelSizeLabel.sizePolicy().hasHeightForWidth()
		)
		self.meanKernelSizeLabel.setSizePolicy(sizePolicy)
		self.meanKernelSizeLabel.setObjectName("meanKernelSizeLabel")
		self.horizontalLayout_6.addWidget(self.meanKernelSizeLabel)
		self.meanKernelSizeSpinBox = QtWidgets.QSpinBox(parent=self.meanGroupBox)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
		)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.meanKernelSizeSpinBox.sizePolicy().hasHeightForWidth()
		)
		self.meanKernelSizeSpinBox.setSizePolicy(sizePolicy)
		self.meanKernelSizeSpinBox.setContextMenuPolicy(
			QtCore.Qt.ContextMenuPolicy.DefaultContextMenu
		)
		self.meanKernelSizeSpinBox.setMinimum(3)
		self.meanKernelSizeSpinBox.setMaximum(15)
		self.meanKernelSizeSpinBox.setSingleStep(2)
		self.meanKernelSizeSpinBox.setProperty("value", 5)
		self.meanKernelSizeSpinBox.setObjectName("meanKernelSizeSpinBox")
		self.horizontalLayout_6.addWidget(self.meanKernelSizeSpinBox)
		self.applyMeanButton = QtWidgets.QPushButton(parent=self.meanGroupBox)
		self.applyMeanButton.setObjectName("applyMeanButton")
		self.horizontalLayout_6.addWidget(self.applyMeanButton)
		spacerItem11 = QtWidgets.QSpacerItem(
			375,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_6.addItem(spacerItem11)
		self.gridLayout.addWidget(self.meanGroupBox, 6, 0, 1, 2)
		self.sepiaGroupBox = QtWidgets.QGroupBox(parent=self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(
			self.sepiaGroupBox.sizePolicy().hasHeightForWidth()
		)
		self.sepiaGroupBox.setSizePolicy(sizePolicy)
		self.sepiaGroupBox.setObjectName("sepiaGroupBox")
		self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.sepiaGroupBox)
		self.horizontalLayout_8.setObjectName("horizontalLayout_8")
		spacerItem12 = QtWidgets.QSpacerItem(
			150,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_8.addItem(spacerItem12)
		self.sepiaGammaLabel = QtWidgets.QLabel(parent=self.sepiaGroupBox)
		self.sepiaGammaLabel.setObjectName("sepiaGammaLabel")
		self.horizontalLayout_8.addWidget(self.sepiaGammaLabel)
		self.sepiaGammaSlider = QtWidgets.QSlider(parent=self.sepiaGroupBox)
		self.sepiaGammaSlider.setMinimum(5)
		self.sepiaGammaSlider.setMaximum(300)
		self.sepiaGammaSlider.setPageStep(25)
		self.sepiaGammaSlider.setProperty("value", 100)
		self.sepiaGammaSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
		self.sepiaGammaSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
		self.sepiaGammaSlider.setObjectName("sepiaGammaSlider")
		self.horizontalLayout_8.addWidget(self.sepiaGammaSlider)
		self.sepiaGammaValue = QtWidgets.QLabel(parent=self.sepiaGroupBox)
		self.sepiaGammaValue.setObjectName("sepiaGammaValue")
		self.horizontalLayout_8.addWidget(self.sepiaGammaValue)
		self.applySepiaButton = QtWidgets.QPushButton(parent=self.sepiaGroupBox)
		self.applySepiaButton.setObjectName("applySepiaButton")
		self.horizontalLayout_8.addWidget(self.applySepiaButton)
		spacerItem13 = QtWidgets.QSpacerItem(
			150,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_8.addItem(spacerItem13)
		self.gridLayout.addWidget(self.sepiaGroupBox, 7, 0, 1, 1)
		self.HEGroupBox = QtWidgets.QGroupBox(parent=self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.HEGroupBox.sizePolicy().hasHeightForWidth())
		self.HEGroupBox.setSizePolicy(sizePolicy)
		self.HEGroupBox.setObjectName("HEGroupBox")
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.HEGroupBox)
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		spacerItem14 = QtWidgets.QSpacerItem(
			250,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_5.addItem(spacerItem14)
		self.applyHEButton = QtWidgets.QPushButton(parent=self.HEGroupBox)
		self.applyHEButton.setObjectName("applyHEButton")
		self.horizontalLayout_5.addWidget(self.applyHEButton)
		spacerItem15 = QtWidgets.QSpacerItem(
			250,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_5.addItem(spacerItem15)
		self.gridLayout.addWidget(self.HEGroupBox, 5, 0, 1, 2)
		self.sobelGroupBox = QtWidgets.QGroupBox(parent=self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Policy.Preferred,
			QtWidgets.QSizePolicy.Policy.Preferred,
		)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(
			self.sobelGroupBox.sizePolicy().hasHeightForWidth()
		)
		self.sobelGroupBox.setSizePolicy(sizePolicy)
		self.sobelGroupBox.setObjectName("sobelGroupBox")
		self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.sobelGroupBox)
		self.horizontalLayout_9.setObjectName("horizontalLayout_9")
		spacerItem16 = QtWidgets.QSpacerItem(
			250,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_9.addItem(spacerItem16)
		self.applySobelButton = QtWidgets.QPushButton(parent=self.sobelGroupBox)
		self.applySobelButton.setObjectName("applySobelButton")
		self.horizontalLayout_9.addWidget(self.applySobelButton)
		spacerItem17 = QtWidgets.QSpacerItem(
			250,
			20,
			QtWidgets.QSizePolicy.Policy.Expanding,
			QtWidgets.QSizePolicy.Policy.Minimum,
		)
		self.horizontalLayout_9.addItem(spacerItem17)
		self.gridLayout.addWidget(self.sobelGroupBox, 8, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 26))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)

		self.loadImageButton.clicked.connect(self.open_image_dialog)
		self.AGCminimumSlider.valueChanged["int"].connect(
			self.set_AGC_minimum_range_value
		)
		self.AGCmaximumSlider.valueChanged["int"].connect(
			self.set_AGC_maximimum_range_value
		)
		self.gammaSlider.valueChanged["int"].connect(self.set_gamma_value)
		self.gaussianRadiusSlider.valueChanged["int"].connect(
			self.set_gaussian_radius_value
		)
		self.sepiaGammaSlider.valueChanged["int"].connect(self.set_sepia_gamma_value)
		self.algorithmsComboBox.currentTextChanged["QString"].connect(
			self.update_settings_layout
		)

		self.applyAGCButton.clicked.connect(self.apply_adaptive_gamma_correction)
		self.applyGammaCorrectionButton.clicked.connect(self.apply_gamma_correction)
		self.applyGaussianBlurButton.clicked.connect(self.apply_gaussian_blur)
		self.applyHEButton.clicked.connect(self.apply_histogram_equalization)
		self.applyMeanButton.clicked.connect(self.apply_mean_blur)
		self.applySepiaButton.clicked.connect(self.apply_sepia_filter)
		self.applySobelButton.clicked.connect(self.apply_sobel_edge_detection)

		# NEW: Connect the compare button
		self.compareButton.clicked.connect(self.compare_serial_parallel)

		self.AGCGroupBox.show()
		self.gammaCorrectionGroupBox.hide()
		self.gaussianGroupBox.hide()
		self.HEGroupBox.hide()
		self.meanGroupBox.hide()
		self.sepiaGroupBox.hide()
		self.sobelGroupBox.hide()
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
			pixmap = QPixmap(fileName)
			self.originalImageLabel.setPixmap(
				pixmap.scaled(
					487, 360, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
				)
			)
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

	# ============ NEW: Serial vs Parallel comparison ============
	def compare_serial_parallel(self):
		"""Run both serial and parallel versions, display outputs and timings."""
		try:
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

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(
			_translate("MainWindow", "Image Processing Algorithms Visualiser")
		)
		self.loadImageButton.setStatusTip(
			_translate("MainWindow", "Load an image from drive.")
		)
		self.loadImageButton.setText(_translate("MainWindow", "Load Image"))
		self.selectAlgorithmLabel.setText(
			_translate("MainWindow", "Select an algorithm:")
		)
		self.algorithmsComboBox.setStatusTip(
			_translate(
				"MainWindow", "Select an image processing algorithm to showcase."
			)
		)
		self.algorithmsComboBox.setItemText(
			0, _translate("MainWindow", "Adaptive Gamma Correction")
		)
		self.algorithmsComboBox.setItemText(
			1, _translate("MainWindow", "Gamma Correction")
		)
		self.algorithmsComboBox.setItemText(
			2, _translate("MainWindow", "Gaussian Blur")
		)
		self.algorithmsComboBox.setItemText(
			3, _translate("MainWindow", "Histogram Equalization")
		)
		self.algorithmsComboBox.setItemText(4, _translate("MainWindow", "Mean Blur"))
		self.algorithmsComboBox.setItemText(5, _translate("MainWindow", "Sepia Filter"))
		self.algorithmsComboBox.setItemText(
			6, _translate("MainWindow", "Sobel Edge Detection")
		)
		self.blockSizeLabel.setText(_translate("MainWindow", "Block size:"))
		self.AGCminimumLabel.setText(_translate("MainWindow", "Minimum:"))
		self.AGCmaximumLabel.setText(_translate("MainWindow", "Maximum:"))
		self.AGCgammaRangeLabel.setText(_translate("MainWindow", "Gamma range"))
		self.AGCminimumRangeValue.setText(_translate("MainWindow", "0.5"))
		self.AGCmaximumRangeValue.setText(_translate("MainWindow", "2.0"))
		self.applyAGCButton.setText(_translate("MainWindow", "Apply"))
		self.gaussianKernelSizeLabel.setText(_translate("MainWindow", "Kernel size:"))
		self.gaussianRadiusLabel.setText(_translate("MainWindow", "Radius:"))
		self.gaussianRadiusValue.setText(_translate("MainWindow", "1.0"))
		self.applyGaussianBlurButton.setText(_translate("MainWindow", "Apply"))
		self.gammaLabel.setText(_translate("MainWindow", "Gamma:"))
		self.gammaValue.setText(_translate("MainWindow", "2.2"))
		self.applyGammaCorrectionButton.setText(_translate("MainWindow", "Apply"))
		self.meanKernelSizeLabel.setText(_translate("MainWindow", "Kernel size:"))
		self.applyMeanButton.setText(_translate("MainWindow", "Apply"))
		self.sepiaGammaLabel.setText(_translate("MainWindow", "Gamma:"))
		self.sepiaGammaValue.setText(_translate("MainWindow", "1.0"))
		self.applySepiaButton.setText(_translate("MainWindow", "Apply"))
		self.applyHEButton.setText(_translate("MainWindow", "Apply"))
		self.applySobelButton.setText(_translate("MainWindow", "Apply"))

		# NEW translations
		self.compareButton.setText(
			_translate("MainWindow", "Compare Serial vs Parallel")
		)
		self.timeLabel.setText(_translate("MainWindow", ""))


if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon("src/gui/icon.png"))
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec())
