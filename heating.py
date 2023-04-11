### Equations ###

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from House_Heating_Load_Model import returnHeatingLoad

BTU_CONVERT = 3412.142 # rate we need to multiply kW heating demand by to get BTU/hr

## Heating
table1 = np.loadtxt("heating_capacity.csv")
model_table = np.genfromtxt('models.csv', dtype='str')

# Selects an HP based on heating demand in kW
def selectHP(heating_demand_kW):
    heating_demand = heating_demand_kW * BTU_CONVERT # first, convert heating demand in kW to BTU/hr
    hp = None # placeholder for selected heat pump

    for ratedCapacity in table1:  # iterate through rated capacity columns until we find the rated capacity that satisfies heating demand
        if ratedCapacity[0] >= heating_demand:
            hp = ratedCapacity[0]
            break
    
    for row in model_table: # looking for the model name based on the selected rated capacity
        if hp == float(row[0]):
            print("Selected heat pump: Goodman Heat Pump Model", row[1]) # this returns the model name eg. 0181B
        
    return ratedCapacity[0] # returns rated capacity in BTU/hr

# Heating COP function with input of ambient temperature and heating demand (BTU/hr)
def heatingCOP(t, ratedCapacity):
    heating_demand = ratedCapacity # selects the heat pump

    for ratedCapacity in table1:
        if ratedCapacity[0] >= heating_demand:
            return round(ratedCapacity[5] + ratedCapacity[6]*t + ratedCapacity[7]*t**2, 6)


# Heating Capacity function with input of ambient temperature and heating demand (BTU/hr)
def heatingCapacity(t, ratedCapacity):
    heating_demand = ratedCapacity
    for ratedCapacity in table1:
        if ratedCapacity[0] > heating_demand:
            return round(ratedCapacity[1] + ratedCapacity[2]*t + ratedCapacity[3]*t**2, 6)
        




### User Input ###

# heating_demand = input("Please input your maximum heating demand (in kW) on the coldest day of the year: ")
# ambient_temp = float(input("Please input the ambient temperature (in Celsius): "))

# print()

# print("Heating COP: ", heatingCOP(float(ambient_temp), float(ratedCapacity)))

## Ask user for ambient temperature OR list of ambient temperatures for each day or each hour - calculate COP on each hour
temp_table = np.genfromtxt('2020temp.csv', dtype='str')

print("Calculating COP for 365 days and 24 hours a day")
heating_demand = input("Please input your maximum heating demand (in kW) on the coldest day of the year: ")
ratedCapacity = selectHP(float(heating_demand))
print()

annualCOP = [[0 for i in range(24)] for j in range(365)]

for i in range(365):
    for j in range(24):
        annualCOP[i][j] = heatingCOP(float(temp_table[i][j]), float(ratedCapacity))

print("Annual COP: ")


## Using heating demand from House Heating Load Model ## 
heatingLoad = returnHeatingLoad() # getting heating load from House Heating Load Model
hd_table = np.full((365, 24), heatingLoad) # filling hourly matrix with value from heating load

print("Calculating heating capacity for 365 days and 24 hours a day using temperature file and heating demand file.")
print()

annualHeatingCapacity = [[0 for i in range(24)] for j in range(365)]

for i in range(365):
    for j in range(24):
        annualHeatingCapacity[i][j] = heatingCapacity(float(temp_table[i][j]), float(hd_table[i][j])) # iterating through both temperature matrix and heating demand matrix

# Convert heating demand and heating capacity into daily (either average or summation), and graph those two lines daily for the entire year
dailyHeatingCapacity = []

for i in range(365): # going through each day of the year
    average = sum(annualHeatingCapacity[i]) / 24 # finding an average for each hour
    dailyHeatingCapacity.append(average)

# Plotting the graph
plt.plot(dailyHeatingCapacity, label='Heating Capacity')
plt.axhline(y = heatingLoad, color = 'r', linestyle = '-', label="Heating Load")
plt.xlabel("Day of the Year")
plt.ylabel("kiloWatts")
plt.title("Heating Capacity vs Heating Load")
leg = plt.legend()
plt.show()
