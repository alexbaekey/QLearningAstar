import numpy as np
import random

class grid:

    def __init__(self):
        """
        2D grid platform for agent to walk through,
        each "cell" of the grid is either free or occupied.
        A 0 will represent free and 1 will represent occupied.
        -1 will represent where the agent is
        """
        self.max_x=10
        self.max_y=10
        dimensions=(self.max_y,self.max_x)
        self.gridmatrix=np.zeros(dimensions,dtype=int)
        self.current_x=0
        self.current_y=0
        self.gridmatrix[self.current_x][self.current_y]=-1 #-1 will indicate agent
        self.direction='r'
        numobst = input("Enter the number of obstacles\n")
        self.place_obstacles(numberofobst=int(numobst))
        numsteps = input("Enter the number of timesteps\n")
        for i in range(int(numsteps)):
            self.movement(direction=self.direction)
            self.print_grid()


    def place_obstacles(self,numberofobst=7):
        """
        places an input number of obtacles randomly in the grid
        """
        for i in range(numberofobst):
	        while(1):
		        x=random.choice(range(9))
		        y=random.choice(range(9))
		        if(self.gridmatrix[y][x]==0):
			        self.gridmatrix[y][x]=1
			        break		


    def movement(self,direction='r'):
        self.gridmatrix[self.current_y][self.current_x]=0
        if(direction=='u' and self.current_y<self.max_y-1 and
        self.gridmatrix[self.current_y+1][self.current_x] is not 1):
	        self.current_y += 1
        if(direction=='d' and self.current_y>0 and
        self.gridmatrix[self.current_y-1][self.current_x] is not 1):
	        self.current_y -= 1
        if(direction=='r' and self.current_x<self.max_x-1 and
        self.gridmatrix[self.current_y][self.current_x+1] is not 1):
	        self.current_x += 1
        if(direction=='u' and self.current_x>0 and
        self.gridmatrix[self.current_y][self.current_x-1] is not 1):
	        self.current_x -= 1
        self.gridmatrix[self.current_y][self.current_x]=-1



    def print_grid(self):
        print(self.gridmatrix)
        return(self.gridmatrix)


if __name__ == "__main__":
    grid1=grid()

