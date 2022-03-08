import os
import cv2 as cv
import numpy as np

from .paper import Paper
from .image_converter import *
from .path_optimizer import *
from .pixel_to_real_space_converter import *

def image_process(src_image_path: str, paper: Paper, debug=False):
	'''
		Process the source image, and return the real-world coordinates
		of line segments.

		Parameters
		----------

		`src_image_path`: the path of the source image

		`paper`: an object of Paper class containing some papar size data

		`debug`: debug flag
	'''

	# read the source image
	src_img = cv.imread(src_image_path)
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
	image_converter = ImageConverter(src_img, image_converter_args, debug)
	print("Converting image to segments...", end="")
	segments = image_converter.convert()
	print("Done")

	# optimize the moving path
	optimizer = PathOptimizer()
	print("Optimizing path...")
	optimized_segments = optimizer.optimize(segments, debug=debug, shape=src_img.shape)

	# convert the line segments in pixel length to the line segments in real-world length
	pixel_to_real = PixelToRealSpaceConverter()

	print("Converting to real space...")
	real_space_segments = pixel_to_real.convert(optimized_segments, src_img.shape, 
		(paper.height, paper.width), (paper.x_offset, paper.y_offset), debug=debug)

	return real_space_segments
