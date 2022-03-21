import math
import progressbar

from .device_abstraction import *

def coordinate_to_angle(x, y, la, lb):
	'''
		Get the coordinate of the pen and the lenghs of two arms to calculate
		the angles of the two servos in radians.

		Parameter
		---------
		The value of the parameters are all in millimeter(mm).

		`x`: x coordinate of the pen

		`y`: y coordinate of the pen

		`la`: the length of the arm a

		`lb`: the length of the arm b
	'''
	ac = math.sqrt(x ** 2 + y ** 2)
	bac = math.acos((la ** 2 + ac ** 2 - lb ** 2) / (2.0 * la * ac))
	yac = math.asin(x / ac)
	yab = (math.pi - yac - bac) if y > 0 else (yac - bac)

	angle_a = yab
	angle_b = math.acos((la ** 2 + lb ** 2 - ac ** 2) / (2.0 * la * lb))

	return (angle_a, angle_b)

def lines_to_angles(lines):
	'''
		@brief Convert line segments produced by ImageProcessing module to the angles
		which are used to control the servos.
	'''
	print("Converting lines to angles...")

	instructions = []
	
	for line in progressbar.progressbar(lines):
		start, end = line

		# move to start instruction
		angle_a, angle_b = coordinate_to_angle(start[0], start[1], ARM_A_LEN, ARM_B_LEN)
		instructions.append((math.degrees(angle_a) + A_OFFSET,
							 math.degrees(angle_b) + B_OFFSET))
		instructions.append(0.5) # delay
		instructions.append(True) # pen down


		length = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

		# in mm
		maxLineDistance = 5 # TODO: make it configurable

		# how many parts to break the line into
		partNum = 1
		if (length > maxLineDistance):
			partNum = math.ceil(length / maxLineDistance)

		partLength = length / partNum

		# (x1+k(x2-x1)/n,y1+k(y2-y1)/n)
		xPart = (end[0] - start[0]) / partNum
		yPart = (end[1] - start[1]) / partNum

		for i in range(1, partNum + 1):
			x = start[0] + i * xPart
			y = start[1] + i * yPart

			angle_a, angle_b = coordinate_to_angle(x, y, ARM_A_LEN, ARM_B_LEN)
			instructions.append((math.degrees(angle_a) + A_OFFSET,
								math.degrees(angle_b) + B_OFFSET))
			instructions.append(0.05)

		instructions.append(False)  # pen up

	return instructions
