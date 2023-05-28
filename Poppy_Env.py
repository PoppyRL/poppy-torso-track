#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import gym
import numpy as np
from gym import spaces
from tqdm import tqdm



# In[2]:


import numpy as np
from utils.skeleton import *
from utils.quaternion import *
from utils.blazepose import blazepose_skeletons
import os
from pypot.creatures import PoppyTorso
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
#from pypot.creatures.ik import IKChain
from pypot.primitive.move import Move
from pypot.primitive.move import MovePlayer




class PoppyEnv(gym.Env):

    def __init__(self,
                 goals=2,
                 terminates=True):
       
        print("Hello, I am Poppy!")
        
        from pypot import vrep
        vrep.close_all_connections()
        self.poppy = PoppyTorso(simulator='vrep')
        
        self.n_goals = goals
      
        self.terminates = terminates

        self.goals_done = 0
        self.is_initialized = False
      
        self.goal = None
        self.goal_positions = []
        self.goal_distances = []
        
        self.episodes = 0  # used for resetting the sim every so often
        self.restart_every_n_episodes = 1000
        
        # observation = 6 joints + 6 velocities + 3 coordinates for target
        self.observation_space_l = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)  #
        
        # action = 6 joint angles
        self.action_space_l = spaces.Box(low=0, high=180, shape=(7,), dtype=np.float32)  #

        super().__init__()
        
      
    
    def seed(self, seed=None):
        return [np.random.seed(seed)]
    

    def one_step(self, action_l, action_r):
        
        
        
        
        for k,m in enumerate(self.poppy.l_arm_chain.motors):
            if (m.name != 'abs_z') and (m.name != 'bust_y') and (m.name != 'bust_x'):   
                        m.goto_position(action_l[k],5)
                        print(m)
            else:
                        m.goto_position(0.0,5)
                    
                    
        for k,m in enumerate(self.poppy.r_arm_chain.motors):
            if (m.name != 'abs_z') and (m.name != 'bust_y') and (m.name != 'bust_x'):   
                        m.goto_position(action_r[k],5)
                        print(m)
            else:
                        m.goto_position(0.0,5)             
                    
                    
        
        obs = self.get_obs()      

        return obs
    
    def reset(self):
        joint_pos = { 'l_elbow_y':0.0,
                     'head_y': 0.0,
                     'r_arm_z': 0.0, 
                     'head_z': 0.0,
                     'r_shoulder_x': 0.0, 
                     'r_shoulder_y': 0.0,
                     'r_elbow_y': 0.0, 
                     'l_arm_z': 0.0,
                     'abs_z': 0.0,
                     'bust_y': 0.0, 
                     'bust_x':0.0,
                     'l_shoulder_x': 0.0,
                     'l_shoulder_y': 0.0
                    }
        for m in self.poppy.motors:
               m.goto_position(joint_pos[m.name],5)
                
    def get_obs(self):
       
        return self.poppy.l_arm_chain.position, self.poppy.r_arm_chain.position

    
    def get_state(self):
        
        return self.poppy.l_arm_chain.joints_position, self.poppy.r_arm_chain.joints_position    
    