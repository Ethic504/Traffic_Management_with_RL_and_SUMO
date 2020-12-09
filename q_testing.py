from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
from sumolib import checkBinary  # Checks for the binary in environ vars
import traci
import numpy as np
from csv import reader

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
    
    print("******************Running Gui********************")
    
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

def run(q_table):
    action_space = [8, 16, 24, 32, 48, 52, 64]
    while traci.simulation.getMinExpectedNumber() > 0: # step loop in a single episode
        state = int(traci.simulation.getTime())
        action = np.argmax(q_table[state,:]) # and will choose the max value index from the Q-table
        print(action,type(action))
        #ac = action_space[action]
        #generate_light_control_file(ac)
        
    print("Done...")
    traci.close()   # this is to stop the simulation that was running 
    sys.stdout.flush()  # buffer for memory
    
def agent_test():
    # read csv file as a list of lists
    with open('q_table.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        q_table = list(csv_reader)
        print(q_table)
    for episodes in range(3):
        print("Running ", episodes+1, " simulation")
        #run(q_table)
        print(q_table[0][0])
        
    

agent_test()