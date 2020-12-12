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
    #while True:
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "map.sumo.cfg",
                              "--tripinfo-output", "tripinfo.xml"])
    
    #print("******************Running Gui********************")
    
# main entry point to sumo
if __name__ == "__main__":
    sumo_config()
   
#--------------------------------------------------------------------------#

def waitingTime():
    a_road_waiting_time = []
    b_road_waiting_time = []
    c_road_waiting_time = []
    d_road_waiting_time = []
    
    a_road = ["143955381#3_0", "143955381#3_1", "143955381#3_2"]
    b_road = ["24375222#3_0", "24375222#3_1", "24375222#3_2"]
    c_road = ["-23747533#0_0", "-23747533#0_1", "-23747533#0_2"]
    d_road = ["384311993#1_0", "384311993#1_1", "384311993#1_2"]
    
    for x in a_road:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            a_road_waiting_time.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        del L0
    for x in b_road:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            b_road_waiting_time.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        del L0
    for x in c_road:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            c_road_waiting_time.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        del L0
    for x in d_road:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            d_road_waiting_time.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
        del L0
    return sum(a_road_waiting_time), sum(b_road_waiting_time), sum(c_road_waiting_time), sum(d_road_waiting_time)

def select_road(li):
    return li.index(max(li))

def generate_light_control_file():
    # road a is connected to junction 1575361842 and lanes starts with 143955381
    # road b is connected to junction 1575325597 and lanes starts with 24375222
    # road c is connected to junction 210330099 and lanes starts with -23747533
    # road d is connected to junction 1693014276 and lanes starts with 384311993

    with open("light_control1_shortest_path.add.xml", "w") as lights:
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
    pass

# traCI runner
def run():
    while traci.simulation.getMinExpectedNumber() > 0: # step loop in a single episode
        state = int(traci.simulation.getTime())
        a_road_waiting_time, b_road_waiting_time, c_road_waiting_time, d_road_waiting_time = waitingTime()
        # print(state, a_road_waiting_time, b_road_waiting_time, c_road_waiting_time, d_road_waiting_time)
        print(select_road([a_road_waiting_time, b_road_waiting_time, c_road_waiting_time, d_road_waiting_time]))
        generate_light_control_file() # responsible for writing the traffic control file
        traci.simulationStep() # performs a simulation step
        
    traci.close()   # this is to stop the simulation that was running 
    sys.stdout.flush()  # buffer for memory
    
def main():
    run()
    
main()