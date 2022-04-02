from time import sleep
from gpiozero import Device, AngularServo, Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory
import progressbar

# PWM pins
# GPIO12 - PWM0 - Servo A
# GPIO13 - PWM1 - Servo B
# GPIO18 - PWM0 - Servo C

SERVO_A_PIN = 12
SERVO_B_PIN = 13
SERVO_C_PIN = 18
BUZZER_PIN = 23

# MG995 (Servo A and B)
# Angle range: 0 - 180 deg
# Pulse width: 500 - 2500 us
# Duty cycle: 2.5 - 12.5%

# SG90 (Servo C)
# Angle range: 0 - 120 deg
# Pulse width: 900 - 2100 us
# Duty cycle: 4.5 - 10.5%

class Controller:
	'''
		This class is used to controll the servos.
	'''

	def __init__(self):
		# https://gpiozero.readthedocs.io/en/stable/api_pins.html#changing-pin-factory
		# use Pi GPIO pin factory to increse accuracy
		Device.pin_factory = PiGPIOFactory()

		# init the buzzer to enable the warning beep
		self.buzzer = Buzzer(BUZZER_PIN)
		self._warning()

		# set up the servos
		self.servo_a = AngularServo(SERVO_A_PIN, 136, 0, 180, 0.5/1000, 2.5/1000)
		self.servo_b = AngularServo(SERVO_B_PIN, 9, 0, 180, 0.5/1000, 2.5/1000)
		self.servo_c = AngularServo(SERVO_C_PIN, 120, 0, 120, 0.9/1000, 2.1/1000)

	def _warning(self):
		self.buzzer.beep(0.1, 0.1, 2, True)
		sleep(1)
		self.buzzer.beep(0.1, 0.1, 2, True)
		sleep(1)
		self.buzzer.beep(1, 3, 1, True)
		sleep(2)

	def _set_servo_a(self, angle):
		# servo A "0 degree": 0 deg
		self.servo_a.angle = angle

	def _set_servo_b(self, angle):
		# servo B dead zone: 163
		# servo B "0 degree": 9 deg
		# reversed
		self.servo_b.angle = min(163, 180 - angle - 9)

	def _set_servo_c(self, isDown):
		self.servo_c.angle = 100 if isDown else 120

		# disable after movement to stop it from making noise
		sleep(0.1)
		self.servo_c.angle = None
	
	def _reset_servos(self):
		self._set_servo_a(0)
		self._set_servo_b(0)
		self._set_servo_c(False)

	def clean_up(self):
		self.servo_a.angle = None
		self.servo_b.angle = None
		self.servo_c.angle = None

	def draw(self, instructions):
		'''
			Use angles to control the servos to move the arms and pen to draw.
		'''

		print("Drawing...")

		for instruction in progressbar.progressbar(instructions):
			if (type(instruction) is bool): # servo C command
				self._set_servo_c(instruction)
			elif (type(instruction) is tuple): # servo A and B command
				self._set_servo_a(instruction[0])
				self._set_servo_b(instruction[1])
			elif (type(instruction) is float): # delay command
				sleep(instruction)
			else:
				raise NotImplementedError
		
		sleep(1)
		
		self._reset_servos()
		sleep(1)

		print("Complete")
