from CreatePricesDf import CreatePricesDf
import matplotlib.pyplot as plt
import numpy as np

#Creation of dataframe Using modified CreatPricesDf()
df_prices = CreatePricesDf()

#Average energy price by year grouped into regions DK1 and DK2
avg_year_cost_DK1 = df_prices.loc[df_prices["PriceArea"]=="DK1"].groupby(df_prices["HourDK"].dt.year)["SpotPriceDKK"].mean()

avg_year_cost_DK2 = df_prices.loc[df_prices["PriceArea"]=="DK2"].groupby(df_prices["HourDK"].dt.year)["SpotPriceDKK"].mean()

##Figure comparing the difference in average price by year for regions DK1 and DK2
#X-axis is being defined for the specified years range
Years = ['2019', '2020', '2021', '2022']
Years_Axis = np.arange(len(Years))

fig, ax = plt.subplots()

#Years axis is being shifted to account for just over half of the bar width
ax.bar(Years_Axis - 0.16, avg_year_cost_DK1.values, width = 0.30, label = "DK1" , color = 'b')
ax.bar(Years_Axis + 0.16, avg_year_cost_DK2.values, width = 0.30, label = "DK2", color = 'r')

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

##Average energy price for regions DK1 and DK2 grouped and average by hour of day
#grouby function is applied to the loc of DK1 and DK2 and then averaged
avg_hour_cost_DK1 = df_prices.loc[df_prices["PriceArea"]=="DK1"].groupby(df_prices["HourDK"].dt.hour)["SpotPriceDKK"].mean()

avg_hour_cost_DK2 = df_prices.loc[df_prices["PriceArea"]=="DK2"].groupby(df_prices["HourDK"].dt.hour)["SpotPriceDKK"].mean()

##Historically highest and lowest hour price for regions DK1 and DK2
hour_max_price_DK1 = avg_hour_cost_DK1.to_numpy().argmax()
hour_max_price_DK2 = avg_hour_cost_DK2.to_numpy().argmax()

hour_min_price_DK1 = avg_hour_cost_DK1.to_numpy().argmin()
hour_min_price_DK2 = avg_hour_cost_DK2.to_numpy().argmin()

##Figure comparing the difference in average price by hour for regions DK1 and DK2
#Create range of x-axis based on hours during day
hours = np.arange(len(avg_hour_cost_DK1))

#Change hour dataline to include every second number starting from 0 to make chart easier to read
plt.xticks(np.delete(hours, np.arange(-1, hours.size, 2)))

plt.plot(hours, avg_hour_cost_DK1, 'bo', linestyle='solid' ,label="DK1", alpha=0.5)
plt.plot(hours, avg_hour_cost_DK2, 'rs', linestyle='solid', label="DK2", alpha=0.5)

plt.grid(alpha = 0.4)

#vertical lines on max and min hour price overlaid on grid
plt.vlines(hour_min_price_DK1,avg_hour_cost_DK2.min() - 0.01, avg_hour_cost_DK1.max(), colors='black',linestyle='dotted', label='Lowest Price')
plt.vlines(hour_max_price_DK2,avg_hour_cost_DK2.min() - 0.01, avg_hour_cost_DK1.max(), colors='black',linestyle='dashdot', label='Highest Price')

plt.xlabel("Hour (CET)")
plt.ylabel("Price (DKK/MWh)")
plt.title("Average Price of Energy in Region DK1 vs. DK2")
plt.legend()
plt.show()

##Average spot price for each hour of day considering each of the 4 year of data
#Data is first grouped into years and hours and then average
avg_hour_year_cost_DK2 = df_prices.loc[df_prices["PriceArea"]=="DK2"].groupby([df_prices["HourDK"].dt.year,df_prices["HourDK"].dt.hour]).mean()

##Figure comparing the difference in average price by hour for years 2019, 2020, 2021, and 2022 in region DK2
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