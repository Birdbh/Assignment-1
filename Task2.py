import os
from CreatePricesDf_new import CreatePricesDf
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from Optimizer import Optimizer

##2.1
#Calling the prices in seperate dataframes
df_pricesDK1, df_pricesDK2 = CreatePricesDf()

# Load prosumer data
file_P = os.path.join(os.getcwd(), 'ProsumerData.csv')
df_net = pd.read_csv(open(file_P))
df_net['HourUTC'] = pd.to_datetime(df_net['HourUTC'], utc=True)
df_net['HourDK'] = df_net['HourUTC'].dt.tz_convert('CET')
df_hourly = df_net.resample('H', on='HourUTC').mean(numeric_only=True)
df_hourly = df_hourly.reset_index()[["HourUTC","PV","Load"]]
df_hourly["HourDK"] = df_hourly['HourUTC'].dt.tz_convert('CET')

#change sampling for only full days

#Sampling spot prices in days from hours
df_pricesDK2days=df_pricesDK2.resample('d', on='HourDK').mean(numeric_only=True)
df_pricesDK2days=df_pricesDK2days.reset_index()[["HourDK","SpotPriceDKK"]]

#Reshaping values in to a array
df_SpotPricehours=df_pricesDK2["SpotPriceDKK"].values[0:27768]

#Rehsaping in 24 values per row
df_SpotPricehours=df_SpotPricehours.reshape(-1,24)

#Making a list for 
df_pricesDK2days["ProfitDKK99"]=np.ones(len(df_pricesDK2days["SpotPriceDKK"]))

# Define the parameters of the problem
Cmax = 10
Pmax = 6
n_c = 0.99
n_d = 0.99
C_0 = 5
C_n = 5

#Looping over every 24 hours to find the profit from using a battery in your household
i=0
for i in range(len(df_pricesDK2days["SpotPriceDKK"])):
    p=df_SpotPricehours[i]
    #this value is off because it takes the last two hours of one day when the data starts into account, need to exldude 2019-8-31 22:00 and 23:00 at the beginning, small change but more accurate

    #Calling Optimizerpy
    profitOpt, p_cOpt, p_dOpt, XOpt = Optimizer(Pmax, n_c, n_d, Cmax, C_0, C_n, p)
    df_pricesDK2days["ProfitDKK99"][i]=profitOpt

#Aggregated yearly profit
df_profitDK2years99=df_pricesDK2days.groupby(df_pricesDK2days["HourDK"].dt.year)["ProfitDKK99"].sum()
df_profitDK2years99=df_profitDK2years99.reset_index()[["HourDK","ProfitDKK99"]]

#X-values
Years = df_profitDK2years99["HourDK"].values
Years_Axis = np.arange(len(Years))

fig, ax = plt.subplots()
ax.set_axisbelow(True)
ax.grid(which='major', axis = 'y', linewidth=0.8, alpha=0.8)
ax.grid(which='minor', axis = 'y', linewidth=0.2, alpha=0.8)
ax.minorticks_on()

plt.bar(Years_Axis, df_profitDK2years99["ProfitDKK99"].values, color = 'b')
plt.xticks(Years_Axis, Years)
plt.xlabel("Year")
plt.ylabel("Profit [DKK]")
plt.title("Profit per Year Installing a Battery in a Household DK2")
plt.show()

#Normalized data:
#Correlation between profit and spot prices
fig, ax = plt.subplots()
ax.set_axisbelow(True)
ax.grid(which='major', linewidth=0.8, alpha=0.8)
ax.grid(which='minor', linewidth=0.2, alpha=0.8)
ax.minorticks_on()

ax.scatter(df_pricesDK2days["SpotPriceDKK"]/np.max(df_pricesDK2days["SpotPriceDKK"]),df_pricesDK2days["ProfitDKK99"]/np.max(df_pricesDK2days["ProfitDKK99"]))
ax.annotate('Pearson correlation coefficient: 0.8101', xy=(350, 20), xycoords='axes points',
            size=10, ha='right', va='top',
            bbox=dict(boxstyle='round', fc='w'))
ax.legend()
### Add the plot of a variable you think can be correlated it

plt.xlabel("Spot prices DK2")
plt.ylabel("Profit from Battery DK2")
plt.title("Correlation Between Spot Price and Optimized Battery Profit in DK2")
plt.show()

# Calculate Pearson correlation
# Check the values of other covariates
corr_matrix = np.corrcoef(df_pricesDK2days["SpotPriceDKK"]/np.max(df_pricesDK2days["SpotPriceDKK"]),df_pricesDK2days["ProfitDKK99"]/np.max(df_pricesDK2days["ProfitDKK99"]))

# extract the correlation coefficient from the matrix
corr_coeff = corr_matrix[0, 1]

# print the correlation coefficient
print("Pearson correlation coefficient:", corr_coeff)

##2.2
#Setting a new column  for the calulation of efficency 95%
df_pricesDK2days["ProfitDKK95"]=np.ones(len(df_pricesDK2days["SpotPriceDKK"]))

n_c2 = 0.95
n_d2 = 0.95

#Looping over every 24 hours to find the profit from using a battery in your household
i=0
for i in range(len(df_pricesDK2days["SpotPriceDKK"])):
    p=df_SpotPricehours[i]

    #Calling Optimizerpy
    profitOpt, p_cOpt, p_dOpt, XOpt = Optimizer(Pmax, n_c2, n_d2, Cmax, C_0, C_n, p)
    df_pricesDK2days["ProfitDKK95"][i]=profitOpt

#Aggregated yearly profit
df_profitDK2years95=df_pricesDK2days.groupby(df_pricesDK2days["HourDK"].dt.year)["ProfitDKK95"].sum()
df_profitDK2years95=df_profitDK2years95.reset_index()[["HourDK","ProfitDKK95"]]

#Setting a new column  for the calulation of efficency 90%
df_pricesDK2days["ProfitDKK90"]=np.ones(len(df_pricesDK2days["SpotPriceDKK"]))

n_c3 = 0.9
n_d3 = 0.9

#Looping over every 24 hours to find the profit from using a battery in your household
i=0
for i in range(len(df_pricesDK2days["SpotPriceDKK"])):
    p=df_SpotPricehours[i]

    #Calling Optimizerpy
    profitOpt, p_cOpt, p_dOpt, XOpt = Optimizer(Pmax, n_c3, n_d3, Cmax, C_0, C_n, p)
    df_pricesDK2days["ProfitDKK90"][i]=profitOpt

#Aggregated yearly profit
df_profitDK2years90=df_pricesDK2days.groupby(df_pricesDK2days["HourDK"].dt.year)["ProfitDKK90"].sum()
df_profitDK2years90=df_profitDK2years90.reset_index()[["HourDK","ProfitDKK90"]]

#Grouped bar plot
_Aggregatedprofityearly=[["2019",df_profitDK2years99["ProfitDKK99"].values[0],df_profitDK2years95["ProfitDKK95"].values[0],df_profitDK2years90["ProfitDKK90"].values[0]],
                         ["2020",df_profitDK2years99["ProfitDKK99"].values[1],df_profitDK2years95["ProfitDKK95"].values[1],df_profitDK2years90["ProfitDKK90"].values[1]],
                         ["2021",df_profitDK2years99["ProfitDKK99"].values[2],df_profitDK2years95["ProfitDKK95"].values[2],df_profitDK2years90["ProfitDKK90"].values[2]],
                         ["2022",df_profitDK2years99["ProfitDKK99"].values[3],df_profitDK2years95["ProfitDKK95"].values[3],df_profitDK2years90["ProfitDKK90"].values[3]]]

_df = pd.DataFrame(_Aggregatedprofityearly,columns=["Year", "99%", "95%", "90%"])
fig, ax = plt.subplots()
ax.set_axisbelow(True)
ax.grid(which='major', axis = 'y', linewidth=0.8, alpha=0.8)
ax.grid(which='minor', axis = 'y', linewidth=0.2, alpha=0.8)
ax.minorticks_on()
plt.xticks(Years_Axis, Years)
ax.bar(Years_Axis - 0.3, _df["99%"], width = 0.30, label="99%")
ax.bar(Years_Axis, _df["95%"], width = 0.30, label="95%")
ax.bar(Years_Axis + 0.3, _df["90%"], width = 0.30, label="90%")
plt.xlabel("Year")
plt.ylabel("Price (DKK/MWh)")
plt.title("Value Gain from 99%, 95%, and 90% Battery Efficiency for Each Year")
plt.legend()
plt.show()
plt.show()