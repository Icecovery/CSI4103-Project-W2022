import argparse
import cv2 as cv
import numpy as np
from image_converter import *

# main program entry point
if __name__ == "__main__":
	# parse the command-line args
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", dest="debug", action="store_true", help="Enable debug outputs.")
	parser.set_defaults(debug=False)
	parser.add_argument("--src_img_path", required=True, dest="src_img_path", action="store", type=str, help="Path to the source image")
	cmd_args = parser.parse_args()
	
	# read the source image
	src_img = cv.imread(cmd_args.src_img_path)
	image_converter_args = ImageConverterArgs(
		blur_radius=21,
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
	image_converter.convert()

	if cmd_args.debug:
		cv.waitKey()