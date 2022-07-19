#Codigo main del bot de trading

#Importación de otros archivos del código
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from Bot_Data import BINANCE, COIN, DATE, FREQUENCY
import Bot_Binance
from binance.client import Client
import csv
import datetime as dt
import math
import os
import random
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

    if os.path.exists("MarketData/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency)):
        os.remove("MarketData/{}{}/Freq_{}.csv".format(Coin, Fiat, Frequency))
    
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

FastSMA_Range = [5, 40]
SlowSMA_Range = [40, 300]

N_Pop = 50 # Population
N_Generations = 10 # Generations to test
P_Best = 0.10 # The 30% of the best individuals are used for reproduction
P_Cross = 0.20 # 20% Crossover probability
P_Mut = 0.60 # 20% Mutation Probability

SMA_Params = []
Best_Individuals = []

for i in range(N_Pop):
    RandomFast = random.randint(FastSMA_Range[0], FastSMA_Range[1]) # Fast SMA Parameters
    RandomSlow = random.randint(SlowSMA_Range[0], SlowSMA_Range[1]) # Slow SMA Parameters
    SMA_Params.append([RandomFast, RandomSlow, 0, 0, 0])

SMA_Params = pd.DataFrame(SMA_Params, columns=['FastSMA', 'SlowSMA', 'NetProfit', 'InitialMoney', 'FinalMoney'])
Best_Individuals = pd.DataFrame(Best_Individuals, columns=['FastSMA', 'SlowSMA', 'NetProfit'])

for i in range(N_Generations):
    for j in range(N_Pop):
          
        Bot_BackTest = Bot_Backtesting.BacktestingClass(COIN["Crypto"], COIN["Fiat"], FREQUENCY, DATE["StartDate"], DATE["EndDate"])

        Bot_BackTest.AddComissions(Bot_1.makerCommission)
        Bot_BackTest.SetInitialMoney(1000.00)
        Bot_BackTest.AddSizers(Bot_BacktestingSizers.FullMoney)
        Bot_BackTest.AddBotAnalyzers()
        SMA_Params['InitialMoney'][j] = Bot_BackTest.BacktestingCore.broker.getvalue()
        Bot_BackTest.BacktestingCore.addstrategy(Bot_Strategy.Strategy, FastSMA=SMA_Params['FastSMA'][j], SlowSMA=SMA_Params['SlowSMA'][j], percents=100)
        Bot_BackTest.RunStrategy()
        
        Net_Profit = Bot_BackTest.ExtractBacktestingResults()
        SMA_Params['NetProfit'][j] = Net_Profit
        SMA_Params['FinalMoney'][j] = Bot_BackTest.BacktestingCore.broker.getvalue()
        
    Best_Individuals = SMA_Params.nlargest(n=int(N_Pop*P_Best), columns=['NetProfit'])
    SMA_Params = SMA_Params.sort_values(by=['NetProfit'], ascending=False)
    SMA_Params = SMA_Params.reset_index(drop = True)

    print('Generation: {}, Best Net Profit: {}'.format(i, Best_Individuals.iloc[0,2]))

    for k in range(int((1.0 - P_Best) * N_Pop)):
        Father1 = Best_Individuals.sample(n=1)
        Father2 = Best_Individuals.sample(n=1)
        
        SMA_Params['FastSMA'][k + int(P_Best*N_Pop)] = math.floor((int(Father1['FastSMA']) + int(Father2['FastSMA'])) / 2)
        SMA_Params['SlowSMA'][k + int(P_Best*N_Pop)] = math.floor((int(Father1['SlowSMA']) + int(Father2['SlowSMA'])) / 2)
    
        if random.uniform(0, 1) <= P_Mut:
            if random.uniform(0, 1) <= 0.50:
                SMA_Params['FastSMA'][k + int(P_Best*N_Pop)] = random.randint(FastSMA_Range[0], FastSMA_Range[1])
            else:
                SMA_Params['SlowSMA'][k + int(P_Best*N_Pop)] = random.randint(SlowSMA_Range[0], SlowSMA_Range[1])


print(Best_Individuals)

print('Test with the best results: \n')

Bot_BackTest = Bot_Backtesting.BacktestingClass(COIN["Crypto"], COIN["Fiat"], FREQUENCY, DATE["StartDate"], DATE["EndDate"])
Bot_BackTest.AddComissions(Bot_1.makerCommission)
Bot_BackTest.SetInitialMoney(1000.00)
Bot_BackTest.AddSizers(Bot_BacktestingSizers.FullMoney)
Bot_BackTest.AddBotAnalyzers()
Bot_BackTest.BacktestingCore.addstrategy(Bot_Strategy.Strategy, FastSMA=Best_Individuals['FastSMA'][0], SlowSMA=Best_Individuals['SlowSMA'][0])
Bot_BackTest.RunStrategy()
Bot_BackTest.PrintCurrentMoney()
Bot_BackTest.PlotBacktestingResults()
