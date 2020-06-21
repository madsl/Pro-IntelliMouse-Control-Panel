from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from intellimouse import IntelliMouse
import sys

class QIntModuloValidator(QIntValidator):
	def __init__(self, modulo, *args, **kwargs):
		self.modulo = modulo
		super(QIntModuloValidator, self).__init__(*args, **kwargs)

	def validate(self, text, position):
		if super().validate(text, position)[0] == QValidator.Acceptable and int(text) % self.modulo == 0:
			return (QValidator.Acceptable, text, position)
		return (QValidator.Invalid, text, position)


class MainWindow(QWidget):
	def __init__(self, ctx):
		super().__init__()
		self.applicationContext = ctx

		try:
			self.mouse = IntelliMouse()
			self.changeLayout(self.createConfigurationLayout())
		except:
			self.changeLayout(self.createErrorLayout())

	def changeLayout(self, new):
		if self.layout() is not None:
			for i in reversed(range(self.layout().count())):
				layout = self.layout().takeAt(i)
				self.clearLayout(layout)
				if isinstance(layout, QWidgetItem):
					if layout.widget() is not None:
						layout.widget().deleteLater()
				else:
					layout.setParent(None)
			self.layout().insertLayout(0, new)
		else:
			self.setLayout(new)

	def clearLayout(self, layout):
		if layout is not None:
			if isinstance(layout, QWidget):
				layout.setParent(None)
			if isinstance(layout, QWidgetItem):
				layout.widget().setParent(None)
			else:
				for i in reversed(range(layout.count())):
					item = layout.itemAt(i)
					if item.widget() is not None:
						item.widget().setParent(None)
					else:
						self.clearLayout(item.layout())

	def onColorButtonPushed(self):
		try:
			color = QColorDialog.getColor(QColor.fromRgb(self.mouse.get_color()))
			if color.isValid():
				self.mouse.set_color(int(color.rgb()))
		except:
			self.changeLayout(self.createErrorLayout())

	def onPollingRateChanged(self):
		try:
			self.mouse.set_polling_rate(int(self.pollingComboBox.currentText()))
		except:
			self.changeLayout(self.createErrorLayout())

	def onDistanceChanged(self):
		try:
			self.mouse.set_lift_off_distance(int(self.distanceComboBox.currentText()))
		except:
			self.changeLayout(self.createErrorLayout())

	def onDpiSliderChanged(self, increments):
		try:
			nearest = increments * round(self.dpiSLider.value() / increments)
			self.dpiSLider.setValue(nearest)
			self.dpiSLider.setSliderPosition(nearest)
			self.dpiLineEdit.setText(str(nearest))
			self.mouse.set_dpi(nearest)
		except:
			self.changeLayout(self.createErrorLayout())

	def onDpiLineEditChanged(self):
		try:
			self.dpiSLider.setValue(int(self.dpiLineEdit.text()))
		except:
			self.changeLayout(self.createErrorLayout())

	def onRetryButtonPressed(self):
		try:
			self.mouse = IntelliMouse()
			self.changeLayout(self.createConfigurationLayout())
		except:
			self.changeLayout(self.createErrorLayout())

	def createErrorLayout(self):
		main = QVBoxLayout()

		image = QPixmap(self.applicationContext.get_resource('error.png')).scaled(128, 128)
		imageLabel = QLabel()
		imageLabel.setPixmap(image)
		imageLabel.setAlignment(Qt.AlignCenter)

		explanationLabel = QLabel('something went wrong \nor the mouse isn\'t currently connected...')
		explanationLabel.setAlignment(Qt.AlignCenter)

		self.retryButton = QPushButton('retry')
		self.retryButton.clicked.connect(lambda: self.onRetryButtonPressed())

		main.addWidget(imageLabel)
		main.addWidget(explanationLabel)
		main.addWidget(self.retryButton)
		main.setSizeConstraint(QLayout.SetFixedSize)
		return main

	def createConfigurationLayout(self):
		colorButton = QPushButton('set LED color')
		colorButton.setToolTip('sets the LED color')
		self.colorButton = colorButton
		colorButton.clicked.connect(lambda: self.onColorButtonPushed())

		pollingComboBox = QComboBox()
		pollingComboBox.setToolTip('sets the polling rate in Hz')
		pollingComboBox.addItems(["125", "500", "1000"])
		try:
			pollingComboBox.setCurrentIndex(pollingComboBox.findText(str(self.mouse.get_polling_rate())))
		except:
			self.changeLayout(self.createErrorLayout())
		self.pollingComboBox = pollingComboBox
		pollingComboBox.activated.connect(lambda: self.onPollingRateChanged())


		distanceComboBox = QComboBox()
		distanceComboBox.setToolTip('sets the lift of distance in mm')
		distanceComboBox.addItems(["2", "3"])
		try:
			distanceComboBox.setCurrentIndex(distanceComboBox.findText(str(self.mouse.get_lift_off_distance())))
		except:
			self.changeLayout(self.createErrorLayout())
		self.distanceComboBox = distanceComboBox
		distanceComboBox.activated.connect(lambda: self.onDistanceChanged())


		dpiSLider = QSlider()
		dpiSLider.setToolTip('sets the dots per inch')
		dpiSLider.setRange(200, 16000)
		dpiSLider.setOrientation(Qt.Horizontal)
		try:
			dpiSLider.setSliderPosition(self.mouse.get_dpi())
		except:
			self.changeLayout(self.createErrorLayout())
		dpiSLider.valueChanged.connect(lambda: self.onDpiSliderChanged(50))
		self.dpiSLider = dpiSLider

		dpiLineEdit = QLineEdit()
		dpiLineEdit.setToolTip('sets the dots per inch')
		dpiLineEdit.setValidator(QIntModuloValidator(50, 200, 16000))
		try:
			dpiLineEdit.insert(str(self.mouse.get_dpi()))
		except:
			self.changeLayout(self.createErrorLayout())
		dpiLineEdit.textEdited.connect(lambda: self.onDpiLineEditChanged())
		self.dpiLineEdit = dpiLineEdit

		dpiGroupBox = QGroupBox("dots per inch")
		dpiGroupBoxLayout = QVBoxLayout()
		dpiGroupBoxLayout.addWidget(dpiSLider)
		dpiGroupBoxLayout.addWidget(dpiLineEdit)
		dpiGroupBox.setLayout(dpiGroupBoxLayout)

		colorGroupBox = QGroupBox("color")
		colorGroupBoxLayout = QVBoxLayout()
		colorGroupBoxLayout.addWidget(colorButton)
		colorGroupBox.setLayout(colorGroupBoxLayout)

		distanceGroupBox = QGroupBox("lift off distance")
		distanceGroupBoxLayout = QVBoxLayout()
		distanceGroupBoxLayout.addWidget(distanceComboBox)
		distanceGroupBox.setLayout(distanceGroupBoxLayout)

		pollingGroupBox = QGroupBox("polling rate")
		pollingGroupBoxLayout = QVBoxLayout()
		pollingGroupBoxLayout.addWidget(pollingComboBox)
		pollingGroupBox.setLayout(pollingGroupBoxLayout)

		main = QVBoxLayout()
		upper = QHBoxLayout()
		upper.addWidget(colorGroupBox)
		upper.addWidget(dpiGroupBox)
		lower = QHBoxLayout()
		lower.addWidget(pollingGroupBox)
		lower.addWidget(distanceGroupBox)

		main.addLayout(upper)
		main.addLayout(lower)
		main.setSizeConstraint(QLayout.SetFixedSize)
		return main



if __name__ == '__main__':
	applicationContext = ApplicationContext()
	window = MainWindow(applicationContext)
	window.show()
	exit_code = applicationContext.app.exec_()
	sys.exit(exit_code)
