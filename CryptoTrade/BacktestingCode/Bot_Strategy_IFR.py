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

        # Data Feeds
        self.Data_1h = self.data0
        self.Data_1d = self.data1

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
        self.stopLoss()

        if self.position:
            if self.position.price < self.Data_1h.close[0]:
                self.close()
                self.log("Venta, %.2f" % self.Data_1h.close[0])

        if not self.position:
            self.buy()
            self.log("Compra, %.2f" % self.Data_1h.close[0])

    def log(self, txt, dt = None):
        dt = dt or self.Data_1h.datetime.date(0)
        
    def stopLoss(self):
        if self.Data_1h.close < 0.90*float(self.position.price):
            self.close()