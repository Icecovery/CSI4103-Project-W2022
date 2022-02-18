import argparse
import os
import cv2 as cv
import numpy as np
from image_converter import *
from path_optimizer import *

def ExportPath(l):
	ans = input("Export path? (y/n): ")
	if (ans.lower() != "y"):
		return None

	# create temp folder
	if not os.path.exists('Temp'):
		os.makedirs('Temp')

	# write lines
	file = open("Temp/path.csv", "w")
	for i in range(len(l)):
		line = str(l[i][0][0]) + "," + str(l[i][0][1]) + "," + str(l[i][1][0]) + "," + str(l[i][1][1]) + "\n"
		file.write(line)
	file.close()

def Main():
	# parse the command-line args
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", dest="debug", action="store_true", help="Enable debug outputs.")
	parser.set_defaults(debug=False)
	parser.add_argument("--src_img_path", required=True, dest="src_img_path", action="store", type=str, help="Path to the source image")
	cmd_args = parser.parse_args()
	
	# read the source image
	src_img = cv.imread(cmd_args.src_img_path)
	image_converter_args = ImageConverterArgs(
		blur_radius=5,
		canny_threshold_1=60,
		canny_threshold_2=10,
		hough_threshold=8,
		aperture_size=3,
		min_line_length=5,
		max_line_gap=5,
		rho=1,
		theta=np.pi/180
	)

	# convert the source image
	image_converter = ImageConverter(src_img, image_converter_args, cmd_args.debug)
	segments = image_converter.convert()

	optimizer = PathOptimizer()
	optimizedSegments = optimizer.Optimize(segments, debug=True, shape=src_img.shape)
	
	# export line coordinates
	ExportPath(optimizedSegments)

	if cmd_args.debug:
		cv.waitKey()

# main program entry point
if __name__ == "__main__":
	Main()