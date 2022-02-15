import numpy as np
import cv2 as cv

class PathOptimizer:
	def Optimize(self, segments, debug=False, shape=None):
		if segments is None:
			raise AttributeError()

		newSegments = []

		currentLine = segments[0]
		currentEnd = 1

		segments.pop(0)

		while len(segments) > 0:
			newSegments.append(currentLine)

			closestId = 0
			closestEnd = 0
			closestDistance = float("inf")

			for i in range(len(segments)):
				distanceSqr, end = self.ClosestDistanceSqr(currentLine[currentEnd], segments[i])

				if distanceSqr <= closestDistance:
					closestId = i
					closestEnd = end
					closestDistance = distanceSqr
			
			currentLine = segments[closestId]
			currentEnd = closestEnd
			segments.pop(closestId)

		
		if debug and shape is not None:
			optimized_img = np.zeros(shape, np.uint8)

			for i in range(0, len(newSegments)):
				# draw line in green
				cv.line(optimized_img, newSegments[i][0], newSegments[i][1], (0, 255, 0), 1, cv.LINE_AA)

				if i < len(newSegments) - 1:
					# draw path in red
					cv.line(optimized_img, newSegments[i][1], newSegments[i + 1][0], (0, 0, 255), 1, cv.LINE_AA)

			cv.imshow("Optimized", optimized_img)

		
		return newSegments

	def ClosestDistanceSqr(self, p, line):
		distanceSqrToP0 = (p[0] - line[0][0]) ** 2 + (p[1] - line[0][1]) ** 2
		distanceSqrToP1 = (p[0] - line[1][0]) ** 2 + (p[1] - line[1][1]) ** 2

		if distanceSqrToP0 <= distanceSqrToP1:
			return (distanceSqrToP0, 0)
		else:
			return (distanceSqrToP1, 1)

