import backtrader as bt
import datetime as dt
import pandas as pd

class Strategy(bt.Strategy):

    def __init__(self):
        self.dataclose = self.datas[0].close

    def prenext(self):
        self.log("",self.dataclose[0])
        
    def next(self):
        self.log("",self.dataclose[0])
        if self.dataclose[0] < self.dataclose[-1]:
            if self.dataclose[-1] < self.dataclose[-2]:
                self.log("BUY CREATE", self.dataclose[0])
                self.buy()

    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print("{} {}".format(dt, txt))
