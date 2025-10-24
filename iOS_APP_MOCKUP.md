# GPIX Signal iOS App - Visual Mockup

## Main Screen (Light Mode)

```
╔═══════════════════════════════════════╗
║  ◀ GPIX              ⚙️  🔔           ║  <- Navigation bar
╠═══════════════════════════════════════╣
║                                       ║
║           ┌─────────────┐             ║
║           │             │             ║
║           │   ● BUY     │             ║  <- Large signal card
║           │             │             ║  <- Green background
║           └─────────────┘             ║
║                                       ║
║         $47.23  +$0.45 (+0.96%)      ║  <- Price info
║         Last updated: 2:30 PM         ║
║                                       ║
╠═══════════════════════════════════════╣
║  ┌───────────────────────────────┐   ║
║  │ 🟢 EXPANSION                  │   ║  <- Cycle badge
║  │ Market conditions favorable    │   ║  <- Green tinted background
║  │                            ⓘ  │   ║
║  └───────────────────────────────┘   ║
╠═══════════════════════════════════════╣
║                                       ║
║  ┌───────────────────────────────┐   ║
║  │ GPIX - 30min                  │   ║
║  │                               │   ║
║  │    48.50 ┈┈┈┈┈┈┈┈┈  (red BB)  │   ║
║  │         ╱╲    ╱╲              │   ║
║  │    48.00│╲╱  ╱  ╲──  (blue MA)│   ║  <- Price chart
║  │      ╱╲│    ╱      │          │   ║     with BB overlay
║  │    47.50│╲──╱       │          │   ║
║  │         │ ▲ BUY     │          │   ║
║  │    47.00 ┈┈┈┈┈┈┈┈┈  (green BB)│   ║
║  │                               │   ║
║  │    10:00  11:00  12:00  13:00│   ║
║  └───────────────────────────────┘   ║
║                                       ║
║  ┌───────────────────────────────┐   ║
║  │ RSI (14)                      │   ║
║  │    70 ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈       │   ║  <- RSI chart
║  │         ╱╲                    │   ║
║  │    50 ─╱──╲───────────        │   ║
║  │            ╲╱                 │   ║
║  │    30 ┈┈┈┈┈┈┈╲────────        │   ║
║  │              ▲ 28.5           │   ║
║  └───────────────────────────────┘   ║
╠═══════════════════════════════════════╣
║  ┌─────────────┬─────────────────┐   ║
║  │ BB Upper    │ RSI             │   ║
║  │ $48.45      │ 28.5            │   ║  <- Key metrics
║  ├─────────────┼─────────────────┤   ║
║  │ BB Middle   │ Position        │   ║
║  │ $47.85      │ None            │   ║
║  ├─────────────┼─────────────────┤   ║
║  │ BB Lower    │ Stop Loss       │   ║
║  │ $47.25      │ --              │   ║
║  └─────────────┴─────────────────┘   ║
╠═══════════════════════════════════════╣
║                                       ║
║      ┌─────────────────────────┐     ║
║      │   Enter Position at      │     ║  <- Action button
║      │      $47.23              │     ║  <- Green button
║      └─────────────────────────┘     ║
║                                       ║
╠═══════════════════════════════════════╣
║   📊      💼      📈      ⚙️        ║  <- Tab bar
║  Signal  Position History Settings   ║
╚═══════════════════════════════════════╝
```

## Signal States

### BUY Signal (Green Theme)
```
╔═══════════════════════════╗
║                           ║
║      ┌─────────────┐      ║
║      │   ● BUY     │      ║
║      │   Signal    │      ║  Background: Light Green (#E8F5E9)
║      └─────────────┘      ║  Text: Dark Green (#2E7D32)
║                           ║  Icon: Green circle
║   $47.23  +$0.45          ║
║                           ║
╚═══════════════════════════╝
```

### SELL Signal (Red Theme)
```
╔═══════════════════════════╗
║                           ║
║      ┌─────────────┐      ║
║      │   ● SELL    │      ║
║      │   Signal    │      ║  Background: Light Red (#FFEBEE)
║      └─────────────┘      ║  Text: Dark Red (#C62828)
║                           ║  Icon: Red circle
║   $48.85  +$2.07          ║
║                           ║
╚═══════════════════════════╝
```

### HOLD Signal (Orange Theme)
```
╔═══════════════════════════╗
║                           ║
║      ┌─────────────┐      ║
║      │   ● HOLD    │      ║
║      │  No Signal  │      ║  Background: Light Orange (#FFF3E0)
║      └─────────────┘      ║  Text: Dark Orange (#E65100)
║                           ║  Icon: Orange circle
║   $47.89  +$0.11          ║
║                           ║
╚═══════════════════════════╝
```

## Economic Cycle Badge Variations

### Expansion (Green)
```
┌─────────────────────────────────────┐
│ 🟢 EXPANSION                        │
│ GDP growing, unemployment low       │  Background: Light Green (#E8F5E9)
│                                  ⓘ │  Border: Green
└─────────────────────────────────────┘
```

### Peak (Orange/Yellow)
```
┌─────────────────────────────────────┐
│ 🟡 PEAK                             │
│ Economy at max, inflation rising    │  Background: Light Orange (#FFF3E0)
│                                  ⓘ │  Border: Orange
└─────────────────────────────────────┘
```

### Contraction (Red)
```
┌─────────────────────────────────────┐
│ 🔴 CONTRACTION                      │
│ Recession indicators active         │  Background: Light Red (#FFEBEE)
│                                  ⓘ │  Border: Red
└─────────────────────────────────────┘
```

### Recovery (Blue)
```
┌─────────────────────────────────────┐
│ 🔵 RECOVERY                         │
│ Economy rebounding from bottom      │  Background: Light Blue (#E3F2FD)
│                                  ⓘ │  Border: Blue
└─────────────────────────────────────┘
```

## Detailed View - Cycle Info Sheet (Tap on ⓘ)

```
╔═══════════════════════════════════════╗
║                                       ║
║        Economic Cycle Details         ║
║                                       ║
╠═══════════════════════════════════════╣
║  ┌───────────────────────────────┐   ║
║  │ 🟢 EXPANSION                  │   ║
║  │ Since: Jan 15, 2024           │   ║
║  │ Duration: 280 days            │   ║
║  └───────────────────────────────┘   ║
║                                       ║
║  Key Indicators:                      ║
║  ────────────────────────────────     ║
║                                       ║
║  📈 GDP Growth:          +2.5%        ║
║     Status: Positive & Growing        ║
║                                       ║
║  👥 Unemployment:        3.8%         ║
║     Status: Low & Stable              ║
║                                       ║
║  💰 Inflation Rate:      2.4%         ║
║     Status: Moderate                  ║
║                                       ║
║  📊 Yield Curve:         +0.35%       ║
║     Status: Positive (Normal)         ║
║                                       ║
║  ────────────────────────────────     ║
║                                       ║
║  What This Means:                     ║
║  • Favorable conditions for stocks    ║
║  • Economic activity growing          ║
║  • Good time for swing trading        ║
║  • Monitor for peak signals           ║
║                                       ║
║  Last Updated: 2 hours ago            ║
║                                       ║
║      ┌─────────────────────────┐     ║
║      │        Got It           │     ║
║      └─────────────────────────┘     ║
║                                       ║
╚═══════════════════════════════════════╝
```

## Position Tracking Screen

```
╔═══════════════════════════════════════╗
║  ◀ Position Details                   ║
╠═══════════════════════════════════════╣
║                                       ║
║  GPIX - Active Position               ║
║                                       ║
║  ┌───────────────────────────────┐   ║
║  │  Entry Price:      $47.23     │   ║
║  │  Current Price:    $48.15     │   ║
║  │  ────────────────────────────  │   ║
║  │  Unrealized P&L:   +$0.92     │   ║
║  │  Return:          +1.95% 📈   │   ║  Green if positive
║  └───────────────────────────────┘   ║
║                                       ║
║  Position Details:                    ║
║  ────────────────────────────────     ║
║                                       ║
║  Entry Date:     Oct 24, 2:30 PM     ║
║  Shares:         100                  ║
║  Entry Signal:   BUY (BB + RSI)       ║
║  Entry Cycle:    🟢 EXPANSION         ║
║                                       ║
║  Risk Management:                     ║
║  ────────────────────────────────     ║
║                                       ║
║  Stop Loss:      $46.28 (-2.0%)      ║
║  Distance:       -$1.87 away          ║
║                                       ║
║  Current Signal: HOLD                 ║
║  Exit Trigger:   $48.45 (BB Upper)    ║
║                                       ║
║  ┌───────────────────────────────┐   ║
║  │   [Mini Chart - Position]     │   ║
║  │                               │   ║
║  │    48.50 ┄┄┄┄┄┄┄┄┄           │   ║
║  │         ╱                     │   ║
║  │    48.00│─────── Current      │   ║
║  │      ╱  │                     │   ║
║  │    47.50│────── Entry         │   ║
║  │         │                     │   ║
║  │    47.00 ┄┄┄┄┄┄┄┄┄           │   ║
║  └───────────────────────────────┘   ║
║                                       ║
║      ┌─────────────────────────┐     ║
║      │   Exit Position at       │     ║
║      │      $48.15              │     ║  Red button
║      └─────────────────────────┘     ║
║                                       ║
╚═══════════════════════════════════════╝
```

## Trade History Screen

```
╔═══════════════════════════════════════╗
║  Trade History                        ║
╠═══════════════════════════════════════╣
║  ┌───────────────────────────────┐   ║
║  │  Total Trades:    12          │   ║
║  │  Win Rate:        66.7%       │   ║
║  │  Avg Return:      +2.3%       │   ║
║  └───────────────────────────────┘   ║
╠═══════════════════════════════════════╣
║                                       ║
║  ┌───────────────────────────────┐   ║
║  │ Oct 24, 2:30 PM → 4:45 PM     │   ║
║  │ 🟢 $47.23 → $48.85            │   ║  Green row for win
║  │ +$1.62  (+3.4%)               │   ║
║  │ Exit: BB Upper                │   ║
║  │ 🟢 EXPANSION → 🟢 EXPANSION   │   ║
║  └───────────────────────────────┘   ║
║                                       ║
║  ┌───────────────────────────────┐   ║
║  │ Oct 23, 10:00 AM → 1:15 PM    │   ║
║  │ 🔴 $46.85 → $45.92            │   ║  Red row for loss
║  │ -$0.93  (-2.0%)               │   ║
║  │ Exit: Stop Loss               │   ║
║  │ 🟢 EXPANSION → 🟡 PEAK        │   ║
║  └───────────────────────────────┘   ║
║                                       ║
║  ┌───────────────────────────────┐   ║
║  │ Oct 22, 11:30 AM → 3:00 PM    │   ║
║  │ 🟢 $47.10 → $48.25            │   ║
║  │ +$1.15  (+2.4%)               │   ║
║  │ Exit: Profit Target           │   ║
║  │ 🟢 EXPANSION → 🟢 EXPANSION   │   ║
║  └───────────────────────────────┘   ║
║                                       ║
║               ⋮                       ║
║                                       ║
╚═══════════════════════════════════════╝
```

## Settings Screen

```
╔═══════════════════════════════════════╗
║  Settings                             ║
╠═══════════════════════════════════════╣
║                                       ║
║  Technical Indicators                 ║
║  ────────────────────────────────     ║
║                                       ║
║  Bollinger Bands                      ║
║  Period:          [20]  ◀─────▶      ║
║  Std Deviation:   [2.0] ◀─────▶      ║
║                                       ║
║  RSI                                  ║
║  Period:          [14]  ◀─────▶      ║
║  Oversold:        [30]  ◀─────▶      ║
║  Overbought:      [70]  ◀─────▶      ║
║                                       ║
║  Risk Management                      ║
║  ────────────────────────────────     ║
║                                       ║
║  Stop Loss:       [2.0%] ◀─────▶     ║
║  Profit Target:   [ OFF ]            ║
║                                       ║
║  Notifications                        ║
║  ────────────────────────────────     ║
║                                       ║
║  BUY Signals      ●────────○         ║  Toggle ON
║  SELL Signals     ●────────○         ║  Toggle ON
║  Stop Loss Hit    ●────────○         ║  Toggle ON
║  Price Alerts     ○────────●         ║  Toggle OFF
║                                       ║
║  Quiet Hours:     10 PM - 7 AM       ║
║                                       ║
║  Display                              ║
║  ────────────────────────────────     ║
║                                       ║
║  Theme:           Auto               ║
║  Refresh Rate:    1 minute           ║
║  Chart Days:      5 days             ║
║                                       ║
║  Data & API                           ║
║  ────────────────────────────────     ║
║                                       ║
║  Polygon API Key: ●●●●●●●●●● [Edit]  ║
║  API Calls Today: 147 / 300          ║
║                                       ║
║  Economic Filter  ●────────○         ║  Toggle ON
║  FRED API Key:    ●●●●●●●●●● [Edit]  ║
║                                       ║
╚═══════════════════════════════════════╝
```

## Push Notification Examples

### BUY Signal Notification
```
┌─────────────────────────────────────┐
│ 📱 GPIX Signal           2:30 PM    │
├─────────────────────────────────────┤
│ 🟢 BUY Signal                       │
│                                     │
│ GPIX at $47.23                      │
│ RSI: 28.5 (Oversold)                │
│ Below BB Lower                      │
│ 🟢 Expansion                        │
└─────────────────────────────────────┘
        [View] [Dismiss]
```

### SELL Signal Notification
```
┌─────────────────────────────────────┐
│ 📱 GPIX Signal           4:45 PM    │
├─────────────────────────────────────┤
│ 🔴 SELL Signal                      │
│                                     │
│ GPIX at $48.85                      │
│ RSI: 72.3 (Overbought)              │
│ Above BB Upper                      │
│ Profit: +$1.62 (+3.4%)              │
└─────────────────────────────────────┘
        [View] [Dismiss]
```

### Stop Loss Alert
```
┌─────────────────────────────────────┐
│ 📱 GPIX Signal           11:15 AM   │
├─────────────────────────────────────┤
│ ⚠️ STOP LOSS TRIGGERED              │
│                                     │
│ GPIX at $45.92                      │
│ Entry: $46.85                       │
│ Loss: -$0.93 (-2.0%)                │
│ Consider exiting position           │
└─────────────────────────────────────┘
        [View] [Dismiss]
```

## Dark Mode Preview

```
╔═══════════════════════════════════════╗
║  ◀ GPIX              ⚙️  🔔           ║  Background: #000000
╠═══════════════════════════════════════╣  Text: #FFFFFF
║                                       ║
║           ┌─────────────┐             ║
║           │             │             ║
║           │   ● BUY     │             ║  Card: #1C1C1E
║           │             │             ║  Accent: Same colors
║           └─────────────┘             ║
║                                       ║
║         $47.23  +$0.45 (+0.96%)      ║
║         Last updated: 2:30 PM         ║
║                                       ║
╠═══════════════════════════════════════╣
║  ┌───────────────────────────────┐   ║
║  │ 🟢 EXPANSION                  │   ║  Darker tinted bg
║  │ Market conditions favorable    │   ║  Maintains colors
║  │                            ⓘ  │   ║
║  └───────────────────────────────┘   ║
╠═══════════════════════════════════════╣
║                                       ║
║       [Chart with same colors]        ║
║    (BB, RSI maintain visibility)      ║
║                                       ║
╚═══════════════════════════════════════╝
```

## Apple Watch Complication (Future)

```
┌──────────────────┐
│ GPIX             │
│ ● BUY  $47.23   │  Glanceable on watch face
│ 🟢 EXP           │  Cycle indicator
└──────────────────┘
```

## Widget (Home Screen - Future)

```
┌────────────────────────────┐
│  GPIX Signal               │
│                            │
│   ●  BUY                   │
│   $47.23  +$0.45           │
│                            │
│   🟢 EXPANSION             │
│   RSI: 28.5  BB: Below     │
│                            │
│   Updated 2 min ago        │
└────────────────────────────┘
```

---

## Design Notes

**Color Psychology:**
- 🟢 Green (Buy/Expansion): Action, Growth, Go
- 🔴 Red (Sell/Contraction): Caution, Stop, Exit
- 🟡 Orange (Hold/Peak): Warning, Attention, Pause
- 🔵 Blue (Recovery): Trust, Stability, Recovery

**Typography Hierarchy:**
- Signal Type: Large, Bold (34pt)
- Price: Medium-Large (28pt)
- Metrics: Regular (17pt)
- Details: Small (11-13pt)

**Touch Targets:**
- Buttons: Minimum 44pt height
- Cards: Tappable for details
- Charts: Interactive gestures

**Accessibility:**
- High contrast ratios (4.5:1 minimum)
- VoiceOver support for all elements
- Dynamic Type support
- Color + icon/text (not color alone)

---

This mockup shows the complete user experience with all the features we've discussed! The economic cycle badge is prominent and color-coded, providing instant context for your trading decisions. 📱✨
