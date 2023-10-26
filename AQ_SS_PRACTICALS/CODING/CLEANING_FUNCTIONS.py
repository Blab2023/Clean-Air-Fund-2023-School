# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 17:51:19 2023

@author: CLi
"""

#importing necessary packages in python
import pandas as pd
import numpy as np
import glob
import datetime

#creating functions needed for cleaning the data

#winds conversion from miles per hour (mph) to metres per sec(mps)
def wind_mph_to_mps(wind_data):
    mps_wind = (wind_data/2.237) # convert from mph to m/s and adding it to a new colums
    return mps_wind

# averaging pm data for 2
def avg_pms_of_2(pm_1st_data, pm_2nd_data):
    avg_pm = (pm_1st_data+pm_2nd_data)/2
    return avg_pm

#some datasets may have '+' in the time component
#removing "+" in date tiime and selecting date range to work with
def work_on_time(csv_data,start_date_time, end_date_time):
    csv_data.index = csv_data.index.tz_localize(None) # removes the '+' in the date time
    csv_data_2020 = csv_data.loc[start_date_time:end_date_time]
    return csv_data_2020

#conversion from Fahrenheit temperature into Celsius
def Fahren_2_Celcius(Fahren_data):
    celc_deci = (Fahren_data - 32) / 1.8
    celc_cal = round(celc_deci) #celc_cal = round(celc_deci,2) (for 2 deci point)
    return celc_cal

## correct pm2.5 data with factor of corretion (pm2.5 = 0.54[pm2.5_data_TTQ] + 1.5[TmpAVG] + 0.12[RH] - 47.33)
def correct_pm25(aq_data,raw_pm_column,temp_column,RH_column):
    pm25correct = ((0.54 * aq_data[raw_pm_column]) + (1.53 * aq_data[temp_column]) + (0.12 * aq_data[RH_column]) - 47.33)
    return pm25correct

def create_seasons(data,MOY_column):
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    seasons = ['winter','winter','spring','spring','spring',
         'summer','summer','summer','fall','fall','fall','winter']
    data["season"] = data[MOY_column].replace(months,seasons)
    return data

def calc_WIND_category16(wind_deg):
    deg = round(wind_deg,2)
    if deg >= 11.25 and deg < 33.75:
        return "NNE"
    elif deg >= 33.75 and deg < 56.25:
        return "NE"
    elif deg >= 56.25 and deg < 78.75:
        return "ENE"
    elif deg >= 78.75 and deg < 101.25:
        return "E"
    elif deg >= 101.25 and deg < 123.75:
        return "ESE"
    elif deg >= 123.75 and deg < 146.25:
        return "SE"
    elif deg >= 146.25 and deg < 168.75:
        return "SSE"
    elif deg >= 168.75 and deg < 191.25:
        return "S"
    elif deg >= 191.25 and deg < 213.75:
        return "SSW"
    elif deg >= 213.75 and deg < 236.25:
        return "SW"
    elif deg >= 236.25 and deg < 258.65:
        return "WSW"
    elif deg >= 258.65 and deg < 281.25:
        return "W"
    elif deg >= 281.25 and deg < 303.75:
        return "WNW"
    elif deg >= 303.75 and deg < 326.25:
        return "NW"
    elif deg >= 326.25 and deg < 348.75:
        return "NNW"
    else:
        return "N"


#===this function works for 8 cardinal points
def calc_WIND_category8(wind_deg):
    deg = round(wind_deg,1)
    if deg >= 22.5 and deg < 67.5:
        return "NE"
    elif deg >= 67.5 and deg < 112.5:
        return "E"
    elif deg >= 112.5 and deg < 157.5:
        return "SE"
    elif deg >= 157.5 and deg < 202.5:
        return "S"
    elif deg >= 202.5 and deg < 247.5:
        return "SW"
    elif deg >= 247.5 and deg < 292.5:
        return "W"
    elif deg >= 292.5 and deg < 337.5:
        return "NW"
    else:
        return "N"    