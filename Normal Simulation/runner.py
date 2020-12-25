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
    waiting_car = []
    
    lane_list = ["143955381#3_0", "143955381#3_1", "143955381#3_2", # each edge has 3 lane
             "24375222#3_0", "24375222#3_1", "24375222#3_2",
              "-23747533#0_0", "-23747533#0_1", "-23747533#0_2",
              "384311993#1_0", "384311993#1_1", "384311993#1_2"]
    
    for x in lane_list:                             # itarate the lanes list and calculates waiting time for each lane
        L0 = traci.lane.getLastStepVehicleIDs(x)    # gets a list of carID waiting on the lane
        for i in L0:                                # iterate in the carID list 
            waitingTimeList.append(traci.vehicle.getWaitingTime(str(i))) # count each car waiting time by carID and in the list
            waiting_car.append(str(i))
        del L0
    return sum(waitingTimeList), len(waiting_car)

import pandas as pd
import csv
def data_write(step, waitingTime, waiting_car):
    # Create the dataframe 
    df = pd.DataFrame({'SIM Time' : step, 
                        'Waiting Time'  : waitingTime,
                        'Waiting Car' : waiting_car,}) 
    df.to_csv('normal_simulation_data.csv') # write a csv file
    print("Ok")


def run():
    getTime_list = []
    getWaitingTime_list = []
    getWaitingCar_list = []
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        #print(traci.simulation.getTime(), ' : ', waitingTimeFunc())
        getTime_list.append(traci.simulation.getTime())
        wt, wc = waitingTimeFunc()
        getWaitingTime_list.append(wt)
        getWaitingCar_list.append(wc)
    data_write(getTime_list, getWaitingTime_list, getWaitingCar_list)
    traci.close()
    sys.stdout.flush()
    print('End of simulation')
    
    
# this function is responsibe for running the simulation
def sumo_config():
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "map.sumo.cfg",])
    print("****************Simulation Started**********************")

    run()

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