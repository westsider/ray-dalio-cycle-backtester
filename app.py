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
from intraday_fetcher import IntradayDataFetcher
from swing_backtester import SwingBacktester
import config


# Page config
st.set_page_config(
    page_title="Ray Dalio Cycle Backtester",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apple-inspired custom CSS
st.markdown("""
<style>
    /* Import fonts closer to SF Pro */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&family=System-ui&display=swap');

    /* Global styles - SF Pro fallback stack */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Inter', sans-serif;
        color: #1d1d1f !important;
    }

    /* Override Streamlit's default white text */
    body, p, div, span, label, a, li, td, th {
        color: #1d1d1f !important;
    }

    /* Main background */
    .main {
        background-color: #f5f5f7 !important;
    }

    .stApp {
        background-color: #f5f5f7 !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #f5f5f7 !important;
    }

    /* Headers - Apple style */
    h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: #1d1d1f !important;
        letter-spacing: -0.02em !important;
        line-height: 1.1 !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: #1d1d1f !important;
        letter-spacing: -0.01em !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #1d1d1f !important;
        margin-top: 1.5rem !important;
    }

    /* Subtitle text */
    .main p {
        font-size: 1rem !important;
        color: #6e6e73 !important;
        line-height: 1.6 !important;
    }

    /* All text elements */
    .main div, .main span, .main label {
        color: #1d1d1f !important;
    }

    /* Markdown text */
    .main .stMarkdown {
        color: #1d1d1f !important;
    }

    /* Metrics - Card style */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #1d1d1f !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #6e6e73 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
    }

    /* Cards/Containers - removed to avoid over-styling */
    /* Individual components will have their own styling */

    /* Info boxes */
    .stAlert {
        background-color: white !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(180deg, #0071e3 0%, #005bb5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 113, 227, 0.2) !important;
    }

    .stButton > button * {
        color: white !important;
    }

    .stButton > button p {
        color: white !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3) !important;
    }

    /* Number input - fix black background issue */
    .stNumberInput > div > div {
        background-color: white !important;
    }

    .stNumberInput input[type="number"] {
        background-color: white !important;
        color: #1d1d1f !important;
    }

    /* Number input buttons (- and +) */
    .stNumberInput button {
        background-color: #e5e5e7 !important;
        color: #1d1d1f !important;
        border: none !important;
        border-radius: 6px !important;
    }

    .stNumberInput button:hover {
        background-color: #d1d1d6 !important;
    }

    .stNumberInput button * {
        color: #1d1d1f !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #fbfbfd !important;
        border-right: 1px solid #d2d2d7;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] span {
        color: #1d1d1f !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #1d1d1f !important;
    }

    /* Radio buttons */
    .stRadio > label {
        font-weight: 500 !important;
        color: #1d1d1f !important;
    }

    .stRadio label {
        color: #1d1d1f !important;
    }

    .stRadio div[role="radiogroup"] label {
        color: #1d1d1f !important;
    }

    /* Sliders */
    .stSlider > div > div > div {
        background-color: #0071e3 !important;
    }

    /* Text inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #d2d2d7 !important;
        padding: 0.5rem 0.75rem !important;
        background-color: white !important;
        color: #1d1d1f !important;
    }

    .stNumberInput input {
        color: #1d1d1f !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: white !important;
    }

    .stSelectbox input {
        background-color: white !important;
        color: #1d1d1f !important;
    }

    .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background-color: white !important;
        color: #1d1d1f !important;
    }

    /* Selectbox dropdown menu */
    [data-baseweb="popover"] {
        background-color: white !important;
    }

    [role="listbox"] {
        background-color: white !important;
    }

    [role="option"] {
        background-color: white !important;
        color: #1d1d1f !important;
    }

    [role="option"]:hover {
        background-color: #f5f5f7 !important;
    }

    /* Checkboxes */
    .stCheckbox {
        font-weight: 400 !important;
    }

    .stCheckbox label {
        color: #1d1d1f !important;
    }

    /* Input labels */
    label {
        color: #1d1d1f !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        background-color: white !important;
    }

    [data-testid="stDataFrame"] table {
        background-color: white !important;
    }

    [data-testid="stDataFrame"] th {
        background-color: #f5f5f7 !important;
        color: #1d1d1f !important;
    }

    [data-testid="stDataFrame"] td {
        background-color: white !important;
        color: #1d1d1f !important;
    }

    /* Success message */
    .stSuccess {
        background-color: #d1f4e0 !important;
        color: #0a6b32 !important;
        border-radius: 12px !important;
    }

    /* Dividers */
    hr {
        border: none !important;
        border-top: 1px solid #d2d2d7 !important;
        margin: 2rem 0 !important;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: white !important;
        color: #0071e3 !important;
        border: 1px solid #0071e3 !important;
        border-radius: 12px !important;
    }

    .stDownloadButton > button:hover {
        background-color: #f5f5f7 !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Spacing */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }

    /* Column containers */
    [data-testid="column"] {
        background-color: white;
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: white !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    /* Remove dark mode elements */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)


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

    # Title and description - Apple style
    st.markdown("""
        <h1 style='margin-bottom: 0.25rem;'>Economic Cycle Backtester.</h1>
        <p style='font-size: 1.5rem; color: #6e6e73; font-weight: 400; margin-bottom: 2rem;'>
            Test trading strategies based on Ray Dalio's economic cycle framework.
        </p>
    """, unsafe_allow_html=True)

    # Create tabs for navigation
    tab1, tab2 = st.tabs(["📈 Economic Cycle Strategy", "⚡ Swing Trading"])

    with tab1:
        show_economic_cycle_page()

    with tab2:
        show_swing_trading_page()


def show_economic_cycle_page():
    """Economic Cycle Strategy Page"""

    # Sidebar for settings
    st.sidebar.header("⚙️ Economic Cycle Settings")

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
        step=10000,
        key="economic_initial_capital"
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
                    start_str = cycle_stages.index[0].strftime('%B %d, %Y')
                    end_str = cycle_stages.index[-1].strftime('%B %d, %Y')
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

        st.dataframe(comparison_df, width='stretch')

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

    fig.update_layout(
        height=900,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1d1d1f', size=12),
        xaxis=dict(color='#1d1d1f'),
        yaxis=dict(color='#1d1d1f'),
        title_font=dict(color='#1d1d1f')
    )

    # Make all axis text dark
    fig.update_xaxes(tickfont=dict(color='#1d1d1f'), title_font=dict(color='#1d1d1f'))
    fig.update_yaxes(tickfont=dict(color='#1d1d1f'), title_font=dict(color='#1d1d1f'))

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

    fig.update_layout(
        height=700,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1d1d1f', size=12),
        xaxis=dict(color='#1d1d1f'),
        yaxis=dict(color='#1d1d1f'),
        title_font=dict(color='#1d1d1f'),
        legend=dict(
            bgcolor='white',
            bordercolor='#d2d2d7',
            borderwidth=1,
            font=dict(color='#1d1d1f')
        )
    )

    # Make all axis text and subplot titles dark
    fig.update_xaxes(tickfont=dict(color='#1d1d1f'), title_font=dict(color='#1d1d1f'))
    fig.update_yaxes(tickfont=dict(color='#1d1d1f'), title_font=dict(color='#1d1d1f'))
    fig.update_annotations(font=dict(color='#1d1d1f', size=14))

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

        st.dataframe(styled_trades, width='stretch')

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


def show_swing_trading_page():
    """Swing Trading Strategy Page"""

    st.sidebar.header("⚡ Swing Trading Settings")

    # Symbol selection
    symbol = st.sidebar.selectbox(
        "Symbol",
        config.SWING_TRADING['SYMBOLS'],
        index=0
    )

    # Backtest period
    days_back = st.sidebar.slider(
        "Backtest Period (days)",
        min_value=7,
        max_value=365,
        value=config.SWING_TRADING['BACKTEST_DAYS'],
        step=7
    )

    # Initial capital
    initial_capital = st.sidebar.number_input(
        "Initial Capital ($)",
        min_value=1000,
        max_value=10000000,
        value=30000,
        step=1000,
        key="swing_initial_capital"
    )

    st.sidebar.subheader("Technical Indicators")

    # Bollinger Bands
    bb_period = st.sidebar.slider(
        "Bollinger Bands Period",
        min_value=10,
        max_value=50,
        value=config.SWING_TRADING['BOLLINGER_PERIOD'],
        step=1
    )

    bb_std = st.sidebar.slider(
        "Bollinger Bands Std Dev",
        min_value=1.0,
        max_value=3.0,
        value=config.SWING_TRADING['BOLLINGER_STD'],
        step=0.1
    )

    # RSI
    rsi_period = st.sidebar.slider(
        "RSI Period",
        min_value=7,
        max_value=21,
        value=config.SWING_TRADING['RSI_PERIOD'],
        step=1
    )

    rsi_entry = st.sidebar.slider(
        "RSI Entry Threshold (Oversold)",
        min_value=20,
        max_value=40,
        value=config.SWING_TRADING['ENTRY_RSI_THRESHOLD'],
        step=1
    )

    rsi_exit = st.sidebar.slider(
        "RSI Exit Threshold (Overbought)",
        min_value=60,
        max_value=80,
        value=config.SWING_TRADING['RSI_OVERBOUGHT'],
        step=1
    )

    st.sidebar.subheader("Entry/Exit Rules")

    entry_condition = st.sidebar.selectbox(
        "Entry Condition",
        ["bb_rsi", "kc_rsi", "squeeze"],
        index=0,
        help="bb_rsi: Price below BB lower + RSI oversold\nkc_rsi: Price below KC lower + RSI oversold\nsqueeze: Squeeze active + conditions"
    )

    exit_condition = st.sidebar.selectbox(
        "Exit Condition",
        ["bb_upper", "bb_middle", "rsi", "kc_upper"],
        index=0,
        help="bb_upper: Price crosses BB upper band\nbb_middle: Price crosses BB middle\nrsi: RSI overbought\nkc_upper: Price crosses KC upper"
    )

    # Risk management
    st.sidebar.subheader("Risk Management")

    stop_loss_pct = st.sidebar.slider(
        "Stop Loss (%)",
        min_value=0.5,
        max_value=10.0,
        value=config.SWING_TRADING['STOP_LOSS_PCT'] * 100,
        step=0.5
    ) / 100

    use_profit_target = st.sidebar.checkbox("Use Profit Target", value=False)
    profit_target_pct = None
    if use_profit_target:
        profit_target_pct = st.sidebar.slider(
            "Profit Target (%)",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=0.5
        ) / 100

    # Economic filter
    st.sidebar.subheader("Economic Filter")
    use_economic_filter = st.sidebar.checkbox(
        "Only trade during Economic Expansion",
        value=False,
        help="Filter trades to only occur during economic expansion periods. This combines macro regime analysis with technical signals."
    )

    if use_economic_filter:
        st.sidebar.info("💡 Will fetch economic data from FRED API to identify expansion periods.")

    # Run backtest button
    run_swing_backtest = st.sidebar.button("🚀 Run Swing Backtest", type="primary")

    # Main content
    if run_swing_backtest:
        with st.spinner(f"Fetching {symbol} 30-minute data from Polygon.io..."):
            try:
                # Fetch intraday data
                fetcher = IntradayDataFetcher()
                intraday_data = fetcher.fetch_30min_bars(symbol, days_back=days_back)

                # Fetch economic data if using filter
                economic_expansion = None
                if use_economic_filter:
                    with st.spinner("Fetching economic cycle data from FRED..."):
                        try:
                            # Need more historical data for cycle classification (requires 180+ days)
                            lookback_days = max(days_back, 365)  # At least 1 year
                            start_date = (datetime.now() - pd.Timedelta(days=lookback_days)).strftime('%Y-%m-%d')
                            economic_data, _ = fetch_data(start_date)
                            cycle_stages, _ = classify_cycles(economic_data, start_date)

                            # Create expansion filter with DatetimeIndex
                            economic_expansion = (cycle_stages == 'Expansion').copy()

                            # Ensure index is DatetimeIndex
                            if not isinstance(economic_expansion.index, pd.DatetimeIndex):
                                # Try to convert to DatetimeIndex
                                try:
                                    economic_expansion.index = pd.to_datetime(economic_expansion.index)
                                except Exception as idx_err:
                                    # If conversion fails, create a new series with proper index
                                    economic_expansion = pd.Series(
                                        economic_expansion.values,
                                        index=pd.to_datetime(economic_expansion.index),
                                        name='expansion'
                                    )

                            # Sort by index to ensure asof works properly
                            economic_expansion = economic_expansion.sort_index()

                            expansion_days = economic_expansion.sum()
                            if expansion_days == 0:
                                st.warning(f"⚠️ No expansion periods detected in the data. The economic filter may prevent all trades. Consider disabling it or extending the backtest period.")
                            else:
                                st.success(f"✓ Economic cycle data loaded ({len(economic_expansion)} days, {expansion_days} expansion days)")
                        except Exception as e:
                            st.warning(f"Could not load economic data: {str(e)}. Trading without economic filter.")
                            import traceback
                            st.code(traceback.format_exc())
                            economic_expansion = None

                st.success(f"✓ Loaded {len(intraday_data)} 30-minute bars for {symbol}")

                # Initialize backtester
                backtester = SwingBacktester(intraday_data, initial_capital=initial_capital)

                # Add indicators
                indicator_config = {
                    'bb_period': bb_period,
                    'bb_std': bb_std,
                    'kc_period': config.SWING_TRADING['KELTNER_PERIOD'],
                    'kc_mult': config.SWING_TRADING['KELTNER_ATR_MULT'],
                    'rsi_period': rsi_period,
                    'atr_period': 14
                }
                backtester.add_indicators(indicator_config)

                with st.spinner("Running swing trading backtest..."):
                    # Run strategy
                    results = backtester.run_strategy(
                        entry_condition=entry_condition,
                        exit_condition=exit_condition,
                        rsi_threshold=rsi_entry,
                        rsi_exit_threshold=rsi_exit,
                        profit_target_pct=profit_target_pct,
                        stop_loss_pct=stop_loss_pct,
                        economic_expansion=economic_expansion
                    )

                # Display results
                display_swing_results(backtester, symbol)

            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    else:
        # Show instructions
        st.info("👈 Configure swing trading settings in the sidebar and click 'Run Swing Backtest'")

        st.subheader("📖 About Swing Trading Strategy")
        st.markdown("""
        This swing trading strategy uses technical indicators to identify short-term trading opportunities
        on 30-minute bars.

        **Entry Signals:**
        - **BB + RSI**: Enter when price drops below lower Bollinger Band AND RSI is oversold
        - **KC + RSI**: Enter when price drops below lower Keltner Channel AND RSI is oversold
        - **Squeeze**: Enter during a squeeze (BB inside KC) with oversold conditions

        **Exit Signals:**
        - **BB Upper**: Exit when price crosses above upper Bollinger Band
        - **BB Middle**: Exit when price returns to middle Bollinger Band
        - **RSI**: Exit when RSI becomes overbought
        - **Stop Loss**: Always active to limit downside risk

        **Optional:**
        - Filter trades to only occur during economic expansion periods
        - Set profit targets for systematic profit-taking
        """)


def display_swing_results(backtester, symbol):
    """Display swing trading backtest results"""

    st.header(f"Swing Trading Results: {symbol}")

    # Performance metrics
    st.subheader("📊 Performance Metrics")

    m = backtester.metrics

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Return", f"{m['total_return']:.2f}%")
        st.metric("Annual Return", f"{m['annual_return']:.2f}%")

    with col2:
        st.metric("Sharpe Ratio", f"{m['sharpe_ratio']:.2f}")
        st.metric("Volatility", f"{m['volatility']:.2f}%")

    with col3:
        st.metric("Max Drawdown", f"{m['max_drawdown']:.2f}%")
        st.metric("Final Value", f"${m['final_value']:,.0f}")

    with col4:
        st.metric("Total Trades", f"{int(m['total_trades'])}")
        st.metric("Win Rate", f"{m['win_rate']:.1f}%")

    # Additional trade statistics
    if m['total_trades'] > 0:
        st.subheader("📈 Trade Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Avg Win", f"{m['avg_win']:.2f}%")
        with col2:
            st.metric("Avg Loss", f"{m['avg_loss']:.2f}%")
        with col3:
            st.metric("Avg Return/Trade", f"{m['avg_return']:.2f}%")

    # Charts
    display_swing_charts(backtester, symbol)

    # Trade history
    display_swing_trades(backtester)


def display_swing_charts(backtester, symbol):
    """Display swing trading charts"""

    st.subheader("📊 Performance Charts")

    results = backtester.results

    # Create subplots
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=(
            f'{symbol} Price with Bollinger Bands',
            'RSI Indicator',
            'Equity Curve',
            'Position'
        ),
        vertical_spacing=0.08,
        row_heights=[0.3, 0.2, 0.3, 0.2]
    )

    # Plot 1: Price with Bollinger Bands
    fig.add_trace(
        go.Scatter(x=results.index, y=results['close'],
                  name='Close', line=dict(color='black', width=1)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=results.index, y=results['bb_upper'],
                  name='BB Upper', line=dict(color='red', width=1, dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=results.index, y=results['bb_middle'],
                  name='BB Middle', line=dict(color='blue', width=1, dash='dot')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=results.index, y=results['bb_lower'],
                  name='BB Lower', line=dict(color='green', width=1, dash='dash')),
        row=1, col=1
    )

    # Add buy/sell signals
    buy_signals = results[results['signal'] == 'BUY']
    sell_signals = results[results['signal'].str.contains('SELL', na=False)]

    if len(buy_signals) > 0:
        fig.add_trace(
            go.Scatter(x=buy_signals.index, y=buy_signals['close'],
                      mode='markers', name='Buy',
                      marker=dict(color='green', size=10, symbol='triangle-up')),
            row=1, col=1
        )

    if len(sell_signals) > 0:
        fig.add_trace(
            go.Scatter(x=sell_signals.index, y=sell_signals['close'],
                      mode='markers', name='Sell',
                      marker=dict(color='red', size=10, symbol='triangle-down')),
            row=1, col=1
        )

    # Plot 2: RSI
    fig.add_trace(
        go.Scatter(x=results.index, y=results['rsi'],
                  name='RSI', line=dict(color='purple', width=2)),
        row=2, col=1
    )
    # Add RSI levels
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # Plot 3: Equity curve
    fig.add_trace(
        go.Scatter(x=results.index, y=results['equity'],
                  name='Equity', line=dict(color='blue', width=2), fill='tozeroy'),
        row=3, col=1
    )

    # Plot 4: Position
    fig.add_trace(
        go.Scatter(x=results.index, y=(results['position'] > 0).astype(int),
                  name='Position', fill='tozeroy', line=dict(color='green')),
        row=4, col=1
    )

    # Update layout
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)

    # Set equity curve Y-axis range with tight padding for better visualization
    equity_min = results['equity'].min()
    equity_max = results['equity'].max()
    equity_range = equity_max - equity_min
    # Use 5% padding on each side, or minimum $2000
    padding = max(equity_range * 0.05, 2000)
    y_range = [equity_min - padding, equity_max + padding]
    fig.update_yaxes(title_text="Equity ($)", range=y_range, row=3, col=1)
    fig.update_yaxes(title_text="Position", tickvals=[0, 1], ticktext=['Out', 'In'], row=4, col=1)
    fig.update_xaxes(title_text="Time", row=4, col=1)

    fig.update_layout(
        height=1000,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1d1d1f', size=12),
        legend=dict(
            bgcolor='white',
            bordercolor='#d2d2d7',
            borderwidth=1,
            font=dict(color='#1d1d1f', size=11)
        )
    )

    # Make all axis text dark
    fig.update_xaxes(tickfont=dict(color='#1d1d1f'), title_font=dict(color='#1d1d1f'))
    fig.update_yaxes(tickfont=dict(color='#1d1d1f'), title_font=dict(color='#1d1d1f'))

    # Update subplot titles to be dark
    fig.update_annotations(font=dict(color='#1d1d1f', size=14))

    st.plotly_chart(fig, use_container_width=True)


def display_swing_trades(backtester):
    """Display swing trade history"""

    st.subheader("📝 Trade History")

    trades_df = backtester.get_trades_df()

    if len(trades_df) > 0:
        # Format display
        display_df = trades_df.copy()
        display_df['entry_time'] = pd.to_datetime(display_df['entry_time']).dt.strftime('%Y-%m-%d %H:%M')
        display_df['exit_time'] = pd.to_datetime(display_df['exit_time']).dt.strftime('%Y-%m-%d %H:%M')
        display_df['entry_price'] = display_df['entry_price'].round(2)
        display_df['exit_price'] = display_df['exit_price'].round(2)
        display_df['return_pct'] = display_df['return_pct'].round(2)
        display_df['profit'] = display_df['profit'].round(2)

        # Color code returns
        def color_returns(val):
            if isinstance(val, (int, float)):
                color = 'green' if val > 0 else 'red'
                return f'color: {color}'
            return ''

        styled_trades = display_df.style.map(
            color_returns,
            subset=['return_pct', 'profit']
        )

        st.dataframe(styled_trades, width='stretch')

        # Summary by exit reason
        st.subheader("Exit Reason Analysis")
        exit_summary = trades_df.groupby('exit_reason').agg({
            'return_pct': ['count', 'mean', 'sum'],
            'profit': 'sum'
        }).round(2)
        st.dataframe(exit_summary, width='stretch')

        # Download button
        csv = trades_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Trade History as CSV",
            data=csv,
            file_name=f"swing_trades_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No trades executed during this period")


if __name__ == "__main__":
    main()
