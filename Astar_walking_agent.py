import numpy as np
import random
import configparser 
import sys
import math
import time
import matplotlib.pyplot as plt
plt.ion()


class sim:

    def __init__(self, numbost, max_x, max_y):
        """
        2D grid platform for agent to walk through,
        each "cell" of the grid is either free or occupied.
        A 0 will represent free and 1 will represent a trap.
        -1 will represent where the agent is
        """
        # Initial values
        self.max_x=max_x
        self.max_y=max_y
        dimensions=(max_y,max_x)
        # Roll for random starting point
        self.start_x=np.random.randint(0,max_x-1)
        self.start_y=np.random.randint(0,max_y)
        #winning block always along right side
        self.win=(max_x,np.random.randint(0,max_y))
        self.end_x=self.win[0]
        self.end_y=self.win[1]
        self.won=False
        # Initialize occupancy grid
        self.gridmatrix=np.zeros(dimensions,dtype=int)
        # Place obstacles on grid
        self.place_obstacles(numberofobst=int(numobst))
        self.x=self.start_x
        self.y=self.start_y
        self.g_grid=np.zeros(dimensions,dtype=float)
        self.h_grid=np.zeros(dimensions,dtype=float)
        self.f_grid=np.zeros(dimensions,dtype=float)
        self.opengrid=np.zeros(dimensions,dtype=int)
        #for opengrid, 0 is open, 1 is closed
        self.timestep=0
        self.path = []
        self.path.append((self.x,self.y))
        #0 is open, 1 is closed
        # run
        self.run()

    def run(self):
        while(self.won==False):
            self.timestep+=1
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if(self.x+i==self.win[0]-1 and self.y+j==self.win[1]-1):
                        self.path.append((self.x+i,self.y+j))
                        self.won=True
                        break;
                    if((self.x+i>=0 and self.x+i<=self.max_x-1) and \
                    (self.y+j>=0 and self.y+j<=self.max_y-1) and not \
                    (i==0 and j==0)):
                        if (self.g_grid[self.y+j][self.x+i]==0):
                            self.calc_g(self.x+i,self.y+j,self.start_x,self.start_y)
                            self.calc_h(self.x+i,self.y+j,self.end_x,self.end_y)
                            self.calc_f(self.x+i,self.y+j)
                    else:
                        #out of bounds
                        pass
            self.printfgrid()
            self.move(self.x,self.y)
            time.sleep(3)
            if(self.won==True):
                break
        self.printresults()

    def calc_g(self,cur_x,cur_y,start_x,start_y):
        self.g_grid[cur_y][cur_x]=math.sqrt((cur_x-start_x)**2+(cur_y-start_y)**2)

    def calc_h(self,cur_x,cur_y,end_x,end_y):
        self.h_grid[cur_y][cur_x]=math.sqrt((cur_x-end_x)**2+(cur_y-end_y)**2)

    def calc_f(self,cur_x,cur_y):
        """
        select lowest f value (g+h)
        move in that direction
        """        
        self.f_grid[cur_y][cur_x]=self.g_grid[cur_y][cur_x]+self.h_grid[cur_y][cur_x]

    def move(self,cur_x,cur_y):
        minf=999999
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if((cur_x+i>=0 and cur_x+i<=self.max_x-1) and \
                (cur_y+j>=0 and cur_y+j<=self.max_y-1) and not \
                (i==0 and j==0) and self.opengrid[cur_y+j][cur_x+i]!=1):
                    if (self.f_grid[cur_y+j][cur_x+i]<minf and \
                    self.gridmatrix[cur_y+j][cur_x+i]!=1):
                        minf=self.f_grid[cur_y+j][cur_x+i]
                        next_x=cur_x+i
                        next_y=cur_y+j
        self.opengrid[cur_y][cur_x]=1
        self.x=next_x
        self.y=next_y
        self.path.append((self.x,self.y))


    def place_obstacles(self,numberofobst=7):
        """
        places an input number of obtacles randomly in the grid
        """
        for i in range(numberofobst):
            while(1):
                x=random.choice(range((self.max_x-1)))
                y=random.choice(range((self.max_y-1)))
                if(self.gridmatrix[y][x]==0 and 
                not ((x==self.start_x and y==self.start_y) or \
                (x==self.win[0]-1 and y==self.win[1]-1))):
                    self.gridmatrix[y][x]=1
                    break	


    def printfgrid(self):
        print(np.round(self.f_grid,2))
        print("\n")

    def printresults(self):
        print("START: " + str(self.start_x)+","+str(self.start_y)+"\n") 
        print("END: " + str(self.end_x)+","+str(self.end_y)+"\n") 
        print("PATH:" + "\n" + str(self.path))


if __name__ == "__main__":
    try:
        configval=sys.argv[1]
        # -c for configuration file, -i for user input
    except:
        print("make sure to include -c for config file or -i for user input")
    if configval== "-c":
        config=configparser.ConfigParser()
        config.read('values.conf')
        numobst    = int(config['sim']['numobst'])
        max_x      = int(config['sim']['max_x'])
        max_y      = int(config['sim']['max_y'])
    elif configval == "-i":
        numobst = input("Enter the number of obstacles\n")
        max_x = input("Enter the max x value for the grid\n")
        max_y = input("Enter the max y value for the grid\n") 
    obj=sim(numobst,max_x,max_y)


