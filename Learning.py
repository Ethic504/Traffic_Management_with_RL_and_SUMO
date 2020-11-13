import os
import sys
import optparse

# import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

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
    waitingTimeList.clear()
    
# main sumo runner and act as single episode each time it is called
def run(q_table,exploration_rate):
    action_space = ('grgr 8', 'grgr 16', 'grgr 32', 'grgr 48',
                    'rgrg 8', 'rgrg 16', 'rgrg 32', 'rgrg 48'
                    'gggg 0')
    while traci.simulation.getMinExpectedNumber() > 0: # step loop in a single episode
        traci.simulationStep()
        #print(traci.simulation.getTime(), ' : ', waitingTimeFunc())
        state = traci.simulation.getTime()
        exploration_rate_threshold = random.uniform(0, 1) # set the exploration thrasehold random in between 0 to 1, this will help the agent so take decission for going exploration or exploatation 
        if exploration_rate_threshold > exploration_rate: # agent will exploite the environment 
            action = np.argmax(q_table[state,:]) # and will choose the max value for the action from the Q-table
            generate_light_control_file(action)
        else: # agent will explore the environment 
            action = random.sample(action_space,1) # and sample an action randomly/takes new action
                    #random.sample(action_space,1) # taking a single action from the touple as string
            generate_light_control_file(action)
    
    traci.close()   # this is to stop the simulation that was running 
    sys.stdout.flush()  # buffer for memory

def generate_light_control_file(action):
    
    with open("light_control1.add.xml", "w") as lights:
        print("""<additional>
              """
            )
    pass

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
import gym
import random
import time
from IPython.display import clear_output
def agent():  
    action_space_size = 8 # 4 traffic light 
    state_space_size = 100
    q_table = np.zeros((state_space_size, action_space_size))
    #print(q_table)
    
    num_episodes = 1000             # number of episode
    max_steps_per_episode = 1000     # number of step per episode
    
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
        run(q_table,exploration_rate)
        # Exploration rate decay
        exploration_rate = min_exploration_rate + \
            (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
            
        rewards_all_episodes.append(rewards_current_episode) # update the reward list for each episode

                
    
    
agent()    
    
'''
dum = ['grgr 8', 'grgr 16', 'grgr 32', 'grgr 48',
       'rgrg 8', 'rgrg 16', 'rgrg 32', 'rgrg 48']

for i in range(10):
    x = random.sample(dum, 2)
    print(x)
'''    
    
    
    
    
    
    
    
    