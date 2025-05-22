import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, time
from config import BD_TZ, RSI_UPPER, RSI_UPPER_Z, RSI_LOWER, RSI_LOWER_Z, RSI_MID

def add_session_rects(fig, slice_df: pd.DataFrame):
    def spans(start_t, end_t):
        out = []
        for d in pd.to_datetime(slice_df["time"]).dt.date.unique():
            s = BD_TZ.localize(datetime.combine(d, start_t))
            e = BD_TZ.localize(datetime.combine(
                d if end_t > start_t else d + pd.Timedelta(days=1), end_t))
            # Check overlap with slice_df time range
            if s <= slice_df["time"].iloc[-1] and e >= slice_df["time"].iloc[0]:
                out.append((s, e))
        return out

    # Session times in BD_TZ (GMT+6)
    london = spans(time(14, 0), time(23, 0))  # 14:00 to 23:00 BD_TZ (London session)
    ny = spans(time(19, 0), time(4, 0))       # 19:00 to 04:00 next day BD_TZ (NY session)

    # Map session datetime to bar_index strings for categorical x-axis
    times = slice_df["time"]

    def dt_to_bar_index(dt):
        pos = times.searchsorted(dt)
        pos = min(max(pos, 0), len(slice_df)-1)
        return str(pos)

    for x0, x1 in london:
        fig.add_vrect(
            x0=dt_to_bar_index(x0),
            x1=dt_to_bar_index(x1),
            layer="below",
            fillcolor="green",
            opacity=0.17,
            line_width=0,
            annotation_text="London",
            annotation_position="top left",
            row=1,  # restrict to main price chart
            col=1
        )

    for x0, x1 in ny:
        fig.add_vrect(
            x0=dt_to_bar_index(x0),
            x1=dt_to_bar_index(x1),
            layer="below",
            fillcolor="orange",
            opacity=0.17,
            line_width=0,
            annotation_text="NY",
            annotation_position="top left",
            row=1,  # restrict to main price chart
            col=1
        )

def create_chart(plot_df, show_rsi=False, show_ema1=False, show_ema2=False, show_ssl=False, 
                ema1_period=None, ema2_period=None, rsi_period=None, chart_h=880):
    
    row_count = 2 if show_rsi else 1
    fig = make_subplots(
        rows=row_count, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.75, 0.25] if show_rsi else [1.0],
        specs=[[{"type": "xy"}]] * row_count
    )

    # --- Main chart (Row 1) ---
    fig.add_trace(go.Candlestick(
        x=[str(i) for i in range(len(plot_df))],
        open=plot_df["open"],
        high=plot_df["high"],
        low=plot_df["low"],
        close=plot_df["close"],
        name="Price"
    ), row=1, col=1)

    if show_ema1:
        fig.add_trace(go.Scatter(
            x=[str(i) for i in range(len(plot_df))],
            y=plot_df["EMA1"],
            name=f"EMA {ema1_period}",
            line=dict(color="blue", width=1.5)
        ), row=1, col=1)

    if show_ema2:
        fig.add_trace(go.Scatter(
            x=[str(i) for i in range(len(plot_df))],
            y=plot_df["EMA2"],
            name=f"EMA {ema2_period}",
            line=dict(color="#FF8C00", width=1.5)
        ), row=1, col=1)

    if show_ssl:
        fig.add_trace(go.Scatter(
            x=[str(i) for i in range(len(plot_df))], y=plot_df["SSL_up"],
            name="SSL Up", line=dict(color="green", dash="dot")
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=[str(i) for i in range(len(plot_df))], y=plot_df["SSL_down"],
            name="SSL Down", line=dict(color="red", dash="dot")
        ), row=1, col=1)

    # --- RSI chart (Row 2) ---
    if show_rsi:
        fig.add_trace(go.Scatter(
            x=[str(i) for i in range(len(plot_df))],
            y=plot_df["RSI"],
            name=f"RSI {rsi_period}",
            line=dict(color="orange", width=1),
        ), row=2, col=1)

        # Reference lines
        fig.add_shape(type="line", x0=0, x1=len(plot_df), y0=RSI_UPPER, y1=RSI_UPPER,
                    line=dict(color="red", dash="dash", width=1), row=2, col=1)
        fig.add_shape(type="line", x0=0, x1=len(plot_df), y0=RSI_UPPER_Z, y1=RSI_UPPER_Z,
                    line=dict(color="red", dash="dash", width=1), row=2, col=1)
        
        fig.add_shape(type="line", x0=0, x1=len(plot_df), y0=RSI_LOWER, y1=RSI_LOWER,
                    line=dict(color="green", dash="dash", width=1), row=2, col=1)
        fig.add_shape(type="line", x0=0, x1=len(plot_df), y0=RSI_LOWER_Z, y1=RSI_LOWER_Z,
                    line=dict(color="green", dash="dash", width=1), row=2, col=1)
        
        fig.add_shape(type="line", x0=0, x1=len(plot_df), y0=RSI_MID, y1=RSI_MID,
                    line=dict(color="gray", dash="dash", width=1), row=2, col=1)

        fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)

    return fig