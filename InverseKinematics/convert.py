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

def lines_to_instructions(lines):
	'''
		Convert line segments produced by ImageProcessing module to the 
		instructions

		Parameters
		----------
		`lines`: list of the coordinates of the line segments

		Return
		------
		A list contains instructions with different types.
		* `float`: sleep time
		* `tuple`: angles of the servos
		* `bool`: True -> pen down; False -> pen up
	'''
	print("Converting lines to instructions...")

	instructions = []

	# in mm
	minimumLineLength = 1  # TODO: make it configurable
	maxSegmentDistance = 5  # TODO: make it configurable
	minimumInterLineInterval = 2 # TODO: make it configurable

	# delay between each interpolated segments in second
	interLineSegmentDelay = 0.05  # TODO: make it configurable
	# delay between each line in second
	interLineDelay = 0.5  # TODO: make it configurable

	lastEnd = (-999, -999)
	
	for line in progressbar.progressbar(lines):
		start, end = line

		# ==== skip line check ====

		length = distance(start, end)
		if (length < minimumLineLength):
			# ignore this line
			continue

		# ==== skip pen lift check ====

		interLineInterval = distance(end, lastEnd)
		lastEnd = end

		# do not lift the pen if inter line interval is too short
		if (interLineInterval > minimumInterLineInterval):
			instructions.append(False)  # pen up

		# move to start
		instructions.append(getAngleInstruction(start[0], start[1]))

		# if inter lien interval is too short, we don't have to stop that long
		if (interLineInterval > minimumInterLineInterval):
			instructions.append(interLineDelay)
		else:
			instructions.append(interLineSegmentDelay)

		instructions.append(True) # pen down

		# ==== interpolation ====

		# how many parts to break the line into
		partNum = 1
		if (length > maxSegmentDistance):
			partNum = math.ceil(length / maxSegmentDistance)

		# (x1+k(x2-x1)/n,y1+k(y2-y1)/n)
		xPart = (end[0] - start[0]) / partNum
		yPart = (end[1] - start[1]) / partNum

		for i in range(1, partNum + 1):
			x = start[0] + i * xPart
			y = start[1] + i * yPart

			# move to segment
			instructions.append(getAngleInstruction(x, y))

			# delay
			instructions.append(interLineSegmentDelay)

	instructions.append(False)  # pen up
	return instructions

def getAngleInstruction(x, y):
	angle_a, angle_b = coordinate_to_angle(x, y, ARM_A_LEN, ARM_B_LEN)
	return (math.degrees(angle_a) + A_OFFSET, math.degrees(angle_b) + B_OFFSET)

def distance(a, b):
	return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
