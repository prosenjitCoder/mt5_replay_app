import streamlit as st
import pandas as pd
from plotly.graph_objects import Figure
from chart_utils import create_chart, add_session_rects
from typing import Dict

def display_main_chart(plot_df: pd.DataFrame, controls: Dict) -> None:
    """Handles all chart display logic"""
    fig = create_chart(
        plot_df, 
        show_rsi=controls['show_rsi'],
        show_ema1=controls['show_ema1'],
        show_ema2=controls['show_ema2'],
        show_ssl=controls['show_ssl'],
        ema1_period=controls['ema1_period'],
        ema2_period=controls['ema2_period'],
        rsi_period=controls['rsi_period'],
        chart_h=controls['chart_h']
    )
    
    if controls['show_sessions']:
        add_session_rects(fig, plot_df)
    
    _configure_chart_layout(fig, plot_df, controls)
    _render_chart(fig)

def _configure_chart_layout(fig: Figure, plot_df: pd.DataFrame, controls: Dict) -> None:
    """Configures chart layout and appearance"""
    current_bar_time = plot_df["time"].iloc[-1] if not plot_df.empty else None
    current_bar_day = current_bar_time.strftime("%d %b %Y (%A)") if current_bar_time else "N/A"
    
    fig.update_layout(
        autosize=True,
        height=controls['chart_h'],
        xaxis_rangeslider_visible=False,
        margin=dict(t=60, b=40, l=10, r=10),
        title=_generate_chart_title(controls, current_bar_day),
        xaxis=_get_xaxis_config(plot_df)
    )

def _generate_chart_title(controls: Dict, current_day: str) -> str:
    """Generates dynamic chart title"""
    return (f"{controls['symbol']}  {controls['selected_tf_label']}  "
            f"{controls['from_date']} → {controls['to_date']}  "
            f"[GMT+6] → {current_day}")

def _get_xaxis_config(plot_df: pd.DataFrame) -> Dict:
    """Generates x-axis tick marks and labels"""
    tickvals = []
    ticktext = []
    prev_day = None
    
    for i, ts in zip(plot_df["bar_index"], plot_df["time"]):
        if prev_day != ts.date():
            tickvals.append(i)
            ticktext.append(ts.strftime("%b %d %H:%M"))
            prev_day = ts.date()
        else:
            tickvals.append(i)
            ticktext.append(ts.strftime("%H:%M"))
    
    return {
        'type': 'category',
        'tickmode': "array",
        'tickvals': [str(i) for i in range(len(plot_df))],
        'ticktext': ticktext,
        'tickangle': -45,
        'tickfont': dict(size=10),
    }

def _render_chart(fig: Figure) -> None:
    """Renders the Plotly chart with consistent config"""
    st.plotly_chart(fig, use_container_width=True, config={
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "toImage", "toggleSpikelines", "resetScale2d",
            "hoverCompareCartesian", "hoverClosestCartesian"
        ]
    })