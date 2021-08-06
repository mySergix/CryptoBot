import datetime as dt
from datetime import datetime
from binance.client import Client
import pandas as pd
import numpy as np
#from binance.exceptions import BinanceAPIException
#from binance.enums import *

#Claves publica y privada de Binance
BINANCE = {
    "API_Key": "4iecH8ptMaIqN4pP2PfM1YTaapkq4TNbjly1Tsn1ZBzecGXwp0SJ0cAEmKGUVV00",
    "Secret_Key": "zjglVcrpkvWpZzuEH0DJiUuzh8LpSMuQgKanSIBV5pjHtkZSFFhEyM8xsGxre4H9"
}

#Pares seleccionados
binance_client = Client(BINANCE["API_Key"], BINANCE["Secret_Key"])

BinanceCoins = pd.DataFrame(binance_client.get_all_tickers())

BinanceCoins = BinanceCoins.drop(columns = "price")

#print(BinanceCoins)

BinanceCoins["symbol"] = BinanceCoins["symbol"].map(str)

#print(type(BinanceCoins["symbol"]))

#for i in BinanceCoins:
BNB_Coins = BinanceCoins[BinanceCoins["symbol"].str.contains("BNB")]

#print(BNB_Coins)
BNB_Coins.dropna(inplace = True)

Length = len(BNB_Coins)
print(Length)
BNB = BNB_Coins.values.copy()
BNB.resize(Length, 1)
#BNB_Coins.resize(Length, 1)
#print(BNB)

BNB_Coins = pd.DataFrame(BNB)
print(BNB_Coins)
#print(BinanceCoins["symbol" == "ETHBTC"])
