# Swing Trading Strategy Guide

## Overview

The swing trading module extends your Ray Dalio Economic Cycle Backtester with intraday trading capabilities on 30-minute bars. It uses technical indicators to identify short-term pullbacks during favorable economic conditions.

## Features

### Data Source
- **Polygon.io API** for reliable 30-minute bar data
- Historical data available (free tier has some limitations on lookback period)
- SPY and QQQ supported out of the box
- Market hours filtering (9:30 AM - 4:00 PM ET)

### Technical Indicators

#### Bollinger Bands
- Default: 20-period SMA with 2 standard deviations
- Identifies overbought/oversold conditions
- Entry signal when price drops below lower band

#### Keltner Channel
- Default: 20-period EMA with 2x ATR
- Alternative volatility-based channel
- Less sensitive to price spikes than Bollinger Bands

#### RSI (Relative Strength Index)
- Default: 14-period RSI
- Oversold threshold: 30 (entry signal)
- Overbought threshold: 70 (exit signal)
- Classic momentum oscillator

#### Additional Indicators
- **ATR (Average True Range)**: Volatility measurement
- **MACD**: Trend following indicator
- **Squeeze Indicator**: When Bollinger Bands contract inside Keltner Channel (low volatility setup)

### Entry Strategies

1. **BB + RSI** (Default)
   - Price < Lower Bollinger Band AND
   - RSI < 30 (oversold)
   - **Use case**: Mean reversion plays during pullbacks

2. **KC + RSI**
   - Price < Lower Keltner Channel AND
   - RSI < 30
   - **Use case**: More conservative entries using ATR-based bands

3. **Squeeze**
   - Bollinger Bands inside Keltner Channel AND
   - RSI < 30 AND
   - Price < Lower BB
   - **Use case**: Low volatility breakout setups

### Exit Strategies

1. **BB Upper** (Default)
   - Exit when price crosses above upper Bollinger Band
   - **Use case**: Mean reversion target

2. **BB Middle**
   - Exit when price returns to middle band (20-period MA)
   - **Use case**: Conservative profit-taking

3. **RSI Overbought**
   - Exit when RSI > 70
   - **Use case**: Momentum-based exits

4. **KC Upper**
   - Exit when price crosses upper Keltner Channel
   - **Use case**: Volatility-based targets

### Risk Management

#### Stop Loss
- Default: 2% stop loss
- Always active to limit downside
- Adjustable from 0.5% to 10%

#### Profit Targets (Optional)
- Can be enabled with custom percentage
- Systematic profit-taking
- Useful for preventing "giving back" gains

#### Economic Filter (Optional)
- Only trade during Economic Expansion periods
- Combines macro regime with technical signals
- Helps avoid trading during recessions/contractions

## How to Use

### 1. Setup
Make sure you have your Polygon API key set in `config.py`:
```python
POLYGON_API_KEY = 'your_polygon_api_key_here'
```

### 2. Run the App
```bash
streamlit run app.py
```

### 3. Navigate to Swing Trading Tab
Click on the "⚡ Swing Trading" tab at the top of the page.

### 4. Configure Settings

**Basic Settings:**
- Symbol: SPY or QQQ
- Backtest Period: 7-365 days (default: 90)
- Initial Capital: Starting equity

**Technical Indicators:**
- Bollinger Bands Period & Std Dev
- RSI Period
- Entry/Exit thresholds

**Entry/Exit Rules:**
- Entry Condition: bb_rsi, kc_rsi, or squeeze
- Exit Condition: bb_upper, bb_middle, rsi, or kc_upper

**Risk Management:**
- Stop Loss %
- Optional Profit Target
- Optional Economic Expansion Filter

### 5. Run Backtest
Click "🚀 Run Swing Backtest" to see results.

## Results Dashboard

### Performance Metrics
- Total Return
- Annualized Return
- Sharpe Ratio
- Volatility
- Max Drawdown
- Final Portfolio Value
- Total Trades
- Win Rate

### Trade Statistics
- Average Win %
- Average Loss %
- Average Return per Trade
- Best/Worst Trade

### Charts
1. **Price with Bollinger Bands**: Visual entry/exit signals
2. **RSI Indicator**: Momentum with overbought/oversold levels
3. **Equity Curve**: Portfolio growth over time
4. **Position**: When strategy is in/out of the market

### Trade History
- Complete list of all trades with:
  - Entry/Exit times
  - Entry/Exit prices
  - Return %
  - Profit/Loss
  - Exit reason (STOP_LOSS, PROFIT_TARGET, TECHNICAL, ECONOMIC)
- Exit Reason Analysis table
- Downloadable CSV export

## Strategy Ideas to Test

### 1. Conservative Mean Reversion
```
Entry: bb_rsi (price < lower BB, RSI < 30)
Exit: bb_middle (return to 20-period MA)
Stop Loss: 1.5%
Profit Target: None
Economic Filter: ON
```

### 2. Aggressive Swing
```
Entry: bb_rsi
Exit: bb_upper (ride to upper band)
Stop Loss: 3%
Profit Target: 5%
Economic Filter: OFF
```

### 3. Low Volatility Breakout
```
Entry: squeeze (BB inside KC)
Exit: kc_upper (volatility expansion)
Stop Loss: 2%
Profit Target: None
Economic Filter: ON
```

### 4. Pure Technical (No Economic Filter)
```
Entry: kc_rsi (more conservative)
Exit: rsi (momentum)
Stop Loss: 2%
Profit Target: 3%
Economic Filter: OFF
```

## Optimization Tips

1. **Backtest Period**: Start with 90 days, then expand to validate
2. **RSI Thresholds**: Try 25/75 for stricter signals, 35/65 for more trades
3. **Stop Loss**: Tighter (1-2%) for mean reversion, wider (3-5%) for trends
4. **Bollinger Period**: Shorter (15) for more reactive, longer (25) for smoother
5. **Economic Filter**: Compare with/without to see impact of macro timing

## Known Limitations

### Polygon.io Free Tier
- Rate limits: 5 calls/minute
- Historical data: Limited lookback on free tier
- The app includes delays to respect rate limits

### Market Hours
- Only trades regular market hours (9:30 AM - 4:00 PM ET)
- No pre-market or after-hours trading

### Slippage & Commissions
- Backtest assumes perfect fills at close prices
- Does not include commissions or slippage
- Real-world results will be lower

### Economic Data Frequency
- Economic indicators are daily/monthly
- Intraday bars are 30-minute
- Economic filter uses nearest available data point

## File Structure

```
intraday_fetcher.py       # Polygon.io data fetcher
technical_indicators.py   # All technical indicator calculations
swing_backtester.py       # Swing trading strategy engine
config.py                 # Configuration (add POLYGON_API_KEY here)
app.py                    # Streamlit web interface (includes swing trading tab)
```

## Next Steps

1. **Test Different Timeframes**: The code is built to support other intervals (15min, 60min)
2. **Add More Symbols**: Modify `config.SWING_TRADING['SYMBOLS']` to include other ETFs
3. **Custom Indicators**: Add your own to `technical_indicators.py`
4. **Walk-Forward Optimization**: Test parameters on rolling windows
5. **Paper Trading**: Use live data to validate signals before real money

## Questions & Suggestions

- Experiment with combining multiple entry conditions
- Try different RSI periods (9, 14, 21) for different personalities
- Test tighter stop losses during high volatility periods
- Compare results with/without the economic expansion filter

Good luck with your swing trading system!
