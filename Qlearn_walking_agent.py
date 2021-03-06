import numpy as np
import random
import configparser 
import sys
import seaborn as sns
import time
import matplotlib.pyplot as plt
plt.ion()

class sim:

    def __init__(self, numbost, maxstep, numepisode, alpha, gamma, max_x, max_y):
        """
        2D grid platform for agent to walk through,
        each "cell" of the grid is either free or occupied.
        A 0 will represent free and 1 will represent a trap.
        -1 will represent where the agent is
        """
        # Initial values
        self.max_x=max_x
        self.max_y=max_y
        # Roll for random starting point
        self.start_x=np.random.randint(0,max_x-1)
        self.start_y=np.random.randint(0,max_y)
        self.maxstep=maxstep
        self.x=self.start_x
        self.y=self.start_y
        #winning block always along right side
        self.win=(max_x,np.random.randint(0,max_y))
        self.won=False
        dimensions=(max_y,max_x)
        # Initialize occupancy grid
        self.gridmatrix=np.zeros(dimensions,dtype=int)
        # Place obstacles on grid
        self.place_obstacles(numberofobst=int(numobst))
        # Create evaluation arrays
        self.total_rewards=np.zeros((numepisode),dtype=float)
        self.numsteps2win=np.zeros((numepisode),dtype=int)
        #Set agent on grid, -1 will indicate agent
        self.gridmatrix[self.start_y][self.start_x]=-1
        #Initialize Q-table and reward grid
        self.init_qtable()   
        self.init_rewardgrid()
        #Set goal on grid, -2 will indicate goal
        self.gridmatrix[self.win[1]-1,self.win[0]-1]=-2
        #Initialize Q-learning values
        self.alpha = alpha
        self.gamma = gamma
        for i in range(numepisode):
            print("Episode #" + str(i+1) + "\n")
            while(1):
                x=np.random.randint(0,max_x-1)
                y=np.random.randint(0,max_y)
                if(self.gridmatrix[y][x]!=1):
                    self.start_x=x
                    self.start_y=y
                    break
            self.start(i)
        self.eval(numepisode)
        self.testagent()

    def start(self,i):
        self.x=self.start_x
        self.y=self.start_y
        self.direction=0
        timestep=0
        totalreward=0
        endgame=False
        self.won=False
        totalreward=0 
        while (timestep<self.maxstep and endgame!=True):
            timestep+=1
            print("step #" + str(timestep))
            action=self.choose_action()
            old_state=self.currentlocation2state()
            action,reward=self.stoc_movement(direction=action)
            totalreward+=reward
            new_state=self.currentlocation2state()
            self.update_qtable(old_state=old_state, \
            new_state=new_state,reward=reward,action=action)
            if(self.gridmatrix[self.win[1]-1][self.win[0]-1]==-1):
                endgame=True
                self.won=True
                self.print_grid()
                print("winner :) \n\n\n")
                self.numsteps2win[i]=timestep
                self.total_rewards[i]=totalreward
                self.gridmatrix[self.win[1]-1][self.win[0]-1]=-2
        if(self.won==False):
            self.numsteps2win[i]=timestep
            self.total_rewards[i]=totalreward
            self.gridmatrix[self.y][self.x]=0

    def testagent(self):
        for i in range(2):
            self.start_noupdate()

    def start_noupdate(self):
        self.x=self.start_x
        self.y=self.start_y
        self.direction=0
        timestep=0
        endgame=False
        self.won=False
        while (timestep<self.maxstep and endgame!=True):
            timestep+=1
            print("step #" + str(timestep))
            action=self.choose_action()
            old_state=self.currentlocation2state()
            action,reward=self.stoc_movement(direction=action)
            self.print_grid()
            time.sleep(1)
            if(self.gridmatrix[self.win[1]-1][self.win[0]-1]==-1):
                endgame=True
                self.won=True
                self.print_grid()
                print("winner :) \n\n\n")
                self.gridmatrix[self.win[1]-1][self.win[0]-1]=-2
                time.sleep(5)

    def init_qtable(self):
        """
        Initialize empty Q value matrix: self.qtable[actionsize][statesize]
        actionsize = 5 for the 5 possible directions 
        statesize = total number of grid elements
        """
        actionsize=5 
        self.qtable=np.zeros((self.max_x*self.max_y,actionsize),dtype=float) 

    def init_rewardgrid(self):
        """
        Initialize reward grid associated with Q-Learning
        Fills self.qtable
        """
        self.rewardgrid=np.zeros((self.max_y,self.max_x))
        for i in range(self.max_x):
            for j in range(self.max_y):
                if(self.gridmatrix[j][i]==0 or \
                self.gridmatrix[j][i]==-1):
                    self.rewardgrid[j][i]=-0.5
        self.rewardgrid[self.win[1]-1,self.win[0]-1]=100

    def choose_action(self):
        """
        Epsilon Greedy algorithm to select action
        """
        #choose action
        epsilon=0.05
        if np.random.uniform(0,1)<epsilon:
            action=np.random.randint(0, 4)
        else:
            state=self.currentlocation2state()
            qvals=self.qtable[state]
            maxq=np.max(qvals)
            possibles = np.asarray(np.where(qvals==maxq)).ravel()
            action=np.random.choice(possibles)
        return action

    def currentlocation2state(self):
        """
        converts x,y coordinates to corresponding state value
        """
        state=self.y*self.max_y+self.x
        return state

    def update_qtable(self,old_state,new_state,reward,action):
        """
        updates qtable
        """    
        qval_newstate=self.qtable[new_state]
        maxq_newstate=np.max(qval_newstate)
        curqval=self.qtable[old_state][action]      
        self.qtable[old_state][action]= \
        (1-self.alpha)*curqval+self.alpha*\
        (reward+self.gamma*maxq_newstate) 

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

    def stoc_movement(self,direction=0):
        """
        stochastic  movement based on Q-Learning algorithm
        """
        r=random.random()
        if (r<0.6):
            # commence direction as commanded
            pass
        if (r>=0.6 and r<0.7):
            #change direction
            direction=(direction+1)%5
            print("CHANGE ACTION, now:"+str(direction))
        if (r>=0.7 and r<0.8):
            #change direction
            direction=(direction+2)%5
            print("CHANGE ACTION, now:"+str(direction))
        # change direction
        if (r>=0.8 and r<0.9):
            #change direction
            direction=(direction+3)%5
            print("CHANGE ACTION, now:"+str(direction))
        # change direction
        if (r>=0.9 and r<=1.0):
            #stay in same spot
            direction=4
            print("CHANGE ACTION, now:"+str(direction))
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
            reward=self.rewardgrid[self.y][self.x]
            #no movement,at far left,collect reward

        #stay still
        if(direction==4):
            # no movement
            reward=self.rewardgrid[self.y][self.x]

        self.gridmatrix[self.y][self.x]=-1
        #token placement marked
        return direction,reward

    def print_grid(self):
        print("occupancy grid:\n")
        print(np.flip(self.gridmatrix,0))
        #print("\n"+"reward grid"+"\n")
        #print(np.flip(self.rewardgrid,0))
        #print("\n"+"qtable" + "\n")
        #print(self.qtable)
        #print("\n")


    def eval(self,numepisodes):
        x=range(1,numepisodes+1,1)
        plt.plot(x,self.numsteps2win)
        plt.title("Number of timesteps to win")
        plt.xlabel("Episode number")
        plt.ylabel("# timesteps to win")
        plt.xticks(np.arange(min(x),max(x)+1,int(max(x)/20)))
        plt.savefig("results/Q-Learn_steps_to_win.png")
        plt.clf()
        plt.plot(x,self.total_rewards)
        plt.title("Total rewards")
        plt.xlabel("Episode number")
        plt.ylabel("Total reward claimed")
        plt.xticks(np.arange(min(x),max(x)+1,int(max(x)/20)))
        plt.savefig("results/Q-Learn_total_rewards.png")
        np.savetxt("results/Q-Learning_grid",self.gridmatrix,fmt='%d')
        np.savetxt("results/final_Qtable",self.qtable,fmt='%.2f',header="up, down, left, right, no move")
        plt.clf()
        ax=sns.heatmap(self.qtable,linewidth=0.5,cmap="YlGnBu")
        plt.savefig("results/qtable.png")



if __name__ == "__main__":
    try:
        configval=sys.argv[1]
        # -c for configuration file, -i for user input
    except:
        print("make sure to include -c for config file or -i for user input")
    if configval == "-c":
        config=configparser.ConfigParser()
        config.read('values.conf')
        numobst    = int(config['sim']['numobst'])
        max_x      = int(config['sim']['max_x'])
        max_y      = int(config['sim']['max_y'])
        maxstep    = int(config['Q-Learn']['maxstep'])
        numepisode = int(config['Q-Learn']['numepisode'])
        alpha      = float(config['Q-Learn']['alpha'])
        gamma      = float(config['Q-Learn']['gamma'])
    elif configval == "-i":
        numobst    = input("Enter the number of obstacles\n")
        maxstep    = input("Enter the maximum number of timesteps\n")
        numepisode = input("Enter the number of episodes\n")
        alpha      = input("Enter the learning rate (alpha)\n")
        gamma      = input("Enter the discount (gamma)\n") 
        max_x      = input("Enter the max x value for the grid\n")
        max_y      = input("Enter the max y value for the grid\n") 
    obj=sim(numobst,maxstep,numepisode,alpha,gamma,max_x,max_y)
