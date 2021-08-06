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

binance_client = Client(BINANCE["API_Key"], BINANCE["Secret_Key"])

def get_filtered_pairs(SelectedCoin, MinimumVolume):

# SelectedCoin -> Una de las monedas a tradear (ej. USDT, EUR, BNB, etc)
# MinimumVolume -> Volumen mínimo del par a tradear (en euros o dolares)

    BinanceCoins = pd.DataFrame(binance_client.get_all_tickers())
    BinanceCoins = BinanceCoins.drop(columns = "price")
    BinanceCoins["symbol"] = BinanceCoins["symbol"].map(str)

    Filtered_Coins = BinanceCoins[BinanceCoins["symbol"].str.contains(SelectedCoin)]
    Filtered_Coins.dropna(inplace = True)
    Filter = Filtered_Coins.values.copy()
    Filter.resize(len(Filtered_Coins), 1)
    Filtered_Coins = pd.DataFrame(Filter)

    print(Filtered_Coins)
    Final_List = pd.DataFrame(columns=("Pair", "Volume"))

    count = int(0)
    for i in range(len(Filtered_Coins)):
        information = binance_client.get_ticker(symbol=Filtered_Coins[0][i])
        if float(information["quoteVolume"]) >= MinimumVolume:
            Final_List.loc[count] = [Filtered_Coins[0][i], float(information["quoteVolume"])]
            count = count + 1

    return Final_List


get_filtered_pairs("USDT", 100000000)
