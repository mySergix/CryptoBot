import pandas as pd
import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *
import datetime as dt
import math
import os
import talib as ta

# Class with Binance data and functions
class Bot_BinanceClass:

    # CONSTRUCTOR
    #_________________________________________________________________________________________________
    def __init__(self, API_Key, Secret_Key, Crypto, Fiat, Frequency, DataElements):

        self.API_Key = API_Key
        self.Secret_Key = Secret_Key

        self.Crypto = Crypto
        self.Fiat = Fiat

        self.Frequency = Frequency
        self.DataElements = DataElements

        self.api_binance = Client(self.API_Key, self.Secret_Key)

        # Variables on purchase and sale operations
        self.BUY = SIDE_BUY
        self.SELL = SIDE_SELL

        self.PairInfo = self.api_binance.get_symbol_info(self.Crypto+self.Fiat)

        self.CryptoDecimals = int(self.PairInfo["baseAssetPrecision"])
        self.FiatDecimals = int(self.PairInfo["quotePrecision"])

        self.FiltersData = self.PairInfo["filters"]

        self.PRICE_FILTER = self.FiltersData[0]
        self.LOT_SIZE = self.FiltersData[2]
        self.MIN_NOTIONAL = self.FiltersData[3]

        self.minPrice = float(self.PRICE_FILTER["minPrice"])
        self.maxPrice = float(self.PRICE_FILTER["maxPrice"])
        self.tickSize = float(self.PRICE_FILTER["tickSize"])

        self.minQty = float(self.LOT_SIZE["minQty"])
        self.maxQty = float(self.LOT_SIZE["maxQty"])
        self.stepSize = float(self.LOT_SIZE["stepSize"])

        self.minNotional = float(self.MIN_NOTIONAL["minNotional"])

        self.PairFees = self.api_binance.get_trade_fee(symbol = self.Crypto+self.Fiat)[0]

        self.makerCommission = float(self.PairFees["makerCommission"])
        self.takerCommission = float(self.PairFees["takerCommission"])

        self.CryptoBalance = self.api_binance.get_asset_balance(self.Crypto)["free"]
        self.FiatBalance = self.api_binance.get_asset_balance(self.Fiat)["free"]

    #________________________________________________________________________________________________________________
    # END CONSTRUCTOR

    # Filtering of data downloaded from Binance
    def Data_filter(Data):
        df = pd.DataFrame(Data)
        df = df.drop([6, 7, 9, 10, 11], axis=1)

        columns = ["time", "open", "high", "low", "close", "volume", "trades"]
        df.columns = columns

        for i in columns:
            df[i] = df[i].astype(float)

        df["start"] = pd.to_datetime(df["time"]*1000000) #Pasar los milisegundos a horario UTC

        return df

    # Update the data of the last candle registered by Binance
    def Update_data(self):
        new_candle = self.api_binance.get_klines(symbol=self.Crypto+self.Fiat, interval=self.Frequency, limit=1)
        # limit = 1 -> the data of the last candle is downloaded
        # interval -> interval of that candle (frquency)
        self.df.drop(index = 0, inplace = True) # The first candle is removed and the rest are moved 1 index down
        self.df = self.df.append(self.Data_filter(new_candle), ignore_index=True)
        self.df.index = list(range(self.DataElements))

    # Update the data on the number of coins of the selected asset
    def Update_account_balance(self):
        self.CryptoBalance = self.api_binance.get_asset_balance(self.Crypto)["free"]
        self.FiatBalance = self.api_binance.get_asset_balance(self.Fiat)["free"]

    # Create a generic market order (usually Market)
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

    # Create a market LIMIT order
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

    # Create a test order to verify that it works
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

    # Notify that an order hast just been filled
    def Notify_order(self):
        Total_price = 0
        Total_quantity = 0
        Average_price = 0
        Comisiones_Totales = 0

        for i in self.New_Order["fills"]: # It is necessary to calculate the mean of the order
            Comisiones_Totales += float(i["commission"])
            Total_quantity += float(i["qty"])
            Total_price += float(i["price"])*float(i["qty"])

        Average_price = Total_price/Total_quantity

        # Register the order data
        self.registro_orden(self.New_Order["type"], self.New_Order["side"], Comisiones_Totales, self.New_Order["commissionAsset"], Average_price, Total_quantity, Total_price)

    # Register all the purchase and sale orders made by the bot
    def Order_register(self, tipo_orden_ejecutada, side, comision, moneda_comision, precio_average, cantidad_crypto, cantidad_fiat):
        f1 = open("OrdersData/Registro_{}_{}_BOT.txt".format(self.Crypto+self.Fiat, self.Frequency), "a+")

        if os.stat("OrdersData/Registro_{}_{}_BOT.txt".format(self.Crypto+self.Fiat, self.Frequency)).st_size == 0:
            f1.write("FECHA \t\t\t TIPO_ORDEN \t ORDEN \t PRECIO \t CANTIDAD_CRYPTO \t CANTIDAD_FIAT \t COMISIÓN \t MONEDA COMISIÓN \n")

        f1.write("{} \t{} \t {} \t\t {} \t\t\t\t {} \t\t\t {} \t\t {} \t\t {} \n".format(str(dt.datetime.now()), tipo_orden_ejecutada, side, str(precio_average),
                                                       str(cantidad_crypto), str(cantidad_fiat), comision, moneda_comision))

        f1.close()

    # Reading the downloaded candlestick data
    def Get_CandleData(self):
        self.CandleData = pd.read_csv("MarketData/{}{}/Freq_{}.csv".format(self.Crypto, self.Fiat, self.Frequency))
        self.DataCandles = len(self.CandleData)

    # Calculation of the SMA Indicator
    def Get_SMA(self, Days):
        self.CandleData["SMA_{}".format(Days)] = ta.SMA(self.CandleData["close"], Days)

    def Get_EMA(self, Days):
        self.CandleData["EMA_{}".format(Days)] = ta.EMA(self.CandleData["close"], Days)

    # Calculation of Stochastic Indicator
    def Get_Stochastic(self, Days, pfast, pslow):
        STO = ta.stochastic(self.CandleData, period = Days, pfast = pfast, pslow = pslow)
        self.CandleData["STO_k_{}_{}_{}".format(Days, pfast, pslow)] = STO.k
        self.CandleData["STO_d_{}_{}_{}".format(Days, pfast, pslow)] = STO.d
