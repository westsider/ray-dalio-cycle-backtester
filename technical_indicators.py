"""
Technical Indicators for Swing Trading
Includes Bollinger Bands, Keltner Channel, RSI, and other indicators
"""

import pandas as pd
import numpy as np


class TechnicalIndicators:
    """Calculate technical indicators for trading signals"""

    @staticmethod
    def bollinger_bands(df, period=20, std_dev=2.0):
        """
        Calculate Bollinger Bands

        Args:
            df: DataFrame with 'close' column
            period: Moving average period
            std_dev: Number of standard deviations

        Returns:
            DataFrame with bb_middle, bb_upper, bb_lower columns
        """
        result = df.copy()

        # Middle band (SMA)
        result['bb_middle'] = result['close'].rolling(window=period).mean()

        # Standard deviation
        rolling_std = result['close'].rolling(window=period).std()

        # Upper and lower bands
        result['bb_upper'] = result['bb_middle'] + (rolling_std * std_dev)
        result['bb_lower'] = result['bb_middle'] - (rolling_std * std_dev)

        # Bandwidth (for reference)
        result['bb_bandwidth'] = (result['bb_upper'] - result['bb_lower']) / result['bb_middle']

        # %B indicator (where price is within bands)
        result['bb_percent'] = (result['close'] - result['bb_lower']) / (result['bb_upper'] - result['bb_lower'])

        return result

    @staticmethod
    def keltner_channel(df, period=20, atr_mult=2.0):
        """
        Calculate Keltner Channel

        Args:
            df: DataFrame with 'high', 'low', 'close' columns
            period: EMA period
            atr_mult: ATR multiplier for channel width

        Returns:
            DataFrame with kc_middle, kc_upper, kc_lower columns
        """
        result = df.copy()

        # Middle line (EMA of close)
        result['kc_middle'] = result['close'].ewm(span=period, adjust=False).mean()

        # Calculate ATR
        result['tr'] = TechnicalIndicators._true_range(result)
        result['atr'] = result['tr'].ewm(span=period, adjust=False).mean()

        # Upper and lower channels
        result['kc_upper'] = result['kc_middle'] + (result['atr'] * atr_mult)
        result['kc_lower'] = result['kc_middle'] - (result['atr'] * atr_mult)

        # Clean up temporary columns
        result = result.drop(['tr'], axis=1)

        return result

    @staticmethod
    def _true_range(df):
        """Calculate True Range for ATR"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        return pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

    @staticmethod
    def rsi(df, period=14):
        """
        Calculate Relative Strength Index (RSI)

        Args:
            df: DataFrame with 'close' column
            period: RSI period

        Returns:
            DataFrame with 'rsi' column
        """
        result = df.copy()

        # Calculate price changes
        delta = result['close'].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate average gains and losses
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        result['rsi'] = 100 - (100 / (1 + rs))

        return result

    @staticmethod
    def stochastic_rsi(df, period=14, smooth_k=3, smooth_d=3):
        """
        Calculate Stochastic RSI

        Args:
            df: DataFrame with 'close' column
            period: RSI period
            smooth_k: %K smoothing period
            smooth_d: %D smoothing period

        Returns:
            DataFrame with 'stoch_rsi_k' and 'stoch_rsi_d' columns
        """
        result = TechnicalIndicators.rsi(df, period)

        # Calculate Stochastic of RSI
        rsi_min = result['rsi'].rolling(window=period).min()
        rsi_max = result['rsi'].rolling(window=period).max()

        result['stoch_rsi'] = (result['rsi'] - rsi_min) / (rsi_max - rsi_min)

        # Smooth for %K and %D
        result['stoch_rsi_k'] = result['stoch_rsi'].rolling(window=smooth_k).mean()
        result['stoch_rsi_d'] = result['stoch_rsi_k'].rolling(window=smooth_d).mean()

        return result

    @staticmethod
    def macd(df, fast=12, slow=26, signal=9):
        """
        Calculate MACD (Moving Average Convergence Divergence)

        Args:
            df: DataFrame with 'close' column
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period

        Returns:
            DataFrame with 'macd', 'macd_signal', 'macd_hist' columns
        """
        result = df.copy()

        # Calculate MACD line
        ema_fast = result['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = result['close'].ewm(span=slow, adjust=False).mean()
        result['macd'] = ema_fast - ema_slow

        # Signal line
        result['macd_signal'] = result['macd'].ewm(span=signal, adjust=False).mean()

        # Histogram
        result['macd_hist'] = result['macd'] - result['macd_signal']

        return result

    @staticmethod
    def atr(df, period=14):
        """
        Calculate Average True Range (ATR)

        Args:
            df: DataFrame with 'high', 'low', 'close' columns
            period: ATR period

        Returns:
            DataFrame with 'atr' column
        """
        result = df.copy()
        result['tr'] = TechnicalIndicators._true_range(result)
        result['atr'] = result['tr'].ewm(span=period, adjust=False).mean()
        result = result.drop(['tr'], axis=1)
        return result

    @staticmethod
    def squeeze_indicator(df, bb_period=20, bb_std=2.0, kc_period=20, kc_mult=1.5):
        """
        Calculate TTM Squeeze indicator (Bollinger Bands inside Keltner Channel)

        Args:
            df: DataFrame with OHLC data
            bb_period: Bollinger Bands period
            bb_std: Bollinger Bands standard deviation
            kc_period: Keltner Channel period
            kc_mult: Keltner Channel ATR multiplier

        Returns:
            DataFrame with 'squeeze_on' column (True when squeeze is active)
        """
        result = df.copy()

        # Calculate Bollinger Bands
        result = TechnicalIndicators.bollinger_bands(result, bb_period, bb_std)

        # Calculate Keltner Channel
        result = TechnicalIndicators.keltner_channel(result, kc_period, kc_mult)

        # Squeeze is ON when BB is inside KC
        result['squeeze_on'] = (result['bb_lower'] > result['kc_lower']) & \
                               (result['bb_upper'] < result['kc_upper'])

        return result

    @staticmethod
    def add_all_indicators(df, config=None):
        """
        Add all technical indicators to the dataframe

        Args:
            df: DataFrame with OHLC data
            config: Dictionary with indicator parameters (optional)

        Returns:
            DataFrame with all indicators
        """
        if config is None:
            config = {
                'bb_period': 20,
                'bb_std': 2.0,
                'kc_period': 20,
                'kc_mult': 2.0,
                'rsi_period': 14,
                'atr_period': 14
            }

        result = df.copy()

        # Add Bollinger Bands
        result = TechnicalIndicators.bollinger_bands(
            result,
            period=config.get('bb_period', 20),
            std_dev=config.get('bb_std', 2.0)
        )

        # Add Keltner Channel
        result = TechnicalIndicators.keltner_channel(
            result,
            period=config.get('kc_period', 20),
            atr_mult=config.get('kc_mult', 2.0)
        )

        # Add RSI
        result = TechnicalIndicators.rsi(
            result,
            period=config.get('rsi_period', 14)
        )

        # Add ATR
        result = TechnicalIndicators.atr(
            result,
            period=config.get('atr_period', 14)
        )

        # Add MACD
        result = TechnicalIndicators.macd(result)

        # Add Squeeze Indicator
        result = TechnicalIndicators.squeeze_indicator(result)

        return result


if __name__ == "__main__":
    # Test the indicators
    import yfinance as yf

    print("Testing Technical Indicators...")

    # Download some test data
    spy = yf.download('SPY', period='3mo', interval='30m', progress=False)
    spy.columns = [col.lower() for col in spy.columns]

    # Add all indicators
    spy_with_indicators = TechnicalIndicators.add_all_indicators(spy)

    print("\nColumns after adding indicators:")
    print(spy_with_indicators.columns.tolist())

    print("\nLast 5 rows:")
    print(spy_with_indicators[['close', 'bb_upper', 'bb_lower', 'rsi', 'squeeze_on']].tail())
