# 📊 Ray Dalio Economic Cycle Backtest

git remote add origin https://github.com/westsider/ray-dalio-cycle-backtester.git

Build a data-driven model that detects where we are in the economic cycle (Expansion, Peak, Contraction, Recovery) and tests simple asset allocation rules.

## 🎯 Project Overview

Inspired by **Ray Dalio's framework**, this project models the economy as a cycle driven by changes in:
- Growth (GDP)
- Inflation
- Credit and interest rates
- Employment

Using public macroeconomic data (FRED) and market data (Yahoo Finance), it identifies the current stage of the cycle and backtests simple investment rules.

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a FRED API Key

1. Go to https://fred.stlouisfed.org/docs/api/api_key.html
2. Sign up for a free account
3. Get your API key
4. Set it as an environment variable:

```bash
export FRED_API_KEY='your_api_key_here'
```

Or edit `config.py` and set `FRED_API_KEY = 'your_api_key_here'`

### 3. Run the Example

```bash
python example_usage.py
```

This will:
- Fetch economic data from FRED (2000-present)
- Classify cycle stages for each time period
- Show current economic state
- Display recent cycle transitions
- Generate a visualization (`economic_cycles.png`)

## 📁 Project Structure

```
RayDalioTests/
├── config.py              # Configuration and indicator definitions
├── data_fetcher.py        # Fetches data from FRED and Yahoo Finance
├── cycle_classifier.py    # Economic cycle classification logic
├── example_usage.py       # Example script demonstrating usage
└── requirements.txt       # Python dependencies
```

## 🔍 How It Works

### Economic Indicators Used

- **Growth**: GDP, Real GDP Growth Rate
- **Inflation**: CPI, PCE Price Index
- **Employment**: Unemployment Rate, Nonfarm Payrolls
- **Credit/Rates**: Federal Funds Rate, Treasury yields, Yield Curve
- **Sentiment**: Consumer Sentiment, Manufacturing indicators

### Cycle Classification Rules

The classifier uses a rule-based approach to identify four stages:

1. **Expansion** 🟢
   - Positive GDP growth
   - Falling or low unemployment
   - Moderate inflation

2. **Peak** 🟡
   - Growth slowing
   - Inflation rising
   - Yield curve inverting

3. **Contraction** 🔴
   - Negative GDP growth
   - Rising unemployment
   - Credit tightening

4. **Recovery** 🔵
   - GDP turning positive
   - Unemployment high but falling
   - Accommodative policy

## 📈 Next Steps

- [ ] **Backtesting Engine**: Test trading strategies (long SPY in Expansion, cash otherwise)
- [ ] **Visualization Dashboard**: Interactive charts showing cycle history
- [ ] **ML Model**: Train a machine learning classifier for better predictions
- [ ] **Multiple Assets**: Add bonds, gold, commodities
- [ ] **All Weather Portfolio**: Compare against Dalio's diversified approach

## 📊 Example Output

```
Current Cycle Stage: Expansion

Recent Cycle Transitions:
Date        Stage         Previous
2020-03-15  Contraction  Expansion
2020-09-01  Recovery     Contraction
2021-03-15  Expansion    Recovery
```

## 🎓 References

- Ray Dalio's Economic Principles
- FRED Economic Data: https://fred.stlouisfed.org/
- Business Cycle Dating (NBER): https://www.nber.org/cycles/

## 📝 License

MIT - Feel free to use and modify for your own research!
