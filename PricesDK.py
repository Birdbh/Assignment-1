def PricesDK(df_prices):
    
    # Set the Sell price equal to the spot price
    df_prices["Sell"] = df_prices["SpotPriceDKK"]
    
    # Define the fixed Tax and TSO columns
    df_prices["Tax"] = 0.7
    df_prices["TSO"] = 0.1
    
    # Add the DSO tariffs
    
    # First the winter period
    
    # Low period
    df_prices.loc[(df_prices["HourDK"].dt.month.isin([1,2,3,10,11,12]))
                  & (df_prices["HourDK"].dt.hour.isin([0,1,2,3,4,5])),
                  "DSO"] = 0.15
    # Peak period
    df_prices.loc[(df_prices["HourDK"].dt.month.isin([1,2,3,10,11,12]))
                  & (df_prices["HourDK"].dt.hour.isin([17,18,19,20])),
                  "DSO"] = 1.35
    # High period
    df_prices.loc[(df_prices["HourDK"].dt.month.isin([1,2,3,10,11,12]))
                  & (df_prices["HourDK"].dt.hour.isin([6,7,8,9,10,11,12,13,14,15,16,21,22,23])),
                  "DSO"] = 0.6
    
    # Apply for the summer period
    
    # Low period
    df_prices.loc[(df_prices["HourDK"].dt.month.isin([4,5,6,7,8,9]))
                  & (df_prices["HourDK"].dt.hour.isin([0,1,2,3,4,5])),
                  "DSO"] = 0.15
    # Peak period
    df_prices.loc[(df_prices["HourDK"].dt.month.isin([4,5,6,7,8,9]))
                  & (df_prices["HourDK"].dt.hour.isin([17,18,19,20])),
                  "DSO"] = 0.6
    # High period
    df_prices.loc[(df_prices["HourDK"].dt.month.isin([4,5,6,7,8,9]))
                  & (df_prices["HourDK"].dt.hour.isin([6,7,8,9,10,11,12,13,14,15,16,21,22,23])),
                  "DSO"] = 0.23
    
    # Calculate VAT
    df_prices["VAT"] = 0.25*(df_prices["Tax"]+df_prices["TSO"]+df_prices["DSO"]+df_prices["SpotPriceDKK"])
    
    # Calculate Buy price
    df_prices["Buy"] = df_prices["Tax"]+df_prices["TSO"]+df_prices["DSO"]+df_prices["SpotPriceDKK"]+df_prices["VAT"]
    
    return df_prices