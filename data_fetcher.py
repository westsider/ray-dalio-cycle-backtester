"""
Data fetcher for macroeconomic indicators from FRED and market data from Yahoo Finance
"""

import pandas as pd
import numpy as np
from fredapi import Fred
import yfinance as yf
from datetime import datetime
import os
from config import FRED_API_KEY, INDICATORS, START_DATE, END_DATE


class EconomicDataFetcher:
    """Fetches and processes macroeconomic data from FRED"""

    def __init__(self, api_key=None):
        """
        Initialize the data fetcher

        Args:
            api_key: FRED API key (if None, tries to get from environment or config)
        """
        if api_key is None:
            api_key = os.environ.get('FRED_API_KEY', FRED_API_KEY)

        if api_key is None:
            raise ValueError(
                "FRED API key required. Get one at https://fred.stlouisfed.org/docs/api/api_key.html\n"
                "Set it via environment variable FRED_API_KEY or in config.py"
            )

        self.fred = Fred(api_key=api_key)
        self.data = None

    def fetch_all_indicators(self, start_date=START_DATE, end_date=END_DATE):
        """
        Fetch all economic indicators from FRED

        Args:
            start_date: Start date for data (YYYY-MM-DD)
            end_date: End date for data (YYYY-MM-DD or None for today)

        Returns:
            DataFrame with all indicators
        """
        print("Fetching economic data from FRED...")

        data_dict = {}

        for name, series_id in INDICATORS.items():
            if series_id is None:  # Skip calculated fields
                continue

            try:
                print(f"  Fetching {name} ({series_id})...")
                series = self.fred.get_series(series_id, observation_start=start_date)
                data_dict[name] = series
            except Exception as e:
                print(f"  Warning: Could not fetch {name}: {e}")

        # Combine all series into a single DataFrame
        df = pd.DataFrame(data_dict)

        # Ensure index is DatetimeIndex (FRED series should have datetime index)
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        # Calculate derived indicators
        if 'TREASURY_10Y' in df.columns and 'TREASURY_2Y' in df.columns:
            df['YIELD_CURVE'] = df['TREASURY_10Y'] - df['TREASURY_2Y']

        # Calculate inflation rate (year-over-year CPI change)
        if 'CPI' in df.columns:
            df['INFLATION_RATE'] = df['CPI'].pct_change(periods=12) * 100

        # Calculate unemployment rate change
        if 'UNEMPLOYMENT' in df.columns:
            df['UNEMPLOYMENT_CHANGE'] = df['UNEMPLOYMENT'].diff()

        # Forward fill to handle different data frequencies
        df = df.resample('D').ffill()

        self.data = df
        print(f"✓ Fetched data from {df.index[0].date()} to {df.index[-1].date()}")

        return df

    def get_market_data(self, ticker='SPY', start_date=START_DATE, end_date=END_DATE):
        """
        Fetch market data from Yahoo Finance

        Args:
            ticker: Stock ticker symbol
            start_date: Start date
            end_date: End date

        Returns:
            DataFrame with market data
        """
        print(f"Fetching {ticker} data from Yahoo Finance...")

        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
            print(f"✓ Fetched {ticker} data from {data.index[0].date()} to {data.index[-1].date()}")
            return data
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None
