"""
Configuration for economic indicators and FRED API
"""

# FRED API Key (users should set their own)
# Get your free API key at: https://fred.stlouisfed.org/docs/api/api_key.html
# IMPORTANT: Replace with your own API key before using
FRED_API_KEY = 'ebde2f9652163f7bc1694fa764f8ea44'  # Set to your FRED API key or use environment variable

# Key Economic Indicators (FRED Series IDs)
INDICATORS = {
    # Growth
    'GDP': 'GDP',                           # Gross Domestic Product
    'GDP_GROWTH': 'A191RL1Q225SBEA',       # Real GDP Growth Rate

    # Inflation
    'CPI': 'CPIAUCSL',                      # Consumer Price Index
    'PCE': 'PCEPI',                         # Personal Consumption Expenditures Price Index

    # Employment
    'UNEMPLOYMENT': 'UNRATE',               # Unemployment Rate
    'PAYROLLS': 'PAYEMS',                   # Total Nonfarm Payrolls

    # Credit & Interest Rates
    'FED_FUNDS': 'FEDFUNDS',               # Federal Funds Rate
    'TREASURY_10Y': 'GS10',                # 10-Year Treasury Rate
    'TREASURY_2Y': 'GS2',                  # 2-Year Treasury Rate
    'YIELD_CURVE': None,                   # Will calculate as 10Y - 2Y

    # Other Leading Indicators
    'PMI': 'MANEMP',                       # Manufacturing Employment (proxy for PMI)
    'CONSUMER_SENTIMENT': 'UMCSENT',       # University of Michigan Consumer Sentiment
}

# Date range for historical data
START_DATE = '2000-01-01'
END_DATE = None  # None means today

# Polygon.io API Key for intraday data
# Get your free API key at: https://polygon.io/
POLYGON_API_KEY = 'ozy1q3Aj1rMRu333da1dVb_syktNSXow'

# Swing Trading Configuration
SWING_TRADING = {
    # Symbols to trade
    'SYMBOLS': ['SPY', 'QQQ'],

    # Default timeframe
    'TIMEFRAME': '30min',  # 30-minute bars

    # Technical indicator parameters
    'BOLLINGER_PERIOD': 20,
    'BOLLINGER_STD': 2.0,
    'KELTNER_PERIOD': 20,
    'KELTNER_ATR_MULT': 2.0,
    'RSI_PERIOD': 14,
    'RSI_OVERSOLD': 30,
    'RSI_OVERBOUGHT': 70,

    # Entry/Exit rules
    'ENTRY_RSI_THRESHOLD': 30,  # RSI must be below this to enter
    'EXIT_UPPER_BAND': True,    # Exit when price crosses upper Bollinger Band
    'PROFIT_TARGET_PCT': None,  # Percentage profit target (None = disabled)
    'STOP_LOSS_PCT': 0.02,      # 2% stop loss

    # Position sizing
    'POSITION_SIZE_PCT': 1.0,   # Use 100% of capital per trade

    # Backtesting period
    'BACKTEST_DAYS': 90,        # Days of historical data to backtest
}
