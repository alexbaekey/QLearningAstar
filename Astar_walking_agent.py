import numpy as np
import random
import configparser 
import sys
import matplotlib.pyplot as plt
plt.ion()

class sim:

    def __init__(self, numbost, maxstep, numepisode, max_x, max_y):
        """
        2D grid platform for agent to walk through,
        each "cell" of the grid is either free or occupied.
        A 0 will represent free and 1 will represent occupied.
        -1 will represent where the agent is
        """
        self.max_x=max_x
        self.max_y=max_y
        self.start_x=0
        self.start_y=0
        dimensions=(max_y,max_x)
        self.gridmatrix=np.zeros(dimensions,dtype=int)
        self.place_obstacles(numberofobst=int(numobst))
        self.maxstep=maxstep
        self.x=0
        self.y=0
        self.win=(max_x,max_y)
        self.won=False
        self.numsteps2win=np.zeros((numepisode),dtype=int)
        self.gridmatrix[0][0]=-1
        # value of -1 will indicate agent
        self.trap=False #?
        for i in range(numepisode):
            print("Episode #" + str(i+1) + "\n")
            self.start(i)
        self.eval(numepisode)

    def start(self,i):
        self.x=0
        self.y=0
        self.direction=0
        timestep=0
        endgame=False
        self.trap=False
        self.won=False
        while (timestep<self.maxstep and endgame!=True):
            timestep+=1
            self.det_movement(direction=self.direction)
            if(self.gridmatrix[self.win[1]-1][self.win[0]-1]==-1):
                endgame=True
                print("WINNER\n\n\n\n\n\n")
                endgame=True
                self.numsetps2win[i]=timestep
                self.gridmatrix[self.win[1]-1][self.win[0]-1]=0
       if(self.won==False):
            self.numsteps2win[i]=timestep
        self.print_grid()
        if(self.trap==False):
            self.gridmatrix[self.y][self.x]=0
        else:
            self.gridmatrix[self.y][self.x]=1
            self.trap=False

    def place_obstacles(self,numberofobst=7):
        """
        places an input number of obtacles randomly in the grid
        """
        for i in range(numberofobst):
            while(1):
                x=random.choice(range((self.max_x-1)))
                y=random.choice(range((self.max_y-1)))
                self.gridmatrix[self.start_y][self.start_x]
                if(self.gridmatrix[y][x]==0 and 
                not ((x==0 and y==0) or (x==self.max_x and y==self.max_y))):
                    self.gridmatrix[y][x]=1
                    break		


    def det_movement(self,direction=0):
        if(self.trap==False):
            self.gridmatrix[self.y][self.x]=0 # token placement cleaned
        else:
            self.gridmatrix[self.y][self.x]=1
            self.trap=False

        #up
        if((direction==0) and (self.y<self.max_y-1)):
            if(self.gridmatrix[self.y+1][self.x]!=1):
                self.y += 1
            else:
                #hit obstacle
                self.y+=1
                self.trap=True
        elif (direction==0 and (self.y>=(self.max_y-1))):
            if(self.gridmatrix[self.y][self.x]==1):
                self.trap=True
            #no movement,at top of grid

        #down
        if((direction==1) and (self.y>0)):
            if(self.gridmatrix[self.y-1][self.x]!=1):
                self.y -= 1
            else:
                #hit obstacle
                self.trap=True
                self.y -=1
        elif(direction==1 and self.y==0):
            if(self.gridmatrix[self.y][self.x]==1):
                self.trap=True
            #no movement,at bottom

        #left
        if((direction==2) and (self.x>0)):
            if(self.gridmatrix[self.y][self.x-1]!=1):
                self.x -= 1
            else:
                # hit obstacle
                self.x -=1
                self.trap=True
        elif((direction==2) and (self.x==0)):
            if(self.gridmatrix[self.y][self.x]==1):
                self.trap=True
            #no movement,at far left

        #right
        if((direction==3) and (self.x<self.max_x-1)):
            if(self.gridmatrix[self.y][self.x+1]!=1):
                self.x += 1
            else:
                #hit obstacle
                self.x += 1
                self.trap=True
        elif((direction==3 and self.x==(self.max_x-1))):
            if(self.gridmatrix[self.y][self.x]==1):
                self.trap=True
            #no movement,at far left

        #stay still
        if(direction==4):
            # no movement
            if(self.gridmatrix[self.y][self.x]==1):
                self.trap=True

        self.gridmatrix[self.y][self.x]=-1
        #token placement marked


    def print_grid(self):
        print("occupancy grid:\n")
        print(np.flip(self.gridmatrix,0))
        #print("\n")
        return(self.gridmatrix)


    def eval(self,numepisodes):
        x=range(1,numepisodes+1,1)
        plt.plot(x,self.numsteps2win)
        plt.title("Number of timesteps to win")
        plt.xlabel("Episode number")
        plt.ylabel("# timesteps to win")
        plt.xticks(np.arange(min(x),max(x)+1,int(max(x)/20)))
        plt.savefig("Astar_steps_to_win.png")


if __name__ == "__main__":
    configval=sys.argv[1]
    # -c for configuration file, -i for user input
    if configval == "-c":
        config=configparser.ConfigParser()
        config.read('values.conf')
        numobst    = int(config['sim']['numobst'])
        maxstep    = int(config['sim']['maxstep'])
        numepisode = int(config['sim']['numepisode'])
        max_x      = int(config['sim']['max_x'])
        max_y      = int(config['sim']['max_y'])
    elif configval == "-i":
        numobst = input("Enter the number of obstacles\n")
        maxstep = input("Enter the maximum number of timesteps\n")
        numepisode = input("Enter the number of episodes\n")
        max_x = input("Enter the max x value for the grid\n")
        max_y = input("Enter the max y value for the grid\n") 
    obj=sim(numobst,maxstep,numepisode,max_x,max_y)
