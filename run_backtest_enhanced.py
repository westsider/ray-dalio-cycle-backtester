"""
Run ENHANCED backtest comparing multiple strategies

Compares:
1. Original strategy (Long Expansion only)
2. Enhanced strategy (Peak + Recovery + stop-loss)
3. Buy & Hold benchmark
"""

from data_fetcher import EconomicDataFetcher
from cycle_classifier import EconomicCycleClassifier
from backtester import Backtester
from backtester_enhanced import BacktesterEnhanced
import matplotlib.pyplot as plt
import pandas as pd


def main():
    """Run enhanced backtest comparison"""

    print("=" * 70)
    print("ENHANCED STRATEGY COMPARISON")
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

    # ========== ORIGINAL STRATEGY ==========
    print("=" * 70)
    print("STRATEGY 1: ORIGINAL (Expansion Only)")
    print("=" * 70)
    print()

    backtester_original = Backtester(
        price_data=spy_data,
        cycle_stages=cycle_stages,
        initial_capital=100000
    )

    results_original = backtester_original.run_strategy(long_stages=['Expansion'])
    print()
    backtester_original.print_summary()

    print()
    print()

    # ========== ENHANCED STRATEGY ==========
    print("=" * 70)
    print("STRATEGY 2: ENHANCED (Peak + Recovery + Stop-Loss)")
    print("=" * 70)
    print()

    backtester_enhanced = BacktesterEnhanced(
        price_data=spy_data,
        cycle_stages=cycle_stages,
        initial_capital=100000
    )

    results_enhanced = backtester_enhanced.run_enhanced_strategy(
        stay_in_peak=True,           # Stay invested during Peak
        peak_stop_loss=0.15,          # 15% stop-loss during Peak
        expansion_stop_loss=0.20,     # 20% stop-loss during Expansion
        include_recovery=True         # Include Recovery stage
    )

    backtester_enhanced.print_summary()

    print()

    # ========== COMPARISON SUMMARY ==========
    print()
    print("=" * 70)
    print("SIDE-BY-SIDE COMPARISON")
    print("=" * 70)
    print()

    print(f"{'Metric':<25} {'Original':>15} {'Enhanced':>15} {'Buy & Hold':>15}")
    print("-" * 70)

    m_orig = backtester_original.metrics
    m_enh = backtester_enhanced.metrics

    print(f"{'Total Return':<25} {m_orig['strategy']['total_return']:>14.2f}% {m_enh['strategy']['total_return']:>14.2f}% {m_orig['buyhold']['total_return']:>14.2f}%")
    print(f"{'Annual Return':<25} {m_orig['strategy']['annual_return']:>14.2f}% {m_enh['strategy']['annual_return']:>14.2f}% {m_orig['buyhold']['annual_return']:>14.2f}%")
    print(f"{'Sharpe Ratio':<25} {m_orig['strategy']['sharpe_ratio']:>15.2f} {m_enh['strategy']['sharpe_ratio']:>15.2f} {m_orig['buyhold']['sharpe_ratio']:>15.2f}")
    print(f"{'Max Drawdown':<25} {m_orig['strategy']['max_drawdown']:>14.2f}% {m_enh['strategy']['max_drawdown']:>14.2f}% {m_orig['buyhold']['max_drawdown']:>14.2f}%")
    print(f"{'Total Trades':<25} {m_orig['trades']['total_trades']:>15.0f} {m_enh['trades']['total_trades']:>15.0f} {0:>15.0f}")
    print(f"{'Win Rate':<25} {m_orig['trades']['win_rate']:>14.1f}% {m_enh['trades']['win_rate']:>14.1f}% {'N/A':>15}")

    print()
    print(f"Enhanced vs Original:")
    print(f"  Return difference: {m_enh['strategy']['total_return'] - m_orig['strategy']['total_return']:+.2f}%")
    print(f"  Sharpe difference: {m_enh['strategy']['sharpe_ratio'] - m_orig['strategy']['sharpe_ratio']:+.2f}")
    print(f"  Drawdown difference: {m_enh['strategy']['max_drawdown'] - m_orig['strategy']['max_drawdown']:+.2f}%")

    print()

    # Show recent trades from enhanced strategy
    print("ENHANCED STRATEGY - RECENT TRADES (Last 10)")
    print("-" * 70)
    recent_trades = backtester_enhanced.get_trades(n=10)
    if recent_trades is not None:
        display_cols = ['entry_date', 'exit_date', 'return_pct', 'days_held', 'exit_reason', 'entry_cycle', 'exit_cycle']
        print(recent_trades[display_cols].to_string(index=False))

    print()

    # ========== VISUALIZATION ==========
    print("Creating comparison chart...")
    print("-" * 70)

    try:
        plot_comparison(results_original, results_enhanced, backtester_original, backtester_enhanced)
        print("✓ Comparison chart saved as 'backtest_enhanced_comparison.png'")
    except Exception as e:
        print(f"Could not create chart: {e}")

    print()
    print("=" * 70)
    print("Enhanced backtest complete!")
    print("=" * 70)


def plot_comparison(results_orig, results_enh, bt_orig, bt_enh):
    """Create comparison visualization"""

    fig, axes = plt.subplots(4, 1, figsize=(16, 12), sharex=True)

    # Plot 1: Equity curves comparison
    ax = axes[0]
    ax.plot(results_orig.index, results_orig['strategy_value'],
            label='Original (Expansion only)', linewidth=2, color='blue', alpha=0.7)
    ax.plot(results_enh.index, results_enh['strategy_value'],
            label='Enhanced (Peak+Recovery+SL)', linewidth=2, color='green', alpha=0.9)
    ax.plot(results_orig.index, results_orig['buyhold_value'],
            label='Buy & Hold', linewidth=2, color='gray', alpha=0.5, linestyle='--')
    ax.set_ylabel('Portfolio Value ($)')
    ax.set_title('Strategy Comparison: Original vs Enhanced vs Buy & Hold')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # Plot 2: Drawdown comparison
    ax = axes[1]

    orig_peak = results_orig['strategy_value'].expanding().max()
    orig_dd = (results_orig['strategy_value'] - orig_peak) / orig_peak * 100

    enh_peak = results_enh['strategy_value'].expanding().max()
    enh_dd = (results_enh['strategy_value'] - enh_peak) / enh_peak * 100

    bh_peak = results_orig['buyhold_value'].expanding().max()
    bh_dd = (results_orig['buyhold_value'] - bh_peak) / bh_peak * 100

    ax.fill_between(results_orig.index, 0, orig_dd,
                    label='Original', alpha=0.4, color='blue')
    ax.fill_between(results_enh.index, 0, enh_dd,
                    label='Enhanced', alpha=0.6, color='green')
    ax.plot(results_orig.index, bh_dd,
            label='Buy & Hold', linewidth=1.5, color='gray', alpha=0.7, linestyle='--')
    ax.set_ylabel('Drawdown (%)')
    ax.set_title('Drawdown Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: Position comparison
    ax = axes[2]
    ax.fill_between(results_orig.index, 0, results_orig['position'],
                    label='Original Position', alpha=0.4, color='blue', step='post')
    ax.fill_between(results_enh.index, 0, results_enh['position'],
                    label='Enhanced Position', alpha=0.6, color='green', step='post')
    ax.set_ylabel('Position')
    ax.set_title('Position Comparison (1 = Long, 0 = Cash)')
    ax.set_ylim(-0.1, 1.1)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 4: Stop-loss levels (Enhanced only)
    ax = axes[3]
    ax.plot(results_enh.index, results_enh['price'],
            label='SPY Price', linewidth=1.5, color='black', alpha=0.7)

    # Plot stop-loss levels when in position
    in_position = results_enh['position'] == 1
    if 'stop_loss_level' in results_enh.columns:
        ax.plot(results_enh.index[in_position],
               results_enh.loc[in_position, 'stop_loss_level'],
               label='Stop-Loss Level', linewidth=1, color='red', alpha=0.5, linestyle=':')

    # Mark stop-loss hits
    sl_hits = results_enh[results_enh['stop_loss_hit'] == True]
    if len(sl_hits) > 0:
        ax.scatter(sl_hits.index, sl_hits['price'],
                  color='red', s=100, marker='x', label='Stop-Loss Hit', zorder=5)

    ax.set_ylabel('SPY Price ($)')
    ax.set_xlabel('Date')
    ax.set_title('Enhanced Strategy: Stop-Loss Tracking')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('backtest_enhanced_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main()
