import numpy as np
import cv2 as cv


class PixelToRealSpaceConverter:

	# size are in (width, height) format
	# coordinate are in (x, y) format
	
	# coordinate is relative to top left of the paper
	# (0,0) ----> x
	# |
	# |
	# V
	# y

	# unit of pixel size is px
	# unit of real size and root coordinate is mm

	def convert(self, segments, pixelSize, realSize=(210, 297), rootCoordinate=(-50, 150)):
		if segments is None:
			raise AttributeError()
		new_segments = []

		# scale image to fit on paper
		scaling_factor = 1.0

		if pixelSize[0] > pixelSize[1]:  # image is wider
			# use width to calculate scaling factor
			scaling_factor = realSize[0] / pixelSize[0]
		else: # image is taller
			# use height to calculate scaling factor
			scaling_factor = realSize[1] / pixelSize[1]

		for segment in segments:
			x1 = segment[0][0] * scaling_factor - rootCoordinate[0]
			y1 = segment[0][1] * scaling_factor - rootCoordinate[1]
			x2 = segment[1][0] * scaling_factor - rootCoordinate[0]
			y2 = segment[1][1] * scaling_factor - rootCoordinate[1]

			start = (x1, y1)
			end = (x2, y2)

			new_segments.append((start, end))

		return new_segments