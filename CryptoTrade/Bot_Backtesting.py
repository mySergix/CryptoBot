import backtrader as bt
import Bot_Strategy
import datetime as dt

class BacktestingClass:

    #CONSTRUCTOR
    #_________________________________________________________________________________________________
    def __init__(self, Crypto, Fiat, Frequency, StartDate, EndDate):
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
        elif self.Frequency[-1] == "h":
            self.TimeFrame = bt.TimeFrame.Minutes
            self.Compresion = 60*int(self.Frequency[0 : len(self.Frequency)-1 : ])
        elif self.Frequency[-1] == "d":
            self.TimeFrame = bt.TimeFrame.Days
            self.Compresion = 1

        self.Data = bt.feeds.GenericCSVData(
             name = self.Crypto,
             dataname = ("MarketData/{}{}/Freq_{}.csv".format(self.Crypto, self.Fiat, self.Frequency)),
             timeframe = self.TimeFrame,
             compression = self.Compresion,
             fromdate = self.StartDate,
             todate = self.EndDate,
             nullvalue = 0.0,
             datetime = 8,
             high = 3,
             low = 4,
             open = 2,
             close = 5
        )

        self.BacktestingCore.adddata(self.Data)

        #________________________________________________________________________________________________________________
        #FIN CONSTRUCTOR

    # Setear la Cantidad Inicial a invertir
    def SetInitialMoney(self, Money):
        self.BacktestingCore.broker.setcash(Money)

    # Mostrar por pantalla el valor actual del protfolio
    def PrintCurrentMoney(self):
        print("Current Portfolio Value: %.2f" % self.BacktestingCore.broker.getvalue())

    # Añadir las comisiones de Binance
    def AddComissions(self, Comisiones):
        self.BacktestingCore.broker.setcommission(commission = Comisiones)

    # Añadir el porcentaje de dinero en cada trade
    def AddSizers(self, Sizer):
        self.BacktestingCore.addsizer(Sizer)

    # Añadir una estrategia al backtesting
    def AddStrategy(self, Strat):
        self.BacktestingCore.addstrategy(Strat)

    # Correr la estrategia implementada
    def RunStrategy(self):
        self.BacktestingCore.run()

    # Plotear los resultados obtenidos
    def PlotBacktestingResults(self):
        self.BacktestingCore.plot()
