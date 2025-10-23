# 🌐 How to Run the Web App

This is the **easiest way** to run your backtests. No command line commands to remember!

---

## 🚀 Quick Start (First Time Setup)

### 1. Install Streamlit (one-time only)

```bash
cd /Users/warrenhansen/Documents/RayDalioTests
source venv/bin/activate
pip install streamlit plotly
```

### 2. Launch the Web App

```bash
streamlit run app.py
```

The app will automatically open in your web browser at `http://localhost:8501`

---

## 📅 Weekly Usage (Easy!)

Every week, just run these 2 commands:

```bash
cd /Users/warrenhansen/Documents/RayDalioTests
source venv/bin/activate
streamlit run app.py
```

That's it! Your browser will open with the interactive dashboard.

---

## 🎯 How to Use the Web App

### Left Sidebar (Settings)

1. **Start Date** - Choose how far back to analyze (default: 2000)
2. **Initial Capital** - Set your starting portfolio value
3. **Strategy Selection**:
   - Original (Expansion Only)
   - Enhanced (Peak + Recovery + Stop-Loss)
   - Compare Both ← **Recommended!**
4. **Enhanced Parameters** (if applicable):
   - Stay invested during Peak? ✓
   - Include Recovery stage? ✓
   - Stop-loss percentages (sliders)

### Run the Backtest

Click the big **"🚀 Run Backtest"** button

### View Results

The app will display:

1. **Current Cycle Stage** - Where are we right now?
2. **Performance Metrics** - Returns, Sharpe ratio, drawdown, etc.
3. **Interactive Charts** - Zoom, pan, hover for details
4. **Trade History** - Every trade with dates and returns
5. **Download Button** - Export trades to CSV

---

## 🎨 Features

### Interactive Charts
- **Zoom**: Click and drag on chart
- **Pan**: Hold shift and drag
- **Hover**: See exact values at any date
- **Reset**: Double-click chart

### Comparison Mode
- See all 3 strategies side-by-side
- Winner automatically highlighted
- Visual comparison charts

### Trade Analysis
- Color-coded returns (green = profit, red = loss)
- Shows exit reasons (Cycle change vs Stop-loss)
- Download trades as CSV for further analysis

---

## 💡 Pro Tips

### Weekly Check (2 minutes)
1. Launch app: `streamlit run app.py`
2. Select "Compare Both"
3. Click "Run Backtest"
4. Check current cycle stage
5. Review latest performance

### Experiment with Settings
- Try different stop-loss percentages
- Test with/without Peak stage
- Compare different time periods
- Save screenshots of interesting results

### Data Freshness
- FRED economic data: Updates monthly
- SPY market data: Updates daily
- App caches data for 1 hour (no need to re-fetch constantly)

---

## 🔧 Troubleshooting

### App won't start?

**Check virtual environment:**
```bash
source venv/bin/activate
```

**Reinstall Streamlit:**
```bash
pip install --upgrade streamlit plotly
```

### Error: "FRED API key required"?

Your API key in `config.py` might need updating. Get a new one at:
https://fred.stlouisfed.org/docs/api/api_key.html

### Port already in use?

Someone else is using port 8501. Try a different port:
```bash
streamlit run app.py --server.port 8502
```

### Browser doesn't open automatically?

Manually go to: http://localhost:8501

---

## 📱 Bonus: Access from Other Devices

Want to check results on your phone/tablet?

1. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet "
   ```

2. Launch app with network access:
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

3. On your phone, visit: `http://YOUR_IP_ADDRESS:8501`

---

## 🆚 Web App vs Command Line

| Feature | Web App | Command Line |
|---------|---------|--------------|
| Easy to use | ✅ Click buttons | ❌ Type commands |
| Interactive charts | ✅ Zoom, hover | ❌ Static images |
| Change settings | ✅ Dropdowns/sliders | ❌ Edit code |
| No commands to remember | ✅ | ❌ |
| Perfect for weekly checks | ✅ | ❌ |

**Recommendation:** Use the web app for weekly analysis. Use command line only for development/debugging.

---

## 📸 What It Looks Like

When you run the app, you'll see:
- **Left sidebar**: All your controls and settings
- **Main area**: Current cycle stage, metrics, charts, trades
- **Interactive charts**: Click and drag to zoom
- **Clean interface**: No code, just results

---

## 🎯 Your New Weekly Workflow

**Monday morning routine (2 minutes):**

```bash
cd /Users/warrenhansen/Documents/RayDalioTests
source venv/bin/activate
streamlit run app.py
```

Then in the browser:
1. Click "Run Backtest"
2. Check current cycle stage
3. Review performance vs last week
4. Done! ✓

---

**Need help?** All your original command-line tools still work. Check `HOW_TO_RUN_BACKTEST.md` for details.

---

**Last Updated:** 2025-10-22
