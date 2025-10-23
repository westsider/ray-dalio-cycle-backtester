"""
Example usage of the Economic Cycle Classifier

This script demonstrates how to:
1. Fetch economic data from FRED
2. Classify cycle stages
3. Display results
"""

from data_fetcher import EconomicDataFetcher
from cycle_classifier import EconomicCycleClassifier, CycleStage
import matplotlib.pyplot as plt
import pandas as pd


def main():
    """Run the economic cycle classification example"""

    print("=" * 60)
    print("Ray Dalio Economic Cycle Classifier")
    print("=" * 60)
    print()

    # Step 1: Fetch economic data
    print("Step 1: Fetching economic data from FRED")
    print("-" * 60)

    # Initialize fetcher (make sure to set your FRED API key)
    fetcher = EconomicDataFetcher()

    # Fetch all indicators
    economic_data = fetcher.fetch_all_indicators(start_date='2000-01-01')

    print()

    # Step 2: Classify cycle stages
    print("Step 2: Classifying economic cycle stages")
    print("-" * 60)

    classifier = EconomicCycleClassifier()
    cycle_stages = classifier.classify(economic_data)

    print()

    # Step 3: Display current stage
    print("Step 3: Current Economic State")
    print("-" * 60)
    current_stage = classifier.get_current_stage()
    print(f"Current Cycle Stage: {current_stage}")

    print()

    # Step 4: Show recent transitions
    print("Step 4: Recent Cycle Transitions (last 10)")
    print("-" * 60)
    transitions = classifier.get_cycle_changes()
    if transitions is not None and len(transitions) > 0:
        recent = transitions.tail(10)
        print(recent.to_string())
    else:
        print("No transitions found")

    print()

    # Step 5: Create a simple visualization
    print("Step 5: Creating visualization...")
    print("-" * 60)

    try:
        # Fetch SPY data
        spy_data = fetcher.get_market_data('SPY', start_date='2000-01-01')
        plot_cycles(economic_data, cycle_stages, spy_data)
        print("✓ Visualization saved as 'economic_cycles.png'")
    except Exception as e:
        print(f"Could not create visualization: {e}")

    print()
    print("=" * 60)
    print("Done! Next step: Use these cycle predictions for backtesting")
    print("=" * 60)


def plot_cycles(data, stages, spy_data=None):
    """Create a visualization of economic cycles"""

    fig, axes = plt.subplots(5, 1, figsize=(14, 14), sharex=True)

    # Convert stages to numeric for plotting
    stage_mapping = {
        CycleStage.CONTRACTION.value: 0,
        CycleStage.RECOVERY.value: 1,
        CycleStage.EXPANSION.value: 2,
        CycleStage.PEAK.value: 3,
    }
    stages_numeric = stages.map(stage_mapping)

    # Plot 1: S&P 500 (SPY) Price
    ax = axes[0]
    if spy_data is not None and 'Close' in spy_data.columns:
        ax.plot(spy_data.index, spy_data['Close'], label='S&P 500 (SPY)', linewidth=1.5, color='blue')
        ax.set_ylabel('SPY Price ($)')
        ax.set_title('S&P 500 Price and Economic Cycle Classification')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)

    # Plot 2: Cycle Stages
    ax = axes[1]
    # Use a line plot with markers instead of filled area
    ax.plot(stages.index, stages_numeric, label='Cycle Stage', linewidth=2, color='darkblue', alpha=0.7)
    ax.scatter(stages.index[::30], stages_numeric[::30], s=20, color='darkblue', alpha=0.5, zorder=5)
    ax.set_ylabel('Cycle Stage')
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['Contraction', 'Recovery', 'Expansion', 'Peak'])
    ax.set_title('Economic Cycle Stages')
    ax.set_ylim(-0.5, 3.5)
    ax.grid(True, alpha=0.3)

    # Plot 3: GDP Growth
    ax = axes[2]
    if 'GDP_GROWTH' in data.columns:
        ax.plot(data.index, data['GDP_GROWTH'], label='GDP Growth', linewidth=1)
        ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax.set_ylabel('GDP Growth (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)

    # Plot 4: Unemployment
    ax = axes[3]
    if 'UNEMPLOYMENT' in data.columns:
        ax.plot(data.index, data['UNEMPLOYMENT'], label='Unemployment Rate', linewidth=1, color='orange')
        ax.set_ylabel('Unemployment (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)

    # Plot 5: Yield Curve
    ax = axes[4]
    if 'YIELD_CURVE' in data.columns:
        ax.plot(data.index, data['YIELD_CURVE'], label='Yield Curve (10Y-2Y)', linewidth=1, color='green')
        ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax.set_ylabel('Yield Spread (%)')
        ax.set_xlabel('Date')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('economic_cycles.png', dpi=150, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main()
