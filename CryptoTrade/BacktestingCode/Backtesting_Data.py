import datetime as dt
from datetime import datetime

# Par de monedas del Backtesting
PAIR = {
    "Base": "BTC",
    "Quote": "USD"
}

STOCK = {
    "Ticker": "TSLA"
}

ASSET = {
    "AssetType": 0 # 0 for Crypto, 1 for Stocks
}

# Fechas de inicio y final (Año-mes-dia) del Backtesting
DATE = {
    "StartDate": "2022-01-01",
    "EndDate": "2022-07-15" #datetime.now()
}

# Frequency available for the candlestick data
Frequency_Available = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]