import numpy as np
import cv2 as cv
import progressbar

class PixelToRealSpaceConverter:

	# size are in (height, width) format
	# coordinate are in (x, y) format
	
	# coordinate is relative to top left of the paper
	# (0,0) ----> x
	# |
	# |
	# V
	# y

	# unit of pixel size is px
	# unit of real size and root coordinate is mm

	def convert(self, segments, shape, realSize, rootCoordinate, debug=False):
		if segments is None:
			raise AttributeError()
		new_segments = []
		
		pixelSize = (shape[0], shape[1])

		# scale image to fit on paper
		scaling_factor = 1.0

		if pixelSize[0] > pixelSize[1]:  # image is wider
			# use width to calculate scaling factor
			scaling_factor = realSize[0] / pixelSize[0]
		else: # image is taller
			# use height to calculate scaling factor
			scaling_factor = realSize[1] / pixelSize[1]

		for segment in progressbar.progressbar(segments):
			x1 = segment[0][0] * scaling_factor - rootCoordinate[0]
			y1 = segment[0][1] * scaling_factor - rootCoordinate[1]
			x2 = segment[1][0] * scaling_factor - rootCoordinate[0]
			y2 = segment[1][1] * scaling_factor - rootCoordinate[1]

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

			realShape = (realSize[0] * scale, realSize[1] * scale, shape[2])
			real_size_img = np.zeros(realShape, np.uint8)

			for s in range(0, len(new_segments)):

				# remove root offset
				realPointStart = ((new_segments[s][0][0] + rootCoordinate[0]) * scale, (new_segments[s][0][1] + rootCoordinate[1]) * scale)
				realPointEnd = ((new_segments[s][1][0] + rootCoordinate[0]) * scale, (new_segments[s][1][1] + rootCoordinate[1]) * scale)
				
				cv.line(real_size_img, realPointStart, realPointEnd, (255, 255, 255), 1, cv.LINE_AA)

			cv.imshow("Real Size", real_size_img)

		return new_segments