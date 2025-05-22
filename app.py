import streamlit as st
import time as tm
from ui.sidebar import create_sidebar
from ui.navigation import create_navigation_controls
from ui.chart import display_main_chart
from core.data import fetch_and_cache_data, prepare_plot_data
from core.state import initialize_app_state, handle_timeframe_change, get_current_index
from indicators import add_emas, fetch_ssl_channel, compute_rsi
from data_fetcher import initialize_mt5, get_symbols
from config import *

def main():
    st.set_page_config(page_title="Forex Replay", layout="wide")
    
    # Initialize MT5 only once at app start
    if 'mt5_initialized' not in st.session_state:
        try:
            initialize_mt5()
            st.session_state['mt5_initialized'] = True
            st.session_state['symbol_names'] = get_symbols()
        except ConnectionError as e:
            st.error(f"❌ {str(e)}")
            st.stop()

    # UI Setup
    controls = create_sidebar()
    
    # Data Handling
    df = fetch_and_cache_data(
        controls['symbol'], 
        controls['selected_tf_label'], 
        controls['from_date'], 
        controls['to_date']
    )
    
    # State Management
    handle_timeframe_change(
        controls['symbol'],
        st.session_state.get("prev_tf_label", "1H"),
        controls['selected_tf_label'],
        controls['from_date'],
        controls['to_date'],
        controls['screen_bars']
    )
    
    # Navigation
    create_navigation_controls(controls['symbol'], controls['screen_bars'], df)
    
    # Prepare data
    idx = get_current_index(controls['symbol'], controls['screen_bars'], len(df))
    plot_df = prepare_plot_data(df, idx, controls['screen_bars'])
    
    # Calculate indicators
    plot_df = add_emas(
        plot_df, 
        controls['ema1_period'] if controls['show_ema1'] else None, 
        controls['ema2_period'] if controls['show_ema2'] else None
    )
    if controls['show_ssl']:
        plot_df["SSL_up"], plot_df["SSL_down"] = fetch_ssl_channel(plot_df)
    if controls['show_rsi']:
        plot_df["RSI"] = compute_rsi(plot_df["close"], controls['rsi_period'])
    
    # Display Chart
    display_main_chart(plot_df, controls)
    
    # Autoplay logic
# In your autoplay section:
    if controls['autoplay'] and idx < len(df):
        st.session_state[f"idx_{controls['symbol']}"] = idx + 1
        tm.sleep(SPEED_PRESETS[controls['selected_speed_label']])
        st.rerun()
        return  # Add this to prevent multiple initializations

if __name__ == "__main__":
    main()