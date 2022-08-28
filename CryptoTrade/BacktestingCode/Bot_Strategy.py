import backtrader as bt
import datetime as dt
import pandas as pd


class Strategy(bt.Strategy):

    params = (
        ('FastSMA', 14), 
        ('SlowSMA', 60),
        ("percents", 100)
    )

    def __init__(self):

        # self.FastSMA = self.params.FastSMA
        # self.SlowSMA = self.params.SlowSMA

        # self.Fast_SMA = bt.indicators.SimpleMovingAverage(self.dataclose, period = self.FastSMA)
        # self.Slow_SMA = bt.indicators.SimpleMovingAverage(self.dataclose, period = self.SlowSMA)

        # Data Feeds
        self.Data_1d = self.data0

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

        self.sma = bt.talib.SMA(self.Data_1d, timeperiod=self.p.FastSMA)
        self.sma = bt.talib.SMA(self.Data_1d, timeperiod=self.p.SlowSMA)

        self.STOCH_1d = bt.talib.STOCH(self.Data_1d.high, self.Data_1d.low, self.Data_1d.close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        self.crossover_Stoch_1d = bt.ind.CrossOver(self.STOCH_1d.slowk, self.STOCH_1d.slowd)  # crossover signal

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("Compra, %.2f" % order.executed.price)
            elif order.issell():
                self.log("Venta, %.2f" % order.executed.price)

    def prenext(self):
        self.log("Close, %.2f" % self.Data_1d.close[0])

    def next(self):
        self.log("Close, %.2f" % self.Data_1d.close[0])
        self.stoploss()

        if self.position:
            if self.crossover_Stoch_1d < 0:
                self.close()
                self.log("Venta, %.2f" % self.Data_1d.close[0])

        if not self.position:
            if self.crossover_Stoch_1d > 0:
                buy_price = self.Data_1d.close * (1 + 0.002)
                cash = self.broker.get_cash()
                print(cash)
                tradeSize = (1.0 * cash) / buy_price
                self.buy(size = tradeSize)
                self.log("Compra, %.2f" % self.Data_1d.close[0])

    def log(self, txt, dt = None):
        dt = dt or self.Data_1d.datetime.date(0)
        #print("{} {}".format(dt, txt))

    # #def stop(self):
    # #    print(self.position)

    def stoploss(self):
        if self.Data_1d.close < 0.90*float(self.position.price):
            self.close()