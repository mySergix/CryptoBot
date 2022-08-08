# BACKTESTING MAIN CODE

# Python Libraries
import pandas as pd
import numpy as np
import csv
import datetime as dt
import math
import os
import random
from binance.client import Client

# Python Libraries Options
pd.options.mode.chained_assignment = None  # default='warn'

# Code Files
from Backtesting_Data import COIN, DATE
import Backtesting_DownloadData 
import Bot_Binance
import Bot_Backtesting
import Bot_Strategy
import Bot_BacktestingSizers


Get_CandlestickData(Frequency_Avail, Frequency, Coin_Cr, Coin_Fi, Date_Start, Date_End):

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
