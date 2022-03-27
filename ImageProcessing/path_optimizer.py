from random import randrange
from math import sqrt
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
			'segments': list of the pairs of the start point and end point for
			each line, like [((1, 1), (2, )) ...].

			'debug': debug flag

			'shape': image shape, img_shape attribute of an object returned by
			cv2.imread() function.
		'''
		# segments[line, line, ...] => array of lines
		# line[point, point] => tuple of two points
		# point[number, number] => tuple of two numbers, x and y

		# shape[w, h] => tuple of int
		if segments is None:
			raise AttributeError()

		# the thing to return
		new_segments = []
    
		GRID_SIZE = int(sqrt(len(segments) * 1)) # seems like a reasonable function
		GRID_WIDTH = shape[1] / GRID_SIZE
		GRID_HEIGHT = shape[0] / GRID_SIZE

		# grid format: list(points)
		# points format: tuple(id, (x, y))
		grid = []
		# create grid
		for _ in range(GRID_SIZE):
			grid_line = []
			for _ in range(GRID_SIZE):
				grid_line.append([])
			grid.append(grid_line)

		# point format: list[points]
		# points format: tuple(oppositeId, (x, y), (gridX, gridY))
		points = []

		# assign points to grid
		point_id = 0
		for segment in segments:

			# start point
			pointA = segment[0]
			gridAX = int( pointA[0] // GRID_WIDTH )
			gridAY = int( pointA[1] // GRID_HEIGHT )
			grid[gridAX][gridAY].append((point_id, pointA))
			
			# also let point remember which grid it is in
			# also the id of other end of the line
			points.append(((point_id + 1, pointA, (gridAX, gridAY))))
			point_id += 1

			# end point
			pointB = segment[1]
			gridBX = int( pointB[0] // GRID_WIDTH )
			gridBY = int( pointB[1] // GRID_HEIGHT )
			grid[gridBX][gridBY].append((point_id, pointB))
			
			# also let point remember which grid it is in
			# also the id of other end of the line
			points.append(((point_id - 1, pointB, (gridBX, gridBY))))
			point_id += 1

		# debug grid assignment using random color
		if debug and shape is not None: 
			grid_img = np.zeros(shape, np.uint8)
			for i in range(GRID_SIZE):
				for j in range(GRID_SIZE):
					c = (randrange(0, 256), randrange(0, 256), randrange(0, 256))
					for p in grid[i][j]:
						cv.circle(grid_img, p[1], radius=1, color=c)
			cv.imshow("Grid", grid_img)

		point_count = 0
		current_pid = 0

		with progressbar.ProgressBar(max_value=len(points), redirect_stdout=True) as bar:
			while True:
				# grid cell point format: tuple(id, (x, y))
				# points point format: tuple(oppositeId, (x, y), (gridX, gridY))
				current_point = points[current_pid]
				opposite_point = points[current_point[0]]
				new_segments.append((current_point[1], opposite_point[1]))

				# remove points from grid
				self.RemovePointFromGridCell(grid, current_point[2][0], current_point[2][1], current_pid)
				self.RemovePointFromGridCell(grid, opposite_point[2][0], opposite_point[2][1], current_point[0])

				# exit condition:
				point_count += 2
				bar.update(point_count)
				if (point_count >= len(points)):
					break

				current_grid = opposite_point[2]
				point_position = opposite_point[1]

				# check current grid first
				# return: tuple(closetPointId, closetDistanceSq)
				closest_point = self.ClosestPointInGrid(grid, current_grid, point_position)

				if (closest_point is not None): 
					current_pid = closest_point[0]
				else: # no point in current grid
					# expand out layer by layer, in each layer check for the closest point
					for grid_layer in range(1, GRID_SIZE):
						closet_point_id = None
						closet_distance_sq = float('inf')

						# layer = 1:
						# T T T
						# M   M
						# D D D

						# layer = 2:
						# T T T T T
						# M       M
						# M       M
						# M       M
						# D D D D D

						# top and down line 
						for x in range(current_grid[0] - grid_layer, current_grid[0] + grid_layer):
							for y in [current_grid[1] - grid_layer, current_grid[1] + grid_layer]:
								result = self.ClosestPointInGrid(grid, (x, y), point_position)
								if (result is None):
									continue
								(id, distance_sq) = result
								if distance_sq < closet_distance_sq:
									closet_distance_sq = distance_sq
									closet_point_id = id
						# middle
						for y in range(current_grid[1] - grid_layer + 1, current_grid[1] + grid_layer - 1):
							for x in [current_grid[0] - grid_layer, current_grid[0] + grid_layer]:
								result = self.ClosestPointInGrid(grid, (x, y), point_position)
								if (result is None):
									continue
								(id, distance_sq) = result
								if distance_sq < closet_distance_sq:
									closet_distance_sq = distance_sq
									closet_point_id = id
						
						if (closet_point_id is not None):
							current_pid = closet_point_id
							break 
		
		# debug optimized line and toolpath
		if debug and shape is not None: 
			optimized_img = np.zeros(shape, np.uint8)

			for i in range(0, len(new_segments)):
				# draw line in green
				cv.line(optimized_img, new_segments[i][0], new_segments[i][1], (0, 255, 0), 1, cv.LINE_AA)

				cv.imshow("Optimized", optimized_img)
				cv.waitKey(10)
				
				if i < len(new_segments) - 1:
					# draw path in red
					cv.line(optimized_img, new_segments[i][1], new_segments[i + 1][0], (0, 0, 255), 1, cv.LINE_AA)
				
				cv.imshow("Optimized", optimized_img)
				cv.waitKey(10)
			
		return new_segments

	# find closest point in a grid, return None if grid_coordinate does not exist or no point in grid
	def ClosestPointInGrid(self, grid, grid_coordinate, point):
		length = len(grid)
		if (grid_coordinate[0] < 0 or grid_coordinate[0] >= length or grid_coordinate[1] < 0 or grid_coordinate[1] >= length):
			return None

		cell = grid[grid_coordinate[0]][grid_coordinate[1]]
		if (len(cell) <= 0):
			return None
		
		closet_point_id = None
		closet_distance_sq = float('inf')
		for p in cell:
			distance_sq = self.DistanceSq(point, p[1])
			if distance_sq < closet_distance_sq:
				closet_distance_sq = distance_sq
				closet_point_id = p[0]
		
		return (closet_point_id, closet_distance_sq)

	# get square of distance for compairsion
	def DistanceSq(self, pointA, pointB):
		return (pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2

	# remove a point from a grid cell by id
	def RemovePointFromGridCell(self, grid, gridX, gridY, id):
		grid_cell = grid[gridX][gridY]
		for point in grid_cell:
			if ((point[0]) == id):
				grid_cell.remove(point)
