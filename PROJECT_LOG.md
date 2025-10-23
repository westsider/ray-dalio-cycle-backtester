# Ray Dalio Economic Cycle Project - Progress Log

## Project Goal
Build a data-driven model that detects economic cycle stages (Expansion, Peak, Contraction, Recovery) and backtest asset allocation strategies.

---

## ✅ Completed Tasks

### Phase 1: Economic Model ✓ (Completed 2025-10-22)

**Files Created:**
- `config.py` - FRED API configuration and economic indicators
- `data_fetcher.py` - Data fetching from FRED and Yahoo Finance
- `cycle_classifier.py` - Rule-based economic cycle classifier
- `example_usage.py` - Demo script with visualization
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

**Achievements:**
- ✅ Set up project structure with virtual environment
- ✅ Configured FRED API key: `ebde2f9652163f7bc1694fa764f8ea44`
- ✅ Implemented data fetcher for 10+ economic indicators (GDP, inflation, unemployment, yield curve, etc.)
- ✅ Built rule-based cycle classifier with 4 stages
- ✅ Tested on historical data (2000-present)
- ✅ Created visualization with S&P 500 price + cycle stages
- ✅ Improved visualization: changed cycle stage from bar chart to line plot

**Current Model Performance:**
- Expansion: 67.6% of time
- Contraction: 16.3%
- Peak: 12.5%
- Recovery: 3.4%
- Current Stage (as of April 2025): **Expansion**

**Key Cycle Transitions Detected:**
- COVID crash: Jan 2020 (Expansion → Contraction)
- Recovery: Aug 2020 (Contraction → Expansion)
- 2022 volatility: Multiple transitions during inflation spike
- Current: Back to Expansion (April 2025)

---

### Phase 2: Backtesting Engine ✓ (Completed 2025-10-22)

**Files Created:**
- `backtester.py` - Original backtesting framework
- `run_backtest.py` - Script to run original strategy
- `backtester_enhanced.py` - Enhanced backtester with improvements
- `run_backtest_enhanced.py` - Comparison script (Original vs Enhanced)
- `HOW_TO_RUN_BACKTEST.md` - User guide for running backtests

**Achievements:**
- ✅ Created full backtesting framework with position tracking
- ✅ Implemented original strategy: Long SPY during Expansion only
- ✅ Calculated comprehensive performance metrics:
  - Total return, Annual return
  - Sharpe ratio, Volatility
  - Maximum drawdown
  - Win rate, Average win/loss
- ✅ Built comparison vs Buy & Hold SPY
- ✅ Generated visualizations: equity curves, drawdowns, positions

**Original Strategy Results (2000-2025):**
- Total Return: **619.94%**
- Annual Return: 7.98%
- Sharpe Ratio: 0.62
- Max Drawdown: -38.12%
- Total Trades: 17
- Win Rate: 70.6%

---

### Phase 3: Enhanced Strategy ✓ (Completed 2025-10-22)

**Strategy Improvements Implemented:**
1. ✅ **Peak Handling** - Stay invested during Peak (with 15% stop-loss)
2. ✅ **Recovery Inclusion** - Enter during Recovery phase
3. ✅ **Stop-Loss Protection** - Trailing stop-loss (20% Expansion, 15% Peak)
4. ✅ **Smart Exits** - Only exit on Contraction or stop-loss trigger

**Enhanced Strategy Results (2000-2025):**
- Total Return: **964.01%** (+344% vs original!)
- Annual Return: 9.63%
- Sharpe Ratio: 0.67
- Max Drawdown: -42.25%
- Total Trades: 11 (more efficient)
- Win Rate: 54.5%
- Stop-loss triggered: Only 2 times in 25 years

**Key Insights:**
- Enhanced strategy **significantly outperforms** both original and Buy & Hold
- Fewer trades but longer holding periods = better performance
- Stop-loss protection limited damage during crashes (2002, 2022)
- Staying in during Peak captured continued gains

---

### Phase 4: Web Application ✓ (Completed 2025-10-22)

**Files Created:**
- `app.py` - Streamlit web application
- `RUN_WEB_APP.md` - Complete guide for using web app
- Updated `requirements.txt` - Added streamlit and plotly

**Features:**
- ✅ Interactive web dashboard (no command line needed!)
- ✅ Click-button interface with dropdowns and sliders
- ✅ Real-time data fetching from FRED and Yahoo Finance
- ✅ Interactive Plotly charts (zoom, pan, hover)
- ✅ Strategy comparison (Original vs Enhanced vs Buy & Hold)
- ✅ Adjustable parameters:
  - Start date selection
  - Initial capital input
  - Stop-loss percentages (sliders)
  - Peak/Recovery toggle switches
- ✅ Trade history display with color-coding
- ✅ CSV download for trade data
- ✅ Current cycle stage indicator
- ✅ Data caching (1-hour) for performance

**Usage:**
```bash
streamlit run app.py
```

**Benefits:**
- No need to remember command line commands
- Easy weekly/monthly checks
- Experiment with settings instantly
- Visual, intuitive interface
- Perfect for non-technical users

---

## 📋 Future Enhancement Ideas

### Phase 5: Strategy Refinements

**Tasks:**
- [ ] Add confirmation signals (2-3 periods before entry/exit)
- [ ] Implement technical overlays (200-day MA, momentum)
- [ ] Multi-timeframe analysis (short-term vs long-term signals)
- [ ] Position sizing based on cycle confidence
- [ ] Options/hedging during Peak stages

### Phase 6: Multi-Asset Extension

**Tasks:**
- [ ] Add bonds (TLT, IEF)
- [ ] Add gold (GLD)
- [ ] Add commodities (DBC)
- [ ] Test "All Weather" style rotations
- [ ] Compare different asset allocations per cycle stage

### Phase 7: Machine Learning (Optional)

**Tasks:**
- [ ] Train ML classifier (Random Forest, XGBoost)
- [ ] Feature engineering from economic indicators
- [ ] Cross-validation for robustness
- [ ] Compare ML vs rule-based performance

---

## 🔧 Technical Setup

**Environment:**
- Python 3.x with virtual environment (`venv`)
- Location: `/Users/warrenhansen/Documents/RayDalioTests`

**Dependencies:**
- pandas, numpy
- yfinance (market data)
- fredapi (economic data)
- matplotlib (static visualization)
- streamlit (web application)
- plotly (interactive charts)
- scikit-learn (future ML)

**Data Sources:**
- FRED (Federal Reserve Economic Data)
- Yahoo Finance (SPY and other tickers)

---

## 📝 Notes & Ideas

- Consider testing on different time periods (pre-2000 data if available)
- Explore transaction costs impact on strategy
- Add regime detection beyond 4 simple stages
- Consider international markets and global indicators
- Document key economic events that match cycle transitions
- Test different stop-loss percentages systematically
- Add email/SMS alerts when cycle stage changes
- Create automated weekly report generation

---

## 🐛 Known Issues (Minor)

- Warning in `cycle_classifier.py:78`: `fillna(method='ffill')` deprecated - need to update to `.ffill()`
- Warning in `data_fetcher.py:71`: `pct_change(fill_method='pad')` deprecated
- Warnings are harmless but should be fixed for cleaner output

---

## 📊 Summary Statistics (as of 2025-10-22)

**Current Market State:**
- Cycle Stage: **Expansion**
- SPY Price: ~$650
- Data Range: 2000-2025 (25+ years)

**Strategy Performance Comparison:**
| Metric | Original | Enhanced | Buy & Hold |
|--------|----------|----------|------------|
| Total Return | 619.94% | **964.01%** | 661.31% |
| Sharpe Ratio | 0.62 | **0.67** | 0.42 |
| Max Drawdown | -38.12% | -42.25% | -55.19% |
| Total Trades | 17 | 11 | 0 |

**Winner: Enhanced Strategy** 🏆

---

## 🚀 Quick Start Commands

**Run web app (recommended):**
```bash
cd /Users/warrenhansen/Documents/RayDalioTests
source venv/bin/activate
streamlit run app.py
```

**Run command-line backtest:**
```bash
python run_backtest_enhanced.py
```

**View economic cycles:**
```bash
python example_usage.py
open economic_cycles.png
```

---

**Last Updated:** 2025-10-22
