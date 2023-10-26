# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 18:10:57 2022

@author: CLi
"""

#============================================================================
import pandas as pd
import numpy as np
from numpy import cov
from numpy import mean
from numpy import std
import matplotlib.pyplot as plt
from matplotlib import pyplot
import seaborn as sb
import seaborn as sns
import scipy as sp
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
from math import sqrt
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error as mae
import scipy.stats as stats



#create the data path==================================
data_path = '../DATA/'



#========================= getting R data ============================
def work_on_time(csv_data, start_date_time, end_date_time):
    #pd.date_range(start='2019-01-01 00:00:00', end='2021-12-31 23:00:00').difference(csv_data.index)
    csv_data.index = csv_data.index.tz_localize(None)  # removes the '+' in the date time 
    csv_data_2020 = csv_data.loc[start_date_time:end_date_time]
    return csv_data_2020


OBS_BAM = pd.read_csv(data_path+'BAM_OBSERVED.csv',
                          na_values=[-99.9, -9.99, -9999, 'M',' ','*',-999],
                          parse_dates=['Time'], index_col='Time')
OBS_BAM = OBS_BAM.rename(columns={"PM2.5" : "BAM_OBS PM2.5"})

GEOS_BAM = pd.read_csv(data_path+'BAM_GEOS.csv',
                          na_values=[-99.9, -9.99, -9999, 'M',' ','*',-999],
                          parse_dates=['Time'], index_col='Time')
GEOS_BAM = GEOS_BAM.rename(columns={" PM2.5" : "BAM_GEOS PM2.5"})

#BAM_DATA_FULL = pd.concat([OBS_BAM,GEOS_BAM])
#BAM_DATA_FULL = BAM_DATA_FULL[['BAM_OBS PM2.5', 'BAM_GEOS PM2.5']]
#BAM_DATA = work_on_time(BAM_DATA_FULL, '2021-01-20 00:00:00', '2021-12-28 23:30:00')

#BAM_DATA.to_csv(data_path+'bam_data_del.csv')
bam_data = pd.merge_asof(OBS_BAM,GEOS_BAM, left_index=True, right_index=True)
bam_data = bam_data[['BAM_OBS PM2.5', 'BAM_GEOS PM2.5']]
bam_data = work_on_time(bam_data, '2021-01-20 00:00:00', '2021-12-28 23:30:00')
bam_data.to_csv(data_path+'bam_data_del.csv')



#ADABRAKA DATA
OBS_ADAB = pd.read_csv(data_path+'ADABRAKA_OBSERVED.csv',
                          na_values=[-99.9, -9.99, -9999, 'M',' ',-999],
                          parse_dates=['Time'], index_col='Time')
OBS_ADAB = OBS_ADAB.rename(columns={"AD PM2.5" : "AD_OBS PM2.5"})

GEOS_ADAB = pd.read_csv(data_path+'ADABRAKA_GEOS.csv',
                          na_values=[-99.9, -9.99, -9999, 'M',' ',-999],
                          parse_dates=['Time'], index_col='Time')
GEOS_ADAB = GEOS_ADAB.rename(columns={" PM2.5" : "AD_GEOS PM2.5"})

ADABRAKA_DATA_FULL = pd.concat([OBS_ADAB,GEOS_ADAB])
ad_data = pd.merge_asof(OBS_ADAB,GEOS_ADAB, left_index=True, right_index=True)
ad_data = ad_data[['AD_OBS PM2.5', 'AD_GEOS PM2.5']]
ad_data = work_on_time(ad_data, '2021-01-20 00:00:00', '2021-12-28 23:30:00')
ad_data.to_csv(data_path+'ad_data_del.csv')
#ADABRAKA_DATA_FULL = ADABRAKA_DATA_FULL[['AD_OBS PM2.5', 'AD_GEOS PM2.5']]
#ADABRAKA_DATA = work_on_time(ADABRAKA_DATA_FULL, '2021-01-20 00:00:00', '2021-12-28 23:30:00')

#ADABRAKA_DATA.to_csv(data_path+'ad_data_del.csv')


#LEGON DATA
OBS_UG = pd.read_csv(data_path+'UG_OBSERVED.csv',
                          na_values=[-99.9, -9.99, -9999, 'M',' ',-999],
                          parse_dates=['Time'], index_col='Time')
OBS_UG = OBS_UG.rename(columns={"UG PM2.5" : "UG_OBS PM2.5"})


GEOS_UG = pd.read_csv(data_path+'UG_GEOS.csv',
                          na_values=[-99.9, -9.99, -9999, 'M',' ',-999],
                          parse_dates=['Time'], index_col='Time')
GEOS_UG = GEOS_UG.rename(columns={" PM2.5" : "UG_GEOS PM2.5"})

#UG_DATA_FULL = pd.concat([OBS_UG,GEOS_UG])
#UG_DATA_FULL = UG_DATA_FULL[['UG_OBS PM2.5', 'UG_GEOS PM2.5']]
#UG_DATA = work_on_time(UG_DATA_FULL, '2021-01-20 00:00:00', '2021-12-28 23:30:00')

#UG_DATA.to_csv(data_path+'ug_data_del.csv')
ug_data = pd.merge_asof(OBS_UG,GEOS_UG, left_index=True, right_index=True)
ug_data = ug_data[['UG_OBS PM2.5', 'UG_GEOS PM2.5']]
ug_data = work_on_time(ug_data, '2021-01-20 00:00:00', '2021-12-28 23:30:00')
ug_data.to_csv(data_path+'ug_data_del.csv')




#scatterplot
slope, intercept, r_value, p_value, std_err = stats.linregress(bam_data['BAM_OBS PM2.5'],bam_data['BAM_GEOS PM2.5'])
plt.figure(figsize=(15,10))
sns.regplot(x='BAM_OBS PM2.5',y='BAM_GEOS PM2.5',data=bam_data,line_kws={'color':'red','label':"y={0:.3f}x+{1:.3f}".format(slope,intercept)})
plt.legend(loc='upper left',fontsize=25)
plt.xticks(fontsize=(25))
plt.yticks(fontsize=(25))





#Line plots
#convert index to columns
ug_data_new = ug_data.reset_index()
fig, axs = plt.subplots(1, 2, figsize=(15, 8), sharex=True)
sns.lineplot(
    x="Time",
    y="UG_OBS PM2.5",
    linewidth=3,
    data=ug_data_new,
    label="OBS PM2.5",
    color="red",
    ax=axs[0],
)
sns.lineplot(
    x="Time",
    y="UG_GEOS PM2.5",
    linewidth=3,
    data=ug_data_new,
    label="GEOS PM2.5",
    color="orange",
    ax=axs[1],
)
fig.suptitle("UG OBSERVED VS GEOS", fontsize=20)
axs[0].set_ylabel("PM 2.5", fontsize=13)
axs[1].set_ylabel("PM2.5", fontsize=13)
sns.despine()





#---------- ALLL THE DATA MERGED ==========================================
#all_data = pd.concat([OBS_BAM,GEOS_BAM, OBS_ADAB, GEOS_ADAB, OBS_UG, GEOS_UG])

all_data = pd.merge_asof(OBS_UG,GEOS_UG,OBS_ADAB, GEOS_ADAB, OBS_UG, GEOS_UG, left_index=True, right_index=True)

data_export_all = work_on_time(all_data, '2021-01-20 00:00:00', '2021-09-30 23:30:00')
data_export = data_export_all[['BAM_OBS PM2.5', 'BAM_GEOS PM2.5', 'AD_OBS PM2.5',
                               'AD_GEOS PM2.5', 'UG_OBS PM2.5','UG_GEOS PM2.5']]
data_export.to_csv(data_path+'evaluation_data_del.csv')
'''