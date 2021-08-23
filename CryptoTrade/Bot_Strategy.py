import backtrader as bt
import datetime as dt
import pandas as pd

class Strategy(bt.Strategy):

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.sma = bt.indicators.SimpleMovingAverage(period = 8)
        self.stocastic = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period = 14, slowk_period = 3, slowd_period = 3)
        self.bearish = 0
        self.bullish = 0


        self.a_sma = 0.4
        self.a_stoch = 0.3
        self.a_demarck = 0.3

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

        self.stoploss()

        if not self.position:
            if self.buying_function() >= 0.7:
                self.buy()
                self.log("Compra, %.2f" % self.dataclose[0])
        else:
            if self.selling_function() >= 0.7:
                self.sell()
                self.log("Venta, %.2f" % self.dataclose[0])

    def buying_function(self):
        buysignal = self.a_sma*self.sma_buysignal() + self.a_stoch*self.stocastic_buysignal() + self.a_demarck*self.demark9_buysignal()

        return buysignal

    def selling_function(self):
        sellsignal = self.a_sma*self.sma_sellsignal() + self.a_stoch*self.stocastic_sellsignal() + self.a_demarck*self.demark9_sellsignal()

        return sellsignal

    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print("{} {}".format(dt, txt))

    def stop(self):
        print(self.position)

    def stocastic_buysignal(self):
        if self.stocastic.slowk[-1] < self.stocastic.slowd[0]:
            if self.stocastic.slowk[0] > self.stocastic.slowd[0]:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def stocastic_sellsignal(self):
        if self.stocastic.slowk[-1] > self.stocastic.slowd[0]:
            if self.stocastic.slowk[0] < self.stocastic.slowd[0]:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def sma_buysignal(self):
        if self.sma[-1] > self.dataclose[-1]:
            if self.sma[0] < self.dataclose[0]:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def sma_sellsignal(self):
        if self.sma[-1] < self.dataclose[-1]:
            if self.sma[0] > self.dataclose[0]:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def demark9_buysignal(self):
        if self.dataclose[0] < self.dataclose[-4]:
            self.bearish += 1
        elif self.dataclose[0] > self.dataclose[-4]:
            self.bearish = 0

        if self.bearish == 8 or self.bearish == 9:
            return 1.0
        else:
            return 0.0

    def demark9_sellsignal(self):
        if self.dataclose[0] > self.dataclose[-4]:
            self.bullish += 1
        elif self.dataclose[0] < self.dataclose[-4]:
            self.bullish = 0

        if self.bullish == 8 or self.bullish == 9:
            return 1.0
        else:
            return 0.0

    def stoploss(self):
        if self.dataclose[0] < 0.98*float(self.position.price):
            self.close()

    def get_numberofcandles(self, totaltime):

        if self.Frequency[-1] == totaltime[-1]:
            candle_ratio = int(totaltime[0 : len(totaltime)-1 : ])/int(self.Frequency[0 : len(self.Frequency)-1 : ])
        else:
            if self.Frequency[-1] == "m":
                freq_seconds = 60*int(self.Frequency[0 : len(self.Frequency)-1 : ])
            elif self.Frequency[-1] == "h":
                freq_seconds = 3600*int(self.Frequency[0 : len(self.Frequency)-1 : ])
            elif self.Frequency[-1] == "d":
                freq_seconds = 7*3600*int(self.Frequency[0 : len(self.Frequency)-1 : ])

            if totaltime[-1] == "m":
                totaltime_seconds = 60*int(totaltime[0 : len(totaltime)-1 : ])
            elif totaltime[-1] == "h":
                totaltime_seconds = 3600*int(totaltime[0 : len(totaltime)-1 : ])
            elif totaltime[-1] == "d":
                totaltime_seconds = 7*3600*int(totaltime[0 : len(totaltime)-1 : ])

            candle_ratio = totaltime_seconds/freq_seconds

        return candle_ratio
