import numpy as np
import csv

def returnHeatingLoad():

    with open('London2020-Temp-RH-Pressure.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile)
        df = np.delete(list(datareader), 0, 0)
        
    col_Temp = [0]
    col_RH = [1]
    col_Pressure = [2]
    Temp_list=[]
    RH_list=[]
    Pressure_list=[]
    for row in df:
            temp = list(row[i] for i in col_Temp) # storing temperatures
            rh = list(row[i] for i in col_RH)
            pressure = list(row[i] for i in col_Pressure) # storing pressure
            Temp_list.append(temp)
            RH_list.append(rh)
            Pressure_list.append(pressure)

    df_temp = [float(i) for i in np.array(Temp_list)] # converting to floats
    df_rh = [float(i) for i in np.array(RH_list)]
    df_pressure = [float(i) for i in np.array(Pressure_list)]

    df_temp2 = np.array(df_temp)
    df_rh2 = np.array(df_rh)
    df_pressure2 = np.array(df_pressure)

    # Inputs for the program - temperatures (T) in centigrade, pressure in (kPa), humidity ratio (w) in in kgw/kga
    # Enthalpies (h) in J/kg, specific volume (ν) in m3/kg, specific heat (Cp) in kJ/kg-K, area (A) in m2,
    # Overall heat transfer coefficients (ht) in W/m2-K and ACH (Air Changes Per Hour) is dimensionless

    # All windows and doors are double glazing with 0.0127 m air space (wood/vinyl)

    T_Outside = df_temp2.T.reshape(365, 24)
    RH_Outside = df_rh2.T.reshape(365, 24)
    P_Outside = df_pressure2.T.reshape(365, 24)
    P_sat = 0.623692418 + 0.0424692499*T_Outside + 0.00134403923*(T_Outside)**2 + 0.0000309447379*(T_Outside)**3 + 3.74294905E-07*(T_Outside)**4
    w_Outside = 0.622*RH_Outside*P_sat/(P_Outside-RH_Outside*P_sat)

    T_Inside = 22.22
    w_Inside = 0.005
    h_Sat_Vapor_Inside = 2541150
    h_Sat_Water_Inside = 93040
    ν_Inside = 0.84589887
    Cp_Air = 1000
    ht_Wall = 0.6809
    ht_Window = 2.89
    ht_Door = 2.89
    ACH = 0.5

    # Partition 1 - Bedroom
    #-----------------------
    # Sensible heat transfer (Sen_HT) in Watts, latent heat transfer (Lat_HT) in Watts, infiltration in m3/hr,
    # Mass flow rate (m) in kg/s
    # For mass flow rate (m) due to infiltration, specific volume of inside air at 22.22 C & 30% RH is considered

    # Windows: North facing assumed to be 0.9144 m high and west facing 1.8288 m high

    A_North_Wall = 8.36127
    A_West_Wall = 6.401019
    A_North_Window = 0.408773
    A_West_Window = 2.74064
    A_Floor = 15.784226
    Height_Of_Roof = 2.4384
    Infiltration_1 = A_Floor * ACH * Height_Of_Roof
    m_1 = Infiltration_1/(ν_Inside*3600)

    Sen_HT_North_Wall = ht_Wall * A_North_Wall * (T_Inside - T_Outside)
    Sen_HT_West_Wall = ht_Wall * A_West_Wall * (T_Inside - T_Outside)
    Sen_HT_North_Window = ht_Window * A_North_Window * (T_Inside - T_Outside)
    Sen_HT_West_Window = ht_Window * A_West_Window * (T_Inside - T_Outside)
    Sen_HT_Infiltration_1 = m_1 * Cp_Air * (T_Inside - T_Outside)
    Tot_Lat_HT_Infiltration_1 = m_1 * (w_Inside - w_Outside) * (h_Sat_Vapor_Inside - h_Sat_Water_Inside)
    Tot_Sen_HT_1 = Sen_HT_North_Wall + Sen_HT_West_Wall + Sen_HT_North_Window + Sen_HT_West_Window + Sen_HT_Infiltration_1

    # Partition 2 - Bathroom
    #-----------------------
    # Sensible heat transfer in Watts, latent heat transfer in Watts, infiltration in m3/hr, mass flow rate in kg/hr
    # For mass flow rate (m) due to infiltration, specific volume of inside air at 22.22 C & 30% RH is considered

    # Window: Assumed to be 0.9144 m high

    A_North_Wall = 6.168762
    A_North_Window = 0.408773
    A_Floor = 7.822436
    Height_Of_Roof = 2.4384

    Sen_HT_North_Wall = ht_Wall * A_North_Wall * (T_Inside - T_Outside)
    Sen_HT_North_Window = ht_Window * A_North_Window * (T_Inside - T_Outside)
    Infiltration_2 = A_Floor * ACH * Height_Of_Roof

    m_2 = Infiltration_2/(ν_Inside*3600)
    Sen_HT_Infiltration_2 = m_2 * Cp_Air * (T_Inside - T_Outside)
    Tot_Lat_HT_Infiltration_2 = m_2 * (w_Inside - w_Outside) * (h_Sat_Vapor_Inside - h_Sat_Water_Inside)
    Tot_Sen_HT_2 = Sen_HT_North_Wall + Sen_HT_North_Window + Sen_HT_Infiltration_2


    # Partition 3 - Bathroom
    #-----------------------
    # Sensible heat transfer in Watts, latent heat transfer in Watts, infiltration in m3/hr, mass flow rate in kg/hr
    # For mass flow rate (m) due to infiltration, specific volume of inside air at 22.22 C & 30% RH is considered

    # Windows: Assumed to be 0.9144 m
    # Doors: Doors are considered 2.1336 m high

    A_North_Wall = 8.955853
    A_East_Wall = 10.600237
    A_North_Window_1 = 0.408773
    A_North_Window_2 = 0.408773
    A_North_Door = 1.895222
    A_Floor = 20.866023
    Height_Of_Roof = 2.4384

    Sen_HT_North_Wall = ht_Wall * A_North_Wall * (T_Inside - T_Outside)
    Sen_HT_East_Wall = ht_Wall * A_East_Wall * (T_Inside - T_Outside)
    Sen_HT_North_Window_1 = ht_Window * A_North_Window_1 * (T_Inside - T_Outside)
    Sen_HT_North_Window_2 = ht_Window * A_North_Window_2 * (T_Inside - T_Outside)
    Sen_HT_North_Door = ht_Door * A_North_Door * (T_Inside - T_Outside)

    Infiltration_3 = A_Floor * ACH * Height_Of_Roof
    m_3 = Infiltration_3/(ν_Inside*3600)
    Sen_HT_Infiltration_3 = m_3 * Cp_Air * (T_Inside - T_Outside)
    Tot_Lat_HT_Infiltration_3 = m_3 * (w_Inside - w_Outside) * (h_Sat_Vapor_Inside - h_Sat_Water_Inside)
    Tot_Sen_HT_3 = Sen_HT_North_Wall + Sen_HT_East_Wall + Sen_HT_North_Window_1 + Sen_HT_North_Window_2 + Sen_HT_North_Door + Sen_HT_Infiltration_3


    # Partition 4 - Dining and Living Space
    #--------------------------------------
    # Sensible heat transfer in Watts, latent heat transfer in Watts, infiltration in m3/hr, mass flow rate in kg/hr
    # For mass flow rate (m) due to infiltration, specific volume of inside air at 22.22 C & 30% RH is considered

    # Windows: Windows are considered 1.8288 m high
    # Doors: Doors are considered 2.1336 m high

    A_East_Wall = 4.57083
    A_South_Wall = 11.092623
    A_East_Window = 2.74064
    A_South_Window_1 = 2.74064
    A_South_Window_2 = 2.74064
    A_South_Door = 3.90193
    A_Floor = 27.973105
    Height_Of_Roof = 2.4384

    Sen_HT_East_Wall = ht_Wall * A_East_Wall * (T_Inside - T_Outside)
    Sen_HT_South_Wall = ht_Wall * A_South_Wall * (T_Inside - T_Outside)
    Sen_HT_East_Window = ht_Window * A_East_Window * (T_Inside - T_Outside)
    Sen_HT_South_Window_1 = ht_Window * A_South_Window_1 * (T_Inside - T_Outside)
    Sen_HT_South_Window_2 = ht_Window * A_South_Window_2 * (T_Inside - T_Outside)
    Sen_HT_South_Door = ht_Door * A_South_Door * (T_Inside - T_Outside)

    Infiltration_4 = A_Floor * ACH * Height_Of_Roof
    m_4 = Infiltration_4/(ν_Inside*3600)
    Sen_HT_Infiltration_4 = m_4 * Cp_Air * (T_Inside - T_Outside)
    Tot_Lat_HT_Infiltration_4 = m_4 * (w_Inside - w_Outside) * (h_Sat_Vapor_Inside - h_Sat_Water_Inside)
    Tot_Sen_HT_4 = Sen_HT_East_Wall + Sen_HT_South_Wall + Sen_HT_East_Window + Sen_HT_South_Window_1 + Sen_HT_South_Window_2 + Sen_HT_South_Door + Sen_HT_Infiltration_4

    # Partition 5 - Side Space
    #-------------------------
    # Sensible heat transfer in Watts, latent heat transfer in Watts, infiltration in m3/hr, mass flow rate in kg/hr
    # For mass flow rate (m) due to infiltration, specific volume of inside air at 22.22 C & 30% RH is considered

    # Doors: Doors are considered 2.1336 m high

    A_West_Wall = 13.164361
    A_South_Wall = 5.85289
    A_East_Door = 1.923093
    A_East_Wall = 2.471221
    A_Floor = 12.950684
    Height_Of_Roof = 2.4384

    Sen_HT_West_Wall = ht_Wall * A_West_Wall * (T_Inside - T_Outside)
    Sen_HT_South_Wall = ht_Wall * A_South_Wall * (T_Inside - T_Outside)
    Sen_HT_East_Door = ht_Door * A_East_Door * (T_Inside - T_Outside)
    Sen_HT_East_Wall = ht_Wall * A_East_Wall * (T_Inside - T_Outside)

    Infiltration_5 = A_Floor * ACH * Height_Of_Roof
    m_5 = Infiltration_5/(ν_Inside*3600)
    Sen_HT_Infiltration_5 = m_5 * Cp_Air * (T_Inside - T_Outside)
    Tot_Lat_HT_Infiltration_5 = m_5 * (w_Inside - w_Outside) * (h_Sat_Vapor_Inside - h_Sat_Water_Inside)
    Tot_Sen_HT_5 = Sen_HT_East_Wall + Sen_HT_South_Wall + Sen_HT_West_Wall + Sen_HT_East_Door + Sen_HT_Infiltration_5

    # Overall Results
    #----------------

    Total_Sen_HT = Tot_Sen_HT_1 + Tot_Sen_HT_2 + Tot_Sen_HT_3 + Tot_Sen_HT_4 + Tot_Sen_HT_5
    Total_Lat_HT = Tot_Lat_HT_Infiltration_1 + Tot_Lat_HT_Infiltration_2 + Tot_Lat_HT_Infiltration_3 + Tot_Lat_HT_Infiltration_4 + Tot_Lat_HT_Infiltration_5
    Total_HT = Total_Sen_HT + Total_Lat_HT # This is in W, need to convert to kW for heating.py 

    return(Total_HT[0, 0]/100) # converting to kW by dividing by 100

