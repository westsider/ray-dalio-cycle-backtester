"""
Streamlit Web App for Ray Dalio Economic Cycle Backtester

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

from data_fetcher import EconomicDataFetcher
from cycle_classifier import EconomicCycleClassifier
from backtester import Backtester
from backtester_enhanced import BacktesterEnhanced


# Page config
st.set_page_config(
    page_title="Ray Dalio Cycle Backtester",
    page_icon="📊",
    layout="wide"
)


# Cache data fetching to avoid re-downloading every time
# Cache key includes start_date so changing date fetches new data
@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def fetch_data(start_date):
    """Fetch economic and market data"""
    fetcher = EconomicDataFetcher()
    economic_data = fetcher.fetch_all_indicators(start_date=start_date)
    spy_data = fetcher.get_market_data('SPY', start_date=start_date)
    return economic_data, spy_data


@st.cache_data(ttl=3600, show_spinner=False)
def classify_cycles(economic_data, start_date):
    """Classify economic cycles - start_date added to cache key"""
    classifier = EconomicCycleClassifier()
    cycle_stages = classifier.classify(economic_data)
    return cycle_stages, classifier


def get_cycle_explanation(stage, economic_data):
    """Generate explanation for why we're in a particular cycle stage"""

    # Get latest values - look back up to 30 days to find most recent valid data
    def get_latest_valid(series_name):
        """Get most recent non-NaN value from a series"""
        if series_name not in economic_data.columns:
            return None
        # Look at last 30 rows to find most recent valid value
        recent_values = economic_data[series_name].iloc[-30:]
        valid_values = recent_values.dropna()
        if len(valid_values) > 0:
            return valid_values.iloc[-1]
        return None

    gdp_growth = get_latest_valid('GDP_GROWTH')
    unemployment = get_latest_valid('UNEMPLOYMENT')
    inflation = get_latest_valid('INFLATION_RATE')
    yield_curve = get_latest_valid('YIELD_CURVE')

    # Calculate trends (last 90 days)
    if len(economic_data) > 90:
        recent = economic_data.iloc[-90:]
        unemployment_trend = recent['UNEMPLOYMENT'].iloc[-1] - recent['UNEMPLOYMENT'].iloc[0] if 'UNEMPLOYMENT' in recent else None
    else:
        unemployment_trend = None

    if stage == "Expansion":
        explanation = "🟢 **The economy is in Expansion phase.** "
        reasons = []

        if gdp_growth is not None and not pd.isna(gdp_growth) and gdp_growth > 0:
            reasons.append(f"GDP growth is positive at {gdp_growth:.1f}%")

        if unemployment is not None and not pd.isna(unemployment):
            if unemployment < 5:
                reasons.append(f"unemployment is low at {unemployment:.1f}%")
            elif unemployment_trend is not None and not pd.isna(unemployment_trend) and unemployment_trend < 0:
                reasons.append(f"unemployment is falling (currently {unemployment:.1f}%)")
            else:
                reasons.append(f"unemployment is moderate at {unemployment:.1f}%")

        if inflation is not None and not pd.isna(inflation):
            if inflation < 3:
                reasons.append(f"inflation is moderate at {inflation:.1f}%")
            elif inflation < 5:
                reasons.append(f"inflation is manageable at {inflation:.1f}%")

        if yield_curve is not None and not pd.isna(yield_curve) and yield_curve > 0:
            reasons.append(f"the yield curve is positive ({yield_curve:.2f}% spread)")

        if reasons:
            explanation += "Key indicators: " + ", ".join(reasons) + ". "
        else:
            explanation += "Economic indicators show positive conditions. "

        explanation += "This is typically a good environment for stocks, with economic activity growing steadily."

    elif stage == "Peak":
        explanation = "🟡 **The economy is at Peak phase.** "
        reasons = []

        if gdp_growth is not None and not pd.isna(gdp_growth):
            if gdp_growth > 0:
                reasons.append(f"GDP growth is slowing but still positive ({gdp_growth:.1f}%)")
            else:
                reasons.append(f"GDP growth has turned negative ({gdp_growth:.1f}%)")

        if inflation is not None and not pd.isna(inflation) and inflation > 3.5:
            reasons.append(f"inflation is elevated at {inflation:.1f}%")

        if yield_curve is not None and not pd.isna(yield_curve) and yield_curve < 0:
            reasons.append(f"the yield curve is inverted ({yield_curve:.2f}% - recession warning)")

        if unemployment is not None and not pd.isna(unemployment) and unemployment < 4:
            reasons.append(f"unemployment is very low at {unemployment:.1f}% (tight labor market)")

        if reasons:
            explanation += "Warning signs: " + ", ".join(reasons) + ". "
        else:
            explanation += "Economic indicators show late-cycle conditions. "

        explanation += "This phase often precedes an economic contraction. The strategy uses tighter stop-losses to protect gains."

    elif stage == "Contraction":
        explanation = "🔴 **The economy is in Contraction phase.** "
        reasons = []

        if gdp_growth is not None and not pd.isna(gdp_growth) and gdp_growth < 0:
            reasons.append(f"GDP growth is negative at {gdp_growth:.1f}%")

        if unemployment is not None and not pd.isna(unemployment):
            if unemployment_trend is not None and not pd.isna(unemployment_trend) and unemployment_trend > 0.3:
                reasons.append(f"unemployment is rising rapidly (now {unemployment:.1f}%)")
            elif unemployment > 6:
                reasons.append(f"unemployment is elevated at {unemployment:.1f}%")

        if yield_curve is not None and not pd.isna(yield_curve) and yield_curve < -0.2:
            reasons.append("the yield curve remains deeply inverted")

        if reasons:
            explanation += "Recession indicators: " + ", ".join(reasons) + ". "
        else:
            explanation += "Economic indicators show contractionary conditions. "

        explanation += "This is a risk-off environment. The strategy moves to cash to preserve capital during downturns."

    elif stage == "Recovery":
        explanation = "🔵 **The economy is in Recovery phase.** "
        reasons = []

        if gdp_growth is not None and not pd.isna(gdp_growth):
            if 0 <= gdp_growth < 2:
                reasons.append(f"GDP growth is turning positive ({gdp_growth:.1f}%)")
            elif gdp_growth >= 2:
                reasons.append(f"GDP growth is accelerating ({gdp_growth:.1f}%)")

        if unemployment is not None and not pd.isna(unemployment):
            if unemployment > 6:
                if unemployment_trend is not None and not pd.isna(unemployment_trend) and unemployment_trend < -0.1:
                    reasons.append(f"unemployment is high ({unemployment:.1f}%) but starting to fall")
                else:
                    reasons.append(f"unemployment remains elevated at {unemployment:.1f}%")

        if yield_curve is not None and not pd.isna(yield_curve) and yield_curve > 0:
            reasons.append("the yield curve has normalized")

        if reasons:
            explanation += "Early recovery signs: " + ", ".join(reasons) + ". "
        else:
            explanation += "Economic indicators show early recovery. "

        explanation += "This is often the best time to invest, as the economy rebounds from recession lows."

    else:
        explanation = f"Current stage: {stage}. Economic conditions are being analyzed."

    return explanation


def main():
    """Main Streamlit app"""

    # Title and description
    st.title("📊 Ray Dalio Economic Cycle Backtester")
    st.markdown("""
    Test trading strategies based on economic cycle detection (Expansion, Peak, Contraction, Recovery).
    This tool fetches real-time economic data from FRED and market data from Yahoo Finance.
    """)

    # Sidebar for settings
    st.sidebar.header("⚙️ Settings")

    # Date range presets
    st.sidebar.subheader("Date Range")
    date_preset = st.sidebar.radio(
        "Quick Select:",
        ["1 Year", "2 Years", "5 Years", "10 Years", "Maximum (2000+)", "Custom"],
        index=4  # Default to Maximum
    )

    # Calculate start date based on preset
    if date_preset == "1 Year":
        start_date = datetime.now().replace(year=datetime.now().year - 1)
    elif date_preset == "2 Years":
        start_date = datetime.now().replace(year=datetime.now().year - 2)
    elif date_preset == "5 Years":
        start_date = datetime.now().replace(year=datetime.now().year - 5)
    elif date_preset == "10 Years":
        start_date = datetime.now().replace(year=datetime.now().year - 10)
    elif date_preset == "Maximum (2000+)":
        start_date = datetime(2000, 1, 1)
    else:  # Custom
        start_date = st.sidebar.date_input(
            "Custom Start Date",
            value=datetime(2000, 1, 1),
            min_value=datetime(1990, 1, 1),
            max_value=datetime.now()
        )
        start_date = datetime.combine(start_date, datetime.min.time())

    # Initial capital
    initial_capital = st.sidebar.number_input(
        "Initial Capital ($)",
        min_value=1000,
        max_value=10000000,
        value=100000,
        step=10000
    )

    # Strategy selection
    st.sidebar.subheader("Strategy Selection")
    strategy_type = st.sidebar.radio(
        "Choose Strategy:",
        ["Original (Expansion Only)", "Enhanced (Peak + Recovery + Stop-Loss)", "Compare Both"]
    )

    # Enhanced strategy parameters
    if strategy_type in ["Enhanced (Peak + Recovery + Stop-Loss)", "Compare Both"]:
        st.sidebar.subheader("Enhanced Strategy Parameters")

        stay_in_peak = st.sidebar.checkbox("Stay invested during Peak", value=True)
        include_recovery = st.sidebar.checkbox("Include Recovery stage", value=True)

        expansion_stop = st.sidebar.slider(
            "Expansion Stop-Loss (%)",
            min_value=5,
            max_value=30,
            value=20,
            step=1
        ) / 100

        peak_stop = st.sidebar.slider(
            "Peak Stop-Loss (%)",
            min_value=5,
            max_value=25,
            value=15,
            step=1
        ) / 100

    # Run button
    run_backtest = st.sidebar.button("🚀 Run Backtest", type="primary")

    # Main content
    if run_backtest:
        with st.spinner("Fetching data from FRED and Yahoo Finance..."):
            try:
                # Fetch data
                start_date_str = start_date.strftime('%Y-%m-%d')
                economic_data, spy_data = fetch_data(start_date_str)

                # Classify cycles (pass start_date_str for cache key)
                cycle_stages, classifier = classify_cycles(economic_data, start_date_str)

                st.success("✓ Data loaded successfully!")

                # Display current cycle stage
                current_stage = classifier.get_current_stage()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Cycle Stage", current_stage)
                with col2:
                    start_str = cycle_stages.index[0].strftime('%Y-%m-%d')
                    end_str = cycle_stages.index[-1].strftime('%Y-%m-%d')
                    st.metric("Data Period", f"{start_str} to {end_str}")
                with col3:
                    latest_price = float(spy_data['Close'].iloc[-1])
                    st.metric("Latest SPY Price", f"${latest_price:.2f}")

                # Add explanation of current stage
                st.markdown("---")
                st.subheader(f"Why {current_stage}?")

                explanation = get_cycle_explanation(current_stage, economic_data)
                st.info(explanation)

                st.divider()

                # Run backtests based on selection
                if strategy_type == "Original (Expansion Only)":
                    run_original_strategy(spy_data, cycle_stages, initial_capital, economic_data)

                elif strategy_type == "Enhanced (Peak + Recovery + Stop-Loss)":
                    run_enhanced_strategy(
                        spy_data, cycle_stages, initial_capital,
                        stay_in_peak, peak_stop, expansion_stop, include_recovery,
                        economic_data
                    )

                else:  # Compare Both
                    run_comparison(
                        spy_data, cycle_stages, initial_capital,
                        stay_in_peak, peak_stop, expansion_stop, include_recovery,
                        economic_data
                    )

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure your FRED API key is set in config.py")

    else:
        # Show instructions when not running
        st.info("👈 Configure settings in the sidebar and click 'Run Backtest' to start")

        st.subheader("📖 How to Use")
        st.markdown("""
        1. **Set parameters** in the sidebar (start date, capital, strategy type)
        2. **Click 'Run Backtest'** to fetch data and run analysis
        3. **View results** including performance metrics, charts, and trade history
        4. **Experiment** with different settings to optimize your strategy
        """)

        st.subheader("📊 Economic Cycle Stages")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **🟢 Expansion**
            - Positive GDP growth
            - Low/falling unemployment
            - Moderate inflation

            **🟡 Peak**
            - Growth slowing
            - Inflation rising
            - Yield curve inverting
            """)

        with col2:
            st.markdown("""
            **🔴 Contraction**
            - Negative GDP growth
            - Rising unemployment
            - Credit tightening

            **🔵 Recovery**
            - GDP turning positive
            - High unemployment but falling
            - Accommodative policy
            """)


def run_original_strategy(spy_data, cycle_stages, initial_capital, economic_data):
    """Run original strategy"""
    st.header("Original Strategy: Long Expansion Only")

    with st.spinner("Running backtest..."):
        backtester = Backtester(spy_data, cycle_stages, initial_capital)
        results = backtester.run_strategy(long_stages=['Expansion'])

        # Display metrics
        display_metrics(backtester, "Original Strategy")

        # Display charts
        display_charts(results, backtester, "Original Strategy")

        # Display trades
        display_trades(backtester)


def run_enhanced_strategy(spy_data, cycle_stages, initial_capital,
                         stay_in_peak, peak_stop, expansion_stop, include_recovery,
                         economic_data):
    """Run enhanced strategy"""
    st.header("Enhanced Strategy: Peak + Recovery + Stop-Loss")

    with st.spinner("Running enhanced backtest..."):
        backtester = BacktesterEnhanced(spy_data, cycle_stages, initial_capital)
        results = backtester.run_enhanced_strategy(
            stay_in_peak=stay_in_peak,
            peak_stop_loss=peak_stop,
            expansion_stop_loss=expansion_stop,
            include_recovery=include_recovery
        )

        # Display metrics
        display_metrics(backtester, "Enhanced Strategy")

        # Display charts
        display_charts(results, backtester, "Enhanced Strategy")

        # Display trades
        display_trades(backtester)


def run_comparison(spy_data, cycle_stages, initial_capital,
                  stay_in_peak, peak_stop, expansion_stop, include_recovery,
                  economic_data):
    """Run comparison of both strategies"""
    st.header("Strategy Comparison: Original vs Enhanced")

    with st.spinner("Running both backtests..."):
        # Original
        bt_orig = Backtester(spy_data, cycle_stages, initial_capital)
        results_orig = bt_orig.run_strategy(long_stages=['Expansion'])

        # Enhanced
        bt_enh = BacktesterEnhanced(spy_data, cycle_stages, initial_capital)
        results_enh = bt_enh.run_enhanced_strategy(
            stay_in_peak=stay_in_peak,
            peak_stop_loss=peak_stop,
            expansion_stop_loss=expansion_stop,
            include_recovery=include_recovery
        )

        # Comparison table
        st.subheader("📊 Performance Comparison")

        comparison_df = pd.DataFrame({
            'Metric': [
                'Total Return',
                'Annual Return',
                'Volatility',
                'Sharpe Ratio',
                'Max Drawdown',
                'Final Value',
                'Total Trades',
                'Win Rate'
            ],
            'Original': [
                f"{bt_orig.metrics['strategy']['total_return']:.2f}%",
                f"{bt_orig.metrics['strategy']['annual_return']:.2f}%",
                f"{bt_orig.metrics['strategy']['volatility']:.2f}%",
                f"{bt_orig.metrics['strategy']['sharpe_ratio']:.2f}",
                f"{bt_orig.metrics['strategy']['max_drawdown']:.2f}%",
                f"${bt_orig.metrics['strategy']['final_value']:,.0f}",
                f"{bt_orig.metrics['trades']['total_trades']:.0f}",
                f"{bt_orig.metrics['trades']['win_rate']:.1f}%"
            ],
            'Enhanced': [
                f"{bt_enh.metrics['strategy']['total_return']:.2f}%",
                f"{bt_enh.metrics['strategy']['annual_return']:.2f}%",
                f"{bt_enh.metrics['strategy']['volatility']:.2f}%",
                f"{bt_enh.metrics['strategy']['sharpe_ratio']:.2f}",
                f"{bt_enh.metrics['strategy']['max_drawdown']:.2f}%",
                f"${bt_enh.metrics['strategy']['final_value']:,.0f}",
                f"{bt_enh.metrics['trades']['total_trades']:.0f}",
                f"{bt_enh.metrics['trades']['win_rate']:.1f}%"
            ],
            'Buy & Hold': [
                f"{bt_orig.metrics['buyhold']['total_return']:.2f}%",
                f"{bt_orig.metrics['buyhold']['annual_return']:.2f}%",
                f"{bt_orig.metrics['buyhold']['volatility']:.2f}%",
                f"{bt_orig.metrics['buyhold']['sharpe_ratio']:.2f}",
                f"{bt_orig.metrics['buyhold']['max_drawdown']:.2f}%",
                f"${bt_orig.metrics['buyhold']['final_value']:,.0f}",
                "0",
                "N/A"
            ]
        })

        st.dataframe(comparison_df, use_container_width=True)

        # Winner announcement
        best_return = max(
            bt_orig.metrics['strategy']['total_return'],
            bt_enh.metrics['strategy']['total_return'],
            bt_orig.metrics['buyhold']['total_return']
        )

        if bt_enh.metrics['strategy']['total_return'] == best_return:
            st.success("🏆 Enhanced Strategy is the winner!")
        elif bt_orig.metrics['strategy']['total_return'] == best_return:
            st.success("🏆 Original Strategy is the winner!")
        else:
            st.info("🏆 Buy & Hold is the winner!")

        # Comparison chart
        display_comparison_chart(results_orig, results_enh)


def display_metrics(backtester, title):
    """Display performance metrics"""
    st.subheader("📈 Performance Metrics")

    m = backtester.metrics

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Return",
            f"{m['strategy']['total_return']:.2f}%",
            delta=f"{m['strategy']['total_return'] - m['buyhold']['total_return']:.2f}% vs B&H"
        )
        st.metric("Annual Return", f"{m['strategy']['annual_return']:.2f}%")

    with col2:
        st.metric("Sharpe Ratio", f"{m['strategy']['sharpe_ratio']:.2f}")
        st.metric("Volatility", f"{m['strategy']['volatility']:.2f}%")

    with col3:
        st.metric("Max Drawdown", f"{m['strategy']['max_drawdown']:.2f}%")
        st.metric("Final Value", f"${m['strategy']['final_value']:,.0f}")

    with col4:
        st.metric("Total Trades", f"{m['trades']['total_trades']:.0f}")
        st.metric("Win Rate", f"{m['trades']['win_rate']:.1f}%")


def display_charts(results, backtester, title):
    """Display interactive charts using Plotly"""
    st.subheader("📊 Performance Charts")

    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Portfolio Value', 'Drawdown', 'Position'),
        vertical_spacing=0.08,
        row_heights=[0.4, 0.3, 0.3]
    )

    # Plot 1: Equity curves
    fig.add_trace(
        go.Scatter(x=results.index, y=results['strategy_value'],
                  name='Strategy', line=dict(color='blue', width=2)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=results.index, y=results['buyhold_value'],
                  name='Buy & Hold', line=dict(color='gray', width=2, dash='dash')),
        row=1, col=1
    )

    # Plot 2: Drawdown
    strategy_peak = results['strategy_value'].expanding().max()
    strategy_dd = (results['strategy_value'] - strategy_peak) / strategy_peak * 100

    buyhold_peak = results['buyhold_value'].expanding().max()
    buyhold_dd = (results['buyhold_value'] - buyhold_peak) / buyhold_peak * 100

    fig.add_trace(
        go.Scatter(x=results.index, y=strategy_dd,
                  name='Strategy DD', fill='tozeroy', line=dict(color='blue')),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=results.index, y=buyhold_dd,
                  name='B&H DD', fill='tozeroy', line=dict(color='gray'), opacity=0.5),
        row=2, col=1
    )

    # Plot 3: Position
    fig.add_trace(
        go.Scatter(x=results.index, y=results['position'],
                  name='Position (1=Long, 0=Cash)', fill='tozeroy', line=dict(color='green')),
        row=3, col=1
    )

    # Update layout
    fig.update_yaxes(title_text="Value ($)", row=1, col=1)
    fig.update_yaxes(title_text="Drawdown (%)", row=2, col=1)
    fig.update_yaxes(
        title_text="Position (1=Long SPY, 0=Cash)",
        tickvals=[0, 1],
        ticktext=['Cash<br>(Out of Market)', 'Long SPY<br>(In Market)'],
        row=3, col=1
    )
    fig.update_xaxes(title_text="Date", row=3, col=1)

    # Add range slider and selector buttons
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=2, label="2Y", step="year", stepmode="backward"),
                dict(count=5, label="5Y", step="year", stepmode="backward"),
                dict(step="all", label="All")
            ]),
            bgcolor="lightgray",
            activecolor="darkgray"
        ),
        rangeslider=dict(visible=True),
        row=3, col=1
    )

    fig.update_layout(height=900, showlegend=True, hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)


def display_comparison_chart(results_orig, results_enh):
    """Display comparison chart"""
    st.subheader("📊 Comparison Charts")

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Portfolio Value Comparison', 'Position Comparison'),
        vertical_spacing=0.12
    )

    # Equity curves
    fig.add_trace(
        go.Scatter(x=results_orig.index, y=results_orig['strategy_value'],
                  name='Original', line=dict(color='blue', width=2)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=results_enh.index, y=results_enh['strategy_value'],
                  name='Enhanced', line=dict(color='green', width=2)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=results_orig.index, y=results_orig['buyhold_value'],
                  name='Buy & Hold', line=dict(color='gray', width=2, dash='dash')),
        row=1, col=1
    )

    # Positions
    fig.add_trace(
        go.Scatter(x=results_orig.index, y=results_orig['position'],
                  name='Original (1=Long, 0=Cash)', fill='tozeroy', line=dict(color='blue'), opacity=0.5),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=results_enh.index, y=results_enh['position'],
                  name='Enhanced (1=Long, 0=Cash)', fill='tozeroy', line=dict(color='green'), opacity=0.7),
        row=2, col=1
    )

    fig.update_yaxes(title_text="Value ($)", row=1, col=1)
    fig.update_yaxes(
        title_text="Position (1=Long SPY, 0=Cash)",
        tickvals=[0, 1],
        ticktext=['Cash<br>(Out of Market)', 'Long SPY<br>(In Market)'],
        row=2, col=1
    )
    fig.update_xaxes(title_text="Date", row=2, col=1)

    # Add range slider and selector buttons
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=2, label="2Y", step="year", stepmode="backward"),
                dict(count=5, label="5Y", step="year", stepmode="backward"),
                dict(step="all", label="All")
            ]),
            bgcolor="lightgray",
            activecolor="darkgray"
        ),
        rangeslider=dict(visible=True),
        row=2, col=1
    )

    fig.update_layout(height=700, showlegend=True, hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)


def display_trades(backtester):
    """Display trade history"""
    st.subheader("📝 Trade History")

    trades = backtester.trades

    if trades is not None and len(trades) > 0:
        # Format dates
        display_trades = trades.copy()
        display_trades['entry_date'] = pd.to_datetime(display_trades['entry_date']).dt.date
        display_trades['exit_date'] = pd.to_datetime(display_trades['exit_date']).dt.date

        # Color code returns
        def color_returns(val):
            if isinstance(val, (int, float)):
                color = 'green' if val > 0 else 'red'
                return f'color: {color}'
            return ''

        styled_trades = display_trades.style.map(
            color_returns,
            subset=['return_pct']
        )

        st.dataframe(styled_trades, use_container_width=True)

        # Download button
        csv = trades.to_csv(index=False)
        st.download_button(
            label="📥 Download Trade History as CSV",
            data=csv,
            file_name=f"trades_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No trades executed")


if __name__ == "__main__":
    main()
