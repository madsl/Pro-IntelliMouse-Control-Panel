import usb.core
import usb.util

VID = 0x045E
PID = 0x082A

DISTANCE_WRITE_PROPERTY  = 0xB8
DISTANCE_READ_PROPERTY  = DISTANCE_WRITE_PROPERTY - 0x02
POLLING_WRITE_PROPERTY = 0x83
POLLING_READ_PROPERTY = POLLING_WRITE_PROPERTY + 0x01
COLOR_WRITE_PROPERTY = 0xB2
COLOR_READ_PROPERTY = COLOR_WRITE_PROPERTY + 0x01
DPI_WRITE_PROPERTY = 0x96
DPI_READ_PROPERTY = DPI_WRITE_PROPERTY + 0x01

POLLING_MAPPING = { 0x02: 125, 0x01: 500, 0x00: 1000}
POLLING_MAPPING_INVERSE = dict(zip(POLLING_MAPPING.values(), POLLING_MAPPING.keys()))

DISTANCE_MAPPING = { 0x00: 2, 0x01: 3 }
DISTANCE_MAPPING_INVERSE = dict(zip(DISTANCE_MAPPING.values(), DISTANCE_MAPPING.keys()))

WRITE_REPORT_ID = 0x24
WRITE_REPORT_LENGTH = 0x49
READ_REPORT_ID = 0x27
READ_REPORT_LENGTH = 0x29

INTERFACE = 0x01

class IntelliMouse():
	def __init__(self):
		self.device = usb.core.find(idVendor=VID, idProduct=PID)
		if self.device is None:
		    raise ValueError("couldn't find the intellimouse...")
		self.device.set_configuration()

	def __write_property(self, property, data):
		if not isinstance(property, int):
			raise TypeError("please make sure to pass a integer for the property argument...")
		if not isinstance(data, list) or not all(isinstance(x, int) for x in data):
			raise TypeError("please make sure to pass a list of integers for the data argument...")
		report = self.__pad_right([WRITE_REPORT_ID, property, len(data)] + data, WRITE_REPORT_LENGTH)
		self.device.ctrl_transfer(0x21, 0x09, 0x03 << 8 | WRITE_REPORT_ID, INTERFACE, report)

	def __read_property(self, property):
		if not isinstance(property, int):
			raise TypeError("please make sure to pass a integer for the property argument...")
		report = self.__pad_right([WRITE_REPORT_ID, property], WRITE_REPORT_LENGTH)
		self.device.ctrl_transfer(0x21, 0x09, 0x03 << 8 | WRITE_REPORT_ID, INTERFACE, report)
		result = list(self.device.ctrl_transfer(0xA1, 0x01, 0x01 << 8 | READ_REPORT_ID, INTERFACE, READ_REPORT_LENGTH))
		return result[4 : 4 + result[3]]

	def __pad_right(self, data, until):
		if not isinstance(data, list) or not all(isinstance(x, int) for x in data):
			raise TypeError("please make sure to pass a list of integers for the data argument...")
		if not isinstance(until, int):
			raise TypeError("please make sure to pass a integer for the until argument...")
		if until <= 0:
			raise ValueError("please pass a positive integer for the until argument...")
		if len(data) >= until:
			return
		return data + ((until - len(data)) * [0x00])

	def get_color(self):
		return int.from_bytes(self.__read_property(COLOR_READ_PROPERTY), byteorder='big')

	def set_color(self, color):
		if not isinstance(color, int):
			raise TypeError("please make sure to pass an integer...")
		color = 0xFFFFFF & color
		self.__write_property(COLOR_WRITE_PROPERTY, list(color.to_bytes(3, byteorder="big")))

	def get_dpi(self):
		return int.from_bytes(self.__read_property(DPI_READ_PROPERTY), byteorder='little')

	def set_dpi(self, dpi):
		if not isinstance(dpi, int):
			raise TypeError("please make sure to pass an integer...")
		if dpi % 50 != 0 or not (dpi >= 200 and dpi <= 16000):
  			raise ValueError("please make sure to pass a valid value (dpi % 50 == 0 and (dpi >= 200 and dpi <= 16000))")
		self.__write_property(DPI_WRITE_PROPERTY, list(dpi.to_bytes(2, byteorder="little")))

	def get_polling_rate(self):
		return POLLING_MAPPING[self.__read_property(POLLING_READ_PROPERTY)[0]]

	def set_polling_rate(self, rate):
		if not isinstance(rate, int):
			raise TypeError("please make sure to pass an integer...")
		if rate != 125 and rate != 500 and rate != 1000:
			raise ValueError("please make sure to pass a valid value (rate == 125 or rate == 500 or rate == 1000)")
		self.__write_property(POLLING_WRITE_PROPERTY, [POLLING_MAPPING_INVERSE[rate]])

	def get_lift_off_distance(self):
		return DISTANCE_MAPPING[self.__read_property(DISTANCE_READ_PROPERTY)[0]]

	def set_lift_off_distance(self, distance):
		if not isinstance(distance, int):
			raise TypeError("please make sure to pass an integer...")
		if distance != 2 and distance != 3:
			raise ValueError("please make sure to pass a valid lift off distance (distance == 2 or distance == 3)")
		self.__write_property(DISTANCE_WRITE_PROPERTY, [DISTANCE_MAPPING_INVERSE[distance]])
