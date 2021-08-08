# Clase con todos los datos y funciones relacionadas con la informacion de la moneda, comprar/vender en binance

# Librerias necesarias
import time

import pandas as pd
import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *
import datetime as dt
import math
import os
#import plotly.graph_objects as plot

# Clase con los datos y las funciones
class BinanceClass:

    #CONSTRUCTOR
    #_________________________________________________________________________________________________
    def __init__(self, API_Key, Secret_Key, Crypto, Fiat, Frequency, FechaInicio, FechaFinal):

        self.PublicKey = API_Key
        self.PrivateKey = Secret_Key

        self.Crypto = Crypto
        self.Fiat = Fiat

        self.Frequency = Frequency
        self.Frequency_Available = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
        #####AÑADIR COMPROBACION FRECUENCIA CORRECTA (CON EL DATAFRAME)######

        self.FechaInicio = FechaInicio
        self.FechaFinal = FechaFinal

        #Calcular el numero total de velas a descargar segun el rango de tiempo seleccionado
        FI = dt.datetime(int(FechaInicio[0:4]), int(FechaInicio[5:7]), int(FechaInicio[8:10]), int(FechaInicio[11:13]),
                        int(FechaInicio[14:16]), int(FechaInicio[17:19]))
        FF = FechaFinal
        self.Total_Time = math.floor((FF - FI).total_seconds())
        ######ELIMINAR EL ULTIMO CARACTER UNICAMENTE Y VER QUÉ CARACTER ES (m, h, d, W o M)######

        if "m" in self.Frequency:
            if(len(self.Frequency)) == 2:
                self.CandleSeconds = 60*float(self.Frequency[0])
                self.CandleMinutes = int(self.Frequency[0])
            else:
                self.CandleSeconds = 60*float(self.Frequency[:2])
                self.CandleMinutes = int(self.Frequency[:2])
        elif "h" in self.Frequency:
            if (len(self.Frequency)) == 2:
                self.CandleSeconds = 3600*float(self.Frequency[0])
                self.CandleMinutes = 60*int(self.Frequency[0])
            else:
                self.CandleSeconds = 3600*float(self.Frequency[:2])
                self.CandleMinutes = 60*int(self.Frequency[:2])
        elif "d" in self.Frequency:
            self.CandleSeconds = 86400*float(self.Frequency[0])
            self.CandleMinutes = 24*60*int(self.Frequency[0])
        elif "w" in self.Frequency:
            self.CandleSeconds = 7*86400*float(self.Frequency[0])
            self.CandleMinutes = 7*24*60*int(self.Frequency[0])
        elif "M" in self.Frequency:
            self.CandleSeconds = 30*86400*float(self.Frequency[0])
            self.CandleMinutes = 30*24*60*int(self.Frequency[0])

        self.DataElements = math.floor(self.Total_Time/self.CandleSeconds)

        #self.binance_client = Client(API_Key, Secret_Key)

        self.df = pd.DataFrame(columns = ["time", "open", "high", "low", "close", "volume", "trades"])

        self.RUN = True

        #Valores por defecto
        self.SMA_R = 10
        self.SMA_L = 20

        #Booleanos de señales de compra o venta
        self.Buy_Signal = False
        self.Sell_Signal = False

        #Booleanos de estados de las ordenes
        self.order_status = None
        self.Order = None

        self.market_order = False

        #Informacion IMPORTANTE!!!!!!
        #self.infoCoin = self.binance_client.get_symbol_info(self.CoinPair) #Informacion sobre el par

        #self.min_multiplo_trade = float(self.infoCoin["filters"][2].get("minQty")) #Múltiplo minimo de compra de la moneda
        #self.max_cantidad_trade = float(self.infoCoin["filters"][2].get("maxQty")) #Maxima cantidad de compra de la moneda
        #self.min_notional_trade = float(self.infoCoin["filters"][3].get("minNotional")) #Cantidad mínima a comprar de la moneda

        #Informacion sobre el balance de la cuenta (libre, no en operaciones)
        #self.cantidad_crypto = self.binance_client.get_asset_balance(asset = self.Crypto).get("free")
        #self.cantidad_fiat = self.binance_client.get_asset_balance(asset = self.Fiat).get("free")

        self.cantidad_orden = 1.0
    #________________________________________________________________________________________________________________
    #FIN CONSTRUCTOR

    # Comprobación de una frecuencia correcta
    def check_frequency(self):
        check = False
        for i in range(len(self.Frequency_Available)):
            if self.Frequency == self.Frequency_Available[i]:
                check = True

        if check == True:
            print("La frecuencia seleccionada de {} es correcta. \n".format(self.Frequency))
        else:
            print("La frecuencia seleccionada de {} NO es correcta. \n".format(self.Frequency))

    # Display de las keys de Binance
    def display_keys(self):
        return print("Keys de Binance: \nPublic Key: {} \nPrivate Key: {} \n".format(self.PublicKey, self.PrivateKey))

    # Display del par de monedas seleccionado
    def display_pair(self):
        return print("Par de monedas seleccionado: {}{} \n".format(self.Crypto, self.Fiat))

    # Display de la frecuencia seleccionada
    def display_frequency(self):
        return print("Frecuencia de las velas seleccionada: {}".format(self.Frequency))

    # Display del numero total de elementos
    def display_elements(self):
        return print("Número total de velas: {}".format(self.DataElements))

    # Descargar los datos de las velas correspondientes para el rango de tiempo seleccionado (en un csv)
    def get_initial_candle_data(self):
        data = self.binance_client.get_klines(symbol=self.CoinPair, interval=self.Frequency, limit=self.DataElements)
        self.df = self.data_filter(data)

    #Convertir los datos que proporciona la API a un Dataframe
