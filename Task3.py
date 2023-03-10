import os
from CreatePricesDfTask3 import CreatePricesDf
from PricesDK import PricesDK
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from ProsumerOptimizer import ProsumerOptimizer

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
#Cost per day
df_days=df_hourly.resample('d', on='HourDK').mean(numeric_only=True)

#Total cost between t_s and t_e
Totsum=df_hourly["Costhour"].sum()

#Consumed each hour of the day means times buy price each hour of the day means
df_hourly["Costhourmean"]=df_hourly.groupby(df_hourly["HourDK"].dt.hour)["Load"].mean()*df_pricesDK2.groupby(df_pricesDK2["HourDK"].dt.hour)["Buy"].mean()
#The sum of the day times all days
Totmean=df_meanhours.sum()*(len(df_hourly["HourDK"])/24)

#The difference between mean and sum calcultions in percents
Totdif=(1-Totmean/Totsum)*100

##3.2
#Import
df_hourly["Import"]=df_hourly["Load"]-df_hourly["PV"]
df_hourly.loc[df_hourly["Import"]<0,"Import"]=0
#Export
df_hourly["Export"]=df_hourly["PV"]-df_hourly["Load"]
df_hourly.loc[df_hourly["Export"]<0,"Export"]=0
#Cost with PV
df_hourly["CostPV"]=df_hourly["Import"]*df_pricesDK2["Buy"]-df_hourly["Export"]*df_pricesDK2["Sell"]
#Sum of cost with PV in year
df_yearlyPV=df_hourly.groupby(df_hourly["HourDK"].dt.year)["CostPV"].sum()

#Sum of cost without PV in year
df_yearlynoPV=df_hourly.groupby(df_hourly["HourDK"].dt.year)["Costhour"].sum()

#Making figure to compare means in years and regions
#X-axis is being defined for the specified years range
Years = np.array([2020,2021,2022])
Years_Axis = np.arange(len(Years))

fig, ax = plt.subplots()

#Years axis is being shifted to account for just over half of the bar width
ax.bar(Years_Axis - 0.16, df_yearlynoPV.values, width = 0.30, label = "Without PV" , color = 'b')
ax.bar(Years_Axis + 0.16, df_yearlyPV.values, width = 0.30, label = "With PV", color = 'r')

plt.xticks(Years_Axis, Years)

#Create specific background line pattern with major and minor lines
ax.set_axisbelow(True)
ax.grid(which='major', axis = 'y', linewidth=0.8, alpha=0.8)
ax.grid(which='minor', axis = 'y', linewidth=0.2, alpha=0.8)
ax.minorticks_on()

plt.xlabel("Year")
plt.ylabel("Cost [DKK]")
plt.title("Cost in a household DK2 with and without PV installed")
plt.legend()
plt.show()

##3.3
#x-values (hours)
hours=np.arange(1,25,1)
plt.plot(hours,df_pricesDK2.groupby(df_pricesDK2["HourDK"].dt.hour)["Buy"].mean(),'o',linestyle='solid',label="Buy price[DKK/kWh]")
plt.plot(hours,df_hourly.groupby(df_hourly["HourDK"].dt.hour)["Load"].mean(),'o',linestyle='solid',label="Consumption[kWh]")

plt.xlabel("Hours")
plt.ylabel("Cost")
plt.title("Consumption mean vs buy price mean over the hours of the day")
plt.legend()
plt.show()

##3.4
# Define the parameters of the problem
Cmax = 10
Pmax = 6
n_c = 0.95
n_d = 0.95
C_0 = 5
C_n = 5

#Reshaping Buy, Sell, PV and Load in to matrix to call each days
df_Buy=df_pricesDK2["Buy"].values.reshape(-1,24)
df_Sell=df_pricesDK2["Sell"].values.reshape(-1,24)
df_PV=df_hourly["PV"].values.reshape(-1,24)
df_Load=df_hourly["Load"].values.reshape(-1,24)

#Cost with only PV from question 3.2
df_costPV=df_hourly["CostPV"].values.reshape(-1,24)
df_costPV[0].sum()

#Sampling spot prices in days from hours
df_pricesDK2days=df_pricesDK2.resample('d', on='HourDK').mean(numeric_only=True)
df_pricesDK2days=df_pricesDK2days.reset_index()[["HourDK","SpotPriceDKK"]]

#Cost with only PV column
df_pricesDK2days["CostPV"]=np.ones(len(df_pricesDK2days["SpotPriceDKK"]))
#Making a profit column
df_pricesDK2days["CostPVBat"]=np.ones(len(df_pricesDK2days["SpotPriceDKK"]))

#Looping over every 24 hours to find the profit from battery and PV
i=0
for i in range(len(df_pricesDK2days["SpotPriceDKK"])):
    #Appending sum of each row ind days from cost with only PV
    df_pricesDK2days["CostPV"][i]=df_costPV[i].sum()

    #Calling the row for Buy, Sell, Pv and Load for next 24 hours
    l_b=df_Buy[i]
    l_s=df_Sell[i]
    p_PV=df_PV[i]
    p_L=df_Load[i]

    #Calling Optimizerpy
    profitOptpro, p_cOptpro, p_dOptpro, p_bOptpro, p_sOptpro, XOptpro = ProsumerOptimizer(Pmax, n_c, n_d, Cmax, C_0, C_n, l_b, l_s, p_PV, p_L)
    df_pricesDK2days["CostPVBat"][i]=profitOptpro

#Benefit per day of using battery vs without
df_pricesDK2days["Benefit"]=df_pricesDK2days["CostPVBat"]-df_pricesDK2days["CostPV"]

#Benefit in years
df_pricesDK2years=df_pricesDK2days.groupby(df_pricesDK2days["HourDK"].dt.year)["Benefit"].sum()
print(df_pricesDK2years.sum()) #Saved over 2 years and 10 month 6099dkk