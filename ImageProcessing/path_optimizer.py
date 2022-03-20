import numpy as np
import cv2 as cv
import progressbar

class PathOptimizer:
	'''
		This class is to optimize the line segments so that the path of the pen
		can be shorter.
	'''

	def optimize(self, segments, debug=False, shape=None):
		'''
			Optimize the line segments.

			Parameters
			----------
			`segments`: list of the pairs of the start point and end point for
			each line, like [((1, 1), (2, )) ...].

			`debug`: debug flag

			`shape`: image shape, img_shape attribute of an object returned by
			cv2.imread() function.
		'''
		if segments is None:
			raise AttributeError()

		new_segments = []

		current_line = segments[0]
		current_end = 1

		segments.pop(0)

		totalLength = len(segments)

		with progressbar.ProgressBar(max_value=totalLength) as bar:

			while len(segments) > 0:
				line = (current_line[1], current_line[0]) if current_end == 1 else current_line
				new_segments.append(line)

				closest_id = 0
				closest_end = 0
				closest_distance = float("inf")

				for i in range(len(segments)):
					distance_sqr, end = self._closest_distance_sqr(current_line[(current_end + 1 ) % 2], segments[i])

					if distance_sqr <= closest_distance:
						closest_id = i
						closest_end = end
						closest_distance = distance_sqr
				
				current_line = segments[closest_id]
				current_end = closest_end
				segments.pop(closest_id)

				bar.update(totalLength - len(segments)) # update progress bar
			
			new_segments.append((current_line[1], current_line[0]) if current_end == 1 else current_line)

		if debug and shape is not None:
			optimized_img = np.zeros(shape, np.uint8)

			for i in range(0, len(new_segments)):
				# draw line in green
				cv.line(optimized_img, new_segments[i][0], new_segments[i][1], (0, 255, 0), 1, cv.LINE_AA)

				if i < len(new_segments) - 1:
					# draw path in red
					cv.line(optimized_img, new_segments[i][1], new_segments[i + 1][0], (0, 0, 255), 1, cv.LINE_AA)

			cv.imshow("Optimized", optimized_img)
		return new_segments

	def _closest_distance_sqr(self, p, line):
		'''
			Private function
		'''
		distance_sqr_to_p0 = (p[0] - line[0][0]) ** 2 + (p[1] - line[0][1]) ** 2
		distance_sqr_to_p1 = (p[0] - line[1][0]) ** 2 + (p[1] - line[1][1]) ** 2

		if distance_sqr_to_p0 <= distance_sqr_to_p1:
			return (distance_sqr_to_p0, 0)
		else:
			return (distance_sqr_to_p1, 1)
