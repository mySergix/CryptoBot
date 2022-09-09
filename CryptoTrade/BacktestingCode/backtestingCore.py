# BACKTESTING BOT CLASS FILE: functions defined to implement the backtesting.

# Python libraries.
import pandas as pd
import math
import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import datetime as dt
import csv

# Imported files.
from settings import FREQUENCIES
import downloadData
import strategy

class BacktestingClass:

    def __init__(self, assetType: int, pair: dict, stock: str, date: dict, dataFrequency: list):

        '''
        Constructor of the class: setting all the information for the backtesting and downloading the subsequent candlestick data,
        which is entered into the strategy class.

            @param assetType: type of asset selected (0 for cryptocurrency, 1 for stocks).
            @param pair: cryptocurrency pair selected (must be in Yahoo Finance list).
            @param stock: stock selected (must be in Yahoo Finance list).
            @param date: start and end dates selected (year-month-day).
            @param dataFrequency: data frequencies selected.

        '''

        self.pair = pair
        self.stock = stock

        self.dtStartDate = dt.datetime(int(date["StartDate"][0:4]), int(date["StartDate"][5:7]), int(date["StartDate"][8:10]))
        self.dtEndDate = dt.datetime(int(date["EndDate"][0:4]), int(date["EndDate"][5:7]), int(date["EndDate"][8:10]))
        self.cerebro = bt.Cerebro()

        for freq in dataFrequency:

            if assetType == 0:
                # Downloading data for cryptocurrency
                downloadData.dataCrypto(FREQUENCIES, freq, self.pair, date["StartDate"], date["EndDate"])

                # Cryptocurrency data feeded into the backtesting
                data = bt.feeds.YahooFinanceCSVData(
                    dataname = ("MarketData/Crypto/{}{}/Freq_{}.csv".format(self.pair["Base"], self.pair["Quote"], freq)),
                    fromdate = self.dtStartDate,
                    todate = self.dtEndDate,
                    reverse = False)

            elif assetType == 1:
                # Downloading data for stocks
                downloadData.dataStocks(FREQUENCIES, freq, self.stock, date["StartDate"],date["EndDate"])

                # Stocks data feeded into the backtesting
                data = bt.feeds.YahooFinanceCSVData(
                    dataname = ("MarketData/Stocks/{}/Freq_{}.csv".format(self.stock, freq)),
                    fromdate = self.dtStartDate,
                    todate = self.dtEndDate,
                    reverse = False)

            self.cerebro.adddata(data)

    def setInitialMoney(self, money):

        '''
        Setting initial cash of the portfolio.

            @param money: cash of the portfolio.

            @return none
        '''

        self.cerebro.broker.setcash(money)
        self.InitialMoney = money

    def printCurrentMoney(self):

        '''
        Printing the current portfolio value.

            @return none
        '''

        print("Current Portfolio Value: %.2f" % self.cerebro.broker.getvalue())

    def setComissions(self, comissions):

        '''
        Setting Binance commissions.

            @param comissions: broker comission for each trade.

            @return none
        '''

        self.cerebro.broker.setcommission(commission = comissions)

    def setSizers(self, sizer):

        '''
        Setting portfolio percentage for each trade.

            @param sizer: sizers class.

            @return none
        '''

        self.cerebro.addsizer(sizer)

    def setStrategy(self, strategy):

        '''
        Setting backtesting strategy.

            @param strategy: strategy class.

            @return none
        '''

        self.cerebro.addstrategy(strategy)

    # Run the implemented strategy
    def runStrategy(self):

        '''
        Running the implemented class.

            @return none
        '''

        self.strats = self.cerebro.run()
        self.strat = self.strats[0]
        self.results = self.strat.analyzers.ta.get_analysis()

    def plotBacktestingResults(self):
        
        '''
        Plotting backtesting results: market analyzers and backtesting plots.

            @return none
        '''

        self.printMarketAnalyzers()
        self.cerebro.plot()

    def setBotAnalyzers(self):

        '''
        Setting bot analyzers (see documentation:
        https://www.backtrader.com/docu/analyzers/analyzers/)

            @return none
        '''

        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")

    def printMarketAnalyzers(self):

        '''
        Printing market analyzers plot. If there are no trades, this function
        warns the user.

            @return none
        '''

        results = self.strat.analyzers.ta.get_analysis()

        if results.total.total==0:
            print("There have been no trades for the current backtesting.")
            return

        else:
            closedTrades = results.total.closed
            wonTrades = results.won.total
            winRatio = wonTrades/closedTrades
            netProfit = results.pnl.net.total
            totalReturn = (netProfit/self.InitialMoney)*100

            totalDays = (self.dtEndDate - self.dtStartDate).days
            monthlyReturn = totalReturn*30.0/totalDays

            fig, ax = plt.subplots(1,1)

            column = ["Results"]

            rows = ["Closed trades",
                     "Won trades",
                     "Win ratio",
                     "Net profit",
                     "Total return",
                     "Start period",
                     "End period",
                     "Monthly return"]

            results = [["{}".format(closedTrades)],
                          ["{}".format(wonTrades)],
                          ["{:.2f} %".format(100*winRatio)],
                          ["{:.2f} {}".format(netProfit, self.pair["Quote"])],
                          ["{:.2f} %".format(totalReturn)],
                          ["{}".format(self.dtStartDate)],
                          ["{}".format(self.dtEndDate)],
                          ["{:.2f} %".format(monthlyReturn)]]

            df = pd.DataFrame(results, columns = column)
            ax.axis('tight')
            ax.axis('off')
            ax.table = plt.table(cellText = df.values,
                              rowLabels = rows,
                              colLabels = column,
                              colWidths =  None,
                              loc = "center")
            ax.table.set_fontsize(20)
            ax.table.scale(1.8, 1.8)

            for (row, col), cell in ax.table.get_celld().items():
                if (row == 0) or (col == -1):
                    cell.set_text_props(fontproperties=FontProperties(weight='bold'))

            ax.table.auto_set_column_width(col=list(range(len(df.columns))))
            plt.title("Backtesting Results", fontsize = 30, fontweight="bold")
