import streamlit as st
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
from config import TIMEFRAME_MAP
from data_fetcher import fetch_data

def fetch_and_cache_data(symbol, selected_tf_label, from_date, to_date):
    df_key = f"df_{symbol}_{selected_tf_label}_{from_date}_{to_date}"
    if df_key not in st.session_state:
        from_dt = datetime(from_date.year, from_date.month, from_date.day)
        to_dt = datetime(to_date.year, to_date.month, to_date.day, 23, 59)
        df = fetch_data(symbol, getattr(mt5, TIMEFRAME_MAP[selected_tf_label]), from_dt, to_dt)
        st.session_state[df_key] = df
    return st.session_state[df_key]

def prepare_plot_data(df, idx, screen_bars):
    start = max(0, idx - screen_bars)
    plot_df = df.iloc[start:idx].copy()
    plot_df.reset_index(drop=True, inplace=True)
    plot_df["bar_index"] = plot_df.index
    return plot_df