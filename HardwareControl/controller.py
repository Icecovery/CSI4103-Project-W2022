from time import sleep
from gpiozero import Device, AngularServo, Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory

from constants import SERVO_A_PIN, SERVO_B_PIN, SERVO_C_PIN, BUZZER_PIN

class Controller:

    def __init__(self, la=160, lb=150):
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

        # store the arm length
        self.la = la
        self.lb = lb

    def _warning(self):
        self.buzzer.beep(0.1, 0.1, 2, True)
        sleep(1)

    def _set_servo_a(self, angle):
        # servo A "0 degree": 7 deg
        self.servo_a.angle = angle + 7

    def _set_servo_b(self, angle):
        # servo B dead zone: 163
        # servo B "0 degree": 9 deg
        # reversed
        self.servo_b.angle = max(163, 180 - angle - 9)

    def _set_servo_c(self, isDown):
        self.servo_c.angle = 100 if isDown else 120

        # disable after movement to stop it from making noise
        sleep(0.1)
        self.servo_c.angle = None

    def clean_up(self):
        self.servo_a.angle = None
        self.servo_b.angle = None
        self.servo_c.angle = None

    # main program
    def main(self):

        self._set_servo_a(0)
        self._set_servo_b(0)
        self._set_servo_c(False)

        sleep(1)

        lines = []
        angles = []
        offset_a = 38.69
        offset_b = 0
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

        # calculate angles
        for line in lines:
            # origin angles
            angle_a1, angle_b1 = coordinate_to_angle(line[0], line[1], self.la, self.lb)

            # destination angles
            angle_a2, angle_b2 = coordinate_to_angle(line[2], line[3], self.la, self.lb)

            angle = []
            angle.append(math.degrees(angle_a1) + offset_a)
            angle.append(math.degrees(angle_b1) + offset_b)
            angle.append(math.degrees(angle_a2) + offset_a)
            angle.append(math.degrees(angle_b2) + offset_b)

            angles.append(angle)

        for angle in angles:
            self._set_servo_a(angle[0])
            self._set_servo_b(angle[1])
            sleep(1)
            self._set_servo_c(True)
            self._set_servo_a(angle[2])
            self._set_servo_b(angle[3])
            sleep(1)
            self._set_servo_c(False)

        sleep(1)

        self._set_servo_a(0)
        self._set_servo_b(0)
        self._set_servo_c(False)

        sleep(1)
