import backtrader as bt
import datetime as dt
import pandas as pd


class Strategy_SMA(bt.Strategy):

    params = (
        ('FastSMA', 30), 
        ('SlowSMA', 250),
        ("percents", 100)
    )

    def __init__(self):

        # Data Feeds
        self.Data_15m = self.datas[0]
        #self.Data_1h = self.data1
        #self.Data_4h = self.data2

        self.FastSMA = self.params.FastSMA
        self.SlowSMA = self.params.SlowSMA
        print(self.datas[0])
        self.sma = bt.talib.SMA(self.datas[0], timeperiod=30)

        #self.Fast_SMA_15m = bt.talib.SMA(self.Data_15m, period = self.FastSMA)
        #self.Slow_SMA_15m = bt.talib.SMA(self.Data_15m, period = self.SlowSMA)

        # self.SMA_Crossover_15m = bt.ind.CrossOver(self.Fast_SMA_15m, self.Slow_SMA_15m)

    # def notify_order(self, order):
    #     if order.status in [order.Submitted, order.Accepted]:
    #         return

    #     if order.status in [order.Completed]:
    #         if order.isbuy():
    #             self.log("Compra, %.2f" % order.executed.price)
    #         elif order.issell():
    #             self.log("Venta, %.2f" % order.executed.price)

    # def prenext(self):
    #     self.log("Close, %.2f" % self.Data_15m.close)

    # def next(self):
    #     #self.log("Close, %.2f" % self.dataclose[0])
    #     self.stoploss()

    #     # if self.position:
    #     #     if self.SMA_Crossover_15m < 0.0:
    #     #         self.close()
    #     #         self.log("Venta, %.2f" % self.dataclose[0])

    #     # if not self.position:
    #     #     if self.SMA_Crossover_15m > 0.0:
    #     #         self.buy()
    #     #         self.log("Compra, %.2f" % self.dataclose[0])

    # def log(self, txt, dt = None):
    #     dt = dt or self.data0.datetime.date(0)
    #     #print("{} {}".format(dt, txt))

    # #def stop(self):
    # #    print(self.position)

    # def stoploss(self):
    #     if self.Data_15m.close < 0.90*float(self.position.price):
    #         self.close()

    # def get_numberofcandles(self, totaltime):

    #     if self.Frequency[-1] == totaltime[-1]:
    #         candle_ratio = int(totaltime[0 : len(totaltime)-1 : ])/int(self.Frequency[0 : len(self.Frequency)-1 : ])
    #     else:
    #         if self.Frequency[-1] == "m":
    #             freq_seconds = 60*int(self.Frequency[0 : len(self.Frequency)-1 : ])
    #         elif self.Frequency[-1] == "h":
    #             freq_seconds = 3600*int(self.Frequency[0 : len(self.Frequency)-1 : ])
    #         elif self.Frequency[-1] == "d":
    #             freq_seconds = 7*3600*int(self.Frequency[0 : len(self.Frequency)-1 : ])

    #         if totaltime[-1] == "m":
    #             totaltime_seconds = 60*int(totaltime[0 : len(totaltime)-1 : ])
    #         elif totaltime[-1] == "h":
    #             totaltime_seconds = 3600*int(totaltime[0 : len(totaltime)-1 : ])
    #         elif totaltime[-1] == "d":
    #             totaltime_seconds = 7*3600*int(totaltime[0 : len(totaltime)-1 : ])

    #         candle_ratio = totaltime_seconds/freq_seconds

    #     return candle_ratio
