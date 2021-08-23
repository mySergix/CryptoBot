#Codigo main del bot de trading

#Importación de otros archivos del código
import pandas as pd
from Bot_Data import BINANCE, COIN, DATE, FREQUENCY
import Bot_Binance
from binance.client import Client
import csv
import datetime as dt
import math
import os
import Bot_Backtesting
import Bot_Strategy
import Bot_BacktestingSizers

API_Binance = Client(BINANCE["API_Key"], BINANCE["Secret_Key"])
Frequency_Available = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]

# Comprobación de una frecuencia correcta
def Check_frequency(Frequency_Ava, Frequency):
    check = False
    for i in range(len(Frequency_Ava)):
        if Frequency == Frequency_Ava[i]:
            check = True

    if check == True:
        print("La frecuencia seleccionada de {} es correcta. \n".format(Frequency))
    else:
        print("La frecuencia seleccionada de {} NO es correcta. \n".format(Frequency))

    return check

# Filtrado de los datos descargados
def Initial_Data_filter(Data):
    df = pd.DataFrame(Data)
    df = df.drop([6, 7, 9, 10, 11], axis=1)

    columns = ["time", "open", "high", "low", "close", "volume", "trades"]
    df.columns = columns

    for i in columns:
        df[i] = df[i].astype(float)

    df["start"] = pd.to_datetime(df["time"]*1000000,format= '%Y-%m-%d %H:%M:%S' )

    return df

def Download_candles_data(Coin, Fiat, Frequency, StartDate, EndDate):

    #Calcular el numero total de velas a descargar segun el rango de tiempo seleccionado
    FI = dt.datetime(int(StartDate[0:4]), int(StartDate[5:7]), int(StartDate[8:10]), int(StartDate[11:13]),
                    int(StartDate[14:16]), int(StartDate[17:19]))
    FF = dt.datetime(int(EndDate[0:4]), int(EndDate[5:7]), int(EndDate[8:10]), int(EndDate[11:13]),
                    int(EndDate[14:16]), int(EndDate[17:19]))
    #EndDate
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

    if not os.path.isdir("MarketData/{}{}/".format(Coin, Fiat)):
        os.mkdir("MarketData/{}{}/".format(Coin, Fiat))


    #with open("MarketData/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency), "w", encoding = "UTF8", newline="") as file:
    #    writer = csv.writer(file)

    Data.to_csv("MarketData/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency))

    return DataElements

# FIN FUNCIONES MAIN_BOT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
# INICIO MAIN_BOT

if Check_frequency(Frequency_Available, FREQUENCY):
    DataElements = Download_candles_data(COIN["Crypto"], COIN["Fiat"], FREQUENCY, DATE["StartDate"], DATE["EndDate"])
else:
    print("Error en la frecuencia seleccionada ({})\n ".format(FREQUENCY))

Bot_1 = Bot_Binance.Bot_BinanceClass(BINANCE["API_Key"], BINANCE["Secret_Key"], COIN["Crypto"], COIN["Fiat"], FREQUENCY, DataElements)

Bot_BackTest = Bot_Backtesting.BacktestingClass(COIN["Crypto"], COIN["Fiat"], FREQUENCY, DATE["StartDate"], DATE["EndDate"])
Bot_BackTest.SetInitialMoney(1000.00)
Bot_BackTest.AddComissions(Bot_1.makerCommission)
Bot_BackTest.AddSizers(Bot_BacktestingSizers.FullMoney)
Bot_BackTest.AddStrategy(Bot_Strategy.Strategy)
Bot_BackTest.AddBotAnalyzers()
Bot_BackTest.RunStrategy()
Bot_BackTest.PrintCurrentMoney()
Bot_BackTest.PlotBacktestingResults()
