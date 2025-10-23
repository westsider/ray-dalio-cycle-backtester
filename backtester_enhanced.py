"""
Enhanced backtesting engine with improved entry/exit timing

Improvements over basic backtester:
1. Peak handling - Stay invested during Peak with stop-loss protection
2. Stop-loss functionality - Protect against sudden drawdowns
3. Recovery inclusion - Enter during Recovery phase
4. Better exit logic - Only exit on confirmed Contraction
"""

import pandas as pd
import numpy as np
from datetime import datetime


class BacktesterEnhanced:
    """
    Enhanced backtesting engine with improved Peak handling and stop-loss
    """

    def __init__(self, price_data, cycle_stages, initial_capital=100000):
        """
        Initialize enhanced backtester

        Args:
            price_data: DataFrame with market prices (must have 'Close' column)
            cycle_stages: Series with cycle stage classifications
            initial_capital: Starting capital in dollars
        """
        self.price_data = price_data
        self.cycle_stages = cycle_stages
        self.initial_capital = initial_capital

        # Align data
        self.data = self._align_data()

        # Results storage
        self.results = None
        self.trades = None
        self.metrics = None

    def _align_data(self):
        """Align price data and cycle stages by date"""
        df = pd.DataFrame()
        df['price'] = self.price_data['Close']
        df['cycle'] = self.cycle_stages

        # Forward fill cycle stages to match daily prices
        df['cycle'] = df['cycle'].ffill()

        # Drop any rows with missing data
        df = df.dropna()

        return df

    def run_enhanced_strategy(self,
                             stay_in_peak=True,
                             peak_stop_loss=0.15,
                             expansion_stop_loss=0.20,
                             include_recovery=True):
        """
        Run enhanced cycle-based strategy

        Strategy rules:
        1. Long during Expansion (with trailing stop-loss)
        2. Long during Peak if stay_in_peak=True (with tighter stop-loss)
        3. Long during Recovery if include_recovery=True
        4. Cash during Contraction
        5. Exit immediately if stop-loss hit

        Args:
            stay_in_peak: Stay invested during Peak stage (default True)
            peak_stop_loss: Stop-loss % during Peak (default 15%)
            expansion_stop_loss: Stop-loss % during Expansion (default 20%)
            include_recovery: Include Recovery stage as long (default True)

        Returns:
            DataFrame with daily portfolio values
        """
        print(f"Running ENHANCED backtest...")
        print(f"Strategy Rules:")
        print(f"  - Long during Expansion (with {expansion_stop_loss*100:.0f}% stop-loss)")
        print(f"  - Stay in Peak: {stay_in_peak} (with {peak_stop_loss*100:.0f}% stop-loss)")
        print(f"  - Include Recovery: {include_recovery}")
        print(f"  - Cash during Contraction")
        print(f"  Initial capital: ${self.initial_capital:,.0f}")
        print(f"  Period: {self.data.index[0].date()} to {self.data.index[-1].date()}")
        print()

        # Initialize
        df = self.data.copy()
        df['position'] = 0.0
        df['entry_price'] = np.nan
        df['peak_since_entry'] = np.nan
        df['stop_loss_level'] = np.nan
        df['stop_loss_hit'] = False

        # Track state
        current_position = 0
        entry_price = None
        peak_since_entry = None

        for i in range(len(df)):
            idx = df.index[i]
            cycle = df.loc[idx, 'cycle']
            price = df.loc[idx, 'price']

            # Determine if we should be long based on cycle
            should_be_long = False
            current_stop_pct = expansion_stop_loss

            if cycle == 'Expansion':
                should_be_long = True
                current_stop_pct = expansion_stop_loss
            elif cycle == 'Peak' and stay_in_peak:
                should_be_long = True
                current_stop_pct = peak_stop_loss
            elif cycle == 'Recovery' and include_recovery:
                should_be_long = True
                current_stop_pct = expansion_stop_loss
            elif cycle == 'Contraction':
                should_be_long = False

            # Check stop-loss if we're currently long
            stop_loss_triggered = False
            if current_position == 1 and entry_price is not None and peak_since_entry is not None:
                # Update peak
                if price > peak_since_entry:
                    peak_since_entry = price

                # Check trailing stop from peak
                stop_loss_level = peak_since_entry * (1 - current_stop_pct)
                df.loc[idx, 'stop_loss_level'] = stop_loss_level

                if price <= stop_loss_level:
                    stop_loss_triggered = True
                    df.loc[idx, 'stop_loss_hit'] = True

            # Position logic
            if current_position == 0:
                # Not in position - check if we should enter
                if should_be_long and not stop_loss_triggered:
                    current_position = 1
                    entry_price = price
                    peak_since_entry = price
                    df.loc[idx, 'entry_price'] = entry_price
            else:
                # In position - check if we should exit
                if not should_be_long or stop_loss_triggered:
                    current_position = 0
                    entry_price = None
                    peak_since_entry = None
                else:
                    # Stay in position
                    df.loc[idx, 'entry_price'] = entry_price
                    df.loc[idx, 'peak_since_entry'] = peak_since_entry

            df.loc[idx, 'position'] = current_position

        # Calculate returns
        df['market_return'] = df['price'].pct_change()
        df['strategy_return'] = df['position'].shift(1) * df['market_return']
        df['strategy_return'] = df['strategy_return'].fillna(0)

        # Calculate cumulative portfolio value
        df['strategy_value'] = self.initial_capital * (1 + df['strategy_return']).cumprod()
        df['buyhold_value'] = self.initial_capital * (1 + df['market_return']).cumprod()

        # Fill initial NaN
        df['strategy_value'] = df['strategy_value'].fillna(self.initial_capital)
        df['buyhold_value'] = df['buyhold_value'].fillna(self.initial_capital)

        # Track position changes
        df['position_change'] = df['position'].diff()

        self.results = df
        self._extract_trades()
        self._calculate_metrics()

        # Print stop-loss stats
        stop_loss_count = df['stop_loss_hit'].sum()
        print(f"Stop-loss triggered: {stop_loss_count} times")
        print()

        return df

    def _extract_trades(self):
        """Extract trade entry and exit points"""
        if self.results is None:
            return

        df = self.results
        trades = []

        # Find entries (position change from 0 to 1)
        entries = df[df['position_change'] == 1].copy()

        # Find exits (position change from 1 to 0)
        exits = df[df['position_change'] == -1].copy()

        # Match entries with exits
        for i, entry in entries.iterrows():
            # Find next exit after this entry
            future_exits = exits[exits.index > i]

            if len(future_exits) > 0:
                exit_date = future_exits.index[0]
                exit_row = df.loc[exit_date]

                entry_price = entry['price']
                exit_price = exit_row['price']
                pnl = (exit_price - entry_price) / entry_price * 100

                # Check if exit was due to stop-loss
                exit_reason = 'Stop-loss' if exit_row['stop_loss_hit'] else 'Cycle change'

                trades.append({
                    'entry_date': i,
                    'exit_date': exit_date,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'return_pct': pnl,
                    'days_held': (exit_date - i).days,
                    'exit_reason': exit_reason,
                    'entry_cycle': entry['cycle'],
                    'exit_cycle': exit_row['cycle']
                })

        self.trades = pd.DataFrame(trades)

    def _calculate_metrics(self):
        """Calculate performance metrics"""
        if self.results is None:
            return

        df = self.results

        # Total returns
        strategy_total_return = (df['strategy_value'].iloc[-1] / self.initial_capital - 1) * 100
        buyhold_total_return = (df['buyhold_value'].iloc[-1] / self.initial_capital - 1) * 100

        # Annualized returns
        years = (df.index[-1] - df.index[0]).days / 365.25
        strategy_annual_return = ((df['strategy_value'].iloc[-1] / self.initial_capital) ** (1/years) - 1) * 100
        buyhold_annual_return = ((df['buyhold_value'].iloc[-1] / self.initial_capital) ** (1/years) - 1) * 100

        # Volatility (annualized)
        strategy_volatility = df['strategy_return'].std() * np.sqrt(252) * 100
        buyhold_volatility = df['market_return'].std() * np.sqrt(252) * 100

        # Sharpe ratio (assuming 0% risk-free rate)
        strategy_sharpe = strategy_annual_return / strategy_volatility if strategy_volatility > 0 else 0
        buyhold_sharpe = buyhold_annual_return / buyhold_volatility if buyhold_volatility > 0 else 0

        # Maximum drawdown
        strategy_dd = self._calculate_max_drawdown(df['strategy_value'])
        buyhold_dd = self._calculate_max_drawdown(df['buyhold_value'])

        # Win rate and trade stats
        if self.trades is not None and len(self.trades) > 0:
            winning_trades = len(self.trades[self.trades['return_pct'] > 0])
            win_rate = (winning_trades / len(self.trades)) * 100
            avg_win = self.trades[self.trades['return_pct'] > 0]['return_pct'].mean()
            avg_loss = self.trades[self.trades['return_pct'] < 0]['return_pct'].mean()

            # Stop-loss exits
            stop_loss_exits = len(self.trades[self.trades['exit_reason'] == 'Stop-loss'])
            stop_loss_pct = (stop_loss_exits / len(self.trades)) * 100 if len(self.trades) > 0 else 0
        else:
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            stop_loss_exits = 0
            stop_loss_pct = 0

        self.metrics = {
            'strategy': {
                'total_return': strategy_total_return,
                'annual_return': strategy_annual_return,
                'volatility': strategy_volatility,
                'sharpe_ratio': strategy_sharpe,
                'max_drawdown': strategy_dd,
                'final_value': df['strategy_value'].iloc[-1],
            },
            'buyhold': {
                'total_return': buyhold_total_return,
                'annual_return': buyhold_annual_return,
                'volatility': buyhold_volatility,
                'sharpe_ratio': buyhold_sharpe,
                'max_drawdown': buyhold_dd,
                'final_value': df['buyhold_value'].iloc[-1],
            },
            'trades': {
                'total_trades': len(self.trades) if self.trades is not None else 0,
                'win_rate': win_rate,
                'avg_win': avg_win if not np.isnan(avg_win) else 0,
                'avg_loss': avg_loss if not np.isnan(avg_loss) else 0,
                'stop_loss_exits': stop_loss_exits,
                'stop_loss_exit_pct': stop_loss_pct,
            }
        }

    def _calculate_max_drawdown(self, equity_curve):
        """Calculate maximum drawdown from equity curve"""
        running_max = equity_curve.expanding().max()
        drawdown = (equity_curve - running_max) / running_max * 100
        return drawdown.min()

    def print_summary(self):
        """Print backtest summary"""
        if self.metrics is None:
            print("No backtest results available. Run run_enhanced_strategy() first.")
            return

        print("=" * 70)
        print("ENHANCED BACKTEST RESULTS SUMMARY")
        print("=" * 70)
        print()

        print(f"{'Metric':<30} {'Strategy':>15} {'Buy & Hold':>15} {'Difference':>10}")
        print("-" * 70)

        # Returns
        print(f"{'Total Return':<30} {self.metrics['strategy']['total_return']:>14.2f}% {self.metrics['buyhold']['total_return']:>14.2f}% {self.metrics['strategy']['total_return'] - self.metrics['buyhold']['total_return']:>9.2f}%")
        print(f"{'Annual Return':<30} {self.metrics['strategy']['annual_return']:>14.2f}% {self.metrics['buyhold']['annual_return']:>14.2f}% {self.metrics['strategy']['annual_return'] - self.metrics['buyhold']['annual_return']:>9.2f}%")

        # Risk metrics
        print(f"{'Volatility (Annual)':<30} {self.metrics['strategy']['volatility']:>14.2f}% {self.metrics['buyhold']['volatility']:>14.2f}% {self.metrics['strategy']['volatility'] - self.metrics['buyhold']['volatility']:>9.2f}%")
        print(f"{'Sharpe Ratio':<30} {self.metrics['strategy']['sharpe_ratio']:>15.2f} {self.metrics['buyhold']['sharpe_ratio']:>15.2f} {self.metrics['strategy']['sharpe_ratio'] - self.metrics['buyhold']['sharpe_ratio']:>10.2f}")
        print(f"{'Max Drawdown':<30} {self.metrics['strategy']['max_drawdown']:>14.2f}% {self.metrics['buyhold']['max_drawdown']:>14.2f}% {self.metrics['strategy']['max_drawdown'] - self.metrics['buyhold']['max_drawdown']:>9.2f}%")

        # Final values
        print(f"{'Final Portfolio Value':<30} ${self.metrics['strategy']['final_value']:>14,.0f} ${self.metrics['buyhold']['final_value']:>14,.0f}")

        print()
        print("TRADING STATISTICS")
        print("-" * 70)
        print(f"Total Trades: {self.metrics['trades']['total_trades']}")
        print(f"Win Rate: {self.metrics['trades']['win_rate']:.1f}%")
        print(f"Average Win: {self.metrics['trades']['avg_win']:.2f}%")
        print(f"Average Loss: {self.metrics['trades']['avg_loss']:.2f}%")
        print(f"Stop-loss Exits: {self.metrics['trades']['stop_loss_exits']} ({self.metrics['trades']['stop_loss_exit_pct']:.1f}%)")

        print()
        print("=" * 70)

    def get_trades(self, n=10):
        """Get last n trades"""
        if self.trades is None or len(self.trades) == 0:
            print("No trades recorded")
            return None

        return self.trades.tail(n)
