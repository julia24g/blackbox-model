import numpy as np
BTU_CONVERT = 3412.142 # rate we need to multiply kW heating demand by to get BTU/hr

# Heating
table1 = np.loadtxt("heating_capacity.csv")

# Selects an HP based on heating demand in kW
def selectHP(heating_demand_kW):
    heating_demand = heating_demand_kW * BTU_CONVERT # first, convert heating demand in kW to BTU/hr

    for ratedCapacity in table1:  # iterate through rated capacity columns until we find the rated capacity that satisfies heating demand
        if ratedCapacity[0] > heating_demand:
            print("Selected heat pump: ", ratedCapacity[0])
            return ratedCapacity[0]

# Heating COP function with input of ambient temperature and heating demand (BTU/hr)
def heatingCOP(t, heating_demand_kW):
    heating_demand = selectHP(heating_demand_kW) # selects the heat pump

    for ratedCapacity in table1:
        if ratedCapacity[0] > heating_demand:
            return round(ratedCapacity[5] + ratedCapacity[6]*t + ratedCapacity[7]*t**2, 6)
        
# Heating Capacity function with input of ambient temperature and heating demand (BTU/hr)
def heatingCapacity(t, heating_demand):
    for ratedCapacity in table1:
        if ratedCapacity[0] > heating_demand:
            return round(ratedCapacity[1] + ratedCapacity[2]*t + ratedCapacity[3]*t**2, 6)

# Cooling
table2 = np.loadtxt("cooling_capacity.csv")

# Cooling COP function with input of temperatures and heating demand (BTU/hr)
def coolingCOP(To, Tiwb, Ti, heating_demand):
    # iterate through rated capacity row
    cols = len(table2[0])
    for col in range(cols):
        if table2[0][col] > heating_demand:
            return round(table2[15][col] + Ti*table2[16][col] + Tiwb*table2[17][col] + To*table2[18][col]+ Ti*Tiwb*table2[19][col] + Ti*To*table2[20][col] + Tiwb*To*table2[21][col] + Ti**2*table2[22][col] + Tiwb**2*table2[23][col] + To**2*table2[24][col] + Ti**2*To*table2[25][col] + Tiwb**2*To*table2[26][col] + Ti*Tiwb*To*table2[27][col], 6)

# Cooling Load function
def coolingLoad(To, Tiwb, Ti, heating_demand):
    cols = len(table2[0])
    for col in range(cols):
        if table2[0][col] > heating_demand:
            return round(table2[1][col] + Ti*table2[2][col] + Tiwb*table2[3][col] + To*table2[4][col]+ Ti*Tiwb*table2[5][col] + Ti*To*table2[6][col] + Tiwb*To*table2[7][col] + Ti**2*table2[8][col] + Tiwb**2*table2[9][col] + To**2*table2[10][col] + Ti**2*To*table2[11][col] + Tiwb**2*To*table2[12][col] + Ti*Tiwb*To*table2[13][col], 6)

# User Input

heating_demand = input("Please input your maximum heating demand (in kW) on the coldest day of the year: ")
ambient_temp = float(input("Input ambient temperature: "))

print("Output:")
print("Heating COP: ", heatingCOP(ambient_temp, heating_demand))
print("Heating Capacity: ", heatingCapacity(ambient_temp, heating_demand))

print()
print("Cooling Equations")
To = float(input("Input ambient temperature: "))
Ti = float(input("Input indoor dry bulb temperature: "))
Tiwb = float(input("Input indoor wet bulb temperature: "))
heating_demand = float(input("Input heating demand: "))

print("Output:")
print("Cooling COP: ", coolingCOP(To, Tiwb, Ti, heating_demand))
print("Cooling Load: ", coolingLoad(To, Tiwb, Ti, heating_demand))


    # can ask user for ambient temperature OR list of ambient temperatures for each day or each hour - calculate COP on each hour
