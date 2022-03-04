from time import sleep
from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

SERVO_A_PIN = 12
SERVO_B_PIN = 13
SERVO_C_PIN = 18

Device.pin_factory = PiGPIOFactory()
servoA = AngularServo(SERVO_A_PIN, 136, 0, 180, 0.5/1000, 2.5/1000)
servoB = AngularServo(SERVO_B_PIN, 9, 0, 180, 0.5/1000, 2.5/1000)
servoC = AngularServo(SERVO_C_PIN, 120, 0, 120, 0.9/1000, 2.1/1000)


def SetA(angle):
	servoA.angle = angle + 7


def SetB(angle):
	servoB.angle = 180 - max(17, angle + 9)


def SetC(isDown):
	servoC.angle = 100 if isDown else 120
	sleep(0.1)
	servoC.angle = None


def cleanup():
	servoA.angle = None
	servoB.angle = None
	servoC.angle = None

SetA(0)
SetB(0)
SetC(False)

cleanup()




# ===
SetA(0); SetB(0)

# ===
SetA(2); SetB(48)

# ===
SetA(86); SetB(142)

SetA(142); SetB(38)