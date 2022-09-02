# This class sets the data for the backtesting.

# Python libraries
import datetime as dt
from datetime import datetime

# Cryptocurrency pair (must be in Yahoo Finance list).
PAIR = {
    "Base": "BTC",
    "Quote": "USD"
}

# Stocks (must be in Yahoo Finance list).
STOCK = {
    "Ticker": "TSLA"
}

# Defining asset type: 0 for cryptocurrency, 1 for stocks.
ASSET = {
    "AssetType": 0
}

# Start and end dates (year-month-day) for the backtesting (datetime.now() for current date).
DATE = {
    "StartDate": "2022-01-01",
    "EndDate": "2022-07-15"
}

# Frequencies available for the candlestick data (must be in Yahoo Finance list).
FREQUENCIES = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
