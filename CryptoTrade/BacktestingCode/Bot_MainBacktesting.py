# BACKTESTING MAIN CODE

# Python Libraries
import pandas as pd
import numpy as np
import csv
import datetime as dt
import math
import os
import random

# Python Libraries Options
pd.options.mode.chained_assignment = None  # default='warn'

# Code Files
from Backtesting_Data import PAIR, STOCK, ASSET, DATE
import downloadData 
import Bot_Backtesting
import Bot_Strategy
import Bot_BacktestingSizers

Bot_BackTest = Bot_Backtesting.BacktestingClass(ASSET["AssetType"], PAIR, STOCK["Ticker"], DATE)
#Bot_BackTest.AddComissions(Bot_1.makerCommission)
Bot_BackTest.SetInitialMoney(1000.00)
Bot_BackTest.AddSizers(Bot_BacktestingSizers.FullMoney)
Bot_BackTest.AddBotAnalyzers()
Bot_BackTest.PrintCurrentMoney()
Bot_BackTest.BacktestingCore.addstrategy(Bot_Strategy.Strategy)
Bot_BackTest.RunStrategy()
Bot_BackTest.PrintCurrentMoney()
Bot_BackTest.PlotBacktestingResults()
