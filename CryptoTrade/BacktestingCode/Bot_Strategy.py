import backtrader as bt
import datetime as dt
import pandas as pd


class Strategy(bt.Strategy):

    params = (
        ('FastSMA', 10), 
        ('SlowSMA', 50),
        ("percents", 100)
    )

    def __init__(self):

        # self.FastSMA = self.params.FastSMA
        # self.SlowSMA = self.params.SlowSMA

        # self.Fast_SMA = bt.indicators.SimpleMovingAverage(self.dataclose, period = self.FastSMA)
        # self.Slow_SMA = bt.indicators.SimpleMovingAverage(self.dataclose, period = self.SlowSMA)

        # Data Feeds
        self.Data_1h = self.data0

        # print(
        #     "{} o {} \th {} \tl {} \tc {}\tv {}".format( 
        #     self.Data_1h.datetime.datetime(),
        #     self.Data_1h.open,
        #     self.Data_1h.high[0],
        #     self.datas[0].low[0],
        #     self.datas[0].close[0],
        #     self.datas[0].volume[0],
        #     )
        # )
        # self.Data_1d = self.data2

        # self.FastSMA = self.params.FastSMA
        # self.SlowSMA = self.params.SlowSMA
        # print(self.datas[0])
        #self.sma = bt.talib.SMA(self.datas[0], timeperiod=30)

        self.Fast_SMA_1d = bt.talib.SMA(self.Data_1h, period = 10)
        self.Slow_SMA_1d = bt.talib.SMA(self.Data_1h, period = 50)

        self.SMA_Crossover_1d = bt.ind.CrossOver(self.Fast_SMA_1d, self.Slow_SMA_1d)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("Compra, %.2f" % order.executed.price)
            elif order.issell():
                self.log("Venta, %.2f" % order.executed.price)

    def prenext(self):
        self.log("Close, %.2f" % self.Data_1h.close[0])

    def next(self):
        self.log("Close, %.2f" % self.Data_1h.close[0])
        self.stoploss()

        if self.position:
            if self.position.price < self.Data_1h.close[0]:
                self.close()
                self.log("Venta, %.2f" % self.Data_1h.close[0])

        if not self.position:
            self.buy()
            self.log("Compra, %.2f" % self.Data_1h.close[0])

    def log(self, txt, dt = None):
        dt = dt or self.Data_1h.datetime.date(0)
        #print("{} {}".format(dt, txt))

    # #def stop(self):
    # #    print(self.position)

    def stoploss(self):
        if self.Data_1h.close < 0.90*float(self.position.price):
            self.close()

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
