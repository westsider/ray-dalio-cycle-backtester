# 📊 How to Run a New Backtest

This guide explains how to run the economic cycle backtest from scratch, even if you haven't touched the code in weeks/months.

---

## 🚀 Quick Start (3 Steps)

### 1. Activate Virtual Environment

```bash
cd /Users/warrenhansen/Documents/RayDalioTests
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### 2. Run the Backtest

```bash
python run_backtest.py
```

This will:
- Fetch latest economic data from FRED
- Fetch latest SPY price data from Yahoo Finance
- Classify economic cycle stages
- Run the backtest (Long SPY during Expansion, cash otherwise)
- Print performance summary
- Generate charts

### 3. View Results

The script will print results to the terminal AND create an image file.

**Open the chart:**
```bash
open backtest_results.png
```

---

## 📈 What to Look At

### Terminal Output

The terminal will show:

1. **Backtest Summary Table**
   - Total Return (Strategy vs Buy & Hold)
   - Annual Return
   - Volatility (risk)
   - Sharpe Ratio (risk-adjusted return)
   - Max Drawdown (worst loss from peak)
   - Final Portfolio Value

2. **Trading Statistics**
   - Total number of trades
   - Win rate (% of profitable trades)
   - Average win/loss per trade

3. **Recent Trades**
   - Last 10 trades with entry/exit dates and returns

### Image File: `backtest_results.png`

This chart shows 3 panels:

1. **Top Panel**: Equity curves
   - Blue line = Cycle Strategy performance
   - Gray line = Buy & Hold performance
   - Shows dollar value of portfolio over time

2. **Middle Panel**: Drawdowns
   - Shows percentage decline from peak
   - Blue = Cycle Strategy drawdown
   - Gray = Buy & Hold drawdown
   - Helps you see risk/losses during downturns

3. **Bottom Panel**: Strategy positions
   - Green shaded = Long SPY (in the market)
   - White = Cash (out of the market)
   - Shows when strategy enters/exits

---

## 🎨 Optional: View Economic Cycle Chart

Want to see the current economic cycle stage?

```bash
python example_usage.py
open economic_cycles.png
```

This shows:
- S&P 500 price history
- Economic cycle stages (Expansion, Peak, Contraction, Recovery)
- GDP growth
- Unemployment rate
- Yield curve

---

## 🔧 Troubleshooting

### Issue: "command not found: python"

Use `python3` instead:
```bash
python3 run_backtest.py
```

### Issue: "No module named 'pandas'" or similar

Your virtual environment isn't activated. Run:
```bash
source venv/bin/activate
```

### Issue: FRED API error

The API key might have expired. Get a new one at:
https://fred.stlouisfed.org/docs/api/api_key.html

Then update it in `config.py` on line 7.

### Issue: "ModuleNotFoundError"

Reinstall dependencies:
```bash
pip install -r requirements.txt
```

---

## 📊 Weekly/Monthly Workflow

### Quick Check (2 minutes)

```bash
cd /Users/warrenhansen/Documents/RayDalioTests
source venv/bin/activate
python run_backtest.py
open backtest_results.png
```

Look at:
- Current cycle stage (printed in output)
- Latest performance vs Buy & Hold
- Recent drawdown levels

### Monthly Deep Dive (5-10 minutes)

1. Run both scripts:
   ```bash
   python example_usage.py
   python run_backtest.py
   ```

2. Open both images:
   ```bash
   open economic_cycles.png
   open backtest_results.png
   ```

3. Check:
   - Did the cycle stage change this month?
   - How is the strategy performing YTD?
   - Are we in a drawdown period?
   - Any new trades executed?

4. Update `PROJECT_LOG.md` with observations

---

## 📁 Key Files Reference

| File | Purpose |
|------|---------|
| `run_backtest.py` | **Main script** - Run this for backtest results |
| `example_usage.py` | Shows economic cycle classification |
| `backtest_results.png` | **Main output** - Performance charts |
| `economic_cycles.png` | Economic indicators and cycle stages |
| `config.py` | Configuration (API key, indicators) |
| `PROJECT_LOG.md` | Track progress and notes |

---

## 💡 Tips

- **Best time to run**: Beginning of each month (after new economic data is released)
- **Data freshness**: FRED economic data updates monthly, SPY updates daily
- **Performance tracking**: Screenshot or save the results each month to compare
- **Experiment**: Edit `run_backtest.py` to test different strategies (see below)

---

## 🧪 Modifying the Strategy

Want to test different cycle stages? Edit `run_backtest.py` around line 37:

**Current (Long during Expansion only):**
```python
results = backtester.run_strategy(long_stages=['Expansion'])
```

**Try these variations:**

1. **Long during Expansion AND Recovery:**
   ```python
   results = backtester.run_strategy(long_stages=['Expansion', 'Recovery'])
   ```

2. **Long during Expansion AND Peak:**
   ```python
   results = backtester.run_strategy(long_stages=['Expansion', 'Peak'])
   ```

3. **Always invested (should match Buy & Hold):**
   ```python
   results = backtester.run_strategy(long_stages=['Expansion', 'Peak', 'Contraction', 'Recovery'])
   ```

4. **Inverse strategy (Long during Contraction only):**
   ```python
   results = backtester.run_strategy(long_stages=['Contraction'])
   ```

After editing, just run `python run_backtest.py` again to see the new results!

---

## 📞 Need Help?

- Check `README.md` for project overview
- Check `PROJECT_LOG.md` for development history
- All code is commented - read the files for details

---

**Last Updated:** 2025-10-22
