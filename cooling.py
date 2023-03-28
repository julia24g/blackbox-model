### Equations ###

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

BTU_CONVERT = 3412.142 # rate we need to multiply kW heating demand by to get BTU/hr

## Cooling
table1 = np.loadtxt("cooling_capacity.csv")
model_table = np.genfromtxt('models.csv', dtype='str') # names of the models associated with rated capacity

# Selects an HP based on cooling demand in kW
def selectHP(cooling_demand_kW):
    cooling_demand = cooling_demand_kW * BTU_CONVERT # first, convert heating demand in kW to BTU/hr
    ratedCapacity = None # placeholder for selected heat pump

    for i in range(len(table1[0])):  # iterate through rated capacity columns until we find the rated capacity that satisfies heating demand
        if table1[0][i] >= cooling_demand:
            ratedCapacity = table1[0][i]
            break
    
    for row in model_table: # looking for the model name based on the selected rated capacity
        if ratedCapacity == float(row[0]):
            print("Selected heat pump: Goodman Heat Pump Model", row[1]) # this returns the model name eg. 0181B
        
    return ratedCapacity # returns rated capacity in BTU/hr

# Cooling COP function
def heatingCOP(ti, tiwb, to, ratedCapacity):
    cooling_load = ratedCapacity # selects the heat pump

    for i in range(len(table1[0])):
        if table1[0][i] >= cooling_load:
            return round(table1[15][i] + table1[16][i]*ti + table1[17][i]*tiwb + table1[18][i]*to + table1[19][i]*ti*tiwb + table1[20][i]*ti*to + table1[21][i]*tiwb*to + table1[22][i]*ti**2 + table1[23][i]*tiwb**2 + table1[24][i]*to**2 + table1[25][i]*ti**2*to + table1[26][i]*tiwb**2*to + table1[27][i]*ti*to*tiwb, 6)
        

# Cooling Load function
def heatingCapacity(ti, tiwb, to, ratedCapacity):
    cooling_load = ratedCapacity # selects the heat pump
    for i in range(len(table1[0])):
        if table1[0][i] >= cooling_load:
            return round(table1[1][i] + table1[2][i]*ti + table1[3][i]*tiwb + table1[4][i]*to + table1[5][i]*ti*tiwb + table1[6][i]*ti*to + table1[7][i]*tiwb*to + table1[8][i]*ti**2 + table1[9][i]*tiwb**2 + table1[10][i]*to**2 + table1[11][i]*ti**2*to + table1[12][i]*tiwb**2*to + table1[13][i]*ti*to*tiwb, 6)
        



## User Input ##