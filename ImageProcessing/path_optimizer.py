import numpy as np
import cv2 as cv
import progressbar

class PathOptimizer:
	def optimize(self, segments, debug=False, shape=None):
		if segments is None:
			raise AttributeError()

		new_segments = []

		current_line = segments[0]
		current_end = 1

		segments.pop(0)

		totalLength = len(segments)

		with progressbar.ProgressBar(max_value=totalLength) as bar:

			while len(segments) > 0:
				new_segments.append(current_line)

				closest_id = 0
				closest_end = 0
				closest_distance = float("inf")

				for i in range(len(segments)):
					distance_sqr, end = self._closest_distance_sqr(current_line[current_end], segments[i])

					if distance_sqr <= closest_distance:
						closest_id = i
						closest_end = end
						closest_distance = distance_sqr
				
				current_line = segments[closest_id]
				current_end = closest_end
				segments.pop(closest_id)

				bar.update(totalLength - len(segments)) # update progress bar

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
		distance_sqr_to_p0 = (p[0] - line[0][0]) ** 2 + (p[1] - line[0][1]) ** 2
		distance_sqr_to_p1 = (p[0] - line[1][0]) ** 2 + (p[1] - line[1][1]) ** 2

		if distance_sqr_to_p0 <= distance_sqr_to_p1:
			return (distance_sqr_to_p0, 0)
		else:
			return (distance_sqr_to_p1, 1)
