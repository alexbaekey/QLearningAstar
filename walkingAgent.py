import numpy as np
import random

class grid():

	def __init__(self)
		"""
		2D grid platform for agent to walk through,
		each "cell" of the grid is either free or occupied.
		A 0 will represent free and 1 will represent occupied.
		"""
		self.max_x=10
		self.max_y=10
		dimensions=(max_x,max_y)
		self.gridmatrix=np.zeros(dimensions,dtype=int)
		self.current_x=0
		self.current_y=0
		self.gridmatrix[current_x][current_y]=1
		

	def place_obstacles(self,numberofobst=7)
		"""
		places an input number of obtacles randomly in the grid
		"""
		for i in range(numberofobst):
			while(1):
				x=random.choice[range(9)]
				y=random.choice[range(9)]
				if(self.gridmatrix[x][y]==0):
					self.gridmatrix[x][y]=1
					break		


	def movement(self,current_x,current_y,direction)
		self.gridmatrix[current_x][current_y]=0
		if(direction=='u' and current_y<max_y-1):
			self.current_y += 1
		if(direction=='d' and current_y>0):
			self.current_y -= 1
		if(direction=='r' and current_x<max_x-1):
			self.current_x += 1
		if(direction=='u' and current_x>0):
			self.current_x -= 1
		self.gridmatrix[current_x][current_y]=1


	def print_grid(self)
		return(self.gridmatrix)


