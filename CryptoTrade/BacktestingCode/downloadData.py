# BACKTESTING DATA EXTRACTION: User defined functions for extracting the datasets containing the information of the market (candles) from Yahoo Finance.

# Python Libraries
import pandas as pd
import numpy as np
import csv
import datetime as dt
import math
import os
import random
import yfinance as yf


def checkFrequency(FrequencyAva: list, Frequency: str):

    '''
    Checking for a correct frequency: Check if the frequency of the data selected by the user exists in the repository of Yahoo Finance.
    Otherwise, prints an error message suggesting the available frequencies.

        @param FrequencyAva: List of frequencies avaliable from Yahoo Finance.
        @param Frequency: User desired frequency.

        @return check: Boleean variable that is true if Frequency exists in FrequencyAva.
    '''

    check = False
    for i in range(len(FrequencyAva)):
        if Frequency == FrequencyAva[i]:
            check = True

    if check == False:
        print("The selected frequency of {} is not available. Select one of the following frequencies:  \n".format(Frequency))
        for i in range(len(FrequencyAva)):
            print("{} \t" .format(FrequencyAva[i]))
        exit()

    return check

def dataCrypto(FrequencyAva: list, Frequency: str, Pair: tuple, StartDate: str, EndDate: str):

    '''
    Downloading the candlestick data into .csv files for cryptocurrencies.

        @param FrequencyAva: List of frequencies avaliable from Yahoo Finance.
        @param Frequency: User desired frequency.
        @param Pair: Coin pair operated.
        @param StartDate: Starting date of the downloaded data.
        @param EndDate: Ending date of the downloaded data.

        @return None
    '''

    # Downloading in case the frequency exists
    if checkFrequency(FrequencyAva, Frequency):

        # Dowloading data from Yahoo Finance
        Data = yf.download('{}-{}'.format(Pair["Base"], Pair["Quote"]), start = StartDate, end = EndDate, index_as_date = False, interval = Frequency)
        Data['time'] = Data.index
        Data['time'] = Data['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Generating the directory of the data
        if not os.path.isdir("MarketData/Crypto/{}{}/".format(Pair["Base"], Pair["Quote"])):
            os.mkdir("MarketData/Crypto/{}{}/".format(Pair["Base"], Pair["Quote"]))

        # Deleting the name in case it already exists
        if os.path.exists("MarketData/Crypto/{}{}/Freq_{}.csv".format(Pair["Base"], Pair["Quote"], Frequency)):
            os.remove("MarketData/Crypto/{}{}/Freq_{}.csv".format(Pair["Base"], Pair["Quote"], Frequency))

        # Generating .csv file from DataFrame
        Data.to_csv("MarketData/Crypto/{}{}/Freq_{}.csv".format(Pair["Base"], Pair["Quote"], Frequency))

    else:
        print("Error for the selected frequency ({})\n ".format(Frequency))


def dataStocks(FrequencyAva: list, Frequency: str, Ticker: str, StartDate: str, EndDate: str):

    '''
    Downloading the candlestick data into .csv files for stocks.

        @param FrequencyAva: List of frequencies avaliable from Yahoo Finance.
        @param Frequency: User desired frequency.
        @param Pair: Coin pair operated.
        @param StartDate: Starting date of the downloaded data.
        @param EndDate: Ending date of the downloaded data.

        @return None
    '''

    # Downloading in case the frequency exists
    if checkFrequency(FrequencyAva, Frequency):

        # Dowloading data from Yahoo Finance
        Data = yf.get_data(Ticker, start_date = StartDate, end_date = EndDate, index_as_date = True, interval = Frequency)
        Data['time'] = Data.index
        Data['time'] = Data['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Generating the directory of the data
        if not os.path.isdir("MarketData/Stocks/{}/".format(Ticker)):
            os.mkdir("MarketData/Stocks/{}/".format(Ticker))

        # Deleting the name in case it already exists
        if os.path.exists("MarketData/Stocks/{}/Freq_{}.csv".format(Ticker, Frequency)):
            os.remove("MarketData/Stocks/{}/Freq_{}.csv".format(Ticker, Frequency))

        # Generating .csv file from DataFrame
        Data.to_csv("MarketData/Stocks/{}/Freq_{}.csv".format(Ticker, Frequency))

    else:
        print("Error for the selected frequency ({})\n ".format(Frequency))
