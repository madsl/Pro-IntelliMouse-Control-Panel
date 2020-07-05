import hid
import sys

class IntelliMouse():
	__VID = 0x045E
	__PID = 0x082A

	__DISTANCE_WRITE_PROPERTY  = 0xB8
	__DISTANCE_READ_PROPERTY  = __DISTANCE_WRITE_PROPERTY - 0x02
	__POLLING_WRITE_PROPERTY = 0x83
	__POLLING_READ_PROPERTY = __POLLING_WRITE_PROPERTY + 0x01
	__COLOR_WRITE_PROPERTY = 0xB2
	__COLOR_READ_PROPERTY = __COLOR_WRITE_PROPERTY + 0x01
	__DPI_WRITE_PROPERTY = 0x96
	__DPI_READ_PROPERTY = __DPI_WRITE_PROPERTY + 0x01

	__POLLING_MAPPING = { 0x02: 125, 0x01: 500, 0x00: 1000}
	__POLLING_MAPPING_INVERSE = dict(zip(__POLLING_MAPPING.values(), __POLLING_MAPPING.keys()))

	__DISTANCE_MAPPING = { 0x00: 2, 0x01: 3 }
	__DISTANCE_MAPPING_INVERSE = dict(zip(__DISTANCE_MAPPING.values(), __DISTANCE_MAPPING.keys()))

	__WRITE_REPORT_ID = 0x24
	__WRITE_REPORT_LENGTH = 0x49
	__READ_REPORT_ID = 0x27
	__READ_REPORT_LENGTH = 0x29

	__INTERFACE = 0x01
	__USAGE_PAGE = 0xFF07
	__USAGE = 0x212

	def __init__(self):
		self.__device = hid.device()
		paths = [path for path in hid.enumerate(self.__VID, self.__PID) if path.get("interface_number") == self.__INTERFACE]
		if not paths:
			raise ValueError("couldn't find the intellimouse...")
		self.__device.open_path(paths[0]["path"])

	def __del__(self):
		self.__device.close()

	def __str__(self):
		return ("Microsoft Pro IntelliMouse \n" +
				"* color: {}\n" +
				"* dots per inch: {}\n" +
				"* polling rate: {}\n" +
				"* lift off distance: {}").format(
					hex(self.get_color()).upper(),
					self.get_dpi(),
					self.get_polling_rate(),
					self.get_lift_off_distance())

	def __write_property(self, property, data):
		if not isinstance(property, int):
			raise TypeError("please make sure to pass a integer for the property argument...")
		if not isinstance(data, list) or not all(isinstance(x, int) for x in data):
			raise TypeError("please make sure to pass a list of integers for the data argument...")
		report = self.__pad_right([self.__WRITE_REPORT_ID, property, len(data)] + data, self.__WRITE_REPORT_LENGTH)
		bytes_written = self.__device.send_feature_report(report)
		if bytes_written != self.__WRITE_REPORT_LENGTH:
			raise IOError("couldn't properly write to device, it may be detached")

	def __read_property(self, property):
		if not isinstance(property, int):
			raise TypeError("please make sure to pass a integer for the property argument...")
		report = self.__pad_right([self.__WRITE_REPORT_ID, property], self.__WRITE_REPORT_LENGTH)
		self.__device.send_feature_report(report)
		result = self.__device.get_input_report(self.__READ_REPORT_ID, self.__READ_REPORT_LENGTH)
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
		return int.from_bytes(self.__read_property(self.__COLOR_READ_PROPERTY), byteorder='big')

	def set_color(self, color):
		if not isinstance(color, int):
			raise TypeError("please make sure to pass an integer...")
		color = 0xFFFFFF & color
		self.__write_property(self.__COLOR_WRITE_PROPERTY, list(color.to_bytes(3, byteorder="big")))

	def get_dpi(self):
		return int.from_bytes(self.__read_property(self.__DPI_READ_PROPERTY), byteorder='little')

	def set_dpi(self, dpi):
		if not isinstance(dpi, int):
			raise TypeError("please make sure to pass an integer...")
		if dpi % 50 != 0 or not (dpi >= 200 and dpi <= 16000):
  			raise ValueError("please make sure to pass a valid value (dpi % 50 == 0 and (dpi >= 200 and dpi <= 16000))")
		self.__write_property(self.__DPI_WRITE_PROPERTY, list(dpi.to_bytes(2, byteorder="little")))

	def get_polling_rate(self):
		return self.__POLLING_MAPPING[self.__read_property(self.__POLLING_READ_PROPERTY)[0]]

	def set_polling_rate(self, rate):
		if not isinstance(rate, int):
			raise TypeError("please make sure to pass an integer...")
		if rate != 125 and rate != 500 and rate != 1000:
			raise ValueError("please make sure to pass a valid value (rate == 125 or rate == 500 or rate == 1000)")
		self.__write_property(self.__POLLING_WRITE_PROPERTY, [self.__POLLING_MAPPING_INVERSE[rate]])

	def get_lift_off_distance(self):
		return self.__DISTANCE_MAPPING[self.__read_property(self.__DISTANCE_READ_PROPERTY)[0]]

	def set_lift_off_distance(self, distance):
		if not isinstance(distance, int):
			raise TypeError("please make sure to pass an integer...")
		if distance != 2 and distance != 3:
			raise ValueError("please make sure to pass a valid lift off distance (distance == 2 or distance == 3)")
		self.__write_property(self.__DISTANCE_WRITE_PROPERTY, [self.__DISTANCE_MAPPING_INVERSE[distance]])
