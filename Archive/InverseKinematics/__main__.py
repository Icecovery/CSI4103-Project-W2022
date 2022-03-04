import argparse
import csv
import math
import os
from coordinate_converter import *

lines = [] # input
angles = [] # output

def export_path_csv(l):
	EXPORT_DIR = "Temp"
	EXPORT_FILE_NAME = "angles.csv"
	FULL_EXPORT_FILE_PATH = os.path.join(EXPORT_DIR, EXPORT_FILE_NAME)
	# create temp folder
	if not os.path.exists(EXPORT_DIR):
		os.makedirs(EXPORT_DIR)
	with open(FULL_EXPORT_FILE_PATH, "w") as file:
		for i in range(len(l)):
			line = str(l[i][0]) + "," + str(l[i][1]) + "," + str(l[i][2]) + "," + str(l[i][3]) + "\n"
			file.write(line)

def main():
	# parse the command-line args
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", dest="debug", action="store_true",
						help="Enable debug outputs.")
	parser.add_argument("-la", dest="la", required=True, action="store",
						type=float, help="Length of arm A (servo 1 to servo 2)")
	parser.add_argument("-lb", dest="lb", required=True, action="store",
						type=float, help="Length of arm B (servo 2 to servo pen)")
	parser.add_argument("-s", "--src_csv_path", required=True, dest="src_csv_path",
						action="store", type=str, help="Path to the source csv file")
	parser.add_argument("--offset_a", dest="offset_a", required=False, action="store", default=0.0,
						type=float, help="Offset angle of servo A for the output")
	parser.add_argument("--offset_b", dest="offset_b", required=False, action="store", default=0.0,
						type=float, help="Offset angle of servo B for the output")
	parser.set_defaults(debug=False)
	cmd_args = parser.parse_args()

	# set arm lengths
	la = cmd_args.la
	lb = cmd_args.lb

	# put vectors from CSV into an array
	with open(cmd_args.src_csv_path, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			i = 0
			while i < len(row): # convert vectors from str to int
				row[i] = float(row[i])
				i += 1
			lines.append(row)

	# calculate angles
	for line in lines:
		# origin angles
		angle_a1, angle_b1 = coordinate_to_angle(line[0], line[1], la, lb)

		# destination angles
		angle_a2, angle_b2 = coordinate_to_angle(line[2], line[3], la, lb)

		angle = []
		angle.append(math.degrees(angle_a1) + cmd_args.offset_a)
		angle.append(math.degrees(angle_b1) + cmd_args.offset_b)
		angle.append(math.degrees(angle_a2) + cmd_args.offset_a)
		angle.append(math.degrees(angle_b2) + cmd_args.offset_b)

		angles.append(angle)

	if cmd_args.debug:
		export_path_csv(angles)

# main program entry point
if __name__ == "__main__":
	main()