from channels import INPUT, OUTPUT
from IO import io
from time import sleep

class Elevator():
	def __init__(self):
		self.direction = OUTPUT.MOTOR_DOWN
		self.moving = False

		for light in OUTPUT.LIGHTS:
			io.set_bit(light, 0)

	def set_speed(self, speed):
		if speed > 0:
			self.direction = OUTPUT.MOTOR_UP
		else if speed < 0:
			self.direction = OUTPUT.MOTOR_DOWN
		else:
			self.stop()

		io.set_bit(OUTPUT.MOTORDIR, self.direction)
		io.write_analog(OUTPUT.MOTOR, 2048+4*abs(speed))
		self.moving = True

	def stop(self):
		if not self.moving:
			return
		if self.direction is OUTPUT.MOTOR_UP:
			io.set_bit(OUTPUT.MOTORDIR, OUTPUT.MOTOR_DOWN)
		else:
			io.set_bit(OUTPUT.MOTORDIR, OUTPUT.MOTOR_UP)

		sleep(0.02)
		io.write_analog(OUTPUT.MOTOR, 2048)

