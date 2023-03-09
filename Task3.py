import os
from CreatePricesDfTask3 import CreatePricesDf
from PricesDK import PricesDK
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

##3.1
#Calling the prices in seperate dataframes
df_pricesDK2 = CreatePricesDf()

# Process electricity prices
df_pricesDK2 = PricesDK(df_pricesDK2)

# Load prosumer data
file_P = os.path.join(os.getcwd(), 'ProsumerData.csv')
df_net = pd.read_csv(open(file_P))
df_net['HourUTC'] = pd.to_datetime(df_net['HourUTC'], utc=True)
df_net['HourDK'] = df_net['HourUTC'].dt.tz_convert('CET')
df_hourly = df_net.resample('H', on='HourUTC').mean(numeric_only=True)
df_hourly = df_hourly.reset_index()[["HourUTC","PV","Load"]]
df_hourly["HourDK"] = df_hourly['HourUTC'].dt.tz_convert('CET')

# Keep part from start to end time and sort
t_s = pd.Timestamp(dt.datetime(2020, 1, 1, 0, 0, 0), tz='CET')
t_e = pd.Timestamp(dt.datetime(2022, 10, 31, 23, 0, 0), tz='CET')

#Locating all times in the choosen zone
df_hourly = df_hourly.loc[(df_hourly['HourDK']>=t_s) & (df_hourly['HourDK']<=t_e)]
df_hourly = df_hourly.reset_index(drop=True)

#Cost per hour
df_hourly["Costhour"]=df_hourly["Load"]*df_pricesDK2["Buy"]
#Total cost between t_s and t_e
Totsum=df_hourly["Costhour"].sum()

#Consumed each hour of the day means times buy price each hour of the day means
df_meanhours=df_hourly.groupby(df_hourly["HourDK"].dt.hour)["Load"].mean()*df_pricesDK2.groupby(df_pricesDK2["HourDK"].dt.hour)["Buy"].mean()
#The sum of the day times all days
Totmean=df_meanhours.sum()*(len(df_hourly["HourDK"])/24)

#The difference between mean and sum calcultions in percents
Totdif=(1-Totmean/Totsum)*100

##3.2
#Consumption minus production
df_hourly["LoadPV"]=df_hourly["Load"]-df_hourly["PV"]

