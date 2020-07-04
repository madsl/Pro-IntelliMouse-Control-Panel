try:
	from fbs_runtime.application_context.PyQt5 import ApplicationContext
except:
	pass
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from intellimouse import IntelliMouse
import sys
import os

class QIntModuloValidator(QIntValidator):
	def __init__(self, modulo, *args, **kwargs):
		self.modulo = modulo
		super(QIntModuloValidator, self).__init__(*args, **kwargs)

	def validate(self, text, position):
		if super().validate(text, position)[0] == QValidator.Acceptable and int(text) % self.modulo == 0:
			return (QValidator.Acceptable, text, position)
		return (QValidator.Invalid, text, position)

class ErrorWindow(QWidget):
	def __init__(self, path, parent=None):
		super(ErrorWindow, self).__init__(parent)

		self.image = QPixmap(path).scaled(128, 128)
		self.imageLabel = QLabel()
		self.imageLabel.setPixmap(self.image)
		self.imageLabel.setAlignment(Qt.AlignCenter)

		self.explanationLabel = QLabel('something went wrong \nor the mouse isn\'t currently connected...')
		self.explanationLabel.setAlignment(Qt.AlignCenter)

		self.retryButton = QPushButton('retry')

		layout = QVBoxLayout()
		layout.addWidget(self.imageLabel)
		layout.addWidget(self.explanationLabel)
		layout.addWidget(self.retryButton)
		layout.setSizeConstraint(QLayout.SetFixedSize)

		self.setLayout(layout)

class ConfigurationWindow(QWidget):
	def __init__(self, parent=None):
		super(ConfigurationWindow, self).__init__(parent)

		self.colorButton = QPushButton('set LED color')
		self.colorButton.setToolTip('sets the LED color')

		self.pollingComboBox = QComboBox()
		self.pollingComboBox.setToolTip('sets the polling rate in Hz')
		self.pollingComboBox.addItems(["125", "500", "1000"])

		self.distanceComboBox = QComboBox()
		self.distanceComboBox.setToolTip('sets the lift of distance in mm')
		self.distanceComboBox.addItems(["2", "3"])

		self.dpiSlider = QSlider()
		self.dpiSlider.setToolTip('sets the dots per inch')
		self.dpiSlider.setRange(200, 16000)
		self.dpiSlider.setOrientation(Qt.Horizontal)

		self.dpiLineEdit = QLineEdit()
		self.dpiLineEdit.setToolTip('sets the dots per inch')
		self.dpiLineEdit.setValidator(QIntModuloValidator(50, 200, 16000))

		self.dpiGroupBox = QGroupBox("dots per inch")
		self.dpiGroupBoxLayout = QVBoxLayout()
		self.dpiGroupBoxLayout.addWidget(self.dpiSlider)
		self.dpiGroupBoxLayout.addWidget(self.dpiLineEdit)
		self.dpiGroupBox.setLayout(self.dpiGroupBoxLayout)

		self.colorGroupBox = QGroupBox("color")
		self.colorGroupBoxLayout = QVBoxLayout()
		self.colorGroupBoxLayout.addWidget(self.colorButton)
		self.colorGroupBox.setLayout(self.colorGroupBoxLayout)

		self.distanceGroupBox = QGroupBox("lift off distance")
		self.distanceGroupBoxLayout = QVBoxLayout()
		self.distanceGroupBoxLayout.addWidget(self.distanceComboBox)
		self.distanceGroupBox.setLayout(self.distanceGroupBoxLayout)

		self.pollingGroupBox = QGroupBox("polling rate")
		self.pollingGroupBoxLayout = QVBoxLayout()
		self.pollingGroupBoxLayout.addWidget(self.pollingComboBox)
		self.pollingGroupBox.setLayout(self.pollingGroupBoxLayout)

		layout = QVBoxLayout()

		upper = QHBoxLayout()
		upper.addWidget(self.colorGroupBox)
		upper.addWidget(self.dpiGroupBox)
		lower = QHBoxLayout()
		lower.addWidget(self.pollingGroupBox)
		lower.addWidget(self.distanceGroupBox)

		layout.addLayout(upper)
		layout.addLayout(lower)
		layout.setSizeConstraint(QLayout.SetFixedSize)

		self.setLayout(layout)

class MainWindow(QMainWindow):
	def __init__(self, ctx):
		super().__init__()
		self.applicationContext = ctx
		self.showAppropriateLayout()

	def showAppropriateLayout(self):
		try:
			self.mouse = IntelliMouse()
			self.showConfigurationWindow()
		except:
			if not isinstance(self.centralWidget(), ErrorWindow):
				self.showErrorWindow()

	def showErrorWindow(self):
		try:
			self.errorWindow = ErrorWindow(self.applicationContext.get_resource('error.png'), self)
		except:
			self.errorWindow = ErrorWindow(os.path.dirname(os.path.abspath(__file__)) + '/../resources/base/error.png', self)
		self.setCentralWidget(self.errorWindow)
		self.setFixedSize(self.sizeHint())
		self.errorWindow.retryButton.clicked.connect(self.showAppropriateLayout)
		self.show()

	def showConfigurationWindow(self):
		self.configurationWindow = ConfigurationWindow(self)

		self.configurationWindow.pollingComboBox.setCurrentIndex(self.configurationWindow.pollingComboBox.findText(str(self.mouse.get_polling_rate())))
		self.configurationWindow.distanceComboBox.setCurrentIndex(self.configurationWindow.distanceComboBox.findText(str(self.mouse.get_lift_off_distance())))
		self.configurationWindow.dpiLineEdit.insert(str(self.mouse.get_dpi()))
		self.configurationWindow.dpiSlider.setValue(self.mouse.get_dpi())

		def onColorButtonPushed():
			try:
				color = QColorDialog.getColor(QColor.fromRgb(self.mouse.get_color()))
				if color.isValid():
					self.mouse.set_color(int(color.rgb()))
			except:
				self.showErrorWindow()

		self.configurationWindow.colorButton.clicked.connect(lambda: onColorButtonPushed())

		def onPollingRateChanged():
			try:
				self.mouse.set_polling_rate(int(self.configurationWindow.pollingComboBox.currentText()))
			except:
				self.showErrorWindow()

		self.configurationWindow.pollingComboBox.activated.connect(lambda: onPollingRateChanged())

		def onDistanceChanged():
			try:
				self.mouse.set_lift_off_distance(int(self.configurationWindow.distanceComboBox.currentText()))
			except:
				self.showErrorWindow()

		self.configurationWindow.distanceComboBox.activated.connect(lambda: onDistanceChanged())

		def onDpiSliderChanged():
			try:
				nearest = 50 * round(self.configurationWindow.dpiSlider.value() / 50)
				self.configurationWindow.dpiSlider.setValue(nearest)
				self.configurationWindow.dpiSlider.setSliderPosition(nearest)
				self.configurationWindow.dpiLineEdit.setText(str(nearest))
				self.mouse.set_dpi(nearest)
			except:
				self.showErrorWindow()

		self.configurationWindow.dpiSlider.valueChanged.connect(lambda: onDpiSliderChanged())

		def onDpiLineEditChanged():
			try:
				self.configurationWindow.dpiSlider.setValue(int(self.configurationWindow.dpiLineEdit.text()))
			except:
				self.showErrorWindow()

		self.configurationWindow.dpiLineEdit.textEdited.connect(lambda: onDpiLineEditChanged())

		self.setCentralWidget(self.configurationWindow)
		self.setFixedSize(self.sizeHint())
		self.show()

if __name__ == '__main__':
	applicationContext = None
	try:
		applicationContext = ApplicationContext()
	except:
		sys.argv[0] = 'Control Panel for Microsoft IntelliMouse Pro'
		applicationContext = QApplication(sys.argv)
	window = MainWindow(applicationContext)
	exit_code = -1
	try:
		exit_code = applicationContext.app.exec_()
	except:
		exit_code = applicationContext.exec_()
	sys.exit(exit_code)
