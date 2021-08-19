import pandas as pd
import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *
import datetime as dt
import math
import os
import talib as ta

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

    # Actualizar los datos sobre la cantidad de monedas del activo seleccionado
    def Update_account_balance(self):
        self.CryptoBalance = self.api_binance.get_asset_balance(self.Crypto)["free"]
        self.FiatBalance = self.api_binance.get_asset_balance(self.Fiat)["free"]

    # Crear una orden de mercado genérica (Market normalmente)
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

    # Crear una orden LIMIT en el mercado
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

    # Crear una test order para comprobar que funciona
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

    # Notificar que se acaba de fillear una orden
    def Notify_order(self):
        Total_price = 0
        Total_quantity = 0
        Average_price = 0
        Comisiones_Totales = 0

        for i in self.New_Order["fills"]: #Es necesario calcular el mean de la orden
            Comisiones_Totales += float(i["commission"])
            Total_quantity += float(i["qty"])
            Total_price += float(i["price"])*float(i["qty"])

        Average_price = Total_price/Total_quantity

        # Registro de los datos de la orden
        self.registro_orden(self.New_Order["type"], self.New_Order["side"], Comisiones_Totales, self.New_Order["commissionAsset"], Average_price, Total_quantity, Total_price)

    # Registrar todas las ordenes de compra y venta que realice el Bot
    def Order_register(self, tipo_orden_ejecutada, side, comision, moneda_comision, precio_average, cantidad_crypto, cantidad_fiat):
        f1 = open("OrdersData/Registro_{}_{}_BOT.txt".format(self.Crypto+self.Fiat, self.Frequency), "a+")

        if os.stat("OrdersData/Registro_{}_{}_BOT.txt".format(self.Crypto+self.Fiat, self.Frequency)).st_size == 0:
            f1.write("FECHA \t\t\t\t\t\tORDEN \t PRECIO \t CANTIDAD_CRYPTO \t CANTIDAD_FIAT \t PRECIO_TOTAL \t COMISIÓN \t MONEDA COMISIÓN \n")

        f1.write("{} \t{} \t {} \t\t {} \t\t\t\t {} \t\t\t {} \t\t {} \t\t {} \n".format(str(dt.datetime.now()), tipo_orden_ejecutada, side, str(precio_average),
                                                       str(cantidad_crypto), str(cantidad_fiat), comision, moneda_comision))

        f1.close()

    # Lectura de los datos de las velas descargados
    def Get_CandleData(self):
        self.CandleData = pd.read_csv("MarketData/{}{}/Freq_{}.csv".format(self.Crypto, self.Fiat, self.Frequency))
        self.DataCandles = len(self.CandleData)

    # Calculo Indicador SMA
    def Get_SMA(self, Days):
        self.CandleData["SMA_{}".format(Days)] = ta.SMA(self.CandleData["close"], Days)

    def Get_EMA(self, Days):
        self.CandleData["EMA_{}".format(Days)] = ta.EMA(self.CandleData["close"], Days)
        
    # Calculo Indicador Estocástico
    def Get_Stochastic(self, Days, pfast, pslow):
        STO = ta.stochastic(self.CandleData, period = Days, pfast = pfast, pslow = pslow)
        self.CandleData["STO_k_{}_{}_{}".format(Days, pfast, pslow)] = STO.k
        self.CandleData["STO_d_{}_{}_{}".format(Days, pfast, pslow)] = STO.d
