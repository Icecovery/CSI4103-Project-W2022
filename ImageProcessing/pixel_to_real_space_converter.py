import numpy as np
import cv2 as cv
import progressbar

class PixelToRealSpaceConverter:
	'''
		This class converts the coordinates in pixel length (px) to the real world length (mm).

		size are in (height, width) format
		coordinate are in (x, y) format

		coordinate is relative to top left of the paper

		(0,0) ----> x \\
		| \\
		| \\
		V \\
		y

		unit of pixel size is px
		unit of real size and root coordinate is mm
	'''

	def convert(self, segments, shape, real_size, root, debug=False):
		'''
			Convert the coordinates in pixel length (px) to the real world length (mm).
			
			Parameters
			----------
			`segments`: list of coordinates in pixel length

			`shape`: the shape of the image in pixel.

			`real_size`: real paper size in mm.

			`root`: the root coordinate of the arm base.

			Return
			------
			A list of coordinates in mm.
		'''
		if segments is None:
			raise AttributeError()
		new_segments = []
		
		pixel_size = (shape[0], shape[1])

		# scale image to fit on paper
		scaling_factor = 1.0

		if pixel_size[0] > pixel_size[1]:  # image is wider
			# use width to calculate scaling factor
			scaling_factor = real_size[0] / pixel_size[0]
		else: # image is taller
			# use height to calculate scaling factor
			scaling_factor = real_size[1] / pixel_size[1]

		for segment in progressbar.progressbar(segments):
			x1 = segment[0][0] * scaling_factor - root[0]
			y1 = segment[0][1] * scaling_factor - root[1]
			x2 = segment[1][0] * scaling_factor - root[0]
			y2 = segment[1][1] * scaling_factor - root[1]

			x1 = round(x1)
			y1 = -round(y1)

			x2 = round(x2)
			y2 = -round(y2)

			start = (x1, y1)
			end = (x2, y2)

			new_segments.append((start, end))


		if debug and shape is not None:
			# window size multiplier
			scale = 3

			realShape = (real_size[0] * scale, real_size[1] * scale, shape[2])
			real_size_img = np.zeros(realShape, np.uint8)

			for s in range(0, len(new_segments)):
				# remove root offset
				real_start = ((new_segments[s][0][0] + root[0]) * scale, (new_segments[s][0][1] + root[1]) * scale)
				real_end = ((new_segments[s][1][0] + root[0]) * scale, (new_segments[s][1][1] + root[1]) * scale)
				
				cv.line(real_size_img, real_start, real_end, (255, 255, 255), 1, cv.LINE_AA)

			cv.imshow("Real Size", real_size_img)

		return new_segments
