import numpy as np
import random
import configparser 


class sim:

    def __init__(self, simtype, numbost, maxstep, numepisode):
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
        self.x=0
        self.y=0
        self.win=(10,10)
        for i in range(numepisode):
            print("Episode #" + str(i+1) + "\n")
            self.start()

    def start(self):
        self.gridmatrix[self.y][self.x]=0
        self.x=0
        self.y=0
        # value of 0 will inidicate unoccupied
        self.gridmatrix[self.y][self.x]=-1
        # value of -1 will indicate agent
        self.direction=0
        self.last_x=0
        self.last_y=0
        if(simtype==1):
            self.init_qtable()   
            self.init_rewardgrid()
        timestep=0
        endgame=False
        totalreward=0
        while (timestep<self.maxstep and endgame!=True):
            self.print_grid()
            if(simtype==0):

                self.det_movement(direction=self.direction)
                if(self.gridmatrix[9][9]==-1):
                    endgame=True
                timestep+=1
            else:
                print("step #" + str(timestep) + "\n")
                self.epsilon_greedy(self.rewardgrid[self.y,self.x])
                self.stoc_movement(direction=self.direction)
                if(self.gridmatrix[9][9]==-1):
                    endgame=True
                timestep+=1
        self.print_grid()

    def init_qtable(self):
        """
        Initialize Q value matrix
        actionsize = 4 for the 4 possible directions
        statesize=100 for all possible 
        """
        actionsize=4 
        state_x=10
        state_y=10
        self.qtable=np.zeros((actionsize,state_x,state_y),dtype=float) 

    def init_rewardgrid(self):
        """
        Initialize reward grid associated with Q-Learning
        Same dimensions as environment grid
        """
        self.rewardgrid=np.zeros((self.max_y,self.max_x))
        self.rewardgrid[self.win[0]-1,self.win[1]-1]=100
        for i in range(self.max_x):
            for j in range(self.max_y):
                if(self.gridmatrix[i][j]==1):
                    self.rewardgrid[i][j]=-20
                if(self.gridmatrix[i][j]==0):
                    self.rewardgrid[i][j]=3


    def epsilon_greedy(self,reward):
        """
        chooses action, updates qtable
        """
        epsilon=0.05
        alpha=0.1   
        gamma=1 
        if np.random.uniform(0,1)<epsilon:
            action=np.random.randint(0, 4)
        else:
            qvals=self.qtable[:,self.y,self.x]
            maxq=np.max(qvals)
            possibles = np.asarray(np.where(qvals==maxq))
            action=np.random.choice(possibles.ravel())
        qval_newstate=self.qtable[:,self.y,self.x]
        maxq_newstate=np.max(qval_newstate)
        curqval=self.qtable[action][self.y][self.x]       
        self.qtable[action][self.last_y][self.last_x]= \
        (1-alpha)*curqval+alpha*(reward+gamma*maxq_newstate) 
        self.direction=action

    def place_obstacles(self,numberofobst=7):
        """
        places an input number of obtacles randomly 
        in the grid
        """
        for i in range(numberofobst):
            while(1):
                x=random.choice(range(9))
                y=random.choice(range(9))
                if(self.gridmatrix[y][x]==0 and 
                not (x==0 and y==0)):
                    self.gridmatrix[y][x]=1
                    break		


    def det_movement(self,direction=0):
        """
        deterministic movement based on A* algorithm
        
        self.last_x=self.x
        self.last_y=self.y 
        self.gridmatrix[self.y][self.x]=0
        if((direction==0) and (self.y<self.max_y-1) and
        (self.gridmatrix[self.y+1][self.x]!=1)):
            self.y += 1
        if((direction==1) and (self.y>0) and
        (self.gridmatrix[self.y-1][self.x]!=1)):
            self.y -= 1
        if((direction==2) and (self.x<self.max_x-1) and
        (self.gridmatrix[self.y][self.x+1]!=1)):
            self.x += 1
        if((direction==3) and (self.x>0) and
        (self.gridmatrix[self.y][self.x-1]!=1)):
            self.x -= 1
        self.gridmatrix[self.y][self.x]=-1
        """

    def stoc_movement(self,direction=0):
        """
        stochastic  movement based on Q-Learning algorithm        
        Inputs:
            directions (dtype:str)
        Outputs:
            None
        """
        self.last_x=self.x
        self.last_y=self.y      
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
        self.gridmatrix[self.y][self.x]=0 # token placement cleaned
        #up
        if((direction==0) and (self.y<self.max_y-1)):
            if(self.gridmatrix[self.y+1][self.x]!=1):
                self.y += 1
                reward=self.rewardgrid[self.y][self.x]
            else:
                reward=self.rewardgrid[self.y][self.x]
                #no movement,hit obstacle,collect reward
        elif (direction==0 and (self.y>=(self.max_y-1))):
            reward=self.rewardgrid[self.y][self.x]
            #no movement,at top of grid,collect reward

        #down
        if((direction==1) and (self.y>0)):
            if(self.gridmatrix[self.y-1][self.x]!=1):
                self.y -= 1
                reward=self.rewardgrid[self.y][self.x]
            else:
                reward=self.rewardgrid[self.y][self.x]
                #no movement,hit obstacle,collect reward
        elif(direction==1 and self.y==0):
            reward=self.rewardgrid[self.y][self.x]
            #no movement,at bottom,collect reward

        #left
        if((direction==2) and (self.x>0)):
            if(self.gridmatrix[self.y][self.x-1]!=1):
                self.x -= 1
                reward=self.rewardgrid[self.y][self.x]
            else:
                reward=self.rewardgrid[self.y][self.x]
                #no movement,hit obstacle,collect reward
        elif((direction==2) and (self.x==0)):
            reward=self.rewardgrid[self.y][self.x]
            #no movement,at far left,collect reward

        #right
        if((direction==3) and (self.x<self.max_x-1)):
            if(self.gridmatrix[self.y][self.x+1]!=1):
                self.x += 1
                reward=self.rewardgrid[self.y][self.x] 
            else:
                reward=self.rewardgrid[self.y][self.x]
                #no movement,hit obstacle,collect reward
        elif((direction==3 and self.x==(self.max_x-1))):
            reward=self.rewardgrid[self.x][self.y]
            #no movement,at far left,collect reward

        #stay still
        if(direction==4):
            # no movement
            reward=self.rewardgrid[self.y][self.x]

        if(direction not in [0,1,2,3,4]):
            print("uh oh /:")
        self.gridmatrix[self.y][self.x]=-1
        #token placement marked
        return reward

    def print_grid(self):
        print("occupancy grid:\n")
        print(self.gridmatrix)
        print("\n"+"reward grid"+"\n")
        print(self.rewardgrid)
        print("\n"+"qtable" + "\n")
        print(self.qtable)
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
        numepisode = int(config['sim']['numepisode'])
    elif (configval is 1):
        simtype=input("Select 0 for deterministic (A* algorithm), 1 for stochastic (Q Learning)\n")
        numobst = input("Enter the number of obstacles\n")
        maxstep = input("Enter the maximum number of timesteps\n")
        numepisode = input("Enter the number of episodes\n")
    obj=sim(simtype,numobst,maxstep,numepisode)
