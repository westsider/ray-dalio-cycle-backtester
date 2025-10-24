"""
Swing Trading Backtester
Implements entry/exit logic based on technical indicators
"""

import pandas as pd
import numpy as np
from datetime import datetime
from technical_indicators import TechnicalIndicators


class SwingBacktester:
    """Backtest swing trading strategies on intraday data"""

    def __init__(self, data, initial_capital=100000):
        """
        Initialize the swing backtester

        Args:
            data: DataFrame with OHLC data and timestamp index
            initial_capital: Starting capital
        """
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0  # Number of shares held
        self.entry_price = None
        self.trades = []
        self.equity_curve = []
        self.results = None
        self.metrics = {}

    def add_indicators(self, config):
        """Add technical indicators to the data"""
        self.data = TechnicalIndicators.add_all_indicators(self.data, config)
        return self

    def run_strategy(self,
                     entry_condition='bb_rsi',
                     exit_condition='bb_upper',
                     rsi_threshold=30,
                     rsi_exit_threshold=70,
                     profit_target_pct=None,
                     stop_loss_pct=0.02,
                     economic_expansion=None):
        """
        Run the swing trading strategy

        Args:
            entry_condition: Entry signal type ('bb_rsi', 'squeeze', 'kc_rsi')
            exit_condition: Exit signal type ('bb_upper', 'profit_target', 'rsi')
            rsi_threshold: RSI level for oversold entry
            rsi_exit_threshold: RSI level for overbought exit
            profit_target_pct: Profit target percentage (None = disabled)
            stop_loss_pct: Stop loss percentage
            economic_expansion: Series indicating economic expansion (True/False)
                               If provided, only trade during expansion

        Returns:
            DataFrame with results
        """
        results = []
        self.position = 0
        self.capital = self.initial_capital
        self.entry_price = None
        self.trades = []
        entry_time = None
        highest_price_since_entry = None

        for i, (timestamp, row) in enumerate(self.data.iterrows()):
            # Skip if indicators not ready
            if pd.isna(row.get('rsi')) or pd.isna(row.get('bb_lower')):
                results.append({
                    'timestamp': timestamp,
                    'close': row['close'],
                    'position': 0,
                    'equity': self.capital,
                    'signal': None
                })
                continue

            # Check if we should be trading (economic expansion filter)
            can_trade = True
            if economic_expansion is not None:
                # Match timestamp to daily economic data
                date = pd.Timestamp(timestamp.date())

                # Try exact match first
                if date in economic_expansion.index:
                    can_trade = economic_expansion.loc[date]
                else:
                    # Find nearest previous date
                    try:
                        # Use asof to get the most recent value
                        can_trade = economic_expansion.asof(date)
                        # If asof returns NaN, default to False (don't trade)
                        if pd.isna(can_trade):
                            can_trade = False
                    except:
                        # If any error, default to True (trade)
                        can_trade = True

            current_price = row['close']
            signal = None

            # If no position, look for entry signals
            if self.position == 0 and can_trade:
                entry_signal = self._check_entry(row, entry_condition, rsi_threshold)

                if entry_signal:
                    # Enter long position
                    shares = int(self.capital / current_price)
                    if shares > 0:
                        self.position = shares
                        self.entry_price = current_price
                        entry_time = timestamp
                        highest_price_since_entry = current_price
                        cost = shares * current_price
                        self.capital -= cost
                        signal = 'BUY'

            # If we have a position, check exit conditions
            elif self.position > 0:
                # Update highest price since entry
                if current_price > highest_price_since_entry:
                    highest_price_since_entry = current_price

                exit_signal = False
                exit_reason = None

                # Stop loss check
                if self.entry_price is not None:
                    loss_pct = (current_price - self.entry_price) / self.entry_price
                    if loss_pct <= -stop_loss_pct:
                        exit_signal = True
                        exit_reason = 'STOP_LOSS'

                # Profit target check
                if not exit_signal and profit_target_pct is not None:
                    gain_pct = (current_price - self.entry_price) / self.entry_price
                    if gain_pct >= profit_target_pct:
                        exit_signal = True
                        exit_reason = 'PROFIT_TARGET'

                # Technical exit check
                if not exit_signal:
                    tech_exit = self._check_exit(row, exit_condition, rsi_exit_threshold)
                    if tech_exit:
                        exit_signal = True
                        exit_reason = 'TECHNICAL'

                # Economic regime exit (contraction)
                if not exit_signal and not can_trade:
                    exit_signal = True
                    exit_reason = 'ECONOMIC'

                # Exit if signal
                if exit_signal:
                    proceeds = self.position * current_price
                    self.capital += proceeds
                    returns = (current_price - self.entry_price) / self.entry_price

                    # Record trade
                    self.trades.append({
                        'entry_time': entry_time,
                        'exit_time': timestamp,
                        'entry_price': self.entry_price,
                        'exit_price': current_price,
                        'shares': self.position,
                        'return_pct': returns * 100,
                        'profit': (current_price - self.entry_price) * self.position,
                        'exit_reason': exit_reason
                    })

                    self.position = 0
                    self.entry_price = None
                    highest_price_since_entry = None
                    signal = f'SELL_{exit_reason}'

            # Calculate current equity
            if self.position > 0:
                equity = self.capital + (self.position * current_price)
            else:
                equity = self.capital

            results.append({
                'timestamp': timestamp,
                'close': current_price,
                'position': self.position,
                'equity': equity,
                'signal': signal,
                'rsi': row.get('rsi'),
                'bb_upper': row.get('bb_upper'),
                'bb_lower': row.get('bb_lower'),
                'bb_middle': row.get('bb_middle')
            })

        self.results = pd.DataFrame(results).set_index('timestamp')
        self._calculate_metrics()

        return self.results

    def _check_entry(self, row, condition, rsi_threshold):
        """Check if entry conditions are met"""
        if condition == 'bb_rsi':
            # Entry: Price below lower BB AND RSI oversold
            return (row['close'] < row['bb_lower']) and (row['rsi'] < rsi_threshold)

        elif condition == 'kc_rsi':
            # Entry: Price below lower Keltner AND RSI oversold
            return (row['close'] < row['kc_lower']) and (row['rsi'] < rsi_threshold)

        elif condition == 'squeeze':
            # Entry: Squeeze is on AND RSI oversold AND price below BB lower
            return (row.get('squeeze_on', False)) and \
                   (row['rsi'] < rsi_threshold) and \
                   (row['close'] < row['bb_lower'])

        return False

    def _check_exit(self, row, condition, rsi_threshold):
        """Check if exit conditions are met"""
        if condition == 'bb_upper':
            # Exit: Price crosses above upper BB
            return row['close'] > row['bb_upper']

        elif condition == 'bb_middle':
            # Exit: Price crosses above middle BB
            return row['close'] > row['bb_middle']

        elif condition == 'rsi':
            # Exit: RSI overbought
            return row['rsi'] > rsi_threshold

        elif condition == 'kc_upper':
            # Exit: Price crosses above upper Keltner
            return row['close'] > row['kc_upper']

        return False

    def _calculate_metrics(self):
        """Calculate performance metrics"""
        if self.results is None or len(self.results) == 0:
            return

        # Convert trades to DataFrame
        trades_df = pd.DataFrame(self.trades) if len(self.trades) > 0 else pd.DataFrame()

        # Calculate equity curve metrics
        total_return = (self.results['equity'].iloc[-1] - self.initial_capital) / self.initial_capital * 100

        # Annualized return
        days = (self.results.index[-1] - self.results.index[0]).days
        years = days / 365.25
        annual_return = (((self.results['equity'].iloc[-1] / self.initial_capital) ** (1/years)) - 1) * 100 if years > 0 else 0

        # Volatility (annualized)
        returns = self.results['equity'].pct_change().dropna()
        # Assuming 252 trading days * 13 bars per day = 3276 bars per year
        bars_per_year = 3276
        volatility = returns.std() * np.sqrt(bars_per_year) * 100

        # Sharpe ratio (assuming 2% risk-free rate)
        risk_free_rate = 0.02
        sharpe = (annual_return - risk_free_rate * 100) / volatility if volatility > 0 else 0

        # Max drawdown
        rolling_max = self.results['equity'].expanding().max()
        drawdown = (self.results['equity'] - rolling_max) / rolling_max * 100
        max_drawdown = drawdown.min()

        # Trade statistics
        if len(trades_df) > 0:
            win_trades = trades_df[trades_df['return_pct'] > 0]
            win_rate = len(win_trades) / len(trades_df) * 100
            avg_win = win_trades['return_pct'].mean() if len(win_trades) > 0 else 0
            avg_loss = trades_df[trades_df['return_pct'] <= 0]['return_pct'].mean() if len(trades_df[trades_df['return_pct'] <= 0]) > 0 else 0
            avg_return = trades_df['return_pct'].mean()
            best_trade = trades_df['return_pct'].max()
            worst_trade = trades_df['return_pct'].min()
        else:
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            avg_return = 0
            best_trade = 0
            worst_trade = 0

        self.metrics = {
            'total_return': total_return,
            'annual_return': annual_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_drawdown,
            'final_value': self.results['equity'].iloc[-1],
            'total_trades': len(trades_df),
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'avg_return': avg_return,
            'best_trade': best_trade,
            'worst_trade': worst_trade
        }

    def get_trades_df(self):
        """Return trades as a formatted DataFrame"""
        if len(self.trades) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(self.trades)
        return df


if __name__ == "__main__":
    # Test the backtester
    from intraday_fetcher import IntradayDataFetcher
    import config

    print("Testing Swing Backtester...")

    # Fetch data
    fetcher = IntradayDataFetcher()
    spy_data = fetcher.fetch_30min_bars('SPY', days_back=30)

    # Run backtest
    backtester = SwingBacktester(spy_data, initial_capital=100000)

    # Add indicators
    indicator_config = {
        'bb_period': config.SWING_TRADING['BOLLINGER_PERIOD'],
        'bb_std': config.SWING_TRADING['BOLLINGER_STD'],
        'kc_period': config.SWING_TRADING['KELTNER_PERIOD'],
        'kc_mult': config.SWING_TRADING['KELTNER_ATR_MULT'],
        'rsi_period': config.SWING_TRADING['RSI_PERIOD'],
        'atr_period': 14
    }
    backtester.add_indicators(indicator_config)

    # Run strategy
    results = backtester.run_strategy(
        entry_condition='bb_rsi',
        exit_condition='bb_upper',
        rsi_threshold=config.SWING_TRADING['ENTRY_RSI_THRESHOLD'],
        stop_loss_pct=config.SWING_TRADING['STOP_LOSS_PCT'],
        profit_target_pct=config.SWING_TRADING['PROFIT_TARGET_PCT']
    )

    print("\nPerformance Metrics:")
    for key, value in backtester.metrics.items():
        print(f"{key}: {value:.2f}")

    print(f"\nTrades executed: {len(backtester.trades)}")
    if len(backtester.trades) > 0:
        print("\nRecent trades:")
        print(backtester.get_trades_df().tail())
