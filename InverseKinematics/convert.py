import math
import progressbar

from .device_abstraction import *

def coordinate_to_angle(x, y, la, lb):
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

	angle_sets = []
	for line in progressbar.progressbar(lines):
		start, end = line
		# current angles
		angle_a1, angle_b1 = coordinate_to_angle(start[0], start[1], ARM_A_LEN, ARM_B_LEN)
		# next angles
		angle_a2, angle_b2 = coordinate_to_angle(end[0], end[1], ARM_A_LEN, ARM_B_LEN)
		
		angle_set = []
		angle_set.append(math.degrees(angle_a1) + A_OFFSET)
		angle_set.append(math.degrees(angle_b1) + B_OFFSET)
		angle_set.append(math.degrees(angle_a2) + A_OFFSET)
		angle_set.append(math.degrees(angle_b2) + B_OFFSET)

		angle_sets.append(angle_set)

	return angle_sets
