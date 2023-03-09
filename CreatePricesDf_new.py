import pandas as pd
import os
import datetime as dt

def CreatePricesDf():

    # Load the data
    price_path = os.path.join(os.getcwd(),'Elspotprices.xlsx')
    df_prices = pd.read_excel(price_path)
    
    # Add timezone information
    df_prices['HourUTC'] = df_prices['HourUTC'].dt.tz_localize('UTC')
    df_prices['HourDK'] = df_prices['HourUTC'].dt.tz_convert('CET')
    
    # Convert prices and filter
    df_prices['SpotPriceDKK'] = df_prices['SpotPriceDKK']/1000

    #Seperating each zone
    #DK1
    df_pricesDK1 = df_prices.loc[df_prices['PriceArea']=="DK1"]
    df_pricesDK1 = df_pricesDK1[['HourUTC','HourDK','SpotPriceDKK']]
    #DK2
    df_pricesDK2 = df_prices.loc[df_prices['PriceArea']=="DK2"]
    df_pricesDK2 = df_pricesDK2[['HourUTC','HourDK','SpotPriceDKK']]
    
    # Sort values
    df_pricesDK1 = df_pricesDK1.sort_values('HourUTC')
    df_pricesDK2 = df_pricesDK2.sort_values('HourUTC')
    
    # Keep part from start to end time and sort
    t_s = pd.Timestamp(dt.datetime(2019, 9, 1, 0, 0, 0), tz='CET')
    t_e = pd.Timestamp(dt.datetime(2022, 10, 31, 23, 0, 0), tz='CET')
    
    #Locating all times in the choosen zone
    #DK1
    df_pricesDK1 = df_pricesDK1.loc[(df_pricesDK1['HourDK']>=t_s) & (df_pricesDK1['HourDK']<=t_e)]
    df_pricesDK1 = df_pricesDK1.reset_index(drop=True)
    #DK2
    df_pricesDK2 = df_pricesDK2.loc[(df_pricesDK2['HourDK']>=t_s) & (df_pricesDK2['HourDK']<=t_e)]
    df_pricesDK2 = df_pricesDK2.reset_index(drop=True)
    
    return df_pricesDK1, df_pricesDK2