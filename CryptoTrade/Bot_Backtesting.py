import backtrader as bt
import Bot_Strategy
import datetime as dt
import backtrader.analyzers as btanalyzers
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
import math

class BacktestingClass:

    # CONSTRUCTOR
    #_________________________________________________________________________________________________
    def __init__(self, BINANCE_KEYS, Crypto, Fiat, Frequency, StartDate, EndDate):
        self.BINANCE_KEYS = BINANCE_KEYS
        self.Crypto = Crypto
        self.Fiat = Fiat
        self.Frequency = Frequency
        self.StartDate = dt.datetime(int(StartDate[0:4]), int(StartDate[5:7]), int(StartDate[8:10]), int(StartDate[11:13]),
                        int(StartDate[14:16]), int(StartDate[17:19]))
        self.EndDate = dt.datetime(int(EndDate[0:4]), int(EndDate[5:7]), int(EndDate[8:10]), int(EndDate[11:13]),
                        int(EndDate[14:16]), int(EndDate[17:19]))

        self.BacktestingCore = bt.Cerebro()

        if self.Frequency[-1] == "m":
            self.TimeFrame = bt.TimeFrame.Minutes
            self.Compresion = 1
            self.formatodt = "%Y-%m-%d %H:%M:%S"
        elif self.Frequency[-1] == "h":
            self.TimeFrame = bt.TimeFrame.Minutes
            self.Compresion = 60*int(self.Frequency[0 : len(self.Frequency)-1 : ])
            self.formatodt = "%Y-%m-%d %H:%M:%S"
        elif self.Frequency[-1] == "d":
            self.TimeFrame = bt.TimeFrame.Days
            self.Compresion = 1
            self.formatodt = "%Y-%m-%d"

        self.Data = bt.feeds.GenericCSVData(
             name = self.Crypto,
             dataname = ("MarketData/{}{}/Freq_{}.csv".format(self.Crypto, self.Fiat, self.Frequency)),
             timeframe = self.TimeFrame,

             compression = self.Compresion,
             fromdate = self.StartDate,
             todate = self.EndDate,
             dtformat = self.formatodt,
             nullvalue = 0.0,
             datetime = 8,
             high = 3,
             low = 4,
             open = 2,
             close = 5
        )

        self.BacktestingCore.adddata(self.Data)

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

        Ordenes_Cerradas = results.total.closed
        Ordenes_Positivas = results.won.total
        Win_Ratio = Ordenes_Positivas/Ordenes_Cerradas
        Net_Profit = results.pnl.net.total
        Retorno_Total = (Net_Profit/self.InitialMoney)*100

        Total_Days = math.floor((self.EndDate - self.StartDate).total_seconds())/(3600*24)
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
                 "Frequency",
                 "Mensual Return"]

        resultados = [["{}".format(Ordenes_Cerradas)],
                      ["{}".format(Ordenes_Positivas)],
                      ["{:.2f} %".format(100*Win_Ratio)],
                      ["{:.2f} {}".format(Net_Profit, self.Fiat)],
                      ["{:.2f} %".format(Retorno_Total)],
                      ["{}".format(self.StartDate)],
                      ["{}".format(self.EndDate)],
                      ["{}".format(self.Frequency)],
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
