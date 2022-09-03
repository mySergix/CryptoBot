# BACKTESTING MAIN CODE

# Python libraries
import pandas as pd
import numpy as np
import csv
import datetime as dt
import math
import os
import random

# Python libraries options
pd.options.mode.chained_assignment = None  # default='warn'

# Imported files
from settings import PAIR, STOCK, ASSET, DATE
import downloadData
import backtestingCore
import strategy as strat
import sizers

backStrategy = backtestingCore.BacktestingClass(ASSET["AssetType"], PAIR, STOCK["Ticker"], DATE, strat.dataFrequency)
# Bot_BackTest.setComissions(Bot_1.makerCommission)
backStrategy.setInitialMoney(1000.0)
backStrategy.setSizers(sizers.FullMoney)
backStrategy.setBotAnalyzers()
backStrategy.setStrategy(strat.Strategy)
backStrategy.runStrategy()
backStrategy.printCurrentMoney()
backStrategy.plotBacktestingResults()
