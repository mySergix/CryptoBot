import pandas as pd
import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *
import datetime as dt
import math
import os

# Clase con los datos y las funciones de Binance
class Bot_BinanceClass:

    #CONSTRUCTOR
    #_________________________________________________________________________________________________
    def __init__(self, API_Key, Secret_Key, Crypto, Fiat, Frequency, DataElements):

        self.API_Key = API_Key
        self.Secret_Key = Secret_Key

        self.Crypto = Crypto
        self.Fiat = Fiat

        self.Frequency = Frequency
        self.DataElements = DataElements

        self.api_binance = Client(self.API_Key, self.Secret_Key)

        # VARIABLES SOBRE LAS OPERACIONES DE COMPRA Y VENTA
        self.BUY = SIDE_BUY
        self.SELL = SIDE_SELL

        self.PairInfo = self.api_binance.get_symbol_info(self.Crypto+self.Fiat)

        self.CryptoDecimals = int(self.PairInfo["baseAssetPrecision"])
        self.FiatDecimals = int(self.PairInfo["quotePrecision"])

    #________________________________________________________________________________________________________________
    #FIN CONSTRUCTOR

    # Filtrado de datos descargados desde BINANCE
    def Data_filter(Data):
        df = pd.DataFrame(Data)
        df = df.drop([6, 7, 9, 10, 11], axis=1)

        columns = ["time", "open", "high", "low", "close", "volume", "trades"]
        df.columns = columns

        for i in columns:
            df[i] = df[i].astype(float)

        df["start"] = pd.to_datetime(df["time"]*1000000) #Pasar los milisegundos a horario UTC

        return df

    # Actualizar los datos de la ultima vela registrada por Binance
    def Update_data(self):
        new_candle = self.api_binance.get_klines(symbol=self.Crypto+self.Fiat, interval=self.Frequency, limit=1)
        # limit = 1 -> se descarga los datos de la ultima vela
        # interval -> intervalo de esa vela (frecuencia)
        self.df.drop(index = 0, inplace = True) #Quitamos la primera vela de todas y movemos el resto 1 indice hacia abajo
        self.df = self.df.append(self.Data_filter(new_candle), ignore_index=True)
        self.df.index = list(range(self.DataElements))

    def Create_Market_Order(self, OperationSide, Quantity):
        try:
            self.OrderName = self.api_binance.create_order(
                symbol = self.Crypto + self.Fiat,
                side = OperationSide,
                type = "MARKET",
                quantity = Quantity
            )

        except BinanceAPIException as e:
            print(e)

    def Create_Limit_Order(self, OperationSide, Quantity, Price):
        try:
            self.OrderName = self.api_binance.create_order(
                symbol = self.Crypto + self.Fiat,
                side = OperationSide,
                type = "LIMIT",
                timeInForce = TIME_IN_FORCE_GTC,
                quantity = "{:.{}f}".format(Quantity, self.CryptoDecimals),
                price = "{:.{}f}".format(Price, self.CryptoDecimals)
            )

        except BinanceAPIException as e:
            print(e)

    def Create_Test_Order(self, OperationSide, Quantity, Price):
        try:
            self.New_Order = self.api_binance.create_test_order(
                symbol = self.Crypto+self.Fiat,
                side = OperationSide,
                type = "MARKET",
                quantity = "{:.{}f}".format(Quantity, self.CryptoDecimals),
            )

        except BinanceAPIException as e:
            print(e)
