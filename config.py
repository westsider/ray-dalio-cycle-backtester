"""
Configuration for economic indicators and FRED API
"""

# FRED API Key (users should set their own)
# Get your free API key at: https://fred.stlouisfed.org/docs/api/api_key.html
# IMPORTANT: Replace with your own API key before using
FRED_API_KEY = 'your_api_key_here'  # Set to your FRED API key or use environment variable

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
