from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

# import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# this function calculates the total waiting time of a step in the intersectio on 4 edge
def waitingTimeFunc():
    waitingTimeList = []
    lane_list = ["143955381#3_0", "143955381#3_1", "143955381#3_2", # each edge has 3 lane
             "24375222#3_0", "24375222#3_1", "24375222#3_2",
              "-23747533#0_0", "-23747533#0_1", "-23747533#0_2",
              "384311993#1_0", "384311993#1_1", "384311993#1_2"]
    
    for x in lane_list:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            waitingTimeList.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        del L0
    return sum(waitingTimeList)
   
def rewardFunc(waitingTime):
    if waitingTime > 500:
        reWoRdd = -1
    elif waitingTime < 200:
        reWoRdd = 10
    elif waitingTime > 200 and waitingTime < 500:
        reWoRdd = 5
    else:
        reWoRdd = -10
    return reWoRdd
    
# main sumo runner and act as single episode each time it is called
def run(q_table,exploration_rate,learning_rate,discount_rate):
    time_list = []
    waiting_list = []
    action_list = []
    reward_list = []
    action_space = (8, 16, 24, 32, 48, 52, 64)
    column = 0
    while traci.simulation.getMinExpectedNumber() > 0: # step loop in a single episode
        
        #print(traci.simulation.getTime(), ' : ', waitingTimeFunc())
        state = int(traci.simulation.getTime())
        exploration_rate_threshold = random.uniform(0, 1) # set the exploration thrasehold random in between 0 to 1, this will help the agent so take decission for going exploration or exploatation 
        if exploration_rate_threshold > exploration_rate: # agent will exploite the environment 
            action = np.argmax(q_table[state,:]) # and will choose the max value index from the Q-table
            generate_light_control_file(action_space[action]) 
            
        else: # agent will explore the environment 
            action = random.sample(action_space,1) # and sample an action randomly/takes new action
                    #random.sample(action_space,1) # taking a single action from the touple as string
            int_action = action[0] # action is a list of 0 index so we made a variable from it
            column = action_space.index(int_action) # 
            generate_light_control_file(int_action) # sending action as a list with 1 element
        traci.simulationStep() # performs a simulation step
        new_state = int(traci.simulation.getTime()) # 
        reward = rewardFunc(waitingTimeFunc())
        
        
        #print(state,int_action,new_state)
        #print(type(reward),type(state), type(new_state),type(int_action))
        
        
        
        # update Q-table
        q_table[state,column] = q_table[state,column] * (1-learning_rate) + learning_rate * (reward + discount_rate * np.max(q_table[int(new_state),:]))
        
        #print(traci.simulation.getTime(), ' : ', waitingTimeFunc(),' : ', action)
        time_list.append(traci.simulation.getTime())
        waiting_list.append(waitingTimeFunc())
        action_list.append(action)
        reward_list.append(reward)
    data_write(time_list, waiting_list, action_list,reward_list, sum(reward_list))
    traci.close()   # this is to stop the simulation that was running 
    sys.stdout.flush()  # buffer for memory
    print("Reward is ",sum(reward_list))
    return q_table

import pandas as pd
import csv
def data_write(Time, waitingTime, action, reward, su):
    # Create the dataframe 
    df = pd.DataFrame({'Time'       : Time, 
                        'Wate'  : waitingTime,
                        'Action' : action,
                        'Reward'  : reward,
                        'Sum_reward': su,}) 
    df.to_csv('action_list.csv') # write a csv file
    print("Leaving Simulation...")

def generate_light_control_file(int_action):
    a = int_action
    #print(a)
    with open("light_control1.add.xml", "w") as lights:
        print('<additional>>', file = lights)
        print('<tlLogic id="1575325597" type="static" programID="2" offset="0">', file = lights)
        print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
        print('<phase duration="6"  state="gggyyy"/>', file = lights)
        print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
        print('<phase duration="6"  state="gggyyy"/>', file = lights)
        print('</tlLogic>', file = lights)
        print('<tlLogic id="1575361842" type="static" programID="2" offset="0">', file = lights)
        print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
        print('<phase duration="6"  state="gggyyy"/>', file = lights)
        print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
        print('<phase duration="6"  state="gggyyy"/>', file = lights)
        print('</tlLogic>', file = lights)
        print('<tlLogic id="1693014276" type="static" programID="2" offset="0">', file = lights)
        print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
        print('<phase duration="6"  state="gggrrr"/>', file = lights)
        print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
        print('<phase duration="6"  state="gggyyy"/>', file = lights)
        print('</tlLogic>', file = lights)
        print('<tlLogic id="210330099" type="static" programID="2" offset="0">', file = lights)
        print('<phase duration="%a" state="GGGggg"/>' %(a), file = lights)
        print('<phase duration="6"  state="yyyggg"/>', file = lights)
        print('<phase duration="%a" state="rrrggg"/>' %(a), file = lights)
        print('<phase duration="6"  state="rrrggg"/>', file = lights)
        print('</tlLogic>', file = lights)
        print('</additional>', file = lights)

def q_table_to_csv(q_table):
    # field names  
    fields = [8, 16, 24, 32, 48, 52, 64]   
      
    with open('q_table.csv', 'w') as f: 
          
        # using csv.writer method from CSV package 
        write = csv.writer(f) 
          
        #write.writerow(fields) 
        write.writerows(q_table) 

# this function is responsibe for running the simulation
def sumo_config():
    #while True:
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "map.sumo.cfg",
                             "--tripinfo-output", "tripinfo.xml"])
    
    print("******************Running Gui********************")
    

# main entry point to sumo
if __name__ == "__main__":
    sumo_config()
    
#***************************************************************************
import numpy as np
#import time
def agent_train():  
    action_space_size = 7
    state_space_size = 2000
    q_table = np.zeros((state_space_size, action_space_size)) # row & column
    #print(q_table)
    
    num_episodes = 100            # number of episode
    #max_steps_per_episode = 100     # number of step per episode
    
    learning_rate = 0.1             # value of alpha
    discount_rate = 0.99            # value of lamda
    
    # efsolon greedy stratagy 
    exploration_rate = 1
    max_exploration_rate = 1
    min_exploration_rate = 0.01
    exploration_decay_rate = 0.001
    
    rewards_all_episodes = []
    
    # Q-learning algorithm
    for episode in range(num_episodes): # this loop contains everything for a single episode
        #sumo_config()
        rewards_current_episode = 0 # reword with in the current episode and for every new episode it sets to 0 and get updated in the episode loop              
        print("Running ", episode, " simulation")
        run(q_table,exploration_rate,learning_rate,discount_rate)
        sumo_config()
        # Exploration rate decay
        exploration_rate = min_exploration_rate + \
             (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
            
        rewards_all_episodes.append(rewards_current_episode) # update the reward list for each episode
    #print(q_table)           
    q_table_to_csv(q_table) # to take Q-table in csv file
    
    # reward_per_hun_epi = np.split(np.array(rewards_all_episodes),num_episodes/100)
    # count = 100
    # for r in reward_per_hun_epi:
    #     print(count, ' : ', str(sum(r/100)))
    #     count += 100
    
agent_train()  
    
'''
dum = (0, 8, 16, 24, 32, 48, 52, 64)
action_space = ('grgr 8', 'grgr 16', 'grgr 32', 'grgr 48',
                    'rgrg 8', 'rgrg 16', 'rgrg 32', 'rgrg 48'
                    'gggg 0')
for i in range(10):
    x = random.sample(dum, 2)
    print(x)
'''     