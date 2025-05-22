import streamlit as st
from typing import Dict, Any
from config import DEFAULT_SYMBOL

def initialize_app_state() -> None:
    """Initialize essential session state variables"""
    if 'symbol_names' not in st.session_state:
        st.session_state['symbol_names'] = []
    if 'prev_tf_label' not in st.session_state:
        st.session_state['prev_tf_label'] = "1H"

def handle_timeframe_change(
    symbol: str,
    prev_tf_label: str,
    selected_tf_label: str,
    from_date: str,
    to_date: str,
    screen_bars: int
) -> None:
    """Manage index preservation when timeframe changes"""
    if prev_tf_label != selected_tf_label:
        prev_df = st.session_state.get(f"df_{symbol}_{prev_tf_label}_{from_date}_{to_date}")
        if prev_df is not None and len(prev_df) > 0:
            idx_key = f"idx_{symbol}"
            old_idx = st.session_state.get(idx_key, screen_bars)
            old_idx = min(old_idx, len(prev_df))
            last_visible_time = prev_df.iloc[old_idx - 1]["time"]
            
            current_df = st.session_state.get(f"df_{symbol}_{selected_tf_label}_{from_date}_{to_date}")
            if current_df is not None:
                new_times = current_df["time"]
                new_idx = new_times.searchsorted(last_visible_time, side='right')
                if new_idx == 0:
                    new_idx = screen_bars
                st.session_state[idx_key] = min(new_idx, len(current_df))
        
        st.session_state["prev_tf_label"] = selected_tf_label

def get_current_index(symbol: str, screen_bars: int, data_length: int) -> int:
    """Get and validate the current display index"""
    idx_key = f"idx_{symbol}"
    if idx_key not in st.session_state:
        st.session_state[idx_key] = screen_bars
    return min(st.session_state[idx_key], data_length)

def update_index(symbol: str, new_index: int) -> None:
    """Update the current display index"""
    st.session_state[f"idx_{symbol}"] = new_index