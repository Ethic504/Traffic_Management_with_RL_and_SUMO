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

# this function is responsibe for running the simulation
def sumo_config():
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "map.sumo.cfg",
                              "--tripinfo-output", "tripinfo.xml"])
    
    print("******************Running Gui********************")
    
# main entry point to sumo
if __name__ == "__main__":
    sumo_config()
   
#--------------------------------------------------------------------------#

def generate_light_control_file(road,action):
    # road a is connected to junction 1575361842 and lanes starts with 143955381
    # road b is connected to junction 1575325597 and lanes starts with 24375222
    # road c is connected to junction 210330099 and lanes starts with -23747533
    # road d is connected to junction 1693014276 and lanes starts with 384311993
    a = action[0] # array to integer
    if road == 0: # for road a
        with open("light_control1_shortest_path.add.xml", "w") as lights:
            print('<additional>>', file = lights)
            # road a
            print('<tlLogic id="1575361842" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road b
            print('<tlLogic id="1575325597" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road c
            print('<tlLogic id="210330099" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="GGGggg"/>' %(a), file = lights)
            print('<phase duration="6"  state="yyyggg"/>', file = lights)
            print('<phase duration="%a" state="rrrggg"/>' %(a), file = lights)
            print('<phase duration="6"  state="rrrggg"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road d
            print('<tlLogic id="1693014276" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggrrr"/>', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            
            print('</additional>', file = lights)

    elif road == 1:
        with open("light_control1_shortest_path.add.xml", "w") as lights:
            print('<additional>>', file = lights)
            # road b
            print('<tlLogic id="1575325597" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road a
            print('<tlLogic id="1575361842" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road c
            print('<tlLogic id="210330099" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="GGGggg"/>' %(a), file = lights)
            print('<phase duration="6"  state="yyyggg"/>', file = lights)
            print('<phase duration="%a" state="rrrggg"/>' %(a), file = lights)
            print('<phase duration="6"  state="rrrggg"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road d
            print('<tlLogic id="1693014276" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggrrr"/>', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            
            print('</additional>', file = lights)
            
    elif road == 2:
        with open("light_control1_shortest_path.add.xml", "w") as lights:
            print('<additional>>', file = lights)
            # road c
            print('<tlLogic id="210330099" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="GGGggg"/>' %(a), file = lights)
            print('<phase duration="6"  state="yyyggg"/>', file = lights)
            print('<phase duration="%a" state="rrrggg"/>' %(a), file = lights)
            print('<phase duration="6"  state="rrrggg"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road a
            print('<tlLogic id="1575361842" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road b
            print('<tlLogic id="1575325597" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road d
            print('<tlLogic id="1693014276" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggrrr"/>', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            
            print('</additional>', file = lights)
    
    elif road == 3:
        with open("light_control1_shortest_path.add.xml", "w") as lights:
            print('<additional>>', file = lights)
            # road d
            print('<tlLogic id="1693014276" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggrrr"/>', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road a
            print('<tlLogic id="1575361842" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road b
            print('<tlLogic id="1575325597" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="gggrrr"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('<phase duration="%a" state="gggGGG"/>' %(a), file = lights)
            print('<phase duration="6"  state="gggyyy"/>', file = lights)
            print('</tlLogic>', file = lights)
            # road c
            print('<tlLogic id="210330099" type="static" programID="2" offset="0">', file = lights)
            print('<phase duration="%a" state="GGGggg"/>' %(a), file = lights)
            print('<phase duration="6"  state="yyyggg"/>', file = lights)
            print('<phase duration="%a" state="rrrggg"/>' %(a), file = lights)
            print('<phase duration="6"  state="rrrggg"/>', file = lights)
            print('</tlLogic>', file = lights)
            
            print('</additional>', file = lights)
    return a

def waitingTime():
    a_road_waiting_time = []
    b_road_waiting_time = []
    c_road_waiting_time = []
    d_road_waiting_time = []
    waiting_car = []
    
    a_road = ["143955381#3_0", "143955381#3_1", "143955381#3_2"]
    b_road = ["24375222#3_0", "24375222#3_1", "24375222#3_2"]
    c_road = ["-23747533#0_0", "-23747533#0_1", "-23747533#0_2"]
    d_road = ["384311993#1_0", "384311993#1_1", "384311993#1_2"]
    
    for x in a_road:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            a_road_waiting_time.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        waiting_car.append(L0)
        del L0
    for x in b_road:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            b_road_waiting_time.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        waiting_car.append(L0)
        del L0
    for x in c_road:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            c_road_waiting_time.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        waiting_car.append(L0)
        del L0
    for x in d_road:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            d_road_waiting_time.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        waiting_car.append(L0)
        del L0
    return sum(a_road_waiting_time), sum(b_road_waiting_time), sum(c_road_waiting_time), sum(d_road_waiting_time), sum(waiting_car)

def select_road(li):
    road = li.index(max(li)) # which road to choose to open and has max waiting time
    return road
          
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

import pandas as pd
import csv
def data_write(step, waitingTime, waitingCar, action, reward):
    # Create the dataframe 
    df = pd.DataFrame({'Step'       : step, 
                        'Waiting Time'  : waitingTime,
                        'Waiting Car' : waitingCar,
                        'Action' : action,
                        'Reward'  : reward,}) 
    df.to_csv('shortest_path_dataset.csv') # write a csv file
    print("Leaving Simulation...")
            
# traCI runner
def run():
    action_space = [8, 16, 24, 32, 48, 52, 64]
    step_list = []
    waiting_list = []
    action_list = []
    reward_list = []
    
    while traci.simulation.getMinExpectedNumber() > 0: # step loop in a single episode
        a_road_waiting_time, b_road_waiting_time, c_road_waiting_time, d_road_waiting_time, waiting_car = waitingTime()
        # print(state, a_road_waiting_time, b_road_waiting_time, c_road_waiting_time, d_road_waiting_time)
        road = select_road([a_road_waiting_time, b_road_waiting_time, c_road_waiting_time, d_road_waiting_time])
        
        action = random.sample(action_space, 1) # gives a random value as array
        generate_light_control_file(road, action)
        #generate_light_control_file() # responsible for writing the traffic control file
        traci.simulationStep() # performs a simulation step
        
        state = int(traci.simulation.getTime())
        total_waiting_time = sum([a_road_waiting_time, b_road_waiting_time, c_road_waiting_time, d_road_waiting_time])
        step_list.append(state)
        waiting_list.append(total_waiting_time)
        action_list.append(action)
        reward_list.append(total_waiting_time)
        
    data_write(step_list, waiting_list, waiting_car, action_list, reward_list)
    del reward_list
    traci.close()   # this is to stop the simulation that was running 
    sys.stdout.flush()  # buffer for memory
    
    
    
def main():
    run()
    
main()