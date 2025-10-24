"""
Intraday data fetcher using Polygon.io API
Fetches 30-minute bars for swing trading
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from polygon import RESTClient
import time
import config


class IntradayDataFetcher:
    """Fetches intraday data from Polygon.io"""

    def __init__(self, api_key=None):
        """
        Initialize the intraday data fetcher

        Args:
            api_key: Polygon API key (defaults to config.POLYGON_API_KEY)
        """
        self.api_key = api_key or config.POLYGON_API_KEY
        self.client = RESTClient(self.api_key)

    def fetch_30min_bars(self, symbol, days_back=90):
        """
        Fetch 30-minute bars for a symbol

        Args:
            symbol: Stock symbol (e.g., 'SPY', 'QQQ')
            days_back: Number of days of historical data to fetch

        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        print(f"Fetching {symbol} 30-minute bars from {start_date.date()} to {end_date.date()}...")

        # Collect all bars
        bars = []
        try:
            for agg in self.client.list_aggs(
                ticker=symbol,
                multiplier=30,
                timespan='minute',
                from_=start_date.strftime('%Y-%m-%d'),
                to=end_date.strftime('%Y-%m-%d'),
                limit=50000
            ):
                bars.append({
                    'timestamp': datetime.fromtimestamp(agg.timestamp / 1000),
                    'open': agg.open,
                    'high': agg.high,
                    'low': agg.low,
                    'close': agg.close,
                    'volume': agg.volume
                })

                # Add small delay to respect rate limits
                time.sleep(0.01)

        except Exception as e:
            print(f"Warning: API error - {str(e)}")
            if len(bars) == 0:
                raise

        # Convert to DataFrame
        df = pd.DataFrame(bars)

        if len(df) == 0:
            raise ValueError(f"No data retrieved for {symbol}")

        # Sort by timestamp
        df = df.sort_values('timestamp').reset_index(drop=True)

        # Filter to market hours only (9:30 AM - 4:00 PM ET)
        # Note: Polygon data is in UTC, so we need to convert
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute

        # Keep only regular market hours (assuming data is in ET)
        # Regular hours: 9:30 AM (9.5) to 4:00 PM (16.0)
        df['time_decimal'] = df['hour'] + df['minute'] / 60
        df = df[(df['time_decimal'] >= 9.5) & (df['time_decimal'] <= 16.0)].copy()

        # Drop helper columns
        df = df.drop(['hour', 'minute', 'time_decimal'], axis=1)

        # Set timestamp as index
        df = df.set_index('timestamp')

        print(f"Retrieved {len(df)} 30-minute bars for {symbol}")
        print(f"Date range: {df.index[0]} to {df.index[-1]}")

        return df

    def fetch_multiple_symbols(self, symbols, days_back=90):
        """
        Fetch 30-minute bars for multiple symbols

        Args:
            symbols: List of stock symbols
            days_back: Number of days of historical data

        Returns:
            Dictionary of {symbol: DataFrame}
        """
        data = {}
        for symbol in symbols:
            try:
                data[symbol] = self.fetch_30min_bars(symbol, days_back)
                # Add delay between symbols to avoid rate limits
                time.sleep(1)
            except Exception as e:
                print(f"Error fetching {symbol}: {str(e)}")
                continue

        return data


if __name__ == "__main__":
    # Test the fetcher
    fetcher = IntradayDataFetcher()
    spy_data = fetcher.fetch_30min_bars('SPY', days_back=30)
    print("\nSPY Data Sample:")
    print(spy_data.head(10))
    print("\n" + "="*50)
    print(spy_data.tail(10))
