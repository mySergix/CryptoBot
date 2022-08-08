# BACKTESTING DATA EXTRACTION

# Python Libraries
import pandas as pd
import numpy as np
import csv
import datetime as dt
import math
import os
import random
from binance.client import Client

# Checking for a correct frequency
def Check_frequency(Frequency_Ava, Frequency):
    check = False
    for i in range(len(Frequency_Ava)):
        if Frequency == Frequency_Ava[i]:
            check = True

    if check == True:
        print("The selected frequency of {} is correct. \n".format(Frequency))
    else:
        print("The selected frequency of {} is NOT correct. \n".format(Frequency))

    return check

# Filtering of downloaded data
def Initial_Data_filter(Data):
    df = pd.DataFrame(Data)
    df = df.drop([6, 7, 9, 10, 11], axis=1)

    columns = ["time", "open", "high", "low", "close", "volume", "trades"]
    df.columns = columns

    for i in columns:
        df[i] = df[i].astype(float)

    df["start"] = pd.to_datetime(df["time"]*1000000,format= '%Y-%m-%d %H:%M:%S' )

    return df

# Download the Candlestick data into csv files
def Download_candles_data(Coin, Fiat, Frequency, StartDate, EndDate):

    # Calculate the total number of candles to download according to the selected time range
    FI = dt.datetime(int(StartDate[0:4]), int(StartDate[5:7]), int(StartDate[8:10]), int(StartDate[11:13]),
                    int(StartDate[14:16]), int(StartDate[17:19]))
    FF = dt.datetime(int(EndDate[0:4]), int(EndDate[5:7]), int(EndDate[8:10]), int(EndDate[11:13]),
                    int(EndDate[14:16]), int(EndDate[17:19]))
    # EndDate
    Total_Time = math.floor((FF - FI).total_seconds())
    ######ELIMINAR EL ULTIMO CARACTER UNICAMENTE Y VER QUÉ CARACTER ES (m, h, d, W o M)######

    if "m" in Frequency:
        if(len(Frequency)) == 2:
            CandleSeconds = 60*float(Frequency[0])
            CandleMinutes = int(Frequency[0])
        else:
            CandleSeconds = 60*float(Frequency[:2])
            CandleMinutes = int(Frequency[:2])
    elif "h" in Frequency:
        if (len(Frequency)) == 2:
            CandleSeconds = 3600*float(Frequency[0])
            CandleMinutes = 60*int(Frequency[0])
        else:
            CandleSeconds = 3600*float(Frequency[:2])
            CandleMinutes = 60*int(Frequency[:2])
    elif "d" in Frequency:
        CandleSeconds = 86400*float(Frequency[0])
        CandleMinutes = 24*60*int(Frequency[0])
    elif "w" in Frequency:
        CandleSeconds = 7*86400*float(Frequency[0])
        CandleMinutes = 7*24*60*int(Frequency[0])
    elif "M" in Frequency:
        CandleSeconds = 30*86400*float(Frequency[0])
        CandleMinutes = 30*24*60*int(Frequency[0])

    DataElements = math.floor(Total_Time/CandleSeconds)

    Header = ["time", "open", "high", "low", "close", "volume", "trades", "start"]
    Data = API_Binance.get_klines(symbol = Coin+Fiat, interval = Frequency, limit = DataElements)
    Data = Initial_Data_filter(Data)

    # Generate the directory of the data
    if not os.path.isdir("MarketData/{}{}/".format(Coin, Fiat)):
        os.mkdir("MarketData/{}{}/".format(Coin, Fiat))

    # If the name already exists, delete it
    if os.path.exists("MarketData/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency)):
        os.remove("MarketData/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency))

    Data.to_csv("MarketData/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency))

    return DataElements

# Function to get the Candlestick data
def Get_CandlestickData(Frequency_Avail, Frequency, Coin_Cr, Coin_Fi, Date_Start, Date_End):

    if Check_frequency(Frequency_Avail, Frequency):
        DataElements = Download_candles_data(Coin_Cr, Coin_Fi, Frequency, Date_Start, Date_End)
    else:
        print("Error for the selected frequency ({})\n ".format(Frequency))