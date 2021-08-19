import backtrader as bt
import datetime as dt
import pandas as pd

class Strategy(bt.Strategy):

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.sma = bt.indicators.SimpleMovingAverage(period = 17)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("Compra, %.2f" % order.executed.price)
            elif order.issell():
                self.log("Venta, %.2f" % order.executed.price)

    def prenext(self):
        self.log("Close, %.2f" % self.dataclose[0])

    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])

        if not self.position:
            if self.sma < self.dataclose[0]:
                self.buy()
                self.log("Compra, %.2f" % self.dataclose[0])
        else:
            if self.sma > self.dataclose[0]:
                self.sell()
                self.log("Venta, %.2f" % self.dataclose[0])

    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print("{} {}".format(dt, txt))

    def stop(self):
        print(self.position)
