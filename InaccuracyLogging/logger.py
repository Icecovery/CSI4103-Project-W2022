from ..HardwareControl.controller import Controller
from InverseKinematics.convert import coordinate_to_angle

def main():
	# input variables
	xlength = int(input("Enter X dimension of grid (mm): "))
	ylength = int(input("Enter Y dimension of grid (mm): "))
	xresolution = int(input("Enter X resolution of grid: "))
	yresolution = int(input("Enter Y resolution of grid: "))

	# output variables
	offsets = []

	# calculate distance between points
	xinterval = xlength / (xresolution - 1)
	yinterval = ylength / (yresolution - 1)

	# configure hardware
	controller = Controller()

	for y in range(yresolution):
		xoffsets = []
		for x in range(xresolution):
			# convert point coords to angles for servos
			xpos = x * xinterval
			ypos = y * yinterval
			angles = coordinate_to_angle(xpos, ypos, 160, 150)

			# move brachigraph
			controller.servo_c(False)
			controller.servo_a(angles[0])
			controller.servo_b(angles[1])
			controller.servo_c(True)

			# prompt user fo offsets
			print("Point = (" + str(x) + ", " + str(y) + ")")
			print("Expected position = (" + str(xpos) + +", " + str(ypos) + ")")
			xoffset = float(input("Enter X offset for point: "))
			yoffset = float(input("Enter Y offset for point: "))
			xoffsets.append([xoffset, yoffset])
		offsets.append(xoffsets)
		
main()