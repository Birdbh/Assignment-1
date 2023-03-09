from CreatePricesDf_new import CreatePricesDf
import matplotlib.pyplot as plt
import numpy as np

##1.1
#Calling the prices in seperate dataframes
df_pricesDK1, df_pricesDK2 = CreatePricesDf()

#Calling the two regions DK1 and DK2 and finding the average of each in years
df_YearavgDK1=df_pricesDK1.groupby(df_pricesDK1["HourDK"].dt.year)["SpotPriceDKK"].mean()
df_YearavgDK2=df_pricesDK2.groupby(df_pricesDK2["HourDK"].dt.year)["SpotPriceDKK"].mean()

#Setting the column names of years and mean spot prices
df_YearavgDK1= df_YearavgDK1.reset_index()[["HourDK","SpotPriceDKK"]]
df_YearavgDK1.rename(columns={"HourDK": "Years"})
df_YearavgDK2= df_YearavgDK2.reset_index()[["HourDK","SpotPriceDKK"]]
df_YearavgDK2.rename(columns={"HourDK": "Years"})

#Making figure to compare means in years and regions
#X-axis is being defined for the specified years range
Years = df_YearavgDK2["HourDK"].values
Years_Axis = np.arange(len(Years))

fig, ax = plt.subplots()

#Years axis is being shifted to account for just over half of the bar width
ax.bar(Years_Axis - 0.16, df_YearavgDK1["SpotPriceDKK"].values, width = 0.30, label = "DK1" , color = 'b')
ax.bar(Years_Axis + 0.16, df_YearavgDK2["SpotPriceDKK"].values, width = 0.30, label = "DK2", color = 'r')

plt.xticks(Years_Axis, Years)

#Create specific background line pattern with major and minor lines
ax.set_axisbelow(True)
ax.grid(which='major', axis = 'y', linewidth=0.8, alpha=0.8)
ax.grid(which='minor', axis = 'y', linewidth=0.2, alpha=0.8)
ax.minorticks_on()

plt.xlabel("Year")
plt.ylabel("Price (DKK/MWh)")
plt.title("Average Price of Energy in Region DK1 vs. DK2")
plt.legend()
plt.show()

#grouby function is applied to the loc of DK1 and DK2 and then averaged
df_hourcostDK1=df_pricesDK1.groupby(df_pricesDK1["HourDK"].dt.hour)["SpotPriceDKK"].mean()
df_hourcostDK2=df_pricesDK2.groupby(df_pricesDK2["HourDK"].dt.hour)["SpotPriceDKK"].mean()

#Historically min and max in the two regions
df_hourminpriceDK1 = df_hourcostDK1.to_numpy().argmin()
df_hourminpriceDK2 = df_hourcostDK2.to_numpy().argmin()
df_hourmaxpriceDK1 = df_hourcostDK1.to_numpy().argmax()
df_hourmaxpriceDK2 = df_hourcostDK2.to_numpy().argmax()

#Create range of x-axis based on hours during day
hours = np.arange(len(df_hourcostDK1))

#Change hour dataline to include every second number starting from 0 to make chart easier to read
plt.xticks(np.delete(hours, np.arange(-1, hours.size, 2)))

plt.plot(hours, df_hourcostDK1, 'bo', linestyle='solid' ,label="DK1", alpha=0.5)
plt.plot(hours, df_hourcostDK2, 'rs', linestyle='solid', label="DK2", alpha=0.5)

plt.grid(alpha = 0.4)

#vertical lines on max and min hour price overlaid on grid
plt.vlines(df_hourminpriceDK1,df_hourcostDK2.min() - 0.01, df_hourcostDK1.max(), colors='black',linestyle='dotted', label='Lowest Price')
plt.vlines(df_hourmaxpriceDK2,df_hourcostDK2.min() - 0.01, df_hourcostDK1.max(), colors='black',linestyle='dashdot', label='Highest Price')

plt.xlabel("Hour (CET)")
plt.ylabel("Price (DKK/MWh)")
plt.title("Average Price of Energy in Region DK1 vs. DK2")
plt.legend()
plt.show()

##1.2
#Data is first grouped into years and hours and then average
avg_hour_year_cost_DK2 = df_pricesDK2.groupby([df_pricesDK2["HourDK"].dt.year,df_pricesDK2["HourDK"].dt.hour]).mean()

#Figure comarping the difference in average price by hour for the years
plt.xticks(np.delete(hours, np.arange(-1, hours.size, 2)))

plt.grid(alpha = 0.4)

#Values for each year are based on the numpy matrix that is 96,1 where each index is a tuple of [year, index #] and each value is a list of [96,1] where each 24 values set is one year
plt.plot(hours, avg_hour_year_cost_DK2.values[0:24], 'o', color = '#bd7ebe', linestyle='solid' ,label=str(avg_hour_year_cost_DK2.index[0][0]))
plt.plot(hours, avg_hour_year_cost_DK2.values[24:48],'o', color = '#b2e061', linestyle='solid' ,label=str(avg_hour_year_cost_DK2.index[24][0]))
plt.plot(hours, avg_hour_year_cost_DK2.values[48:72], 'o', color = '#7eb0d5', linestyle='solid' ,label=str(avg_hour_year_cost_DK2.index[48][0]))
plt.plot(hours, avg_hour_year_cost_DK2.values[72:96], 'o', color = '#fd7f6f', linestyle='solid' ,label=str(avg_hour_year_cost_DK2.index[72][0]))

plt.xlabel("Hour (CET)")
plt.ylabel("Price (DKK/MWh)")
plt.title("Average Price of Energy in Region DK2")
plt.legend()
plt.show()

##1.3
#Check the comment github