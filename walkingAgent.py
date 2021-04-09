import numpy as np
import random
import configparser 


class sim:

    def __init__(self, simtype, numbost, maxstep, numepoc):
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
        self.place_obstacles(numberofobst=int(numobst))
        self.maxstep=maxstep
        self.current_x=0
        self.current_y=0
        for i in range(numepoc):
            print("Epoch #" + str(i+1) + "\n")
            self.start()

    def start(self):
        self.gridmatrix[self.current_y][self.current_x]=0
        self.current_x=0
        self.current_y=0
        # value of 0 will inidicate unoccupied
        self.gridmatrix[self.current_y][self.current_x]=-1
        # value of -1 will indicate agent
        self.direction=0
        for i in range(int(self.maxstep)):
            self.print_grid()
            if(simtype==0):
                self.det_movement(direction=self.direction)
            else:
                self.stoc_movement(direction=self.direction)


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

    def det_movement(self,direction=0):
        """
        deterministic movement based on A* algorithm
        """
        self.gridmatrix[self.current_y][self.current_x]=0
        if((direction==0) and (self.current_y<self.max_y-1) and
        (self.gridmatrix[self.current_y+1][self.current_x]!=1)):
            self.current_y += 1
        if((direction==1) and (self.current_y>0) and
        (self.gridmatrix[self.current_y-1][self.current_x]!=1)):
            self.current_y -= 1
        if((direction==2) and (self.current_x<self.max_x-1) and
        (self.gridmatrix[self.current_y][self.current_x+1]!=1)):
            self.current_x += 1
        if((direction==3) and (self.current_x>0) and
        (self.gridmatrix[self.current_y][self.current_x-1]!=1)):
            self.current_x -= 1
        self.gridmatrix[self.current_y][self.current_x]=-1


    def stoc_movement(self,direction=0):
        """
        stochastic  movement based on Q-Learning algorithm        
        Inputs:
            directions (dtype:str)
        Outputs:
            None
        """
        r=random.random()
        if (r<0.6):
            # commence direction as commanded
            pass
        if (r>=0.6 and r<0.7):
            #change direction
            direction=(direction+1)%4
        if (r>=0.7 and r<0.8):
            #change direction
            direction=(direction+2)%4
        # change direction
        if (r>=0.8 and r<0.9):
            #change direction
            direction=(direction+3)%4
        # change direction
        if (r>=0.9 and r<1.0):
            #stay in same spot
            direction=4
            pass
        self.gridmatrix[self.current_y][self.current_x]=0 # token placement cleaned
        if((direction==0) and (self.current_y<self.max_y-1) and
        (self.gridmatrix[self.current_y+1][self.current_x]!=1)):
            self.current_y += 1
        if((direction==1) and (self.current_y>0) and
        (self.gridmatrix[self.current_y-1][self.current_x]!=1)):
            self.current_y -= 1
        if((direction==2) and (self.current_x<self.max_x-1) and
        (self.gridmatrix[self.current_y][self.current_x+1]!=1)):
            self.current_x += 1
        if((direction==3) and (self.current_x>0) and
        (self.gridmatrix[self.current_y][self.current_x-1]!=1)):
            self.current_x -= 1
        if(direction==4):
            # no movement
            pass
        self.gridmatrix[self.current_y][self.current_x]=-1
        #token placement marked

    def print_grid(self):
        print(self.gridmatrix)
        print("\n")
        return(self.gridmatrix)



if __name__ == "__main__":
    configval=int(input("read from input (0) or new configuration (1)?\n"))
    if (configval is 0):
        config=configparser.ConfigParser()
        config.read('values.conf')
        simtype = int(config['sim']['simtype'])
        numobst = int(config['sim']['numobst'])
        maxstep = int(config['sim']['maxstep'])
        numepoc = int(config['sim']['numepoc'])
    elif (configval is 1):
        simtype=input("Select 0 for deterministic (A* algorithm), 1 for stochastic (Q Learning)\n")
        numobst = input("Enter the number of obstacles\n")
        maxstep = input("Enter the maximum number of timesteps\n")
        numepoc = input("Enter the number of epochs\n")
    obj=sim(simtype,numobst,maxstep,numepoc)
