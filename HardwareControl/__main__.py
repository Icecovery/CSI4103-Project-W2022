from time import sleep
from gpiozero import Device, AngularServo, Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory
from coordinate_converter import *;
import csv

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

	def setup(self):
		# https://gpiozero.readthedocs.io/en/stable/api_pins.html#changing-pin-factory
		# Use Pi GPIO pin factory to increse accuracy
		# Device.pin_factory = PiGPIOFactory()

		# self.buzzer = Buzzer(BUZZER_PIN)
		# self.warning()

		# self.servoA = AngularServo(SERVO_A_PIN, 136, 0, 180, 0.5/1000, 2.5/1000)
		# self.servoB = AngularServo(SERVO_B_PIN, 9, 0, 180, 0.5/1000, 2.5/1000)
		# self.servoC = AngularServo(SERVO_C_PIN, 120, 0, 120, 0.9/1000, 2.1/1000)
		pass
		

	def warning(self):
		self.buzzer.beep(0.1, 0.1, 2, True)
		sleep(1)

	def SetServoA(self, angle):
		# servo A 0: 7 deg
		self.servoA.angle = angle + 7

	def SetServoB(self, angle):
		# servo B dead zone: 163
		# servo B 0: 9 deg
		# reversed
		self.servoB.angle = 180 - max(17, angle + 9)

	def SetServoC(self, isDown):
		self.servoC.angle = 100 if isDown else 120

		# disable after movement to stop it from making noise
		sleep(0.1)
		self.servoC.angle = None 

	def cleanup(self):
		self.servoA.angle = None
		self.servoB.angle = None
		self.servoC.angle = None

	# main program
	def main(self):
		
		# Testing patten

		# self.SetServoA(0)
		# self.SetServoB(0)
		# self.SetServoC(False)

		# sleep(1)

		lines = []
		angles = []
		offset_a = 38.69
		offset_b = 0
		la = 160
		lb = 150
		src_csv_path = "path.csv" 

		# put vectors from CSV into an array
		with open(src_csv_path, 'r') as file:
			reader = csv.reader(file)
			for row in reader:
				i = 0
				while i < len(row):  # convert vectors from str to int
					row[i] = float(row[i])
					i += 1
				lines.append(row)
		
		print(lines)

		# calculate angles
		# for line in lines:
		# 	# origin angles
		# 	angle_a1, angle_b1 = coordinate_to_angle(line[0], line[1], la, lb)

		# 	# destination angles
		# 	angle_a2, angle_b2 = coordinate_to_angle(line[2], line[3], la, lb)

		# 	angle = []
		# 	angle.append(math.degrees(angle_a1) + offset_a)
		# 	angle.append(math.degrees(angle_b1) + offset_b)
		# 	angle.append(math.degrees(angle_a2) + offset_a)
		# 	angle.append(math.degrees(angle_b2) + offset_b)

		# 	angles.append(angle)

		# for angle in angles:
		# 	self.SetServoA(angle[0])
		# 	self.SetServoB(angle[1])
		# 	sleep(1)
		# 	self.SetServoC(True)
		# 	self.SetServoA(angle[2])
		# 	self.SetServoB(angle[3])
		# 	sleep(1)
		# 	self.SetServoC(False)

		# sleep(1)
		
		# self.SetServoA(0)
		# self.SetServoB(0)
		# self.SetServoC(False)

		# sleep(1)

# main entry point
if __name__ == '__main__':
	try:
		controller = Controller()
		controller.setup()
		controller.main()
	except KeyboardInterrupt:
		pass
	finally:
		if (controller is not None):
			controller.cleanup()
		pass
