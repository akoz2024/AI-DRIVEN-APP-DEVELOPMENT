"""Assignment 1: Stock Analysis Streamlit App built on the Stock class.

The Stock class owns the data (download, returns, moving average, plots).
This file owns the interface. Run with: streamlit run assignment_1.py
"""
from datetime import date, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from stock import Stock

END = date.today()
START = END - timedelta(days=365)

st.set_page_config(layout="wide", page_title="Stock Analysis", page_icon="📈")
st.title("Stock Analysis")


@st.cache_data(show_spinner=False)
def load_stock(ticker, start_date, end_date, ma_window, long_window):
    """Create (and therefore download) a Stock. Cached on its arguments."""
    return Stock(ticker, start_date, end_date,
                 ma_window=ma_window, long_window=long_window)


# --- Sidebar (shared by both tabs) ---
st.sidebar.title("Inputs")
ticker = st.sidebar.text_input("Ticker symbol", value="AAPL").strip().upper()
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", START)
end_date = col2.date_input("End Date", END)
ma_window = st.sidebar.slider("Short Moving Average (days)",
                              min_value=5, max_value=200, value=20, step=1)
long_window = st.sidebar.slider("Long Moving Average (days)",
                                min_value=5, max_value=200, value=50, step=1)
if ma_window >= long_window:
    st.sidebar.warning("The short window should be smaller than the long window.")
if st.sidebar.button("Run Analysis", type="primary"):
    # A button is only True for one rerun, so remember that it was pressed
    st.session_state.run = True

if start_date >= end_date:
    st.error("Start date must be before end date.")
    st.stop()

single_tab, portfolio_tab = st.tabs(["Single Stock Analysis", "Portfolio Comparison"])

# --- Tab 1: Single Stock Analysis ---
with single_tab:
    if not st.session_state.get("run"):
        st.info("Choose a ticker in the sidebar and click **Run Analysis**.")
    else:
        with st.spinner(f"Downloading {ticker}..."):
            stock = load_stock(ticker, start_date, end_date, ma_window, long_window)

        if stock.data is None:
            st.error(stock.message)
        else:
            st.success(stock.message)
            data = stock.data

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Last Close", f"${data['Close'].iloc[-1]:,.2f}",
                      f"{data['change'].iloc[-1]:+,.2f} vs prior close")
            # return is a log return, so the sum converts to a simple return with exp
            m2.metric("Cumulative Return", f"{np.exp(data['return'].sum()) - 1:.2%}")
            m3.metric("Trading Days", len(data))
            m4.metric("Daily Volatility", f"{data['return'].std():.2%}")

            # Price chart with moving averages (not provided by the class)
            price_fig = go.Figure()
            price_fig.add_trace(go.Scatter(x=data.index, y=data['Close'],
                                           name="Close", line=dict(width=2)))
            for column, window, dash in [("MA", ma_window, "dash"),
                                         ("MA_long", long_window, "dot")]:
                # The first window - 1 rows of each MA are NaN, so drop them
                ma = data[column].dropna()
                price_fig.add_trace(go.Scatter(x=ma.index, y=ma, name=f"{window}-day MA",
                                               line=dict(width=2, dash=dash)))
            price_fig.update_layout(title=f"{stock.symbol} Close and Moving Averages",
                                    xaxis_title="Date", yaxis_title="Price ($)",
                                    hovermode="x unified")
            st.plotly_chart(price_fig, width="stretch")

            c1, c2 = st.columns(2)
            c1.plotly_chart(stock.plot_performance(), width="stretch")
            c2.plotly_chart(stock.plot_return_dist(), width="stretch")

            st.subheader("Daily Return Statistics")
            st.dataframe(data['return'].describe().to_frame("return"))

# --- Tab 2: Portfolio Comparison ---
with portfolio_tab:
    tickers_text = st.text_input("Ticker symbols (comma-separated)",
                                 value="AAPL, MSFT, GOOG")
    tickers = list(dict.fromkeys(t.strip().upper()
                                 for t in tickers_text.split(",") if t.strip()))

    returns = {}
    for symbol in tickers:
        with st.spinner(f"Downloading {symbol}..."):
            stock = load_stock(symbol, start_date, end_date, ma_window, long_window)
        if stock.data is None:
            st.error(stock.message)
            continue
        returns[symbol] = stock.data['return']

    if returns:
        # Keep only dates every ticker traded so all lines share one start date
        combined = pd.DataFrame(returns).dropna()
        # Zero-based: day one is the starting point, so its return is not counted
        combined.iloc[0] = 0.0
        performance = combined.cumsum()
        assert (performance.iloc[0] == 0.0).all()

        perf_fig = go.Figure()
        colors = px.colors.qualitative.D3
        for i, symbol in enumerate(performance.columns):
            perf_fig.add_trace(go.Scatter(x=performance.index, y=performance[symbol],
                                          name=symbol, mode="lines",
                                          line=dict(color=colors[i % len(colors)], width=2)))
        perf_fig.add_hline(y=0, line_dash="dash", line_color="gray")
        perf_fig.update_layout(title="Zero-based Cumulative Performance",
                               xaxis_title="Date", yaxis_title="Cumulative Return",
                               yaxis_tickformat=".1%", hovermode="x unified",
                               legend_title_text="Ticker")
        st.plotly_chart(perf_fig, width="stretch")
        st.caption(f"All lines start at 0.0 on {performance.index[0]:%b %d, %Y}. "
                   "Cumulative return is the running sum of daily log returns.")
    elif tickers:
        st.warning("None of the tickers could be downloaded.")
