import datetime as dt
from datetime import datetime

# Par de monedas del Backtesting
COIN = {
    "Crypto": "BTC",
    "Fiat": "USD"
}

# Fechas de inicio y final (Año, mes, dia, horas, minutos, segundos) del Backtesting
DATE = {
    "StartDate": "2022-01-01",
    "EndDate": "2022-07-15"
    #datetime.now()
}

# Frequency available for the candlestick data
Frequency_Available = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]