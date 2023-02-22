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
    #df_prices['SpotPriceDKK'] = df_prices['SpotPriceDKK']/1000

    #Include DK1 & DK2 Areas in Dataframe
    df_prices = df_prices.loc[(df_prices['PriceArea']=='DK1') | (df_prices['PriceArea']=='DK2')]

    #Adjust DataFrame Labels
    df_prices = df_prices[['HourDK','PriceArea','SpotPriceDKK']]
    
    # Sort values
    df_prices = df_prices.sort_values('HourDK')
    
    # Keep part from start to end time and sort
    t_s = pd.Timestamp(dt.datetime(2019, 1, 1, 0, 0, 0), tz='CET')
    t_e = pd.Timestamp(dt.datetime(2022, 12, 31, 23, 0, 0), tz='CET')
    
    df_prices = df_prices.loc[(df_prices['HourDK']>=t_s) & (df_prices['HourDK']<=t_e)]
    df_prices = df_prices.reset_index(drop=True)
    
    return df_prices

CreatePricesDf()