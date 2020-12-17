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
    