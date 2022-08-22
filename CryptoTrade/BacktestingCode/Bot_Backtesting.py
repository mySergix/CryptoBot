# BACKTESTING BOT CLASS FILE

# Libraries
import pandas as pd
import math
import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import datetime as dt
import csv

# Files imported
from Backtesting_Data import Frequency_Available
import Backtesting_DownloadData
import Bot_Strategy

class BacktestingClass:

    # CONSTRUCTOR
    def __init__(self, AssetType, Crypto, Fiat, Stock, StartDate, EndDate):

        self.Crypto = Crypto
        self.Fiat = Fiat
        self.Stock = Stock
       
        self.StartDate = dt.datetime(int(StartDate[0:4]), int(StartDate[5:7]), int(StartDate[8:10]))
        self.EndDate = dt.datetime(int(EndDate[0:4]), int(EndDate[5:7]), int(EndDate[8:10]))
        self.BacktestingCore = bt.Cerebro()

        DataFrequency = ['1h', '1d']

        for Freq in DataFrequency:
            if Freq[-1] == "m":
                self.TimeFrame = bt.TimeFrame.Minutes
                self.Compresion = 1
                self.formatodt = "%Y-%m-%d %H:%M:%S"
            elif Freq[-1] == "h":
                self.TimeFrame = bt.TimeFrame.Minutes
                self.Compresion = 60*int(Freq[0 : len(Freq)-1 : ])
                self.formatodt = "%Y-%m-%d %H:%M:%S"
            elif Freq[-1] == "d":
                self.TimeFrame = bt.TimeFrame.Days
                self.Compresion = 1 # Revisar lo de compression
                self.formatodt = "%Y-%m-%d"

            if AssetType == 0:
                # Data Downloading for Crypto
                Backtesting_DownloadData.Get_CandlestickData_Crypto(Frequency_Available, Freq, self.Crypto, self.Fiat, StartDate, EndDate)

                # Data feeded into the backtesting bot (Crypto)
                Data = bt.feeds.YahooFinanceCSVData(
                    dataname = ("MarketData/Crypto/{}{}/Freq_{}.csv".format(self.Crypto, self.Fiat, Freq)),
                    fromdate = self.StartDate,
                    todate = self.EndDate,
                    reverse = False)

            elif AssetType == 1:
                # Data Downloading for Stocks
                Backtesting_DownloadData.Get_CandlestickData_Stocks(Frequency_Available, Freq, self.Stock, StartDate, EndDate)
             
                # Data feeded into the backtesting bot (Stocks)
                Data = bt.feeds.YahooFinanceCSVData(
                    dataname = ("MarketData/Stocks/{}/Freq_{}.csv".format(self.Stock, Freq)),
                    fromdate = self.StartDate,
                    todate = self.EndDate,
                    reverse = False)

            self.BacktestingCore.adddata(Data)

        #________________________________________________________________________________________________________________
        # END CONSTRUCTOR

    # Set the initial quantity to invest
    def SetInitialMoney(self, Money):
        self.BacktestingCore.broker.setcash(Money)
        self.InitialMoney = Money

    # Show on screen the current portfolio value
    def PrintCurrentMoney(self):
        print("Current Portfolio Value: %.2f" % self.BacktestingCore.broker.getvalue())

    # Add Binance comissions
    def AddComissions(self, Comissions):
        self.BacktestingCore.broker.setcommission(commission = Comissions)

    # Add the money percentage of each trade
    def AddSizers(self, Sizer):
        self.BacktestingCore.addsizer(Sizer)

    # Add a backtesting strategy
    def AddStrategy(self, Strat):
        self.BacktestingCore.addstrategy(Strat)

    # Run the implemented strategy
    def RunStrategy(self):
        self.strats = self.BacktestingCore.run()
        self.strat = self.strats[0]
        self.results = self.strat.analyzers.ta.get_analysis()

    # Plot the obtained results
    def PlotBacktestingResults(self):
        self.Print_MarketAnalyzers()
        self.BacktestingCore.plot()

    def AddBotAnalyzers(self):
        self.BacktestingCore.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")

    def ExtractBacktestingResults(self):
        try:
            return self.results.pnl.net.total
        except KeyError:
            return 0.0

    def Print_MarketAnalyzers(self):

        results = self.strat.analyzers.ta.get_analysis()

        print(results)
        Ordenes_Cerradas = results.total.closed
        Ordenes_Positivas = results.won.total
        Win_Ratio = Ordenes_Positivas/Ordenes_Cerradas
        Net_Profit = results.pnl.net.total
        Retorno_Total = (Net_Profit/self.InitialMoney)*100

        Total_Days = (self.EndDate - self.StartDate).days
        Ratio = 30/Total_Days
        Retorno_Mensual = Retorno_Total*Ratio

        fig, ax = plt.subplots(1,1)

        columnas = ["Results"]

        filas = ["Closed Orders",
                 "Won Orders",
                 "Win Ratio",
                 "Net Profit",
                 "Total Return",
                 "Start Period",
                 "End Period",
                 "Mensual Return"]

        resultados = [["{}".format(Ordenes_Cerradas)],
                      ["{}".format(Ordenes_Positivas)],
                      ["{:.2f} %".format(100*Win_Ratio)],
                      ["{:.2f} {}".format(Net_Profit, self.Fiat)],
                      ["{:.2f} %".format(Retorno_Total)],
                      ["{}".format(self.StartDate)],
                      ["{}".format(self.EndDate)],
                      ["{:.2f} %".format(Retorno_Mensual)]]

        df = pd.DataFrame(resultados, columns = columnas)
        ax.axis('tight')
        ax.axis('off')
        ax.table = plt.table(cellText = df.values,
                          rowLabels = filas,
                          colLabels = columnas,
                          colWidths =  None,
                          loc = "center")
        ax.table.set_fontsize(20)
        ax.table.scale(1.8, 1.8)

        for (row, col), cell in ax.table.get_celld().items():
            if (row == 0) or (col == -1):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))

        ax.table.auto_set_column_width(col=list(range(len(df.columns))))
        plt.title("Backtesting Results", fontsize = 30, fontweight="bold")
