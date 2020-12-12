from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
from sumolib import checkBinary  # Checks for the binary in environ vars
import traci
import numpy as np
import csv
import time

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
    #while True:
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "map.sumo.cfg",
                              "--tripinfo-output", "tripinfo.xml"])
    
    #print("******************Running Gui********************")
    
# main entry point to sumo
if __name__ == "__main__":
    sumo_config()
    
def generate_light_control_file(action):
    a = action
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

def run(q_table,episodes,action_space):
    
    print("Running Simulation ", episodes)
    count = 0
    while traci.simulation.getMinExpectedNumber() > 0: # step loop in a single episode
        state = int(traci.simulation.getTime())
        try:
            # it will choose the max value index from the Q-table
            #rows_count = len(q_table) # how many row in q_table
            
            a_row = q_table[count]
            max_value = max(a_row)
            index = a_row.index(max_value)
            print(state,"   The max value ",max_value, " and Index in ",index)
            count += 1
            #print(state,type(state))
        except ValueError:
            time.sleep(1)
            print("The q_table empty")
            time.sleep(1)
            break
        
        action = action_space[index]
        generate_light_control_file(action)
        traci.simulationStep() # performs a simulation step

    traci.close()   # this is to stop the simulation that was running 
    sys.stdout.flush()  # buffer for memory
    time.sleep(1)
    
    
def agent_test():
    # read csv file as a list of lists
    q_table = list(csv.reader(open('q_table.csv')))
    q_table = [list( map(float,i) ) for i in q_table] # convert list of string into list of integer
    action_space = [8, 16, 24, 32, 48, 52, 64]
    print(q_table)
    for episodes in range(3):
        run(q_table,episodes,action_space)
        print("Done  ", episodes)
        sumo_config()
    

agent_test()




























