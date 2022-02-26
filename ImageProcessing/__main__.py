import argparse
import os
import cv2 as cv
import numpy as np
from parso import parse
from image_converter import *
from path_optimizer import *
from pixel_to_real_space_converter import *

def export_path_csv(l):
	EXPORT_DIR = "Temp"
	EXPORT_FILE_NAME = "path.csv"
	FULL_EXPORT_FILE_PATH = os.path.join(EXPORT_DIR, EXPORT_FILE_NAME)

	# create temp folder
	if not os.path.exists(EXPORT_DIR):
		os.makedirs(EXPORT_DIR)

	with open(FULL_EXPORT_FILE_PATH, "w") as file:
		for i in range(len(l)):
			line = str(l[i][0][0]) + "," + str(l[i][0][1]) + "," + str(l[i][1][0]) + "," + str(l[i][1][1]) + "\n"
			file.write(line)

def main():
	# parse the command-line args
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug",
						dest="debug", action="store_true", help="Enable debug outputs.")
	parser.add_argument("-s", "--src_img_path",
						required=True, dest="src_img_path", action="store", type=str, help="Path to the source image")
	parser.add_argument("--height",
						required=True, dest="height", action="store", type=int, help="Height of the paper")
	parser.add_argument("--width",
						required=True, dest="width", action="store", type=int, help="Width of the paper")
	parser.add_argument("-x", "--x_offset",
						required=True, dest="x_offset", action="store", type=int, help="X offset of the origin")
	parser.add_argument("-y", "--y_offset",
						required=True, dest="y_offset", action="store", type=int, help="Y offset of the origin")
	parser.set_defaults(debug=False)
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

	# optimize the moving path
	optimizer = PathOptimizer()
	optimized_segments = optimizer.optimize(segments, debug=cmd_args.debug, shape=src_img.shape)

	# convert image to real space
	pixel_to_real = PixelToRealSpaceConverter()
	real_space_segments = pixel_to_real.convert(optimized_segments, src_img.shape, 
		(cmd_args.height, cmd_args.width), (cmd_args.x_offset, cmd_args.y_offset), debug=cmd_args.debug)

	if cmd_args.debug:
		export_path_csv(real_space_segments)
		cv.waitKey()

# main program entry point
if __name__ == "__main__":
	main()