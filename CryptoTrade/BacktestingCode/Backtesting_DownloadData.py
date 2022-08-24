# BACKTESTING DATA EXTRACTION

# Python Libraries
import pandas as pd
import numpy as np
import csv
import datetime as dt
import math
import os
import random
import yfinance as yf

# Checking for a correct frequency
def Check_frequency(Frequency_Ava, Frequency):
    check = False
    for i in range(len(Frequency_Ava)):
        if Frequency == Frequency_Ava[i]:
            check = True

    if check == False:
        print("The selected frequency of {} is not available. Select one of the following frequencies:  \n".format(Frequency))
        for i in range(len(Frequency_Ava)):
            print("{} \t" .format(Frequency_Ava[i]))
        exit()
    
    return check


# Download the Candlestick data into csv files for Crypto
def Download_candles_data_Crypto(Coin, Fiat, Frequency, StartDate, EndDate):

    Data = yf.download('{}-{}'.format(Coin, Fiat), start = StartDate, end = EndDate, index_as_date = False, interval = Frequency)
    Data['time'] = Data.index
    Data['time'] = Data['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Generate the directory of the data
    if not os.path.isdir("MarketData/Crypto/{}{}/".format(Coin, Fiat)):
        os.mkdir("MarketData/Crypto/{}{}/".format(Coin, Fiat))

    # If the name already exists, delete it
    if os.path.exists("MarketData/Crypto/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency)):
        os.remove("MarketData/Crypto/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency))

    Data.to_csv("MarketData/Crypto/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency))


# Download the Candlestick data into csv files for Stocks
def Download_candles_data_Stocks(Ticker, Frequency, StartDate, EndDate):

    Data = yf.get_data(Ticker, start_date = StartDate, end_date = EndDate, index_as_date = True, interval = Frequency)

    # Generate the directory of the data
    if not os.path.isdir("MarketData/Stocks/{}/".format(Ticker)):
        os.mkdir("MarketData/Stocks/{}/".format(Ticker))

    # If the name already exists, delete it
    if os.path.exists("MarketData/Stocks/{}/Freq_{}.csv".format(Ticker, Frequency)):
        os.remove("MarketData/Stocks/{}/Freq_{}.csv".format(Ticker, Frequency))

    Data.to_csv("MarketData/Stocks/{}/Freq_{}.csv".format(Ticker, Frequency))


# Function to get the Candlestick data for Crypto
def Get_CandlestickData_Crypto(Frequency_Avail, Frequency, Coin_Cr, Coin_Fi, Date_Start, Date_End):

    if Check_frequency(Frequency_Avail, Frequency):
        Download_candles_data_Crypto(Coin_Cr, Coin_Fi, Frequency, Date_Start, Date_End)
    else:
        print("Error for the selected frequency ({})\n ".format(Frequency))


# Function to get the Candlestick data for Stocks
def Get_CandlestickData_Stocks(Frequency_Avail, Frequency, Ticker, Date_Start, Date_End):

    if Check_frequency(Frequency_Avail, Frequency):
        Download_candles_data_Stocks(Ticker, Frequency, Date_Start, Date_End)
    else:
        print("Error for the selected frequency ({})\n ".format(Frequency))