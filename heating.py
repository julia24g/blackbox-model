import numpy as np
BTU_CONVERT = 3412.142 # rate we need to multiply kW heating demand by to get BTU/hr

# Heating
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
            break
        
    return ratedCapacity[0] # returns rated capacity in BTU/hr

# Heating COP function with input of ambient temperature and heating demand (BTU/hr)
def heatingCOP(t, heating_demand_kW):
    heating_demand = selectHP(heating_demand_kW) # selects the heat pump

    for ratedCapacity in table1:
        if ratedCapacity[0] >= heating_demand:
            return round(ratedCapacity[5] + ratedCapacity[6]*t + ratedCapacity[7]*t**2, 6)
        

# User Input

heating_demand = input("Please input your maximum heating demand (in kW) on the coldest day of the year: ")
ambient_temp = float(input("Please input the ambient temperature (in Celsius): "))

print()
print("Heating COP: ", heatingCOP(float(ambient_temp), float(heating_demand)))


# can ask user for ambient temperature OR list of ambient temperatures for each day or each hour - calculate COP on each hour
temp_table = np.genfromtxt('2020temp.csv', dtype='str')

print("Calculating COP for 365 days and 24 hours a day")
heating_demand = input("Please input your maximum heating demand (in kW) on the coldest day of the year: ")
print()

annualCOP = [[0 for i in range(24)] for j in range(365)]

for i in range(365):
    for j in range(24):
        annualCOP[i][j] = heatingCOP(float(temp_table[i][j]), float(heating_demand))

print("Annual COP matrix: ")
print(annualCOP)

# output of house model will be input for this model
# calculate heating capacity of HP using the maximum heating capacity equation (365 x 24 matrix using heat pump and temperatures)
# then, convert heating demand and heating capacity into daily (either average or summation), and graph those two lines daily for the entire year

