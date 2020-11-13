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


# https://sumo.dlr.de/daily/pydoc/traci._simulation.html for getting any info of the simulation
# contains TraCI control loop
#from Q_Learning_agent import Agent as agent # calling Q_Learnign_agent file

def run():
    #getTime_list = []
    #getWaitingTime_list = []
    time = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print(traci.simulation.getTime(), ' : ', waitingTimeFunc())
        if time == 6:
            break
        time += 1
        #agent(traci.simulation.getTime(), waitingTimeFunc())
        #getTime_list.append(traci.simulation.getTime())
        #getWaitingTime_list.append(waitingTimeFunc())
    #data_write(getTime_list, getWaitingTime_list)
    traci.close()
    sys.stdout.flush()
'''
import pandas as pd
import csv
def data_write(getTime_list, getWaitingTime_list):
    # Create the dataframe 
    df = pd.DataFrame({'Time'       : getTime_list, 
                        'Wate'  : getWaitingTime_list}) 
    df.to_csv('set2.csv') # write a csv file
    print("Ok")
'''
# this function is responsibe for running the simulation
def sumo_config():
    while True:
        sumoBinary = checkBinary('sumo')
        traci.start([sumoBinary, "-c", "map.sumo.cfg",
                                 "--tripinfo-output", "tripinfo.xml"])
        run()
        print("**************************************")

# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    # if options.nogui:
    #     sumoBinary = checkBinary('sumo')
    # else:
    #     sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    #traci.start([sumoBinary, "-c", "map.sumo.cfg","--tripinfo-output", "tripinfo.xml"]) # starts traci and take the trip info for other calculation
    sumo_config()