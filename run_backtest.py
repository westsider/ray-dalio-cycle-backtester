"""
Run backtest of cycle-based trading strategy

Strategy: Long SPY during Expansion, cash otherwise
Benchmark: Buy & Hold SPY
"""

from data_fetcher import EconomicDataFetcher
from cycle_classifier import EconomicCycleClassifier
from backtester import Backtester
import matplotlib.pyplot as plt
import pandas as pd


def main():
    """Run the backtest"""

    print("=" * 70)
    print("RAY DALIO CYCLE STRATEGY BACKTEST")
    print("=" * 70)
    print()

    # Step 1: Fetch data
    print("Step 1: Fetching data...")
    print("-" * 70)

    fetcher = EconomicDataFetcher()
    economic_data = fetcher.fetch_all_indicators(start_date='2000-01-01')
    spy_data = fetcher.get_market_data('SPY', start_date='2000-01-01')

    print()

    # Step 2: Classify cycles
    print("Step 2: Classifying economic cycles...")
    print("-" * 70)

    classifier = EconomicCycleClassifier()
    cycle_stages = classifier.classify(economic_data)

    print()

    # Step 3: Run backtest
    print("Step 3: Running backtest...")
    print("-" * 70)

    backtester = Backtester(
        price_data=spy_data,
        cycle_stages=cycle_stages,
        initial_capital=100000
    )

    # Strategy: Long during Expansion only
    results = backtester.run_strategy(long_stages=['Expansion'])

    print()

    # Step 4: Print results
    backtester.print_summary()

    print()

    # Step 5: Show recent trades
    print("RECENT TRADES (Last 10)")
    print("-" * 70)
    recent_trades = backtester.get_trades(n=10)
    if recent_trades is not None:
        print(recent_trades.to_string(index=False))

    print()

    # Step 6: Create visualization
    print("Step 6: Creating performance charts...")
    print("-" * 70)

    try:
        plot_performance(backtester)
        print("✓ Performance chart saved as 'backtest_results.png'")
    except Exception as e:
        print(f"Could not create chart: {e}")

    print()
    print("=" * 70)
    print("Backtest complete!")
    print("=" * 70)


def plot_performance(backtester):
    """Create performance visualization"""

    df = backtester.results

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    # Plot 1: Equity curves
    ax = axes[0]
    ax.plot(df.index, df['strategy_value'], label='Cycle Strategy', linewidth=2, color='blue')
    ax.plot(df.index, df['buyhold_value'], label='Buy & Hold', linewidth=2, color='gray', alpha=0.7)
    ax.set_ylabel('Portfolio Value ($)')
    ax.set_title('Portfolio Value: Cycle Strategy vs Buy & Hold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # Plot 2: Drawdown
    ax = axes[1]
    strategy_peak = df['strategy_value'].expanding().max()
    strategy_dd = (df['strategy_value'] - strategy_peak) / strategy_peak * 100

    buyhold_peak = df['buyhold_value'].expanding().max()
    buyhold_dd = (df['buyhold_value'] - buyhold_peak) / buyhold_peak * 100

    ax.fill_between(df.index, 0, strategy_dd, label='Cycle Strategy', alpha=0.5, color='blue')
    ax.fill_between(df.index, 0, buyhold_dd, label='Buy & Hold', alpha=0.3, color='gray')
    ax.set_ylabel('Drawdown (%)')
    ax.set_title('Drawdown Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: Position indicator
    ax = axes[2]
    ax.fill_between(df.index, 0, df['position'], label='Long SPY', alpha=0.3, color='green', step='post')
    ax.set_ylabel('Position')
    ax.set_xlabel('Date')
    ax.set_title('Strategy Position (1 = Long SPY, 0 = Cash)')
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('backtest_results.png', dpi=150, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main()
