FOREX REPLAY APP - TECHNICAL SUMMARY
===================================

1. CORE FUNCTIONALITY
---------------------
- Interactive candlestick chart replay system
- Connect to MetaTrader 5 for real market data
- Simulate historical market movements
- Keyboard-controlled navigation (←/→ arrows)

2. KEY FEATURES
---------------
2.1 Chart Features:
- Multiple timeframe support (1M to 1D)
- Adjustable chart height and visible candles
- Customizable technical indicators:
  * SSL Channels
  * Dual EMAs (configurable periods)
  * RSI with overbought/oversold levels
- Trading session visualization (London/NY)

2.2 Navigation Controls:
- Manual step-by-step replay (forward/backward)
- Auto-play with adjustable speed presets
- Date range selection for historical periods
- Persistent position memory per symbol/timeframe

3. TECHNICAL ARCHITECTURE
------------------------
3.1 File Structure:
app.py                - Main application entry point
├── ui/               - User interface components
│   ├── sidebar.py    - Control panel rendering
│   ├── navigation.py - Navigation logic
│   └── chart.py      - Chart visualization
└── core/             - Business logic
    ├── data.py       - Data fetching/handling
    └── state.py      - Session state management

3.2 Key Dependencies:
- Streamlit (Web Interface)
- MetaTrader5 (Data Connection)
- Plotly (Interactive Charts)
- Pandas (Data Processing)

4. SETUP REQUIREMENTS
---------------------
4.1 Prerequisites:
- MetaTrader 5 terminal installed
- Active MT5 account (demo or real)
- Python 3.8+

4.2 Configuration:
- Edit config.py for:
  * Default symbol (EURUSD)
  * Timezone settings (GMT+6)
  * Indicator parameters
  * Autoplay speed presets

5. USAGE SCENARIOS
------------------
5.1 Training:
- Practice technical analysis
- Test trading strategies
- Study market patterns

5.2 Analysis:
- Review historical price action
- Compare indicator behavior
- Analyze session overlaps

6. LIMITATIONS
--------------
- Requires MT5 terminal running
- Data quality depends on broker history
- Not optimized for mobile devices

7. FUTURE ENHANCEMENTS
----------------------
- Add more indicators (MACD, Bollinger Bands)
- Implement drawing tools
- Add trade simulation mode
- Dark/light theme toggle

8. MAINTENANCE NOTES
--------------------
- Keyboard navigation requires window focus
- Session times are hardcoded for GMT+6
- Large date ranges may impact performance

=======================