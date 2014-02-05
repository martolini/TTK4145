from schlang import *
from channels import INPUT, OUTPUT


class IOException(Exception):
	def __init__(self, value, error=None, errno=-1):
		self.value = value
		self.error = error
		self.errno = errno

	def __str__(self):
		return repr(self.value+ ' (' + self.error+').')


class IO:
	def __init__(self):
		self.status = 0
		self.it_g = POINTER(comedi_t)
		self.it_g = comedi_open("/dev/comedi0")
		if not self.it_g:
			raise IOException('Could not connect to elevator')

		for i in xrange(8):
			self.status |= comedi_dio_config(self.it_g, INPUT.PORT1, i, COMEDI_INPUT)
			self.status |= comedi_dio_config(self.it_g, OUTPUT.PORT2, i, COMEDI_OUTPUT)
			self.status |= comedi_dio_config(self.it_g, OUTPUT.PORT3, i+8, COMEDI_OUTPUT)
			self.status |= comedi_dio_config(self.it_g, INPUT.PORT4, i+16, COMEDI_INPUT)
		if self.status < 0:
			raise IOException('Status nonzero after init')

	def set_bit(self, channel, value):
		if value != 0 or value != 1:
			raise IOException("Tried to set value %d to channel %d" % (value, channel))
		if comedi_dio_write(self.it_g, channel >> 8, channel & 0xff, value) < 0:
			raise IOException("Could not write value %d to channel %d" % (value, channel))

	def write_analog(self, channel, value):
		if comedi_data_write(self.it_g, channel >> 8, channel & 0xff, 0, AREF_GROUND, value) < 0:
			raise IOException("Could not write value %d to channel %d" % (value, channel))

	def read_bit(self, channel):
		data = lsampl_t()
		retval = comedi_dio_read(self.it_g, channel >> 8, channel & 0xff, byteref(data))
		if retval < 0:
			raise IOException("Could not read from channel %d" % channel)
		return data

	def read_analog(self, channel):
		data = lsampl_t()
		reval = comedi_data_read(self.it_g, channel >> 8, channel & 0xff, 0, AREF_GROUND, byteref(data))
		if retval < 0:
			raise IOException("Could not read from analog channel %d" % channel)
		return data

io = IO()

	
