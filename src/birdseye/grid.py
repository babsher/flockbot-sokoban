import numpy as np
import cv2
import operator
import csv
import random
import math

#the number of grid cells in the x and y directions
CELLS_X = 9
CELLS_Y = 8

class Grid:

	def __init__(self, layout_file):

		#the number of cells in x and y
		self.cells_x = CELLS_X
		self.cells_y = CELLS_Y

		self.init_from_file(layout_file)

		#a list of the grid spaces where there are boxes
		self.box_points = []

		#a list of the grid spaces where there are goals
		self.goal_points = []

		#a list of grid spaces where there are obstacles
		self.obs_points = []

		#flockbot locations and orientations
		self.flock_points = []

		#img for displays
		self.reset_display()

		#did the grid get updated?
		self.grid_changed = True

	def init_from_file(self, filename):
		'''parses the grid layout file and generates a row-major grid where each
		element is a polygon corresponding to that gridspace'''

		points = self.get_points_from_file(filename)
		sorted_pts = self.sort_points(points)

		self.grid_poly = []

		#create a polygon for each grid space we are suppoosed to have
		for y in range(self.cells_y):

			grid_row = []

			for x in range(self.cells_x):
				poly_points = (sorted_pts[y][x],sorted_pts[y][x+1],sorted_pts[y+1][x],sorted_pts[y+1][x+1])
				poly = cv2.convexHull(np.array(poly_points))
				grid_row.append(poly)

			self.grid_poly.append(grid_row)

		#set the min and max values
		self.minx = min(points, key=operator.itemgetter(0))[0]
		self.maxx = max(points, key=operator.itemgetter(0))[0]
		self.miny = min(points, key=operator.itemgetter(1))[1]
		self.maxy = max(points, key=operator.itemgetter(1))[1]

	def get_points_from_file(self, filename):
		'''gets the points from a file, converts them to ints, and returns the list'''
		points = []
		with open(filename, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				points.append((int(row[0]),int(row[1])))
		return points

	def sort_points(self, points):
		'''takes the given list of points and sorts them into a 2-d list
		based on the cells x and cells y'''

		all_sorted = []

		#sort into rows by y points
		points.sort(key=operator.itemgetter(1))

		#break up the points into rows based on the number of cells
		#append that row to all_sorted
		for i in range(self.cells_y+1):
			row = points[(i*(self.cells_x+1)):((i*(self.cells_x+1))+self.cells_x+1)]
			all_sorted.append(row)

		#sort the rows by x based on the first point in each row 
		for row in all_sorted:
			row.sort(key=operator.itemgetter(0,0))

		return all_sorted

	def reset_display(self):
		self.grid_img = np.zeros((480,640,3))

	def overlay_grid(self,img):
		'''draws the polygonal grid onto the given img and returns the resulting img'''
		for y,row in enumerate(self.grid_poly):
			for x,poly in enumerate(row):
				cv2.drawContours(img,[poly],-1,np.array([0,77,255]))

		return img

	def display_grid(self):
		'''displays the grid in a window'''
		if self.grid_changed:
			self.reset_display()
			for y,row in enumerate(self.grid_poly):
				for x,poly in enumerate(row):
					if (x,y) in self.box_points:
						cv2.drawContours(self.grid_img,[poly],-1,np.array([0,77,255]),-1)
					elif (x,y) in self.goal_points:
						cv2.drawContours(self.grid_img,[poly],-1,np.array([0,255,0]),-1)
					elif (x,y) in self.obs_points:
						cv2.drawContours(self.grid_img,[poly],-1,np.array([0,0,255]),-1)
					else:
						cv2.drawContours(self.grid_img,[poly],-1,np.array([0,77,255]))
			self.grid_changed = False
		
		cv2.imshow("Grid",cv2.flip(self.grid_img,-1))

	def set_boxes(self, points):
		'''sets the box points'''
		if points != self.box_points:
			self.box_points = points
			self.grid_changed = True

	def set_goals(self, points):
		'''sets the goal points'''
		if points != self.goal_points:
			self.goal_points = points
			self.grid_changed = True

	def set_obs(self, points):
		'''sets the obstacle points'''
		if points != self.obs_points:
			self.obs_points = points
			self.grid_changed = True

	def set_flocks(self, points):
		'''sets the flockbot points'''
		if points != self.flock_points:
			self.flock_points = points
			self.grid_changed = True

	def in_grid(self,point):
		'''given an x,y coordinate of a pixel, will return true if pixel is in the grid, false if not'''
		x,y = point

		if x >= self.minx and x <= self.maxx and y >= self.miny and y <= self.maxy:
			return True

		return False

	def where_in_grid(self,point):
		'''given an x,y coordinate of a pixel, will return the x,y cell that the pixel is in'''
		x,y = point

		for y in range(self.cells_y):
			for x in range(self.cells_x):
				poly = self.grid_poly[y][x]
				if cv2.pointPolygonTest(poly,point,False) >= 0:
					return (x,y)

	def get_box_pts(self):
		return [self.flip_pt(pt) for pt in self.box_points]

	def get_goal_pts(self):
		return [self.flip_pt(pt) for pt in self.goal_points]

	def get_obs_pts(self):
		return [self.flip_pt(pt) for pt in self.obs_points]

	def get_flock_pts(self):
		return [(self.flip_(pt),orientation) for pt,orientation in self.flock_points]

	def flip_pt(self,pt):
		return ((np.absolute((self.cells_x-1)-pt[0])),pt[1])

