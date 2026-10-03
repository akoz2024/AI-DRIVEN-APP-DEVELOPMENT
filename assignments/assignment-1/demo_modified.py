from datetime import date, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

END = date.today()
START = date.today() - timedelta(days=365)

st.set_page_config(layout="wide",
                   page_title="Stock Price Analysis", page_icon=":)")

st.title("Stock Analysis")

st.sidebar.title("Inputs")
ticker = st.sidebar.text_input("Enter stock ticker symbol",
                               value="AAPL",)
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", START)
end_date = col2.date_input("End Date", END)
mv_avg = st.sidebar.slider("Short Moving Average",
                           min_value= 1,
                           max_value= 100,
                           value= 20,
                           step= 1)
mv_avg_long = st.sidebar.slider("Long Moving Average",
                                min_value= 1,
                                max_value= 200,
                                value= 50,
                                step= 1)
run_analysis = st.sidebar.button("Run Analysis", type="primary")

@st.cache_data
def get_stock_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start_date, end_date)
        if data.empty:
            return None, f"No data for {ticker}"
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data, f"Successfully downloaded data for {ticker}"
    except Exception as e:
        return None, f"Download failed due to {e}"

if run_analysis:
    with st.spinner(f"Downloading {ticker}..."):
        data, message = get_stock_data(ticker, start_date, end_date)

    if data is None:
        st.error(message)
    else:
        st.success(message)
        df = data.copy()
        df['change'] = df['Close'] - df['Close'].shift(1)
        df['return'] = np.log(df['Close']).diff().round(4)
        df = df.dropna()
        df['MA'] = df['Close'].rolling(window=mv_avg).mean()
        df['MA_long'] = df['Close'].rolling(window=mv_avg_long).mean()

        m1, m2, m3 = st.columns(3)
        m1.metric("Last Close", f"${df['Close'].iloc[-1]:,.2f}",
                  f"{df['change'].iloc[-1]:,.2f}")
        m2.metric("Cumulative Return", f"{df['return'].sum():.2%}")
        m3.metric("Trading Days", len(df))

        fig = px.line(df, x=df.index, y=['Close', 'MA', 'MA_long'],
                      title=f"{ticker} Close with {mv_avg} and {mv_avg_long} day Moving Averages",
                      labels={'value': 'Price', 'variable': ''})
        st.plotly_chart(fig, width='stretch')

        c1, c2 = st.columns(2)
        performance = df['return'].cumsum()
        perf_fig = px.line(x=performance.index, y=performance.values,
                           title=f"Performance of {ticker}",
                           labels={'x': 'Date', 'y': 'Cum Return'})
        perf_fig.update_layout(yaxis_tickformat='.1%')
        c1.plotly_chart(perf_fig, width='stretch')

        hist_fig = px.histogram(df['return'], nbins=35,
                                title=f"Distribution of daily returns for {ticker}")
        c2.plotly_chart(hist_fig, width='stretch')

        st.subheader("Return Statistics")
        st.dataframe(df['return'].describe())
